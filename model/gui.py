"""
@author evan
"""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

import frequencydot as dot
import caesar_generator
import affine_generator

from time import sleep
def cgtrain(a,b):
    yield "1"
    #sleep(3)
    yield "2"
    #sleep(3)
    yield "3"
    #sleep(3)
    yield "4"

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
        # don't start training again with one currently active
        if self.training:
            return
        self.training = True

        # get cipher choice
        ciph_tb = next( (t for t in ToggleButton.get_widgets('ciph') if t.state=='down'), None)
        if ciph_tb == None:
            self.aistatus.text = 'Please select a cipher'
            self.training = False
            return
        cipher = ciph_tb.id

        # get length choice    
        len_tb = next( (t for t in ToggleButton.get_widgets('len') if t.state=='down'), None)
        if len_tb == None:
            self.aistatus.text = 'Please select a ciphertext length'
            self.training = False
            return
        length = int(len_tb.id)
        
# uncomment this when language works lol
##        lang_tb = next( (t for t in ToggleButton.get_widgets('lang') if t.state=='down'), None)
##        if lang_tb == None:
##            self.aistatus.text = 'Please select a language'
##            self.training = False
##            return
##        lang = lang_tb.id

        if cipher == 'caesar':
            for msg in caesar_generator.train(length, 'eng'):
                self.aistatus.text = msg + ' for ' + str(length) + ' words'
        elif cipher == 'affine':
            for msg in affine_generator.train(length, 'eng'):
                self.aistatus.text = msg + ' for ' + str(length) + ' words'
# this line is for evan who cant do anything with tf so he has to simulate the interactivity :(
        elif cipher == 'evan':
            for msg in cgtrain(length, 'eng'):
                self.aistatus.text = msg + ' for ' + str(length) + 'words'

        self.training = False

    def dot(self,a):
        if self.dotting:
            return
        self.dotting = True
        tb = next( (t for t in ToggleButton.get_widgets('len') if t.state=='down'), None)
        if tb == None:
            self.dotlabel.text = 'Please select a ciphertext length'
            self.dotting = False
            return
##        lang_tb = next( (t for t in ToggleButton.get_widgets('lang') if t.state=='down'), None)
##        if lang_tb == None:
##            self.aistatus.text = 'Please select a language'
##            self.training = False
##            return
##        lang = lang_tb.id

        results = dot.test_all()
        self.dotlabel.text = 'Frequency analysis accuracy, ' + tb.text.split()[0] + ' letters: ' + str(results)
        self.dottting = False
        
    def __init__(self, **kwargs):
        super(AI, self).__init__(**kwargs)
        self.training = False
        self.dotting = False

        self.ciph1 = ToggleButton(text='Caesar cipher', id='caesar', group='ciph', size_hint=(.1,.1), pos_hint={'center_x':.15, 'center_y':.55}, background_normal='', background_color=(.6,.6,.6,1))
        self.ciph2 = ToggleButton(text='Affine cipher', id='affine', group='ciph', size_hint=(.1,.1), pos_hint={'center_x':.15, 'center_y':.45}, background_normal='', background_color=(.6,.6,.6,1))
        self.ciph3 = ToggleButton(text='Evan\'s test', id='evan', group='ciph', size_hint=(.1,.1), pos_hint={'center_x':.15, 'center_y':.35}, background_normal='', background_color=(.6,.6,.6,1))
        self.add_widget(self.ciph1)
        self.add_widget(self.ciph2)
        self.add_widget(self.ciph3)

        self.len1 = ToggleButton(text='20 words', id='20', group='len', size_hint=(.1,.1), pos_hint={'center_x':.35,'center_y':.7}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len2 = ToggleButton(text='30 words', id='30', group='len', size_hint=(.1,.1), pos_hint={'center_x':.35,'center_y':.6}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len3 = ToggleButton(text='100 words', id='100', group='len', size_hint=(.1,.1), pos_hint={'center_x':.35,'center_y':.5}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len4 = ToggleButton(text='250 words', id='250', group='len', size_hint=(.1,.1), pos_hint={'center_x':.35,'center_y':.4}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len5 = ToggleButton(text='500 words', id='500', group='len', size_hint=(.1,.1), pos_hint={'center_x':.35,'center_y':.3}, background_normal='', background_color=(.6, .6, .6, 1))
        self.add_widget(self.len1)
        self.add_widget(self.len2)
        self.add_widget(self.len3)
        self.add_widget(self.len4)
        self.add_widget(self.len5)
        self.trainbutton = Button(text='Train model', size_hint=(.25, .15), pos_hint={'center_x':.75, 'center_y':.725})
        self.trainbutton.bind(on_release=self.train)
        self.add_widget(self.trainbutton)
        self.aistatus = Label(text='Model status', size_hint=(.25, .15), pos_hint={'center_x':.75, 'center_y':.575}, color=(0, 0, 0, 1))
        self.add_widget(self.aistatus)
        self.dotbutton = Button(text='Frequency analysis', size_hint=(.25, .15), pos_hint={'center_x':.75, 'center_y':.425})
        self.dotbutton.bind(on_release=self.dot)
        self.add_widget(self.dotbutton)
        self.dotlabel = Label(text='Frequency analysis results', size_hint=(.25, .15), pos_hint={'center_x':.75, 'center_y':.275}, color=(0,0,0,1))
        self.add_widget(self.dotlabel)
    

ThisGUI().run()
