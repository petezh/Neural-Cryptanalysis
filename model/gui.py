import kivy
#kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import caesar_generator



class ThisGUI(App):
    def build(self):
        return AI()

class AI(GridLayout):
    def train():
        length = int(self.length.split()[0])
        for msg in caesar_generator.train():
            setattr(self.status, 'text', msg)
        
    def __init__(self, **kwargs):
        super(AI, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='lang_choice'))
        self.lang = TextInput(multiline=False)
        self.add_widget(self.lang)
        self.dropdown = DropDown()
        for length in [20, 30, 100, 250, 500]:
            btn = Button(text='%d letters' % length, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.ddbutton = Button(text='Set training length', size_hint=(None,None))
        self.ddbutton.bind(on_release=self.dropdown.open)
        self.add_widget(self.ddbutton)
        self.trainbutton = Button(text='Train model')
        self.trainbutton.bind(on_click=self.train)
        self.add_widget(self.trainbutton)
        self.status = Label(text='Status')
        self.add_widget(self.status)
        

ThisGUI().run()
