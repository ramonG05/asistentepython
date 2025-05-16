import speech_recognition as sr
import subprocess
import webbrowser
import os
import re
import platform
import requests
from bs4 import BeautifulSoup

class AsistenteVoz:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sistema = platform.system()  # Detecta el sistema operativo
        
    def escuchar(self):
        """Escucha el micrófono y devuelve el texto reconocido"""
        with sr.Microphone() as source:
            print("Escuchando...")
            # Ajustar para ruido ambiental
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)
            
        try:
            texto = self.recognizer.recognize_google(audio, language="es-ES")
            print(f"Has dicho: {texto}")
            return texto.lower()
        except sr.UnknownValueError:
            print("No pude entender lo que dijiste")
            return ""
        except sr.RequestError:
            print("No pude conectarme al servicio de reconocimiento")
            return ""
    
    def abrir_aplicacion(self, nombre_app):
        """Abre una aplicación según el sistema operativo"""
        try:
            if self.sistema == "Windows":
                # Lista de aplicaciones comunes y sus rutas/comandos en Windows
                apps = {
                    "brave": "brave.exe",
                    "navegador": "brave.exe",
                    "chrome": "chrome.exe",
                    "firefox": "firefox.exe",
                    "word": "winword.exe",
                    "excel": "excel.exe",
                    "bloc de notas": "notepad.exe",
                    "notepad": "notepad.exe",
                    "calculadora": "calc.exe",
                    "explorador de archivos": "explorer.exe",
                }
                
                if nombre_app.lower() in apps:
                    subprocess.Popen(apps[nombre_app.lower()])
                    return True
                else:
                    # Intenta ejecutar el nombre directamente
                    subprocess.Popen(nombre_app)
                    return True
                    
            elif self.sistema == "Darwin":  # macOS
                apps = {
                    "brave": "Brave Browser",
                    "navegador": "Brave Browser",
                    "chrome": "Google Chrome",
                    "safari": "Safari",
                    "firefox": "Firefox",
                    "word": "Microsoft Word",
                    "excel": "Microsoft Excel",
                    "notas": "Notes",
                    "calculadora": "Calculator",
                    "finder": "Finder",
                }
                
                if nombre_app.lower() in apps:
                    subprocess.Popen(["open", "-a", apps[nombre_app.lower()]])
                    return True
                else:
                    # Intenta abrir directamente
                    subprocess.Popen(["open", "-a", nombre_app])
                    return True
                    
            elif self.sistema == "Linux":
                # En Linux, simplemente intenta ejecutar el comando
                subprocess.Popen([nombre_app])
                return True
                
            return False
        except Exception as e:
            print(f"Error al abrir la aplicación: {e}")
            return False
    
    def reproducir_musica(self, cancion):
        """Abre Brave y reproduce la primera canción encontrada en YouTube"""
        # Necesitamos las bibliotecas para obtener el HTML y extraer la URL del video
        import requests
        from bs4 import BeautifulSoup
        
        query = cancion.replace(" ", "+")
        search_url = f"https://www.youtube.com/results?search_query={query}"
        
        try:
            # Obtenemos la página de resultados
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos el ID del primer video en los resultados
            # Esto es un poco complejo porque YouTube usa JavaScript para cargar resultados
            scripts = soup.find_all('script')
            video_id = None
            
            for script in scripts:
                if script.string and 'var ytInitialData' in script.string:
                    # Buscamos el primer videoId en el script
                    match = re.search(r'videoId":"([^"]+)"', script.string)
                    if match:
                        video_id = match.group(1)
                        break
            
            if video_id:
                # Formamos la URL directa del video
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                # Abrimos Brave
                self.abrir_aplicacion("brave")
                
                # Abrimos el video directamente
                webbrowser.open(video_url)
                print(f"Reproduciendo el video: {video_url}")
                return True
            else:
                # Si no encontramos video_id, caemos al método anterior
                print("No se pudo encontrar el ID del video, abriendo búsqueda general...")
                self.abrir_aplicacion("brave")
                webbrowser.open(search_url)
                return True
                
        except Exception as e:
            print(f"Error al buscar la canción: {e}")
            # En caso de error, abrimos la búsqueda general
            self.abrir_aplicacion("brave")
            webbrowser.open(search_url)
            return True
    
    def procesar_comando(self, comando):
        """Procesa el comando de voz y ejecuta la acción correspondiente"""
        # Comando para abrir aplicaciones
        if re.search(r"(abrir|abre|ejecuta|ejecutar|inicia|iniciar)\s+(\w+)", comando):
            match = re.search(r"(abrir|abre|ejecuta|ejecutar|inicia|iniciar)\s+(.+)", comando)
            if match:
                app_name = match.group(2).strip()
                print(f"Intentando abrir: {app_name}")
                self.abrir_aplicacion(app_name)
                return f"Abriendo {app_name}"
        
        # Comando para reproducir música
        elif re.search(r"(reproducir|reproduce|pon|poner|escuchar|tocar)\s+(.+)", comando):
            match = re.search(r"(reproducir|reproduce|pon|poner|escuchar|tocar)\s+(.+)", comando)
            if match:
                cancion = match.group(2).strip()
                print(f"Buscando música: {cancion}")
                self.reproducir_musica(cancion)
                return f"Reproduciendo {cancion}"
                
                    
        
        # Comando para buscar archivos (básico, se puede mejorar después)
        elif re.search(r"(buscar|busca|encuentra|encontrar)\s+archivo[s]?\s+(.+)", comando):
            match = re.search(r"(buscar|busca|encuentra|encontrar)\s+archivo[s]?\s+(.+)", comando)
            if match:
                archivo = match.group(2).strip()
                return f"La búsqueda de archivos se implementará en una versión futura."
        
        # Comando de ayuda
        elif re.search(r"(ayuda|ayúdame|qué puedes hacer|funciones)", comando):
            return "Puedo abrir aplicaciones diciendo 'abrir [nombre]' y reproducir música diciendo 'reproducir [canción]'."
        
        # Comando para salir
        elif re.search(r"(salir|terminar|finalizar|adiós)", comando):
            return "salir"
        
        else:
            return "No entendí ese comando. Prueba decir 'ayuda' para ver lo que puedo hacer."

def main():
    asistente = AsistenteVoz()
    print("¡Hola! dime qlq quieres mano?.")
    print("Puedes pedirme que abra aplicaciones o reproduzca música.")
    print("Di 'ayuda' para más información o 'salir' para terminar.")
    
    while True:
        comando = asistente.escuchar()
        if not comando:
            continue
            
        respuesta = asistente.procesar_comando(comando)
        print(respuesta)
        
        if respuesta == "salir":
            print("¡Hasta pronto!")
            break

if __name__ == "__main__":
    main()