import os
import sys
import datetime
from database import init_db
from controllers import ClienteController, ProductoController, PedidoController
from models import Cliente, Producto, Pedido, DetallePedido

class App:
    def __init__(self):
        # Inicializar la base de datos
        if not os.path.exists('techlab.db'):
            print("Inicializando base de datos...")
            init_db()
        
        self.cliente_controller = ClienteController()
        self.producto_controller = ProductoController()
        self.pedido_controller = PedidoController()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== SISTEMA DE GESTIÓN TECHLAB =====\n")
        print("1. Gestión de Clientes")
        print("2. Gestión de Productos")
        print("3. Gestión de Pedidos")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            self.menu_clientes()
        elif opcion == "2":
            self.menu_productos()
        elif opcion == "3":
            self.menu_pedidos()
        elif opcion == "0":
            print("\n¡Gracias por usar el Sistema de Gestión TechLab!")
            sys.exit(0)
        else:
            input("\nOpción no válida. Presione Enter para continuar...")
            self.mostrar_menu_principal()
    
    # ===== MENÚ DE CLIENTES =====
    def menu_clientes(self):
        """Muestra el menú de gestión de clientes."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n===== GESTIÓN DE CLIENTES =====\n")
            print("1. Ver todos los clientes")
            print("2. Buscar cliente")
            print("3. Agregar nuevo cliente")
            print("4. Editar cliente")
            print("5. Eliminar cliente")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.listar_clientes()
            elif opcion == "2":
                self.buscar_cliente()
            elif opcion == "3":
                self.agregar_cliente()
            elif opcion == "4":
                self.editar_cliente()
            elif opcion == "5":
                self.eliminar_cliente()
            elif opcion == "0":
                break
            else:
                input("\nOpción no válida. Presione Enter para continuar...")
    
    def listar_clientes(self):
        """Muestra todos los clientes."""
        clientes = self.cliente_controller.listar_todos()
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== LISTA DE CLIENTES =====\n")
        
        if not clientes:
            print("No hay clientes registrados.")
        else:
            print(f"{'ID':<5} {'Nombre':<30} {'Email':<30} {'Teléfono':<15}")
            print("-" * 80)
            for cliente in clientes:
                print(f"{cliente.id:<5} {cliente.nombre:<30} {cliente.email:<30} {cliente.telefono:<15}")
        
        input("\nPresione Enter para continuar...")
    
    def buscar_cliente(self):
        """Busca clientes por nombre, email o teléfono."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== BUSCAR CLIENTE =====\n")
        
        termino = input("Ingrese nombre, email o teléfono a buscar: ")
        if not termino:
            return
        
        clientes = self.cliente_controller.buscar(termino)
        
        print("\nResultados de la búsqueda:\n")
        if not clientes:
            print("No se encontraron clientes con ese criterio.")
        else:
            print(f"{'ID':<5} {'Nombre':<30} {'Email':<30} {'Teléfono':<15}")
            print("-" * 80)
            for cliente in clientes:
                print(f"{cliente.id:<5} {cliente.nombre:<30} {cliente.email:<30} {cliente.telefono:<15}")
        
        input("\nPresione Enter para continuar...")
    
    def agregar_cliente(self):
        """Agrega un nuevo cliente."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== AGREGAR NUEVO CLIENTE =====\n")
        
        nombre = input("Nombre: ")
        if not nombre:
            print("El nombre es obligatorio.")
            input("\nPresione Enter para continuar...")
            return
        
        email = input("Email: ")
        if not email:
            print("El email es obligatorio.")
            input("\nPresione Enter para continuar...")
            return
        
        # Verificar si el email ya existe
        if self.cliente_controller.obtener_por_email(email):
            print("\nYa existe un cliente con ese email.")
            input("\nPresione Enter para continuar...")
            return
        
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        
        cliente = Cliente(nombre=nombre, email=email, telefono=telefono, direccion=direccion)
        if self.cliente_controller.crear(cliente):
            print("\nCliente agregado correctamente.")
        else:
            print("\nError al agregar el cliente.")
        
        input("\nPresione Enter para continuar...")
    
    def editar_cliente(self):
        """Edita un cliente existente."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== EDITAR CLIENTE =====\n")
        
        id_cliente = input("Ingrese el ID del cliente a editar (0 para cancelar): ")
        if not id_cliente or id_cliente == "0":
            return
        
        try:
            id_cliente = int(id_cliente)
        except ValueError:
            print("\nID inválido.")
            input("\nPresione Enter para continuar...")
            return
        
        cliente = self.cliente_controller.obtener_por_id(id_cliente)
        if not cliente:
            print("\nCliente no encontrado.")
            input("\nPresione Enter para continuar...")
            return
        
        print(f"\nEditando cliente: {cliente.nombre} ({cliente.email})\n")
        
        nombre = input(f"Nombre [{cliente.nombre}]: ")
        if nombre:
            cliente.nombre = nombre
        
        email_original = cliente.email
        email = input(f"Email [{cliente.email}]: ")
        if email:
            cliente.email = email
        
        telefono = input(f"Teléfono [{cliente.telefono}]: ")
        if telefono:
            cliente.telefono = telefono
        
        direccion = input(f"Dirección [{cliente.direccion}]: ")
        if direccion:
            cliente.direccion = direccion
        
        # Verificar si el nuevo email ya existe (si se cambió)
        if cliente.email != email_original and self.cliente_controller.obtener_por_email(cliente.email):
            print("\nYa existe un cliente con ese email.")
            input("\nPresione Enter para continuar...")
            return
        
        if self.cliente_controller.actualizar(cliente):
            print("\nCliente actualizado correctamente.")
        else:
            print("\nError al actualizar el cliente.")
        
        input("\nPresione Enter para continuar...")
    
    def eliminar_cliente(self):
        """Elimina un cliente existente."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== ELIMINAR CLIENTE =====\n")
        
        id_cliente = input("Ingrese el ID del cliente a eliminar (0 para cancelar): ")
        if not id_cliente or id_cliente == "0":
            return
        
        try:
            id_cliente = int(id_cliente)
        except ValueError:
            print("\nID inválido.")
            input("\nPresione Enter para continuar...")
            return
        
        cliente = self.cliente_controller.obtener_por_id(id_cliente)
        if not cliente:
            print("\nCliente no encontrado.")
            input("\nPresione Enter para continuar...")
            return
        
        confirmacion = input(f"\n¿Está seguro de eliminar al cliente {cliente.nombre}? (s/n): ")
        if confirmacion.lower() != "s":
            print("\nOperación cancelada.")
            input("\nPresione Enter para continuar...")
            return
        
        if self.cliente_controller.eliminar(cliente.id):
            print("\nCliente eliminado correctamente.")
        else:
            print("\nNo se puede eliminar el cliente porque tiene pedidos asociados.")
        
        input("\nPresione Enter para continuar...")
    
    # ===== MENÚ DE PRODUCTOS =====
    def menu_productos(self):
        """Muestra el menú de gestión de productos."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n===== GESTIÓN DE PRODUCTOS =====\n")
            print("1. Ver todos los productos")
            print("2. Buscar producto")
            print("3. Agregar nuevo producto")
            print("4. Editar producto")
            print("5. Eliminar producto")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.listar_productos()
            elif opcion == "2":
                self.buscar_producto()
            elif opcion == "3":
                self.agregar_producto()
            elif opcion == "4":
                self.editar_producto()
            elif opcion == "5":
                self.eliminar_producto()
            elif opcion == "0":
                break
            else:
                input("\nOpción no válida. Presione Enter para continuar...")
    
    def listar_productos(self):
        """Muestra todos los productos."""
        productos = self.producto_controller.listar_todos()
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== LISTA DE PRODUCTOS =====\n")
        
        if not productos:
            print("No hay productos registrados.")
        else:
            print(f"{'ID':<5} {'Nombre':<30} {'Precio':<10} {'Stock':<10}")
            print("-" * 60)
            for producto in productos:
                print(f"{producto.id:<5} {producto.nombre:<30} ${producto.precio:<9.2f} {producto.stock:<10}")
        
        input("\nPresione Enter para continuar...")
    
    def buscar_producto(self):
        """Busca productos por nombre o descripción."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== BUSCAR PRODUCTO =====\n")
        
        termino = input("Ingrese nombre o descripción a buscar: ")
        if not termino:
            return
        
        productos = self.producto_controller.buscar(termino)
        
        print("\nResultados de la búsqueda:\n")
        if not productos:
            print("No se encontraron productos con ese criterio.")
        else:
            print(f"{'ID':<5} {'Nombre':<30} {'Precio':<10} {'Stock':<10}")
            print("-" * 60)
            for producto in productos:
                print(f"{producto.id:<5} {producto.nombre:<30} ${producto.precio:<9.2f} {producto.stock:<10}")
        
        input("\nPresione Enter para continuar...")
    
    def agregar_producto(self):
        """Agrega un nuevo producto."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== AGREGAR NUEVO PRODUCTO =====\n")
        
        nombre = input("Nombre: ")
        if not nombre:
            print("El nombre es obligatorio.")
            input("\nPresione Enter para continuar...")
            return
        
        descripcion = input("Descripción: ")
        
        try:
            precio = float(input("Precio: "))
            if precio < 0:
                raise ValueError
        except ValueError:
            print("\nPrecio inválido.")
            input("\nPresione Enter para continuar...")
            return
        
        try:
            stock = int(input("Stock inicial: "))
            if stock < 0:
                raise ValueError
        except ValueError:
            print("\nStock inválido.")
            input("\nPresione Enter para continuar...")
            return
        
        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
        if self.producto_controller.crear(producto):
            print("\nProducto agregado correctamente.")
        else:
            print("\nError al agregar el producto.")
        
        input("\nPresione Enter para continuar...")
    
    def editar_producto(self):
        """Edita un producto existente."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== EDITAR PRODUCTO =====\n")
        
        id_producto = input("Ingrese el ID del producto a editar (0 para cancelar): ")
        if not id_producto or id_producto == "0":
            return
        
        try:
            id_producto = int(id_producto)
        except ValueError:
            print("\nID inválido.")
            input("\nPresione Enter para continuar...")
            return
        
        producto = self.producto_controller.obtener_por_id(id_producto)
        if not producto:
            print("\nProducto no encontrado.")
            input("\nPresione Enter para continuar...")
            return
        
        print(f"\nEditando producto: {producto.nombre} (${producto.precio})\n")
        
        nombre = input(f"Nombre [{producto.nombre}]: ")
        if nombre:
            producto.nombre = nombre
        
        descripcion = input(f"Descripción [{producto.descripcion}]: ")
        if descripcion:
            producto.descripcion = descripcion
        
        precio_str = input(f"Precio [${producto.precio}]: ")
        if precio_str:
            try:
                precio = float(precio_str)
                if precio < 0:
                    raise ValueError
                producto.precio = precio
            except ValueError:
                print("\nPrecio inválido. Se mantendrá el valor anterior.")
        
        stock_str = input(f"Stock [{producto.stock}]: ")
        if stock_str:
            try:
                stock = int(stock_str)
                if stock < 0:
                    raise ValueError
                producto.stock = stock
            except ValueError:
                print("\nStock inválido. Se mantendrá el valor anterior.")
        
        if self.producto_controller.actualizar(producto):
            print("\nProducto actualizado correctamente.")
        else:
            print("\nError al actualizar el producto.")
        
        input("\nPresione Enter para continuar...")
    
    def eliminar_producto(self):
        """Elimina un producto existente."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== ELIMINAR PRODUCTO =====\n")
        
        id_producto = input("Ingrese el ID del producto a eliminar (0 para cancelar): ")
        if not id_producto or id_producto == "0":
            return
        
        try:
            id_producto = int(id_producto)
        except ValueError:
            print("\nID inválido.")
            input("\nPresione Enter para continuar...")
            return
        
        producto = self.producto_controller.obtener_por_id(id_producto)
        if not producto:
            print("\nProducto no encontrado.")
            input("\nPresione Enter para continuar...")
            return
        
        confirmacion = input(f"\n¿Está seguro de eliminar el producto {producto.nombre}? (s/n): ")
        if confirmacion.lower() != "s":
            print("\nOperación cancelada.")
            input("\nPresione Enter para continuar...")
            return
        
        if self.producto_controller.eliminar(producto.id):
            print("\nProducto eliminado correctamente.")
        else:
            print("\nNo se puede eliminar el producto porque está asociado a pedidos.")
        
        input("\nPresione Enter para continuar...")
    
    # ===== MENÚ DE PEDIDOS =====
    def menu_pedidos(self):
        """Muestra el menú de gestión de pedidos."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n===== GESTIÓN DE PEDIDOS =====\n")
            print("1. Ver todos los pedidos")
            print("2. Ver pedidos por cliente")
            print("3. Ver detalle de pedido")
            print("4. Crear nuevo pedido")
            print("5. Cambiar estado de pedido")
            print("6. Eliminar pedido")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.listar_pedidos()
            elif opcion == "2":
                self.listar_pedidos_por_cliente()
            elif opcion == "3":
                self.ver_detalle_pedido()
            elif opcion == "4":
                self.crear_pedido()
            elif opcion == "5":
                self.cambiar_estado_pedido()
            elif opcion == "6":
                self.eliminar_pedido()
            elif opcion == "0":
                break
            else:
                input("\nOpción no válida. Presione Enter para continuar...")
    
    def listar_pedidos(self):
        """Muestra todos los pedidos."""
        pedidos = self.pedido_controller.listar_todos()
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== LISTA DE PEDIDOS =====\n")
        
        if not pedidos:
            print("No hay pedidos registrados.")
        else:
            print(f"{'ID':<5} {'Cliente':<30} {'Fecha':<15} {'Estado':<15} {'Total':<10}")
            print("-" * 80)
            for pedido in pedidos:
                print(f"{pedido.id:<5} {pedido.cliente.nombre:<30} {pedido.fecha:<15} {pedido.estado:<15} ${pedido.total:<9.2f}")
        
        input("\nPresione Enter para continuar...")
    
    def listar_pedidos_por_cliente(self):
        """Muestra los pedidos de un cliente específico."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== PEDIDOS POR CLIENTE =====\n")
        
        # Buscar cliente
        termino = input("Ingrese nombre, email o teléfono del cliente: ")
        if not termino:
            return
        
        clientes = self.cliente_controller.buscar(termino)
        
        if not clientes:
            print("\nNo se encontraron clientes con ese criterio.")
            input("\nPresione Enter para continuar...")
            return
        
        # Si hay más de un cliente, mostrar lista para seleccionar
        if len(clientes) > 1:
            print("\nSe encontraron varios clientes. Seleccione uno:\n")
            print(f"{'#':<3} {'Nombre':<30} {'Email':<30}")
            print("-" * 65)
            
            for i, cliente in enumerate(clientes):
                print(f"{i+1:<3} {cliente.nombre:<30} {cliente.email:<30}")
            
            seleccion = input("\nSeleccione un cliente (número) o 0 para cancelar: ")
            if not seleccion or seleccion == "0":
                return
            
            try:
                indice = int(seleccion) - 1
                if indice < 0 or indice >= len(clientes):
                    raise ValueError
                cliente = clientes[indice]
            except ValueError:
                print("\nSelección inválida.")
                input("\nPresione Enter para continuar...")
                return
        else:
            cliente = clientes[0]
        
        # Mostrar pedidos del cliente
        pedidos = self.pedido_controller.listar_por_cliente(cliente.id)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n===== PEDIDOS DEL CLIENTE: {cliente.nombre} =====\n")
        
        if not pedidos:
            print("Este cliente no tiene pedidos registrados.")
        else:
            print(f"{'ID':<5} {'Fecha':<15} {'Estado':<15} {'Total':<10}")
            print("-" * 50)
            for pedido in pedidos:
                print(f"{pedido.id:<5} {pedido.fecha:<15} {pedido.estado:<15} ${pedido.total:<9.2f}")
        
        input("\nPresione Enter para continuar...")
    
    def ver_detalle_pedido(self):
        """Muestra el detalle de un pedido específico."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== DETALLE DE PEDIDO =====\n")
        
        id_pedido = input("Ingrese el ID del pedido a consultar (0 para cancelar): ")
        if not id_pedido or id_pedido == "0":
            return
        
        try:
            id_pedido = int(id_pedido)
        except ValueError:
            print("\nID inválido.")
            input("\nPresione Enter para continuar...")
            return
        
        pedido = self.pedido_controller.obtener_por_id(id_pedido)
        if not pedido:
            print("\nPedido no encontrado.")
            input("\nPresione Enter para continuar...")
            return
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n===== DETALLE DEL PEDIDO #{pedido.id} =====\n")
        
        print(f"Cliente: {pedido.cliente.nombre}")
        print(f"Fecha: {pedido.fecha}")
        print(f"Estado: {pedido.estado}")
        print("\nProductos:")
        print(f"{'Cantidad':<10} {'Producto':<30} {'Precio Unit.':<15} {'Subtotal':<15}")
        print("-" * 70)
        
        for detalle in pedido.detalles:
            subtotal = detalle.cantidad * detalle.precio_unitario
            print(f"{detalle.cantidad:<10} {detalle.producto.nombre:<30} ${detalle.precio_unitario:<14.2f} ${subtotal:<14.2f}")
        
        print("-" * 70)
        print(f"{'TOTAL:':<56} ${pedido.total:<14.2f}")
        
        input("\nPresione Enter para continuar...")
    
    def crear_pedido(self):
        """Crea un nuevo pedido."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== CREAR NUEVO PEDIDO =====\n")
        
        # Paso 1: Seleccionar cliente
        print("Paso 1: Seleccionar cliente\n")
        
        termino = input("Ingrese nombre, email o teléfono del cliente: ")
        if not termino:
            return
        
        clientes = self.cliente_controller.buscar(termino)
        
        if not clientes:
            print("\nNo se encontraron clientes con ese criterio.")
            input("\nPresione Enter para continuar...")
            return
        
        # Si hay más de un cliente, mostrar lista para seleccionar
        if len(clientes) > 1:
            print("\nSe encontraron varios clientes. Seleccione uno:\n")
            print(f"{'#':<3} {'Nombre':<30} {'Email':<30}")
            print("-" * 65)
            
            for i, cliente in enumerate(clientes):
                print(f"{i+1:<3} {cliente.nombre:<30} {cliente.email:<30}")
            
            seleccion = input("\nSeleccione un cliente (número) o 0 para cancelar: ")
            if not seleccion or seleccion == "0":
                return
            
            try:
                indice = int(seleccion) - 1
                if indice < 0 or indice >= len(clientes):
                    raise ValueError
                cliente = clientes[indice]
            except ValueError:
                print("\nSelección inválida.")
                input("\nPresione Enter para continuar...")
                return
        else:
            cliente = clientes[0]
        
        # Paso 2: Agregar productos al pedido
        detalles = []
        total_pedido = 0.0
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n===== CREAR NUEVO PEDIDO =====\n")
            print(f"Cliente: {cliente.nombre}")
            
            if detalles:
                print("\nProductos agregados:")
                print(f"{'#':<3} {'Cantidad':<10} {'Producto':<30} {'Precio Unit.':<15} {'Subtotal':<15}")
                print("-" * 75)
                
                for i, detalle in enumerate(detalles):
                    subtotal = detalle.cantidad * detalle.precio_unitario
                    print(f"{i+1:<3} {detalle.cantidad:<10} {detalle.producto.nombre:<30} ${detalle.precio_unitario:<14.2f} ${subtotal:<14.2f}")
                
                print("-" * 75)
                print(f"{'TOTAL:':<59} ${total_pedido:<14.2f}")
            
            print("\nPaso 2: Agregar productos al pedido\n")
            print("1. Agregar producto")
            print("2. Eliminar producto")
            print("3. Finalizar pedido")
            print("0. Cancelar pedido")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._agregar_producto_a_pedido(detalles, total_pedido)
                # Recalcular el total
                total_pedido = sum(detalle.cantidad * detalle.precio_unitario for detalle in detalles)
            elif opcion == "2":
                if not detalles:
                    print("\nNo hay productos para eliminar.")
                    input("\nPresione Enter para continuar...")
                    continue
                
                # Mostrar productos en el pedido para eliminar
                print("\nSeleccione el producto a eliminar:\n")
                print(f"{'#':<3} {'Cantidad':<10} {'Producto':<30}")
                print("-" * 45)
                
                for i, detalle in enumerate(detalles):
                    print(f"{i+1:<3} {detalle.cantidad:<10} {detalle.producto.nombre:<30}")
                
                seleccion = input("\nSeleccione un producto (número) o 0 para cancelar: ")
                if not seleccion or seleccion == "0":
                    continue
                
                try:
                    indice = int(seleccion) - 1
                    if indice < 0 or indice >= len(detalles):
                        raise ValueError
                    detalles.pop(indice)
                    # Recalcular el total
                    total_pedido = sum(detalle.cantidad * detalle.precio_unitario for detalle in detalles)
                    print("\nProducto eliminado del pedido.")
                except ValueError:
                    print("\nSelección inválida.")
                input("\nPresione Enter para continuar...")
            elif opcion == "3":
                if not detalles:
                    print("\nNo se puede finalizar un pedido sin productos.")
                    input("\nPresione Enter para continuar...")
                    continue
                
                # Crear el pedido
                fecha = datetime.datetime.now().strftime("%Y-%m-%d")
                pedido = Pedido(
                    cliente_id=cliente.id,  # Cambiado de cliente=cliente a cliente_id=cliente.id
                    fecha=fecha,
                    estado="Pendiente",
                    total=total_pedido
                )
                
                # Mantener los detalles como objetos DetallePedido
                # pero asegurarnos de que tienen el atributo producto_id
                for detalle in detalles:
                    detalle.producto_id = detalle.producto.id
                
                if self.pedido_controller.crear(pedido, detalles):
                    print("\nPedido creado correctamente.")
                    input("\nPresione Enter para continuar...")
                    return
                else:
                    print("\nError al crear el pedido.")
                    input("\nPresione Enter para continuar...")
            elif opcion == "0":
                confirmacion = input("\n¿Está seguro de cancelar el pedido? (s/n): ")
                if confirmacion.lower() == "s":
                    print("\nPedido cancelado.")
                    input("\nPresione Enter para continuar...")
                    return
            else:
                input("\nOpción no válida. Presione Enter para continuar...")
    
    def _agregar_producto_a_pedido(self, detalles, total_pedido):
        """Agrega un producto al pedido actual."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== AGREGAR PRODUCTO AL PEDIDO =====\n")
        
        # Buscar producto
        termino = input("Ingrese nombre o descripción del producto: ")
        if not termino:
            return
        
        productos = self.producto_controller.buscar(termino)
        
        if not productos:
            print("\nNo se encontraron productos con ese criterio.")
            input("\nPresione Enter para continuar...")
            return
        
        # Si hay más de un producto, mostrar lista para seleccionar
        if len(productos) > 1:
            print("\nSe encontraron varios productos. Seleccione uno:\n")
            print(f"{'#':<3} {'Nombre':<30} {'Precio':<10} {'Stock':<10}")
            print("-" * 55)
            
            for i, producto in enumerate(productos):
                print(f"{i+1:<3} {producto.nombre:<30} ${producto.precio:<9.2f} {producto.stock:<10}")
            
            seleccion = input("\nSeleccione un producto (número) o 0 para cancelar: ")
            if not seleccion or seleccion == "0":
                return
            
            try:
                indice = int(seleccion) - 1
                if indice < 0 or indice >= len(productos):
                    raise ValueError
                producto = productos[indice]
            except ValueError:
                print("\nSelección inválida.")
                input("\nPresione Enter para continuar...")
                return
        else:
            producto = productos[0]
        
        # Verificar stock
        if producto.stock <= 0:
            print("\nEste producto no tiene stock disponible.")
            input("\nPresione Enter para continuar...")
            return
        
        # Solicitar cantidad
        try:
            cantidad = int(input(f"\nCantidad (stock disponible: {producto.stock}): "))
            if cantidad <= 0:
                raise ValueError
            if cantidad > producto.stock:
                print("\nLa cantidad solicitada excede el stock disponible.")
                input("\nPresione Enter para continuar...")
                return
        except ValueError:
            print("\nCantidad inválida.")
            input("\nPresione Enter para continuar...")
            return
        
        # Verificar si el producto ya está en el pedido
        for detalle in detalles:
            if detalle.producto.id == producto.id:
                # Actualizar cantidad si ya existe
                nueva_cantidad = detalle.cantidad + cantidad
                if nueva_cantidad > producto.stock:
                    print("\nLa cantidad total excede el stock disponible.")
                    input("\nPresione Enter para continuar...")
                    return
                detalle.cantidad = nueva_cantidad
                print(f"\nSe actualizó la cantidad del producto {producto.nombre}.")
                input("\nPresione Enter para continuar...")
                return
        
        # Agregar nuevo detalle
        detalle = DetallePedido(
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )
        detalles.append(detalle)
        
        print(f"\nProducto {producto.nombre} agregado al pedido.")
        input("\nPresione Enter para continuar...")
    
    def cambiar_estado_pedido(self):
        """Cambia el estado de un pedido."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== CAMBIAR ESTADO DE PEDIDO =====\n")
        
        id_pedido = input("Ingrese el ID del pedido (0 para cancelar): ")
        if not id_pedido or id_pedido == "0":
            return
        
        try:
            id_pedido = int(id_pedido)
        except ValueError:
            print("\nID inválido.")
            input("\nPresione Enter para continuar...")
            return
        
        pedido = self.pedido_controller.obtener_por_id(id_pedido)
        if not pedido:
            print("\nPedido no encontrado.")
            input("\nPresione Enter para continuar...")
            return
        
        print(f"\nPedido #{pedido.id} - Cliente: {pedido.cliente.nombre}")
        print(f"Estado actual: {pedido.estado}")
        print("\nEstados disponibles:")
        print("1. Pendiente")
        print("2. En proceso")
        print("3. Enviado")
        print("4. Entregado")
        print("5. Cancelado")
        
        opcion = input("\nSeleccione el nuevo estado (número) o 0 para cancelar: ")
        if not opcion or opcion == "0":
            return
        
        estados = {
            "1": "Pendiente",
            "2": "En proceso",
            "3": "Enviado",
            "4": "Entregado",
            "5": "Cancelado"
        }
        
        if opcion not in estados:
            print("\nOpción inválida.")
            input("\nPresione Enter para continuar...")
            return
        
        nuevo_estado = estados[opcion]
        pedido.estado = nuevo_estado
        
        if self.pedido_controller.actualizar(pedido):
            print(f"\nEstado del pedido actualizado a: {nuevo_estado}")
        else:
            print("\nError al actualizar el estado del pedido.")
        
        input("\nPresione Enter para continuar...")

    def eliminar_pedido(self):
        """Elimina un pedido existente."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== ELIMINAR PEDIDO =====\n")
        
        id_pedido = input("Ingrese el ID del pedido a eliminar (0 para cancelar): ")
        if not id_pedido or id_pedido == "0":
            return
        
        try:
            id_pedido = int(id_pedido)
        except ValueError:
            print("\nID inválido.")
            input("\nPresione Enter para continuar...")
            return
        
        pedido = self.pedido_controller.obtener_por_id(id_pedido)
        if not pedido:
            print("\nPedido no encontrado.")
            input("\nPresione Enter para continuar...")
            return
        
        confirmacion = input(f"\n¿Está seguro de eliminar el pedido #{pedido.id} del cliente {pedido.cliente.nombre}? (s/n): ")
        if confirmacion.lower() != "s":
            print("\nOperación cancelada.")
            input("\nPresione Enter para continuar...")
            return
        
        if self.pedido_controller.eliminar(pedido.id):
            print("\nPedido eliminado correctamente.")
        else:
            print("\nError al eliminar el pedido.")
        
        input("\nPresione Enter para continuar...")

# Agregar este código al final del archivo (fuera de la clase)
if __name__ == "__main__":
    app = App()
    while True:
        try:
            app.mostrar_menu_principal()
        except KeyboardInterrupt:
            print("\n\nPrograma terminado por el usuario.")
            break
        except Exception as e:
            print(f"\nError inesperado: {e}")
            input("\nPresione Enter para continuar...")