from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.utils.encoding import filepath_to_uri
import speech_recognition as sr
import moviepy.editor as mp


# Create your views here.
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        path = 'media/'+uploaded_file.name
        fs.save(path, uploaded_file)
        video = mp.VideoFileClip(path)
        path = path+'.wav'
        video.audio.write_audiofile(path)
        fs.delete(path.replace('.wav',''))
        text = conversion(path)
        fs.delete(path)
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


