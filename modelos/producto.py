"""Modulo que contiene la clase Producto."""

from typing import Any, Dict


class Producto:
    """Representa un producto del restaurante.

    El codigo se genera automaticamente desde el servicio Restaurante,
    por lo que no se solicita manualmente al usuario. Ademas de la
    logica propia del dominio, la clase sabe convertirse a un
    diccionario compatible con JSON (`to_dict`) y reconstruirse a
    partir de uno (`from_dict`), lo que permite persistir productos en
    un archivo sin que el resto del sistema deje de trabajar con
    objetos Producto.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        disponible: bool = True,
        stock: int = 0,
    ) -> None:
        self._validar_datos(codigo, nombre, categoria, precio, stock)
        self.codigo: str = codigo
        self.nombre: str = nombre
        self.categoria: str = categoria
        self.precio: float = precio
        self.disponible: bool = disponible
        self.stock: int = stock

    @staticmethod
    def _validar_datos(
        codigo: str, nombre: str, categoria: str, precio: float, stock: int
    ) -> None:
        """Valida los datos minimos de un producto.

        Lanza ValueError si algun dato no es coherente, evitando crear
        objetos Producto invalidos ya sea desde el menu o al
        reconstruirlos desde el archivo JSON.
        """
        if not codigo or not str(codigo).strip():
            raise ValueError("El código del producto no puede estar vacío.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not categoria or not categoria.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio del producto debe ser un número mayor o igual a cero.")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("El stock del producto debe ser un número entero mayor o igual a cero.")

    def vender(self, cantidad: int) -> None:
        """Disminuye el stock del producto en la cantidad indicada.

        Se asume que la validacion de cantidad y stock suficiente ya
        fue realizada por quien invoca este metodo (Restaurante). Aun
        asi, se protege el invariante de que el stock nunca quede en
        valores negativos.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")
        if cantidad > self.stock:
            raise ValueError("No hay stock suficiente para realizar la venta.")
        self.stock -= cantidad

    def mostrar_informacion(self) -> str:
        """Devuelve una cadena con la informacion del producto."""
        return (
            f"Código: {self.codigo} | Producto: {self.nombre} | "
            f"Categoría: {self.categoria} | Precio: ${self.precio:.2f} | "
            f"Disponible: {self.disponible} | Stock: {self.stock}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el producto a un diccionario compatible con JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "disponible": self.disponible,
            "stock": self.stock,
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Producto":
        """Reconstruye un objeto Producto a partir de un diccionario.

        Se espera que `datos` provenga de un registro leido desde el
        archivo JSON. Si falta alguna clave esperada, se propaga un
        KeyError con un mensaje claro; si algun valor es invalido, la
        propia validacion del constructor lanza un ValueError. Ambas
        excepciones son responsabilidad de quien llama a este metodo
        (ArchivoServicio), que decide como manejarlas.
        """
        try:
            return cls(
                codigo=str(datos["codigo"]),
                nombre=str(datos["nombre"]),
                categoria=str(datos["categoria"]),
                precio=float(datos["precio"]),
                disponible=bool(datos["disponible"]),
                stock=int(datos["stock"]),
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de producto no contiene la clave requerida: {error}"
            ) from error
