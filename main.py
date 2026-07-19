from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
import requests
import json

# ⚠️ PLACE YOUR ACTUAL GOOGLE AI STUDIO API KEY HERE
API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Using standard beta model endpoint route
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class ChatBubble(Label):
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.text_size = (Window.width * 0.7, None)
        self.size_hint_y = None
        self.bind(texture_size=self._update_size)
        if is_user:
            self.halign = 'right'
            self.color = (0.2, 0.6, 1, 1)
        else:
            self.halign = 'left'
            self.color = (1, 1, 1, 1)

    def _update_size(self, *args):
        self.height = self.texture_size[1] + 20

class KriggaAIApp(App):
    def build(self):
        self.title = "Krigga AI"
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.scroll_view = ScrollView(size_hint=(1, 0.85))
        self.chat_history = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.chat_history.bind(minimum_height=self.chat_history.setter('height'))
        self.scroll_view.add_widget(self.chat_history)
        main_layout.add_widget(self.scroll_view)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        self.text_input = TextInput(hint_text="Talk to Krigga AI...", multiline=False, size_hint=(0.8, 1))
        self.text_input.bind(on_text_validate=self.send_message)
        
        send_button = Button(text="Send", size_hint=(0.2, 1), background_color=(0.1, 0.7, 0.3, 1))
        send_button.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_button)
        main_layout.add_widget(input_layout)
        
        self.add_message("Hello! I am Krigga AI. How can I help you today?", is_user=False)
        return main_layout

    def add_message(self, text, is_user):
        bubble = ChatBubble(text=text, is_user=is_user)
        self.chat_history.add_widget(bubble)
        self.scroll_view.scroll_y = 0

    def send_message(self, instance):
        user_text = self.text_input.text.strip()
        if not user_text:
            return
            
        if API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            self.add_message("System Error: Please add your Gemini API key inside main.py!", is_user=False)
            return

        self.add_message(user_text, is_user=True)
        self.text_input.text = ""
        
        # Explicit role and parts structure required by Gemini API schema
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
                self.add_message(f"Error {response.status_code}: Server rejected request block.", is_user=False)
        except Exception as e:
            self.add_message("Connection timed out. Check your device internet status.", is_user=False)

if __name__ == '__main__':
    KriggaAIApp().run()
