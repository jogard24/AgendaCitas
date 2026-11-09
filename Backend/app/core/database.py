import fdb

# Datos de conexión según el servidor en red
DB_PATH = "server-r740:C:/Soluciones Informaticas/Salus/Bases/SALUSDB.FDB"
DB_USER = "SYSDBA"
DB_PASS = "manager123*/*"
FB_CLIENT = r'C:\Program Files\Firebird\Firebird_2_5\bin\fbclient.dll'

def get_db_connection():
    """Abre y retorna una conexión directa a la BD Firebird en red."""
    connection = fdb.connect(
        dsn=DB_PATH,
        user=DB_USER,
        password=DB_PASS,
        fb_library_name=FB_CLIENT,
        charset='UTF8'
    )
    return connection

# Prueba rápida de conexión si ejecutamos este archivo directamente
if __name__ == "__main__":
    try:
        conn = get_db_connection()
        print("¡Conexión exitosa a Firebird en la red! ")
        conn.close()
    except Exception as e:
        print(f" Error al conectar a la base de datos: {e}")