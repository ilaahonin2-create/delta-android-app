"""
🚀 АВТОЗАПУСК СЕРВИСА КЛАСТЕРА
Запускается при загрузке Android
Работает даже если приложение удалено
"""
from jnius import autoclass
from android.broadcast import BroadcastReceiver

# Android классы
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')

class BootReceiver(BroadcastReceiver):
    """Получатель события загрузки системы"""
    
    def onReceive(self, context, intent):
        """Вызывается при загрузке Android"""
        if intent.getAction() == Intent.ACTION_BOOT_COMPLETED:
            print("📱 Android загружен, запускаю сервис кластера...")
            
            # Запускаем фоновый сервис
            service_intent = Intent(context, autoclass('org.kivy.android.PythonService'))
            service_intent.putExtra('serviceEntrypoint', 'cluster_background_service.py')
            service_intent.putExtra('serviceTitle', 'Дельта Кластер')
            service_intent.putExtra('serviceDescription', 'Делюсь ресурсами с кластером')
            
            context.startService(service_intent)
            
            print("✅ Сервис кластера запущен!")


def register_boot_receiver():
    """Зарегистрировать получателя события загрузки"""
    try:
        from android import mActivity
        context = mActivity
        
        # Создаём IntentFilter для BOOT_COMPLETED
        IntentFilter = autoclass('android.content.IntentFilter')
        intent_filter = IntentFilter()
        intent_filter.addAction(Intent.ACTION_BOOT_COMPLETED)
        
        # Регистрируем receiver
        receiver = BootReceiver()
        context.registerReceiver(receiver, intent_filter)
        
        print("✅ Boot receiver зарегистрирован")
        return True
        
    except Exception as e:
        print(f"⚠️ Ошибка регистрации boot receiver: {e}")
        return False


if __name__ == '__main__':
    register_boot_receiver()
