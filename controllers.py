import sqlite3
from database import get_db_connection
from models import Cliente, Producto, Pedido, DetallePedido
import datetime

class ClienteController:
    """Controlador para operaciones CRUD de clientes."""
    
    def crear(self, cliente):
        """Crea un nuevo cliente en la base de datos."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (?, ?, ?, ?)',
                (cliente.nombre, cliente.email, cliente.telefono, cliente.direccion)
            )
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al crear cliente: {e}")
            return False
    
    def obtener_por_id(self, id):
        """Obtiene un cliente por su ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clientes WHERE id = ?', (id,))
            row = cursor.fetchone()
            
            conn.close()
            return Cliente.from_db_row(row) if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener cliente: {e}")
            return None
    
    def obtener_por_email(self, email):
        """Obtiene un cliente por su email."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clientes WHERE email = ?', (email,))
            row = cursor.fetchone()
            
            conn.close()
            return Cliente.from_db_row(row) if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener cliente por email: {e}")
            return None
    
    def listar_todos(self):
        """Obtiene todos los clientes."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clientes ORDER BY nombre')
            rows = cursor.fetchall()
            
            conn.close()
            return [Cliente.from_db_row(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al listar clientes: {e}")
            return []
    
    def buscar(self, termino):
        """Busca clientes por nombre, email o teléfono."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT * FROM clientes WHERE nombre LIKE ? OR email LIKE ? OR telefono LIKE ? ORDER BY nombre',
                (f'%{termino}%', f'%{termino}%', f'%{termino}%')
            )
            rows = cursor.fetchall()
            
            conn.close()
            return [Cliente.from_db_row(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al buscar clientes: {e}")
            return []
    
    def actualizar(self, cliente):
        """Actualiza un cliente existente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE clientes SET nombre = ?, email = ?, telefono = ?, direccion = ? WHERE id = ?',
                (cliente.nombre, cliente.email, cliente.telefono, cliente.direccion, cliente.id)
            )
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar cliente: {e}")
            return False
    
    def eliminar(self, id):
        """Elimina un cliente por su ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar si el cliente tiene pedidos asociados
            cursor.execute('SELECT COUNT(*) FROM pedidos WHERE cliente_id = ?', (id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                conn.close()
                return False  # No se puede eliminar porque tiene pedidos asociados
            
            cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar cliente: {e}")
            return False


class ProductoController:
    """Controlador para operaciones CRUD de productos."""
    
    def crear(self, producto):
        """Crea un nuevo producto en la base de datos."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)',
                (producto.nombre, producto.descripcion, producto.precio, producto.stock)
            )
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al crear producto: {e}")
            return False
    
    def obtener_por_id(self, id):
        """Obtiene un producto por su ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
            row = cursor.fetchone()
            
            conn.close()
            return Producto.from_db_row(row) if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener producto: {e}")
            return None
    
    def listar_todos(self):
        """Obtiene todos los productos."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM productos ORDER BY nombre')
            rows = cursor.fetchall()
            
            conn.close()
            return [Producto.from_db_row(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al listar productos: {e}")
            return []
    
    def buscar(self, termino):
        """Busca productos por nombre o descripción."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT * FROM productos WHERE nombre LIKE ? OR descripcion LIKE ? ORDER BY nombre',
                (f'%{termino}%', f'%{termino}%')
            )
            rows = cursor.fetchall()
            
            conn.close()
            return [Producto.from_db_row(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al buscar productos: {e}")
            return []
    
    def actualizar(self, producto):
        """Actualiza un producto existente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE productos SET nombre = ?, descripcion = ?, precio = ?, stock = ? WHERE id = ?',
                (producto.nombre, producto.descripcion, producto.precio, producto.stock, producto.id)
            )
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar producto: {e}")
            return False
    
    def eliminar(self, id):
        """Elimina un producto por su ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar si el producto está en algún pedido
            cursor.execute('SELECT COUNT(*) FROM detalles_pedido WHERE producto_id = ?', (id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                conn.close()
                return False  # No se puede eliminar porque está en pedidos
            
            cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar producto: {e}")
            return False
    
    def actualizar_stock(self, id, cantidad):
        """Actualiza el stock de un producto."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('UPDATE productos SET stock = stock + ? WHERE id = ?', (cantidad, id))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar stock: {e}")
            return False


