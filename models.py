class Cliente:
    """Modelo para representar un cliente en el sistema."""
    
    def __init__(self, id=None, nombre="", email="", telefono="", direccion=""):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
    
    @classmethod
    def from_db_row(cls, row):
        """Crea una instancia de Cliente a partir de una fila de la base de datos."""
        if row is None:
            return None
        return cls(
            id=row['id'],
            nombre=row['nombre'],
            email=row['email'],
            telefono=row['telefono'],
            direccion=row['direccion']
        )
    
    def __str__(self):
        return f"Cliente(id={self.id}, nombre='{self.nombre}', email='{self.email}')"


class Producto:
    """Modelo para representar un producto en el sistema."""
    
    def __init__(self, id=None, nombre="", descripcion="", precio=0.0, stock=0):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
    
    @classmethod
    def from_db_row(cls, row):
        """Crea una instancia de Producto a partir de una fila de la base de datos."""
        if row is None:
            return None
        return cls(
            id=row['id'],
            nombre=row['nombre'],
            descripcion=row['descripcion'],
            precio=row['precio'],
            stock=row['stock']
        )
    
    def __str__(self):
        return f"Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio}, stock={self.stock})"


class Pedido:
    """Modelo para representar un pedido en el sistema."""
    
    def __init__(self, id=None, cliente_id=None, fecha="", estado="", total=0.0, cliente=None, detalles=None):
        self.id = id
        self.cliente_id = cliente_id
        self.fecha = fecha
        self.estado = estado
        self.total = total
        self.cliente = cliente  # Objeto Cliente asociado
        self.detalles = detalles or []  # Lista de detalles del pedido
    
    @classmethod
    def from_db_row(cls, row, cliente=None):
        """Crea una instancia de Pedido a partir de una fila de la base de datos."""
        if row is None:
            return None
        return cls(
            id=row['id'],
            cliente_id=row['cliente_id'],
            fecha=row['fecha'],
            estado=row['estado'],
            total=row['total'],
            cliente=cliente
        )
    
    def __str__(self):
        return f"Pedido(id={self.id}, cliente_id={self.cliente_id}, fecha='{self.fecha}', total={self.total})"


class DetallePedido:
    """Modelo para representar un detalle de pedido en el sistema."""
    
    def __init__(self, id=None, pedido_id=None, producto_id=None, cantidad=0, precio_unitario=0.0, producto=None):
        self.id = id
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.producto = producto  # Objeto Producto asociado
    
    @classmethod
    def from_db_row(cls, row, producto=None):
        """Crea una instancia de DetallePedido a partir de una fila de la base de datos."""
        if row is None:
            return None
        return cls(
            id=row['id'],
            pedido_id=row['pedido_id'],
            producto_id=row['producto_id'],
            cantidad=row['cantidad'],
            precio_unitario=row['precio_unitario'],
            producto=producto
        )
    
    def subtotal(self):
        """Calcula el subtotal del detalle (precio unitario * cantidad)."""
        return self.precio_unitario * self.cantidad
    
    def __str__(self):
        return f"DetallePedido(id={self.id}, pedido_id={self.pedido_id}, producto_id={self.producto_id}, cantidad={self.cantidad})"