from tkinter import Tk,Button,Entry,Label,ttk,PhotoImage
from tkinter import StringVar,Scrollbar,Frame,messagebox
from conexion import Comunicacion
import pandas as pd
from time import strftime
class Ventana(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.nombre=StringVar()
        self.edad=StringVar()
        self.correo=StringVar()
        self.telefono=StringVar()
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=1)
        self.master.rowconfigure(1,weight=5)
        self.base_datos=Comunicacion()
        self.widgets()
        
    def widgets(self):
        self.frame_uno=Frame(self.master,bg='white',height=200,width=800)
        self.frame_uno.grid(column=0,row=0,sticky='nsew')
        self.frame_dos=Frame(self.master,bg='white',height=300,width=800)
        self.frame_dos.grid(column=0,row=1,sticky='nsew')
        
        self.frame_uno.columnconfigure([0,1,2],weight=1)
        self.frame_uno.rowconfigure([0,1,2,3,4],weight=1)
        self.frame_dos.columnconfigure(0,weight=1)
        self.frame_dos.rowconfigure(0,weight=1)
        
        # button y labels
        Label(self.frame_uno,text='Opciones',bg='white',fg='black',
              font=('Arial',13,'bold')).grid(column=2,row=0)
        Button(self.frame_uno,text='Refrescar',font=('Arial',9,'bold'),command=self.actualizar_tabla,
               fg='black',bg='deep sky blue',width=20,bd=3).grid(column=2,row=1,pady=5)
        
        Label(self.frame_uno,text='Agregar y Actualizar datos',fg='black',bg='white',
              font=('Arial',13,'bold')).grid(columnspan=2,column=0,row=0,pady=5)
        Label(self.frame_uno,text='Nombre',fg='black',bg='white',
              font=('Rockwell',13,'bold')).grid(column=0,row=1,pady=5)
        Label(self.frame_uno,text='Edad',fg='black',bg='white',
              font=('Rockwell',13,'bold')).grid(column=0,row=2,pady=5)
        Label(self.frame_uno,text='Correo',fg='black',bg='white',
              font=('Rockwell',13,'bold')).grid(column=0,row=3,pady=5)
        Label(self.frame_uno,text='Telefono',fg='black',bg='white',
              font=('Rockwell',13,'bold')).grid(column=0,row=4,pady=5)
        Entry(self.frame_uno,textvariable=self.nombre,font=('Comic Sans MS',12),
              highlightbackground='deep sky blue',highlightthickness=5).grid(column=1,row=1)
        Entry(self.frame_uno,textvariable=self.edad,font=('Comic Sans MS',12),
              highlightbackground='deep sky blue',highlightthickness=5).grid(column=1,row=2)
        Entry(self.frame_uno,textvariable=self.correo,font=('Comic Sans MS',12),
              highlightbackground='deep sky blue',highlightthickness=5).grid(column=1,row=3)
        Entry(self.frame_uno,textvariable=self.telefono,font=('Comic Sans MS',12),
              highlightbackground='deep sky blue',highlightthickness=5).grid(column=1,row=4)
        
        Button(self.frame_uno,text='AÑADIR DATOS',font=('Arial',9,'bold'),bg='deep sky blue',command=self.agregar_datos,
               width=20,bd=3).grid(column=2,row=2,pady=5,padx=5)
        Button(self.frame_uno,text='LIMPIAR CAMPOS',font=('Arial',9,'bold'),bg='deep sky blue',command=self.limpiar_campos,
               width=20,bd=3).grid(column=2,row=3,pady=5,padx=5)
        Button(self.frame_uno,text='ACTUALIZAR DATOS',font=('Arial',9,'bold'),bg='deep sky blue',command=self.actualizar_datos,
               width=20,bd=3).grid(column=2,row=4,pady=5,padx=5)
        Button(self.frame_uno,text='EXPORTAR A EXCEL',font=('Arial',9,'bold'),bg='deep sky blue',command=self.guardar_datos,
               width=20,bd=3).grid(column=2,row=5,pady=5,padx=5)
        
        estilo_tabla=ttk.Style()
        estilo_tabla.configure('Treeview',font=('Helvetica',10,'bold'),foreground='black',
                               background='white')
        estilo_tabla.map('Treeview',background=[('selected','deep sky blue')],foreground=[('selected','black')])
        estilo_tabla.configure('Heading',background='white',foreground='deep sky blue',
                               padding=3,font=('Arial',10,'bold'))
        self.tabla=ttk.Treeview(self.frame_dos)
        self.tabla.grid(column=0,row=0,sticky='nsew')
        ladox=ttk.Scrollbar(self.frame_dos,orient='horizontal',command=self.tabla.xview)
        ladox.grid(column=0,row=1,sticky='ew')
        ladoy=ttk.Scrollbar(self.frame_dos,orient='vertical',command=self.tabla.yview)
        ladoy.grid(column=1,row=0,sticky='ns')
        self.tabla.configure(xscrollcommand=ladox.set,yscrollcommand=ladoy.set)
        
        self.tabla['columns']=('Edad','Correo','Telefono')
        self.tabla.column('#0',minwidth=100,width=120,anchor='center')
        self.tabla.column('Edad',minwidth=100,width=120,anchor='center')
        self.tabla.column('Correo',minwidth=100,width=120,anchor='center')
        self.tabla.column('Telefono',minwidth=100,width=105,anchor='center')
        
        self.tabla.heading('#0',text='Nombre',anchor='center')
        self.tabla.heading('Edad',text='Edad',anchor='center')
        self.tabla.heading('Correo',text='Correo',anchor='center')
        self.tabla.heading('Telefono',text='Telefono',anchor='center')
        # manipulaciones
        self.tabla.bind("<<TreeviewSelect>>",self.obtener_fila)
        self.tabla.bind("<Double-1>",self.eliminar_datos)
        
    def obtener_fila(self,event):
        item=self.tabla.focus()
        if not item:
            return  # No hay ningún elemento seleccionado
        self.data = self.tabla.item(item)
        nombre = self.data.get('text', '')
        values = self.data.get('values', [])
        self.nombre.set(nombre)
        self.edad.set(values[0] if len(values) > 0 else '')
        self.correo.set(values[1] if len(values) > 1 else '')
        self.telefono.set(values[2] if len(values) > 2 else '')

        
        
    def eliminar_datos(self,event):
        self.limpiar_campos()
        item=self.tabla.selection()[0]
        x=messagebox.askquestion('Informacio', '¿ Deseas eliminar ?')
        if x=='yes':
            self.tabla.delete(item)
            self.base_datos.eliminar_datos(self.data['text'])
            
    def agregar_datos(self):
        nombre=self.nombre.get()
        edad=self.edad.get()
        correo=self.correo.get()
        telefono=self.telefono.get()
        datos=(edad,correo,telefono)
        if nombre and edad and correo and telefono !='':
            self.tabla.insert('',0,text=nombre,values=datos)
            self.base_datos.insertar_datos(nombre,edad,correo,telefono)
            self.limpiar_campos()
            
    def actualizar_tabla(self):
        self.limpiar_campos()
        datos = self.base_datos.mostrar_datos()
        self.tabla.delete(*self.tabla.get_children())
        for dato in datos:
            self.tabla.insert('', 'end', text=dato[1], values=(dato[2], dato[3], dato[4]))
            
    def guardar_datos(self):
        self.limpiar_campos()
        datos = self.base_datos.mostrar_datos()
        registros = []
        for dato in datos:
            registro = {
                'Nombre': dato[1],
                'Edad': dato[2],
                'Correo': dato[3],
                'Telefono': dato[4]
            }
            registros.append(registro)
        fecha = strftime('%d-%m-%Y_%H-%M-%S')
        df = pd.DataFrame(registros)
        df.to_excel(f'Datos_{fecha}.xlsx', index=False)
        messagebox.showinfo('Información', 'Datos guardados exitosamente.')


    def actualizar_datos(self):
        try:
            item = self.tabla.focus()
            if not item:
                messagebox.showwarning("Advertencia", "Por favor, selecciona una fila para actualizar.")
                return
            
            self.data = self.tabla.item(item)
            nombre_actual = self.data.get('text', '')
            
            nombre = self.nombre.get()
            edad = self.edad.get()
            correo = self.correo.get()
            telefono = self.telefono.get()
            
            if not all([nombre, edad, correo, telefono]):
                messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
                return
            
            datos = self.base_datos.mostrar_datos()
            for fila in datos:
                Id = fila[0]
                nombre_bd = fila[1]
                if nombre_bd == nombre_actual:
                    self.base_datos.actualizar_datos(Id, nombre, edad, correo, telefono)
                    self.actualizar_tabla()
                    self.limpiar_campos()
                    messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
                    return
            messagebox.showerror("Error", "No se pudo encontrar el registro para actualizar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar los datos: {e}")

        
    def limpiar_campos(self):
        self.nombre.set('')
        self.edad.set('')
        self.correo.set('')
        self.telefono.set('')
        
if __name__ =="__main__":
    ventana=Tk()
    ventana.title('')
    ventana.minsize(height=400,width=600)
    ventana.geometry('800x500')
    app=Ventana(ventana)
    app.mainloop()