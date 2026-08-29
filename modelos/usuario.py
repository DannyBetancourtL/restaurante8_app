"""Modulo que contiene la clase Usuario."""

from typing import Any, Dict


class Usuario:
    """Representa de forma general a una persona registrada en el sistema.

    Esta clase concentra la informacion basica de cualquier persona
    registrada (identificacion, nombre y correo), sin definir todavia
    una jerarquia de tipos especificos de usuario. Ademas, sabe
    convertirse a un diccionario compatible con JSON (`to_dict`) y
    reconstruirse a partir de uno (`from_dict`), lo que permite
    persistir usuarios en un archivo.
    """

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        self._validar_datos(identificacion, nombre, correo)
        self.identificacion: str = identificacion
        self.nombre: str = nombre
        self.correo: str = correo

    @staticmethod
    def _validar_datos(identificacion: str, nombre: str, correo: str) -> None:
        """Valida los datos minimos de un usuario.

        Lanza ValueError si algun dato no es coherente, evitando crear
        objetos Usuario invalidos ya sea desde el menu o al
        reconstruirlos desde el archivo JSON.
        """
        if not identificacion or not str(identificacion).strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not correo or "@" not in correo:
            raise ValueError("El correo del usuario no es válido.")

    def mostrar_informacion(self) -> str:
        """Devuelve una cadena con la informacion del usuario."""
        return (
            f"Identificación: {self.identificacion} | Nombre: {self.nombre} | "
            f"Correo: {self.correo}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el usuario a un diccionario compatible con JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Usuario":
        """Reconstruye un objeto Usuario a partir de un diccionario.

        Si falta alguna clave esperada, se propaga un KeyError con un
        mensaje claro; si algun valor es invalido, la propia
        validacion del constructor lanza un ValueError.
        """
        try:
            return cls(
                identificacion=str(datos["identificacion"]),
                nombre=str(datos["nombre"]),
                correo=str(datos["correo"]),
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de usuario no contiene la clave requerida: {error}"
            ) from error
