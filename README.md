Instalación de dependencias para el Asistente de Voz
Requisitos previos

Python 3.7 o superior
Pip (gestor de paquetes de Python)
Micrófono funcional

Instalación de dependencias
1. Instalar las bibliotecas principales
bashpip install SpeechRecognition
pip install PyAudio
pip install PyQt5
pip install requests
pip install beautifulsoup4
2. Dependencias específicas por sistema operativo
Windows
bash# No se requieren dependencias adicionales específicas para Windows
macOS
bash# Si hay problemas con PyAudio en macOS
brew install portaudio
pip install PyAudio
Linux (Ubuntu/Debian)
bash# Dependencias para reconocimiento de voz
sudo apt-get update
sudo apt-get install python3-pyaudio
sudo apt-get install portaudio19-dev
sudo apt-get install flac
3. Verificar la instalación
Para verificar que todas las dependencias están correctamente instaladas:
bashpython -c "import speech_recognition, pyaudio, PyQt5, requests, bs4"
Si no aparece ningún error, todas las bibliotecas se han instalado correctamente.
Ejecución del asistente
Para ejecutar el asistente de voz, guarda el código en un archivo llamado asistente.py y ejecuta:
bashpython asistente.py
Solución de problemas comunes
Error con PyAudio
Si encuentras errores al instalar PyAudio, prueba estos comandos alternativos:
Windows:
bashpip install pipwin
pipwin install pyaudio
macOS:
bash# Usando Homebrew
brew install portaudio
pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
Error con SpeechRecognition
Asegúrate de tener un micrófono configurado correctamente y que tu sistema tenga acceso a internet para utilizar el reconocimiento de voz.
Error con PyQt5
Si PyQt5 falla durante la instalación:
bash# Alternativa para PyQt5
pip install PySide2
Y luego modifica las importaciones en el código para usar PySide2.
