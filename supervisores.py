print('Apartado de supervisores de PDSS')
import random
from time import sleep
from datetime import date, datetime, time
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

print("Bienvenido/a al sistema de Supervisores de PDSS")
print('Package Delivery Service Sistem')
print('Desarrollado por: Eligabriel Espinal')
sleep(2)
def generar_id_supervisor():
    try:
        datos = supabase.table("supervisores").select("id_supervisor").order("id_supervisor", desc=True).limit(1).execute()

        if len(datos.data) == 0:
            return 1  

        ultimo_id = datos.data[0]["id_supervisor"]
        return ultimo_id + 1
    except Exception as e:
        print(f"❌ Error al generar ID: {e}")
        return None


def calcular_edad(fecha_nacimiento_str): 
    try: 
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
    except ValueError: 
        return None 
    
    hoy = date.today()

    edad = hoy.year - fecha_nacimiento.year 
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day): 
        edad -= 1
    return edad

def agregar_supervisor():
    nombre = input("Escribe el nombre: ").strip()

    if not nombre:
        print("\n❌ No puedes insertar un nombre vacío.")
        return
    
    apellidos = input("Escribe el apellido: ").strip()
    if not apellidos:
        print("\n❌ No puedes insertar un apellido vacío.")
        return
    
    fecha_nacimiento = input("Escribe la fecha de nacimiento (YYYY-MM-DD): ").strip()
    edad = calcular_edad(fecha_nacimiento)
    
    if edad is None:
        print("\n❌ Fecha de nacimiento inválida. Usa el formato YYYY-MM-DD (ej: 1990-05-15)")
        return
    
    telefono = input("Escribe el teléfono: ").strip()
    if not telefono:
        print("\n❌ No puedes insertar un teléfono vacío.")
        return
    
    dni = input("Escribe el DNI: ").strip()
    if not dni: 
        print("\n❌ No puedes insertar un DNI vacío.")
        return
    
    nuevo_id = generar_id_supervisor ()

    try:
        insertar = supabase.table("supervisores").insert({
            "id_supervisor": nuevo_id,
            "nombre": nombre,
            "apellidos": apellidos,
            "fecha_nacimiento": fecha_nacimiento,
            "edad": edad,
            "telefono": telefono,
            "dni": dni
        }).execute()

        if insertar.data:
            print(f"\n✅ Registro agregado correctamente. Tu ID es el N.{nuevo_id}")
        else:
            print("\n❌ Ocurrió un error al insertar.")
    except Exception as e:
        print(f"\n❌ Error al agregar dato: {e}")

def mostrar_supervisor():
    nuevo_id = input("Escribe tu ID para ver tus datos: ").strip()

    if not nuevo_id.isdigit():
        print("\n❌ El ID debe ser un número.")
        return

    nuevo_id = int(nuevo_id)
    
    try:
        datos = supabase.table("supervisores").select("*").eq("id_supervisor", nuevo_id).execute()

        if len(datos.data) == 0:
            print("\n❌ No existe un usuario con ese ID.")
            return

        print("\n=== TUS DATOS ===")
        for fila in datos.data:
            print(f"ID: {fila['id_cliente']} | Nombre: {fila['nombre']} | Apellidos: {fila['apellidos']} | Fecha Nac: {fila['fecha_nacimiento']} | Edad: {fila['edad']} | Teléfono: {fila['telefono']} | DNI: {fila['dni']} | Casillero: {fila['id_casillero']}")
    except Exception as e:
        print(f"\n❌ Error al obtener datos: {e}")


