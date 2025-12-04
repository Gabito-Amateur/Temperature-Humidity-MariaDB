#------------------Librerias-----------------
import pygame
import time
import threading
from grovepi import *
import MySQLdb


#------------------Funciones-----------------

# Función que obtiene los datos del sensor
def get_sensor_data():
    global temp, hum
    while True:
        try:
            # Lee los valores de temperatura y humedad
            [temp, hum] = dht(dht_sensor_port, 0)  # Cambia a 1 si usas un DHT11
            print("Temp = {}C \t Humidity = {}%".format(temp, hum))
            save_to_db(temp, hum)  # Guarda los datos en la base de datos
        except (IOError, TypeError) as e:
            print("Error en la lectura del sensor:", e)
            temp, hum = None, None  # En caso de error, ponemos los valores como None

        # Espera 2 segundos antes de hacer la siguiente lectura
        time.sleep(2)

# Función que muestra los datos en la ventana de Pygame
def display_data():
    screen.fill(BACKGROUND_COLOR)  # Limpia la pantalla

    # Lecturas actuales
    if temp is not None and hum is not None:
        temp_text = font.render("Temp: {}C".format(temp), True, TEXT_COLOR)
        hum_text = font.render("Humidity: {}%".format(hum), True, TEXT_COLOR)

        screen.blit(temp_text, (50, 50))
        screen.blit(hum_text, (50, 100))
    else:
        error_text = font.render("Error al leer el sensor.", True, (255, 0, 0))
        screen.blit(error_text, (50, 50))

    # Valores máximos/mínimos del día
    data = get_daily_min_max()
    if data:
        maxmin_text1 = font.render(
            "Max Temp: {}C  Min Temp: {}C".format(data['max_temp'], data['min_temp']),
            True, (0, 0, 120)
        )

        maxmin_text2 = font.render(
            "Max Hum: {}%  Min Hum: {}%".format(data['max_hum'], data['min_hum']),
            True, (0, 0, 120)
        )

        screen.blit(maxmin_text1, (50, 170))
        screen.blit(maxmin_text2, (50, 210))

    pygame.display.flip()  # Actualiza la pantalla


def save_to_db(temperatura, humedad):
    try:
        conexion = MySQLdb.connect(
            host="localhost",
            user="raspiuser",
            passwd="1234",
            db="sensores"
        )
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO dht11 (temperatura, humedad) VALUES (%s, %s)",
            (temperatura, humedad)
        )
        conexion.commit()
        conexion.close()
        print("Datos guardados en MariaDB")
    except MySQLdb.Error as e:
        print("Error al guardar en la BD:", e)

def get_daily_min_max():
    try:
        conexion = MySQLdb.connect(
            host="localhost",
            user="raspiuser",
            passwd="1234",
            db="sensores"
        )
        cursor = conexion.cursor()

        query = """
            SELECT 
                MAX(temperatura),
                MIN(temperatura),
                MAX(humedad),
                MIN(humedad)
            FROM dht11
            WHERE DATE(fecha) = CURDATE();
        """
        cursor.execute(query)
        result = cursor.fetchone()
        conexion.close()

        max_temp, min_temp, max_hum, min_hum = result

        return {
            "max_temp": max_temp,
            "min_temp": min_temp,
            "max_hum": max_hum,
            "min_hum": min_hum
        }

    except MySQLdb.Error as e:
        print("Error al consultar máximos/mínimos:", e)
        return None


# Función principal
def main():
    global temp, hum
    # Creamos un hilo para ejecutar la función get_sensor_data()
    sensor_thread = threading.Thread(target=get_sensor_data)
    sensor_thread.daemon = True  # Asegura que el hilo se cierre cuando termine el programa principal
    sensor_thread.start()  # Inicia el hilo

    # Bucle principal de la app
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Termina el bucle si el usuario cierra la ventana

        display_data()  # Muestra los datos del sensor en la ventana
        time.sleep(2)  # Espera 2 segundos antes de actualizar los datos

    pygame.quit()  # Cierra Pygame

#------------------Programa Principal-----------------

# Configuración del puerto del sensor
dht_sensor_port = 7  # Asegúrate de usar el puerto correcto

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300

# Crear la ventana de Pygame
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sensor de Temperatura y Humedad")

# Colores
BACKGROUND_COLOR = (255, 255, 255)  # Blanco
TEXT_COLOR = (0, 0, 0)  # Negro
GREEN = (0, 255, 0)  # Verde

# Fuente para mostrar texto
font = pygame.font.Font(None, 36)

if __name__ == "__main__":
    temp, hum = None, None  # Inicializa las variables de temperatura y humedad
    main()

