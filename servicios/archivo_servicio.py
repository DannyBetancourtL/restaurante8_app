"""Modulo que contiene la clase ArchivoServicio.

Concentra toda la lectura y escritura de los archivos JSON del
sistema (productos, usuarios y ventas), manteniendo la persistencia
separada de la logica de negocio que vive en el servicio Restaurante.
"""

import json
from pathlib import Path
from typing import Any, List, Type, TypeVar

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

T = TypeVar("T")


class ArchivoServicio:
    """Servicio encargado de cargar y guardar productos, usuarios y ventas.

    No conoce reglas de negocio del restaurante (duplicados, stock,
    etc.): solo sabe convertir entre objetos y sus archivos JSON
    correspondientes, manejando de forma controlada los errores
    propios del acceso a archivos y del formato de los datos.
    """

    def __init__(
        self,
        ruta_productos: str = "datos/productos.json",
        ruta_usuarios: str = "datos/usuarios.json",
        ruta_ventas: str = "datos/ventas.json",
    ) -> None:
        self.ruta_productos: Path = Path(ruta_productos)
        self.ruta_usuarios: Path = Path(ruta_usuarios)
        self.ruta_ventas: Path = Path(ruta_ventas)

    # ------------------------- Metodos genericos -------------------------

    def _cargar_lista(self, ruta_archivo: Path, clase: Type[T]) -> List[T]:
        """Carga y reconstruye una lista de objetos desde un archivo JSON.

        `clase` debe exponer un metodo de clase `from_dict(dict) -> T`.
        Si el archivo no existe, esta vacio, no es JSON valido, o no
        hay permisos suficientes, se informa la situacion y se
        devuelve una lista vacia en lugar de detener el programa.
        Los registros individuales invalidos se omiten uno a uno.
        """
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido: Any = json.load(archivo)
        except FileNotFoundError:
            print(
                f"Aviso: no se encontró '{ruta_archivo}'. "
                "Se iniciará con una colección vacía."
            )
            return []
        except json.JSONDecodeError:
            print(
                f"Aviso: el archivo '{ruta_archivo}' no contiene un JSON válido. "
                "Se iniciará con una colección vacía."
            )
            return []
        except PermissionError:
            print(
                f"Error: no se tienen permisos para leer '{ruta_archivo}'. "
                "Se iniciará con una colección vacía."
            )
            return []

        if not isinstance(contenido, list):
            print(
                f"Aviso: el contenido de '{ruta_archivo}' no tiene el formato "
                "esperado (se esperaba una lista). Se ignorará."
            )
            return []

        objetos: List[T] = []
        for indice, registro in enumerate(contenido, start=1):
            try:
                if not isinstance(registro, dict):
                    raise ValueError("el registro no es un objeto JSON válido")
                objetos.append(clase.from_dict(registro))  # type: ignore[attr-defined]
            except KeyError as error:
                print(f"Aviso: se omitió el registro #{indice} de '{ruta_archivo}' ({error}).")
            except ValueError as error:
                print(f"Aviso: se omitió el registro #{indice} de '{ruta_archivo}' ({error}).")

        return objetos

    def _guardar_lista(self, ruta_archivo: Path, objetos: List[Any]) -> bool:
        """Guarda una lista de objetos en un archivo JSON.

        Cada objeto debe exponer `to_dict()`. Devuelve True si el
        guardado fue exitoso, False si ocurrió un error controlado de
        acceso al archivo.
        """
        datos = [objeto.to_dict() for objeto in objetos]

        try:
            ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
            return True
        except PermissionError:
            print(
                f"Error: no se tienen permisos para escribir en '{ruta_archivo}'. "
                "Los cambios no se guardaron en el archivo."
            )
            return False
        except OSError as error:
            print(f"Error al guardar '{ruta_archivo}': {error}")
            return False

    # ---------------------------- Productos ----------------------------

    def cargar_productos(self) -> List[Producto]:
        """Carga los productos almacenados en productos.json."""
        return self._cargar_lista(self.ruta_productos, Producto)

    def guardar_productos(self, productos: List[Producto]) -> bool:
        """Guarda la lista de productos en productos.json."""
        return self._guardar_lista(self.ruta_productos, productos)

    # ---------------------------- Usuarios -----------------------------

    def cargar_usuarios(self) -> List[Usuario]:
        """Carga los usuarios almacenados en usuarios.json."""
        return self._cargar_lista(self.ruta_usuarios, Usuario)

    def guardar_usuarios(self, usuarios: List[Usuario]) -> bool:
        """Guarda la lista de usuarios en usuarios.json."""
        return self._guardar_lista(self.ruta_usuarios, usuarios)

    # ----------------------------- Ventas ------------------------------

    def cargar_ventas(self) -> List[Venta]:
        """Carga las ventas almacenadas en ventas.json."""
        return self._cargar_lista(self.ruta_ventas, Venta)

    def guardar_ventas(self, ventas: List[Venta]) -> bool:
        """Guarda la lista de ventas en ventas.json."""
        return self._guardar_lista(self.ruta_ventas, ventas)