def actualizar_dato_supervisor():
    id_obj = input("Escribe el ID del registro a actualizar: ").strip()

    if not id_obj.isdigit():
        print("\n❌ El ID debe ser un número.")
        return

    id_num = int(id_obj)

    try:
        datos = supabase.table("cliente").select("*").eq("id_cliente", id_num).execute()
        if len(datos.data) == 0:
            print("\n❌ No existe un registro con ese ID.")
            return

        print("\n=== ¿Qué quieres actualizar? ===")
        print("1. Nombre")
        print("2. Apellidos")
        print("3. Fecha de nacimiento")
        print("4. Teléfono")
        print("5. DNI")
        print("6. Cancelar")

        opcion = input("\nSelecciona una opción: ").strip()

        campos = {
            "1": "nombre",
            "2": "apellidos",
            "3": "fecha_nacimiento",
            "4": "telefono",
            "5": "dni"
        }

        if opcion not in campos and opcion != "6":
            print("\n❌ Opción no válida.")
            return
        if opcion == "6":
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
            
            actualizar = supabase.table("cliente").update({
                "fecha_nacimiento": nuevo_valor,
                "edad": edad
            }).eq("id_cliente", id_num).execute()
        else:
            actualizar = supabase.table("cliente").update(
                {campo: nuevo_valor}
            ).eq("id_cliente", id_num).execute()

        if actualizar.data:
            print(f"\n✅ El campo '{campo}' fue actualizado correctamente.")
        else:
            print("\n❌ Error al actualizar.")
    except Exception as e:
        print(f"\n❌ Error al actualizar dato: {e}")
def borrar_supervisor():
    id_obj = input("Escribe el ID del registro a borrar: ")
    id_num = int(id_obj)

    borrar = supabase.table("supervisores").delete().eq("id_supervisor", id_num).execute()
    if borrar.data:
        print(f"\n✅ Registro con ID {id_num} borrado correctamente.")
    else:
        print("\n❌ No existe un registro con ese ID.")
    
def generar_id_cliente():
    try:
        datos = supabase.table("clientes").select("id_cliente").order("id_cliente", desc=True).limit(1).execute()

        if len(datos.data) == 0:
            return 1  

        ultimo_id = datos.data[0]["id_cliente"]
        return ultimo_id + 1
    except Exception as e:
        print(f"❌ Error al generar ID: {e}")
        return None

def generar_id_casillero():
    try:
        datos = supabase.table("clientes").select("id_casillero").order("id_casillero", desc=True).limit(1).execute()

        if len(datos.data) == 0:
            return 1  

        ultimo_id_casillero = datos.data[0]["id_casillero"]
        return ultimo_id_casillero + 1
    except Exception as e:
        print(f"❌ Error al generar ID de casillero: {e}")
        return None
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

    nuevo_id = generar_id_cliente()
    nuevo_id_casillero = generar_id_casillero()

    if nuevo_id is None or nuevo_id_casillero is None:
        print("\n❌ No se pudo generar el ID. Intenta de nuevo.")
        return

    try:
        insertar = supabase.table("clientes").insert({
            "id_cliente": nuevo_id,
            "nombre": nombre,
            "apellidos": apellidos,
            "fecha_nacimiento": fecha_nacimiento,
            "edad": edad,
            "telefono": telefono,
            "sucursal": sucursal,
            "dni": dni,
            "id_casillero": nuevo_id_casillero
        }).execute()

        if insertar.data:
            print(f"\n✅ Registro agregado correctamente. Tu ID es el N.{nuevo_id} y tu casillero es el N.{nuevo_id_casillero}")
            return nuevo_id, nombre, apellidos, edad
        else:
            print("\n❌ Ocurrió un error al insertar.")
    except Exception as e:
        print(f"\n❌ Error al insertar dato: {e}")
def mostrar_dato_cliente():
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

def borrar_cliente():
    id_obj = input("Escribe el ID del registro a borrar: ")
    id_num = int(id_obj)

    borrar = supabase.table("clientes").delete().eq("id_cliente", id_num).execute()
    if borrar.data:
        print(f"\n✅ Registro con ID {id_num} borrado correctamente.")
    else:
        print("\n❌ No existe un registro con ese ID.")

