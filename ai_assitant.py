import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime

r = sr.Recognizer()
phone_numbers = {"king": "0374583408", "bin": "0942021380", "dat": "44402042004"}
bank_account = {"king": "0374583408", "bin": "0942021380", "dat": "44402042004"}

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Giọng nam hoặc nữ
    engine.say(command)
    engine.runAndWait()

def listen():
    """Lắng nghe lệnh từ người dùng."""
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('Listening... Ask now...')
            speak("Ask me anything you want")
            audioin = r.listen(source)
            my_text = r.recognize_google(audioin).lower()
            print("You said:", my_text)
            return my_text
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
    except sr.RequestError as e:
        speak(f"Sorry, there was a request error: {e}")
    return ""

def process_command(command):
    """Xử lý lệnh người dùng."""
    if 'play' in command:
        song = command.replace('play', "").strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif 'date' in command or 'day' in command:
        today = datetime.date.today()
        speak(f"Today is {today}")
        print(today)

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Current time is {current_time}")
        print(current_time)

    elif "phone number" in command:
        for name in phone_numbers:
            if name in command:
                speak(f"{name}'s phone number is {phone_numbers[name]}")
                return
        speak("I can't find that phone number.")

    elif 'bank account' in command:
        for account in bank_account:
            if account in command:
                speak(f"{account}'s bank account number is {bank_account[account]}")
                return
        speak("I can't find that bank account.")

    elif 'stop' in command:
        speak("Thank you for using!")
        exit()  # Kết thúc chương trình

    else:
        try:
            info = wikipedia.summary(command, sentences=1)
            speak(info)
        except wikipedia.exceptions.DisambiguationError:
            speak("The search term is ambiguous. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("The page does not exist. Try another term.")

def main():
    while True:
        command = listen()
        if command:
            process_command(command)

# Chạy chương trình chính
main()
