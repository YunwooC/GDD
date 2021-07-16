from tkinter import *

def main():

    # main window
    window = Tk()
    window.title('Growing Degrees Day Simulator')
    window.geometry('1440x1024')
    
    canvas = Canvas(window,width=1440,height=1024,bg='white')
    nav_graph=Button(window, text="Graph",width=30,height=3)
    nav_info=Button(window, text="How to Use", width=30, height=3)
    minimize=Button(window, text="—", width=17, height=2)
    close=Button(window, text="X", width=17, height=2)
    maximize=Button(window, width=17, height=2)
    

    # header
    canvas.create_line(1067, 0, 1067, 47, width=2)
    canvas.create_line(1196, 0, 1196, 47, width=2)
    canvas.create_line(1325, 0, 1325, 47, width=2)
    canvas.create_line(1067, 0, 1067, 47, width=2)

    # title
    canvas.create_line(0, 47, 1440, 47, width=2)
    canvas.create_line(0, 302, 1440, 302, width=2)
    
    canvas.pack()
    nav_graph.place(x=0, y=247)
    nav_info.place(x=175, y=247)
    minimize.place(x=1067, y=0)
    close.place(x=1325, y=0)
    maximize.place(x=1196, y=0)

    
    # starting the program
    window.mainloop()

main()
