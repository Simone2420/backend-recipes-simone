# 🛠️ Guía de Trabajo: Git Merge & Alembic Migrations

Este documento es una guía práctica para mantener un historial de Git limpio y organizado ("merges bonitos") y para utilizar correctamente el sistema de migraciones con **Alembic** en este proyecto.

---

## 🌿 Parte 1: Guía de Git (Merges Limpios y Bonitos)

Un historial de commits limpio facilita la depuración, el entendimiento del código a futuro y la integración continua. Aquí tienes las pautas y flujos para lograr integraciones limpias.

### 1.1 ¿Qué es un Merge "Bonito"?
Un merge bonito evita perder el contexto de las ramas en el historial principal (`main` o `develop`). Queremos un historial estructurado que muestre de forma limpia el ciclo de vida de cada rama de características (feature branch).

Para lograr esto en la consola, utilizamos la estrategia de **Merge sin Fast-Forward (`--no-ff`)**:
* **`--no-ff` (No Fast-Forward)**: Obliga a Git a crear siempre un commit de fusión (merge commit) incluso si la rama se podría fusionar de forma directa. Esto mantiene la historia ramificada agrupada visualmente y clara.

---

### 1.2 Flujo de Trabajo Paso a Paso

#### Paso A: Mantén tu rama actualizada con `rebase`
Cuando estés trabajando en tu rama (`feat/modelos`) y quieras incorporar los cambios de `main`, **no uses `git merge main`**. Usa:
```bash
# 1. Cambia a main y descarga lo último
git checkout main
git pull origin main

# 2. Vuelve a tu rama y haz rebase
git checkout feat/modelos
git rebase main
```
> [!NOTE]
> El `rebase` mueve el punto de partida de tu rama al final del `main` actual, eliminando commits de merge innecesarios en tu historial local.

#### Paso B: Integración en la rama principal (`main`) usando `--no-ff`
Cuando tu tarea esté terminada y probada, realiza la integración de la siguiente manera desde la consola:

```bash
# 1. Asegúrate de estar en la rama destino con lo último
git checkout main
git pull origin main

# 2. Realiza el merge sin Fast-Forward especificando el mensaje de fusión
git merge --no-ff feat/modelos -m "Merge branch 'feat/modelos' into main"

# 3. Sube los cambios al repositorio remoto
git push origin main

# 4. (Opcional) Borra tu rama local si ya no la necesitas
git branch -d feat/modelos
```

---

### 1.3 Buenas Prácticas para Mensajes de Commit
Utiliza la convención de **Conventional Commits**:
* **`feat:`** Una nueva característica (ej. `feat: add comment deletion endpoint`).
* **`fix:`** Corrección de un error (ej. `fix: database connection pool recycle time`).
* **`docs:`** Cambios solo en documentación (ej. `docs: update readme with alembic guide`).
* **`refactor:`** Cambios que no corrigen errores ni añaden características (ej. `refactor: optimize recipe service queries`).
* **`chore:`** Tareas de mantenimiento o configuración (ej. `chore: update dependencies in requirements.txt`).

---

### 1.4 Resolución Limpia de Conflictos
Si durante un `git rebase main` encuentras conflictos:
1. Git detendrá el proceso y te dirá qué archivos tienen conflicto.
2. Abre los archivos en VS Code. Verás los marcadores `<<<<<<< HEAD` y `=======`.
3. Selecciona la opción adecuada (Aceptar cambios entrantes, actuales o ambos).
4. Guarda los cambios del archivo en conflicto.
5. Agrega el archivo al área de preparación (stage):
   ```bash
   git add <archivo-con-conflicto>
   ```
6. Continúa el rebase (no hagas `git commit`):
   ```bash
   git rebase --continue
   ```
7. Si en cualquier momento te equivocas o te asustas, puedes abortar el proceso y volver a como estabas antes de iniciar el rebase:
   ```bash
   git rebase --abort
   ```

---

## 🗄️ Parte 2: Sistema de Migraciones con Alembic

**Alembic** es la herramienta que maneja los cambios en la base de datos MySQL de este proyecto utilizando los modelos de SQLAlchemy.

