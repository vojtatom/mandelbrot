#!/usr/bin/env python3
 
from tkinter import *
from time import sleep

class MainImage():

    def __init__(self, main):

        # ini values, except for root, can be adjusted
        self.root = main
        self.aspect = 4 / 3 # aspect ratio of the window (and pictures)
        self.width = 600 # width of the widnow
        self.width_graph = self.def_wg = 4 #width of the displayed area on the x-axes
        self.center_w = self.def_w = -1 #center on x-axes
        self.center_h = self.def_h = 0 # center on y-axes
        self.iterations = self.def_i = 35 #initial number of iterations
        self.color_scheme = (0, 1/3, 2/3) #color scheme... values should be between 0 and 1, RGB, eg. (0, 1/3, 2/3) means that R

        #some other useful values
        self.height = round(self.width / self.aspect)
        self.height_graph = self.def_hg = round(self.width_graph / self.aspect)

        #canvas and label ini
        self.canvas = Canvas(main, width=self.width, height=self.height, highlightthickness=0)
        self.my_image = self.canvas.create_image((self.width, self.height), anchor=SE)
        self.label = Label(main, borderwidth=5, bg="black", fg="white")

        #center lines and text
        self.canvas.create_line(self.width / 2, 0, self.width / 2, self.height)
        self.canvas.create_line(0, self.height / 2, self.width, self.height / 2)

        #update label and image
        self.update_text()
        self.update_image(False) 

        #keys and actions
        self.canvas.bind("<Key>", self.reset)
        self.canvas.bind("<Button-1>", self.zoomin)
        self.canvas.bind("<Button-3>", self.zoomout)
        self.canvas.pack()
        self.label.pack(fill=X, anchor=W)

    def zoomin(self, event):
        self.canvas.focus_set()
        self.adjust_center(event)
        self.width_graph /= 2
        self.height_graph /= 2
        self.iterations = round( self.iterations * 1.2 )
        self.update_image()

    def zoomout(self, event):
        self.adjust_center(event)
        self.width_graph *= 2
        self.height_graph *= 2
        self.iterations = round( self.iterations / 1.2 )
        self.update_image()

    def reset(self, event) :
        if event.char == 'r' :
            self.center_w, self.center_h = self.def_w, self.def_h
            self.root.title("Reseting...")
            self.root.update()
            self.width_graph, self.height_graph = self.def_wg, self.def_hg
            self.iterations = self.def_i
            self.update_image()
        elif event.char == 's' :
            self.root.title("saving image...")
            try :
                with open('mandelbrot.pbm', 'wb') as file :
                    file.write(self.data['data'])
                    file.close()
                self.label.config(text="image saved!")
            except :
                self.label.config(text="image not saved!")
            self.label.update()
            sleep(1)
            self.root.title("saving image...")
            self.update_text()

    def adjust_center(self, event) :
        self.center_w = (self.center_w - self.width_graph / 2 ) + (event.x / ( self.width / self.width_graph))
        self.center_h = (self.center_h + self.height_graph / 2 ) - (event.y / ( self.height / self.height_graph))
        self.root.title("Updating...")
        self.root.update()

    def update_image(self, show_progress = True) :
        rows = calculate_matrix(self, show_progress)
        image = create_bytearray(self, rows)
        self.data = PhotoImage(data=bytes(image))
        # change image
        self.canvas.itemconfig(self.my_image, image=self.data)
        self.update_text()
        self.canvas.update()

    def update_text(self) :
        self.root.title("mandelbrot - " + str(self.iterations) + " iterations")
        text = "center: x " + "%.4f" % self.center_w + " y " + "%.4f" % self.center_h + " | width of the graph: " + str(self.width_graph)
        self.label.config(text=text)

    def show_progress(self, value) :
        text = "recalculating image " + str(value) + "%"
        self.label.config(text=text)
        self.label.update()

def iterate(z, c) :
    return z*z + c

def color_steps(c, iterations) :
    z = complex(0,0)
    for i in range(iterations) :
       z = iterate(z, c)
       if abs(z) > 2 :
         break
    return i

def update_progress(i, pre_value, image) :
    max = image.height
    value = round(100 * i / max)

    if(value > pre_value) :
        image.show_progress(value)
    return value

def calculate_matrix(image, show_progress = True) :
    rows, columns = [], []
    
    start_w = image.center_w - image.width_graph / 2
    start_h = image.center_h + image.height_graph / 2

    step_w = image.width_graph / image.width
    step_h = image.height_graph / image.height
    progress = -1
    for i in range(image.height) :
        if show_progress :
            progress = update_progress(i, progress, image)
        for j in range(image.width) :
            number = complex(start_w + j * step_w, start_h - i * step_w)
            columns.append(color_steps(number, image.iterations))
        rows.append(columns)
        columns = []

    return rows

def create_bytearray(image, rows) :
    image_data = bytearray()
    image_data += bytes('P6\n' + str(image.width) + ' ' + str(image.height) + '\n255\n', "ASCII")

    for c, x in enumerate(rows) :
        for f in x :
            image_data.append( color(image.color_scheme[0], image.iterations, f) )
            image_data.append( color(image.color_scheme[1], image.iterations, f) )
            image_data.append( color(image.color_scheme[2], image.iterations, f) )
    return image_data

def color(shift, iterations, value) :
    if shift < (value / iterations) :
        x = (value * 255 * 3) / (iterations)
        if x > 255 :
            return 255
        else :
            return round(x)
    return 0



#----------------------------------------------------------------------------------------------------------------------------------------
print("\nNAVIGATION:\nzoom in - left click,\nzoom out - right click,\nreset view - press r,\nsave image - press s\n")
print("please wait until the picture loads...")

# UPDATE WINDOW 
root = Tk()
root.resizable(width=False, height=False)
MainImage(root)
 
root.mainloop()
