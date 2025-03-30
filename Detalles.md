# Detalles del Proyecto

Este documento proporciona una descripción detallada de todos los archivos del proyecto, incluyendo las funciones que contiene cada uno con explicaciones extensas sobre su funcionamiento.

## Estructura de Archivos

### Controladores

#### `controllers/__init__.py`
Archivo de inicialización del paquete de controladores. Este archivo permite que Python reconozca el directorio como un paquete y facilita la importación de los controladores desde otros módulos del proyecto. También puede contener importaciones para exponer clases específicas directamente desde el paquete.

#### `controllers/producto_controller.py`
Controlador para la gestión de productos. Este controlador implementa el patrón MVC (Modelo-Vista-Controlador) para separar la lógica de negocio relacionada con los productos de la interfaz de usuario y el acceso a datos.

**Funciones:**
- `__init__()`: Constructor del controlador. Inicializa el controlador de productos y establece cualquier configuración necesaria. No requiere parámetros ya que utiliza la conexión a la base de datos a través de la función `get_db_connection()` cuando es necesario.

- `crear(producto)`: Crea un nuevo producto en la base de datos. Recibe un objeto de tipo Producto con los datos a insertar, valida que los campos obligatorios estén presentes (nombre, precio y stock), prepara la consulta SQL para la inserción, ejecuta la consulta y devuelve el ID del producto recién creado. Maneja posibles errores durante el proceso de inserción.

- `obtener_por_id(producto_id)`: Recupera un producto por su ID. Recibe el ID del producto como parámetro, realiza una consulta a la base de datos para obtener todos los datos del producto con ese ID, y si lo encuentra, crea y devuelve un objeto Producto con esos datos. Si no encuentra ningún producto con ese ID, devuelve None.

- `actualizar(producto)`: Actualiza la información de un producto existente. Recibe un objeto Producto con el ID del producto a actualizar y los nuevos valores para sus atributos. Verifica que el producto exista, prepara y ejecuta la consulta SQL de actualización, y devuelve True si la actualización fue exitosa o False en caso contrario.

- `eliminar(producto_id)`: Elimina un producto de la base de datos. Recibe el ID del producto a eliminar, verifica primero si el producto está siendo utilizado en algún pedido (para mantener la integridad referencial), y si no es así, ejecuta la consulta SQL para eliminar el producto. Devuelve True si la eliminación fue exitosa o False si el producto no existe o está siendo utilizado.

- `buscar(termino)`: Busca productos por nombre o descripción. Recibe un término de búsqueda, construye una consulta SQL que busca coincidencias parciales tanto en el nombre como en la descripción de los productos, ejecuta la consulta y devuelve una lista de objetos Producto que coinciden con el criterio de búsqueda.

#### `controllers/cliente_controller.py`
Controlador para la gestión de clientes. Implementa la lógica de negocio para crear, leer, actualizar y eliminar información de clientes en la base de datos.

**Funciones:**
- `__init__()`: Constructor del controlador. Inicializa el controlador de clientes sin requerir parámetros específicos. Establece el estado inicial del controlador y prepara el acceso a la base de datos a través de la función `get_db_connection()`.

- `crear(cliente)`: Crea un nuevo cliente en la base de datos. Recibe un objeto Cliente con los datos a insertar, valida que los campos obligatorios estén presentes (nombre, email), verifica que el email no esté ya registrado para otro cliente (para evitar duplicados), prepara y ejecuta la consulta SQL para la inserción, y devuelve el ID del cliente recién creado.

- `obtener_por_id(cliente_id)`: Recupera un cliente por su ID. Recibe el ID del cliente como parámetro, consulta la base de datos para obtener todos los datos del cliente con ese ID, y si lo encuentra, crea y devuelve un objeto Cliente con esos datos. Incluye manejo de errores para casos donde el cliente no existe.

- `actualizar(cliente)`: Actualiza la información de un cliente existente. Recibe un objeto Cliente con el ID del cliente a actualizar y los nuevos valores para sus atributos. Verifica que el cliente exista, comprueba que si se está cambiando el email no entre en conflicto con otro cliente, prepara y ejecuta la consulta SQL de actualización, y devuelve True si la actualización fue exitosa.

