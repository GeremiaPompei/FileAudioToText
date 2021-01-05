from django.core.files.storage import FileSystemStorage
from django.utils.encoding import filepath_to_uri
from django.shortcuts import redirect
import speech_recognition as sr
import moviepy.editor as mp
from django.http import HttpResponse
from django.http import FileResponse
import os
import json

def redirect_view(request):
    return redirect('/static/index.html')

def uploadVideo(request):
    if request.method == 'POST':
        response_data = {}
        d = 'media'
        fs = FileSystemStorage()
        uploaded_file = request.FILES['document']
        path = ''
        try:
            path = os.path.join(d, uploaded_file.name)
            path = fs.save(path, uploaded_file)
            response_data['name'] = path
            response_data['duration'] = int(mp.VideoFileClip(path).duration)
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            if(os._exists(path)):
                os.remove(path)
            return 'Error!'

def removeVideo(request):
    if request.method == 'POST':
        path = str(request.POST['name'])
        os.remove(path)
        return 'Success!'

def splitVideo(request):
    if request.method == 'POST':
        summ = 30
        pathv = ''
        pathc = ''
        try:
            pathv = request.POST['name']
            index = int(request.POST['index'])
            video = mp.VideoFileClip(pathv)
            duration = int(video.duration)
            if index > duration:
                return 'Error!'
            if index+summ <= duration:
                clip=video.subclip(index,index+summ)
            else:
                clip=video.subclip(index,duration)
            pathc='media/tmp_'+pathv.replace('media/','')
            clip.write_videofile(pathc,fps=1)
            response = FileResponse(open(pathc, 'rb'))
            os.remove(pathc)
            return response
        except Exception as e:
            if(os._exists(pathc)):
                os.remove(pathc)
            if(os._exists(pathv)):
                os.remove(pathv)
            return 'Error!'

def videoToAudio(request):
    if request.method == 'POST':
        fs = FileSystemStorage()
        d = 'media'
        pathv = ''
        patha = ''
        try:
            uploaded_file = request.FILES['document']
            pathv = os.path.join(d, uploaded_file.name)
            fs.save(pathv, uploaded_file)
            video = mp.VideoFileClip(pathv)
            patha = pathv+'.wav'
            video.audio.write_audiofile(patha)
            fs.delete(pathv)
            response = FileResponse(open(patha, 'rb'))
            os.remove(patha)
            return response
        except Exception as e:
            if(os._exists(pathv)):
                os.remove(pathv)
            if(os._exists(patha)):
                os.remove(patha)
            return 'Error!'

def audioToText(request):
    if request.method == 'POST':
        response_data = {}
        d = 'media'
        fs = FileSystemStorage()
        path = ''
        try:
            uploaded_file = request.FILES['document']
            path = os.path.join(d, uploaded_file.name)
            fs.save(path, uploaded_file)
            text = conversion(path)
            fs.delete(path)
            response_data['text'] = text
        except Exception as e:
            if(os._exists(path)):
                os.remove(path)
            response_data['text'] = 'Error!'
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


