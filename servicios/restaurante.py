"""Modulo que contiene la clase de servicio Restaurante."""

from typing import Dict, List, Optional, Set

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """Servicio encargado de administrar productos, usuarios y ventas.

    Aplica varias estructuras de datos de Python, cada una con una
    finalidad concreta dentro del sistema:

    - list: `self._productos`, `self._usuarios` y `self._ventas`
      mantienen las colecciones dinamicas de objetos que se registran,
      listan, actualizan, eliminan o consultan durante la ejecucion.
    - dict: `self._indice_productos` asocia cada codigo de producto
      (clave) con su objeto Producto (valor), permitiendo busquedas,
      actualizaciones y eliminaciones eficientes sin recorrer toda la
      lista cada vez.
    - set: `obtener_categorias()` recorre los productos registrados y
      devuelve un conjunto con las categorias unicas, sin duplicados.
    """

    def __init__(self, nombre: str = "Restaurante Sabor Lojano") -> None:
        self.nombre: str = nombre
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._ventas: List[Venta] = []
        self._indice_productos: Dict[str, Producto] = {}
        self._contador_producto: int = 0

    # ---------------------- Gestion de productos ----------------------

    def cargar_productos_iniciales(self, productos: List[Producto]) -> None:
        """Incorpora al servicio una lista de productos ya reconstruidos.

        Se utiliza al iniciar la aplicacion, con los objetos Producto
        recuperados por ArchivoServicio desde datos/productos.json. El
        contador interno de codigos se ajusta para continuar la
        numeracion sin repetir codigos ya existentes.
        """
        for producto in productos:
            self.registrar_producto(producto)
            try:
                numero = int(producto.codigo)
                if numero > self._contador_producto:
                    self._contador_producto = numero
            except ValueError:
                # Codigos no numericos no afectan el contador automatico.
                pass

    def obtener_productos(self) -> List[Producto]:
        """Devuelve la lista de objetos Producto registrados.

        Se utiliza para persistir la coleccion completa en JSON tras
        una operacion de registro, actualizacion, eliminacion o venta.
        """
        return list(self._productos)

    def generar_codigo_producto(self) -> str:
        """Genera automaticamente el siguiente codigo de producto."""
        self._contador_producto += 1
        return str(self._contador_producto)

    def registrar_producto(self, producto: Producto) -> bool:
        """Registra un producto si su codigo no esta repetido.

        Devuelve True si el registro fue exitoso, False si el codigo
        ya existia.
        """
        if producto.codigo in self._indice_productos:
            return False
        self._productos.append(producto)
        self._indice_productos[producto.codigo] = producto
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """Busca un producto por su codigo. Devuelve None si no existe."""
        return self._indice_productos.get(codigo)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: Optional[str] = None,
        categoria: Optional[str] = None,
        precio: Optional[float] = None,
        disponible: Optional[bool] = None,
        stock: Optional[int] = None,
    ) -> bool:
        """Actualiza los campos indicados de un producto existente.

        Solo se modifican los campos que se reciban distintos de None,
        lo que permite actualizaciones parciales. Devuelve True si el
        producto existe y fue actualizado, False si no se encontro.
        """
        producto = self._indice_productos.get(codigo)
        if producto is None:
            return False

        nuevo_nombre = nombre if nombre is not None else producto.nombre
        nueva_categoria = categoria if categoria is not None else producto.categoria
        nuevo_precio = precio if precio is not None else producto.precio
        nuevo_stock = stock if stock is not None else producto.stock

        # Se reutilizan las validaciones de Producto para asegurar que
        # una actualizacion parcial no deje el objeto en un estado
        # invalido (por ejemplo, un precio o stock negativo).
        Producto._validar_datos(producto.codigo, nuevo_nombre, nueva_categoria, nuevo_precio, nuevo_stock)

        producto.nombre = nuevo_nombre
        producto.categoria = nueva_categoria
        producto.precio = nuevo_precio
        producto.stock = nuevo_stock
        if disponible is not None:
            producto.disponible = disponible
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """Elimina un producto por su codigo.

        Devuelve True si el producto existia y fue eliminado, False si
        no se encontro.
        """
        producto = self._indice_productos.pop(codigo, None)
        if producto is None:
            return False
        self._productos.remove(producto)
        return True

    def listar_productos(self) -> List[str]:
        """Devuelve la informacion de todos los productos registrados."""
        return [producto.mostrar_informacion() for producto in self._productos]

    def obtener_categorias(self) -> Set[str]:
        """Devuelve el conjunto de categorias unicas de los productos.

        Se utiliza un set para eliminar automaticamente las categorias
        repetidas entre los distintos productos registrados.
        """
        return {producto.categoria for producto in self._productos}

    # ----------------------- Gestion de usuarios -----------------------

    def cargar_usuarios_iniciales(self, usuarios: List[Usuario]) -> None:
        """Incorpora al servicio una lista de usuarios ya reconstruidos.

        Se utiliza al iniciar la aplicacion, con los objetos Usuario
        recuperados por ArchivoServicio desde datos/usuarios.json.
        """
        for usuario in usuarios:
            self.registrar_usuario(usuario)

    def obtener_usuarios(self) -> List[Usuario]:
        """Devuelve la lista de objetos Usuario registrados.

        Se utiliza para persistir la coleccion completa en JSON tras
        una operacion de registro.
        """
        return list(self._usuarios)

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """Registra un usuario si su identificacion no esta repetida.

        Devuelve True si el registro fue exitoso, False si la
        identificacion ya existia.
        """
        if self.buscar_usuario(usuario.identificacion) is not None:
            return False
        self._usuarios.append(usuario)
        return True

    def listar_usuarios(self) -> List[str]:
        """Devuelve la informacion de todos los usuarios registrados."""
        return [usuario.mostrar_informacion() for usuario in self._usuarios]

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        """Busca un usuario por su identificacion. Devuelve None si no existe."""
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    # ------------------------- Gestion de ventas -------------------------

    def cargar_ventas_iniciales(self, ventas: List[Venta]) -> None:
        """Incorpora al servicio una lista de ventas ya reconstruidas.

        Se utiliza al iniciar la aplicacion, con los objetos Venta
        recuperados por ArchivoServicio desde datos/ventas.json. No se
        vuelve a descontar stock: el stock guardado en productos.json
        ya refleja el resultado de estas ventas.
        """
        self._ventas.extend(ventas)

    def obtener_ventas(self) -> List[Venta]:
        """Devuelve la lista de objetos Venta registrados.

        Se utiliza para persistir la coleccion completa en JSON tras
        realizar una nueva venta.
        """
        return list(self._ventas)

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        """Registra la venta de un producto a un usuario.

        Antes de registrar la venta se comprueba que el usuario exista,
        que el producto exista, que la cantidad solicitada sea mayor
        que cero y que exista stock suficiente. Si todo es valido, se
        crea la Venta, se agrega a la coleccion y se descuenta el stock
        del producto. Devuelve True si la venta se realizo con exito,
        False en caso contrario.
        """
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        producto.vender(cantidad)
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> List[Venta]:
        """Devuelve unicamente las ventas asociadas a un usuario.

        Recorre la coleccion de ventas y filtra aquellas cuyo
        usuario_id coincide con la identificacion recibida.
        """
        ventas_usuario: List[Venta] = []
        for venta in self._ventas:
            if venta.usuario_id == identificacion_usuario:
                ventas_usuario.append(venta)
        return ventas_usuario
