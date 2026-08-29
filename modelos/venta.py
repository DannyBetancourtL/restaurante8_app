"""Modulo que contiene la clase Venta."""

from typing import Any, Dict


class Venta:
    """Representa la relación entre un usuario y un producto vendido.

    Una venta conserva la identificación del usuario que compró, el
    código del producto vendido y la cantidad adquirida. No incluye
    facturación, IVA, descuentos ni métodos de pago: su única
    responsabilidad es registrar esta relación dentro de una colección
    y permitir su posterior consulta.
    """

    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int) -> None:
        self._validar_datos(usuario_id, producto_codigo, cantidad)
        self.usuario_id: str = usuario_id
        self.producto_codigo: str = producto_codigo
        self.cantidad: int = cantidad

    @staticmethod
    def _validar_datos(usuario_id: str, producto_codigo: str, cantidad: int) -> None:
        """Valida los datos minimos de una venta."""
        if not usuario_id or not str(usuario_id).strip():
            raise ValueError("La venta debe estar asociada a un usuario válido.")
        if not producto_codigo or not str(producto_codigo).strip():
            raise ValueError("La venta debe estar asociada a un producto válido.")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser un número entero mayor que cero.")

    def mostrar_informacion(self, nombre_producto: str = "") -> str:
        """Devuelve una cadena con la informacion de la venta.

        Si se recibe el nombre del producto (obtenido desde el
        servicio), se incluye para hacer el resultado más legible.
        """
        detalle_producto = f"{self.producto_codigo}"
        if nombre_producto:
            detalle_producto = f"{self.producto_codigo} ({nombre_producto})"
        return (
            f"Usuario: {self.usuario_id} | Producto: {detalle_producto} | "
            f"Cantidad: {self.cantidad}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la venta a un diccionario compatible con JSON."""
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Venta":
        """Reconstruye un objeto Venta a partir de un diccionario."""
        try:
            return cls(
                usuario_id=str(datos["usuario_id"]),
                producto_codigo=str(datos["producto_codigo"]),
                cantidad=int(datos["cantidad"]),
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de venta no contiene la clave requerida: {error}"
            ) from error