def inicio():
    while True:
        print("\n==============================")
        print("        MENÚ PRINCIPAL        ")
        print("==============================")
        print("1. Agregar Supervisor")
        print("2. Iniciar Sesión")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            agregar_supervisor()
        elif opcion == "2":
            id_obj = input("Escribe tu ID para iniciar sesión: ").strip()

            if not id_obj.isdigit():
                print("\n❌ El ID debe ser un número.")
                continue  # Volver al menú en lugar de return

            id_num = int(id_obj)
            
            try:
                datos = supabase.table("supervisores").select("*").eq("id_supervisor", id_num).execute()
                
                if len(datos.data) == 0:
                    print("\n❌ No existe un registro con ese ID.")
                    continue  # Volver al menú
                
                # Si existe, mostrar datos o hacer login
                print(f"\n✅ Bienvenido {datos.data[0]['nombre']} {datos.data[0]['apellidos']}")
                break
            except Exception as e:
                print(f"\n❌ Error al iniciar sesión: {e}")
                
        elif opcion == "3":
            print("\n👋 Saliendo del programa...")
            exit()
        else:
            print("\n❌ Opción no válida.")
def actualizar_cliente():
    id_obj = input("Escribe el ID del registro a actualizar: ").strip()

    if not id_obj.isdigit():
        print("\n❌ El ID debe ser un número.")
        return

    id_num = int(id_obj)

    try:
        datos = supabase.table("clientes").select("*").eq("id_cliente", id_num).execute()
        if len(datos.data) == 0:
            print("\n❌ No existe un registro con ese ID.")
            return

        print("\n=== ¿Qué quieres actualizar? ===")
        print("1. Nombre")
        print("2. Apellidos")
        print("3. Fecha de nacimiento")
        print("4. Teléfono")
        print("5. DNI")
        print("6. Sucursal")
        print("7. Cancelar")

        opcion = input("\nSelecciona una opción: ").strip()

        campos = {
            "1": "nombre",
            "2": "apellidos",
            "3": "fecha_nacimiento",
            "4": "telefono",
            "5": "dni",
            "6": "sucursal"
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
            
            actualizar = supabase.table("cliente").update({
                "fecha_nacimiento": nuevo_valor,
                "edad": edad
            }).eq("id_cliente", id_num).execute()
        else:
            actualizar = supabase.table("clientes").update(
                {campo: nuevo_valor}
            ).eq("id_cliente", id_num).execute()

        if actualizar.data:
            print(f"\n✅ El campo '{campo}' fue actualizado correctamente.")
        else:
            print("\n❌ Error al actualizar.")
    except Exception as e:
        print(f"\n❌ Error al actualizar dato: {e}")
def menuc():
    while True:
        print("\n==============================")
        print("        MENÚ CLIENTES       ")
        print("==============================")
        print("1. Agregar dato")
        print("2. Mostrar mis datos")
        print("3. Actualizar dato por ID")
        print("4. Borrar dato por ID")
        print("5. Salir")
        

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            mostrar_dato_cliente()
        elif opcion == "3":
            actualizar_cliente()
        elif opcion == "4":
            borrar_cliente()
        elif opcion == "5":
            print("\n👋 Saliendo del programa...")
            break
        else:
            print("\n❌ Opción no válida.")
def menus():
    while True:
        print("\n==============================")
        print("        MENÚ SUPERVISORES       ")
        print("==============================")
        print("1. Agregar Supervisor")
        print("2. Mostrar datos")
        print("3. Actualizar dato por ID")
        print("4. Borrar dato por ID")
        print("5. Salir")
        

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            agregar_supervisor()
        elif opcion == "2":
            mostrar_supervisor()    
        elif opcion == "3":
            actualizar_dato_supervisor()
        elif opcion == "4":
            borrar_supervisor()
        elif opcion == "5":
            print("\n👋 Saliendo del programa...")
            break
        else:
            print("\n❌ Opción no válida.")

def generar_id_paquete():
    """Genera un ID único para el paquete"""
    timestamp = int(time.time())
    aleatorio = random.randint(1000, 9999)
    return f"PQ{timestamp}{aleatorio}"

def generar_descripcion():
    """Genera aleatoriamente si es caja o bolsa"""
    tipos = ['Caja', 'Bolsa']
    return random.choice(tipos)

def generar_peso():
    """Genera un peso aleatorio entre 1 y 50 libras"""
    return round(random.uniform(1.0, 50.0), 2)

# ============================================
# FUNCIONES PRINCIPALES
# ============================================

def comprar_paquete():
    """Agrega un nuevo paquete a la tabla de Supabase"""
    print("\n" + "="*50)
    print("        COMPRAR PAQUETE")
    print("="*50)
    
    opcion = 1
    estados = "Compado"
    estado = estados[opcion]
    
    # Generar datos automáticos
    id_paquete = generar_id_paquete()
    descripcion = generar_descripcion()
    peso = generar_peso()
    
    # Crear objeto de datos
    nuevo_paquete = {
        "id_paquete": id_paquete,
        "descripcion": descripcion,
        "peso": peso,
        "estado": estado
    }
    
    # Insertar en Supabase
    try:
        response = supabase.table("paquetes").insert(nuevo_paquete).execute()
        
        # Mostrar confirmación
        print("\n" + "="*50)
        print("✅ PAQUETE AGREGADO EXITOSAMENTE")
        print("="*50)
        print(f"ID Paquete:   {id_paquete}")
        print(f"Descripción:  {descripcion}")
        print(f"Peso:         {peso} lbs")
        print(f"Estado:       {estado}")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error al agregar el paquete: {e}")
        print("="*50)
        
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
def menup():
    while True:
        print("\n==============================")
        print("        MENÚ PAQUETES       ")
        print("==============================")
        print("1. Agregar Paquete")
        print("2. Ver los Paquetes")
        print("3. Salir")
        

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            comprar_paquete()
        elif opcion == "2":
            mostrar_paquetes()
        elif opcion == "3":
            print("\n👋 Saliendo del programa...")
            break
        else:
            print("\n❌ Opción no válida.")

#DELIVERYS
def generar_id_delivery():
    """Genera el siguiente ID disponible para delivery"""
    try:
        datos = supabase.table("dely").select("id_dely").order("id_dely", desc=True).limit(1).execute()
        if len(datos.data) == 0:
            return 1
        return datos.data[0]["id_dely"] + 1
    except Exception as e:
        print(f"❌ Error al generar ID: {e}")
        return None

def registrar_delivery():
    """Registra un nuevo delivery en el sistema"""
    print('Iniciando el Servicio de Deliverys...')
    print('Servicio de Deliverys Iniciado con Éxito.')
    
    print('Le damos la bienvenida al servicio de Deliverys de PDSS')
    print('Nuestro objetivo es brindar ingresos extra o estables cuidando las pertenencias '
          'de nuestros clientes, ofreciendo un servicio rápido, confiable y seguro.')

    nombre = input('Ingrese su nombre: ').strip()
    apellidos = input("Ingrese sus apellidos: ").strip()
    Fecha_nacimiento = input("Ingrese su fecha de nacimiento (DD/MM/AAAA): ").strip()

    while True:
        edad = calcular_edad(Fecha_nacimiento)

        if edad is None:
            print("❌ Formato de fecha de nacimiento inválido. Por favor use DD/MM/AAAA.")
            Fecha_nacimiento = input("Ingrese su fecha de nacimiento nuevamente: ").strip()
        elif edad < 18:
            print("❌ Lo siento, debe ser mayor de edad para registrarse como repartidor.")
            Fecha_nacimiento = input("Ingrese una fecha válida (DD/MM/AAAA): ").strip()
        else:
            break

    telefono = input("Ingrese su número de teléfono: ").strip()
    direccion = input("Ingrese su dirección de residencia: ").strip()
    documento = input("Ingrese su documento de identidad (DNI) o Pasaporte: ").strip()

    nuevo_id = generar_id_delivery()
    if nuevo_id is None:
        print("❌ Error al generar ID. Intente nuevamente.")
        return None, None, None, None

    fecha_bd = datetime.strptime(Fecha_nacimiento, "%d/%m/%Y").strftime("%Y-%m-%d")

    try:
        insertar = supabase.table("dely").insert({
            "id_dely": nuevo_id,
            "nombre": nombre,
            "apellidos": apellidos,
            "edad": edad,
            "fecha_nacimiento": fecha_bd,
            "telefono": telefono,
            "direccion": direccion,
            "dni": documento
        }).execute()

        if insertar.data:
            print(f"\n✅ Registro exitoso. Bienvenido/a, {nombre} {apellidos}")
            print(f'🆔 Este será tu ID de repartidor: PDSS-{nuevo_id:04d}')
            print('📋 Recuerda siempre cumplir con las normas de seguridad.')
            return nuevo_id, nombre, apellidos, edad
        else:
            print("❌ Error al registrar delivery")
            return None, None, None, None
            
    except Exception as e:
        print(f"❌ Error al registrar: {e}")
        return None, None, None, None


def login_delivery():
    """Permite a un delivery iniciar sesión"""
    print("\n=== INICIAR SESIÓN ===")
    id_delivery = input("Ingresa tu ID de delivery: ").strip()
    
    if not id_delivery.isdigit():
        print("❌ ID inválido")
        return None, None, None, None
    
    id_delivery = int(id_delivery)
    
    try:
        delivery = supabase.table("dely").select("*").eq("id_dely", id_delivery).execute()
        
        if len(delivery.data) == 0:
            print("❌ Delivery no encontrado")
            return None, None, None, None
        
        delivery_data = delivery.data[0]
        print(f"\n✅ Bienvenido de vuelta {delivery_data['nombre']} {delivery_data['apellidos']}")
        
        return (delivery_data['id_dely'], 
                delivery_data['nombre'], 
                delivery_data['apellidos'], 
                delivery_data['edad'])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None, None, None


def asignar_paquete_a_delivery(id_delivery):
    print(f"\n=== ASIGNAR PAQUETE AL DELIVERY ID: {id_delivery} ===\n")
    
    id_paquete = input("Ingresa el ID del paquete: ").strip()
    
    if not id_paquete.isdigit():
        print("❌ El ID debe ser un número")
        return
    
    id_paquete = int(id_paquete)
    
    try:
        paquete = supabase.table("paquetes").select("*").eq("id_paquete", id_paquete).execute()
        
        if len(paquete.data) == 0:
            print(f"❌ El paquete con ID {id_paquete} NO EXISTE")
            return
        
        paquete_data = paquete.data[0]
        
        if paquete_data['id_dely'] is not None and paquete_data['id_dely'] != id_delivery:
            print(f"❌ El paquete ya está asignado a otro delivery")
            return
        
        if paquete_data['estado'] == 'entregado':
            print("❌ Este paquete ya fue entregado")
            return
        
        actualizar = supabase.table("paquetes").update({
            "id_dely": id_delivery,
            "estado": "en_transito",
            "fecha_asignacion": datetime.now().isoformat()
        }).eq("id_paquete", id_paquete).execute()
        
        if actualizar.data:
            print("\n✅ Paquete asignado exitosamente!")
            print(f"📦 ID Paquete: {id_paquete}")
            print(f"📝 Descripción: {paquete_data['descripcion']}")
            print(f"📍 Destino: {paquete_data['destino']}")
            print(f"⚖️ Peso: {paquete_data['peso']} kg")
        else:
            print("❌ Error al asignar el paquete")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def ver_mis_paquetes(id_delivery):
    try:
        paquetes = supabase.table("paquetes").select("*").eq("id_dely", id_delivery).execute()
        
        if len(paquetes.data) == 0:
            print("\n📭 No tienes paquetes asignados")
            return
        
        print("\n" + "="*70)
        print("                    MIS PAQUETES")
        print("="*70)
        
        for paquete in paquetes.data:
            print(f"\n📦 ID: {paquete['id_paquete']} | Estado: {paquete['estado'].upper()}")
            print(f"   Descripción: {paquete['descripcion']}")
            print(f"   Destino: {paquete['destino']}")
            print(f"   Peso: {paquete['peso']} kg")
            print("-" * 70)
        
        input("\nPresiona ENTER para continuar...")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def marcar_entregado(id_delivery):
    id_paquete = input("\nIngresa el ID del paquete a marcar como entregado: ").strip()
    
    if not id_paquete.isdigit():
        print("❌ El ID debe ser un número")
        return
    
    id_paquete = int(id_paquete)
    
    try:
        paquete = supabase.table("paquetes").select("*") \
            .eq("id_paquete", id_paquete).eq("id_dely", id_delivery).execute()
        
        if len(paquete.data) == 0:
            print("❌ Este paquete no está asignado a ti")
            return
        
        actualizar = supabase.table("paquetes").update({
            "estado": "entregado",
            "fecha_entrega": datetime.now().isoformat()
        }).eq("id_paquete", id_paquete).execute()
        
        if actualizar.data:
            print(f"✅ Paquete {id_paquete} marcado como ENTREGADO")
        else:
            print("❌ Error al actualizar el estado")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def consultar_datos_delivery(id_delivery):
    try:
        delivery = supabase.table("dely").select("*").eq("id_dely", id_delivery).execute()
        
        if len(delivery.data) == 0:
            print("❌ Datos no encontrados")
            return
        
        data = delivery.data[0]
        
        print("\n" + "="*70)
        print("              DATOS DEL REPARTIDOR")
        print("="*70)
        print(f"🆔 ID: PDSS-{data['id_dely']:04d}")
        print(f"👤 Nombre: {data['nombre']} {data['apellidos']}")
        print(f"🎂 Edad: {data['edad']} años")
        print(f"📞 Teléfono: {data['telefono']}")
        print(f"🏠 Dirección: {data['direccion']}")
        print(f"📄 Documento: {data['dni']}")
        print("="*70)
        
        input("\nPresiona ENTER para continuar...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
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

def borrar_personal_caja():
    id_obj = input("Escribe el ID del registro a borrar: ")
    id_num = int(id_obj)

    borrar = supabase.table("personal_caja").delete().eq("id_personal", id_num).execute()
    if borrar.data:
        print(f"\n✅ Registro con ID {id_num} borrado correctamente.")
    else:
        print("\n❌ No existe un registro con ese ID.") 
def inicio_delivery():
    while True:
        print("\n==============================")
        print("       MENÚ DELIVERY       ")
        print("==============================")
        print("1. Registrar como Delivery")
        print("2. Iniciar Sesión")
        print("3. Salir")
        

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            registrar_delivery()
        elif opcion == "2":
            login_delivery()
        elif opcion == "3":
            print("\n👋 Saliendo del programa...")
            break
        else:
            print("\n❌ Opción no válida.")
def menud():
    while True:
        print("\n==============================")
        print("       MENÚ DELIVERY       ")
        print("==============================")
        print("1. Asignar Paquete")
        print("2. Ver Mis Paquetes")
        print("3. Marcar Paquete como Entregado")
        print("4. Consultar Mis Datos")
        print("5. Salir")
        

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            asignar_paquete_a_delivery()
        elif opcion == "2":
            ver_mis_paquetes()
        elif opcion == "3":
            marcar_entregado()
        elif opcion == "4":
            consultar_datos_delivery()
        elif opcion == "5":
            print("\n👋 Saliendo del programa...")
            break
        else:
            print("\n❌ Opción no válida.")
def menu_personal():
    while True:
        print("\n==============================")
        print("     MENÚ PERSONAL DE CAJA    ")
        print("==============================")
        print("1. Registrar Personal de Caja")
        print("2. Iniciar Usuario de Caja")
        print("3. Actualizar personal de Caja")
        print("4. Borrar personal de Caja")
        print("5. Salir")
        

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            registrar_personal_caja()
        elif opcion == "2":
            login_personal_caja()
        elif opcion == "3":
            actualizar_personal_caja()
        elif opcion == "4":
            borrar_personal_caja()
        elif opcion == "5":
            break
        else:
            print("\n❌ Opción no válida.")


def apartados():
    while True:
        print("\n==============================")
        print("       APARTADOS      ")
        print("==============================")
        print("1.Supervisores")
        print("2.Paquetes")
        print("3.Deliveries")
        print("4.Personal de caja")
        print("5.Clientes")
        print("6. Salir")
        

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            menus()
        elif opcion == "2":
            menup()
        elif opcion == "3":
            inicio_delivery()
        elif opcion == "4":
            menu_personal()
        elif opcion == "5":
            menuc()
        elif opcion == "6":
            print("\n👋 Saliendo del programa...")
            exit()
        else:
            print("\n❌ Opción no válida.")

           


# Ej;
inicio()
apartados()