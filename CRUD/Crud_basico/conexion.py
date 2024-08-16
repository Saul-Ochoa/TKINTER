import sqlite3

class Comunicacion():
    def __init__(self):
        self.conexion = sqlite3.connect('base_datos1.db')
        
    # insertar datos
    def insertar_datos(self, nombre, edad, correo, telefono):
        cursor = self.conexion.cursor()
        bd = '''INSERT INTO datos (Nombre, Edad, Correo, Telefono)
                VALUES (?, ?, ?, ?)'''
        cursor.execute(bd, (nombre, edad, correo, telefono))
        self.conexion.commit()
        cursor.close()
        
    # mostrar datos
    def mostrar_datos(self):
        cursor = self.conexion.cursor()
        bd = "SELECT * FROM datos"
        cursor.execute(bd)
        datos = cursor.fetchall()
        cursor.close()  # Cierra el cursor después de usarlo
        return datos
    
    # eliminar datos
    def eliminar_datos(self, nombre):
        cursor = self.conexion.cursor()
        bd = '''DELETE FROM datos WHERE Nombre = ?'''
        cursor.execute(bd, (nombre,))
        self.conexion.commit()
        cursor.close()
        
    # actualizar_datos
    def actualizar_datos(self, ID, nombre, edad, correo, telefono):
        cursor = self.conexion.cursor()
        bd = '''UPDATE datos SET Nombre = ?, Edad = ?, Correo = ?, Telefono = ? 
                WHERE ID = ?'''
        cursor.execute(bd, (nombre, edad, correo, telefono, ID))
        dato = cursor.rowcount
        self.conexion.commit()
        cursor.close()
        return dato
