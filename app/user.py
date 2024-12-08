import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.states as st
import app.database.requests as req


logger = logging.getLogger(__name__)

user = Router()


# ----- ОБРАБОТКА /start -----------
@user.message(CommandStart())
async def cmd_start(message: Message):
    await req.create_user(message.from_user.id)
    await message.answer(
        "Добро пожаловать в бот!\nУзнате список всех команд с помощью /help\nНажмите на кнопку что бы добавить характеристики вашего авто",
        reply_markup=kb.start_kb
    )

