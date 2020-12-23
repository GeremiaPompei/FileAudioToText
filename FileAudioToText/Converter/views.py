from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.utils.encoding import filepath_to_uri
import speech_recognition as sr

# Create your views here.
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pathAudio = 'media/'+uploaded_file.name
        fs.save(pathAudio, uploaded_file)
        text = conversion(pathAudio)
        fs.delete(pathAudio)
        return render(request,"upload.html", {"codedtxt": "data:text/plain;charset=utf-8,"+filepath_to_uri(text), "download": "Download", "txt": text})
    return render(request, 'upload.html')

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


