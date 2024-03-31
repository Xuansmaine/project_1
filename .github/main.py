from logging.handlers import RotatingFileHandler
from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
#---- for audio----#
from recorder import AudioRecorder
from kivy.clock import Clock
import os
#---- for inputpage----#
import requests
import threading
#---- for gps ----#
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.popup import Popup





r = 242/255
g =168/255
b = 141/255
t = 0
color = (r , g ,b ,t)
Window.clearcolor = color

ip = "http://192.168.0.107:5000"
btn_color =(58/255,27/255,215/255,1)


font_path = "Roboto"

width, height = Window.size
font_size = width / 50
class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        # Create a layout
        self.layout = FloatLayout()
        # Create a label
        
        self.label = Label(text="Hi user! Below are the fuctions: ", size_hint=(50,50), font_size=font_size,
                           pos_hint={'center_x': 0.5, 'center_y': 0.7})

       # ------ where a white box need to recive and show notification form AlderEyes ------ #

        # Create a button
        self.button1 = Button(text='Monitoring', size_hint=(0.7,0.08),
                             size=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.400}, font_name = font_path)
        self.button1.on_press = self.next_info

        self.button2 = Button(text='Run AlderEyes', size_hint = (0.7,0.08),
                             size=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.300},font_name = font_path)
        self.button2.on_press = self.next_run

        self.button3 = Button(text='Voice Message', size_hint = (0.7,0.08),
                             size=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.200},font_name = font_path)
        self.button3.on_press = self.next_record

        self.button4 = Button(text='Nearest Hospital', size_hint = (0.7,0.08),
                             size=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.100},font_name = font_path)
        self.button4.on_press = self.next_hospital




        # Add widgets to the layout


        self.layout.add_widget(self.button1)
        self.layout.add_widget(self.button2)
        self.layout.add_widget(self.button3)
        self.layout.add_widget(self.button4)
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    

    def next_run(self):
        self.manager.current  = 'run'
    def next_record(self):
        self.manager.current = "recorder"
    def next_hospital(self):
        self.manager.current = 'gps'
    def next_info(self):
        self.manager.current = 'info'




