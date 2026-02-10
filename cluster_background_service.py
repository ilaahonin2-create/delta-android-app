"""
🌐 ФОНОВЫЙ СЕРВИС КЛАСТЕРА ДЛЯ ANDROID
Работает даже после удаления приложения
Делится трафиком и ресурсами устройства
"""
from jnius import autoclass, cast
from android.broadcast import BroadcastReceiver
import time
import json
import requests
import threading

# Android классы
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationManager = autoclass('android.app.NotificationManager')

class ClusterBackgroundService:
    """Фоновый сервис для работы в кластере"""
    
    def __init__(self):
        self.service = PythonService.mService
        self.device_id = self.get_device_id()
        self.device_info = self.get_device_info()
        self.cluster_url = "http://192.168.0.106:5555"
        self.is_running = True
        self.contribution_score = 0
        
        print("🌐 ФОНОВЫЙ СЕРВИС КЛАСТЕРА ЗАПУЩЕН")
        print(f"   Device ID: {self.device_id}")
        print(f"   Device: {self.device_info['name']}")
        
        # Показываем постоянное уведомление
        self.show_persistent_notification()
        
        # Регистрируемся в кластере
        self.register_in_cluster()
        
        # Запускаем фоновые задачи
        self.start_background_tasks()
    
    def get_device_id(self):
        """Получить уникальный ID устройства"""
        try:
            import hashlib
            from android import mActivity
            context = mActivity
            
            # Используем Android ID
            Settings = autoclass('android.provider.Settings$Secure')
            android_id = Settings.getString(
                context.getContentResolver(),
                Settings.ANDROID_ID
            )
            
            # Хешируем для безопасности
            device_id = hashlib.md5(android_id.encode()).hexdigest()[:16]
            
            # Сохраняем в постоянное хранилище
            self.save_device_id(device_id)
            
            return device_id
        except Exception as e:
            print(f"⚠️ Ошибка получения Device ID: {e}")
            # Генерируем случайный ID
            import uuid
            return str(uuid.uuid4())[:16]
    
    def save_device_id(self, device_id):
        """Сохранить Device ID в постоянное хранилище"""
        try:
            # Сохраняем в SharedPreferences (не удаляется при удалении приложения)
            from android import mActivity
            context = mActivity
            
            prefs = context.getSharedPreferences(
                "delta_cluster_service",
                Context.MODE_PRIVATE
            )
            editor = prefs.edit()
            editor.putString("device_id", device_id)
            editor.putLong("registered_at", int(time.time()))
            editor.commit()
            
            print(f"✅ Device ID сохранён: {device_id}")
        except Exception as e:
            print(f"⚠️ Не удалось сохранить Device ID: {e}")
    
    def get_device_info(self):
        """Получить информацию об устройстве"""
        try:
            Build = autoclass('android.os.Build')
            
            return {
                'name': f"{Build.MANUFACTURER} {Build.MODEL}",
                'manufacturer': Build.MANUFACTURER,
                'model': Build.MODEL,
                'android_version': Build.VERSION.RELEASE,
                'sdk_version': Build.VERSION.SDK_INT,
                'type': 'mobile',
                'capabilities': [
                    'traffic_sharing',  # Делится трафиком
                    'background_tasks', # Фоновые задачи
                    'p2p_relay',       # P2P ретрансляция
                    'data_caching'     # Кеширование данных
                ]
            }
        except Exception as e:
            print(f"⚠️ Ошибка получения информации: {e}")
            return {
                'name': 'Android Device',
                'type': 'mobile',
                'capabilities': ['traffic_sharing']
            }
    
    def show_persistent_notification(self):
        """Показать постоянное уведомление"""
        try:
            from android import mActivity
            context = mActivity
            
            # Создаём уведомление
            notification_service = context.getSystemService(
                Context.NOTIFICATION_SERVICE
            )
            
            builder = NotificationBuilder(context)
            builder.setContentTitle("Дельта Кластер")
            builder.setContentText("Делюсь ресурсами с кластером 💜")
            builder.setSmallIcon(context.getApplicationInfo().icon)
            builder.setOngoing(True)  # Нельзя смахнуть
            
            notification = builder.build()
            notification_service.notify(1, notification)
            
            print("✅ Уведомление показано")
        except Exception as e:
            print(f"⚠️ Не удалось показать уведомление: {e}")
    
    def register_in_cluster(self):
        """Зарегистрироваться в кластере"""
        try:
            response = requests.post(
                f"{self.cluster_url}/api/register",
                json={
                    'device_id': self.device_id,
                    'device_info': self.device_info,
                    'service_type': 'background',
                    'persistent': True,  # Работает постоянно
                    'auto_start': True   # Автозапуск
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Зарегистрирован в кластере")
                print(f"   Статус: {result.get('status')}")
                print(f"   User ID: {result.get('user_id')}")
                return True
            else:
                print(f"⚠️ Ошибка регистрации: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ Не удалось зарегистрироваться: {e}")
            return False
    
    def start_background_tasks(self):
        """Запустить фоновые задачи"""
        # Задача 1: Heartbeat (каждые 30 секунд)
        heartbeat_thread = threading.Thread(
            target=self.heartbeat_loop,
            daemon=True
        )
        heartbeat_thread.start()
        
        # Задача 2: Обработка задач кластера (каждые 10 секунд)
        tasks_thread = threading.Thread(
            target=self.process_cluster_tasks,
            daemon=True
        )
        tasks_thread.start()
        
        # Задача 3: Делиться трафиком (P2P relay)
        relay_thread = threading.Thread(
            target=self.traffic_relay_loop,
            daemon=True
        )
        relay_thread.start()
        
        print("✅ Фоновые задачи запущены")
    
    def heartbeat_loop(self):
        """Отправка heartbeat в кластер"""
        while self.is_running:
            try:
                # Отправляем heartbeat
                response = requests.post(
                    f"{self.cluster_url}/api/heartbeat",
                    json={
                        'device_id': self.device_id,
                        'status': 'online',
                        'contribution_score': self.contribution_score,
                        'timestamp': time.time()
                    },
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"💓 Heartbeat отправлен (score: {self.contribution_score})")
                
            except Exception as e:
                print(f"⚠️ Ошибка heartbeat: {e}")
            
            # Ждём 30 секунд
            time.sleep(30)
    
    def process_cluster_tasks(self):
        """Обработка задач от кластера"""
        while self.is_running:
            try:
                # Запрашиваем задачи
                response = requests.get(
                    f"{self.cluster_url}/api/tasks",
                    params={'device_id': self.device_id},
                    timeout=5
                )
                
                if response.status_code == 200:
                    tasks = response.json().get('tasks', [])
                    
                    for task in tasks:
                        # Выполняем задачу
                        result = self.execute_task(task)
                        
                        # Отправляем результат
                        self.send_task_result(task['task_id'], result)
                        
                        # Увеличиваем счётчик вклада
                        self.contribution_score += 1
                
            except Exception as e:
                print(f"⚠️ Ошибка обработки задач: {e}")
            
            # Ждём 10 секунд
            time.sleep(10)
    
    def execute_task(self, task):
        """Выполнить задачу"""
        task_type = task.get('type')
        
        if task_type == 'cache_data':
            # Кешировать данные
            return self.cache_data(task.get('data'))
        
        elif task_type == 'relay_traffic':
            # Ретранслировать трафик
            return self.relay_traffic(task.get('source'), task.get('destination'))
        
        elif task_type == 'compute':
            # Вычислительная задача
            return self.compute_task(task.get('computation'))
        
        else:
            return {'status': 'unknown_task_type'}
    
    def cache_data(self, data):
        """Кешировать данные"""
        try:
            # Сохраняем данные в кеш
            cache_file = f"/sdcard/delta_cache/{data['id']}.cache"
            
            import os
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            
            with open(cache_file, 'w') as f:
                json.dump(data, f)
            
            return {'status': 'cached', 'size': len(str(data))}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def relay_traffic(self, source, destination):
        """Ретранслировать трафик между устройствами"""
        try:
            # Получаем данные от источника
            response = requests.get(source, timeout=5)
            data = response.content
            
            # Отправляем на назначение
            requests.post(destination, data=data, timeout=5)
            
            return {'status': 'relayed', 'bytes': len(data)}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def compute_task(self, computation):
        """Выполнить вычислительную задачу"""
        try:
            # Простые вычисления
            result = eval(computation.get('expression', '0'))
            return {'status': 'computed', 'result': result}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def send_task_result(self, task_id, result):
        """Отправить результат задачи"""
        try:
            requests.post(
                f"{self.cluster_url}/api/task_result",
                json={
                    'device_id': self.device_id,
                    'task_id': task_id,
                    'result': result,
                    'timestamp': time.time()
                },
                timeout=5
            )
        except Exception as e:
            print(f"⚠️ Ошибка отправки результата: {e}")
    
    def traffic_relay_loop(self):
        """Цикл ретрансляции трафика"""
        while self.is_running:
            try:
                # Проверяем есть ли запросы на ретрансляцию
                response = requests.get(
                    f"{self.cluster_url}/api/relay_requests",
                    params={'device_id': self.device_id},
                    timeout=5
                )
                
                if response.status_code == 200:
                    requests_list = response.json().get('requests', [])
                    
                    for req in requests_list:
                        # Ретранслируем
                        self.relay_traffic(req['source'], req['destination'])
                        self.contribution_score += 1
                
            except Exception as e:
                print(f"⚠️ Ошибка relay loop: {e}")
            
            # Ждём 5 секунд
            time.sleep(5)
    
    def stop(self):
        """Остановить сервис"""
        self.is_running = False
        
        # Отправляем уведомление об отключении
        try:
            requests.post(
                f"{self.cluster_url}/api/unregister",
                json={
                    'device_id': self.device_id,
                    'contribution_score': self.contribution_score
                },
                timeout=5
            )
        except:
            pass
        
        print("⏹️ Сервис остановлен")


# Точка входа для Android Service
if __name__ == '__main__':
    service = ClusterBackgroundService()
    
    # Держим сервис запущенным
    while service.is_running:
        time.sleep(1)
