import random
from datetime import date, datetime
import time
from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client
from datetime import datetime, date

try:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ConnectionError("Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env")

    supabase: Client = create_client(url, key)
    print("✅ Conexión a Supabase establecida correctamente\n")

except ConnectionError as e:
    print(f"❌ Error de conexión: {e}")
    exit()
except Exception as e:
    print(f"❌ Error al conectar con Supabase: {e}")
    exit()

def generar_id_personal():
    try:
        datos = supabase.table("personal_caja").select("id_personal").order("id_personal", desc=True).limit(1).execute()

        if len(datos.data) == 0:
            return 1  

        ultimo_id = datos.data[0]["id_personal"]
        return ultimo_id + 1
    except Exception as e:
        print(f"❌ Error al generar ID: {e}")
        return None
def registrar_personal_caja():
    nombre = input("Escribe el nombre: ").strip()

    if not nombre:
        print("\n❌ No puedes insertar un nombre vacío.")
        return
    
    apellidos = input("Escribe el apellido: ").strip()
    if not apellidos:
        print("\n❌ No puedes insertar un apellido vacío.")
        return

    fecha_nacimiento = input("Escribe la fecha de nacimiento (DD/MM/AAAA): ").strip()
    edad, fecha_nacimiento = calcular_edad(fecha_nacimiento)

    if edad is None:
        print("\n❌ Fecha de nacimiento inválida.")
        return None, None, None, None

    
    if edad is None:
        print("\n❌ Fecha de nacimiento inválida. Usa el formato DD/MM/AAAA (ej: 15/05/1990)")
        return
    
    telefono = input("Escribe el teléfono: ").strip()
    if not telefono:
        print("\n❌ No puedes insertar un teléfono vacío.")
        return
    
    dni = input("Escribe el DNI: ").strip()
    if not dni: 
        print("\n❌ No puedes insertar un DNI vacío.")
        return
    
    nuevo_id = generar_id_personal()
    print("\n=== Sucursales Disponibles ===")
    print("1. Villa Mella")
    print("2. Santo Domingo Este")
    print("3. Av. 27 de Febrero")

    sucursal = input("Escoge una sucursal: ").strip()
    print(f"\n✅ Sucursal '{sucursal}' seleccionada.")

    try:
        insertar = supabase.table("personal_caja").insert({
            "id_personal": nuevo_id,
            "nombre": nombre,
            "apellidos": apellidos,
            "fecha_nacimiento": fecha_nacimiento,
            "edad": edad,
            "telefono": telefono,
            "dni": dni,
            "sucursal": sucursal
        }).execute()

        if insertar.data:
            print(f"\n✅ Registro agregado correctamente. Tu ID es el N.{nuevo_id} ")
            return nuevo_id, nombre, apellidos, edad
        else:
            print("\n❌ Ocurrió un error al insertar.")
    except Exception as e:
        print(f"\n❌ Error al insertar dato: {e}")  
def login_personal_caja():
    print("\n=== INICIAR SESIÓN PERSONAL DE CAJA ===")
    id_personal = input("Ingresa tu ID de personal de caja: ").strip()
    
    if not id_personal.isdigit():
        print("❌ ID inválido")
        return None, None, None, None
    
    id_personal = int(id_personal)
    
    try:
        personal = supabase.table("personal_caja").select("*").eq("id_personal", id_personal).execute()
        
        if len(personal.data) == 0:
            print("❌ Personal de caja no encontrado")
            return None, None, None, None
        
        personal_data = personal.data[0]
        print(f"\n✅ Bienvenido de vuelta {personal_data['nombre']} {personal_data['apellidos']}")
        
        return (personal_data['id_personal'], 
                personal_data['nombre'], 
                personal_data['apellidos'], 
                personal_data['edad'])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None, None, None