class InputPage(Screen):
    def __init__(self, **kwargs):
        super(InputPage, self).__init__(**kwargs)
        layout = FloatLayout()
        self.label = Label(text="motion detected", size_hint=(0.8, 0.8),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.button = Button(text='Home', size_hint=(0.16, 0.125),
                             size=(0.3, 0.1), pos_hint={'center_x': 0.8, 'center_y': 0.125})
        self.button.bind(on_press=self.back_main)

        layout.add_widget(self.label)
        layout.add_widget(self.button)

        self.add_widget(layout)

        # Schedule the check_motion function to run every 5 minutes
        Clock.schedule_interval(self.check_motion, 1)  # 300 seconds = 5 minutes

    def check_motion(self, dt):
        try:
            response = requests.get(ip)
            if response.status_code == 200 :#and response.json().get("motion_detected"):
                self.display_notification("There's motion detected in house!")
            else:
                self.display_notification("No Motion detected in 2 hours. Please check on the elderly!")
        except Exception as e:
            print("Error:", e)
            self.display_message("Error waiting for signal")

    def display_message(self, message):
        self.label.text = message

    def display_notification(self, message):
        self.label.text = message
        self.label.font_size = font_size

    def back_main(self, instance):
        self.manager.current = "main"


class InfoPopup(Popup):
    # def __init__(self, title, text, **kwargs):
    #     super().__init__(**kwargs)
    #     self.title = title
    #     self.content = Label(text=text, halign='center', valign='middle', font_size=14)
    pass

class GPSPage(Screen):

    def __init__(self, **kwargs):
        super(GPSPage, self).__init__(**kwargs)
        layout = FloatLayout()
        self.button3 = Button(text='Home', size_hint=(0.16,0.125),
                             size=(0.3, 0.1), pos_hint={'center_x': 0.8, 'center_y': 0.125},font_name = font_path)
        self.button3.bind(on_press=self.back_main)
        layout.add_widget(self.button3)

        # Create a MapView widget
        self.mapview = MapView(zoom=16, lat=3.020786, lon=101.622825)
        # Add the MapView widget to the screen
        self.add_widget(self.mapview)
        # Create a popup for marker information
        self.popup = Popup(title="Infomation", content=Label(text=""), size_hint=(None, None), size=(500, 200))

        # Map marker locations to their information
        self.marker_info = {
            (13.6513, 100.4964): "Current location",
            (13.6777, 100.4986): "IMH Thonburi hospital, contact:+6624279966",
            (13.68159, 100.474723): "Bangmod hospital, contact:+6628670606",
            (3.020786, 101.622825) : "Current location",
            (3.023914694006378, 101.62222327872797) : "Columbia Asia Hospital, contact:+0380648688"

        }

        # Add markers with popups
        # self.mapview.add_marker(MapMarkerPopup(lat=13.6513, lon=100.4964, size=(70, 70), on_release=self.show_info))
        # self.mapview.add_marker(MapMarkerPopup(lat=13.6777, lon=100.4986, size=(70, 70), on_release=self.show_info))
        # self.mapview.add_marker(MapMarkerPopup(lat=13.68159, lon=100.474723, size=(70, 70), on_release=self.show_info))
        self.mapview.add_marker(MapMarkerPopup(lat=3.020786, lon=101.622825, size=(70, 70), on_release=self.show_info))
        self.mapview.add_marker(MapMarkerPopup(lat=3.023914694006378, lon=101.62222327872797, size=(70, 70), on_release=self.show_info))
        self.add_widget(layout)

    def back_main(self, instance):
        self.manager.current = "main"

    def show_info(self, instance):
        # Get the marker's latitude and longitude
        lat, lon = instance.lat, instance.lon

        # Look up the information for the marker
        info = self.marker_info.get((lat, lon), "Unknown Location")

        # Set the popup content to display the information
        self.popup.content = Label(text=info)

        # Open the popup
        self.popup.open()

        # Add markers with popups
        # self.mapview.add_marker(MapMarkerPopup(lat=13.6513, lon=100.4964, size=(70, 70),  on_marker_touch=self.show_info))
        # self.mapview.add_marker(MapMarkerPopup(lat=13.6777, lon=100.4986, size=(70, 70), on_marker_touch=self.show_info))
        # self.mapview.add_marker(MapMarkerPopup(lat=13.68159, lon=100.474723, size=(70, 70), on_marker_touch=self.show_info))
    
    # Create a popup for marker information


    
    

class RUNPage(Screen):
    def __init__(self, **kwargs):
        super(RUNPage, self).__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="you can Run / Sleep AlderEyes here! ", size_hint=(None, None),font_size = font_size,
                                size=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.7}))
        self.button1 = Button(text= "Run",size_hint=(0.16,0.125),font_size=font_size,
                             size=(0.4, 0.1), pos_hint={'center_x': 0.3, 'center_y': 0.4},font_name = font_path,
                             background_color = (1, 1, 1, 1)) # set the default background color to white
        self.button1.bind(on_press=self.pressed_run)

        self.button2 = Button(text= "Sleep",size_hint=(0.16,0.125),font_size=font_size,
                             size=(0.4, 0.1), pos_hint={'center_x': 0.7, 'center_y': 0.4},font_name = font_path,
                             background_color = (1, 1, 1, 1)) # set the default background color to white
        self.button2.bind(on_press=self.pressed_sleep)

        self.button3 = Button(text='Home', size_hint=(0.16,0.125),
                             size=(0.3, 0.1), pos_hint={'center_x': 0.8, 'center_y': 0.125},font_name = font_path)
        self.button3.bind(on_press=self.back_main)

        layout.add_widget(self.button1)
        layout.add_widget(self.button2)
        layout.add_widget(self.button3)

        self.add_widget(layout)

    def back_main(self, instance):
        self.manager.current = "main"

    def run_AlderEyes(self , none):
        requests.post(ip, data={'command': 'forward'})

    def sleep_AlderEyes(self, none):
        requests.post(ip, data={'command': 'backward'})

    def pressed_run(self, instance):
        self.button1.background_color = (127/255, 255/255, 0/255) # set the background color to (255,245,182)
        self.button2.background_color = (1, 1, 1, 1) # reset the background color of the sleep button to white

    def pressed_sleep(self, instance):
        self.button1.background_color = (1, 1, 1, 1) # reset the background color of the run button to white
        self.button2.background_color = (127/255, 255/255, 0/255) # set the background color to (255,245,182)

