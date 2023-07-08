import speech_recognition as sr
r = sr.Recognizer()
from gtts import gTTS

async def speechToText(audio_file_path):
    with sr.AudioFile(audio_file_path) as source:
        # listen for the data (load audio to memory)
        audio = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_whisper(
                        audio,
                        model="medium.en",
                        show_dict=True,
                    )["text"]
        return text
async def textToSpeech(text, audio_file_path):
    tts = gTTS(text, lang='en', tld='com.au')
    tts.save(audio_file_path)
    return audio_file_path