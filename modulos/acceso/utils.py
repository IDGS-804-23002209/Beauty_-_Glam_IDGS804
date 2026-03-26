from datetime import datetime
from flask import request
# from app import bitacora_db 

def registrar_auditoria(usuario, accion, resultado="Exitoso"):
    log = {
        "usuario": usuario,
        "accion": accion,
        "resultado": resultado,
        "ip": request.remote_addr,
        "dispositivo": request.user_agent.string,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # bitacora_db.bitacora.insert_one(log)
    print(f"LOG MONGODB: {log}") # Para que lo veas en consola mientras pruebas