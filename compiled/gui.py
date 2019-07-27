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
from kivy.properties import StringProperty
import threading
import os.path


from time import sleep
def cgtrain():
    yield "1"
    sleep(1)
    yield "2"
    sleep(1)
    yield "3"
    sleep(1)
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

    def file_checker(self, ciph, length, lang):
        return os.path.exists(lang + '_' + str(length) + '_' + ciph[0:3] + '.csv')

    def train_helper(self, not_used):
        threading.Thread(target=self.train).start()
    def train(self):
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
        ciph = ciph_tb.id

##        if cipher == 'affine':
##            self.aistatus.text = 'Affine not yet implemented with the GUI.'
##            self.training = False
##            return

        # get length choice    
        len_tb = next( (t for t in ToggleButton.get_widgets('len') if t.state=='down'), None)
        if len_tb == None:
            self.aistatus.text = 'Please select a ciphertext length'
            self.training = False
            return
        length = int(len_tb.id)
        
        lang_tb = next( (t for t in ToggleButton.get_widgets('lang') if t.state=='down'), None)
        if lang_tb == None:
            self.aistatus.text = 'Please select a language'
            self.training = False
            return
        lang = lang_tb.id

        self.aistatus.text = 'Checking necessary files...'
        files = self.file_checker(ciph, length, lang)
        if files:
            self.aistatus.text = 'Files exist. Moving directly to training...'
        else:
            self.aistatus.text = 'Files do not exist. Generating necessary files...'
        sleep(1)

        if ciph == 'evan':
            for msg in cgtrain():
                self.aistatus.text = msg
            self.training = False
            return
        
        import generator
        import train
        
        # actual work begins here
        languages = {'eng': 'English', 'span': 'Spanish', 'fren': 'French'}
        self.aistatus.text = 'Creating snippets in ' + languages[lang] + '...'
        generator.generate(length, lang)
        self.aistatus.text = 'Snippets created. Encrypting snippets for testing...'
        generator.encrypt(length, lang, ciph)
        self.aistatus.text = 'Encryption complete. Advancing to neural network.'
        for msg in train.train(length, lang, ciph):
            self.aistatus.text = msg
        self.training = False

    def dot_helper(self, not_used):
        threading.Thread(target=self.dot).start()

    def dot(self):
        if self.dotting:
            return
        self.dotting = True

        ciph_tb = next( (t for t in ToggleButton.get_widgets('ciph') if t.state=='down'), None)
        if ciph_tb == None:
            self.dotlabel.text = 'Please select a cipher'
            self.dotting = False
            return

        len_tb = next( (t for t in ToggleButton.get_widgets('len') if t.state=='down'), None)
        if len_tb == None:
            self.dotlabel.text = 'Please select a ciphertext length'
            self.dotting = False
            return

        length = int(len_tb.id)
        lang_tb = next( (t for t in ToggleButton.get_widgets('lang') if t.state=='down'), None)
        if lang_tb == None:
            self.dotlabel.text = 'Please select a language'
            self.dotting = False
            return
        lang = lang_tb.id

        if ciph_tb.id != 'caesar':
            self.dotlabel.text = 'Frequency analysis currently only available for caesar cipher.'
            self.dotting = False
            return
        
        import train
        results = train.test_all(length, lang)
        self.dotlabel.text = 'Frequency analysis accuracy: '+ str(results)
        self.dotting = False
        
    def __init__(self, **kwargs):
        super(AI, self).__init__(**kwargs)
        self.training = False
        self.dotting = False

        self.ciph1 = ToggleButton(text='Caesar cipher', id='caesar', group='ciph', size_hint=(.1,.1), pos_hint={'center_x':.15, 'center_y':.6}, background_normal='', background_color=(.6,.6,.6,1))
        self.ciph2 = ToggleButton(text='Affine cipher', id='affine', group='ciph', size_hint=(.1,.1), pos_hint={'center_x':.15, 'center_y':.5}, background_normal='', background_color=(.6,.6,.6,1))
        self.ciph3 = ToggleButton(text='Evan\'s test', id='evan', group='ciph', size_hint=(.1,.1), pos_hint={'center_x':.15, 'center_y':.4}, background_normal='', background_color=(.6,.6,.6,1))
        self.add_widget(self.ciph1)
        self.add_widget(self.ciph2)
        self.add_widget(self.ciph3)

        self.len1 = ToggleButton(text='1 words', id='1', group='len', size_hint=(.1,.1), pos_hint={'center_x':.3,'center_y':.8}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len2 = ToggleButton(text='2 words', id='2', group='len', size_hint=(.1,.1), pos_hint={'center_x':.3,'center_y':.7}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len3 = ToggleButton(text='4 words', id='4', group='len', size_hint=(.1,.1), pos_hint={'center_x':.3,'center_y':.6}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len4 = ToggleButton(text='8 words', id='8', group='len', size_hint=(.1,.1), pos_hint={'center_x':.3,'center_y':.5}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len5 = ToggleButton(text='16 words', id='16', group='len', size_hint=(.1,.1), pos_hint={'center_x':.3,'center_y':.4}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len6 = ToggleButton(text='32 words', id='32', group='len', size_hint=(.1,.1), pos_hint={'center_x':.3,'center_y':.3}, background_normal='', background_color=(.6, .6, .6, 1))
        self.len7 = ToggleButton(text='64 words', id='64', group='len', size_hint=(.1,.1), pos_hint={'center_x':.3,'center_y':.2}, background_normal='', background_color=(.6, .6, .6, 1))
        self.add_widget(self.len1)
        self.add_widget(self.len2)
        self.add_widget(self.len3)
        self.add_widget(self.len4)
        self.add_widget(self.len5)
        self.add_widget(self.len6)
        self.add_widget(self.len7)

        self.lang1 = ToggleButton(text='English', id='eng', group='lang', size_hint=(.1,.1), pos_hint={'center_x':.45,'center_y':.6}, background_normal='', background_color=(.6, .6, .6, 1))
        self.lang2 = ToggleButton(text='Spanish', id='span', group='lang', size_hint=(.1,.1), pos_hint={'center_x':.45,'center_y':.5}, background_normal='', background_color=(.6, .6, .6, 1))
        self.lang3 = ToggleButton(text='French', id='fren', group='lang', size_hint=(.1,.1), pos_hint={'center_x':.45,'center_y':.4}, background_normal='', background_color=(.6, .6, .6, 1))
        self.add_widget(self.lang1)
        self.add_widget(self.lang2)
        self.add_widget(self.lang3)
        
        self.trainbutton = Button(text='Train model', size_hint=(.25, .15), pos_hint={'center_x':.75, 'center_y':.725})
        self.trainbutton.bind(on_release=self.train_helper)
        self.add_widget(self.trainbutton)
        self.aistatus = Label(text='Model status', size_hint=(.25, .15), pos_hint={'center_x':.75, 'center_y':.575}, color=(0, 0, 0, 1))
        self.add_widget(self.aistatus)
        self.dotbutton = Button(text='Frequency analysis', size_hint=(.25, .15), pos_hint={'center_x':.75, 'center_y':.425})
        self.dotbutton.bind(on_release=self.dot_helper)
        self.add_widget(self.dotbutton)
        self.dotlabel = Label(text='Frequency analysis results', size_hint=(.25, .15), pos_hint={'center_x':.75, 'center_y':.275}, color=(0,0,0,1))
        self.add_widget(self.dotlabel)


ThisGUI().run()
