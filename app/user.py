import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.states as st
import app.database.requests as req
from app.utils import clear_text


logger = logging.getLogger(__name__)
user = Router()


# ----- /id -----
@user.message(Command('id'))
async def cmd_id(message: Message):
    """Отправляет ID пользователя."""
    user_id = message.from_user.id
    await message.answer(
        f"`{user_id}`",
        reply_markup=kb.main_kb,
        parse_mode='MARKDOWN'
    )

# ----- /start -----
@user.message(CommandStart())
async def cmd_start(message: Message):
    """Приветственное сообщение."""
    await message.answer(
        "Добро пожаловать в бот! 🤖\n"
        "Узнайте список всех команд с помощью /help 📜\n"
        "Используйте кнопки меню для быстрого взаимодействия 🚀\n"
        "Хотите войти в аккаунт для синхронизации избранных поделок?",
        reply_markup=kb.start_kb
    )

# ----- Авторизация -----
@user.callback_query(F.data == 'join_to_account')
async def join_to_account(callback: CallbackQuery):
    """Авторизация пользователя."""
    await req.create_user(callback.from_user.id)
    await callback.message.answer(
        'Вы вошли в аккаунт! 🔓🔥', 
        reply_markup=kb.main_kb
    )

@user.callback_query(F.data == 'skip')
async def skip_cmd(callback: CallbackQuery,state: FSMContext):
    """Пропустить авторизацию."""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        'Вы в главном меню 🏠!', 
        reply_markup=kb.main_kb
    )

# ----- Получение идеи -----
@user.message(F.text == 'Получить идею🌟')
async def cmd_get_idea(message: Message, state: FSMContext):
    """Начало выбора материалов."""
    await message.delete()
    await state.update_data(materials=[])
    await message.answer(
        "Из списка ниже выберите материалы 🧩:\n\n• ",
        reply_markup=await kb.materials_kb()
    )

@user.callback_query(F.data == 'clear_materials')
async def cmd_clear_materials(callback: CallbackQuery, state: FSMContext):
    """Очистка списка материалов."""
    await callback.message.delete()
    await state.update_data(materials=[])
    await callback.message.answer(
        "Из списка ниже выберите материалы 🧩:\n\n• ",
        reply_markup=await kb.materials_kb()
    )

@user.callback_query(F.data.startswith("materials_add_"))
async def cmd_add_material(callback: CallbackQuery, state: FSMContext):
    """Добавление/удаление материалов из списка."""
    material = callback.data.split("_")[-1]
    user_data = await state.get_data()
    materials = user_data.get('materials', [])

    new_text, new_materials, edited = await clear_text(material, materials)
    if edited:
        await state.update_data(materials=new_materials)
        await callback.message.edit_text(
            text=new_text,
            reply_markup=await kb.materials_kb()
        )

@user.callback_query(F.data == 'accept_materials')
async def cmd_accept_materials(callback: CallbackQuery, state: FSMContext):
    """Принять выбранные материалы и получить идеи."""
    await callback.message.delete()
    user_data = await state.get_data()
    materials = user_data.get('materials', [])
    ideas = await req.find_best_matching_ideas(materials)
    await callback.message.answer(
        'Выберите Поделку из предложенных 🎨:',
        reply_markup=await kb.ideas_kb(ideas)
    )

@user.callback_query(F.data.startswith("idea_"))
async def cmd_show_idea(callback: CallbackQuery, state: FSMContext):
    """Отобразить выбранную идею."""
    idea_id = callback.data.split("_")[1]
    text = await req.revert_idea_to_text(idea_id)
    await callback.message.answer(
        text, 
        reply_markup=await kb.favorites_kb(callback.from_user.id, idea_id, True)
    )

@user.callback_query(F.data.startswith("favorite_"))
async def cmd_favorite_idea(callback: CallbackQuery, state: FSMContext):
    """Добавить идею в избранное."""
    idea_id = callback.data.split("_")[1]
    text = callback.message.text + '\n'
    added = await req.add_to_favorite(iid=idea_id, tg_id=callback.from_user.id)
    if not added:
        await callback.message.answer('Вы не авторизованы! 🚫')
    else:
        await callback.message.edit_text(
            text=text,
            reply_markup=await kb.favorites_kb(callback.from_user.id, idea_id, False)
        )

@user.callback_query(F.data.startswith("unfavorite_"))
async def cmd_unfavorite_idea(callback: CallbackQuery, state: FSMContext):
    """Удалить идею из избранного."""
    idea_id = callback.data.split("_")[1]
    text = callback.message.text + '\n'
    removed = await req.delete_favorite(iid=idea_id, tg_id=callback.from_user.id)
    if not removed:
        await callback.message.answer('Вы не авторизованы! 🚫')
    else:
        await callback.message.edit_text(
            text=text,
            reply_markup=await kb.favorites_kb(callback.from_user.id, idea_id, True)
        )
