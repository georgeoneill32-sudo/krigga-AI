from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
import requests
import json

# Set premium application dark-mode background color (#11151E)
Window.clearcolor = (0.07, 0.08, 0.12, 1)

# ⚠️ PLACE YOUR ACTUAL GOOGLE AI STUDIO API KEY HERE
API_KEY = "AQ.Ab8RN6LNJV7opi_PRbTlmjMWsqZbmSDbAUQcVpQWm5N26R8xbg"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class ChatBubble(Label):
    """A highly aesthetic message bubble with rounded corners and adaptive scaling."""
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = '15sp'
        self.color = (1, 1, 1, 1)
        self.padding = (16, 12)
        self.size_hint = (None, None)
        
        # Color definitions: Modern iOS Blue for User, Elegant Charcoal for AI
        if is_user:
            self.bg_color = (0.16, 0.50, 0.95, 1)  # #2980F6
        else:
            self.bg_color = (0.15, 0.18, 0.24, 1)  # #262E3D

        self.bind(width=self._update_canvas, height=self._update_canvas, texture_size=self._update_size)

    def _update_size(self, *args):
        """Forces crisp text wrapping up to 70% of screen width and adjusts bounding box height."""
        max_width = Window.width * 0.70
        if self.texture_size[0] > max_width:
            self.text_size = (max_width, None)
            self.width = max_width
        else:
            self.text_size = (None, None)
            self.width = self.texture_size[0] + 32
        self.height = self.texture_size[1] + 24

    def _update_canvas(self, *args):
        """Redraws smooth canvas instructions behind the label text layer."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[16, 16, 16, 16])


class MessageRow(BoxLayout):
    """A full-width invisible layout wrapper that floats chat bubbles to the right or left."""
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.padding = (12, 4)
        
        bubble = ChatBubble(text=text, is_user=is_user)
        bubble.bind(height=self._adjust_row_height)
        
        # Add layout springs using empty space filler classes
        if is_user:
            self.add_widget(Widget(size_hint_x=1))  # Push bubble right
            self.add_widget(bubble)
        else:
            self.add_widget(bubble)
            self.add_widget(Widget(size_hint_x=1))  # Push bubble left

    def _adjust_row_height(self, instance, value):
        self.height = value + 8


class KriggaAIApp(App):
    def build(self):
        self.title = "Krigga AI"
        
        # Core vertical architecture frame
        main_layout = BoxLayout(orientation='vertical', padding=(12, 16), spacing=12)
        
        # Chat History Container
        self.scroll_view = ScrollView(size_hint=(1, 0.88), do_scroll_x=False)
        self.chat_history = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        self.chat_history.bind(minimum_height=self.chat_history.setter('height'))
        self.scroll_view.add_widget(self.chat_history)
        main_layout.add_widget(self.scroll_view)
        
        # Typographic bottom dock panel container
        input_container = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10)
        
        # Beautiful clean Text Box area
        self.text_input = TextInput(
            hint_text="Message Krigga AI...",
            multiline=False,
            size_hint=(0.82, None),
            height=50,
            pos_hint={'center_y': 0.5},
            background_normal='',
            background_color=(0.15, 0.18, 0.24, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.55, 0.62, 1),
            padding=(16, 14, 16, 14),
            cursor_color=(0.16, 0.50, 0.95, 1)
        )
        self.text_input.bind(on_text_validate=self.send_message)
        
        # Clean, modern Send Button
        send_button = Button(
            text="Send",
            font_name="Roboto",
            font_size="15sp",
            bold=True,
            size_hint=(0.18, None),
            height=50,
            pos_hint={'center_y': 0.5},
            background_normal='',
            background_color=(0.16, 0.50, 0.95, 1),
            color=(1, 1, 1, 1)
        )
        send_button.bind(on_press=self.send_message)
        
        input_container.add_widget(self.text_input)
        input_container.add_widget(send_button)
        main_layout.add_widget(input_container)
        
        # Populate initial bot welcome note
        self.add_message("Hello! I am Krigga AI. How can I help you today?", is_user=False)
        return main_layout

    def add_message(self, text, is_user):
        row = MessageRow(text=text, is_user=is_user)
        self.chat_history.add_widget(row)
        
        # Smoothly scroll window down to display latest response entry
        def scroll_down(*args):
            self.scroll_view.scroll_y = 0
        from kivy.clock import Clock
        Clock.schedule_once(scroll_down, 0.1)

    def send_message(self, instance):
        user_text = self.text_input.text.strip()
        if not user_text:
            return
            
        if API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            self.add_message("System Warning: Insert your real Gemini API key string near line 14!", is_user=False)
            return

        self.add_message(user_text, is_user=True)
        self.text_input.text = ""
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_text}]
                }
            ]
        }
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                ai_response = data['candidates'][0]['content']['parts'][0]['text']
                self.add_message(ai_response, is_user=False)
            else:
                self.add_message(f"Error {response.status_code}: Server rejected request content.", is_user=False)
        except Exception as e:
            self.add_message("Connection timed out. Check your internet connectivity status.", is_user=False)


if __name__ == '__main__':
    KriggaAIApp().run()
