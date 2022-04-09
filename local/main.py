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

def sbobina(output, filepath, language):
    try:
        output.delete('1.0', END)
        dir = filepath.rsplit('/', 1)[0] + "/sbobonator_" + random_name() + "/"
        os.mkdir(dir)
        name = video_to_audio(dir, filepath)
        gen = conversion(dir, name, language.get(), 1)
        text = ""
        while text is not None:
            text = next(gen, None)
            output.insert(END, text)
    except Exception as e:
        print(f"[FINAL EXCEPTION: {e}]")
    try:
        for path in os.listdir(dir):
            os.remove(dir + path)
        os.rmdir(dir)
    except Exception as e:
        print(e)

choices = ['it-IT', 'en-US']
language = StringVar(root)
language.set(choices[0])

text = Text()
text.pack()
OptionMenu(root, language, *choices).pack()
Button(root, text ="File", command = lambda:choice()).pack()
Button(root, text ="Sbobina", command = lambda:sbobina(text, filename, language)).pack()

root.mainloop()