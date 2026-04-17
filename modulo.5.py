import redis
import json

# Conexión
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


# -------- GENERAR ID --------
def generar_id():
    return r.incr("contador_libros")


# -------- AGREGAR --------
def agregar_libro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado: ")

    libro_id = generar_id()
    clave = f"libro:{libro_id}"

    libro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    r.set(clave, json.dumps(libro))

    print(" Libro agregado")


# -------- VER TODOS --------
def ver_libros():
    claves = r.scan_iter("libro:*")

    for clave in claves:
        libro_json = r.get(clave)

        if libro_json:
            libro = json.loads(libro_json)
            print(f"\n{clave} → {libro}")


# -------- BUSCAR --------
def buscar_libros():
    termino = input("Buscar: ").lower()

    for clave in r.scan_iter("libro:*"):
        libro_json = r.get(clave)

        if libro_json:
            libro = json.loads(libro_json)

            if (termino in libro["titulo"].lower() or
                termino in libro["autor"].lower() or
                termino in libro["genero"].lower()):

                print(f"\n{clave} → {libro}")


# -------- ACTUALIZAR --------
def actualizar_libro():
    clave = input("ID del libro (ej: libro:1): ")

    libro_json = r.get(clave)

    if libro_json:
        libro = json.loads(libro_json)

        print("Campos:", list(libro.keys()))
        campo = input("Campo a actualizar: ")

        if campo in libro:
            nuevo_valor = input("Nuevo valor: ")
            libro[campo] = nuevo_valor

            r.set(clave, json.dumps(libro))
            print(" Actualizado")
        else:
            print(" Campo inválido")
    else:
        print("Libro no encontrado")


# -------- ELIMINAR --------
def eliminar_libro():
    clave = input("ID del libro: ")

    if r.delete(clave):
        print(" Eliminado")
    else:
        print(" No existe")


# -------- MENÚ --------
def menu():
    while True:
        print("\n--- BIBLIOTECA ---")
        print("1. Agregar libro")
        print("2. Ver libros")
        print("3. Buscar libros")
        print("4. Actualizar libro")
        print("5. Eliminar libro")
        print("6. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            ver_libros()
        elif opcion == "3":
            buscar_libros()
        elif opcion == "4":
            actualizar_libro()
        elif opcion == "5":
            eliminar_libro()
        elif opcion == "6":
            print(" Saliendo...")
            break
        else:
            print(" Opción inválida")


if __name__ == "__main__":
    try:
        menu()
    except Exception as e:
        print(" Error:", e)