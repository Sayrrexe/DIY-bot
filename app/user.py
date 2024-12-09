import logging
import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.states as st
import app.database.requests as req
from app.utils import clear_text

logger = logging.getLogger(__name__)
user = Router()

# --- Command Handlers ---

@user.message(Command('id'))
async def cmd_id(message: Message):
    """Sends the user ID."""
    user_id = message.from_user.id
    await message.answer(
        f"Ваш уникальный ID: `{user_id}` 🔑", 
        reply_markup=kb.main_kb,
        parse_mode='MARKDOWN'
    )

@user.message(CommandStart())
async def cmd_start(message: Message):
    """Sends a welcome message."""
    await message.answer(
        "Добро пожаловать в бот! 🤖🎉"

        "Узнайте список всех команд с помощью /help 📜\n"
        "Используйте кнопки меню для быстрого взаимодействия 🚀\n"
        "Хотите войти в аккаунт для синхронизации избранных поделок?",
        reply_markup=kb.start_kb
    )

# --- Authorization Handlers ---

@user.callback_query(F.data == 'join_to_account')
async def join_to_account(callback: CallbackQuery):
    """Handles user authorization."""
    await req.create_user(callback.from_user.id)
    await callback.message.answer(
        'Вы успешно вошли в аккаунт! 🔓🔥', 
        reply_markup=kb.main_kb
    )

@user.callback_query(F.data == 'skip')
async def skip_cmd(callback: CallbackQuery, state: FSMContext):
    """Skips authorization."""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        'Вы находитесь в главном меню 🏠! Используйте кнопки ниже для взаимодействия.', 
        reply_markup=kb.main_kb
    )

# --- Idea Handlers ---

@user.message(F.text == 'Получить идею🌟')
async def cmd_get_idea(message: Message, state: FSMContext):
    """Starts the material selection process."""
    await message.delete()
    await state.update_data(materials=[])
    await message.answer(
        "Из списка ниже выберите материалы 🧩:\n\n• ",
        reply_markup=await kb.materials_kb()
    )

@user.callback_query(F.data == 'clear_materials')
async def cmd_clear_materials(callback: CallbackQuery, state: FSMContext):
    """Clears the material list."""
    await callback.message.delete()
    await state.update_data(materials=[])
    await callback.message.answer(
        "Из списка ниже выберите материалы 🧩:\n\n• ",
        reply_markup=await kb.materials_kb()
    )

@user.callback_query(F.data.startswith("materials_add_"))
async def cmd_add_material(callback: CallbackQuery, state: FSMContext):
    """Adds/removes materials from the list."""
    material = callback.data.split("_")[-1]
    user_data = await state.get_data()
    materials = user_data.get('materials', [])

    new_text, new_materials, edited = await clear_text(material, materials)
    if edited:
        await state.update_data(materials=new_materials)
        await callback.message.edit_text(
            text=f"Материал обновлён: {new_text} 🛠️", 
            reply_markup=await kb.materials_kb()
        )

@user.callback_query(F.data == 'accept_materials')
async def cmd_accept_materials(callback: CallbackQuery, state: FSMContext):
    """Accepts selected materials and suggests ideas."""
    await callback.message.delete()
    user_data = await state.get_data()
    materials = user_data.get('materials', [])
    ideas = await req.find_best_matching_ideas(materials)
    await callback.message.answer(
        'Подберите Поделку из наших рекомендаций 🎨✨:',
        reply_markup=await kb.ideas_kb(ideas)
    )