### 2.1 Configuración del Proyecto
* **Archivo de Configuración**: [alembic.ini](file:///c:/Users/ASUS/OneDrive/Desktop/backend-recipes-simone/alembic.ini) define los parámetros generales.
* **Script de Entorno**: [migrations/env.py](file:///c:/Users/ASUS/OneDrive/Desktop/backend-recipes-simone/migrations/env.py) inicializa el motor de base de datos.
  * ⚠️ **Muy importante**: Alembic necesita conocer todos los modelos de base de datos para poder auto-detectar cambios. Estos se importan en [migrations/env.py](file:///c:/Users/ASUS/OneDrive/Desktop/backend-recipes-simone/migrations/env.py#L9-L13). Si creas un nuevo modelo de base de datos en un nuevo archivo dentro de [models/](file:///c:/Users/ASUS/OneDrive/Desktop/backend-recipes-simone/models), **debes importarlo en `env.py`** para que Alembic lo tome en cuenta.

---

### 2.2 Flujo de Trabajo para Crear Migraciones

Cuando modifiques o crees un modelo SQLAlchemy en la carpeta [models/](file:///c:/Users/ASUS/OneDrive/Desktop/backend-recipes-simone/models):

#### Paso 1: Asegura tu entorno virtual y tu base de datos local
Asegúrate de tener el entorno virtual activo, las dependencias de [requirements.txt](file:///c:/Users/ASUS/OneDrive/Desktop/backend-recipes-simone/requirements.txt) instaladas y un archivo [.env](file:///c:/Users/ASUS/OneDrive/Desktop/backend-recipes-simone/.env) configurado con tu `DATABASE_URL` local activa.
```powershell
# Activar entorno virtual en Windows (Powershell)
.venv\Scripts\Activate.ps1
```

#### Paso 2: Generar la migración automáticamente
Ejecuta el comando `revision --autogenerate` con un mensaje descriptivo:
```bash
alembic revision --autogenerate -m "add_column_prep_time_to_recipes"
```
Esto creará un nuevo archivo `.py` dentro de la carpeta `migrations/versions/`.

#### Paso 3: ¡REVISAR LA MIGRACIÓN GENERADA! (Crítico)
> [!WARNING]
> La auto-generación de Alembic **no es infalible**.
> * **Sí detecta**: Tablas nuevas, columnas nuevas, eliminaciones de tablas/columnas, cambios básicos de tipos.
> * **NO detecta automáticamente**: Cambios de nombre de tablas o columnas (lo interpretará como eliminar la vieja y crear una nueva, perdiendo tus datos).
> * **A veces omite**: Restricciones de tipo CHECK, algunas claves externas o índices complejos.
>
> Abre el archivo generado en `migrations/versions/<hash>_add_column_prep_time_to_recipes.py` y revisa las funciones `upgrade()` y `downgrade()` antes de ejecutar nada. Si hay cambios de nombre de columnas, modifícalo manualmente usando `op.alter_column()`.

#### Paso 4: Aplicar la migración a tu base de datos local
Para aplicar los cambios en tu base de datos local actual, ejecuta:
```bash
alembic upgrade head
```
Esto llevará la base de datos a la última versión disponible.

---

### 2.3 Comandos Esenciales de Alembic

| Comando | Descripción |
| :--- | :--- |
| `alembic upgrade head` | Aplica todas las migraciones pendientes hasta la más reciente. |
| `alembic downgrade -1` | Revierte la última migración aplicada (vuelve un paso atrás). |
| `alembic downgrade base` | Revierte absolutamente todas las migraciones aplicadas. |
| `alembic current` | Muestra la versión actual de la base de datos (el hash aplicado). |
| `alembic history --verbose` | Muestra el historial completo de todas las migraciones creadas y su orden. |
| `alembic revision -m "mensaje"` | Crea una migración vacía (para cuando quieres escribir SQL/operaciones manualmente). |

---

### 2.4 Resolución de Problemas Frecuentes

#### 1. Error de "Multiple Heads" (Ramas Divergentes)
Este error ocurre cuando dos personas crearon migraciones al mismo tiempo en ramas diferentes, y ahora al unirlas en `main` hay dos "cabezas" sin un orden claro.
* **Ejemplo de error**: `alembic.util.exc.CommandError: Multiple heads are present; please specify the head revision on which to operate`
* **Solución**: Une ambas ramas en una sola migración de fusión ("merge"):
  ```bash
  alembic merge heads -m "merge branch revisions"
  ```
  Esto creará un nuevo archivo en `migrations/versions/` que unifica los dos caminos. Luego podrás hacer `alembic upgrade head`.

#### 2. Mi migración local no coincide con la base de datos
Si has hecho cambios a mano en la base de datos sin usar Alembic, el estado de autogeneración puede fallar o intentar borrar tablas existentes.
* **Solución**: Intenta mantener tu base de datos local siempre sincronizada únicamente a través de Alembic. Evita crear tablas o columnas directamente en el gestor SQL (como phpMyAdmin, DBeaver o Workbench). Si lo hiciste, añade esas columnas manualmente al modelo SQLAlchemy y crea una migración vacía (`alembic revision -m "sync_db"`) escribiendo a mano los comandos correspondientes.
