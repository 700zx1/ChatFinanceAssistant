from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivymd.uix.screenmanager import MDScreenManager, MDScreen
from kivymd.uix.screen import MDScreen
from insights_screen import InsightsScreen
from backend.voice_assistant import listen_to_user, say_response
from backend.suggestions import get_keyword_suggestion, get_time_based_prompt, get_random_fun_prompt

class ChatBubble(MDCard):
    def __init__(self, text, sender='user', **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = 0.8
        self.orientation = "vertical"
        self.padding = 10
        self.radius = [10, 10, 10, 10]
        self.md_bg_color = (0.2, 0.2, 0.2, 1) if sender == 'bot' else (0.1, 0.5, 0.8, 1)
        self.add_widget(MDLabel(text=text, theme_text_color="Custom", text_color=(1, 1, 1, 1)))

class ChatScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical')
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_area = MDBoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_area.bind(minimum_height=self.chat_area.setter('height'))
        self.scroll.add_widget(self.chat_area)

        self.input_box = MDBoxLayout(size_hint=(1, 0.15))
        self.text_input = MDTextField(hint_text="Type something...", multiline=False)
        self.send_button = MDRaisedButton(text="Send", on_release=self.on_send)
        self.voice_button = MDRaisedButton(text="Voice: OFF", on_release=self.toggle_voice)
        self.input_box.add_widget(self.text_input)
        self.input_box.add_widget(self.send_button)
        self.input_box.add_widget(self.voice_button)

        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.input_box)
        self.add_widget(self.layout)

        self.voice_enabled = False
        self.last_suggestion = None

        self.add_bot_message("Hey there! I'm your Finance Buddy. What’s on your mind today?")

    def add_user_message(self, message):
        bubble = ChatBubble(text=message, sender='user')
        self.chat_area.add_widget(bubble)

    def add_bot_message(self, message):
        bubble = ChatBubble(text=message, sender='bot')
        self.chat_area.add_widget(bubble)
        if self.voice_enabled:
            say_response(message)

    def on_send(self, instance):
        text = self.text_input.text.strip()
        if text:
            self.add_user_message(text)
            self.text_input.text = ""
            self.respond(text)

    def toggle_voice(self, *args):
        self.voice_enabled = not self.voice_enabled
        self.voice_button.text = f"Voice: {'ON' if self.voice_enabled else 'OFF'}"
        if self.voice_enabled:
            user_text = listen_to_user()
            if user_text:
                self.add_user_message(user_text)
                self.respond(user_text)

    def respond(self, text):
        suggestion = get_keyword_suggestion(text) or get_time_based_prompt() or get_random_fun_prompt()
        self.last_suggestion = suggestion
        self.add_bot_message(suggestion if suggestion else "Hmm, I'm still learning. Try asking about budgets or goals!")

class ChatFinanceApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        sm = MDScreenManager()
        sm.add_widget(ChatScreen(name="chat"))
        sm.add_widget(InsightsScreen(name="insights"))
        return sm

if __name__ == "__main__":
    ChatFinanceApp().run()
