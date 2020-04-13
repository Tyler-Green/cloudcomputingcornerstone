import azure.cognitiveservices.speech as speechsdk
import time
import wave

def speech_recognize_continuous_from_file(thisisafile):
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription="324eb65db1f642b59c071edeae3bf61d", region="westus")
    audio_config = speechsdk.audio.AudioConfig(filename=thisisafile)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
    # </SpeechContinuousRecognitionWithFile>


# Creates an audio configuration that points to an audio file.
# Replace with your own audio filename.
audio_filename = "Letterkenny/oneZ.wav"
#files = ["Letterkenny/GoTime.wav"]
print(f"-------------------------\n{audio_filename}\n-------------------------\n")
speech_recognize_continuous_from_file(audio_filename)
print(f"\n-------------------------\n")