- `eliminar(cliente_id)`: Elimina un cliente de la base de datos. Recibe el ID del cliente a eliminar, verifica primero si el cliente tiene pedidos asociados (para mantener la integridad referencial), y si no es así, ejecuta la consulta SQL para eliminar el cliente. Implementa transacciones para asegurar que la operación sea atómica.

- `buscar(termino)`: Busca clientes por nombre, email, teléfono o dirección. Recibe un término de búsqueda, construye una consulta SQL que busca coincidencias parciales en varios campos del cliente, ejecuta la consulta y devuelve una lista de objetos Cliente que coinciden con el criterio de búsqueda. Optimiza la búsqueda para mejorar el rendimiento.

#### `controllers/pedido_controller.py`
Controlador para la gestión de pedidos. Maneja la lógica de negocio relacionada con la creación y gestión de pedidos de clientes, incluyendo sus detalles.

**Funciones:**
- `__init__()`: Constructor del controlador. Inicializa el controlador de pedidos y establece cualquier configuración necesaria. Prepara el controlador para manejar las operaciones relacionadas con pedidos y sus detalles asociados.

- `crear(pedido, detalles)`: Crea un nuevo pedido con sus detalles. Recibe un objeto Pedido y una lista de objetos DetallePedido. Implementa una transacción para asegurar que tanto el pedido como todos sus detalles se guarden correctamente o no se guarde nada. Verifica la disponibilidad de stock para cada producto solicitado, actualiza el stock de los productos, calcula el total del pedido basado en los detalles, y devuelve el ID del pedido creado.

- `obtener_por_id(pedido_id)`: Recupera un pedido por su ID. Recibe el ID del pedido, consulta la base de datos para obtener los datos del pedido y todos sus detalles asociados, crea un objeto Pedido con esos datos y una lista de objetos DetallePedido, y los devuelve. Incluye información del cliente y productos relacionados.

- `actualizar_estado(pedido_id, nuevo_estado)`: Actualiza el estado de un pedido. Recibe el ID del pedido y el nuevo estado a asignar, verifica que el pedido exista, prepara y ejecuta la consulta SQL para actualizar el estado, y devuelve True si la actualización fue exitosa. Implementa validación para asegurar que el nuevo estado sea válido.

- `eliminar(pedido_id)`: Elimina un pedido y sus detalles. Recibe el ID del pedido a eliminar, implementa una transacción para eliminar primero todos los detalles del pedido y luego el pedido mismo, asegurando que no queden registros huérfanos. Actualiza el stock de los productos para reflejar la cancelación del pedido.

- `buscar_por_cliente(cliente_id)`: Busca pedidos de un cliente específico. Recibe el ID del cliente, consulta la base de datos para obtener todos los pedidos asociados a ese cliente, y devuelve una lista de objetos Pedido. Opcionalmente puede incluir filtros adicionales como rango de fechas o estado del pedido.

### Modelos

#### `models/__init__.py`
Archivo de inicialización del paquete de modelos. Facilita la importación de las clases de modelo desde otros módulos del proyecto. Define importaciones para exponer directamente las clases principales como Producto, Cliente, Pedido y DetallePedido desde el paquete models.

#### `models/producto.py`
Modelo para representar productos. Define la estructura de datos para los productos en el sistema.

**Funciones:**
- `__init__(id=None, nombre=None, descripcion=None, precio=None, stock=None)`: Constructor del modelo. Inicializa un objeto Producto con los atributos especificados. Todos los parámetros son opcionales para permitir la creación de objetos vacíos que se pueden llenar posteriormente. Realiza validaciones básicas como asegurar que el precio sea un número positivo y el stock sea un entero no negativo.

- `__str__()`: Representación en cadena del producto. Devuelve una cadena con la información principal del producto (ID, nombre, precio y stock) formateada de manera legible. Esta función es útil para depuración y para mostrar información del producto en interfaces de texto.

#### `models/cliente.py`
Modelo para representar clientes. Define la estructura de datos para los clientes en el sistema.

