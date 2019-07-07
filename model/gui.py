import kivy
#kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

import caesar_generator

class ThisGUI(App):
    def build(self):
        self.root = AI()
        self.root.bind(size=self._update_rect, pos=self._update_rect)
        
        with self.root.canvas.before:
            Color(.9, .9, .9, 1)
            self.rect = Rectangle(size=self.root.size, pos=self.root.pos)
        return self.root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class AI(FloatLayout):
    def train(self,a):
        tb = next( (t for t in ToggleButton.get_widgets('len') if t.state=='down'), None)
        length = int(tb.text.split()[0]) if tb else None
        for msg in caesar_generator.train(length,'eng'):
            self.status.text = msg
    def __init__(self, **kwargs):
        super(AI, self).__init__(**kwargs)
#        self.add_widget(Label(text='lang_choice'))
#        self.lang = TextInput(multiline=False)
#        self.add_widget(self.lang)
        self.len1 = ToggleButton(text='20 words', group='len', size_hint=(.1,.1), pos_hint={'right':.2,'top':.9}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len2 = ToggleButton(text='30 words', group='len', size_hint=(.1,.1), pos_hint={'right':.2,'top':.8}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len3 = ToggleButton(text='100 words', group='len', size_hint=(.1,.1), pos_hint={'right':.2,'top':.7}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len4 = ToggleButton(text='250 words', group='len', size_hint=(.1,.1), pos_hint={'right':.2,'top':.6}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len5 = ToggleButton(text='500 words', group='len', size_hint=(.1,.1), pos_hint={'right':.2,'top':.5}, background_normal='', background_color=(.6, .6, .6, 1))
        self.add_widget(self.len1)
        self.add_widget(self.len2)
        self.add_widget(self.len3)
        self.add_widget(self.len4)
        self.add_widget(self.len5)
##        self.dropdown = DropDown()
##        for length in [20, 30, 100, 250, 500]:
##            btn = Button(text='%d letters' % length, size_hint_y=None, height=44)
##            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
##            self.dropdown.add_widget(btn)
##        self.ddbutton = Button(text='Training length', size_hint=(None,None))
##        self.ddbutton.bind(on_release=self.dropdown.open)
##        self.dropdown.bind(on_select=lambda instance, x: setattr(self.ddbutton, 'text', x))
##        self.add_widget(self.ddbutton)
        self.trainbutton = Button(text='Train model', size_hint=(.25, .25), pos_hint={'center_x':.75, 'center_y':.75})
        self.trainbutton.bind(on_release=self.train)
        self.add_widget(self.trainbutton)
        self.status = Label(text='Status', size_hint=(1, .3), color=(0, 0, 0, 1))
        self.add_widget(self.status)
        self.test = Label(text='test',size_hint = (.25,.25), color = (0,0,0,1))
        self.add_widget(self.test)
        self.test.text = 'hit'
    

ThisGUI().run()
