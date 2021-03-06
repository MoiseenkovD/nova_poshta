from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler

from decorators import command
from configs import configs

import helpers

bot = Updater(token=configs['TOKEN'], use_context=True)

@command(bot, 'start')
def start(update: Update, context: CallbackContext):
    np_df = helpers.get_schedule_df()

    regions = list(np_df.sort_values(by='Область')['Область'].unique())

    regions_buttons = []

    for region in regions:
        regions_buttons.append(InlineKeyboardButton(str(region), callback_data=f'set_region:{region}'))

    regions_keyboard = InlineKeyboardMarkup(helpers.chunks(regions_buttons, 2))

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='У якій області ви проживаєте?',
        reply_markup=regions_keyboard
    )


def button(update: Update, context: CallbackContext):
    np_df = helpers.get_schedule_df()

    query = update.callback_query

    query.answer()

    action, *payload = query.data.split(':')

    if action == 'set_region':
        cities = helpers.get_cities_in_region(np_df, payload[0])
        city_buttons = []

        for i, city in enumerate(cities):
            city_buttons.append(InlineKeyboardButton(str(city), callback_data=f'set_city:{payload[0]}:{i}'))

        city_keyboard = InlineKeyboardMarkup(helpers.chunks(city_buttons, 3))

        query.edit_message_text(text=f"✅ Обрана область: {payload[0]}")

        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text=f"Оберіть ваше місто:",
            reply_markup=city_keyboard
        )

    elif action == 'set_city':
        region = payload[0]

        cities = helpers.get_cities_in_region(np_df, region)
        city = cities[int(payload[1])]

        query.edit_message_text(text=f"✅ Обране місто: {city}")

        locations = np_df[(np_df['Область'] == region) & (np_df['Місто'] == city)]

        location_work = []

        for location in locations.values:
            number = location[2]
            address = location[3]
            department_type = location[4]
            weekday = location[5]
            saturday = location[6]
            sunday = location[7]

            location_work.append(f'<strong>НП№{number}</strong>\n'
                                 f'📍{address} ({department_type})\n'
                                 f'<strong>ПН-ПТ:</strong> {weekday}\n'
                                 f'<strong>СБ:</strong> {saturday}\n'
                                 f'<strong>ВС:</strong> {sunday}\n'
                                 )

        location_work_str = '\n'.join(location_work)

        if len(location_work_str) > 4095:
            for x in range(0, len(location_work_str), 4095):
                context.bot.send_message(
                    chat_id=update.callback_query.from_user.id,
                    text=location_work_str[x:x + 4095],
                    parse_mode=ParseMode.HTML
                )
        else:
            context.bot.send_message(
                chat_id=update.callback_query.from_user.id,
                text=f'{location_work_str}',
                parse_mode=ParseMode.HTML
            )


bot.start_polling()


def main():
    button_handler = CallbackQueryHandler(button)
    bot.dispatcher.add_handler(button_handler)


if __name__ == '__main__':
    main()
