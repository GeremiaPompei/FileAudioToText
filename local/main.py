import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from sbobinator import *
            
root=Tk()
root.title('SBOBINATOR')
#root.withdraw()

filename = ''
def choice():
    global filename
    filename = askopenfilename()

def sbobina(output, filename, language):
    try:
        output.delete('1.0', END)
        name = video_to_audio(filename)
        text = conversion(name, language.get())
        output.insert(END, text)
        if name == '' or name != filename:
            os.remove(name)
    except Exception as e:
        output.insert(END, e)

choices = ['it-IT', 'en-US']
language = StringVar(root)
language.set(choices[0])

text = Text()
text.pack()
OptionMenu(root, language, *choices).pack()
Button(root, text ="File", command = lambda:choice()).pack()
Button(root, text ="Sbobina", command = lambda:sbobina(text, filename, language)).pack()

root.mainloop()