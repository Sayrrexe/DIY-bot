from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.models import Favorite,Material, User, Question

# Главное меню
start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Войти (автоматически) 🔓", callback_data="join_to_account"
            )
        ],
        [
            InlineKeyboardButton(
                text="Пропустить (или позже в настройках) ⏭️", callback_data="skip"
            )
        ],
    ]
)

auth_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Авторизоваться 🔓", callback_data="join_to_account"
            )
        ],
        [InlineKeyboardButton(text="Назад ⏭️", callback_data="skip")],
    ]
)

delete_account_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Удалить ❌", callback_data="submit_delete_account"
            )
        ],
        [InlineKeyboardButton(text="Назад ⏭️", callback_data="skip")],
    ]
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить идею 🌟")],
        [KeyboardButton(text="Создать мыло 🧼")],
        [KeyboardButton(text="Профиль 🏠")],
    ],
    resize_keyboard=True,
)

empty_kb = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)


async def profile_kb(tg_id: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру профиля с избранным идеями.
    """
    keyboard = InlineKeyboardBuilder()
    user = await User.get(tg_id=tg_id)
    list_favorite = await Favorite.filter(user=user).all()
    for favorite in list_favorite:
        idea = await favorite.idea
        keyboard.add(
            InlineKeyboardButton(text=idea.description, callback_data=f"idea_{idea.id}")
        )

    keyboard.add(InlineKeyboardButton(text="Домой 🏠", callback_data="skip"))
    keyboard.add(
        InlineKeyboardButton(
            text="Удалить мой аккаунт ❌", callback_data="delete_account"
        )
    )
    return keyboard.adjust(1).as_markup()


async def materials_kb() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора материалов.
    Каждая кнопка — это материал из базы.
    """
    keyboard = InlineKeyboardBuilder()
    materials = await Material.all()
    callback_prefix = "materials_add"
    counter = 0

    for material in materials:
        counter += 1
        material_name = material.name
        parts = [part.strip() for part in material_name.split(" ") if part.strip()]
        finish_text = ":".join(parts) if len(parts) > 1 else parts[0]
        keyboard.add(
            InlineKeyboardButton(
                text=material_name, callback_data=f"{callback_prefix}_{finish_text}"
            )
        )

    # Добавляем "заглушку" для выравнивания, если нечетное кол-во кнопок
    if counter % 2 == 1:
        keyboard.add(InlineKeyboardButton(text=" ", callback_data="ignore"))

    # Функциональные кнопки управления
    keyboard.add(
        InlineKeyboardButton(text="Сбросить ◀️", callback_data="clear_materials")
    )
    keyboard.add(InlineKeyboardButton(text="Отмена ❌", callback_data="skip"))
    keyboard.add(
        InlineKeyboardButton(text="Принять ✅", callback_data="accept_materials")
    )

    return keyboard.adjust(2).as_markup()


async def ideas_kb(ideas) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора конкретной идеи.
    """
    keyboard = InlineKeyboardBuilder()
    for idea in ideas:
        keyboard.row(
            InlineKeyboardButton(text=idea.description, callback_data=f"idea_{idea.id}")
        )

    # Кнопки навигации
    keyboard.row(
        InlineKeyboardButton(text="Домой 🏠", callback_data="skip"),
        InlineKeyboardButton(text="Отмена ❌", callback_data="clear_materials"),
    )

    return keyboard.as_markup()


async def favorites_kb(tg_id: int, idea_id: int, status: bool) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для добавления/удаления идеи в избранное,
    а также возвращения в главное меню.
    """
    keyboard = InlineKeyboardBuilder()
    user = await User.filter(tg_id=tg_id).first()

    if user:
        if not status:
            keyboard.row(
                InlineKeyboardButton(
                    text="Добавить в избранное ⭐", callback_data=f"favorite_{idea_id}"
                )
            )
        else:
            keyboard.row(
                InlineKeyboardButton(
                    text="Удалить из избранного ❌⭐",
                    callback_data=f"unfavorite_{idea_id}",
                )
            )

    # Кнопки навигации
    keyboard.row(
        InlineKeyboardButton(text="Домой 🏠", callback_data="skip"),
        InlineKeyboardButton(text="Заново 🔄️", callback_data="clear_materials"),
    )

    return keyboard.as_markup()


async def get_cb_by_status_questions(status: str) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру в зависимости от статуса вопроса.
    """
    keyboard = InlineKeyboardBuilder()

    if status == "color":
        question = await Question.get(id=2).prefetch_related("answers")
        related_answers = await question.answers.all()
        question_id = 1
    elif status == "form":
        question = await Question.get(id=1).prefetch_related("answers")
        related_answers = await question.answers.all()
        question_id = 2
    elif status == "additives":
        question = await Question.get(id=3).prefetch_related("answers")
        related_answers = await question.answers.all()
        question_id = 3
    else:
        related_answers = []
        question_id = None

    for answer in related_answers:
        keyboard.row(
            InlineKeyboardButton(
                text=answer.answer, callback_data=f"answer_{question_id}_{answer.id}"
            )
        )

    return keyboard.as_markup()
