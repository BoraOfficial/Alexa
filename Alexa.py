from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json
import time
import datetime
import sys
import re
import random
from pytube import YouTube
import requests
from gtts import gTTS
from playsound import playsound
from googletrans import Translator
translator = Translator()
import lxml.etree
import speech_recognition as sr
import signal
from os import system, remove, rename, startfile, kill

from moviepy.editor import *



headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}



# Gets the IP and turns it into city information
url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)


city = data['city']
country = data['country']
# print(country)
  


def get_territory_languages():
    url = "https://raw.githubusercontent.com/BoraOfficial/cldr/master/common/supplemental/supplementalData.xml"
    langxml = urlopen(url)
    langtree = lxml.etree.XML(langxml.read())

    territory_languages = {}
    for t in langtree.find('territoryInfo').findall('territory'):
        langs = {}
        for l in t.findall('languagePopulation'):
            langs[l.get('type')] = {
                'percent': float(l.get('populationPercent')),
                'official': bool(l.get('officialStatus'))
            }
        territory_languages[t.get('type')] = langs
    return territory_languages

TERRITORY_LANGUAGES = get_territory_languages()

def get_official_locale_ids(country_code):
    country_code = country_code.upper()
    langs = TERRITORY_LANGUAGES[country_code].items()
    # most widely-spoken first:
    try:
        langs.sort(key=lambda l: l[1]['percent'], reverse=True)
    except:
        pass
    return [
        '{lang}_{terr}'.format(lang=lang, terr=country_code)
        for lang, spec in langs if spec['official']
    ]

locale_ids = get_official_locale_ids(country)
# print(locale_ids[0])
def listToString(s): 
    
    empty = "" 
    
    return (empty.join(s))

language = listToString(locale_ids[0]).replace("_", "-")






