try:
    import speech_recognition as sr
    from gtts import gTTS
    from pydub.playback import play
    from pydub import AudioSegment
    import requests
    import geocoder
    from func_timeout import func_timeout, FunctionTimedOut
    from random import choice
    from ast import literal_eval
    from os import system, name, path, remove
    import webbrowser as wb
    from time import sleep
    from datetime import datetime


except ImportError:
    print("Please install the pre-requisites")
    quit()


data = {}
microphone = None
greetings = [
    "Namaste",
    "Ram Ram",
    "Jai Jinendra",
    "Jai Shri Krishna",
    "Satsriaakaal",
    "Hello",
    "Hi",
]
what_am_i_doing_list = [
    "I am talking to you right now!",
    "I know everything, so i am chilling!",
    "I'm drinking tea.",
    "I'm preparing for JEE Advance for the past 10 years but cannot clear it!!",
    "Damn, you woke me up! I was sleeping bruh.",
]
how_am_i_list = [
    "Talking to you makes me feel great!",
    "I'm depressed. Anyways...",
    "I'm great but you should be studying right now...",
    "I don't have any feelings, bruh.",
    "I think I will not be able to make it through the day!",
]

covid_api_url = "https://api.rootnet.in/covid19-in/stats/latest"
joke_api_url = "https://official-joke-api.appspot.com/jokes/random"


def cls():
    system("cls") if name == "nt" else system("clear")


def get_mics():
    mics = sr.Microphone.list_microphone_names()
    new_list_of_mics = []
    for id, mic in enumerate(mics, start=0):
        if mic == " - Output":
            break
        elif mic == " - Input":
            continue
        else:
            new_list_of_mics.append(mic)
            print(f"{id} - {mic}")
    speak("Enter the number of the mic you want to use? ")
    which_mic = input("? ")

    if which_mic.isnumeric():
        return int(which_mic)
    else:
        get_mics()


def get_city():
    g = geocoder.ip("me")
    return g.city


def save_to_file(data):
    with open("config.txt", "w") as file:
        file.write(str(data))


def is_internet_active():
    try:
        _ = requests.get("https://www.google.com", timeout=1)
        return True
    except requests.ConnectionError:
        return False


def exitam():
    speak("It was nice talking to you, hope to see you soon!")
    remove("speech.mp3")
    quit()


def listen():
    def audio_equals_r_dot_listen(r, source):
        print("Listening..")
        audio = r.listen(source)
        return audio

    m = data["mic"]
    r = sr.Recognizer()
    while True:
        with sr.Microphone(device_index=m) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = func_timeout(20, audio_equals_r_dot_listen, args=(r, source))
                break
            except FunctionTimedOut:
                print("Could you say that again?")
                continue
    try:
        print(r.recognize_whisper(audio))
        return r.recognize_whisper(audio)
    except sr.UnknownValueError:
        speak("Voice not clear! Please repeat!")
    except sr.RequestError:
        speak("Server didn't respond!")


def speak(text):
    print(text)
    if name == "nt":
        ffmpeg = "ffmpeg.exe"
        AudioSegment.converter = ffmpeg
    else:
        pass
    mp3 = "speech.mp3"
    txt2speech = gTTS(text=text, lang="en-in")
    txt2speech.save(mp3)
    play(AudioSegment.from_mp3(mp3))


def web_search(q):
    exceptions = ["search for", "search", "tell me about", "what is"]
    query = ""
    for exception in exceptions:
        if exception in q:
            q = q.replace(exception, "")
    query = q.split()
    parsed_query = "+".join(query)
    google_url = f"https://www.google.com/search?q={parsed_query}"
    speak("Here's what I found!")
    wb.open_new_tab(google_url)


def india_covid():
    try:
        res = requests.get(covid_api_url)
        res.raise_for_status()
    except (requests.HTTPError, Exception, requests.exceptions.ConnectionError):
        print("Please check your network connection.")
    else:
        rJSON = res.json()
        data = rJSON["data"]
        speak(
            f"Total cases of COVID-19 in India are {data['summary']['total']}; whereas {data['summary']['discharged']} have been discharged and {data['summary']['deaths']} people died!"
        )


def jokeAPI():
    try:
        res = requests.get(joke_api_url)
        res.raise_for_status()
    except (requests.HTTPError, Exception, requests.exceptions.ConnectionError):
        print("Please check your network connection.")
    else:
        json = res.json()
        speak(json["setup"])
        sleep(1)
        speak(json["punchline"])


def weather_api():
    req = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={get_city()}&units=metric&appid=4153fb471c99f9f74d20c091db20bd22"
    )
    res = req.json()
    main_obj = res["main"]
    wind = res["wind"]
    speak(f"The current weather in {get_city()} is {res['weather'][0]['main']}")
    speak(f"The current temperature is {main_obj['temp']} degree celsius")
    speak(f"The minimum temperature is {main_obj['temp_min']} degree celsius")
    speak(f"The maximum temperature is {main_obj['temp_max']} degree celsius")
    speak(f"Visibility is {res['visibility']}")
    speak(f"Wind speed is {wind['speed']} kilometres per hour")
    speak(f"Wind degree is {wind['deg']} degrees")
    pass


