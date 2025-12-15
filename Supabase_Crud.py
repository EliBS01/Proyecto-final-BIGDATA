from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ConnectionError("Faltan SUPABASE_URL o SUPABASE_KEY")

supabase: Client = create_client(url, key)

ultimo_id_generado = None

def generar_id():
    datos = supabase.table("public").select("id").order("id", desc=True).limit(1).execute()

    if len(datos.data) == 0:
        return 1  

    ultimo_id = datos.data[0]["id"]
    return ultimo_id + 1 

def agregar_dato():
    global ultimo_id_generado

    nombre = input("Escribe el nombre: ").strip()

    if not nombre:
        print("\n No puedes insertar un nombre vacío.")
        return
    apellidos = input("Escribe el apellido: ").strip()
    if not apellidos:
        print("\n No puedes insertar un apellido vacío.")
        return
    edad = input("Escribe la edad: ").strip()
    if not edad.isdigit():
        print("\n La edad debe ser un número.")
        return  
    telefono = input("Escribe el teléfono: ").strip()
    if not telefono:
        print("\n No puedes insertar un teléfono vacío.")
        return
    dni = input("Escribe el DNI: ").strip()
    if not dni: 
        print("\n No puedes insertar un DNI vacío.")
        return
    nuevo_id = generar_id()

    insertar = supabase.table("public").insert({
        "id": nuevo_id,
        "nombre": nombre,
        "apellidos": apellidos,
        "edad": int(edad),
        "telefono": telefono,
        "dni": dni 
    }).execute()

    if insertar.data:
        ultimo_id_generado = nuevo_id
        print(f"\n✅ Registro agregado correctamente con ID {nuevo_id}")
    else:
        print("\n❌ Ocurrió un error al insertar.")

def mostrar_mis_datos():
    nuevo_id = input("Escribe tu ID para ver tus datos: ")

    if not nuevo_id.isdigit():
        print("\n❌ El ID debe ser un número.")
        return

    nuevo_id = int(nuevo_id)
    datos = supabase.table("public").select("*").eq("id", nuevo_id).execute()

    if len(datos.data) == 0:
        print("\n❌ No existe un usuario con ese ID.")
        return

    print("\n=== TUS DATOS ===")
    for fila in datos.data:
        print(f"ID: {fila['id']} | Nombre: {fila['nombre']} | Apellidos: {fila['apellidos']} | Edad: {fila['edad']} | Teléfono: {fila['telefono']} | DNI: {fila['dni']}")


def actualizar_dato():
    id_obj = input("Escribe el ID del registro a actualizar: ")

    if not id_obj.isdigit():
        print("\n❌ El ID debe ser un número.")
        return

    id_num = int(id_obj)

    # Verificar si existe el registro
    datos = supabase.table("public").select("*").eq("id", id_num).execute()
    if len(datos.data) == 0:
        print("\n❌ No existe un registro con ese ID.")
        return

    print("\n=== ¿Qué quieres actualizar? ===")
    print("1. Nombre")
    print("2. Apellidos")
    print("3. Edad")
    print("4. Teléfono")
    print("5. DNI")
    print("6. Cancelar")

    opcion = input("\nSelecciona una opción: ")

    campos = {
        "1": "nombre",
        "2": "apellidos",
        "3": "edad",
        "4": "telefono",
        "5": "dni"
    }

    if opcion not in campos and opcion != "6":
        print("\n❌ Opción no válida.")
        return
    if opcion == "6":
        print("\nOperación cancelada.")
        return

    campo = campos[opcion]
    nuevo_valor = input(f"Escribe el nuevo valor para '{campo}': ").strip()

    if not nuevo_valor:
        print("\n❌ El valor no puede estar vacío.")
        return

    # Si es edad, convertir a número
    if campo == "edad":
        if not nuevo_valor.isdigit():
            print("\n❌ La edad debe ser un número.")
            return
        nuevo_valor = int(nuevo_valor)

    actualizar = supabase.table("public").update(
        {campo: nuevo_valor}
    ).eq("id", id_num).execute()

    if actualizar.data:
        print(f"\n✅ El campo '{campo}' fue actualizado correctamente.")
    else:
        print("\n❌ Error al actualizar.")
    
def borrar_dato():
    id_obj = input("Escribe el ID del registro a borrar: ")
    id_num = int(id_obj)

    borrar = supabase.table("public").delete().eq("id", id_num).execute()

    if borrar.data:
        print(f"\n✅ Registro con ID {id_num} borrado correctamente.")
    else:
        print("\n❌ No existe un registro con ese ID.")
    

def menu():
    while True:
        print("\n==============================")
        print("        MENÚ PRINCIPAL        ")
        print("==============================")
        print("1. Agregar dato")
        print("2. Mostrar todos los datos")
        print("3. Actualizar dato por ID")
        print("4. Borrar dato por ID")
        print("5. Salir")
        

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            agregar_dato()
        elif opcion == "2":
            mostrar_mis_datos()
        elif opcion == "3":
            actualizar_dato()
        elif opcion == "4":
            borrar_dato()
        elif opcion == "5":
            print("\n👋 Saliendo del programa...")
            break
        else:
            print("\n❌ Opción no válida.")


# Ejecutar programa
menu()