def weather(city):
	city = city.replace(" ", "+")
	res = requests.get(
		f'https://www.google.com/search?q=weather+in+{city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
	# print("Searching...\n")
	soup = BeautifulSoup(res.text, 'html.parser')
	location = soup.select('#wob_loc')[0].getText().strip()
	time = soup.select('#wob_dts')[0].getText().strip()
	info = soup.select('#wob_dc')[0].getText().strip()
	weather = soup.select('#wob_tm')[0].getText().strip()
	info_english = translator.translate(info, dest='en') # in case they dont live in the US or UK
	# print(location)
	# print(time)
	# print(info)
	speak = "The weather is "+info_english.text+" and it's "+weather+" degrees outside"
	# print(speak)
	try:
		trans_to_orig_lang = translator.translate(speak, dest=language)
		gTTS(text=trans_to_orig_lang, lang=language, slow=False).save("weathertemp18762.mp3")
	except:
		# print("Language not supported! Using default language instead.")
		gTTS(text=speak, lang="en", slow=False).save("weathertemp18762.mp3")
	playsound("weathertemp18762.mp3")
	remove("weathertemp18762.mp3")







r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        # print("Speak Anything :")
        clear = open("speech.txt", "w")
        clear.write("")
        clear.close()
        try:
            # audio = r.listen(source,timeout=1,phrase_time_limit=10)
            # print("You said : {}".format(text))
            f = open("speech.txt", "a")
            f.write(r.recognize_google(r.listen(source,timeout=1,phrase_time_limit=10)))
            f.close()
            content = open("speech.txt", "r")
            read_content = content.read().replace("-", " ")
            content.close()

            if "alexa how is the weather" in read_content.lower():

                weather(city)
                read_content = None
                content = None
            elif "alexa set an alarm for" in read_content.lower():
                alarm_done = "Successfully set an alarm for "+read_content[read_content.find('for'):].replace("for ", "")
                if ":" in alarm_done:
                    try:
                        trans_to_orig_lang = translator.translate(alarm_done, dest=language)
                        gTTS(text=trans_to_orig_lang, lang=language, slow=False).save("alarmtemp18762.mp3")
                    except:
                        # print("Language not supported! Using default language instead.")
                        gTTS(text=alarm_done, lang="en", slow=False).save("alarmtemp18762.mp3")
                    playsound("alarmtemp18762.mp3")
                    remove("alarmtemp18762.mp3")
                    alarm = open("alarm.txt", "w")
                    alarm.write(read_content[read_content.find('for'):].replace("for ", ""))
                    alarm.close()
                    startfile("alarm.py")
                else:
                    pass

                
                read_content = None
                content = None

            elif "alexa spell" in read_content.lower():
                
                try:
                    transl_to_orignal_lang = translator.translate(read_content[read_content.find('spell'):].replace("spell", "")+" is spelled"+" ".join(read_content[read_content.find('spell'):].replace("spell", "")), dest=language)
                    gTTS(text=transl_to_orignal_lang, lang=language, slow=True).save("spelltemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text=read_content[read_content.find('spell'):].replace("spell", "")+" is spelled"+" ".join(read_content[read_content.find('spell'):].replace("spell", "")), lang="en", slow=True).save("spelltemp18762.mp3")
                playsound("spelltemp18762.mp3")
                remove("spelltemp18762.mp3")
                read_content = None
                content = None

            elif "alexa play" in read_content.lower():
                
                song = " ".join(read_content[read_content.find('play'):].replace("play ", ""))
                try:
                    transl_lang = translator.translate("Loading please wait", dest=language)
                    gTTS(text=transl_lang, lang=language, slow=False).save("songtemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text="Loading please wait", lang="en", slow=True).save("songtemp18762.mp3")
                playsound("songtemp18762.mp3")
                remove("songtemp18762.mp3")
                track = song.replace(" ", "%20")
                html = urlopen("https://www.youtube.com/results?search_query="+track+"+music")
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                # print(video_ids[0])

                yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[0])

                video = yt.streams.filter(only_audio=False).first()
                out_file = video.download(output_path=".", filename="song.mp4")
                music = VideoFileClip("song.mp4")
                music.audio.write_audiofile("song.wav")
                startfile("music.py")
                
                read_content = None
                content = None

            elif "alexa what day is it" in read_content.lower():
                try:
                    transl_t_orignal_lang = translator.translate("Today is "+datetime.datetime.now().strftime("%A"), dest=language)
                    gTTS(text=transl_t_orignal_lang, lang=language, slow=False).save("daytemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text="Today is "+datetime.datetime.now().strftime("%A"), lang="en", slow=False).save("daytemp18762.mp3")
                playsound("daytemp18762.mp3")
                remove("daytemp18762.mp3")
                read_content = None
                content = None
                
            elif "alexa what time is it" in read_content.lower():
                try:
                    transl4_orignal_lang = translator.translate("It is "+datetime.datetime.now().strftime('%H:%M'), dest=language)
                    gTTS(text=transl4_orignal_lang, lang=language, slow=False).save("timetemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text="It is "+datetime.datetime.now().strftime('%H:%M'), lang="en", slow=False).save("timetemp18762.mp3")
                playsound("timetemp18762.mp3")
                remove("timetemp18762.mp3")
                read_content = None
                content = None
            elif "alexa tell me a joke" in read_content.lower():
                with open("jokes.lock", encoding="utf8") as f:
                    jokes = f.read().splitlines()
                gTTS(text=random.SystemRandom().choice(jokes), lang="en", slow=False).save("joketemp18762.mp3")
                playsound("joketemp18762.mp3")
                remove("joketemp18762.mp3")
                read_content = None
                content = None
            elif "alexa what can you do" in read_content.lower():
                try:
                    trans4_orignal_lang = translator.translate("I can tell you how is the weather like, I can tell you the news, I can play your favorite songs, I can set an alarm for you, I can tell you a joke and much more", dest=language)
                    gTTS(text=trans4_orignal_lang, lang=language, slow=False).save("whattemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text="I can tell you how is the weather like, I can tell you the news, I can play your favorite songs, I can set an alarm for you, I can tell you a joke and much more", lang="en", slow=False).save("whattemp18762.mp3")
                playsound("whattemp18762.mp3")
                remove("whattemp18762.mp3")
                read_content = None
                content = None
            elif "alexa alarm off" in read_content.lower():
                stopalrm = open("alarm.stop", "w")
                stopalrm.close()
                read_content = None
                content = None
            elif "alexa stop" in read_content.lower():
                try:
                    pid = open("music.stop", "r")
                    appid = pid.read()
                    pid.close()
                    kill(int(appid), signal.CTRL_C_EVENT)
                    remove("song.mp3")
                    remove("song.mp4")
                    remove("music.stop")
                except:
                    pass
                read_content = None
                content = None
            elif "alexa calculate" in read_content.lower():
                calculate = " ".join(read_content[read_content.find('calculate'):].replace("calculate ", ""))
                calculatenbsp = calculate.replace(" ", "+")
                question = requests.get(f'https://www.google.com/search?q={calculatenbsp}', headers=headers)
                soup = BeautifulSoup(question.text, 'html.parser')

                try:
                    searchresult = str(str(soup.find("span", class_="qv3Wpe")).replace('<span class="qv3Wpe" id="cwos" jsname="VssY5c">', '')).replace("</span>", "")
                except:
                    # print("Your question's answer wasn't found on the internet!")
                    pass


                if searchresult.find("<") == -1:
                    # print(searchresult)
                    try:
                        tra_orignal_lang = translator.translate("The answer is"+searchresult, dest=language)
                        gTTS(text=tra_orignal_lang, lang=language, slow=True).save("calctemp18762.mp3")
                    except:
                        # print("Language not supported! Using default language instead.")
                        gTTS(text="The answer is"+searchresult, lang="en", slow=True).save("calctemp18762.mp3")
                    playsound("calctemp18762.mp3")
                    remove("calctemp18762.mp3")
                else:
                    # print("an error has occurred please try again later")
                    pass

                del soup
                calculate = None
                calculatenbsp = None
                question = None
                searchresult = None
                read_content = None
                content = None
            elif "alexa tell me a fun fact" in read_content.lower():
                with open("facts.lock", encoding="utf8") as f:
                    facts = f.read().splitlines()
                gTTS(text=random.SystemRandom().choice(facts), lang="en", slow=False).save("facttemp18762.mp3")
                playsound("facttemp18762.mp3")
                remove("facttemp18762.mp3")
                read_content = None
                content = None
            elif "alexa do you love me" in read_content.lower():
                try:
                    tr_orignal_lang = translator.translate("There are many types of love. Ours is just as friends", dest=language)
                    gTTS(text=tr_orignal_lang, lang=language, slow=True).save("lovtemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text="There are many types of love. Ours is just as friends", lang="en", slow=True).save("lovtemp18762.mp3")
                playsound("lovtemp18762.mp3")
                remove("lovtemp18762.mp3")
                read_content = None
                content = None
            elif "alexa do you like me" in read_content.lower():
                try:
                    tr_orignal_lang = translator.translate("Yes I do!", dest=language)
                    gTTS(text=tr_orignal_lang, lang=language, slow=True).save("liketemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text="Yes I do!", lang="en", slow=True).save("liketemp18762.mp3")
                playsound("liketemp18762.mp3")
                remove("liketemp18762.mp3")
                read_content = None
                content = None
            elif "alexa rock paper scissors shoot" in read_content.lower():
                inputted = " ".join(read_content[read_content.find('shoot'):].replace("shoot ", ""))
                if inputted == "k":
                    user = inputted.replace("k", "rock")
                    pass
                elif inputted == "rock":
                    user = inputted
                    pass
                elif inputted == "r":
                    user = inputted.replace("r", "paper")
                    pass
                elif inputted == "paper":
                    user = inputted
                    pass
                elif inputted == "s":
                    user = inputted.replace("s", "scissors")
                    pass
                elif inputted == "scissors":
                    user = inputted
                    pass
                else:
                    raise Exception(user+" is not valid.")

                choice = random.randint(1, 3)
                if choice == 1:
                    bot = "rock"
                elif choice == 2:
                    bot = "paper"
                elif choice == 3:
                    bot = "scissors"
                if choice == 1:
                    if user == "scissors":
                        stat = "you lost"
                    elif user == "rock":
                        stat = "it was a draw"
                    elif user == "paper":
                        stat = "you won"
                elif choice == 2:
                    if user == "scissors":
                        stat = "you won"
                    elif user == "rock":
                        stat = "you lost"
                    elif user == "paper":
                        stat = "it was a draw"
                elif choice == 3:
                    if user == "scissors":
                        stat = "it was a draw"
                    elif user == "rock":
                        stat = "you won"
                    elif user == "paper":
                        stat = "you lost"
                print("I chose "+bot+" and "+stat)
                try:
                    orignal_lang = translator.translate("I chose "+bot+" and "+stat, dest=language)
                    gTTS(text=orignal_lang, lang=language, slow=False).save("rocktemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text="I chose "+bot+" and "+stat, lang="en", slow=False).save("rocktemp18762.mp3")
                playsound("rocktemp18762.mp3")
                remove("rocktemp18762.mp3")
                del choice
                del inputted
                del user
                del stat
                del bot
                read_content = None
                content = None
                
            elif "alexa tell me the news" in read_content.lower():
                html = urlopen("http://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en")
                soup = BeautifulSoup(html.read(), 'lxml')
                news = soup.find('a', class_="DY5T1d RZIKme").contents[0]

                try:
                    tr_orignal_lang = translator.translate(news, dest=language)
                    gTTS(text=tr_orignal_lang, lang=language, slow=True).save("newstemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text=news, lang="en", slow=True).save("newstemp18762.mp3")
                playsound("newstemp18762.mp3")
                remove("newstemp18762.mp3")
                del html
                del soup
                del news
                read_content = None
                content = None

            elif "alexa how many calories are in" in read_content.lower():
                calories_searc = read_content[read_content.find('in'):].replace("in ", "")
                calories_search = calories_searc.replace(" ", "+")
                html = requests.get(f"http://www.google.com/search?q=how+many+calories+are+in+{calories_search}", headers=headers)
                soup = BeautifulSoup(html.text, 'html.parser')
                calories = soup.find('div', class_="Z0LcW an_fna").contents[0]
                weight_unit = soup.find('div', class_="Cc3NMb an-sbl").contents[0]
                kcal_result = calories+" per "+weight_unit
                try:
                    orignal_lang = translator.translate(kcal_result, dest=language)
                    gTTS(text=orignal_lang, lang=language, slow=False).save("kcaltemp18762.mp3")
                except:
                    # print("Language not supported! Using default language instead.")
                    gTTS(text=kcal_result, lang="en", slow=False).save("kcaltemp18762.mp3")
                playsound("kcaltemp18762.mp3")
                remove("kcaltemp18762.mp3")
                del html
                del req
                del soup
                del calories
                del calories_search
                del kcal_result
                del weight_unit
                read_content = None
                content = None

            else:
                # print(f"{read_content} is not familiar")
                pass
        except:
           # print("error")
           pass
