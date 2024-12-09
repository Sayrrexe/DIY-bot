from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.models import Material, User, Question, Answers

# Главное меню
start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Войти (автоматически) 🔓', callback_data='join_to_account')],
        [InlineKeyboardButton(text='Пропустить (или позже в настройках) ⏭️', callback_data='skip')]
    ]
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Получить идею🌟')],
        [KeyboardButton(text='Создать мыло🧼')],
        [KeyboardButton(text='Профиль🏠')]
    ],
    resize_keyboard=True
)

empty_kb = ReplyKeyboardMarkup(
    keyboard=[],
    resize_keyboard=True
)

async def materials_kb():
    """
    Создает клавиатуру для выбора материалов.
    Каждая кнопка — это материал из базы.
    """
    keyboard = InlineKeyboardBuilder()
    materials = await Material.all()
    callback_prefix = 'materials_add'
    counter = 0

    for material in materials:
        # Разделение текста для формирования callback_data
        counter += 1
        material_name = material.name
        parts = [part.strip() for part in material_name.split(' ') if part.strip()]
        finish_text = ':'.join(parts) if len(parts) > 1 else parts[0]
        keyboard.add(
            InlineKeyboardButton(text=material_name, callback_data=f'{callback_prefix}_{finish_text}')
        )
        
    if counter % 2 == 1:
        keyboard.add(InlineKeyboardButton(text=' ', callback_data='ignore')) 

    # Добавляем функциональные кнопки управления
    keyboard.add(InlineKeyboardButton(text='Сбросить◀️', callback_data='clear_materials'))
    keyboard.add(InlineKeyboardButton(text='Отмена❌', callback_data='skip'))
    keyboard.add(InlineKeyboardButton(text='Принять ✅', callback_data='accept_materials'))

    # Выравнивание по 3 столбца
    return keyboard.adjust(2).as_markup()

async def ideas_kb(ideas):
    """
    Создает клавиатуру для выбора конкретной поделки (идеи).
    Каждая идея — отдельная кнопка.
    """
    keyboard = InlineKeyboardBuilder()
    for idea in ideas:
        keyboard.row(
            InlineKeyboardButton(text=idea.description, callback_data=f'idea_{idea.id}')
        )

    # Кнопки навигации
    keyboard.row(
        InlineKeyboardButton(text='Домой🏠', callback_data='skip'),
        InlineKeyboardButton(text='Отмена❌', callback_data='clear_materials')
    )

    return keyboard.as_markup()

async def favorites_kb(tg_id, idea_id, status):
    """
    Создает клавиатуру для добавления/удаления идеи в избранное, 
    а также возвращения в главное меню.
    """
    keyboard = InlineKeyboardBuilder()
    user = await User.filter(tg_id=tg_id).first()

    if user:
        if status:
            keyboard.row(InlineKeyboardButton(text='Добавить в избранное ⭐', callback_data=f'favorite_{idea_id}'))
        else:
            keyboard.row(InlineKeyboardButton(text='Удалить из избранного ❌⭐', callback_data=f'unfavorite_{idea_id}'))

    # Кнопки навигации
    keyboard.row(
        InlineKeyboardButton(text='Домой🏠', callback_data='skip'),
        InlineKeyboardButton(text='Заново🔄️', callback_data='clear_materials')
    )

    return keyboard.as_markup()

async def get_cb_by_status_questions(status):
    keyboard = InlineKeyboardBuilder()
    
    
    if status == 'color':
        question = await Question.get(id=2).prefetch_related('answers')
        related_answers = await question.answers.all()
        id = 1
    if status == 'form':
        question = await Question.get(id=1).prefetch_related('answers')
        related_answers = await question.answers.all()
        id = 2
    if status == 'additives':
        question = await Question.get(id=3).prefetch_related('answers')
        related_answers = await question.answers.all()
        id = 3
    
    for answer in related_answers:
        keyboard.row(InlineKeyboardButton(text=answer.answer, callback_data=f'answer_{id}_{answer.id}'))
        
    return keyboard.as_markup()
        