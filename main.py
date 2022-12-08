# pip install python-telegram-bot
from telegram.ext import *
import random
import keys
from datetime import datetime

print('Starting up bot...')


# Lets us use the /start command
def start_command(update, context):
    update.message.reply_text('Hello there! I\'m a bot. What\'s up?')


# Lets us use the /help command
def help_command(update, context):
    # List of all the replies
    l = ['["hello", "hi", "sup", "yo", "whatsup"]', '["who are you", "who are you?"]', '["time", "time?"]', '["roll", "number", "random"]']
    update.message.reply_text("Here are the commands I can respond to: " + str(l))


# Lets us use the /roll command
def roll_command(update, context):
    update.message.reply_text(random.randrange(1000))
    

def check(a):
    count = 0
    for i in range(len(a)):
        if not(a[i].isdigit()):
            count += 1
        else:
            return count
    return count


def handle_response(text) -> str:
    # Create your own response logic
    
    text = text.lower()
    if text in ["hello", "hi", "sup", "yo", "whatsup"]:
        return 'Hey there!'

    if 'how are you' in text:
        return 'I\'m good! what about you?'
    
    if text in ["who are you", "who are you?"]:
        return "I am a bot created by Mohamed!"

    if text in ["time", "time?"]:
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")

        return str(date_time)
    
    a = check(text)
    n = ["roll", "number", "random"]
    if text[:a - 1] in l or text[:a] in l:    
        if text[a:]:
            return random.randrange(int(text[check(text):]))
        else:
            return random.randrange(1000)
        
    return "Idk what you are trying to say."


def handle_message(update, context):
    # Get basic info of the incoming message
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{text}" in: {message_type}')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if '@Your Bot UserName' in text:
            new_text = text.replace('@Your Bot UserName', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    # Reply normal if the message is in private
    update.message.reply_text(response)


# Log errors
def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    updater = Updater(keys.token, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('roll', roll_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()