def menú_personal_caja(id_personal, nombre, apellidos, edad):
    while True:
        print(f"\n=== MENÚ PERSONAL DE CAJA ===")
        print("1. Ver mis datos")
        print("2. Actualizar mis datos")
        print("3. Cerrar sesión")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            mostrar_mis_datos()
        elif opcion == "2":
            actualizar_personal_caja()
        elif opcion == "3":
            print(f"\n✅ Sesión cerrada para {nombre} {apellidos}\n")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")
######clientes
def generar_id():
    try:
        datos = supabase.table("clientes").select("id_cliente").order("id_cliente", desc=True).limit(1).execute()

        if len(datos.data) == 0:
            return 1  

        ultimo_id = datos.data[0]["id_cliente"]
        return ultimo_id + 1
    except Exception as e:
        print(f"❌ Error al generar ID: {e}")
        return None
def calcular_edad(fecha_nacimiento_str):
    try:
        if "/" in fecha_nacimiento_str:
            fecha = datetime.strptime(fecha_nacimiento_str, "%d/%m/%Y")
        else:
            fecha = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d")
    except ValueError:
        return None, None

    hoy = date.today()
    edad = hoy.year - fecha.year

    if (hoy.month, hoy.day) < (fecha.month, fecha.day):
        edad -= 1

    return edad, fecha.strftime("%Y-%m-%d")

def registrar_cliente():
    nombre = input("Escribe el nombre: ").strip()

    if not nombre:
        print("\n❌ No puedes insertar un nombre vacío.")
        return
    
    apellidos = input("Escribe el apellido: ").strip()
    if not apellidos:
        print("\n❌ No puedes insertar un apellido vacío.")
        return

    fecha_nacimiento = input("Escribe la fecha de nacimiento (DD/MM/AAAA): ").strip()
    edad, fecha_nacimiento = calcular_edad(fecha_nacimiento)

    if edad is None:
        print("\n❌ Fecha de nacimiento inválida.")
        return None, None, None, None

    
    if edad is None:
        print("\n❌ Fecha de nacimiento inválida. Usa el formato DD/MM/AAAA (ej: 15/05/1990)")
        return
    
    telefono = input("Escribe el teléfono: ").strip()
    if not telefono:
        print("\n❌ No puedes insertar un teléfono vacío.")
        return
    print("\n=== Sucursales Disponibles ===")
    print("1. Villa Mella")
    print("2. Santo Domingo Este")
    print("3. Av. 27 de Febrero")

    sucursal = input("Escoge una sucursal: ").strip()
    print(f"\n✅ Sucursal '{sucursal}' seleccionada.")

    
    dni = input("Escribe el DNI: ").strip()
    if not dni: 
        print("\n❌ No puedes insertar un DNI vacío.")
        return
    
    nuevo_id = generar_id()

    try:
        insertar = supabase.table("clientes").insert({
            "id_cliente": nuevo_id,
            "nombre": nombre,
            "apellidos": apellidos,
            "fecha_nacimiento": fecha_nacimiento,
            "edad": edad,
            "telefono": telefono,
            "sucursal": sucursal,
            "dni": dni
        }).execute()

        if insertar.data:
            print(f"\n✅ Registro agregado correctamente. Tu ID es el N.{nuevo_id} ")
            return nuevo_id, nombre, apellidos, edad
        else:
            print("\n❌ Ocurrió un error al insertar.")
    except Exception as e:
        print(f"\n❌ Error al insertar dato: {e}")
def login_cliente():
    """Permite a un cliente iniciar sesión"""
    print("\n=== INICIAR SESIÓN ===")
    id_cliente = input("Ingresa tu ID de cliente: ").strip()
    
    if not id_cliente.isdigit():
        print("❌ ID inválido")
        return None, None, None, None
    
    id_cliente = int(id_cliente)
    
    try:
        cliente = supabase.table("clientes").select("*").eq("id_cliente", id_cliente).execute()
        
        if len(cliente.data) == 0:
            print("❌ Cliente no encontrado")
            return None, None, None, None
        
        cliente_data = cliente.data[0]
        print(f"\n✅ Bienvenido de vuelta {cliente_data['nombre']} {cliente_data['apellidos']}")
        
        return (cliente_data['id_cliente'], 
                cliente_data['nombre'], 
                cliente_data['apellidos'], 
                cliente_data['edad'])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None, None, None

