import moviepy.editor as mp

print('Aggiungi percorso video: ')
video=mp.VideoFileClip(input())
video.audio.write_audiofile('vc_audio.wav')
