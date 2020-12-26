from django.core.files.storage import FileSystemStorage
from django.utils.encoding import filepath_to_uri
from django.shortcuts import redirect
from rest_framework.response import Response
import speech_recognition as sr
import moviepy.editor as mp
from django.http import HttpResponse
import os
import json

def redirect_view(request):
    return redirect('/static/index.html')

# Create your views here.
def upload(request):
    if request.method == 'POST':
        response_data = {}
        d = 'media'
        fs = FileSystemStorage()
        try:
            uploaded_file = request.FILES['document']
            path = os.path.join(d, uploaded_file.name)
            fs.save(path, uploaded_file)
            video = mp.VideoFileClip(path)
            path = path+'.wav'
            video.audio.write_audiofile(path)
            fs.delete(path.replace('.wav',''))
            text = conversion(path)
            fs.delete(path)
            response_data['text'] = text
        except Exception as e:
            if os._exists(d):
                for f in os.listdir(d):
                    os.remove(os.path.join(d,f))
            response_data['text'] = 'error'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

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