**Funciones:**
- `__init__(id=None, nombre=None, email=None, telefono=None, direccion=None)`: Constructor del modelo. Inicializa un objeto Cliente con los atributos especificados. Todos los parámetros son opcionales. Implementa validaciones básicas como verificar el formato del email y asegurar que el nombre no esté vacío cuando se proporciona.

- `__str__()`: Representación en cadena del cliente. Devuelve una cadena con la información principal del cliente (ID, nombre, email) formateada de manera legible. Facilita la visualización de información del cliente en logs y depuración.

#### `models/pedido.py`
Modelo para representar pedidos. Define la estructura de datos para los pedidos en el sistema.

**Funciones:**
- `__init__(id=None, cliente_id=None, fecha=None, estado=None, total=None)`: Constructor del modelo. Inicializa un objeto Pedido con los atributos especificados. Si no se proporciona una fecha, utiliza la fecha actual. Define estados válidos para el pedido (como "pendiente", "enviado", "entregado", "cancelado") y valida que el estado proporcionado sea válido.

- `__str__()`: Representación en cadena del pedido. Devuelve una cadena con la información principal del pedido (ID, cliente_id, fecha, estado y total) formateada de manera legible. Útil para mostrar información resumida del pedido.

#### `models/detalle_pedido.py`
Modelo para representar detalles de pedidos. Define la estructura de datos para los ítems individuales dentro de un pedido.

**Funciones:**
- `__init__(id=None, pedido_id=None, producto_id=None, cantidad=None, precio_unitario=None)`: Constructor del modelo. Inicializa un objeto DetallePedido con los atributos especificados. Valida que la cantidad sea un entero positivo y el precio unitario sea un número positivo. Calcula automáticamente el subtotal multiplicando la cantidad por el precio unitario.

- `__str__()`: Representación en cadena del detalle de pedido. Devuelve una cadena con la información principal del detalle (producto_id, cantidad, precio_unitario y subtotal) formateada de manera legible. Facilita la visualización de los ítems del pedido.

### Base de Datos

#### `database/__init__.py`
Archivo de inicialización del paquete de base de datos. Expone las funciones principales para el manejo de la base de datos, como `get_db_connection()` e `init_db()`, para que sean fácilmente importables desde otros módulos.

#### `database/db.py`
Funciones para la gestión de la base de datos. Proporciona una capa de abstracción para interactuar con la base de datos SQLite.

**Funciones:**
- `get_db_connection()`: Obtiene una conexión a la base de datos. Crea una conexión a la base de datos SQLite especificada en la configuración, establece la fábrica de filas para que devuelva objetos tipo diccionario (sqlite3.Row), y devuelve la conexión. Implementa manejo de errores para casos donde la base de datos no existe o no se puede acceder.

- `init_db()`: Inicializa la base de datos creando las tablas necesarias. Lee un archivo de esquema SQL que contiene las definiciones de todas las tablas (productos, clientes, pedidos, detalles_pedido) y ejecuta esas definiciones para crear la estructura de la base de datos. Verifica primero si las tablas ya existen para evitar errores.

- `close_db(conn)`: Cierra una conexión a la base de datos. Recibe una conexión abierta y la cierra de manera segura, asegurándose de que todos los cambios pendientes se guarden correctamente. Implementa manejo de errores para casos donde la conexión ya está cerrada.

### Pruebas

#### `tests/test_producto_controller.py`
Pruebas unitarias para el controlador de productos. Verifica que todas las funcionalidades del controlador de productos funcionen correctamente.

**Funciones:**
- `setUp()`: Configura el entorno de prueba antes de cada test. Crea una base de datos en memoria para las pruebas, configura un mock para la función `get_db_connection()` para que devuelva esta base de datos en memoria, crea las tablas necesarias y inicializa el controlador de productos. Esto asegura que cada prueba comience con un estado limpio y conocido.

- `tearDown()`: Limpia el entorno después de cada test. Detiene el patcher que se usó para mockear `get_db_connection()` y cierra la conexión a la base de datos en memoria. Esto libera recursos y asegura que no haya efectos secundarios entre pruebas.

