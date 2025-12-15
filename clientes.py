#CREAR
#su propio usuario
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


def actualizar_dato():
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
def generar_paquete():
    try:
        datos = supabase.table("paquetes").select("id_paquete").order("id_paquete", desc=True).limit(1).execute()

        if len(datos.data) == 0:
            return 1  

        ultimo_id = datos.data[0]["id_paquete"]
        return ultimo_id + 1
    except Exception as e:
        print(f"❌ Error al generar ID: {e}")
        return None
def generar_descripcion():
    """Genera aleatoriamente si es caja o bolsa"""
    tipos = ['Caja', 'Bolsa']
    return random.choice(tipos)

def generar_peso():
    """Genera un peso aleatorio entre 1 y 50 libras"""
    return round(random.uniform(1.0, 50.0), 2)

def comprar_paquete():
    """Agrega un nuevo paquete a la tabla de Supabase"""
    print("\n" + "="*50)
    print("        COMPRAR PAQUETE")
    print("="*50)
    
    opcion = 1
    estados = "Compado"
    estado = estados[opcion]
    
    # Generar datos automáticos
    id_paquete = generar_paquete()
    descripcion = generar_descripcion()
    peso = generar_peso()
    
    # Crear objeto de datos
    nuevo_paquete = {
        "id_paquete": id_paquete,
        "descripcion": descripcion,
        "id_cliente": id_cliente,
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
def mostrar_paquetes(id_cliente):
    try:
        paquetes = supabase.table("paquetes") \
            .select("id_paquete, descripcion, peso, estado") \
            .eq("id_cliente", id_cliente) \
            .execute()

        if not paquetes.data:
            print("\n📭 No tienes paquetes registrados.")
            return

        print("\n" + "="*60)
        print("         TUS PAQUETES")
        print("="*60)

        for i, paquete in enumerate(paquetes.data, start=1):
            print(f"\nPaquete #{i}")
            print(f" ID: {paquete['id_paquete']}")
            print(f" Descripción: {paquete['descripcion']}")
            print(f" Peso: {paquete['peso']} lbs")
            print(f" Estado: {paquete['estado'].upper()}")
            print("-"*60)

    except Exception as e:
        print(f"❌ Error al consultar paquetes: {e}")
    


def menuc(id_cliente=None, nombre=None, apellidos=None, edad=None):
    while True:
        print("\n==============================")
        print("        MENÚ PRINCIPAL        ")
        print("==============================")
        print("1. Mostrar paquetes")
        print("2. Mostrar mis datos")
        print("3. Actualizar dato por ID")
        print("4. Comprar paquete")
        print("5. Salir")
        

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            mostrar_paquetes(id_cliente)
        elif opcion == "2":
            mostrar_mis_datos()
        elif opcion == "3":
            actualizar_dato()
        elif opcion == "4":
            comprar_paquete() 
        elif opcion == "5":
            print("\n👋 Saliendo del programa...")
            break
        else:
            print("\n❌ Opción no válida.")


# Ejecutar programa
while True:
    print('\n<------------------------------------->')
    print('===== MENÚ DELIVERYS PDSS =====')
    print('Seleccione una opción:')
    print('1. Registrarse como Cliente')
    print('2. Iniciar Sesión')
    print('3. Salir del Sistema')
    print('=====================================')

    try:
        opcion = int(input('Favor digitar una de las opciones: '))
    except ValueError:
        print("❌ Debe ingresar un número. Intente de nuevo.")
        continue

    if opcion == 1:
        id_cliente, nom, ape, ed = registrar_cliente()
        if id_cliente:
            menuc(id_cliente, nom, ape, ed)
            
    elif opcion == 2:
        id_cliente, nom, ape, ed = login_cliente()
        if id_cliente:
            menuc(id_cliente, nom, ape, ed)
            
    elif opcion == 3:
        print('👋 Saliendo del Sistema...')
        print('Gracias por usar el Servicio de Deliverys de PDSS. ¡Hasta luego!')
        break
        
    else:
        print('❌ Opción no válida. Por favor, intente de nuevo.')
    


menuc()