class PedidoController:
    """Controlador para operaciones CRUD de pedidos."""
    
    def crear(self, pedido, detalles):
        """Crea un nuevo pedido con sus detalles."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insertar el pedido
            cursor.execute(
                'INSERT INTO pedidos (cliente_id, fecha, estado, total) VALUES (?, ?, ?, ?)',
                (pedido.cliente_id, pedido.fecha, pedido.estado, pedido.total)
            )
            
            # Obtener el ID del pedido recién insertado
            pedido_id = cursor.lastrowid
            
            # Insertar los detalles del pedido
            for detalle in detalles:
                cursor.execute(
                    'INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)',
                    (pedido_id, detalle.producto_id, detalle.cantidad, detalle.precio_unitario)
                )
                
                # Actualizar el stock del producto
                cursor.execute(
                    'UPDATE productos SET stock = stock - ? WHERE id = ?',
                    (detalle.cantidad, detalle.producto_id)
                )
            
            conn.commit()
            conn.close()
            return pedido_id
        except sqlite3.Error as e:
            print(f"Error al crear pedido: {e}")
            return None
    
    def obtener_por_id(self, id):
        """Obtiene un pedido por su ID, incluyendo cliente y detalles."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Obtener el pedido
            cursor.execute('SELECT * FROM pedidos WHERE id = ?', (id,))
            row_pedido = cursor.fetchone()
            
            if not row_pedido:
                conn.close()
                return None
            
            # Obtener el cliente del pedido
            cursor.execute('SELECT * FROM clientes WHERE id = ?', (row_pedido['cliente_id'],))
            row_cliente = cursor.fetchone()
            cliente = Cliente.from_db_row(row_cliente) if row_cliente else None
            
            # Crear el objeto pedido
            pedido = Pedido.from_db_row(row_pedido, cliente)
            
            # Obtener los detalles del pedido
            cursor.execute('SELECT * FROM detalles_pedido WHERE pedido_id = ?', (id,))
            rows_detalles = cursor.fetchall()
            
            detalles = []
            for row_detalle in rows_detalles:
                # Obtener el producto del detalle
                cursor.execute('SELECT * FROM productos WHERE id = ?', (row_detalle['producto_id'],))
                row_producto = cursor.fetchone()
                producto = Producto.from_db_row(row_producto) if row_producto else None
                
                detalle = DetallePedido.from_db_row(row_detalle, producto)
                detalles.append(detalle)
            
            pedido.detalles = detalles
            
            conn.close()
            return pedido
        except sqlite3.Error as e:
            print(f"Error al obtener pedido: {e}")
            return None
    
    def listar_todos(self):
        """Obtiene todos los pedidos con información básica."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.*, c.nombre as cliente_nombre 
                FROM pedidos p 
                JOIN clientes c ON p.cliente_id = c.id 
                ORDER BY p.fecha DESC
            ''')
            rows = cursor.fetchall()
            
            pedidos = []
            for row in rows:
                cliente = Cliente(id=row['cliente_id'], nombre=row['cliente_nombre'])
                pedido = Pedido.from_db_row(row, cliente)
                pedidos.append(pedido)
            
            conn.close()
            return pedidos
        except sqlite3.Error as e:
            print(f"Error al listar pedidos: {e}")
            return []
    
    def listar_por_cliente(self, cliente_id):
        """Obtiene todos los pedidos de un cliente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.*, c.nombre as cliente_nombre 
                FROM pedidos p 
                JOIN clientes c ON p.cliente_id = c.id 
                WHERE p.cliente_id = ? 
                ORDER BY p.fecha DESC
            ''', (cliente_id,))
            rows = cursor.fetchall()
            
            pedidos = []
            for row in rows:
                cliente = Cliente(id=row['cliente_id'], nombre=row['cliente_nombre'])
                pedido = Pedido.from_db_row(row, cliente)
                pedidos.append(pedido)
            
            conn.close()
            return pedidos
        except sqlite3.Error as e:
            print(f"Error al listar pedidos por cliente: {e}")
            return []
    
    def actualizar(self, pedido):
        """Actualiza un pedido existente en la base de datos."""
        try:
            conn = sqlite3.connect('techlab.db')
            cursor = conn.cursor()
            
            # Actualizar el pedido
            cursor.execute(
                "UPDATE pedidos SET estado = ? WHERE id = ?",
                (pedido.estado, pedido.id)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar pedido: {e}")
            return False
    
    def actualizar_estado(self, id, estado):
        """Actualiza el estado de un pedido."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('UPDATE pedidos SET estado = ? WHERE id = ?', (estado, id))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar estado del pedido: {e}")
            return False
    
    def eliminar(self, id):
        """Elimina un pedido y sus detalles, y restaura el stock de productos."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Obtener los detalles del pedido para restaurar el stock
            cursor.execute('SELECT producto_id, cantidad FROM detalles_pedido WHERE pedido_id = ?', (id,))
            detalles = cursor.fetchall()
            
            # Restaurar el stock de cada producto
            for detalle in detalles:
                cursor.execute(
                    'UPDATE productos SET stock = stock + ? WHERE id = ?',
                    (detalle['cantidad'], detalle['producto_id'])
                )
            
            # Eliminar los detalles del pedido
            cursor.execute('DELETE FROM detalles_pedido WHERE pedido_id = ?', (id,))
            
            # Eliminar el pedido
            cursor.execute('DELETE FROM pedidos WHERE id = ?', (id,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar pedido: {e}")
            return False