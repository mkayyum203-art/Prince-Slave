import os
# Video playback fix for Android
os.environ['KIVY_VIDEO'] = 'ffpyplayer'

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.filemanager import MDFileManager

import sqlite3
import hashlib
import math

Window.softinput_mode = "below_target"

KV = '''
ScreenManager:
    LoginScreen:
    SignupScreen:
    AdminDashboardScreen:
    TraineeDashboardScreen:
    AssignTaskScreen:
    VideoPlayerScreen:
    TaskDetailScreen:

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(12)
        padding: dp(20)
        MDTopAppBar:
            title: "Pro-Level Training App"
            elevation: 4
        Widget:
            size_hint_y: None
            height: dp(30)
        MDLabel:
            text: "Login"
            halign: "center"
            font_style: "H4"
        MDTextField:
            id: login_username
            hint_text: "Username"
            icon_right: "account"
        MDTextField:
            id: login_password
            hint_text: "Password"
            password: True
            icon_right: "lock"
        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": 0.5}
            on_release: app.login()
        MDTextButton:
            text: "Create Account"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = "signup"
        Widget:

<SignupScreen>:
    name: "signup"
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(12)
        padding: dp(20)
        MDTopAppBar:
            title: "Create Account"
            anchor_title: "left"
        MDTextField:
            id: signup_username
            hint_text: "Username"
        MDTextField:
            id: signup_password
            hint_text: "Password"
            password: True
        MDTextField:
            id: signup_role
            hint_text: "Role (admin or trainee)"
        MDRaisedButton:
            text: "Sign Up"
            pos_hint: {"center_x": 0.5}
            on_release: app.signup()
        Widget:

<AdminDashboardScreen>:
    name: "admindashboard"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Admin Dashboard"
        ScrollView:
            MDBoxLayout:
                id: admin_box
                orientation: "vertical"
                adaptive_height: True
                padding: dp(12)
                spacing: dp(12)
                MDCard:
                    orientation: "vertical"
                    padding: dp(12)
                    size_hint_y: None
                    height: dp(150)
                    MDLabel:
                        text: "Assign Training"
                        font_style: "H6"
                    MDRaisedButton:
                        text: "Assign Task"
                        on_release: app.root.current = "assigntask"
                MDList:
                    id: trainee_list

<TraineeDashboardScreen>:
    name: "traineedashboard"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Trainee Dashboard"
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: dp(12)
                spacing: dp(12)
                MDCard:
                    orientation: "vertical"
                    padding: dp(12)
                    size_hint_y: None
                    height: dp(200)
                    MDLabel:
                        id: traineewelcome
                        font_style: "H5"
                    MDProgressBar:
                        id: xpprogress
                        value: 0
                    MDLabel:
                        id: levellabel
                        text: "Level: 1"
                MDList:
                    id: traineetasklist

<AssignTaskScreen>:
    name: "assigntask"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Assign Task"
        MDTextField:
            id: tasktitle
            hint_text: "Task Title"
        MDTextField:
            id: taskassignee
            hint_text: "Assign to (Username)"
        MDRaisedButton:
            text: "Create Task"
            on_release: app.assign_task()

<VideoPlayerScreen>:
    name: "videoplayer"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Video Drill"
        Video:
            id: vid_player
            source: ""
            state: "play"
            options: {'allow_stretch': True}

<TaskDetailScreen>:
    name: "taskdetail"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Task Details"
        MDLabel:
            id: detailtitle
            font_style: "H5"
        MDRaisedButton:
            text: "Play Video"
            on_release: app.open_task_video()
'''

class LoginScreen(Screen): pass
class SignupScreen(Screen): pass
class AdminDashboardScreen(Screen): pass
class TraineeDashboardScreen(Screen): pass
class AssignTaskScreen(Screen): pass
class VideoPlayerScreen(Screen): pass
class TaskDetailScreen(Screen): pass

class DatabaseManager:
    def __init__(self, db_name="training.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT, xp INTEGER DEFAULT 0)")
        cur.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, videopath TEXT, assignedto TEXT, status TEXT DEFAULT 'pending')")
        self.conn.commit()

class ProTrainingApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.db = DatabaseManager()
        return Builder.load_string(KV)

    def login(self):
        # Basic Logic for UI Navigation
        self.root.current = "traineedashboard"

    def signup(self):
        self.root.current = "login"

if __name__ == "__main__":
    ProTrainingApp().run()
