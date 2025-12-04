# 🌡️ Sistema de Monitoreo de Temperatura y Humedad con MariaDB

<div align="center">

![Python](https://img.shields.io/badge/Python-3.5+-blue.svg)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-3-red.svg)
![MariaDB](https://img.shields.io/badge/MariaDB-10.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Un sistema completo de monitoreo ambiental que captura datos de temperatura y humedad mediante un sensor DHT11, los almacena en una base de datos MariaDB y los visualiza en tiempo real con una interfaz gráfica.

</div>

---

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema de monitoreo ambiental que obtiene lecturas continuas de temperatura y humedad a través de un sensor DHT11 conectado a una Raspberry Pi 3. Los datos se almacenan en una base de datos MariaDB local y se visualizan en una interfaz gráfica desarrollada con Pygame, mostrando tanto los valores actuales como los máximos y mínimos del día.

### ✨ Características Principales

- 📊 **Lectura continua** de temperatura y humedad cada 2 segundos
- 💾 **Almacenamiento persistente** en base de datos MariaDB
- 🖥️ **Interfaz gráfica** en tiempo real con Pygame
- 📈 **Estadísticas diarias** (valores máximos y mínimos)
- 🔄 **Procesamiento multihilo** para operaciones no bloqueantes
- ⚠️ **Manejo robusto de errores** en lectura de sensores y BD

---

## 🛠️ Componentes de Hardware

| Componente | Descripción |
|------------|-------------|
| **Raspberry Pi 3** | Computadora de placa única (SBC) |
| **GrovePi+ Kit** | Shield para Raspberry Pi con conectores Grove |
| **Sensor DHT11** | Sensor de temperatura y humedad digital |
| **Cable Grove** | Para conexión del sensor al puerto digital |

### 📐 Diagrama de Conexión

```
Raspberry Pi 3
     |
     └── GrovePi+ Shield
              |
              └── Puerto Digital D7 ──── Sensor DHT11
```

> **Nota:** El sensor DHT11 está conectado al puerto digital 7 (D7) del GrovePi+. Este puerto puede modificarse en el código según tu configuración.

---

## 💻 Requisitos de Software

### Sistema Operativo
- Raspberry Pi OS (anteriormente Raspbian)
- Python 3.5 o superior (compatible con la sintaxis de Raspberry Pi)

### Dependencias de Python

```bash
# Bibliotecas del sistema
sudo apt-get update
sudo apt-get install python3-pygame python3-mysqldb

# Biblioteca GrovePi
git clone https://github.com/DexterInd/GrovePi.git
cd GrovePi/Script
sudo chmod +x install.sh
sudo ./install.sh
```

### Bibliotecas Utilizadas

- **pygame** - Interfaz gráfica de usuario
- **grovepi** - Comunicación con sensores Grove
- **MySQLdb** - Conector para MariaDB/MySQL
- **threading** - Procesamiento concurrente
- **time** - Control de intervalos de lectura

---

## 🗄️ Configuración de la Base de Datos

### 1. Instalación de MariaDB

```bash
sudo apt-get install mariadb-server mariadb-client
sudo mysql_secure_installation
```

### 2. Creación de la Base de Datos

Accede a MariaDB como root:

```bash
sudo mysql -u root -p
```

Ejecuta los siguientes comandos SQL:

```sql
-- Crear la base de datos
CREATE DATABASE sensores;

-- Crear el usuario con permisos
CREATE USER 'raspiuser'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON sensores.* TO 'raspiuser'@'localhost';
FLUSH PRIVILEGES;

-- Usar la base de datos
USE sensores;

-- Crear la tabla para almacenar lecturas
CREATE TABLE dht11 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura FLOAT NOT NULL,
    humedad FLOAT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_fecha (fecha)
);
```

### 3. Verificación

```sql
-- Verificar la estructura de la tabla
DESCRIBE dht11;

-- Salir de MariaDB
EXIT;
```

### 🔐 Personalización de Credenciales

Para usar tus propias credenciales, modifica las siguientes líneas en `sensor_temp_hum_mariaDB.py`:

```python
conexion = MySQLdb.connect(
    host="localhost",        # Cambiar si la BD está en otro servidor
    user="raspiuser",        # Tu usuario de MariaDB
    passwd="1234",           # Tu contraseña
    db="sensores"            # Nombre de tu base de datos
)
```

---

## 🚀 Instalación y Uso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Temperature-Humidity-MariaDB.git
cd Temperature-Humidity-MariaDB
```

### 2. Configurar el Puerto del Sensor

Abre el archivo `sensor_temp_hum_mariaDB.py` y verifica/modifica:

```python
dht_sensor_port = 7  # Puerto donde está conectado el sensor DHT11
```

### 3. Ejecutar el Programa

```bash
python3 sensor_temp_hum_mariaDB.py
```

### 4. Interfaz de Usuario

Una ventana de Pygame se abrirá mostrando:

- **Temperatura actual** en grados Celsius
- **Humedad actual** en porcentaje
- **Máximos y mínimos del día** para ambas variables

Para cerrar el programa, simplemente cierra la ventana de Pygame.

---

## 📊 Estructura del Código

### Arquitectura del Sistema

```
┌─────────────────────────────────────┐
│         Hilo Principal              │
│   (Pygame - Interfaz Gráfica)      │
└──────────────┬──────────────────────┘
               │
               │ Lee variables globales
               │
┌──────────────▼──────────────────────┐
│      Hilo de Sensor (Daemon)        │
│  - Lee sensor DHT11 cada 2s         │
│  - Actualiza variables temp/hum     │
│  - Guarda en MariaDB                │
└─────────────────────────────────────┘
```

### Funciones Principales

| Función | Descripción |
|---------|-------------|
| `get_sensor_data()` | Lee datos del sensor DHT11 continuamente |
| `display_data()` | Renderiza la interfaz gráfica con Pygame |
| `save_to_db()` | Inserta lecturas en la base de datos |
| `get_daily_min_max()` | Consulta estadísticas del día actual |
| `main()` | Inicializa hilos y bucle principal |

---

## 🔧 Resolución de Problemas

### El sensor no lee datos

```bash
# Verificar que GrovePi esté instalado
python3 -c "import grovepi; print('GrovePi OK')"

# Verificar firmware de GrovePi
cd ~/GrovePi/Firmware
sudo ./firmware_update.sh
```

### Error de conexión a MariaDB

```bash
# Verificar que el servicio esté activo
sudo systemctl status mariadb

# Iniciar si está detenido
sudo systemctl start mariadb

# Probar conexión manual
mysql -u raspiuser -p -h localhost sensores
```

### Error "IOError" o "TypeError" en sensor

- Verifica las conexiones físicas del sensor
- Asegúrate de que el puerto sea el correcto (D7)
- Intenta con otro puerto Grove si persiste el problema
- El DHT11 puede fallar ocasionalmente; el código maneja estos errores

### Ventana de Pygame no aparece

```bash
# Instalar dependencias de SDL
sudo apt-get install python3-pygame libsdl2-dev

# Verificar que DISPLAY esté configurado
echo $DISPLAY
```

---

## 📈 Consultas SQL Útiles

```sql
-- Ver todas las lecturas de hoy
SELECT * FROM dht11 WHERE DATE(fecha) = CURDATE();

-- Promedio de temperatura por hora
SELECT 
    HOUR(fecha) as hora,
    AVG(temperatura) as temp_promedio,
    AVG(humedad) as hum_promedio
FROM dht11
WHERE DATE(fecha) = CURDATE()
GROUP BY HOUR(fecha);

-- Últimas 10 lecturas
SELECT * FROM dht11 ORDER BY fecha DESC LIMIT 10;

-- Limpiar datos antiguos (más de 30 días)
DELETE FROM dht11 WHERE fecha < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

## 🔄 Mejoras Futuras

- [ ] Implementar gráficos históricos con matplotlib
- [ ] Añadir alertas cuando se superen umbrales
- [ ] Crear API REST para acceso remoto
- [ ] Implementar dashboard web con Flask
- [ ] Exportar datos a CSV/Excel
- [ ] Soporte para múltiples sensores
- [ ] Notificaciones por email/Telegram

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Siéntete libre de usar, modificar y distribuir este código.

---

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📧 Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.

---

<div align="center">

**Desarrollado con ❤️ para la comunidad Raspberry Pi**

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub

</div>
