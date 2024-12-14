import os
import shutil

# Recorrer las aplicaciones y eliminar las migraciones excepto __init__.py
apps = ['accounts', 'transactions', 'inventory', 'reports', 'usuarios']

for app in apps:
    migrations_path = os.path.join(app, 'migrations')
    if os.path.exists(migrations_path):
        for file in os.listdir(migrations_path):
            file_path = os.path.join(migrations_path, file)
            if file != '__init__.py':
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except PermissionError as e:
                    print(f"Error al eliminar {file_path}: {e}")

print("Archivos de migraciones eliminados.")
