from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.utils.encoding import filepath_to_uri
import speech_recognition as sr
import moviepy.editor as mp
import os

# Create your views here.
def upload(request):
    print('ok')
    if request.method == 'POST':
        fs = FileSystemStorage()
        try:
            if not os._exists('media'):
                os.mkdir('media')
            uploaded_file = request.FILES['document']
            path = 'media/'+uploaded_file.name
            fs.save(path, uploaded_file)
            video = mp.VideoFileClip(path)
            path = path+'.wav'
            video.audio.write_audiofile(path)
            fs.delete(path.replace('.wav',''))
            text = conversion(path)
            fs.delete(path)
            return render(request, text)
        except Exception as e:
            for f in os.listdir('media'):
                os.remove('media/'+f)

def conversion(sound):
	r = sr.Recognizer()
	with sr.AudioFile(sound) as source:
		r.adjust_for_ambient_noise(source)
		r.pause_threshold = 1800.0
		audio = r.listen(source)
		try:
			return r.recognize_google(audio, language="it-IT")
		except Exception as e:
			return e