- `test_crear_producto()`: Prueba la creación de productos. Crea un nuevo producto con datos de prueba, verifica que se haya creado correctamente en la base de datos, y comprueba que todos los atributos del producto se hayan guardado correctamente. Utiliza una base de datos en memoria separada para evitar problemas de conexión cerrada.

- `test_obtener_por_id()`: Prueba la obtención de productos por ID. Primero crea un producto en la base de datos, luego intenta recuperarlo por su ID, y verifica que todos los atributos del producto recuperado coincidan con los del producto original. Comprueba tanto casos exitosos como casos donde el producto no existe.

- `test_actualizar()`: Prueba la actualización de productos. Crea un producto en la base de datos, luego crea un objeto Producto con el mismo ID pero con datos actualizados, llama al método actualizar del controlador, y verifica que los cambios se hayan guardado correctamente en la base de datos. Prueba tanto actualizaciones exitosas como fallidas.

- `test_eliminar()`: Prueba la eliminación de productos. Crea un producto en la base de datos, llama al método eliminar del controlador con el ID del producto, y verifica que el producto ya no exista en la base de datos. También prueba casos donde el producto no se puede eliminar porque está siendo utilizado en pedidos.

- `test_buscar()`: Prueba la búsqueda de productos. Crea varios productos con diferentes nombres y descripciones en la base de datos, luego realiza búsquedas con diferentes términos y verifica que los resultados incluyan solo los productos que coinciden con el término de búsqueda. Prueba búsquedas por nombre y por descripción.

#### `tests/test_cliente_controller.py`
Pruebas unitarias para el controlador de clientes. Verifica que todas las funcionalidades del controlador de clientes funcionen correctamente.

**Funciones:**
- `setUp()`: Configura el entorno de prueba antes de cada test. Similar a la configuración para las pruebas del controlador de productos, crea una base de datos en memoria, configura un mock para `get_db_connection()`, crea las tablas necesarias e inicializa el controlador de clientes.

- `tearDown()`: Limpia el entorno después de cada test. Detiene el patcher y cierra la conexión a la base de datos en memoria, asegurando que cada prueba comience con un estado limpio.

- `test_crear_cliente()`: Prueba la creación de clientes. Crea un nuevo cliente con datos de prueba, verifica que se haya creado correctamente en la base de datos, y comprueba que todos los atributos del cliente se hayan guardado correctamente. También prueba casos de error como intentar crear un cliente con un email duplicado.

- `test_obtener_por_id()`: Prueba la obtención de clientes por ID. Crea un cliente en la base de datos, luego lo recupera por su ID y verifica que todos los atributos coincidan. También prueba el caso donde se intenta recuperar un cliente que no existe.

- `test_actualizar()`: Prueba la actualización de clientes. Crea un cliente, luego actualiza sus datos y verifica que los cambios se hayan guardado en la base de datos. Prueba tanto actualizaciones exitosas como casos donde la actualización falla debido a restricciones como emails duplicados.

- `test_eliminar()`: Prueba la eliminación de clientes. Crea un cliente, lo elimina usando el controlador, y verifica que ya no exista en la base de datos. También prueba casos donde el cliente no se puede eliminar porque tiene pedidos asociados.

- `test_buscar()`: Prueba la búsqueda de clientes. Crea varios clientes con diferentes datos, realiza búsquedas con varios términos y verifica que los resultados incluyan solo los clientes que coinciden con el término de búsqueda. Prueba búsquedas por nombre, email, teléfono y dirección.

#### `tests/test_pedido_controller.py`
Pruebas unitarias para el controlador de pedidos. Verifica que todas las funcionalidades del controlador de pedidos funcionen correctamente.

**Funciones:**
- `setUp()`: Configura el entorno de prueba antes de cada test. Crea una base de datos en memoria, configura un mock para `get_db_connection()`, crea todas las tablas necesarias (productos, clientes, pedidos, detalles_pedido) e inicializa el controlador de pedidos. También crea algunos productos y clientes de prueba para usar en las pruebas de pedidos.

