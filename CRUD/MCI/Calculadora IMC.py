from tkinter import *
import tkinter as tk
from tkinter import ttk, Label, PhotoImage, Entry, StringVar, Button
from PIL import Image, ImageTk

class IMCCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title('Calculadora de IMC')
        self.root.geometry("470x580+300+200")
        self.root.resizable(False, False)

        # Icono
        self.image_icon = PhotoImage(file='icon.png')
        self.root.iconphoto(False, self.image_icon)

        # Top
        self.top = PhotoImage(file='top.png')
        self.top_image = Label(self.root, image=self.top, background='#f0f1f5')
        self.top_image.place(x=-10, y=-10)

        # Botón box
        Label(self.root, width=72, height=18, bg='lightblue').pack(side=tk.BOTTOM)

        # Dos boxes
        self.box = PhotoImage(file='box.png')
        Label(self.root, image=self.box).place(x=20, y=100)
        Label(self.root, image=self.box).place(x=240, y=100)

        # Scale
        self.scale_image = PhotoImage(file='scale.png')
        Label(self.root, image=self.scale_image).place(x=20, y=310)

        ################################ Slider 1 #######################################
        self.style = ttk.Style()
        self.style.configure("TScale", background='white')
        self.current_value = tk.DoubleVar()

        self.slider = ttk.Scale(self.root, from_=0, to=220, orient='horizontal', style='TScale',
                                command=self.slider_changed, variable=self.current_value)
        self.slider.place(x=80, y=250)
        
        self.label_height=Label(root,text='Height (m)',fg="black",bg='white',font='Arial 15 bold')
        self.label_height.place(x=85,y=120)

        ################################ Slider 2 #######################################
        self.current_value2 = tk.DoubleVar()
        self.slider2 = ttk.Scale(self.root, from_=0, to=200, orient='horizontal', style='TScale',
                                 command=self.slider_changed2, variable=self.current_value2)
        self.slider2.place(x=300, y=250)
        
        self.label_weight=Label(root,text='Weight (kg)',fg="black",bg='white',font='Arial 15 bold')
        self.label_weight.place(x=300,y=120)

        # Entry boxes
        self.height_var = StringVar()
        self.weight_var = StringVar()

        self.height_entry = Entry(self.root, textvariable=self.height_var, width=5, font='Arial 50', bg='#fff', fg='#000', bd=0, justify=tk.CENTER)
        self.height_entry.place(x=35, y=160)

        self.weight_entry = Entry(self.root, textvariable=self.weight_var, width=5, font='Arial 50', bg='#fff', fg='#000', bd=0, justify=tk.CENTER)
        self.weight_entry.place(x=255, y=160)
        #self.weight_entry.set(get_current_value2())

        # Imagen del hombre
        self.second_image = Label(self.root, bg='lightblue')
        self.second_image.place(x=70, y=530)
        
        # Boton IMC
        self.button_entry = Button(root, text='View Report', width=15, height=2, font='Arial 10 bold', bg='#1f6e68', fg='white', command=self.BMI)
        self.button_entry.place(x=280, y=340)
        
        # Label IMC
        self.label_imc_1 = Label(root, font='Arial 60 bold', bg='lightblue', fg='#fff')
        self.label_imc_1.place(x=125, y=305)
        
        self.label_imc_2 = Label(root, font='Arial 20 bold', bg='lightblue', fg='#3b3a3a')
        self.label_imc_2.place(x=260, y=430)
        
        self.label_imc_3 = Label(root, font='Arial 10', bg='lightblue')
        self.label_imc_3.place(x=190, y=500)

    def get_current_value(self):
        return '{: .2f}'.format(self.current_value.get())
    
    def get_current_value2(self):
        return '{: .2f}'.format(self.current_value2.get())

    def slider_changed(self, event):
        self.height_var.set(self.get_current_value())
        size = int(float(self.get_current_value()))
        
        try:
            img = Image.open('man.png')
            resized_image = img.resize((50, 10 + size))
            photo2 = ImageTk.PhotoImage(resized_image)

            self.second_image.config(image=photo2)
            self.second_image.place(x=70, y=550 - size)
            self.second_image.image = photo2
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
      
    def slider_changed2(self, event):
        self.weight_var.set(self.get_current_value2())
    
    def BMI(self):
        h = float(self.height_var.get())
        w = float(self.weight_var.get())
        m = h / 100
        bmi = round(float(w / m**2), 1)
        
        if bmi <= 18.5:
            self.label_imc_2.config(text='Underweight!')
            self.label_imc_3.config(text='You have lower weight than normal body!')
        elif 18.5 < bmi <= 25:
            self.label_imc_2.config(text='Normal!')
            self.label_imc_3.config(text='It indicates that you are healthy')
        elif 25 < bmi < 30:
            self.label_imc_2.config(text='Overweight!')
            self.label_imc_3.config(text='It indicates that a person is slightly overweight!')
        else:
            self.label_imc_2.config(text='Obesity!')
            self.label_imc_3.config(text='You have higher weight than normal body!')

if __name__ == '__main__':
    root = tk.Tk()
    app = IMCCalculator(root)
    root.mainloop()