# -*- coding: utf-8 -*-

import speech_recognition as sr
import inquirer
import time
import webbrowser
import playsound
import os
import random
import pyttsx3
# from urllib.request import urlopen
from datetime import datetime 

r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

questions = [
    inquirer.List('language',
                message="Choose language.",
                choices=["English", "Korean"],
            ),
]
answers = inquirer.prompt(questions)['language']

if answers == "English":
    engine.setProperty('voice', "com.apple.speech.synthesis.voice.samantha")
else:
    engine.setProperty('voice', "com.apple.speech.synthesis.voice.yuna")


def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ''

    try:
        if answers == "English":
            voice_data = r.recognize_google(audio, language="en-CA")
        else:
            voice_data = r.recognize_google(audio, language="ko-KR")
    except sr.UnknownValueError:
        if answers == "English":
            speak("Sorry, I didn't quite get that.")
        else:
            speak("죄송합니다. 다시 한번 말씀해주세요.")
    except sr.RequestError:
        if answers == "English":
            speak("An error occurred. Please try again later.")
        else:
            speak("오류가 발생했습니다. 나중에 다시 시도해 주세요.")
    return voice_data.lower()

def speak(audio_string):
    print(audio_string)
    engine.say(audio_string)
    engine.runAndWait()


def respond(voice_data):
    # name
    if "what is your name" in voice_data:
        speak("My name is Shiri.")
    # name (k ver)
    if u"이름이 뭐" in voice_data:
        speak("제 이름은 쉬리입니다.")
    # time
    if "what time is it" in voice_data:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        speak("It is " + current_time)
    # time (k ver)
    if u"몇 시" in voice_data:
        now = datetime.now()
        current_time = now.strftime("%H시 %M분")
        speak(current_time + "입니다.")
    # search
    if "search" in voice_data:
        search = record_audio("What do you want to search for?")
        speak("Here is what I found for " + search + ".")
        url = "https://google.com/search?q=" + search
        webbrowser.get().open(url)
    # search (k ver)
    if u"검색" in voice_data:
        search = record_audio("무엇을 검색해드릴까요?")
        speak(search + "에 대한 검색 결과입니다.")
        url = "https://google.com/search?q=" + search
        webbrowser.get().open(url)
    # location
    if "find location" in voice_data:
        location = record_audio("What is the location?")
        speak("Here is the location of " + location + ".")
        url = "https://google.ca/maps/place/" + location + "/&amp;"
        webbrowser.get().open(url)
    # location (k ver)
    if u"위치" in voice_data:
        location = record_audio("What is the location?")
        speak(location + "의 위치입니다.")
        url = "https://google.ca/maps/place/" + location + "/&amp;"
        webbrowser.get().open(url)
    # exit
    exit_str = ["exit", u"끝", u"꺼져"]
    for i in exit_str:
        if i in voice_data:
            exit()
        
time.sleep(1)
if answers == "English":
    speak("How can I help you?")
else:
    speak("무엇을 도와드릴까요?")
while 1:
    voice_data = record_audio()
    respond(voice_data)