def mostrar_mis_datos():
    nuevo_id = input("Escribe tu ID para ver tus datos: ").strip()

    if not nuevo_id.isdigit():
        print("\n❌ El ID debe ser un número.")
        return

    nuevo_id = int(nuevo_id)
    
    try:
        datos = supabase.table("clientes").select("*").eq("id_cliente", nuevo_id).execute()

        if len(datos.data) == 0:
            print("\n❌ No existe un usuario con ese ID.")
            return

        print("\n=== TUS DATOS ===")
        for fila in datos.data:
            print(f"ID: {fila['id_cliente']} | Nombre: {fila['nombre']} | Apellidos: {fila['apellidos']} | Fecha Nac: {fila['fecha_nacimiento']} | Edad: {fila['edad']} | Teléfono: {fila['telefono']} | DNI: {fila['dni']} | Casillero: {fila['id_casillero']}")
    except Exception as e:
        print(f"\n❌ Error al obtener datos: {e}")


def actualizar_personal_caja():
    id_obj = input("Escribe el ID del registro a actualizar: ").strip()

    if not id_obj.isdigit():
        print("\n❌ El ID debe ser un número.")
        return

    id_num = int(id_obj)

    try:
        datos = supabase.table("personal_caja").select("*").eq("id_personal", id_num).execute()
        if len(datos.data) == 0:
            print("\n❌ No existe un registro con ese ID.")
            return

        print("\n=== ¿Qué quieres actualizar? ===")
        print("1. Nombre")
        print("2. Apellidos")
        print("3. Fecha de nacimiento")
        print("4. Teléfono")
        print("5. DNI")
        print("6 Cancelar")

        opcion = input("\nSelecciona una opción: ").strip()

        campos = {
            "1": "nombre",
            "2": "apellidos",
            "3": "fecha_nacimiento",
            "4": "telefono",
            "5": "dni"
        }

        if opcion not in campos and opcion != "7":
            print("\n❌ Opción no válida.")
            return
        if opcion == "7":
            print("\n✅ Operación cancelada.")
            return

        campo = campos[opcion]
        nuevo_valor = input(f"Escribe el nuevo valor para '{campo}': ").strip()

        if not nuevo_valor:
            print("\n❌ El valor no puede estar vacío.")
            return

        # Si actualizamos fecha de nacimiento, recalcular edad
        if campo == "fecha_nacimiento":
            edad = calcular_edad(nuevo_valor)
            if edad is None:
                print("\n❌ Fecha inválida. Usa el formato YYYY-MM-DD")
                return

            actualizar = supabase.table("personal_caja").update({
                "fecha_nacimiento": nuevo_valor,
                "edad": edad
            }).eq("id_personal", id_num).execute()
        else:
            actualizar = supabase.table("personal_caja").update(
                {campo: nuevo_valor}
            ).eq("id_personal", id_num).execute()

        if actualizar.data:
            print(f"\n✅ El campo '{campo}' fue actualizado correctamente.")
        else:
            print("\n❌ Error al actualizar.")
    except Exception as e:
        print(f"\n❌ Error al actualizar dato: {e}")

def ver_paquetes_id():
    """Muestra los paquetes asociados al cliente"""
    print("\n" + "="*50)
    print("        MIS PAQUETES")
    print("="*50)

    id_cliente = input("Escribe tu ID de cliente: ").strip()

    try:
        response = supabase.table("paquetes").select("*").eq("id_cliente", id_cliente).execute()
        paquetes = response.data

        if not paquetes:
            print("\n❌ No tienes paquetes registrados.")
            print("="*50)
            return

        print(f"\n✅ Tienes {len(paquetes)} paquete(s) registrado(s):")
        for paquete in paquetes:
            print("-"*50)
            print(f"ID Paquete:   {paquete['id_paquete']}")
            print(f"Descripción:  {paquete['descripcion']}")
            print(f"Peso:         {paquete['peso']} lbs")
            print(f"Estado:       {paquete['estado']}")
        print("="*50)

    except Exception as e:
        print(f"❌ Error al obtener los paquetes: {e}")
        print("="*50)