@user.callback_query(F.data.startswith("idea_"))
async def cmd_show_idea(callback: CallbackQuery, state: FSMContext):
    """Displays the selected idea with a photo and text."""
    idea_id = callback.data.split("_")[1]
    text, image_path = await req.revert_idea_to_text(idea_id)
    status = await req.is_idea_favorite(callback.from_user.id, idea_id)

    if image_path and os.path.exists(image_path):
        try:
            await callback.message.answer_photo(
                photo=FSInputFile(image_path, filename="idea_image.png"), 
                caption=text,
                reply_markup=await kb.favorites_kb(callback.from_user.id, idea_id, status)
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке фото: {e}")
            await callback.message.answer(
                text, 
                reply_markup=await kb.favorites_kb(callback.from_user.id, idea_id, status)
            )
    else:
        await callback.message.answer(
            text, 
            reply_markup=await kb.favorites_kb(callback.from_user.id, idea_id, status)
        )

@user.callback_query(F.data.startswith("favorite_"))
async def cmd_favorite_idea(callback: CallbackQuery, state: FSMContext):
    """Adds the idea to favorites and updates the keyboard."""
    idea_id = callback.data.split("_")[1]
    added = await req.add_to_favorite(iid=idea_id, tg_id=callback.from_user.id)

    if not added:
        await callback.message.answer('Вы не авторизованы! 🚫')
        return

    try:
        await callback.message.edit_reply_markup(
            reply_markup=await kb.favorites_kb(callback.from_user.id, idea_id, True)
        )
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (добавление в избранное): {e}")
        await callback.message.answer('Не удалось обновить клавиатуру. Попробуйте позже.')

@user.callback_query(F.data.startswith("unfavorite_"))
async def cmd_unfavorite_idea(callback: CallbackQuery, state: FSMContext):
    """Removes the idea from favorites and updates the keyboard."""
    idea_id = callback.data.split("_")[1]
    removed = await req.delete_favorite(iid=idea_id, tg_id=callback.from_user.id)

    if not removed:
        await callback.message.answer('Вы не авторизованы! 🚫')
        return

    try:
        await callback.message.edit_reply_markup(
            reply_markup=await kb.favorites_kb(callback.from_user.id, idea_id, False)
        )
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (удаление из избранного): {e}")
        await callback.message.answer('Не удалось обновить клавиатуру. Попробуйте позже.')

# --- Soap Creation Handlers ---

@user.message(F.text == 'Создать мыло🧼')
async def create_soap_cmd(message: Message, state: FSMContext):
    """Starts the soap creation process."""
    await message.delete()
    await message.answer(
        'Для создания вашего мыла, нужно будет ответить на несколько вопросов!',
        reply_markup=kb.empty_kb
    )
    await state.set_state(st.QuestionsFsm.color)
    await message.answer(
        'Самое главное это цвет, давайте выберем его, нажмите на 1 из предложенных',
        reply_markup=await kb.get_cb_by_status_questions('color')
    )

@user.callback_query(F.data.startswith("answer_1_"))
async def answer_color(callback: CallbackQuery, state: FSMContext):
    """Handles the color question."""
    await callback.message.delete()
    answer_id = callback.data.split("_")[2]
    await state.update_data(color=answer_id)
    await state.set_state(st.QuestionsFsm.form)
    await callback.message.answer(
        'Неменее важна и Форма, ведь она радует глаз и позволяет удобно пользоваться мылом',
        reply_markup=await kb.get_cb_by_status_questions('form')
    )

@user.callback_query(F.data.startswith("answer_2_"))
async def answer_form(callback: CallbackQuery, state: FSMContext):
    """Handles the form question."""
    await callback.message.delete()
    answer_id = callback.data.split("_")[2]
    await state.update_data(form=answer_id)
    await state.set_state(st.QuestionsFsm.additives)
    await callback.message.answer(
        'На последок, выберите 1 добавление к вашему мылу из списка:\n',
        reply_markup=await kb.get_cb_by_status_questions('additives')
    )

@user.callback_query(F.data.startswith("answer_3_"))
async def answer_additives(callback: CallbackQuery, state: FSMContext):
    """Handles the additives question."""
    await callback.message.delete()
    answer_id = callback.data.split("_")[2]
    await state.update_data(additives=answer_id)
    data = await state.get_data()
    path = await req.get_soap_img(data)
    text = await req.get_soap_text(data)

    if path and os.path.exists(path):
        try:
            await callback.message.answer_photo(
                photo=FSInputFile(path, filename="soap_image.png"), 
                caption=text
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке фото: {e}")
            await callback.message.answer(
                f'При отправке фото произошла ошибка, мы уже передали её разработчикам!\n{text}'
            )

    await state.clear()

# --- Profile Handlers ---

@user.message(F.text == 'Профиль🏠')
async def profile_cmd(message: Message, state: FSMContext):
    """Displays the user profile."""
    await message.delete()
    user = await req.is_user_auth(message.from_user.id)
    if not user:
        await message.answer('Вы не авторизованы, хотите авторизоваться?')
        return
    count = await req.get_count_user_favorite(message.from_user.id)
    await message.answer(
        f'Приветствуем, {message.from_user.id} 👋
Поделок в избранном:\n{count}',
        reply_markup=await kb.profile_kb(message.from_user.id)
    )

@user.callback_query(F.data == 'delete_account')
async def delete_account_prompt(callback: CallbackQuery, state: FSMContext):
    """Prompts account deletion confirmation."""
    await callback.message.delete()
    await callback.message.answer(
        'Вы уверены, что хотите удалить аккаунт?\nВосстановить избранное будет невозможно!',
        reply_markup=kb.delete_account_kb
    )

@user.callback_query(F.data == 'submit_delete_account')
async def delete_account(callback: CallbackQuery, state: FSMContext):
    """Deletes the user account."""
    await callback.message.delete()
    await req.delete_my_account(tg_id=callback.from_user.id)
    await callback.answer('Аккаунт удалён!')
