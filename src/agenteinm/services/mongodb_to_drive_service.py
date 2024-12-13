import os
import json
import pickle
from pymongo import MongoClient
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuraciones
MONGODB_URI = os.getenv("MONGODB_URI")
METADATA_FILE = "mongodb_metadata.json"
ROOT_FOLDER_ID = '1KAm5k2Jg7zsOmY3k8xhzxo0ZKnE_tUWm'
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')  # Ruta local

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]


def get_google_drive_service():
    """Autentica y devuelve un cliente de Google Drive."""
    creds = None

    # Verificar si existe token.pickle (credenciales guardadas)
    token_path = os.path.join(os.path.dirname(__file__), "token.pickle")
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # Si no hay credenciales válidas, autenticarse manualmente
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"❌ No se encontró 'credentials.json' en: {CREDENTIALS_FILE}")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)

        # Guardar token para reutilización
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("drive", "v3", credentials=creds)


def connect_mongodb():
    """Establece la conexión con MongoDB."""
    try:
        client = MongoClient(MONGODB_URI)
        db = client["agenteinm"]  # Base de datos específica
        print("✅ Conexión a MongoDB exitosa: Base de datos 'agenteinm'")
        return db
    except Exception as e:
        print(f"❌ Error al conectar con MongoDB: {e}")
        return None


def extract_metadata(db):
    """Extrae los metadatos de la colección 'reports'."""
    try:
        collection = db["reports"]
        documents = list(collection.find({}, {"_id": 0}))
        for doc in documents:
            for key, value in doc.items():
                if isinstance(value, datetime):
                    doc[key] = value.isoformat()
        return documents
    except Exception as e:
        print(f"❌ Error al extraer metadatos: {e}")
        return None


def save_metadata_to_file(metadata, file_name):
    """Guarda los metadatos en un archivo JSON."""
    try:
        with open(file_name, "w") as file:
            json.dump(metadata, file, indent=4)
        print(f"✅ Metadatos guardados en {file_name}")
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")


def upload_to_google_drive(file_path, folder_id=ROOT_FOLDER_ID):
    """Sube un archivo JSON a Google Drive."""
    try:
        service = get_google_drive_service()
        file_metadata = {
            "name": os.path.basename(file_path),
            "parents": [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype="application/json")
        uploaded_file = service.files().create(
            body=file_metadata, media_body=media, fields="id, webViewLink"
        ).execute()
        print(f"✅ Archivo subido exitosamente a Google Drive: {uploaded_file.get('webViewLink')}")
    except Exception as e:
        print(f"❌ Error al subir el archivo a Google Drive: {e}")