- `tearDown()`: Limpia el entorno después de cada test. Detiene el patcher y cierra la conexión a la base de datos en memoria, asegurando que cada prueba comience con un estado limpio.

- `test_crear_pedido()`: Prueba la creación de pedidos. Crea un nuevo pedido con varios detalles, verifica que se haya creado correctamente en la base de datos junto con sus detalles, y comprueba que el stock de los productos se haya actualizado correctamente. También prueba casos de error como intentar crear un pedido con productos que no tienen suficiente stock.

- `test_obtener_por_id()`: Prueba la obtención de pedidos por ID. Crea un pedido con detalles, luego lo recupera por su ID y verifica que tanto el pedido como sus detalles se recuperen correctamente. Comprueba que todos los atributos coincidan con los datos originales.

- `test_actualizar_estado()`: Prueba la actualización del estado de pedidos. Crea un pedido, cambia su estado usando el controlador, y verifica que el cambio se haya guardado en la base de datos. Prueba tanto cambios de estado válidos como inválidos.

- `test_eliminar()`: Prueba la eliminación de pedidos. Crea un pedido con detalles, lo elimina usando el controlador, y verifica que tanto el pedido como sus detalles se hayan eliminado de la base de datos. También comprueba que el stock de los productos se restaure correctamente.

- `test_buscar_por_cliente()`: Prueba la búsqueda de pedidos por cliente. Crea varios pedidos para diferentes clientes, realiza búsquedas por ID de cliente y verifica que los resultados incluyan solo los pedidos del cliente especificado. También prueba filtros adicionales como estado del pedido o rango de fechas.

### Interfaz de Usuario

#### `ui/main_window.py`
Ventana principal de la aplicación. Proporciona la interfaz gráfica principal desde la cual se accede a todas las funcionalidades del sistema.

**Funciones:**
- `__init__()`: Constructor de la ventana principal. Inicializa la ventana principal de la aplicación, configura el título, tamaño y otras propiedades básicas de la ventana. También inicializa los controladores necesarios (ProductoController, ClienteController, PedidoController) para interactuar con la base de datos.

- `setup_ui()`: Configura la interfaz de usuario. Crea y organiza todos los elementos visuales de la interfaz, como menús, botones, tablas y paneles. Define la estructura general de la interfaz y establece las propiedades visuales de cada elemento.

- `connect_signals()`: Conecta las señales de la interfaz con sus manejadores. Asocia eventos de la interfaz (como clics en botones o selecciones en menús) con las funciones que deben ejecutarse cuando ocurren esos eventos. Esto implementa la interactividad de la aplicación.

- `show_productos()`: Muestra la lista de productos. Consulta la base de datos para obtener todos los productos, los muestra en una tabla o lista en la interfaz, y configura las opciones para crear, editar o eliminar productos. Implementa filtros y ordenamiento para facilitar la navegación.

- `show_clientes()`: Muestra la lista de clientes. Similar a `show_productos()`, pero para clientes. Consulta la base de datos para obtener todos los clientes, los muestra en la interfaz, y proporciona opciones para gestionar los clientes.

- `show_pedidos()`: Muestra la lista de pedidos. Consulta la base de datos para obtener todos los pedidos, los muestra en la interfaz con información resumida, y proporciona opciones para ver detalles, cambiar estado o eliminar pedidos. Incluye filtros por cliente, estado y fecha.

#### `ui/producto_dialog.py`
Diálogo para crear y editar productos. Proporciona una interfaz para introducir o modificar los datos de un producto.

**Funciones:**
- `__init__(producto=None)`: Constructor del diálogo. Inicializa el diálogo para crear o editar un producto. Si se proporciona un objeto Producto, el diálogo se configura para editar ese producto, mostrando sus datos actuales. Si no se proporciona ningún producto, el diálogo se configura para crear uno nuevo con campos vacíos.

- `setup_ui()`: Configura la interfaz de usuario del diálogo. Crea y organiza los campos de entrada para cada atributo del producto (nombre, descripción, precio, stock), añade etiquetas descriptivas, y configura los botones de aceptar y cancelar. Implementa validación básica para asegurar que los datos introducidos sean válidos.

