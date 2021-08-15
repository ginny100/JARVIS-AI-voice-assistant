# Import modules
import pyttsx3 # Text to speech module
import datetime # Date and time module
import speech_recognition as sr # Speech Recognition module
import wikipedia # Wikipedia search module
import smtplib # SMTP client session object used to send mail to any Internet machine with an SMTP or ESMTP listener daemon
import webbrowser as wb # Web browser module
import os # Operating System module
import pyautogui # This module allows you to take a screenshot
import psutil # Process and system utilities
import pyjokes # Module supporting the jokes function

# Init
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
newVoiceRate = 190 # set the voice rate
engine.setProperty('rate', newVoiceRate)

# The speak function - speaks the text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# The time function - gets the current time
def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S") # 12-hour format
    #Time = datetime.datetime.now().strftime("%H:%M:%S") # 24-hour format
    speak("It's")
    speak(Time)
    speak("now")

# The date function - gets the current date
def date():
    # Get the weekday
    today_weekday = datetime.datetime.today().weekday() + 1 # starting from 0 -> add 1
    week = { 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday' }
    if today_weekday in week.keys():
        weekday = week[today_weekday]
        #print(weekday)
    # Get the date 
    today_date = datetime.datetime.now().day
    dates = {   1: 'the first', 2: 'the second', 3: 'the third', 4: 'the fourth', 5: 'the fifth', 
                6: 'the sixth', 7: 'the seventh', 8: 'the eighth', 9: 'the ninth', 10: 'the tenth',
                11: 'the eleventh', 12: 'the twelfth', 13: 'the thirteenth', 14: 'the fourteenth', 15: 'the fifteenth', 
                16: 'the sixteenth', 17: 'the seventeenth', 18: 'the eighteenth', 19: 'the nineteenth', 20: 'the twentieth', 
                21: 'the twenty first', 22: 'the twenty second', 23: 'the twenty third', 24: 'the twenty fourth', 25: 'the twenty fifth',
                26: 'the twenty sixth', 27: 'the twenty seventh', 28: 'the twenty eighth', 29: 'the twenty ninth', 30: 'the thirtieth', 
                31: 'the thirty-first'  }
    if today_date in dates.keys():
        date = dates[today_date]
        #print(date)
    # Get the month
    today_month = datetime.datetime.now().month
    months = {  1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December' }
    if today_month in months.keys():
        month = months[today_month]
        #print(month)
    # Get the year
    year = str(datetime.datetime.now().year)
    # Speak the full date of today
    speak("Today is" + weekday + month + date + year)

# The greeting function - greets the user
def wishme():
    speak("Welcome back friend")
    hour = datetime.datetime.now().hour
    # Greetings
    if hour >= 6 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    elif hour >= 18 and hour < 24:
        speak("Good evening")
    else:
        speak("Good night")
    speak("I'm Jarvis. How can I help you?")

# The take command function - gets commands from user
def take_command():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key (To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`.)
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Unable to understand audio")
        speak("Say that again please...")
        return "None"
    except sr.RequestError as e:
        print(e)
        speak("Say that again please...")
        return "None"
    return data

# The send email - sends an email
def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("test@gmail.com", "123test") # Your email credential
    server.sendmail("text@gmail.com", to, content)
    server.close()

# The screenshot function - captures the screen
def screenshot():
    capture = pyautogui.screenshot()
    capture.save("./screenshots/ss.png") # Save the sceenshot as a .png file

# The CPU function - gets CPU and battery
def cpu():
    # Get the CPU usage
    usage = str(psutil.cpu_percent())
    print(usage)
    speak("CPU is at" + usage)
    # Get the battery percentage
    battery = psutil.sensors_battery
    print(battery)
    speak("battery is at" + battery.percent)

# The jokes function - tells a joke
def jokes():
    speak(pyjokes.get_joke())

# Main function
if __name__ == '__main__':
    wishme()
    while True:
        query = take_command().lower()
        print(query)
        if "time" in query:
            time()
        elif "date" in query:
            date()
        elif "wikipedia" in query:
            speak("Searching...")
            print("Searching...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences = 2)
            speak(result)
        elif "send email" in query:
            try:
                speak("What should I say?")
                content = take_command()
                to = "xyz@gmail.com" # receiver
                send_email(to, content)
                speak(content)
            except Exception as e:
                speak(e)
                speak("Unable to send the email")
        elif "search in chrome" in query:
            speak("What should I search for?")
            # Location of your google chrome driver in your machine
            chromepath = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome %s" # MacOS
            #chromepath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s" # Windows
            search = take_command().lower()
            wb.get(chromepath).open_new_tab(search + ".com")
        elif "logout" in query:
            os.system("shutdown - l")
        elif "shutdown" in query:
            os.system("shutdown /s /t 1")
        elif "restart" in query:
            os.system("shutdown - /r /t 1")
        elif "play songs" in query:
            songs_dir = "./playlist" # Path of your music file
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))
        elif "remember that" in query:
            speak("What should I remember?")
            data = take_command()
            speak("I have to remember that" + data)
            remember = open("data.txt", "w") # open the data.txt file
            remember.write(data) # write in the file
            remember.close() # close the file
        elif "do you know anything" in query:
            remember = open("data.txt", "r")
            speak("You told me to remember that" + remember.read())
        elif "screenshot" in query:
            screenshot()
            speak("The screen has been captured")
        elif "cpu" in query:
            cpu()
        elif "joke" in query:
            jokes()
        elif "stop" in query:
            quit()
        