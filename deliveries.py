from time import sleep
from datetime import date, datetime
from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client

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

print("Bienvenido a la app de Deliverys de PDSS")
print('Package Delivery Service System')
print('Desarrollado por: Eligabriel Espinal')
sleep(2)


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


def calcular_edad(fecha_nacimiento_str): 
    """Calcula la edad a partir de una fecha de nacimiento"""
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%d/%m/%Y").date()
    except ValueError:
        return None 
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year 
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day): 
        edad -= 1
    return edad


def registrar_delivery():
    """Registra un nuevo delivery en el sistema"""
    print('Iniciando el Servicio de Deliverys...')
    sleep(2)
    print('Servicio de Deliverys Iniciado con Éxito.')
    sleep(2)
    
    print('Le damos la bienvenida al servicio de Deliverys de PDSS')
    sleep(1)
    print('Nuestro objetivo es brindar ingresos extra o estables cuidando las pertenencias '
          'de nuestros clientes, ofreciendo un servicio rápido, confiable y seguro.')
    sleep(3)

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

    # Generar ID
    nuevo_id = generar_id_delivery()
    if nuevo_id is None:
        print("❌ Error al generar ID. Intente nuevamente.")
        return None, None, None, None

    # Convertir fecha al formato de base de datos (YYYY-MM-DD)
    fecha_bd = datetime.strptime(Fecha_nacimiento, "%d/%m/%Y").strftime("%Y-%m-%d")

    try:
        # Insertar en la base de datos
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
            print(f"\n✅ Registro exitoso. Bienvenido/a, {nombre} {apellidos}, al equipo de repartidores de PDSS!")
            sleep(1)
            print(f'🆔 Este será tu ID de repartidor: PDSS-{nuevo_id:04d}')
            sleep(1)
            print('📋 Recuerda siempre cumplir con las normas de seguridad y brindar un excelente servicio a nuestros clientes.')
            sleep(3)
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
        sleep(2)
        
        return (delivery_data['id_dely'], 
                delivery_data['nombre'], 
                delivery_data['apellidos'], 
                delivery_data['edad'])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None, None, None


def asignar_paquete_a_delivery(id_delivery):
    """Permite al delivery escanear/ingresar IDs de paquetes para asignárselos"""
    print(f"\n=== ASIGNAR PAQUETE AL DELIVERY ID: {id_delivery} ===\n")
    
    id_paquete = input("Ingresa el ID del paquete: ").strip()
    
    if not id_paquete.isdigit():
        print("❌ El ID debe ser un número")
        sleep(2)
        return
    
    id_paquete = int(id_paquete)
    
    try:
        # 1. Verificar que el paquete existe
        paquete = supabase.table("paquetes").select("*").eq("id_paquete", id_paquete).execute()
        
        if len(paquete.data) == 0:
            print(f"❌ El paquete con ID {id_paquete} NO EXISTE")
            sleep(2)
            return
        
        paquete_data = paquete.data[0]
        
        # 2. Verificar que el paquete no esté ya asignado a otro delivery
        if paquete_data['id_dely'] is not None and paquete_data['id_dely'] != id_delivery:
            print(f"❌ El paquete ya está asignado a otro delivery (ID: {paquete_data['id_dely']})")
            sleep(2)
            return
        
        # 3. Verificar estado del paquete
        if paquete_data['estado'] == 'entregado':
            print("❌ Este paquete ya fue entregado")
            sleep(2)
            return
        
        # 4. Asignar el paquete al delivery
        actualizar = supabase.table("paquetes").update({
            "id_dely": id_delivery,
            "estado": "en_transito",
            "fecha_asignacion": datetime.now().isoformat()
        }).eq("id_paquete", id_paquete).execute()
        
        if actualizar.data:
            print(f"\n✅ Paquete asignado exitosamente!")
            sleep(1)
            print(f"📦 ID Paquete: {id_paquete}")
            print(f"📝 Descripción: {paquete_data['descripcion']}")
            print(f"📍 Destino: {paquete_data['destino']}")
            print(f"⚖️ Peso: {paquete_data['peso']} kg")
            sleep(3)
        else:
            print("❌ Error al asignar el paquete")
            sleep(2)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sleep(2)


def ver_mis_paquetes(id_delivery):
    """Muestra todos los paquetes asignados a un delivery"""
    try:
        paquetes = supabase.table("paquetes").select("*").eq("id_dely", id_delivery).execute()
        
        if len(paquetes.data) == 0:
            print("\n📭 No tienes paquetes asignados")
            sleep(2)
            return
        
        print("\n" + "="*70)
        print("                    MIS PAQUETES")
        print("="*70)
        
        for paquete in paquetes.data:
            estado_emoji = {
                "pendiente": "⏳",
                "en_transito": "🚚",
                "entregado": "✅"
            }
            emoji = estado_emoji.get(paquete['estado'], "📦")
            
            print(f"\n{emoji} ID: {paquete['id_paquete']} | Estado: {paquete['estado'].upper()}")
            print(f"   Descripción: {paquete['descripcion']}")
            print(f"   Destino: {paquete['destino']}")
            print(f"   Peso: {paquete['peso']} kg")
            print(f"   Asignado: {paquete.get('fecha_asignacion', 'N/A')}")
            print("-" * 70)
        
        input("\nPresiona ENTER para continuar...")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sleep(2)


