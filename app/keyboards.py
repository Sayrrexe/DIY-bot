from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.models import Material, User

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Войти ( автоматически )', callback_data='join_to_account')],
    [InlineKeyboardButton(text='Пропустить ( или настроить позже в настройках )',callback_data='skip')]
])


main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить идею🌟')],
    [KeyboardButton(text='Созать свечу🕯️')],
    [KeyboardButton(text='Создать мыло🧼')]
])

async def materials_kb():
    keyboard = InlineKeyboardBuilder()
    materials = await Material.all()
    callback = 'materials_add' 
    
    i = 0
    for material in materials:
        i += 1
        material = material.name
        only_text_list  = material.split(' ')
        only_text_list.pop(-1)
        if len(only_text_list) > 1:
            finish_text = ':'.join([part for part in only_text_list if part.strip()])
        else:
            finish_text = only_text_list[0]
        keyboard.add(InlineKeyboardButton(text=f'{material}', callback_data=f'{callback}_{finish_text}'))

    if i % 3 == 1:
        keyboard.add(InlineKeyboardButton(text=' ', callback_data='ignore'))
        keyboard.add(InlineKeyboardButton(text=' ', callback_data='ignore'))  
    elif i % 3 == 2:
        keyboard.add(InlineKeyboardButton(text=' ', callback_data='ignore'))
           
        
    keyboard.add(InlineKeyboardButton(text='Сбросить◀️', callback_data='clear_materials'))
    keyboard.add(InlineKeyboardButton(text='🏜️', callback_data='ignore'))
    keyboard.add(InlineKeyboardButton(text='Отмена❌', callback_data='skip'))
    keyboard.add(InlineKeyboardButton(text='Принять ✅', callback_data='accept_materials'))
    return keyboard.adjust(3).as_markup()

async def ideas_kb(ideas):
    keyboard = InlineKeyboardBuilder()
    
    
    for idea in ideas:
        keyboard.row(InlineKeyboardButton(text=idea.description, callback_data=f'idea_{idea.id}'))

    keyboard.row(InlineKeyboardButton(text='Домой🏠', callback_data='skip'), 
                 InlineKeyboardButton(text='Отмена❌', callback_data='clear_materials'))

    
    return keyboard.as_markup()


async def favorites_kb(tg_id, id, status):
    keyboard = InlineKeyboardBuilder()
    
    user = User.get(tg_id=tg_id)
    if user:
        if status:
            keyboard.row(InlineKeyboardButton(text='Добавить в избранное', callback_data=f'favorite_{id}'))
        else:
            keyboard.row(InlineKeyboardButton(text='Удалить из избранного', callback_data=f'unfavorite_{id}'))
    
    keyboard.row(InlineKeyboardButton(text='Домой🏠', callback_data='skip'),
    InlineKeyboardButton(text='Заново🔄️', callback_data='clear_materials'))

    return keyboard.as_markup()
