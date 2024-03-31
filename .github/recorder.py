import pyaudio
import wave
import threading

p = pyaudio.PyAudio()
devices = []

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.recording_lock = threading.Lock()  # Add recording lock
        self.stream = None
        self.device_index = None

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            input=True,
            frames_per_buffer=1024
        )
        self.stream.start_stream()

    def stop_recording(self):
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.audio.terminate()

    def save_recording(self, filename="output.wav"):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()
    
    def list_input_devices(self):
        num_devices = self.audio.get_device_count()
        devices = []
        for i in range(num_devices):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info.get('maxInputChannels') > 0:
                devices.append((i, device_info.get('name')))
        return devices

# class AudioRecorder:
#     def __init__(self):
#         self.audio = pyaudio.PyAudio()
#         self.frames = []
#         self.is_recording = False
#         self.recording_lock = threading.Lock()
#         self.stream = None
#         self.device_index = None



#     def start_recording(self, device_index=None):
#         try:
#             self.is_recording = True
#             self.frames = []
#             self.device_index = device_index
#             if device_index is None:
#                 # Default to the first available input device
#                 devices = self.list_input_devices()
#                 if devices:
#                     self.device_index = devices[0][0]
#                 else:
#                     print("No input devices found.")
#                     return
#             self.stream = self.audio.open(
#                 format=pyaudio.paInt16,
#                 channels=2,
#                 rate=48000,
#                 input=True,
#                 frames_per_buffer=1024,
#                 input_device_index=self.device_index
#             )
#             # Start reading frames from the stream and append them to self.frames
#             while self.is_recording:
#                 data = self.stream.read(1024)
#                 self.frames.append(data)
#         except Exception as e:
#             print("Error starting recording:", str(e))

#     def stop_recording(self):
#         try:
#             self.is_recording = False
#             if self.stream:
#                 self.stream.stop_stream()
#                 self.stream.close()
#                 self.stream = None
#             self.audio.terminate()
#         except Exception as e:
#             print("Error stopping recording:", str(e))

#     def save_recording(self, filename="output.wav"):
#         try:
#             if len(self.frames) <= 0 :
#                 print("No audio frames captured.")
#                 return
#             wf = wave.open(filename, 'wb')
#             wf.setnchannels(2)
#             wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
#             wf.setframerate(48000)
#             wf.writeframes(b''.join(self.frames))
#             wf.close()
#             print("Recording saved to:", filename)
#         except Exception as e:
#             print("Error saving recording:", str(e))

# Usage:
# from my_audio_recorder import AudioRecorderApp
# AudioRecorderApp().run()


