#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import os
from dotenv import load_dotenv
from crew import Agenteinm
from services.mongodb_to_drive_service import (
    connect_mongodb,
    extract_metadata,
    save_metadata_to_file,
    upload_to_google_drive
)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Cargar variables de entorno
load_dotenv()

def run():
    """
    Ejecuta el crew inmobiliario con estructura jerárquica.
    También extrae metadatos de MongoDB y los guarda en Google Drive automáticamente.
    """
    inputs = {
        'zona': 'Santiago Centro',
        'fecha': datetime.now().strftime("%Y-%m-%d"),
        'tipo_propiedad': 'Residencial',
        'presupuesto_min': '1000 UF',
        'presupuesto_max': '5000 UF'
    }
    
    print("\nIniciando análisis inmobiliario...")
    print(f"Zona: {inputs['zona']}")
    print(f"Fecha: {inputs['fecha']}")
    print(f"Tipo de Propiedad: {inputs['tipo_propiedad']}")
    print(f"Rango de Presupuesto: {inputs['presupuesto_min']} - {inputs['presupuesto_max']}\n")
    
    # Ejecutar crew inmobiliario
    crew = Agenteinm().crew()
    results = crew.kickoff(inputs=inputs)

    reports_dir = f"reports/{datetime.now().strftime('%Y-%m-%d')}"
    print("\nAnálisis completado!")
    print(f"Reportes generados en: {reports_dir}/")
    print("- market_analysis_[timestamp].md: Análisis de mercado del CEO Virtual")
    print("- legal_review_[timestamp].md: Análisis legal del Abogado")
    print("- coordination_report_[timestamp].md: Reporte integrado del Task Manager")
    
    # Iniciar extracción y subida de metadatos
    print("\nIniciando extracción y guardado de metadatos en Google Drive...")
    db = connect_mongodb()
    if db is not None:  # Validar conexión
        metadata = extract_metadata(db)
        if metadata:
            save_metadata_to_file(metadata, "mongodb_metadata.json")
            upload_to_google_drive("mongodb_metadata.json")
        else:
            print("❌ No se pudieron extraer metadatos.")
    else:
        print("❌ No se pudo conectar a la base de datos.")
    
    print("\nTarea de metadatos completada con éxito.")
    return results

def train():
    """
    Entrena el crew para mejorar la coordinación y respuestas.
    """
    inputs = {
        'zona': 'Santiago Centro',
        'fecha': datetime.now().strftime("%Y-%m-%d"),
        'tipo_propiedad': 'Residencial',
        'presupuesto_min': '1000 UF',
        'presupuesto_max': '5000 UF'
    }
    try:
        Agenteinm().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Error durante el entrenamiento: {e}")

def replay():
    """
    Reproduce una ejecución específica del crew.
    """
    try:
        Agenteinm().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"Error durante la reproducción: {e}")

def test():
    """
    Prueba el crew con diferentes configuraciones.
    """
    inputs = {
        'zona': 'Santiago Centro',
        'fecha': datetime.now().strftime("%Y-%m-%d"),
        'tipo_propiedad': 'Residencial',
        'presupuesto_min': '1000 UF',
        'presupuesto_max': '5000 UF'
    }
    try:
        Agenteinm().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Error durante las pruebas: {e}")

if __name__ == "__main__":
    run()
