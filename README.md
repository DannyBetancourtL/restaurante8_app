# Sistema de Restaurante — restaurante_app

Estudiante: Danny Henry Betancourt Luzón
Universidad: Universidad Estatal Amazónica
Carrera: Tecnologías de la Información
Asignatura: Programación Orientada a Objetos
Semana: 11
Tema: Relación Usuario–Producto mediante Venta, control de stock y persistencia JSON

Descripción del sistema

restaurante_app es un sistema de consola desarrollado en Python para la administración básica de un restaurante. El sistema permite gestionar productos, usuarios y ventas.

En esta semana se continúa con el desarrollo realizado anteriormente y se incorpora la venta de productos como una nueva operación. La venta permite relacionar a un usuario registrado con un producto, verificar que exista suficiente stock y guardar la operación realizada.

Además, la información de productos, usuarios y ventas se almacena en archivos JSON. De esta manera, los datos no se pierden cuando se cierra el programa y pueden recuperarse nuevamente al iniciar la aplicación.

Datos de ejemplo en el primer arranque

Cuando el programa se ejecuta por primera vez y los archivos productos.json, usuarios.json y ventas.json no contienen información, se cargan algunos datos de ejemplo para poder probar el funcionamiento del sistema.

Restaurante: Sabor Lojano

Productos:

Humitas — Comida — $1.50 — Stock: 15
Jugo de tomate — Bebida — $1.50 — Stock: 20

Usuarios:

Danny Betancourt — 1101234567
Carlos Pérez — 1107654321

En las siguientes ejecuciones, los datos que ya fueron guardados se cargan desde los archivos JSON. De esta manera, la información no se vuelve a registrar ni se generan datos duplicados.

Estructura del proyecto
restaurante_app/

├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
│
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
│
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
│
└── main.py
Responsabilidad de cada componente
Producto

Se encuentra en modelos/producto.py. Esta clase representa los productos disponibles en el restaurante.

Además de almacenar información como código, nombre, categoría, precio y disponibilidad, ahora cuenta con el atributo stock, que permite conocer la cantidad disponible de cada producto.

También tiene el método vender(cantidad), utilizado para disminuir el stock cuando se realiza una venta. Antes de modificarlo se comprueba que exista suficiente cantidad disponible.

La clase también cuenta con los métodos to_dict() y from_dict(), utilizados para guardar los productos en formato JSON y posteriormente reconstruir los objetos cuando se inicia nuevamente el programa.

Usuario

La clase Usuario, ubicada en modelos/usuario.py, representa a las personas registradas en el sistema.

Se realizan validaciones de sus datos y también se permite convertir la información del usuario a un diccionario mediante to_dict(), así como reconstruirlo utilizando from_dict() cuando se recuperan los datos desde el archivo JSON.

Venta

La clase Venta, ubicada en modelos/venta.py, representa una operación de venta realizada en el restaurante.

Una venta relaciona:

El usuario que realiza la compra.
El producto adquirido.
La cantidad comprada.

Para realizar esta relación se utilizan principalmente usuario_id, producto_codigo y cantidad.

La clase no maneja aspectos como facturación, IVA o métodos de pago, ya que el objetivo de esta semana es trabajar con colecciones, relaciones entre objetos y persistencia de información.

Restaurante

La clase Restaurante, ubicada en servicios/restaurante.py, se encarga de administrar las colecciones de productos, usuarios y ventas.

Entre sus principales funciones se encuentra vender_producto(), que realiza las comprobaciones necesarias antes de registrar una venta. También dispone de consultar_ventas_usuario(), que permite consultar las ventas realizadas por un usuario determinado.

Además, proporciona métodos como:

obtener_productos()
obtener_usuarios()
obtener_ventas()

Estos métodos permiten acceder a la información sin tener que modificar directamente las listas internas de la clase.

ArchivoServicio

El archivo servicios/archivo_servicio.py se encarga de guardar y recuperar la información utilizando archivos JSON.

Para esto se utilizan funciones y recursos propios de Python como:

with open()
json.load()
json.dump()

La información se almacena utilizando codificación UTF-8 y se aplica la misma lógica para las tres colecciones del sistema.

main.py

Es el archivo principal del programa. Se encarga de mostrar el menú por consola, solicitar información al usuario y coordinar las operaciones del sistema.

Al iniciar, carga los productos, usuarios y ventas almacenados. Cuando se realiza una operación que modifica la información, se actualizan los archivos JSON correspondientes.

Relación Usuario + Producto → Venta

El proceso para realizar una venta se puede representar de la siguiente manera:

Usuario registrado
       ↓
Producto existente
       ↓
Validar cantidad solicitada
       ↓
Comprobar stock disponible
       ↓
Crear Venta
       ↓
Agregar la venta a la colección
       ↓
Disminuir el stock del producto
       ↓
Guardar ventas.json y productos.json

El método:

Restaurante.vender_producto(
    codigo_producto,
    identificacion_usuario,
    cantidad
)

