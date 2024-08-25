import pyodbc
from conexion import Articulos
from tkinter import Tk, Button, Entry, Label, ttk, StringVar, Frame, messagebox
from time import strftime

class Root(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.lectores_nombre = StringVar()
        self.lectores_telefono = StringVar()
        self.lectores_direccion = StringVar()
        self.lectores_observacion = StringVar()
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=5)
        self.base_datos = Articulos()
        self.widgets()
        self.mostrar_datos_en_tabla()

    def widgets(self):
        self.frame_uno = Frame(self.master, bg='white', height=200, width=800)
        self.frame_uno.grid(column=0, row=0, sticky='nsew')
        self.frame_dos = Frame(self.master, bg='white', height=300, width=800)
        self.frame_dos.grid(column=0, row=1, sticky='nsew')
        self.frame_uno.columnconfigure([0, 1, 2], weight=1)
        self.frame_uno.rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.frame_dos.columnconfigure(0, weight=1)
        self.frame_dos.rowconfigure(0, weight=1)
        
        # Labels
        Label(self.frame_uno, text='Agregar y Actualizar datos', fg='black', bg='white',
              font=('Arial', 13, 'bold')).grid(columnspan=2, column=0, row=0, pady=5)
        Label(self.frame_uno, text='Nombre', fg='black', bg='white',
              font=('Rockwell', 13, 'bold')).grid(column=0, row=1, pady=5)
        Label(self.frame_uno, text='Telefono', fg='black', bg='white',
              font=('Rockwell', 13, 'bold')).grid(column=0, row=2, pady=5)
        Label(self.frame_uno, text='Dirección', fg='black', bg='white',
              font=('Rockwell', 13, 'bold')).grid(column=0, row=3, pady=5)
        Label(self.frame_uno, text='Observación', fg='black', bg='white',
              font=('Rockwell', 13, 'bold')).grid(column=0, row=4, pady=5)
        
        # Entry 
        Entry(self.frame_uno, textvariable=self.lectores_nombre, font=('Comic Sans MS', 12),
              highlightbackground='deep sky blue', highlightthickness=5).grid(column=1, row=1)
        Entry(self.frame_uno, textvariable=self.lectores_telefono, font=('Comic Sans MS', 12),
              highlightbackground='deep sky blue', highlightthickness=5).grid(column=1, row=2)
        Entry(self.frame_uno, textvariable=self.lectores_direccion, font=('Comic Sans MS', 12),
              highlightbackground='deep sky blue', highlightthickness=5).grid(column=1, row=3)
        Entry(self.frame_uno, textvariable=self.lectores_observacion, font=('Comic Sans MS', 12),
              highlightbackground='deep sky blue', highlightthickness=5).grid(column=1, row=4)
        
        # Button
        Button(self.frame_uno, text='AÑADIR DATOS', font=('Arial', 9, 'bold'), bg='deep sky blue',
               width=20, bd=3, command=self.agregar_datos).grid(column=2, row=1, pady=5, padx=5)
        Button(self.frame_uno, text='LIMPIAR CAMPOS', font=('Arial', 9, 'bold'), bg='deep sky blue', command=self.limpiar_campos,
               width=20, bd=3).grid(column=2, row=2, pady=5, padx=5)
        Button(self.frame_uno, text='Editar CAMPOS', font=('Arial', 9, 'bold'), bg='deep sky blue',command=self.editar_datos,
               width=20, bd=3).grid(column=2, row=3, pady=5, padx=5)
        Button(self.frame_uno, text='Exportar CAMPOS', font=('Arial', 9, 'bold'), bg='deep sky blue',
               width=20, bd=3).grid(column=2, row=4, pady=5, padx=5)
        # Treeview
        estilo_tabla = ttk.Style()
        estilo_tabla.configure('Treeview', font=('Helvetica', 10, 'bold'), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'deep sky blue')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='deep sky blue', padding=3, font=('Arial', 10, 'bold'))
        
        self.tabla = ttk.Treeview(self.frame_dos, columns=("id","nombre", "telefono", "direccion", "observacion"), show='headings')
        self.tabla.grid(column=0, row=0, sticky='nsew')
        
        ladox = ttk.Scrollbar(self.frame_dos, orient='horizontal', command=self.tabla.xview)
        ladox.grid(column=0, row=1, sticky='ew')
        ladoy = ttk.Scrollbar(self.frame_dos, orient='vertical', command=self.tabla.yview)
        ladoy.grid(column=1, row=0, sticky='ns')
        self.tabla.configure(xscrollcommand=ladox.set, yscrollcommand=ladoy.set)
        # Eventos
        self.tabla.bind("<<TreeviewSelect>>",self.obtener_filas)
        self.tabla.bind("<Double-1>",self.eliminar_datos)
        
        # Configurar encabezados de columnas
        self.tabla.heading("id",text="Id")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("telefono", text="Teléfono")
        self.tabla.heading("direccion", text="Dirección")
        self.tabla.heading("observacion", text="Observación")
        
        self.tabla.column("id", minwidth=0, width=60)
        self.tabla.column("nombre", minwidth=0, width=150)
        self.tabla.column("telefono", minwidth=0, width=100)
        self.tabla.column("direccion", minwidth=0, width=200)
        self.tabla.column("observacion", minwidth=0, width=250)

    def limpiar_campos(self):
        self.lectores_nombre.set('')
        self.lectores_direccion.set('')
        self.lectores_observacion.set('')
        self.lectores_telefono.set('')

    def agregar_datos(self):
        nombre = self.lectores_nombre.get()
        telefono = self.lectores_telefono.get()
        direccion = self.lectores_direccion.get()
        observacion = self.lectores_observacion.get()
        
        if nombre and telefono and direccion and observacion:
            datos = (nombre, telefono, direccion, observacion)
            self.base_datos.insertar(datos)
            self.mostrar_datos_en_tabla()
            self.limpiar_campos()
    
    def mostrar_datos_en_tabla(self):
        # Limpiar la tabla antes de mostrar los datos
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # Obtener los datos desde la base de datos
        rows = self.base_datos.mostrar_datos()
        for row in rows:
            # Asegurarse de que cada valor en la fila no tenga espacios adicionales
            row = tuple(str(item).strip() for item in row)
            self.tabla.insert("", "end", values=row)
        
    def obtener_filas(self, event=None):
        item = self.tabla.focus()
        if not item:
            return  # No hay ningún elemento seleccionado
        
        # Obtener los valores de la fila seleccionada
        data = self.tabla.item(item)['values']
        
        # Asegúrate de que hay suficientes valores en la fila
        if len(data) >= 4:
            id_nombre = data[1]
            id_telefono = data[2]
            id_direccion = data[3]
            id_observacion = data[4]
            
            # Configurar los valores en los campos correspondientes
            self.lectores_nombre.set(id_nombre)
            self.lectores_telefono.set(id_telefono)
            self.lectores_direccion.set(id_direccion)
            self.lectores_observacion.set(id_observacion)

    def editar_datos(self):
        # Obtener el item seleccionado
        selected_item = self.tabla.focus()
        
        if not selected_item:
            messagebox.showwarning('Advertencia', 'No se ha seleccionado ningún registro')
            return
        
        # Obtener los valores de la fila seleccionada
        data = self.tabla.item(selected_item)['values']
        
        if len(data) >= 5:
            # Crear un cuadro de diálogo de confirmación
            if messagebox.askyesno("Confirmar", "¿Deseas actualizar este registro?"):
                # Si se confirma, se llama a la función actualizar_datos
                resultado = self.base_datos.actualizar_datos(
                    self.lectores_nombre.get(),   
                    self.lectores_telefono.get(), 
                    self.lectores_direccion.get(), 
                    self.lectores_observacion.get(), 
                    data[0]  # El ID es el primer valor en la fila seleccionada
                )
                
                if resultado:
                    messagebox.showinfo('Éxito', 'Registro actualizado correctamente')
                    self.mostrar_datos_en_tabla()  # Actualizar la tabla con los nuevos datos
                    self.limpiar_campos()
                else:
                    messagebox.showerror('Error', 'No se pudo actualizar el registro')


    def eliminar_datos(self, event):
        # Obtener el item seleccionado
        selected_item = self.tabla.selection()
        
        if not selected_item:
            messagebox.showwarning('Advertencia', 'No se ha seleccionado ningún registro')
            return
        
        # Confirmar la eliminación
        confirmacion = messagebox.askquestion('Confirmación', '¿Deseas eliminar este registro?')
        if confirmacion == 'yes':
            # Obtener el ID del lector de la fila seleccionada
            item = self.tabla.item(selected_item)
            id_lector = item['values'][0]  # El ID es el primer valor
            
            # Eliminar del Treeview
            self.tabla.delete(selected_item)
            
            # Eliminar de la base de datos
            self.base_datos.eliminar_datos(id_lector)

            messagebox.showinfo('Información', 'Registro eliminado correctamente')
 
    
if __name__ == '__main__':
    ventana = Tk()
    ventana.title('Crud-SQL')
    ventana.minsize(height=400, width=600)
    ventana.geometry('800x500')
    app = Root(ventana)
    app.mainloop()