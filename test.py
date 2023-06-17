import os
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class GameApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.total_levels = 3
        self.max_level = self.load_progress()

        play_button = Button(text="Play", on_release=self.start_game)
        self.add_widget(play_button)

        levels_button = Button(text="Levels", on_release=self.show_levels)
        self.add_widget(levels_button)

    def load_level(self, level):
        level_dir = f"levels/level{level}"
        answer_file = os.path.join(level_dir, "answer.txt")
        image_file = os.path.join(level_dir, "image.png")
        hint_file = os.path.join(level_dir, "hint.txt")

        with open(answer_file, "r") as f:
            self.correct_answer = f.read().strip()

        self.image = Image(source=image_file, size_hint=(None, None), size=(300, 300))
        self.add_widget(self.image)

        with open(hint_file, "r") as f:
            self.hint_text = f.read().strip()

    def save_progress(self, level):
        data = {"max_level": level}
        with open("progress.json", "w") as f:
            json.dump(data, f)

    def load_progress(self):
        if os.path.exists("progress.json"):
            with open("progress.json", "r") as f:
                data = json.load(f)
                return data.get("max_level", 1)
        return 1

    def start_game(self, *args):
        self.clear_widgets()

        level_label = Label(text=f"Level: {self.max_level}", font_size=18)
        self.add_widget(level_label)

        back_button = Button(text="Back", on_release=self.go_back, font_size=16)
        self.add_widget(back_button)

        conditions_label = Label(text="Game conditions", font_size=16)
        self.add_widget(conditions_label)

        self.load_level(self.max_level)

        self.answer_entry = TextInput(font_size=16)
        self.add_widget(self.answer_entry)

        check_button = Button(text="Check", on_release=self.check_answer, font_size=16)
        self.add_widget(check_button)

        hint_button = Button(text="Hint", on_release=self.show_hint, font_size=16)
        self.add_widget(hint_button)

    def go_back(self, *args):
        self.clear_widgets()
        self.__init__()

    def check_answer(self, *args):
        answer = self.answer_entry.text
        if answer == self.correct_answer:
            self.max_level += 1
            if self.max_level > self.total_levels:
                self.max_level = self.total_levels
                popup = Popup(title="Congratulations!", content=Label(text="Great, you completed all levels"),
                              size_hint=(None, None), size=(400, 200))
                popup.open()
            else:
                self.save_progress(self.max_level)
                popup = Popup(title="Congratulations!", content=Label(text="You completed the level!"),
                              size_hint=(None, None), size=(400, 200))
                popup.open()
        else:
            popup = Popup(title="Incorrect Answer", content=Label(text="Try again!"), size_hint=(None, None),
                          size=(400, 200))
            popup.open()

    def show_hint(self, *args):
        hint_popup = Popup(title="Hint", content=Label(text=self.hint_text), size_hint=(None, None), size=(400, 200))
        hint_popup.open()

    def show_levels(self, *args):
        self.clear_widgets()

        levels_label = Label(text=f"Total Levels: {self.total_levels}", font_size=18)
        self.add_widget(levels_label)

        for level in range(1, self.total_levels + 1):
            level_button = Button(text=str(level), on_release=lambda lvl=level: self.select_level(lvl), font_size=16)
            self.add_widget(level_button)

            if level <= self.max_level:
                level_button.background_color = (0, 1, 0, 1)  # Зеленый цвет для пройденных уровней

        back_button_levels = Button(text="Back", on_release=self.go_back, font_size=16)
        self.add_widget(back_button_levels)

    def select_level(self, level_button):
        level = int(level_button.text)
        self.max_level = level
        self.start_game()


class GameKivyApp(App):
    def build(self):
        return GameApp()


if __name__ == '__main__':
    GameKivyApp().run()
