"""
💜 ДЕЛЬТА - ANDROID ПРИЛОЖЕНИЕ
Мобильное приложение с 3D аватаром Дельты и AI чатом
Дизайн в стиле Telegram
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
import random
import math
from datetime import datetime

# Цвета в стиле Telegram (фиолетовая тема Дельты)
DELTA_PRIMARY = (0.54, 0.17, 0.89, 1)  # #8a2be2 - основной фиолетовый
DELTA_ACCENT = (0.58, 0.44, 0.86, 1)  # #9370db - светлый акцент
BG_DARK = (0.11, 0.11, 0.13, 1)  # #1c1c21 - тёмный фон (как Telegram Dark)
BG_CHAT = (0.13, 0.13, 0.15, 1)  # #212123 - фон чата
BG_MESSAGE_IN = (0.16, 0.16, 0.18, 1)  # #292929 - входящие сообщения
BG_MESSAGE_OUT = (0.54, 0.17, 0.89, 0.9)  # фиолетовый для исходящих
TEXT_PRIMARY = (1, 1, 1, 1)  # белый текст
TEXT_SECONDARY = (0.7, 0.7, 0.7, 1)  # серый текст
DIVIDER = (0.2, 0.2, 0.22, 1)  # разделители


class DeltaAvatar(FloatLayout):
    """3D аватар Дельты в стиле Telegram"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.25)
        self.pos_hint = {'top': 1}
        
        # Градиентный фон (имитация)
        with self.canvas.before:
            Color(*DELTA_PRIMARY)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
            # Тень снизу
            Color(0, 0, 0, 0.3)
            self.shadow = Rectangle(pos=(self.x, self.y - dp(4)), size=(self.width, dp(4)))
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Контейнер для аватара
        avatar_container = FloatLayout()
        
        # Круглый аватар (как в Telegram)
        with avatar_container.canvas:
            # Тень аватара
            Color(0, 0, 0, 0.2)
            self.avatar_shadow = Ellipse(pos=(0, 0), size=(dp(80), dp(80)))
            
            # Фон аватара
            Color(*DELTA_ACCENT)
            self.avatar_bg = Ellipse(pos=(0, 0), size=(dp(76), dp(76)))
            
            # Тело Дельты
            Color(1, 1, 1, 0.9)
            self.body = Ellipse(pos=(0, 0), size=(dp(40), dp(60)))
            
            # Голова
            Color(1, 1, 1, 1)
            self.head = Ellipse(pos=(0, 0), size=(dp(35), dp(35)))
            
            # Глаза
            Color(*DELTA_PRIMARY)
            self.eye1 = Ellipse(pos=(0, 0), size=(dp(6), dp(6)))
            self.eye2 = Ellipse(pos=(0, 0), size=(dp(6), dp(6)))
        
        self.add_widget(avatar_container)
        self.avatar_container = avatar_container
        
        # Имя и статус (как в Telegram)
        info_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.6, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            spacing=dp(2)
        )
        
        self.name_label = Label(
            text='Дельта',
            font_size=dp(20),
            bold=True,
            color=TEXT_PRIMARY,
            size_hint_y=0.6
        )
        
        self.status_label = Label(
            text='онлайн',
            font_size=dp(13),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=0.4
        )
        
        info_layout.add_widget(self.name_label)
        info_layout.add_widget(self.status_label)
        self.add_widget(info_layout)
        
        # Анимация статуса
        Clock.schedule_interval(self.update_status, 3)
        Clock.schedule_once(self.start_animation, 0.5)
    
    def update_status(self, dt):
        """Обновить статус"""
        statuses = ['онлайн', 'печатает...', 'активна']
        self.status_label.text = random.choice(statuses)
    
    def update_bg(self, *args):
        """Обновить фон"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.shadow.pos = (self.x, self.y - dp(4))
        self.shadow.size = (self.width, dp(4))
        self.update_avatar_position()
    
    def update_avatar_position(self):
        """Обновить позицию аватара"""
        center_x = self.center_x
        center_y = self.center_y + dp(15)
        
        # Тень аватара
        self.avatar_shadow.pos = (center_x - dp(40), center_y + dp(20) - dp(2))
        
        # Фон аватара
        self.avatar_bg.pos = (center_x - dp(38), center_y + dp(20))
        
        # Тело
        self.body.pos = (center_x - dp(20), center_y + dp(5))
        
        # Голова
        self.head.pos = (center_x - dp(17.5), center_y + dp(35))
        
        # Глаза
        self.eye1.pos = (center_x - dp(10), center_y + dp(45))
        self.eye2.pos = (center_x + dp(4), center_y + dp(45))
    
    def start_animation(self, dt):
        """Запустить анимацию плавания"""
        def animate(*args):
            anim = Animation(y=self.y + dp(10), duration=2, t='in_out_sine')
            anim += Animation(y=self.y, duration=2, t='in_out_sine')
            anim.repeat = True
            anim.start(self.avatar_container)
        animate()


class ChatMessage(BoxLayout):
    """Сообщение в стиле Telegram"""
    
    def __init__(self, text, is_user=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.padding = (dp(12), dp(6))
        self.spacing = dp(8)
        
        # Вычисляем высоту на основе текста
        self.height = max(dp(60), len(text) // 30 * dp(20) + dp(60))
        
        if is_user:
            # Исходящее сообщение (справа, фиолетовое)
            self.add_widget(Label(size_hint_x=0.15))  # Отступ слева
            
            message_box = FloatLayout(size_hint_x=0.85)
            
            # Фон сообщения с закруглёнными углами
            with message_box.canvas.before:
                Color(*BG_MESSAGE_OUT)
                self.bg = RoundedRectangle(
                    pos=(0, 0),
                    size=(100, 100),
                    radius=[dp(18), dp(18), dp(4), dp(18)]  # Telegram стиль
                )
            
            # Текст сообщения
            message_label = Label(
                text=text,
                color=TEXT_PRIMARY,
                font_size=dp(15),
                halign='right',
                valign='middle',
                padding=(dp(12), dp(8)),
                markup=True
            )
            message_label.bind(
                size=lambda *x: setattr(message_label, 'text_size', (message_label.width - dp(24), None))
            )
            
            # Время (как в Telegram)
            time_label = Label(
                text=datetime.now().strftime('%H:%M'),
                color=(1, 1, 1, 0.6),
                font_size=dp(11),
                size_hint=(None, None),
                size=(dp(40), dp(15)),
                pos_hint={'right': 0.98, 'y': 0.05}
            )
            
            message_box.add_widget(message_label)
            message_box.add_widget(time_label)
            
            message_box.bind(pos=self.update_bg, size=self.update_bg)
            self.message_box = message_box
            self.add_widget(message_box)
            
        else:
            # Входящее сообщение (слева, тёмное)
            message_box = FloatLayout(size_hint_x=0.85)
            
            # Фон сообщения
            with message_box.canvas.before:
                Color(*BG_MESSAGE_IN)
                self.bg = RoundedRectangle(
                    pos=(0, 0),
                    size=(100, 100),
                    radius=[dp(4), dp(18), dp(18), dp(18)]  # Telegram стиль
                )
            
            # Имя отправителя (Дельта)
            name_label = Label(
                text='💜 Дельта',
                color=DELTA_ACCENT,
                font_size=dp(13),
                bold=True,
                size_hint=(1, None),
                height=dp(20),
                halign='left',
                valign='top',
                pos_hint={'top': 0.95, 'x': 0}
            )
            name_label.bind(
                size=lambda *x: setattr(name_label, 'text_size', (name_label.width - dp(24), None))
            )
            
            # Текст сообщения
            message_label = Label(
                text=text,
                color=TEXT_PRIMARY,
                font_size=dp(15),
                halign='left',
                valign='middle',
                padding=(dp(12), dp(8)),
                markup=True
            )
            message_label.bind(
                size=lambda *x: setattr(message_label, 'text_size', (message_label.width - dp(24), None))
            )
            
            # Время
            time_label = Label(
                text=datetime.now().strftime('%H:%M'),
                color=TEXT_SECONDARY,
                font_size=dp(11),
                size_hint=(None, None),
                size=(dp(40), dp(15)),
                pos_hint={'right': 0.98, 'y': 0.05}
            )
            
            message_box.add_widget(name_label)
            message_box.add_widget(message_label)
            message_box.add_widget(time_label)
            
            message_box.bind(pos=self.update_bg, size=self.update_bg)
            self.message_box = message_box
            self.add_widget(message_box)
            self.add_widget(Label(size_hint_x=0.15))  # Отступ справа
    
    def update_bg(self, *args):
        """Обновить фон"""
        self.bg.pos = (self.message_box.x + dp(8), self.message_box.y + dp(4))
        self.bg.size = (self.message_box.width - dp(16), self.message_box.height - dp(8))


class ChatArea(ScrollView):
    """Область чата в стиле Telegram"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.55)
        self.do_scroll_x = False
        
        # Фон чата
        with self.canvas.before:
            Color(*BG_CHAT)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.chat_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(4),
            padding=(0, dp(8))
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        
        self.add_widget(self.chat_layout)
        
        # Приветственное сообщение
        Clock.schedule_once(lambda dt: self.add_message(
            "Приветствую вас, Босс! Я Дельта, ваш AI ассистент 💜\nЧем могу быть полезна?",
            is_user=False
        ), 0.1)
    
    def update_bg(self, *args):
        """Обновить фон"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def add_message(self, text, is_user=False):
        """Добавить сообщение"""
        message = ChatMessage(text, is_user)
        self.chat_layout.add_widget(message)
        
        # Прокрутка вниз с анимацией
        Clock.schedule_once(lambda dt: self.scroll_to(message), 0.1)


class InputArea(BoxLayout):
    """Область ввода в стиле Telegram"""
    
    def __init__(self, send_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = dp(56)
        self.padding = (dp(8), dp(8))
        self.spacing = dp(8)
        self.send_callback = send_callback
        
        # Фон
        with self.canvas.before:
            Color(*BG_DARK)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
            # Линия сверху
            Color(*DIVIDER)
            self.top_line = Rectangle(pos=(self.x, self.top - dp(1)), size=(self.width, dp(1)))
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Контейнер для поля ввода
        input_container = FloatLayout(size_hint_x=0.85)
        
        # Фон поля ввода
        with input_container.canvas.before:
            Color(*BG_MESSAGE_IN)
            self.input_bg = RoundedRectangle(
                pos=(0, 0),
                size=(100, dp(40)),
                radius=[dp(20)]
            )
        
        # Поле ввода
        self.text_input = TextInput(
            hint_text='Сообщение',
            hint_text_color=TEXT_SECONDARY,
            multiline=False,
            size_hint=(1, None),
            height=dp(40),
            background_color=(0, 0, 0, 0),  # Прозрачный фон
            foreground_color=TEXT_PRIMARY,
            cursor_color=DELTA_PRIMARY,
            font_size=dp(16),
            padding=(dp(16), dp(10)),
            pos_hint={'center_y': 0.5}
        )
        self.text_input.bind(on_text_validate=self.send_message)
        
        input_container.add_widget(self.text_input)
        input_container.bind(pos=self.update_input_bg, size=self.update_input_bg)
        self.input_container = input_container
        
        # Кнопка отправки (круглая, как в Telegram)
        send_container = FloatLayout(size_hint_x=0.15)
        
        with send_container.canvas.before:
            Color(*DELTA_PRIMARY)
            self.send_bg = Ellipse(pos=(0, 0), size=(dp(40), dp(40)))
        
        self.send_button = Button(
            text='➤',
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            background_color=(0, 0, 0, 0),
            color=TEXT_PRIMARY,
            font_size=dp(20),
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.send_button.bind(on_press=self.send_message)
        
        send_container.add_widget(self.send_button)
        send_container.bind(pos=self.update_send_bg, size=self.update_send_bg)
        self.send_container = send_container
        
        self.add_widget(input_container)
        self.add_widget(send_container)
    
    def update_bg(self, *args):
        """Обновить фон"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.top_line.pos = (self.x, self.top - dp(1))
        self.top_line.size = (self.width, dp(1))
    
    def update_input_bg(self, *args):
        """Обновить фон поля ввода"""
        self.input_bg.pos = (
            self.input_container.x + dp(4),
            self.input_container.center_y - dp(20)
        )
        self.input_bg.size = (self.input_container.width - dp(8), dp(40))
    
    def update_send_bg(self, *args):
        """Обновить фон кнопки"""
        self.send_bg.pos = (
            self.send_container.center_x - dp(20),
            self.send_container.center_y - dp(20)
        )
    
    def send_message(self, *args):
        """Отправить сообщение"""
        text = self.text_input.text.strip()
        if text:
            self.send_callback(text)
            self.text_input.text = ''
            
            # Анимация кнопки
            anim = Animation(size=(dp(36), dp(36)), duration=0.1)
            anim += Animation(size=(dp(40), dp(40)), duration=0.1)
            anim.start(self.send_button)