- `accept()`: Maneja la aceptación del diálogo. Se ejecuta cuando el usuario hace clic en el botón "Aceptar". Valida todos los datos introducidos, muestra mensajes de error si hay problemas, y si todo es correcto, cierra el diálogo con resultado de aceptación. Implementa validaciones más completas que las de la interfaz.

- `get_producto()`: Obtiene el producto del formulario. Crea un nuevo objeto Producto con los datos introducidos en el formulario, o actualiza el objeto existente si se estaba editando. Realiza conversiones de tipo necesarias (como convertir texto a números para precio y stock).

#### `ui/cliente_dialog.py`
Diálogo para crear y editar clientes. Proporciona una interfaz para introducir o modificar los datos de un cliente.

**Funciones:**
- `__init__(cliente=None)`: Constructor del diálogo. Inicializa el diálogo para crear o editar un cliente. Si se proporciona un objeto Cliente, el diálogo se configura para editar ese cliente, mostrando sus datos actuales. Si no se proporciona ningún cliente, el diálogo se configura para crear uno nuevo.

- `setup_ui()`: Configura la interfaz de usuario del diálogo. Crea y organiza los campos de entrada para cada atributo del cliente (nombre, email, teléfono, dirección), añade etiquetas descriptivas, y configura los botones de aceptar y cancelar. Implementa validación en tiempo real para el formato del email.

- `accept()`: Maneja la aceptación del diálogo. Valida todos los datos introducidos, especialmente el formato del email, muestra mensajes de error si hay problemas, y si todo es correcto, cierra el diálogo con resultado de aceptación.

- `get_cliente()`: Obtiene el cliente del formulario. Crea un nuevo objeto Cliente con los datos introducidos en el formulario, o actualiza el objeto existente si se estaba editando. Aplica formateo y normalización a los datos (como eliminar espacios innecesarios).

#### `ui/pedido_dialog.py`
Diálogo para crear y editar pedidos. Proporciona una interfaz para introducir o modificar los datos de un pedido y sus detalles.

**Funciones:**
- `__init__(pedido=None)`: Constructor del diálogo. Inicializa el diálogo para crear o editar un pedido. Si se proporciona un objeto Pedido, el diálogo se configura para editar ese pedido, mostrando sus datos actuales y sus detalles. Si no se proporciona ningún pedido, el diálogo se configura para crear uno nuevo.

- `setup_ui()`: Configura la interfaz de usuario del diálogo. Crea y organiza los campos para seleccionar el cliente, la fecha y el estado del pedido. También crea una tabla para mostrar y editar los detalles del pedido, y botones para añadir y eliminar detalles.

- `add_detalle()`: Añade un detalle al pedido. Muestra un diálogo secundario para seleccionar un producto, introducir la cantidad y confirmar el precio. Valida que haya suficiente stock disponible y añade el detalle a la tabla de detalles del pedido. Actualiza el total del pedido.

- `remove_detalle()`: Elimina un detalle del pedido. Elimina el detalle seleccionado de la tabla de detalles y actualiza el total del pedido. Confirma con el usuario antes de eliminar para evitar eliminaciones accidentales.

- `accept()`: Maneja la aceptación del diálogo. Valida que el pedido tenga al menos un detalle y que todos los datos sean válidos. Si todo es correcto, cierra el diálogo con resultado de aceptación.

- `get_pedido()`: Obtiene el pedido y sus detalles del formulario. Crea un nuevo objeto Pedido con los datos introducidos y una lista de objetos DetallePedido para cada fila en la tabla de detalles, o actualiza los objetos existentes si se estaba editando.

### Archivo Principal

#### `main.py`
Punto de entrada de la aplicación. Inicia la aplicación y muestra la ventana principal.

**Funciones:**
- `main()`: Función principal que inicia la aplicación. Configura el entorno de la aplicación, inicializa la base de datos si es necesario, crea y muestra la ventana principal, y entra en el bucle principal de eventos de la interfaz gráfica. También configura el manejo de excepciones no capturadas para mejorar la robustez de la aplicación.