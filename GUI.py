# Codes by Jiabao Qiu
from Tkinter import *
import tkMessageBox
from random import randint
import webbrowser as controller
import App as app
import train as t

notify = ["You might also like...","Do you mean...","How about..."]

# Print the results for the user input
def getArtists(userInput):
    output.forget()
    label.forget()
    if (userInput==''):
        tkMessageBox.showinfo("Oops!", "Please enter the full name of an artist.")
    else:
        app.generateTopTracks(userInput)
        results = t.findArtists()
        n = 0
        out = ""
        for result in results:
            out = out+results[n]+"\n"
            n=n+1
        out = out[:-1]
        label['text'] = notify[randint(0,2)]
        output['text'] = out
        random_name = results[randint(0,9)]
        check_it_out['command'] = lambda: controller.open_new_tab('http://www.google.com/search?q='+random_name)
    return 0

# Rests are the widgets

black = '#191414'
white = '#FFFFFF'

root = Tk()
root.winfo_toplevel().title("Similar Artists")
root.resizable(False,False)
root.configure(bg=white)

hint = Label(root,text="Enter the name of your favorite artist!",bg=white,fg=black,font='Helvetica')
hint.grid(row=0,columnspan=2)

entry = Entry(root,highlightbackground=white,fg=black,font='Helvetica')
entry.grid(row=1,column=0)

output = Label(root,text="\n\n\n\n\n\n\n\n",bg=white,fg=black,font='Helvetica')
output.grid(row=3,columnspan=2)
label = Label(root,text="",bg=white,fg=black,font='Helvetica')
label.grid(row=2,columnspan=2)

start = Button(root,highlightbackground=white,fg=black,text='Find artists!',font='Helvetica',
               command = lambda: getArtists(entry.get()))
start.grid(row=1,column=1)

check_it_out = Button(root,highlightbackground='white',fg='black',text='Search on Google',
                      font='Helvetica',command=lambda: tkMessageBox.showinfo("Oops!", "We didn't find any artists related."))
check_it_out.grid(row=4,columnspan=2)

mainloop()
root.destroy()
