# Nfc-detector
El proyecto consiste en el desarrollo de una aplicación web diseñada para gestionar el registro de entradas y salidas de estudiantes utilizando tecnología NFC (Near Field Communication). Cada estudiante posee un tag NFC que almacena su información personal, como su identificación o matrícula.

Cuando el tag es escaneado, la aplicación extrae la información contenida en el mismo y registra automáticamente la hora y el evento (entrada o salida) en un listado. Este registro se almacena en blocs de notas para un respaldo sencillo y eficiente de los datos. Además, la aplicación cuenta con un apartado visual donde se despliega el historial de movimientos, permitiendo consultar en tiempo real las entradas y salidas de cada estudiante de manera organizada y accesible.

Debido a las restricciones de permisos al utilizar el lector NFC en navegadores móviles, se implementó Ngrok para exponer la aplicación de manera segura y accesible desde un servidor público. Esto permitió que la funcionalidad de NFC estuviera disponible en dispositivos móviles, garantizando una experiencia fluida para los usuarios.

Este sistema tiene como objetivo optimizar el control de acceso en entornos educativos, reduciendo la necesidad de procesos manuales y mejorando la precisión del registro de datos.
