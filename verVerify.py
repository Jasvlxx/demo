import subprocess

# Lista de paquetes
paquetes = [
    "crewai", "crewai-tools", "langchain", "openai", "langchain-openai",
    "pydantic", "PyYAML", "dnspython", "python-dotenv", "pymongo",
    "google-api-python-client", "google-auth", "google-auth-oauthlib",
    "google-auth-httplib2", "requests", "colorama", "pytest", "black", "flake8"
]

# Iterar y mostrar la versión de cada paquete
for paquete in paquetes:
    try:
        resultado = subprocess.check_output(f"pip show {paquete}", shell=True, text=True)
        for linea in resultado.splitlines():
            if linea.startswith("Version:"):
                print(f"{paquete}=={linea.split(' ')[1]}")
    except subprocess.CalledProcessError:
        print(f"No se pudo encontrar la versión de {paquete}")
