# coding=utf-8
import os
import sys
import httpx

# URL base de la API
BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_api():
    print("🚀 Iniciando pruebas de la API de Recetas...")
    
    # 1. Iniciar sesión como administrador
    print("\n🔐 1. Iniciando sesión como administrador...")
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    try:
        response = httpx.post(f"{BASE_URL}/auth/login", json=login_data)
    except Exception as e:
        print(f"❌ Error al conectar con el servidor: {e}")
        print("Asegúrate de que el servidor uvicorn está corriendo en http://127.0.0.1:8000")
        sys.exit(1)
        
    if response.status_code != 200:
        print(f"❌ Error de inicio de sesión ({response.status_code}): {response.text}")
        sys.exit(1)
        
    token_info = response.json()
    access_token = token_info["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    print("✅ Sesión iniciada correctamente!")
    
    # 2. Crear una dificultad (si no existe)
    print("\n🏷️  2. Creando dificultad 'Fácil'...")
    diff_data = {"name": "Fácil"}
    response = httpx.post(f"{BASE_URL}/recipes/difficulties/", json=diff_data, headers=headers)
    
    if response.status_code in [201, 200]:
        diff_info = response.json()
        print(f"✅ Dificultad configurada: ID={diff_info['id']}, Nombre={diff_info['name']}")
        difficulty_id = diff_info['id']
    else:
        # Si ya existe o da error, listamos las dificultades para obtener una
        print("⚠️ No se pudo crear directamente, buscando en las dificultades existentes...")
        response = httpx.get(f"{BASE_URL}/recipes/difficulties/", headers=headers)
        diffs = response.json()
        if not diffs:
            print("❌ No hay dificultades disponibles y no se pudo crear una nueva.")
            sys.exit(1)
        difficulty_id = diffs[0]['id']
        print(f"✅ Usando dificultad existente: ID={difficulty_id}, Nombre={diffs[0]['name']}")

    # 3. Crear un ingrediente (si no existe)
    print("\n🥕 3. Creando ingrediente 'Pollo'...")
    ing_data = {"name": "Pollo"}
    response = httpx.post(f"{BASE_URL}/ingredients/", json=ing_data, headers=headers)
    
    if response.status_code in [201, 200]:
        ing_info = response.json()
        print(f"✅ Ingrediente configurado: ID={ing_info['id']}, Nombre={ing_info['name']}")
        ingredient_id = ing_info['id']
    else:
        print("⚠️ No se pudo crear el ingrediente, buscando en los existentes...")
        response = httpx.get(f"{BASE_URL}/ingredients/", headers=headers)
        ings = response.json()
        if not ings:
            print("❌ No hay ingredientes disponibles y no se pudo crear uno nuevo.")
            sys.exit(1)
        ingredient_id = ings[0]['id']
        print(f"✅ Usando ingrediente existente: ID={ingredient_id}, Nombre={ings[0]['name']}")

    # 4. Crear una receta
    print("\n🍳 4. Creando una nueva receta...")
    recipe_data = {
        "name": "Arroz con Pollo de Prueba",
        "description": "Una receta deliciosa de prueba para validar la API.",
        "difficulty_id": difficulty_id,
        "info": {
            "prep_time": 15,
            "cook_time": 25,
            "total_time": 40,
            "calories": 350
        },
        "ingredients": [
            {
                "quantity": "500",
                "measurement_unit": "g",
                "ingredient_id": ingredient_id
            }
        ],
        "steps": [
            {
                "content": "Cocinar el pollo con cebolla y ajo.",
                "description": "Hervir el pollo hasta que esté tierno y desmenuzar.",
                "order": 1
            },
            {
                "content": "Mezclar con el arroz y vegetales.",
                "description": "Cocinar todo junto en la olla arrocera.",
                "order": 2
            }
        ]
    }
    
    response = httpx.post(f"{BASE_URL}/recipes/", json=recipe_data, headers=headers)
    if response.status_code != 201:
        print(f"❌ Error al crear receta ({response.status_code}): {response.text}")
        sys.exit(1)
        
    recipe_info = response.json()
    recipe_id = recipe_info['id']
    print(f"✅ Receta creada con éxito! ID={recipe_id}, Nombre='{recipe_info['name']}'")
    
    # 5. Obtener todas las recetas
    print("\n📚 5. Obteniendo listado de todas las recetas...")
    response = httpx.get(f"{BASE_URL}/recipes/")
    if response.status_code != 200:
        print(f"❌ Error al obtener listado ({response.status_code}): {response.text}")
        sys.exit(1)
        
    recipes_list = response.json()
    print(f"✅ Se encontraron {len(recipes_list)} recetas en total.")
    
    # 6. Obtener detalles de la receta recién creada
    print(f"\n🔍 6. Obteniendo detalles de la receta ID {recipe_id}...")
    response = httpx.get(f"{BASE_URL}/recipes/{recipe_id}")
    if response.status_code != 200:
        print(f"❌ Error al obtener detalles de la receta ({response.status_code}): {response.text}")
        sys.exit(1)
        
    detail = response.json()
    print(f"✅ Detalle recuperado correctamente:")
    print(f"   - Nombre: {detail['name']}")
    print(f"   - Dificultad: {detail['difficulty']['name'] if detail.get('difficulty') else 'N/A'}")
    print(f"   - Calorías: {detail['infos']['calories'] if detail.get('infos') else 'N/A'} kcal")
    print(f"   - Ingredientes: {len(detail.get('ingredients', []))}")
    print(f"   - Pasos: {len(detail.get('steps', []))}")

    # 7. Calificar la receta
    print(f"\n⭐ 7. Calificando la receta ID {recipe_id} con 5 estrellas...")
    response = httpx.post(f"{BASE_URL}/recipes/{recipe_id}/rate?rating=5", headers=headers)
    if response.status_code != 200:
        print(f"❌ Error al calificar la receta ({response.status_code}): {response.text}")
        sys.exit(1)
    print(f"✅ Calificación agregada correctamente: {response.json()}")

    # 8. Limpiar: Eliminar la receta de prueba
    print(f"\n🗑️  8. Eliminando la receta de prueba ID {recipe_id} para dejar la base limpia...")
    response = httpx.delete(f"{BASE_URL}/recipes/{recipe_id}", headers=headers)
    if response.status_code != 200:
        print(f"❌ Error al eliminar la receta ({response.status_code}): {response.text}")
        sys.exit(1)
    print("✅ Receta de prueba eliminada exitosamente!")
    
    print("\n🎉 ¡Todas las pruebas de la API pasaron exitosamente!")

if __name__ == "__main__":
    test_api()
