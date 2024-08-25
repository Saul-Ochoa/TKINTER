import pyodbc
class Articulos:
    def __init__(self):
        # Configuración de la conexión
        self.server = 'DESKTOP-BLERSIO'
        self.database = 'BD_CRUD'
        self.connection_string = (
            f'DRIVER={{SQL Server}};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            'Trusted_Connection=yes;'
        )

    def abrir(self):
        try:
            conn = pyodbc.connect(self.connection_string)
            return conn
        except pyodbc.Error as e:
            return None

    def insertar(self, datos):
        conn = self.abrir()
        if conn:
            try:
                cursor = conn.cursor()
                sql = (
                    'INSERT INTO Table_lectores '
                    '(lectores_nombre, lectores_telefono, lectores_direccion, lectores_observacion) '
                    'VALUES (?, ?, ?, ?)'
                )
                cursor.execute(sql, datos)
                conn.commit()
            finally:
                conn.close()

    def consulta(self, nombre):
        conn = self.abrir()
        if conn:
            try:
                cursor = conn.cursor()
                sql = (
                    'SELECT lectores_nombre, lectores_telefono, lectores_direccion, lectores_observacion '
                    'FROM Table_lectores '
                    'WHERE lectores_nombre = ?'
                )
                cursor.execute(sql, (nombre,))
                return cursor.fetchall()
            finally:
                conn.close()

    def mostrar_datos(self):
        conn = self.abrir()
        if conn:
            try:
                cursor = conn.cursor()
                sql = 'SELECT * FROM Table_lectores'
                cursor.execute(sql)
                return cursor.fetchall()
            finally:
                conn.close()
                
    def eliminar_datos(self, nombre):
        conn = self.abrir()
        if conn:
            try:
                cursor = conn.cursor()
                sql = 'DELETE FROM Table_lectores WHERE lectores_IdLector = ?'
                cursor.execute(sql, (nombre,))
                conn.commit()
            finally:
                cursor.close()

    def actualizar_datos(self, nombre1, nombre2, nombre3, nombre4, nombre5):
        conn = self.abrir()
        if conn:
            try:
                cursor = conn.cursor()
                sql = '''
                    UPDATE Table_lectores
                    SET lectores_nombre = ?, lectores_telefono = ?, lectores_direccion = ?, lectores_observacion = ?
                    WHERE lectores_IdLector = ?
                '''
                cursor.execute(sql, (nombre1, nombre2, nombre3, nombre4, nombre5))
                data = cursor.rowcount
                conn.commit()
                return data
            except pyodbc.Error as e:
                print(f"Error al actualizar los datos: {e}")
                return None
            finally:
                cursor.close()
                conn.close() 
