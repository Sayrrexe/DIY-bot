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

materials = []

# ----- /id -----
@user.message(Command('id'))
async def cmd_start(message: Message):
    id = message.from_user.id
    await message.answer(
        f"`{id}`",
        reply_markup=kb.main_kb, parse_mode='MARKDOWN'
    )

# ----- ОБРАБОТКА /start -----------
@user.message(CommandStart())
async def cmd_start(message: Message):
    
    await message.answer(
        "Добро пожаловать в бот!\nУзнате список всех команд с помощью /help\nИспользуйте кнопки меню для быстрого взаимодействия\nХотите войти в аккаунт для синхронизации избранных поделок?",
        reply_markup=kb.start_kb
    )
    
# ----- Авторизация -----------
@user.callback_query(F.data == 'join_to_account')
async def join_to_account(callback: CallbackQuery):
    await req.create_user(callback.from_user.id)
    await callback.message.answer('Вы вошли в аккаунт!🔥', reply_markup = kb.main_kb)
    
@user.callback_query(F.data == 'skip')
async def skip_cmd(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Вы в главном меню🏠!', reply_markup = kb.main_kb)

# ----- Идея -----------
@user.message(F.text == 'Получить идею🌟')
async def cmd_get_idea(message: Message):
    await message.delete()
    await message.answer('Из списка ниже выберите, те материалы, которые у вас есть\nОни появятся в списке ниже:\n\n• \n\n ', reply_markup=await kb.materials_kb())

@user.callback_query(F.data == 'clear_materials')
async def cmd_get_idea(callback: CallbackQuery):
    await callback.message.delete()
    global materials
    materials = []
    await callback.message.answer('Из списка ниже выберите, те материалы, которые у вас есть\nОни появятся в списке ниже:\n\n• \n\n ', reply_markup=await kb.materials_kb())
    
@user.callback_query(F.data.startswith("materials_add_"))
async def added_get_callback(callback: CallbackQuery, state: FSMContext):
    global materials
    
    data = callback.data.split("_")[-1]
    text = callback.message.text
    
    text, materials, edit = await clear_text(data, materials)
    if edit:
        await callback.message.edit_text(
            text=text,
            reply_markup=await kb.materials_kb()
        )
    

@user.callback_query(F.data == 'accept_materials')
async def cmd_get_idea(callback: CallbackQuery):
    await callback.message.delete()
    global materials
    ideas = await req.find_similar_crafts(materials)
    await callback.message.answer('Выберите Поделку из предложенных', reply_markup=await kb.ideas_kb(ideas))

@user.callback_query(F.data.startswith("idea_"))
async def added_get_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_")[1]
    text = await req.revert_idea_to_text(data)
    await callback.message.answer(text, reply_markup=await kb.favorites_kb(callback.from_user.id, data, True))
    
@user.callback_query(F.data.startswith("favorite_"))
async def added_get_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_")[1]
    text = callback.message.text + '\n'
    a = await req.add_to_favorite(iid=data,tg_id=callback.from_user.id)
    if not a:
        await callback.message.answer('вы не авторизованы!')
    await callback.message.edit_text(
            text=text,
            reply_markup=await kb.favorites_kb(callback.from_user.id, data, False))
    
@user.callback_query(F.data.startswith("unfavorite_"))
async def added_get_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_")[1]
    text = callback.message.text + '\n'
    a = await req.delete_favorite(iid=data,tg_id=callback.from_user.id)
    if not a:
        await callback.message.answer('вы не авторизованы!')
    await callback.message.edit_text(
            text=text,
            reply_markup=await kb.favorites_kb(callback.from_user.id, data, True))
    
    
    

    
    
