
import tkinter as tk
from tkinter import filedialog
from analyse import *

class MyGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.index = 0

        self.title("Prediction of ...")

        self.Analyse = Analyse()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()


        window_width = 900
        window_height = 600

        x = screen_width / 2 - window_width / 2  # Center horizontally
        y = screen_height / 2 - window_height / 2  # Center vertically 

        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")  


        # File dialog button
        self.file_button = tk.Button(self, text="Open File", command=self.open_file)
        self.file_button.pack()
        self.file_button.place(x = 250, y = 50, width= 70, height= 20)

        self.anal_button = tk.Button(self, text="Analyse", command=self.anal)
        self.anal_button.place(x = 280, y = 320, width = 80, height = 20)

        self.load_button = tk.Button(self, text="Load", command=self.load_excel)
        self.load_button.pack()
        self.load_button.place(x = 120, y = 100, width= 70, height= 30)
        self.load_button.config(state="disabled")

        # List box
        self.list_box = tk.Listbox(self)
        self.list_box.pack()
        self.list_box.place(x = 70, y = 200, width = 200, height = 300)

        self.list_box.bind('<<ListboxSelect>>', self.on_listbox_select)
        # Input boxes
        # self.input_boxes = []
        # for i in range(4):
        #     entry = tk.Entry(self)
        #     entry.pack()
        #     self.input_boxes.append(entry)

        self.file_path_input = tk.Entry(self)
        self.file_path_input.place(x = 125, y = 50, width= 100, height= 20)

        label = tk.Label(self, text = "File Path")
        label.place(x = 70, y = 50, width = 50, height = 20)

        label_name = tk.Label(self, text = "Member List", font=("Arial", 16))
        label_name.place(x = 70, y = 170, width = 200, height = 20)


        #############################################
        label_x_1 = tk.Label(self, text = "Raise")
        label_x_1.place(x = 500, y = 200, width = 50, height = 20)

        label_x_2 = tk.Label(self, text = "Retain")
        label_x_2.place(x = 600, y = 200, width = 50, height = 20)

        label_x_3 = tk.Label(self, text = "Reduce")
        label_x_3.place(x = 700, y = 200, width = 50, height = 20)

        label_y_1 = tk.Label(self, text = "MPR")
        label_y_1.place(x = 350, y = 250, width = 100, height = 20)

        label_y_2 = tk.Label(self, text = "CORRIDOR")
        label_y_2.place(x = 350, y = 320, width = 100, height = 20)

        label_y_3 = tk.Label(self, text = "CRR")
        label_y_3.place(x = 350, y = 390, width = 100, height = 20)

        label_y_4 = tk.Label(self, text = "LIQUIDITY RATIO")
        label_y_4.place(x = 350, y = 460, width = 100, height = 20)
        

        self.mpr_1 = tk.Entry(self)
        self.mpr_1.place(x = 500, y = 250, width= 70, height= 20)

        self.mpr_2 = tk.Entry(self)
        self.mpr_2.place(x = 600, y = 250, width= 70, height= 20)

        self.mpr_3 = tk.Entry(self)
        self.mpr_3.place(x = 700, y = 250, width= 70, height= 20)

        self.corridor_1 = tk.Entry(self)
        self.corridor_1.place(x = 500, y = 320, width= 70, height= 20)


        self.corridor_2 = tk.Entry(self)
        self.corridor_2.place(x = 600, y = 320, width= 70, height= 20)

        self.corridor_3 = tk.Entry(self)
        self.corridor_3.place(x = 700, y = 320, width= 70, height= 20)

        self.crr_1 = tk.Entry(self)
        self.crr_1.place(x = 500, y = 390, width= 70, height= 20)

        self.crr_2 = tk.Entry(self)
        self.crr_2.place(x = 600, y = 390, width= 70, height= 20)

        self.crr_3 = tk.Entry(self)
        self.crr_3.place(x = 700, y = 390, width= 70, height= 20)

        self.liq_1 = tk.Entry(self)
        self.liq_1.place(x = 500, y = 460, width= 70, height= 20)

        self.liq_2 = tk.Entry(self)
        self.liq_2.place(x = 600, y = 460, width= 70, height= 20)

        self.liq_3 = tk.Entry(self)
        self.liq_3.place(x = 700, y = 460, width= 70, height= 20)



    def open_file(self):
        self.file_path = filedialog.askopenfilename()
        # Do something with the file path, like displaying it or processing the file
        self.file_path_input.delete(0, tk.END)
        self.file_path_input.insert(0, self.file_path)
        # self.file_path_input.config(state="disabled")

        
        self.load_button.config(state="active")
    
    def on_listbox_select(self, event):
        index = self.list_box.curselection()
        self.index = index[0]

    def load_excel(self):
        self.Analyse.setExcel(self.file_path)
        arr = self.Analyse.get_names()
        
        self.list_box.delete(0, tk.END)

        for item in arr:
            self.list_box.insert(tk.END, str(item))

    def MPR_fill(self, arr):
        self.mpr_1.delete(0, tk.END)
        self.mpr_1.insert(0, float(arr[0][0] * 100))

        self.mpr_2.delete(0, tk.END)
        self.mpr_2.insert(0, float(arr[0][1] * 100))

        self.mpr_3.delete(0, tk.END)
        self.mpr_3.insert(0, float(arr[0][2] * 100))
        
    def corridor_fill(self, arr):
        self.corridor_1.delete(0, tk.END)
        self.corridor_1.insert(0, float(arr[0][0] * 100))

        self.corridor_2.delete(0, tk.END)
        self.corridor_2.insert(0, float(arr[0][1] * 100))

        self.corridor_3.delete(0, tk.END)
        self.corridor_3.insert(0, float(arr[0][2] * 100))

    def crr_fill(self, arr):
        self.crr_1.delete(0, tk.END)
        self.crr_1.insert(0, float(arr[0][0] * 100))

        self.crr_2.delete(0, tk.END)
        self.crr_2.insert(0, float(arr[0][1] * 100))

        self.crr_3.delete(0, tk.END)
        self.crr_3.insert(0, float(arr[0][2] * 100))

    def liquid_fill(self, arr):
        self.liq_1.delete(0, tk.END)
        self.liq_1.insert(0, float(arr[0][0] * 100))

        self.liq_2.delete(0, tk.END)
        self.liq_2.insert(0, float(arr[0][1] * 100))

        self.liq_3.delete(0, tk.END)
        self.liq_3.insert(0, float(arr[0][2] * 100))

    def anal(self):
        self.MPR_fill(self.Analyse.predict(self.index, 0))
        self.corridor_fill(self.Analyse.predict(self.index, 1))
        self.crr_fill(self.Analyse.predict(self.index, 2))
        self.liquid_fill(self.Analyse.predict(self.index, 3))

        

if __name__ == "__main__":
    app = MyGUI()
    app.mainloop()