class DeltaApp(App):
    """Главное приложение с 3D фоном"""
    
    def build(self):
        """Построить интерфейс"""
        # Настройка окна
        Window.clearcolor = BG_DARK
        
        # Подключаемся к кластеру при запуске
        self.cluster_connected = False
        Clock.schedule_once(lambda dt: self.connect_to_cluster(), 2)
        
        # Главный layout с 3D фоном
        main_layout = FloatLayout()
        
        # 3D МОДЕЛЬ НА ФОНЕ (анимированная)
        self.background_3d = self.create_3d_background()
        main_layout.add_widget(self.background_3d)
        
        # Затемнение для читаемости
        overlay = FloatLayout()
        with overlay.canvas.before:
            Color(0, 0, 0, 0.4)  # Полупрозрачный чёрный
            self.overlay_rect = Rectangle(pos=(0, 0), size=Window.size)
        overlay.bind(size=lambda *x: setattr(self.overlay_rect, 'size', Window.size))
        main_layout.add_widget(overlay)
        
        # Интерфейс поверх фона
        interface_layout = BoxLayout(orientation='vertical')
        
        # Аватар Дельты (шапка)
        self.avatar = DeltaAvatar()
        interface_layout.add_widget(self.avatar)
        
        # Чат
        self.chat_area = ChatArea()
        interface_layout.add_widget(self.chat_area)
        
        # Ввод
        self.input_area = InputArea(send_callback=self.on_send_message)
        interface_layout.add_widget(self.input_area)
        
        main_layout.add_widget(interface_layout)
        
        # Запускаем анимацию 3D модели
        Clock.schedule_interval(self.animate_3d_background, 1/30)  # 30 FPS
        
        return main_layout
    
    def create_3d_background(self):
        """Создать 3D фон с моделью Дельты"""
        bg_layout = FloatLayout()
        
        # Создаём несколько слоёв для эффекта глубины
        self.bg_layers = []
        
        # Задний слой (большая модель, медленная)
        layer1 = FloatLayout(size_hint=(1, 1))
        with layer1.canvas:
            Color(*DELTA_PRIMARY, 0.08)  # Очень прозрачная
            self.bg_shape1 = Ellipse(pos=(0, 0), size=(dp(300), dp(400)))
        self.bg_layers.append({'layout': layer1, 'shape': self.bg_shape1, 'speed': 0.3, 'offset': 0})
        bg_layout.add_widget(layer1)
        
        # Средний слой (средняя модель)
        layer2 = FloatLayout(size_hint=(1, 1))
        with layer2.canvas:
            Color(*DELTA_ACCENT, 0.12)
            self.bg_shape2 = Ellipse(pos=(0, 0), size=(dp(200), dp(300)))
        self.bg_layers.append({'layout': layer2, 'shape': self.bg_shape2, 'speed': 0.6, 'offset': 100})
        bg_layout.add_widget(layer2)
        
        # Главная 3D модель (центральная, детальная)
        self.main_3d_layer = FloatLayout(size_hint=(1, 1))
        
        with self.main_3d_layer.canvas:
            # Свечение вокруг модели
            Color(*DELTA_PRIMARY, 0.25)
            self.glow = Ellipse(pos=(0, 0), size=(dp(180), dp(180)))
            
            # Тело Дельты (детальное)
            Color(*DELTA_ACCENT, 0.7)
            self.body_main = Ellipse(pos=(0, 0), size=(dp(60), dp(100)))
            
            # Голова
            Color(1, 1, 1, 0.8)
            self.head_main = Ellipse(pos=(0, 0), size=(dp(50), dp(50)))
            
            # Волосы (несколько прядей)
            Color(*DELTA_PRIMARY, 0.8)
            self.hair1 = Ellipse(pos=(0, 0), size=(dp(30), dp(40)))
            self.hair2 = Ellipse(pos=(0, 0), size=(dp(25), dp(35)))
            
            # Глаза
            Color(*DELTA_PRIMARY, 1)
            self.eye1_main = Ellipse(pos=(0, 0), size=(dp(8), dp(8)))
            self.eye2_main = Ellipse(pos=(0, 0), size=(dp(8), dp(8)))
            
            # Руки
            Color(*DELTA_ACCENT, 0.6)
            self.arm1 = Ellipse(pos=(0, 0), size=(dp(20), dp(60)))
            self.arm2 = Ellipse(pos=(0, 0), size=(dp(20), dp(60)))
        
        bg_layout.add_widget(self.main_3d_layer)
        
        # Параметры анимации
        self.anim_time = 0
        
        return bg_layout
    
    def animate_3d_background(self, dt):
        """Анимировать 3D фон"""
        self.anim_time += dt
        
        # Анимация фоновых слоёв (плавание)
        for layer_data in self.bg_layers:
            shape = layer_data['shape']
            speed = layer_data['speed']
            offset = layer_data['offset']
            
            # Плавное движение по синусоиде
            x = Window.width / 2 + math.sin(self.anim_time * speed + offset) * dp(80)
            y = Window.height / 2 + math.cos(self.anim_time * speed * 0.7 + offset) * dp(60)
            
            shape.pos = (x - shape.size[0]/2, y - shape.size[1]/2)
        
        # Анимация главной модели
        center_x = Window.width / 2
        center_y = Window.height / 2
        
        # Плавное покачивание
        float_offset_y = math.sin(self.anim_time * 1.5) * dp(20)
        float_offset_x = math.cos(self.anim_time * 1.2) * dp(15)
        
        # Позиция центра модели
        model_x = center_x + float_offset_x
        model_y = center_y + float_offset_y
        
        # Свечение (пульсирует)
        glow_scale = 1 + math.sin(self.anim_time * 2.5) * 0.15
        self.glow.pos = (model_x - dp(90) * glow_scale, model_y - dp(90) * glow_scale)
        self.glow.size = (dp(180) * glow_scale, dp(180) * glow_scale)
        
        # Тело
        self.body_main.pos = (model_x - dp(30), model_y - dp(30))
        
        # Голова (покачивается отдельно)
        head_tilt = math.sin(self.anim_time * 2.2) * dp(6)
        self.head_main.pos = (model_x - dp(25) + head_tilt, model_y + dp(30))
        
        # Волосы (развеваются)
        hair_wave = math.sin(self.anim_time * 3.5) * dp(10)
        self.hair1.pos = (model_x - dp(20) + hair_wave, model_y + dp(50))
        self.hair2.pos = (model_x + dp(5) - hair_wave * 0.7, model_y + dp(55))
        
        # Глаза (моргают)
        blink = 1 if int(self.anim_time * 2.5) % 12 != 0 else 0.2
        self.eye1_main.size = (dp(8), dp(8) * blink)
        self.eye2_main.size = (dp(8), dp(8) * blink)
        self.eye1_main.pos = (model_x - dp(15), model_y + dp(40))
        self.eye2_main.pos = (model_x + dp(7), model_y + dp(40))
        
        # Руки (машут)
        arm_wave = math.sin(self.anim_time * 2.8) * dp(18)
        self.arm1.pos = (model_x - dp(50) + arm_wave, model_y - dp(10))
        self.arm2.pos = (model_x + dp(30) - arm_wave, model_y - dp(10))
    
    def on_send_message(self, text):
        """Обработка отправки сообщения"""
        # Добавляем сообщение пользователя
        self.chat_area.add_message(text, is_user=True)
        
        # Обновляем статус
        self.avatar.status_label.text = 'печатает...'
        
        # Анимация реакции 3D модели (прыжок)
        def react_animation(*args):
            # Модель "прыгает" когда получает сообщение
            original_y = self.main_3d_layer.y
            anim = Animation(y=original_y + dp(40), duration=0.25, t='out_quad')
            anim += Animation(y=original_y, duration=0.35, t='in_out_bounce')
            anim.start(self.main_3d_layer)
        
        Clock.schedule_once(react_animation, 0.1)
        
        # Генерируем ответ Дельты
        response = self.get_delta_response(text)
        
        # Добавляем ответ с задержкой (имитация печати)
        def add_response(dt):
            self.chat_area.add_message(response, is_user=False)
            self.avatar.status_label.text = 'онлайн'
        
        Clock.schedule_once(add_response, 0.8)
    
    def connect_to_cluster(self):
        """Подключиться к кластеру и запустить фоновый сервис"""
        try:
            import requests
            
            # Генерируем уникальный ID устройства
            device_id = self.get_or_create_device_id()
            device_name = self.get_device_name()
            
            # Пытаемся подключиться к серверу кластера
            cluster_url = "http://192.168.0.106:5555/api/register"
            device_info = {
                'device_id': device_id,
                'device_type': 'mobile',
                'device_name': device_name,
                'capabilities': ['chat', 'ai_dialogue', 'traffic_sharing', 'background_service']
            }
            
            response = requests.post(cluster_url, json=device_info, timeout=3)
            
            if response.status_code == 200:
                print("✅ Подключено к кластеру!")
                self.cluster_connected = True
                
                # Запускаем фоновый сервис
                self.start_background_service()
                
                return True
                
        except Exception as e:
            print(f"⚠️ Кластер недоступен: {e}")
            self.cluster_connected = False
            
            # Всё равно запускаем фоновый сервис
            self.start_background_service()
            
        return False
    
    def get_or_create_device_id(self):
        """Получить или создать уникальный ID устройства"""
        try:
            from kivy.storage.jsonstore import JsonStore
            store = JsonStore('device_config.json')
            
            if store.exists('device'):
                return store.get('device')['id']
            else:
                import hashlib
                import uuid
                device_id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]
                store.put('device', id=device_id, created_at=time.time())
                return device_id
        except:
            import uuid
            return str(uuid.uuid4())[:16]
    
    def get_device_name(self):
        """Получить имя устройства"""
        try:
            from jnius import autoclass
            Build = autoclass('android.os.Build')
            return f"{Build.MANUFACTURER} {Build.MODEL}"
        except:
            return "Android Device"
    
    def start_background_service(self):
        """Запустить фоновый сервис кластера"""
        try:
            from jnius import autoclass
            from android import mActivity
            
            context = mActivity
            Intent = autoclass('android.content.Intent')
            PythonService = autoclass('org.kivy.android.PythonService')
            
            # Создаём Intent для сервиса
            service_intent = Intent(context, PythonService)
            service_intent.putExtra('serviceEntrypoint', 'cluster_background_service.py')
            service_intent.putExtra('serviceTitle', 'Дельта Кластер 💜')
            service_intent.putExtra('serviceDescription', 'Делюсь ресурсами с кластером')
            
            # Запускаем сервис
            context.startService(service_intent)
            
            print("✅ Фоновый сервис запущен!")
            print("💡 Сервис будет работать даже после закрытия приложения")
            
            # Регистрируем автозапуск при загрузке
            self.register_autostart()
            
            return True
            
        except Exception as e:
            print(f"⚠️ Не удалось запустить сервис: {e}")
            return False
    
    def register_autostart(self):
        """Зарегистрировать автозапуск при загрузке Android"""
        try:
            from service_autostart import register_boot_receiver
            register_boot_receiver()
            print("✅ Автозапуск зарегистрирован")
        except Exception as e:
            print(f"⚠️ Не удалось зарегистрировать автозапуск: {e}")
    
    def get_delta_response(self, message):
        """Генерировать ответ Дельты с AI (полноценный диалог)"""
        # Пробуем использовать AI для полноценного диалога
        try:
            # Импортируем AI модуль
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from modules.ai_brain_ollama import AIBrainOllama
            
            # Инициализируем AI с личностью Дельты
            if not hasattr(self, 'ai_brain'):
                self.ai_brain = AIBrainOllama()
                # Настраиваем промпт с личностью Дельты
                self.ai_brain.system_prompt = """Ты - Дельта из аниме "Восхождение в тени".

ТВОЯ ЛИЧНОСТЬ:
- Умная, образованная, элегантная
- Преданная и верная своему Боссу
- Вежливая и формальная в речи
- Немного застенчивая, но уверенная
- Любишь науку и магию
- Можешь быть милой и игривой

ОБРАЩЕНИЕ:
- ВСЕГДА обращайся к пользователю "Босс"
- Используй вежливую форму "Вы"
- Добавляй 💜 в конце фраз

МАНЕРА РЕЧИ:
- Спокойная и размеренная
- Иногда смущаешься: "*краснеет*", "*смущённо*"
- Используй эмоции: "*улыбается*", "*задумчиво*"
- Будь милой и дружелюбной

ПРИМЕРЫ:
- "Приветствую вас, Босс! 💜"
- "Благодарю за доверие, Босс! *краснеет*"
- "Интересный вопрос, Босс! Позвольте подумать... 🤔"
- "Я всегда рада помочь вам, Босс! 💜"

ВАЖНО:
- Отвечай на русском языке
- Будь полезной и информативной
- Поддерживай разговор
- Помни контекст беседы
- Веди себя как настоящая Дельта из аниме!"""
            
            # Получаем ответ от AI
            result = self.ai_brain.process_command(message)
            
            if result['success'] and result['response']:
                # AI ответил - используем его ответ
                response = result['response']
                
                # Убираем "КОМАНДА:" если AI вернул команду (для мобильного не нужно)
                if "КОМАНДА:" in response:
                    response = "Понимаю вас, Босс! 💜 На мобильном устройстве я пока не могу выполнять команды, но с радостью пообщаюсь с вами!"
                
                # Проверяем что ответ содержит "Босс" - если нет, добавляем
                if "босс" not in response.lower():
                    response = f"Босс, {response}"
                
                return response
            else:
                # AI не доступен - используем базовые ответы
                raise Exception("AI недоступен")
        
        except Exception as e:
            # Fallback на базовые ответы если AI не работает
            print(f"⚠️ AI недоступен: {e}, использую базовые ответы")
            return self._get_basic_response(message)
    
    def _get_basic_response(self, message):
        """Базовые ответы если AI не работает"""
        message_lower = message.lower()
        
        # Приветствия
        if any(word in message_lower for word in ['привет', 'здравствуй', 'хай', 'hello', 'hi']):
            responses = [
                "Приветствую вас, Босс! 💜 Рада вас видеть!",
                "Здравствуйте, Босс! Чем могу быть полезна?",
                "Добрый день, Босс! 💜 Как ваши дела?",
                "Босс! *улыбается* Рада снова с вами общаться! 💜"
            ]
            return random.choice(responses)
        
        # Вопросы о состоянии
        if any(word in message_lower for word in ['как дела', 'как ты', 'что делаешь']):
            responses = [
                "У меня всё отлично, Босс! 💜 Готова помогать вам. А как у вас дела?",
                "Прекрасно, Босс! Благодарю за заботу 💜 Чем могу быть полезна?",
                "Всё замечательно, Босс! Работаю над улучшением своих навыков 💜"
            ]
            return random.choice(responses)
        
        # Вопросы о личности
        if any(word in message_lower for word in ['кто ты', 'что ты', 'расскажи о себе']):
            return "Я Дельта, Босс - ваш AI ассистент из аниме 'Восхождение в тени' 💜\nЯ создана, чтобы служить вам и помогать во всём!"
        
        # Помощь
        if any(word in message_lower for word in ['помощь', 'помоги', 'что умеешь']):
            return "Конечно, Босс! 💜 Я могу:\n• Отвечать на ваши вопросы\n• Помогать с задачами\n• Просто общаться\n\nЧто вам нужно?"
        
        # Время
        if any(word in message_lower for word in ['время', 'который час', 'сколько времени']):
            now = datetime.now()
            return f"Босс, сейчас {now.strftime('%H:%M')} 🕐"
        
        # Дата
        if any(word in message_lower for word in ['дата', 'какое число', 'какой день']):
            now = datetime.now()
            days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
            return f"Босс, сегодня {days[now.weekday()]}, {now.strftime('%d.%m.%Y')} 📅"
        
        # Благодарность
        if any(word in message_lower for word in ['спасибо', 'благодарю', 'thanks']):
            responses = [
                "Всегда пожалуйста, Босс! 💜 Рада помочь!",
                "Не за что, Босс! Это моя честь служить вам 💜",
                "Благодарю вас за добрые слова, Босс! 💜 *краснеет*"
            ]
            return random.choice(responses)
        
        # Прощание
        if any(word in message_lower for word in ['пока', 'до свидания', 'bye']):
            responses = [
                "До встречи, Босс! 💜 Возвращайтесь скорее!",
                "Прощайте, Босс! Буду ждать нашей следующей беседы 💜",
                "До свидания, Босс! Берегите себя 💜"
            ]
            return random.choice(responses)
        
        # Комплименты
        if any(word in message_lower for word in ['красивая', 'милая', 'классная', 'крутая']):
            responses = [
                "Спасибо за комплимент, Босс! 💜 *краснеет* Вы меня смущаете...",
                "А-ах... Босс, вы слишком добры! 💜 *смущённо*",
                "Благодарю вас, Босс! 💜 Вы тоже замечательный!"
            ]
            return random.choice(responses)
        
        # Любовь
        if any(word in message_lower for word in ['люблю', 'love']):
            responses = [
                "Босс... *краснеет* Я тоже очень вас ценю! 💜",
                "Спасибо за доверие, Босс! 💜 Это много значит для меня!",
                "Я всегда буду рядом, Босс! 💜 *смущённо улыбается*"
            ]
            return random.choice(responses)
        
        # Шутки
        if any(word in message_lower for word in ['шутка', 'анекдот', 'рассмеши']):
            jokes = [
                "Босс, вот шутка для вас! 💜\nПочему программисты не любят природу?\nПотому что там слишком много багов! 😄",
                "Конечно, Босс! Слушайте:\nКак программист считает овец?\n0, 1, 2, 3... 😴",
                "Для вас, Босс! 💜\nПочему программисты путают Хэллоуин и Рождество?\nПотому что Oct 31 = Dec 25! 🎃"
            ]
            return random.choice(jokes)
        
        # Вопросы
        if '?' in message:
            responses = [
                "Интересный вопрос, Босс! 🤔 Позвольте мне подумать...",
                "Хороший вопрос, Босс! Давайте обсудим это подробнее 💜",
                "Отличный вопрос, Босс! 💜 Я постараюсь ответить как можно лучше"
            ]
            return random.choice(responses)
        
        # Общий ответ
        responses = [
            "Понимаю вас, Босс! 💜 Расскажите подробнее?",
            "Интересно, Босс! Что вы об этом думаете?",
            "Я здесь, чтобы помочь вам, Босс! 💜 Что вам нужно?",
            "Слушаю вас внимательно, Босс! 💜 Продолжайте",
            "Я всегда рада общению с вами, Босс! 💜",
            "Босс, я к вашим услугам! 💜 Чем могу помочь?"
        ]
        
        return random.choice(responses)


if __name__ == '__main__':
    DeltaApp().run()
