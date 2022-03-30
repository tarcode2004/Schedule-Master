from kivymd.app import MDApp
import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta, date
from dateutil.parser import parse as is_date

class MainApp(MDApp):
    user_idToken = ""
    local_id = ""

    def display_user_tokens(self):
        self.root.ids.the_label.text = "local_id: " + self.local_id + "\n user_idToken: " + self.user_idToken

    def sign_out(self):
        self.root.ids.firebase_login_screen.log_out()
        self.root.current = 'firebase_login_screen'
    
    def luis(self):
        try:
            # Get Configuration Settings
            load_dotenv()
            lu_app_id = os.getenv('LU_APP_ID')
            lu_prediction_region = os.getenv('LU_PREDICTION_REGION')
            lu_prediction_key = os.getenv('LU_PREDICTION_KEY')

            # Configure speech service and get intent recognizer
            # Configure speech service and get intent recognizer
            speech_config = speech_sdk.SpeechConfig(subscription=lu_prediction_key, region=lu_prediction_region)
            audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
            recognizer = speech_sdk.intent.IntentRecognizer(speech_config, audio_config)

            # Get the model from the AppID and add the intents we want to use
            # Get the model from the AppID and add the intents we want to use
            model = speech_sdk.intent.LanguageUnderstandingModel(app_id=lu_app_id)
            intents = [
                (model, "GetTime"),
                (model, "GetDate"),
                (model, "GetDay"),
                (model, "None")
            ]
            recognizer.add_intents(intents)

            # Process speech input
            # Process speech input
            intent = ''
            result = recognizer.recognize_once_async().get()
            if result.reason == speech_sdk.ResultReason.RecognizedIntent:
                intent = result.intent_id
                print("Query: {}".format(result.text))
                print("Intent: {}".format(intent))
                json_response = json.loads(result.intent_json)
                print("JSON Response:\n{}\n".format(json.dumps(json_response, indent=2)))
            elif result.reason == speech_sdk.ResultReason.RecognizedSpeech:
                # Speech was recognized, but no intent was identified.
                intent = result.text
                print("I don't know what {} means.".format(intent))
            elif result.reason == speech_sdk.ResultReason.NoMatch:
                # Speech wasn't recognized
                print("Sorry. I didn't understand that.")
            elif result.reason == speech_sdk.ResultReason.Canceled:
                # Something went wrong
                print("Intent recognition canceled: {}".format(result.cancellation_details.reason))
                if result.cancellation_details.reason == speech_sdk.CancellationReason.Error:
                    print("Error details: {}".format(result.cancellation_details.error_details))
                # Get the first entity (if any)
            # Get the first entity (if any)
            entity_type = ''
            entity_value = ''
            if len(json_response["entities"]) > 0:
                entity_type = json_response["entities"][0]["type"]
                entity_value = json_response["entities"][0]["entity"]
                print(entity_type + ': ' + entity_value)
                # Apply the appropriate action
            # Apply the appropriate action
            if intent == 'GetTime':
                location = 'local'
                # Check for entities
                if entity_type == 'Location':
                    location = entity_value
                # Get the time for the specified location
                print(GetTime(location))

            elif intent == 'GetDay':
                date_string = date.today().strftime("%m/%d/%Y")
                # Check for entities
                if entity_type == 'Date':
                    date_string = entity_value
                # Get the day for the specified date
                print(GetDay(date_string))

            elif intent == 'GetDate':
                day = 'today'
                # Check for entities
                if entity_type == 'Weekday':
                    # List entities are lists
                    day = entity_value
                # Get the date for the specified day
                print(GetDate(day))

            else:
                # Some other intent (for example, "None") was predicted
                print('You said {}'.format(result.text))
                if result.text.lower().replace('.', '') == 'stop':
                    intent = result.text
                else:
                    print('Try asking me for the time, the day, or the date.')
        
        except Exception as ex:
            print(ex)

MainApp().run()