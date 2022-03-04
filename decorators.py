from telegram.ext import CommandHandler


def command(bot, command_name):
    def decorator(func):
        handler = CommandHandler(command_name, func)
        bot.dispatcher.add_handler(handler)
        return func
    return decorator