import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import time
import json
import requests
from datetime import datetime, timedelta, date
from dateutil.parser import parse as is_date

#Speech to text
def STT():
    """
    Returns text converted from speech detected in microphone, 
    or returns none if no text is detected or if there is an error.
    """
    try:
        # Get Configuration Settings
        load_dotenv()
        lu_app_id = os.getenv('LU_APP_ID')
        lu_prediction_region = os.getenv('LU_PREDICTION_REGION')
        lu_prediction_key = os.getenv('LU_PREDICTION_KEY')

        # Configure speech service and get intent recognizer
        # Configure speech service and get intent recognizer
        speech_config = speechsdk.SpeechConfig(subscription=lu_prediction_key, region=lu_prediction_region)
        audio_config = speechsdk.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.intent.IntentRecognizer(speech_config, audio_config)

        # Get the model from the AppID and add the intents we want to use
        # Get the model from the AppID and add the intents we want to use
        model = speechsdk.intent.LanguageUnderstandingModel(app_id=lu_app_id)

        # Process speech input
        # Process speech input
        intent = ''
        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # Speech was recognized, but no intent was identified.
            intent = result.text
            return intent
        elif result.reason == speechsdk.ResultReason.NoMatch:
            # Speech wasn't recognized
            print("Sorry. I didn't understand that.")
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            # Something went wrong
            print("Intent recognition canceled: {}".format(result.cancellation_details.reason))
            if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(result.cancellation_details.error_details))
            # Get the first entity (if any)
            return None
        # Get the first entity (if any)

    except Exception as ex:
        print(ex)

#text to speech
def TTS(text):
    try: 
        load_dotenv()
        sregion = os.getenv('SPEECH_REGION')
        key = os.getenv('SPEECH_KEY')
        speech_config = speechsdk.SpeechConfig(subscription=key, region=sregion)
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        # The language of the voice that speaks.
        speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
    except Exception as ex:
        print(ex)

#Task Status Understanding
def TSU():
    try: 
        load_dotenv()
        TSID = os.getenv('TASK_STATUS_ID')
        lu_prediction_region = os.getenv('LU_PREDICTION_REGION')
        lu_prediction_key = os.getenv('LU_PREDICTION_KEY')

        # Configure speech service and get intent recognizer
        speech_config = speechsdk.SpeechConfig(subscription=lu_prediction_key, region=lu_prediction_region)
        audio_config = speechsdk.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.intent.IntentRecognizer(speech_config, audio_config)

        model = speechsdk.intent.LanguageUnderstandingModel(app_id=TSID)
        intents = [
            (model, "Task Completed"),
            (model, "Working on Task"),
            (model, "Partially Completed"),
            (model, "Did not complete"),
            (model, "None")
        ]
        recognizer.add_intents(intents)
        intent = ''
        result = recognizer.recognize_once_async().get()
        if result.reason == speechsdk.ResultReason.RecognizedIntent:
            intent = result.intent_id
            print(intent)
            return intent
        elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # Speech was recognized, but no intent was identified.
            #intent = result.text
            #print("I don't know what {} means.".format(intent))
            return None
        elif result.reason == speechsdk.ResultReason.NoMatch:
            # Speech wasn't recognized
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            # Something went wrong
            print("Intent recognition canceled: {}".format(result.cancellation_details.reason))
            if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(result.cancellation_details.error_details))
            return None
    except Exception as ex:
        print(ex)


# Reason for Not Completing Task Understanding
def NCU():
    try: 
        load_dotenv()
        TSID = os.getenv('INCOMPLETE_REASON_ID')
        lu_prediction_region = os.getenv('LU_PREDICTION_REGION')
        lu_prediction_key = os.getenv('LU_PREDICTION_KEY')

        # Configure speech service and get intent recognizer
        speech_config = speechsdk.SpeechConfig(subscription=lu_prediction_key, region=lu_prediction_region)
        audio_config = speechsdk.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.intent.IntentRecognizer(speech_config, audio_config)

        model = speechsdk.intent.LanguageUnderstandingModel(app_id=TSID)
        intents = [
            (model, "Lack of Faith"),
            (model, "Break"),
            (model, "Serious Excuse"),
            (model, "None")
        ]
        recognizer.add_intents(intents)
        intent = ''
        result = recognizer.recognize_once_async().get()
        if result.reason == speechsdk.ResultReason.RecognizedIntent:
            intent = result.intent_id
            print(intent)
            return intent
        elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # Speech was recognized, but no intent was identified.
            #intent = result.text
            #print("I don't know what {} means.".format(intent))
            return None
        elif result.reason == speechsdk.ResultReason.NoMatch:
            # Speech wasn't recognized
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            # Something went wrong
            print("Intent recognition canceled: {}".format(result.cancellation_details.reason))
            if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(result.cancellation_details.error_details))
            return None
    except Exception as ex:
        print(ex)

# Yes or No understanding
def YN():
    try: 
        load_dotenv()
        TSID = os.getenv('YN_ID')
        lu_prediction_region = os.getenv('LU_PREDICTION_REGION')
        lu_prediction_key = os.getenv('LU_PREDICTION_KEY')

        # Configure speech service and get intent recognizer
        speech_config = speechsdk.SpeechConfig(subscription=lu_prediction_key, region=lu_prediction_region)
        audio_config = speechsdk.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.intent.IntentRecognizer(speech_config, audio_config)

        model = speechsdk.intent.LanguageUnderstandingModel(app_id=TSID)
        intents = [
            (model, "yes"),
            (model, "no"),
            (model, "None")
        ]
        recognizer.add_intents(intents)
        intent = ''
        result = recognizer.recognize_once_async().get()
        if result.reason == speechsdk.ResultReason.RecognizedIntent:
            intent = result.intent_id
            print(intent)
            return intent
        elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # Speech was recognized, but no intent was identified.
            #intent = result.text
            #print("I don't know what {} means.".format(intent))
            return None
        elif result.reason == speechsdk.ResultReason.NoMatch:
            # Speech wasn't recognized
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            # Something went wrong
            print("Intent recognition canceled: {}".format(result.cancellation_details.reason))
            if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(result.cancellation_details.error_details))
            return None
    except Exception as ex:
        print(ex)

