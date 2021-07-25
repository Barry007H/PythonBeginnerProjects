from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import time
import playsound
import speech_recognition as sr
import pyttsx3
import pytz

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ["nd", "rd", "th", "st"]

def speak(text) :
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_user_audio() :
    r = sr.Recognizer()
    with sr.Microphone() as source :
        audio = r.listen(source)
        said = ""

        try :
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said


def authentic_user():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(day, service) :
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    UTC = pytz.UTC
    date.astimezone(UTC)
    end_date.astimezone(UTC)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(), singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def get_date(text) :
    text = text.lower()

    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    if text.count("today") > 0 : return today
    if text.count("tomorrow") > 0: return tomorrow

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split() :
        if word in MONTHS : month = MONTHS.index(word) + 1
        elif word in DAYS : day_of_week = DAYS.index(word) + 1
        elif word.isdigit() : day = int(word)
        else :
            for ext in DAY_EXTENSIONS :
                found = word.find(ext)
                if found > 0 :
                    try :
                        day = int(word[:found])
                    except :
                        pass
    if month < today.month and month != -1 : year += 1
    if day < today.day and month == -1 and day != -1 : month + 1
    if month == -1 and day == -1 and day_of_week != -1 :
        current_day_of_week = today.weekday()
        diff = day_of_week - current_day_of_week
        if diff < 0 :
            diff += 7
            if text.count("next") > 1 : diff +=7

        return today + datetime.timedelta(diff)

    return datetime.date(month=month, day=day, year=year)

SERVICE = authentic_user()
text = get_user_audio()
get_events(get_date(text), SERVICE)