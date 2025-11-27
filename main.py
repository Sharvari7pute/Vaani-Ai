import speech_recognition as sr
import pyttsx3
from openai import OpenAI

client = OpenAI(api_key=" your api key ")  # ADD YOUR KEY

# ---------------------- SPEAK FUNCTION ----------------------
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---------------------- AI LANGUAGE DETECTION ----------------------
def detect_language_with_ai(text):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Detect only the language code like hi, mr, en, ta, te, bn."},
            {"role": "user", "content": text}
        ]
    )
    return res.choices[0].message.content.strip()

# ---------------------- AI REPLY ----------------------
def ai_reply(user_text, lang_code):
    prompt = f"Reply in the same language ({lang_code}). User said: {user_text}"

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Vaani AI."},
            {"role": "user", "content": prompt}
        ]
    )
    return r.choices[0].message.content

# ---------------------- MAIN ----------------------
def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("\nVAANI AI Ready — Multilingual Mode \n")

    while True:
        with mic as source:
            print("Listening…")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # STEP 1: FREE GOOGLE SPEECH TO TEXT
            text = recognizer.recognize_google(audio)
            print("User:", text)

            # STEP 2: AI LANGUAGE DETECTION
            lang_code = detect_language_with_ai(text)
            print("Language detected:", lang_code)

            # STEP 3: AI REPLY IN SAME LANGUAGE
            reply = ai_reply(text, lang_code)
            print("Vaani AI:", reply)

            # STEP 4: SPEAK RESPONSE
            speak(reply)

        except Exception as e:
            print("Error:", e)
            speak("Sorry, I did not understand.")

if __name__ == "__main__":
    main()