def ver_paquetes():
    """Muestra todos los paquetes en la tabla"""
    print("\n" + "="*50)
    print("        TODOS LOS PAQUETES")
    print("="*50)

    try:
        response = supabase.table("paquetes").select("*").execute()
        paquetes = response.data

        if not paquetes:
            print("\n❌ No hay paquetes registrados.")
            print("="*50)
            return

        print(f"\n✅ Hay {len(paquetes)} paquete(s) registrado(s):")
        for paquete in paquetes:
            print("-"*50)
            print(f"ID Paquete:   {paquete['id_paquete']}")
            print(f"Descripción:  {paquete['descripcion']}")
            print(f"Peso:         {paquete['peso']} lbs")
            print(f"Estado:       {paquete['estado']}")
            print(f"ID Cliente:   {paquete['id_cliente']}")
        print("="*50)

    except Exception as e:
        print(f"❌ Error al obtener los paquetes: {e}")
        print("="*50)

def mostrar_paquetes():
    while True:
        print("\n==============================")
        print("        MENÚ PAQUETES       ")
        print("==============================")
        print("1. Ver paquete por ID")
        print("2. Ver todos los Paquetes")
        print("3. Salir")
        

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            ver_paquetes_id()
        elif opcion == "2":
            ver_paquetes()
        elif opcion == "3":
            print("\n👋 Saliendo del programa...")
            break
        else:
            print("\n❌ Opción no válida.")
    nuevo_id = input("Escribe tu ID para ver tus datos: ")

    if not nuevo_id.isdigit():
        print("\n❌ El ID debe ser un número.")
        return

    nuevo_id = int(nuevo_id)
    datos = supabase.table("clientes").select("*").eq("id", nuevo_id).execute()

    if len(datos.data) == 0:
        print("\n❌ No existe un usuario con ese ID.")
        return

    print("\n=== DATOS ===")
    for fila in datos.data:
        print(f"ID: {fila['id']} | Nombre: {fila['nombre']} | Apellidos: {fila['apellidos']} | Edad: {fila['edad']} | Teléfono: {fila['telefono']} | DNI: {fila['dni']}")
    print("="*50)
    
    id_cliente = input("Escribe tu ID de cliente: ").strip()
    
    try:
        response = supabase.table("paquetes").select("*").eq("id_cliente", id_cliente).execute()
        paquetes = response.data
        
        if not paquetes:
            print("\n❌ No tienes paquetes registrados.")
            print("="*50)
            return
        
        print(f"\n✅ Tienes {len(paquetes)} paquete(s) registrado(s):")
        for paquete in paquetes:
            print("-"*50)
            print(f"ID Paquete:   {paquete['id_paquete']}")
            print(f"Descripción:  {paquete['descripcion']}")
            print(f"Peso:         {paquete['peso']} lbs")
            print(f"Estado:       {paquete['estado']}")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error al obtener los paquetes: {e}")
        print("="*50)

def menu_personal_caja(id_personal, nombre, apellidos, edad):
    while True:
        print(f"\n=== MENÚ PERSONAL DE CAJA ===")
        print("1. Ver mis datos")
        print("2. Actualizar mis datos")
        print("3. Ver paquetes de clientes")
        print("4. Cerrar sesión")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            mostrar_mis_datos()
        elif opcion == "2":
            actualizar_personal_caja()
        elif opcion == "3":
            mostrar_paquetes()
        elif opcion == "4":
            print(f"\n✅ Sesión cerrada para {nombre} {apellidos}\n")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")