def marcar_entregado(id_delivery):
    """Marca un paquete como entregado"""
    id_paquete = input("\nIngresa el ID del paquete a marcar como entregado: ").strip()
    
    if not id_paquete.isdigit():
        print("❌ El ID debe ser un número")
        sleep(2)
        return
    
    id_paquete = int(id_paquete)
    
    try:
        # Verificar que el paquete esté asignado a este delivery
        paquete = supabase.table("paquetes").select("*").eq("id_paquete", id_paquete).eq("id_dely", id_delivery).execute()
        
        if len(paquete.data) == 0:
            print("❌ Este paquete no está asignado a ti")
            sleep(2)
            return
        
        # Marcar como entregado
        actualizar = supabase.table("paquetes").update({
            "estado": "entregado",
            "fecha_entrega": datetime.now().isoformat()
        }).eq("id_paquete", id_paquete).execute()
        
        if actualizar.data:
            print(f"✅ Paquete {id_paquete} marcado como ENTREGADO")
            sleep(2)
        else:
            print("❌ Error al actualizar el estado")
            sleep(2)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sleep(2)


def consultar_datos_delivery(id_delivery):
    """Consulta y muestra los datos del delivery"""
    try:
        delivery = supabase.table("dely").select("*").eq("id_dely", id_delivery).execute()
        
        if len(delivery.data) == 0:
            print("❌ Datos no encontrados")
            sleep(2)
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
        print(f"📄 Documento: {data['documento']}")
        print("="*70)
        
        input("\nPresiona ENTER para continuar...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sleep(2)


def menu_principal_delivery(id_delivery, nombre, apellidos, edad):
    """Menú principal para deliverys con sesión iniciada"""
    
    while True:
        print('\n<------------------------------------->')
        print(f'===== DELIVERY: {nombre} {apellidos} =====')
        print('Seleccione una opción:')
        print('1. Recoger un paquete (Escanear ID)')
        print('2. Ver mis paquetes asignados')
        print('3. Entregar un paquete (Marcar como entregado)')
        print('4. Anomalías en la entrega')
        print('5. Soporte Técnico')
        print('6 Saldo Actual')
        print('7 Consultar mis datos de repartidor')
        print('8 Cerrar sesión')
        print('=====================================')

        try:
            opcion = int(input('Favor digitar una de las opciones: '))
        except ValueError:
            print("❌ Debe ingresar un número. Intente de nuevo.")
            continue

        if opcion == 1:
            print('📦 Ha seleccionado recoger un paquete.')
            sleep(1)
            asignar_paquete_a_delivery(id_delivery)
            
        elif opcion == 2:
            print('📋 Mostrando tus paquetes asignados...')
            sleep(1)
            ver_mis_paquetes(id_delivery)
            
        elif opcion == 3:
            print('✅ Ha seleccionado entregar un paquete.')
            sleep(1)
            marcar_entregado(id_delivery)
            
        elif opcion == 4:
            print('⚠️ Ha seleccionado reportar anomalías en la entrega.')
            sleep(2)
            print('Por favor, describa la anomalía encontrada')
            texto_anomalia = input().strip()

            insertar_anomalia = supabase.table("anomalias").insert({
                "id_dely": id_delivery,
                "anomalia": texto_anomalia
            }).execute()

            if insertar_anomalia.data:
                print('✅ Anomalía reportada exitosamente. Nuestro equipo se pondrá en contacto.')
                sleep(2)
            else:
                print("❌ Ocurrió un error al registrar la anomalía")

            
            
        elif opcion == 5:
            print('🛠️ Ha seleccionado soporte técnico.')
            sleep(2)
            print('Por favor, describa el problema técnico:')
            problema = input()
            print('✅ Problema reportado exitosamente.')
            sleep(2)
            
        elif opcion == 6:
            print('💰 Ha seleccionado ver su saldo actual.')
            sleep(2)
            print('Mostrando saldo...')
            sleep(2)
            print('Saldo mostrado exitosamente.')
            
        elif opcion == 7:
            print('📄 Consultando tus datos...')
            sleep(1)
            consultar_datos_delivery(id_delivery)
            
        elif opcion == 8:
            print('👋 Cerrando sesión...')
            sleep(2)
            print('Sesión cerrada correctamente.')
            break
            
        else:
            print('❌ Opción no válida. Por favor, intente de nuevo.')
            sleep(1)


# ========== PROGRAMA PRINCIPAL ==========

while True:
    print('\n<------------------------------------->')
    print('===== MENÚ DELIVERYS PDSS =====')
    print('Seleccione una opción:')
    print('1. Registrarse como Delivery')
    print('2. Iniciar Sesión')
    print('3. Salir del Sistema')
    print('=====================================')

    try:
        opcion = int(input('Favor digitar una de las opciones: '))
    except ValueError:
        print("❌ Debe ingresar un número. Intente de nuevo.")
        continue

    if opcion == 1:
        id_del, nom, ape, ed = registrar_delivery()
        if id_del:
            menu_principal_delivery(id_del, nom, ape, ed)
            
    elif opcion == 2:
        id_del, nom, ape, ed = login_delivery()
        if id_del:
            menu_principal_delivery(id_del, nom, ape, ed)
            
    elif opcion == 3:
        print('👋 Saliendo del Sistema...')
        sleep(2)
        print('Gracias por usar el Servicio de Deliverys de PDSS. ¡Hasta luego!')
        break
        
    else:
        print('❌ Opción no válida. Por favor, intente de nuevo.')
        sleep(1)

