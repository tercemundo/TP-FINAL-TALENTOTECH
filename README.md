# TechLab - Sistema de Gestión de Ventas

## Descripción
TechLab es un sistema de gestión de ventas desarrollado en Python que permite administrar clientes, productos y pedidos. La aplicación utiliza SQLite como base de datos para almacenar la información.

## Características

### Gestión de Clientes
- Crear, ver, actualizar y eliminar clientes
- Buscar clientes por nombre, email o teléfono
- Visualizar historial de pedidos por cliente

### Gestión de Productos
- Crear, ver, actualizar y eliminar productos
- Buscar productos por nombre o descripción
- Control de inventario (stock)

### Gestión de Pedidos
- Crear nuevos pedidos seleccionando cliente y productos
- Ver detalles de pedidos
- Cambiar estado de pedidos (Pendiente, En proceso, Enviado, Entregado, Cancelado)
- Eliminar pedidos

## Requisitos
- Python 3.6 o superior
- SQLite3

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/techlab.git
cd techlab
```
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```
3. Ejecuta la aplicación:
```bash
python app.py