def date_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y. And the time is %H:%M:%S!")
    speak(f"Today is {dt_string}")


def hi():
    speak(f"*blushing* {choice(greetings)} ji!")


def show_abilities():
    speak("I'm opening a webpage, there you can see the commands!")
    wb.open_new_tab("https://github.com/prayag2/VIST#commands-that-can-be-used-for")


def solve():
    while True:
        try:
            speak("Enter an expression.")
            exp = input("? ")
            eval_exp = eval(exp)
        except:
            speak("Please enter a correct expression!")
            continue
        else:
            speak(str(eval_exp))
            break


def pronunciation():
    while True:
        speak("Which word's pronunciation do you want to check?")
        word = input("? ").lower()
        if word.isalpha():
            speak(f"This word is pronounced as {word}!")
        else:
            speak(f"Please enter a correct word {data['name']}!")


def feedback():
    speak("Please send your feedback:")
    speak("axityatrips@gmail.com")
    speak("prayagjain2@gmail.com")


def countdown():
    sec = int(input("Enter seconds for the countdown\n? "))
    while sec > 0:
        print(sec)
        sleep(1)
        sec -= 1


def what_am_i_doing():
    speak(choice(what_am_i_doing_list))


def how_am_i():
    speak(choice(how_am_i_list))


def cmd_prompt():
    commands = [
        {
            "trigger_on": [
                "what can you do",
                "help",
                "what you can do",
                "what are your abilities",
            ],
            "func": show_abilities,
            "args_required": False,
        },
        {
            "trigger_on": [
                "covid status",
                "covid",
                "corona",
                "corona virus",
                "covid-19 status",
                "corona status",
                "corona virus status",
                "covid-19",
                "coronavirus",
            ],
            "func": india_covid,
            "args_required": False,
        },
        {
            "trigger_on": ["calculate", "solve", "calculator", "evaluate"],
            "func": solve,
            "args_required": False,
        },
        {
            "trigger_on": [
                "search",
                "web search",
                "web",
                "search for",
                "tell me about",
                "what is",
            ],
            "func": web_search,
            "args_required": True,
        },
        {
            "trigger_on": [
                "crack a joke",
                "tell me a joke",
                "joke",
                "fun",
                "laugh",
                "make me laugh",
                "tell me something funny",
            ],
            "func": jokeAPI,
            "args_required": False,
        },
        {
            "trigger_on": ["bye", "exit", "good bye"],
            "func": exitam,
            "args_required": False,
        },
        {"trigger_on": ["date", "time"], "func": date_time, "args_required": False},
        {"trigger_on": greetings, "func": hi, "args_required": False},
        {
            "trigger_on": ["what are you doing", "doing"],
            "func": what_am_i_doing,
            "args_required": False,
        },
        {
            "trigger_on": ["how are you", "how have you been doing", "how is it going"],
            "func": how_am_i,
            "args_required": False,
        },
        {
            "trigger_on": [
                "pronunciation",
                "how is this word pronounced",
                "pronounced",
                "how do you speak this",
            ],
            "func": pronunciation,
            "args_required": False,
        },
        {
            "trigger_on": ["support", "feedback"],
            "func": feedback,
            "args_required": False,
        },
        {"trigger_on": ["countdown"], "func": countdown, "args_required": False},
        {"trigger_on": ["weather"], "func": weather_api, "args_required": False},
    ]
    speak("How may I help you?")
    while True:
        try:
            inp = listen().lower()
            # inp = input("? ").lower()
        except AttributeError:
            continue
        else:
            internet_search = True
            for dictionary_index in range(len(commands)):
                for keysentence in commands[dictionary_index]["trigger_on"]:
                    if keysentence.lower() in inp:
                        if commands[dictionary_index]["args_required"]:
                            commands[dictionary_index]["func"](inp)
                        else:
                            commands[dictionary_index]["func"]()
                        internet_search = False
                        break
                else:
                    continue
            else:
                if internet_search:
                    web_search(inp)


def main():
    cls()
    global data

    def save_to_file(data):
        with open("config.txt", "w") as file:
            file.write(str(data))

    def save_name(name_key, name_value):
        data[str(name_key)] = name_value
        save_to_file(data)

    def save_mic(mic_key, mic_value):
        data[str(mic_key)] = mic_value
        save_to_file(data)

    if path.isfile("config.txt"):
        with open("config.txt", "r") as file:
            try:
                data = literal_eval(file.read())
            except:
                speak("Your data is corrupted. Clearing cache...")
                remove("config.txt")
                main()
            else:
                m = get_mics()
                save_mic("mic", m)
                speak(f"{choice(greetings)}, {data['name']}!")
    else:
        m = get_mics()
        save_mic("mic", m)
        speak(
            "Hey there! I am Vist, your virtual and personal assistant! Can you please enter your name?"
        )
        name = input("? ")
        speak(f"That's a nice name, {name}!")
        save_name("name", name)


if __name__ == "__main__":
    if is_internet_active():
        main()
        cmd_prompt()
    else:
        print("Connect to a working network and try again!")
