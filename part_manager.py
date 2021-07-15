from tkinter import *

def main():

    # main window
    window = Tk()
    window.title('Growing Degrees Day Simulator')
    window.geometry('1440x1024')
    
    canvas = Canvas(window,width=1440,height=1024,bg='white')

    # header
    canvas.create_line(1067, 0, 1067, 47, width=2)
    canvas.create_line(1196, 0, 1196, 47, width=2)
    canvas.create_line(1325, 0, 1325, 47, width=2)
    canvas.create_line(1067, 0, 1067, 47, width=2)

    # title
    canvas.create_line(0, 47, 1440, 47, width=2)
    canvas.create_line(0, 302, 1440, 302, width=2)

    canvas.pack()

    # starting the program
    window.mainloop()

main()