class RecorderPage(Screen):
    def __init__(self, **kwargs):
        super(RecorderPage, self).__init__(**kwargs)
        self.audio_recorder = AudioRecorder()
        self.recording = False

        layout = FloatLayout()
        layout.add_widget(Label(text="You can record your messages here!", size_hint=(None, None),font_size = font_size,
                                size=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.7}))

        self.record_button = Button(text='Press to record', size_hint=(0.3, 0.1),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.record_button.bind(on_press=self.toggle_recording)

        self.play_button = Button(text='Play Audio', size_hint=(0.3, 0.1),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.45})
        self.play_button.bind(on_press=self.play_audio)

        self.home_button = Button(text='Home', size_hint=(0.16,0.125),
                             size=(0.3, 0.1), pos_hint={'center_x': 0.8, 'center_y': 0.125})
        self.home_button.bind(on_press=self.back_main)

        layout.add_widget(self.record_button)
        layout.add_widget(self.play_button)
        layout.add_widget(self.home_button)

        self.add_widget(layout)

    def toggle_recording(self, _):
        if not self.audio_recorder.is_recording:
            self.audio_recorder.start_recording()
            self.record_button.text = 'Recording...'
            Clock.schedule_interval(self.update_recording_status, 1.0 / 30.0)
        else:
            self.audio_recorder.stop_recording()
            self.audio_recorder.save_recording()
            self.record_button.text = 'Press to record'

    def start_recording(self):
        with self.audio_recorder.recording_lock:
            self.recording = True
            self.record_button.text = 'Recording...'
            threading.Thread(target=self.audio_recorder.start_recording).start()
            Clock.schedule_interval(self.update_recording_status, 1.0 / 30.0)

    def update_recording_status(self, dt):
        # Update UI based on recording status
        if self.audio_recorder.is_recording:
            # Perform actions specific to recording status
            pass
        else:
            # Perform actions for when not recording
            pass

    def stop_recording(self):
        with self.audio_recorder.recording_lock:
            self.recording = False
            self.record_button.text = 'Press to record'
            threading.Thread(target=self.audio_recorder.stop_recording).start()

    def play_audio(self, instance):
        try:
            # Use the recorded file for playback
            os.system("output1.wav")  # Adjust this line for your OS if needed
        except Exception as e:
            print("Error playing audio:", str(e))

    def back_main(self, instance):
        self.manager.current = "main"


class MyApp(App):
    def build(self):
        # Create the screen manager
        self.screen_manager = ScreenManager()

        # Add the pages
        self.main_page = MainPage(name='main')
        self.input_page = InputPage(name= 'info')
        self.gps_page = GPSPage(name = 'gps')
        self.run_page = RUNPage(name = 'run')
        self.recorder_page = RecorderPage(name = 'recorder')

        self.screen_manager.add_widget(self.main_page)
        self.screen_manager.add_widget(self.input_page)
        self.screen_manager.add_widget(self.gps_page)
        self.screen_manager.add_widget(self.run_page)
        self.screen_manager.add_widget(self.recorder_page)



        return self.screen_manager


if __name__ == '__main__':
    MyApp().run()


