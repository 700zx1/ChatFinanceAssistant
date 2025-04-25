from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from backend.insights import get_insight_summary
import matplotlib.pyplot as plt
import os

class InsightsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        summary = get_insight_summary()
        layout.add_widget(MDLabel(text=f"Total Suggestions: {summary['total']}", halign='center'))
        layout.add_widget(MDLabel(text=f"Accepted: {summary['accepted']}, Ignored: {summary['ignored']}, Rejected: {summary['rejected']}", halign='center'))

        self.create_pie_chart(summary)
        if os.path.exists("data/reaction_pie.png"):
            layout.add_widget(Image(source="data/reaction_pie.png", size_hint=(1, 0.8)))

        self.add_widget(layout)

    def create_pie_chart(self, summary):
        labels = ["Accepted", "Ignored", "Rejected"]
        sizes = [summary["accepted"], summary["ignored"], summary["rejected"]]
        colors = ["#4caf50", "#ffeb3b", "#f44336"]

        plt.figure(figsize=(4, 4))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors)
        plt.title("User Reactions")
        os.makedirs("data", exist_ok=True)
        plt.savefig("data/reaction_pie.png")
        plt.close()
