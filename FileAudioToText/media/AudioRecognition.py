import speech_recognition as sr

def main():
	print("Inserisci path del file audio: ")
	sound = input()
	r = sr.Recognizer()
	with sr.AudioFile(sound) as source:
		r.adjust_for_ambient_noise(source)
		print("Converting audio file to text...")
		r.pause_threshold = 1800.0
		audio = r.listen(source)
		try:
			print("Converted audio is: \n"+r.recognize_google(audio, language="it-IT"))
		except Exception as e:
			print(e)
main()
