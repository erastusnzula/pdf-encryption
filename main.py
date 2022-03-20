import os
import sys
from os.path import dirname, expanduser, sep

from PyPDF2 import PdfFileReader, PdfFileWriter
from kivy import platform
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, WipeTransition, Screen
from kivy_garden.filebrowser import FileBrowser


class Encrypt(Screen):
    file = None
    selected_file = StringProperty('< No file selected >')
    focus_text = BooleanProperty(False)
    encryption_button_disabled = BooleanProperty(True)
    password_input_disabled = BooleanProperty(True)
    change_file_button = BooleanProperty(True)
    file_select_disabled = BooleanProperty(False)
    display_select_button = BooleanProperty(True)
    password = StringProperty()
    file_encrypt_button = StringProperty('Encrypt')
    change_file = StringProperty('Change file')
    count_files_encrypted = StringProperty()
    count = 0
    user_path = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'windows':
            self.user_path = dirname(expanduser('~')) + sep + 'Downloads'
        else:
            self.user_path = expanduser('~') + sep + 'Downloads'

    def select_file(self, instance):
        self.file = '.'.join(instance.selection)
        if self.file.endswith('.pdf'):
            self.selected_file = 'Selected file : ' + os.path.basename(self.file)
            # self.file_select_disabled = True
            self.encryption_button_disabled = False
            self.password_input_disabled = False
            self.change_file_button = False
            self.display_select_button = False
            self.focus_text = True
        else:
            self.selected_file = "Please select a file with '.pdf ' extension."
            self.display_select_button = False
            popup = Popup(title='Select file',
                          content=Label(text="Please select a file with '.pdf ' extension."),
                          size_hint=(None, None), size=(400, 100))
            popup.open()

    def enable_select_file(self):
        self.file_encrypt_button = 'Encrypt'
        self.file_select_disabled = False
        self.selected_file = '< No file selected >'
        self.password_input_disabled = True
        self.display_select_button = True
        self.change_file_button = True
        self.encryption_button_disabled = True
        self.change_file = "Change file"

    def encrypt_file(self, instance):
        if self.password:
            file = PdfFileReader(self.file)  # Read the file.
            new_file = PdfFileWriter()
            pages = file.getNumPages()
            for page in range(pages):
                new_file.addPage(file.getPage(page))
            new_file.encrypt(user_pwd=self.password, use_128bit=True)
            os.makedirs('Encrypted files', exist_ok=True)
            file_basename = os.path.basename(self.file)
            if file_basename in os.listdir('Encrypted files'):
                file_basename = f'{os.path.splitext(file_basename)[0][:-1]}' \
                                f'{len(os.listdir("Encrypted files")) + 1}' \
                                f'{os.path.splitext(file_basename)[1]}'
            filename = os.path.join('Encrypted files', file_basename)
            with open(filename, 'wb') as f:
                new_file.write(f)
            # self.file_encrypt_button = "File encrypted"
            # self.change_file = "Encrypt another file"
            # self.file_select_disabled = False
            self.count += 1
            self.count_files_encrypted = 'ENCRYPTED FILES: ' + str(self.count)
            self.enable_select_file()

        else:
            popup = Popup(title='Password',
                          content=Label(text='Please enter password.'),
                          size_hint=(None, None), size=(400, 100))
            popup.open()

    @staticmethod
    def exit_protocol():
        sys.exit()


class EncryptApp(App):
    def build(self):
        screen = ScreenManager(transition=WipeTransition())
        screen.add_widget(Encrypt(name='password'))
        return screen


if __name__ == '__main__':
    EncryptApp().run()
