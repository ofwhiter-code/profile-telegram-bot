#Брал инструменты из телеграмма
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler

#переменные, чтобы работали по порядку, хз
NAME = 0
AGE = 1
CITY = 2
CONFIRM = 3
EDIT_CHOICE = 4
EDIT_NAME = 5
EDIT_AGE = 6
EDIT_CITY = 7


#Команда старт, которая начинает заполнение анкеты
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name= update.effective_user.first_name
    await update.message.reply_text(f"Hello,{user_name}!\nI'm a profile bot! Lets's fill out your profile!\nSend your name.For help write /help.")
    return NAME

#Имя) А также после него выбор на age, чтобы age не хватал все слова подряд, а только цифру
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    keyboard = [
        [InlineKeyboardButton("14-17", callback_data="14-17"),
         InlineKeyboardButton("18-25", callback_data="18-25")],
         [InlineKeyboardButton("26-35", callback_data="26-35"),
          InlineKeyboardButton("36+", callback_data="36+")]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your age:", reply_markup=reply_markup)
    #возращаем после ответа к age
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["age"] = query.data
    #после выбора от отвечает, что возраст:такой то такой то.
    await query.edit_message_text(f"Age: {query.data}✅")
    await query.message.reply_text("Now send your city:")
    return CITY

#Город, так как это окончательный пункт для заполнения профиля, потом дает выбор,создавать ли профиль с выбором ответа да или нет и развязками
async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    keyboard = [
    [
        InlineKeyboardButton("Yes", callback_data="yes"),
        InlineKeyboardButton("No", callback_data="no")
    ]
]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Create profile?", reply_markup=reply_markup)
    return CONFIRM

#Выбор создавать ли вообще профиль, есть кнопки да или нет
async def confirm(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    await query.edit_message_reply_markup(reply_markup=None)
    
    if query.data == "yes":
        name = context.user_data.get("name")
        age = context.user_data.get("age")
        city = context.user_data.get("city")
        await query.message.reply_text(f"👤Your profile!:\n{name},\n{age} years old,\nliving in {city},\nWrite /profile anytime!")
    else:
        await query.message.reply_text("Ok! Profile creation cancelled. Write /start if you want to try again.")
    return ConversationHandler.END 


#Команду хелп сделал епта
async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start-for start bot\n/help-for all commands\n/profile-open a profile")


#Сделал сам профиль, а также если нету данных что ему тоже писать. Как будет готов профиль, то он отправит данные а также кнопки с выбором изменить или удалить профиль
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data.get("name", "не указано")
    age = context.user_data.get("age", "не указано")
    city = context.user_data.get("city", "не указано")
    
    keyboard = [
        [InlineKeyboardButton("Edit profile✏️", callback_data="edit"),
        InlineKeyboardButton("Delete Profile🗑️", callback_data="delete")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"{name},\n{age},years old,\nliving in {city}",reply_markup=reply_markup)

#Сделал развилки от выбора кнопки в изменении профиля 
async def profile_actions(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "edit":
        keyboard = [
            [InlineKeyboardButton("📝Name", callback_data="edit_name")],
            [InlineKeyboardButton("🎂Age", callback_data="edit_age")],
            [InlineKeyboardButton("🌍City", callback_data="edit_city")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("What do you want to edit?", reply_markup=reply_markup)
        return EDIT_CHOICE
    
    elif query.data == "delete":
        context.user_data.clear()
        await query.edit_message_text("🗑️Profile deleted! Write /start to create new one")
        return ConversationHandler.END

#Изменение профиля
async def edit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "edit_name":
        await query.edit_message_text("Send your name:")
        return EDIT_NAME
    elif query.data == "edit_age":
        keyboard = [
            [InlineKeyboardButton("14-17", callback_data="14-17"),
         InlineKeyboardButton("18-25", callback_data="18-25")],
         [InlineKeyboardButton("26-35", callback_data="26-35"),
          InlineKeyboardButton("36+", callback_data="36+")]

        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Choose your age:", reply_markup=reply_markup)
        return EDIT_AGE
    elif query.data == "edit_city":
        await query.edit_message_text("Send new city:")
        return EDIT_CITY
    
#Функции для изменения профиля
async def save_edit_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("✅Name updated! Write /profile to see.")
    return ConversationHandler.END
async def save_edit_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["age"] = query.data
    await query.edit_message_text(f"✅Age updated: {query.data}")
    return ConversationHandler.END

async def save_edit_sity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text("✅City updated! Write /profile to see")
    return ConversationHandler.END



#Шаги а также команды
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start),
                  CommandHandler("help", help_command),
                  CallbackQueryHandler(profile_actions, pattern="^(edit|delete)$")],
    states={
        NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_name)],
        AGE: [CallbackQueryHandler(get_age)],
        CITY: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_city)],
        CONFIRM: [CallbackQueryHandler(confirm)],
        EDIT_CHOICE: [CallbackQueryHandler(edit_choice)],
        EDIT_NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), save_edit_name)],
        EDIT_AGE: [CallbackQueryHandler(save_edit_age)],
        EDIT_CITY: [MessageHandler(filters.TEXT & (~filters.COMMAND), save_edit_sity)],
    },
    fallbacks=[CommandHandler("help", help_command),
               CommandHandler("start",start)]
)
#Тут писал, команду профиль, создавал бота самого, а также чтобы edit и delete не мешались с ответом yes go да и тд.
app = Application.builder().token("8868895970:AAHgMID1UFNmM1rAVfIcc5OwnRyz-Od3OOc").build()
app.add_handler(conv_handler)
print("BOT ZAPUSHEN")
app.add_handler(CommandHandler("profile", profile))
app.run_polling()
