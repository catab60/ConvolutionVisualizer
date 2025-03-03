from tkinter import *
import threading
import math
import colorsys
import time

class ConvolutionVisualizer():
    def __init__(self, root):
        self.root = root
        self.root.title("Convolution Visualizer")
        self.root.geometry("1400x800")
        self.root.maxsize(1400, 800)
        self.root.minsize(1400, 800)

        self.kernelSize = 4
        self.kernelPos = (0, 0)
        self.prevKernelPos = (0, 0)
        self.cells = []
        self.outputcells = []
        self.padding = 2 * 2
        self.InputSize = 9

        self.InputFrame = Frame(self.root, width=200, height=800)
        self.InputFrame.place(x=0, y=0)

        Label(self.InputFrame, text="Input Size:").place(relx=0.5, y=20, anchor="n")
        self.Entry1 = Scale(self.InputFrame, from_=1, to=16, orient="horizontal", command=lambda val: self.create_grid(val))
        self.Entry1.place(relx=0.5, y=40, anchor="n")

        Label(self.InputFrame, text="Kernel Size:").place(relx=0.5, y=100, anchor="n")
        self.Entry2 = Scale(self.InputFrame, from_=1, to=50, orient="horizontal", command=lambda val: self.create_weight(val))
        self.Entry2.place(relx=0.5, y=120, anchor="n")

        Label(self.InputFrame, text="Padding:").place(relx=0.5, y=180, anchor="n")
        self.Entry3 = Scale(self.InputFrame, from_=0, to=16, orient="horizontal", command=lambda val: self.update_padding(val))
        self.Entry3.place(relx=0.5, y=200, anchor="n")

        Label(self.InputFrame, text="Speed:").place(relx=0.5, y=260, anchor="n")
        self.Entry4 = Scale(self.InputFrame, from_=0.1, to=1, orient="horizontal", resolution=0.1)
        self.Entry4.place(relx=0.5, y=280, anchor="n")

        self.DisplayFrame = Frame(self.root, width=800, height=800, bg="black")
        self.DisplayFrame.place(x=200, y=0)

        Label(self.root, text="Weight").place(x=1050, y=18)

        self.WeightFrame = Frame(self.root, width=300, height=300, bg="pink")
        self.WeightFrame.place(x=1050, y=50)

        Label(self.root, text="Output").place(x=1050, y=432, anchor="sw")

        self.OutputFrame = Frame(self.root, width=300, height=300, bg="yellow")
        self.OutputFrame.place(x=1050, y=750, anchor="sw")

        self.Entry1.set(9)
        self.Entry2.set(4)
        self.Entry3.set(2)
        self.Entry4.set(1)

        self.create_grid(self.InputSize)
        self.create_weight(4)
        self.create_output()
        self.create_padding(2 * 2)

        self.mainloop()

    def create_padding(self, padding):
        self.padding = padding
        rows, cols = len(self.cells), len(self.cells[0])
        self.result = []

        for layer in range(self.padding // 2):
            border = []

            top, bottom = layer, rows - layer - 1
            left, right = layer, cols - layer - 1

            for col in range(left, right + 1):
                border.append(self.cells[top][col])

            for row in range(top + 1, bottom + 1):
                border.append(self.cells[row][right])

            if bottom > top:
                for col in range(right - 1, left - 1, -1):
                    border.append(self.cells[bottom][col])

            if left < right:
                for row in range(bottom - 1, top, -1):
                    border.append(self.cells[row][left])

            self.result.append(border)

        for i in self.result:
            for j in i:
                j.config(bg="green")

    def update_padding(self, val):
        self.padding = int(val) * 2
        self.create_grid(self.InputSize)

    def create_output(self):
        self.outputcells = []
        size = self.InputSize - self.kernelSize + self.padding + 1
        button_size = math.ceil(300 / size)

        for i in range(size):
            line = []
            for j in range(size):
                btn = Button(self.OutputFrame, bg="white", relief="groove", highlightthickness=0)
                btn.place(x=j * button_size, y=i * button_size, width=button_size, height=button_size)
                line.append(btn)
            self.outputcells.append(line)

        if button_size * size > 300:
            for i in range(size):
                self.OutputFrame.winfo_children()[i * size + size - 1].config(width=size - (size - 1) * button_size)
            for j in range(size):
                self.OutputFrame.winfo_children()[(size - 1) * size + j].config(height=size - (size - 1) * button_size)

        self.outputcells[0][0].config(bg='black')

    def update_output(self):
        for i in self.outputcells:
            for j in i:
                j.config(bg="white")

        self.outputcells[self.kernelPos[0]][self.kernelPos[1]].config(bg='black')

    def create_weight(self, size):
        size = int(size)
        self.kernelSize = size
        self.kernelPos = (0, -1)
        button_size = math.ceil(300 / size)

        for i in range(size):
            for j in range(size):
                hue = (i + j) / (10 * size)
                rgb = colorsys.hsv_to_rgb(hue % 1, 1, 1)
                hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
                btn = Button(self.WeightFrame, bg=hex_color, relief="flat")
                btn.place(x=j * button_size, y=i * button_size, width=button_size, height=button_size)

        if button_size * size > 300:
            for i in range(size):
                self.WeightFrame.winfo_children()[i * size + size - 1].config(width=size - (size - 1) * button_size)
            for j in range(size):
                self.WeightFrame.winfo_children()[(size - 1) * size + j].config(height=size - (size - 1) * button_size)

        try:
            self.create_output()
        except:
            pass

    
        

    def create_grid(self, size1):
        self.kernelPos = (0, -1)
        self.cells = []
        try:
            size = int(size1)
            if size < 1 or size > 16:
                raise ValueError
        except ValueError:
            self.Entry1.delete(0, "end")
            self.Entry1.insert(0, "16")
            size = 16

        size = size + self.padding

        button_size = math.ceil(800 / size)

        for i in range(size):
            line = []
            for j in range(size):
                btn = Button(self.DisplayFrame, bg="white", relief="sunken")
                line.append(btn)
                btn.place(x=j * button_size, y=i * button_size, width=button_size, height=button_size)
            self.cells.append(line)

        if button_size * size > 800:
            for i in range(size):
                self.DisplayFrame.winfo_children()[i * size + size - 1].config(width=size - (size - 1) * button_size)
            for j in range(size):
                self.DisplayFrame.winfo_children()[(size - 1) * size + j].config(height=size - (size - 1) * button_size)
        self.InputSize = int(size1)
        self.create_output()

    def update_kernel(self, size, pos):

        prev_row, prev_col = self.prevKernelPos
        for i in range(size):
            for j in range(size):
                if 0 <= prev_row + i < len(self.cells) and 0 <= prev_col + j < len(self.cells[0]):
                    if self.cells[prev_row + i][prev_col + j]["bg"] != "green":
                        self.cells[prev_row + i][prev_col + j].config(bg="white")

        for i in range(size):
            for j in range(size):
                if 0 <= pos[0] + i < len(self.cells) and 0 <= pos[1] + j < len(self.cells[0]):
                    hue = (i + j) / (10 * size)
                    rgb = colorsys.hsv_to_rgb(hue % 1, 1, 1)
                    r, g, b = int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
                    if self.cells[pos[0] + i][pos[1] + j]["bg"] == "green":
                        tint_factor = 0.4
                        r = int(r * (1 - tint_factor))
                        b = int(b * (1 - tint_factor))
                        g = min(255, int(g + (tint_factor * (255 - g))))
                    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
                    self.cells[pos[0] + i][pos[1] + j].config(bg=hex_color)
    
        self.prevKernelPos = pos
        self.kernelSize = size
        


        

    def mainloop(self):
        def sub_process():
            while True:
                if self.kernelPos[1] + self.kernelSize >= self.InputSize + self.padding:
                    self.kernelPos = (self.kernelPos[0] + 1, 0)
                else:
                    self.kernelPos = (self.kernelPos[0], self.kernelPos[1] + 1)

                if self.kernelPos[0] >= self.InputSize + self.padding - self.kernelSize + 1:
                    self.kernelPos = (0, 0)

                try:
                    self.create_padding(self.padding)
                except:
                    pass
                try:
                    self.update_kernel(self.kernelSize, self.kernelPos)
                except:
                    pass
                try:
                    self.update_output()
                except:
                    pass
                self.root.update()
                self.root.update_idletasks()

                time.sleep(float(self.Entry4.get()))

        threading.Thread(target=sub_process).start()


root = Tk()
app = ConvolutionVisualizer(root)
root.mainloop()