primero comprueba que el usuario exista y que el producto seleccionado se encuentre registrado.

Después verifica que la cantidad solicitada sea mayor que cero y que el producto tenga suficiente stock.

Si todas las condiciones se cumplen, se crea una nueva Venta, se agrega a la colección de ventas y se descuenta la cantidad correspondiente del stock del producto.

De esta forma se evita registrar una venta cuando no existe el producto, el usuario no está registrado o no hay suficientes unidades disponibles.

Consulta de ventas por usuario

El método:

Restaurante.consultar_ventas_usuario(identificacion_usuario)

permite consultar las ventas realizadas por un usuario específico.

Para hacerlo, se recorre la colección de ventas y se comparan los identificadores de cada venta con la identificación proporcionada.

Por ejemplo:

for venta in self._ventas:
    if venta.usuario_id == identificacion_usuario:
        ...

De esta manera se pueden obtener solamente las operaciones realizadas por el usuario seleccionado.

Persistencia de las tres colecciones

En esta versión del proyecto se guardan tres tipos de información:

productos.json

Contiene los productos registrados y su stock actual.

Se actualiza cuando se registra, modifica o elimina un producto y también cuando se realiza una venta, debido a que la cantidad disponible cambia.

usuarios.json

Contiene los usuarios registrados en el sistema.

Se actualiza cuando se registra un nuevo usuario.

ventas.json

Contiene las ventas realizadas.

Cada vez que se registra una venta, se guarda la nueva información en este archivo.

Una venta puede modificar dos archivos al mismo tiempo:

ventas.json
    ↓
Se registra la nueva venta

productos.json
    ↓
Se actualiza el stock

Esto permite conservar tanto el historial de operaciones como la cantidad actual de productos disponibles.

Manejo de excepciones

El sistema incluye diferentes controles para evitar que errores en los archivos o en los datos provoquen el cierre inesperado del programa.

FileNotFoundError: se presenta cuando alguno de los archivos JSON todavía no existe. En este caso se puede iniciar la colección correspondiente sin información.
json.JSONDecodeError: permite controlar el caso en que un archivo JSON tenga información incorrecta o no pueda ser interpretado.
PermissionError: se controla cuando no existen permisos suficientes para leer o escribir un archivo.
KeyError: puede aparecer cuando un registro recuperado del JSON no contiene alguna de las claves necesarias para reconstruir un objeto.
ValueError: se utiliza para controlar datos que no cumplen las validaciones establecidas, como una cantidad de venta igual o menor que cero o un stock inválido.

Los errores de registros individuales se manejan sin afectar innecesariamente al resto de la información almacenada.

Comprobación del funcionamiento

Para comprobar el funcionamiento del sistema se realizaron diferentes pruebas:

Se ejecutó main.py sin contar inicialmente con los archivos JSON.
Se comprobó el registro y almacenamiento de usuarios y productos.
Se realizó una venta de un producto disponible.
Se verificó que el stock disminuyera después de la venta.
Se comprobó que la venta quedara registrada en ventas.json.
Se consultaron las ventas realizadas por un usuario.
Se cerró el programa y se volvió a ejecutar para comprobar que los datos fueran recuperados desde los archivos JSON.
Se intentó realizar una venta con una cantidad superior al stock disponible y se comprobó que la operación fuera rechazada.

Estas pruebas permitieron comprobar tanto el funcionamiento de las colecciones como la persistencia de los datos.

Instrucciones de ejecución

Para ejecutar el proyecto se deben seguir los siguientes pasos:

Tener instalado Python 3.9 o una versión superior.
Ubicarse en la carpeta principal del proyecto restaurante_app.
Ejecutar el archivo principal:
python main.py

En sistemas donde se utilice python3, también se puede ejecutar:

python3 main.py
Utilizar las opciones disponibles en el menú de consola.

Los archivos correspondientes a productos, usuarios y ventas se almacenan automáticamente dentro de la carpeta datos/.

Reflexión

El desarrollo de esta semana permitió ampliar el funcionamiento del sistema del restaurante, ya que anteriormente se trabajaba principalmente con productos y usuarios y ahora se incorpora una relación entre ellos mediante la venta.

Crear una clase Venta permite mantener un registro de las operaciones realizadas y no solamente disminuir el stock del producto. Gracias a esto es posible saber qué usuario realizó una compra, qué producto adquirió y qué cantidad compró.

También fue importante trabajar con las tres colecciones y su almacenamiento en archivos JSON. Esto permite que la información permanezca disponible después de cerrar el programa y pueda ser utilizada nuevamente cuando se vuelva a ejecutar.

Finalmente, separar las clases de los servicios y del archivo main.py ayuda a mantener el proyecto organizado. Cada parte tiene una función específica: los modelos representan los datos, Restaurante controla las operaciones y ArchivoServicio se encarga de la persistencia. Esto facilita continuar agregando nuevas funciones al sistema en las siguientes semanas.