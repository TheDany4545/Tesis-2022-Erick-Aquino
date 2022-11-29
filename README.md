# Estimulador nervio vago y su varilla programadora 2022
En este respositorio se encuentra la combinación de los avances previos a la Fase IV. En esta fase se logró crear un modo de reconocimiento automático. Además de la creacion de PCB para la varilla programadora.

## Modo automático
Es basado en el modo de funcionamiento de *detección y respuesta* también conocido como *AutoStim* de los modelos LivaNova 106 y 1000. Consiste en emplear un sistema de monitoreo y relocección de información de impulsos eléctricos de la actividad cardíaca mediante un electrocardiograma (ECG). La administración de la dosis para la terapia se activa de forma automática al momento de detectar un aumento rápido en la frecuencia cardiaca, la cual es asociada a las convulsiones.

### Documentación
Se enceuntran artículos cientificos, datasheets de distintos componentes y microcontroladores, pinouts y base de datos en formato .csv para hacer las pruebas.

### Estimulador
Carpeta donde se encuentra los códigos de los microcontroladores ESP8266 y Trinket M0 para la estimulación VNS y la recepción de parámetros. También se encuntran los diseños de PCB's de distintos años.

### Recursos
Capeta donde se encuentra la libreria PyHRV modificada para la obtención de resultados en el análisis de los ECG´s. También se encuentra una herramienta de Matlab obtenida desde Physionet para la simulación de un ECG donde uno pude modificar parámetros de simulación. Se agregó un archivo .txt con un link para descargar todas las librerias y se describe la instalación en anaconda.

### Varilla Programadora
En la varilla programadora se tiene el envio de parámetros el cual es modificable a través de una interfaz gráfica la cual se ejecuta desde python y esto lo hace a través del microcontrolador ESP8266 al cual se le carga un programa en C que permite la comunicación entre la interfaz gráfica y el estimualdor por medio del envio de parámetros a través del NRFL24L01.

<p align="center">
![ECGV3](https://user-images.githubusercontent.com/45274181/204594546-e67789b7-99ad-4b47-ba8b-1eb101cf408b.gif)

</p>



