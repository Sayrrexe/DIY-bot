import logging
import re

from typing import List
from webbrowser import get

from tortoise.exceptions import DoesNotExist
from app.database.models import Favorite, User, Material, Idea
from collections import Counter
from tortoise.expressions import Q


logger = logging.getLogger(__name__)


# ----- ПОЛЬЗОВАТЕЛЬ -----------
async def create_user(tg_id: int):  # создание пользователя
    user = await User.get_or_create(tg_id=tg_id)
    return

async def is_user_auth(tg_id: int):
    try:
        user = await User.get(tg_id=tg_id)
        if user:
            return True
    except DoesNotExist:
        return False

async def delete_my_account(tg_id: int):
    try:
        user = await User.get(tg_id=tg_id)
        # Удаляем связанные избранные записи
        await Favorite.filter(user=user).delete()
        # Теперь удаляем пользователя
        await user.delete()
        return True
    except DoesNotExist:
        return False

    
async def get_count_user_favorite(tg_id):
    try:
        user = await User.get(tg_id=tg_id)
        if user:
            count = await Favorite.filter(user=user).count()
            return count
        else:
            return False
    except DoesNotExist:
        return False
    
async def is_idea_favorite(tg_id, iid):
    try:
        user = await User.get(tg_id=tg_id)
        idea = await Idea.get(id=iid)
        if user:
            is_favorite = await Favorite.get(user=user, idea=idea)
            if is_favorite:
                return True
            else:
                return False
        else:
            return False
    except DoesNotExist:
        return False
    
async def add_to_favorite(tg_id, iid):
    try:
        user = await User.get(tg_id=tg_id)
        idea = await Idea.get(id=iid)
        # Проверяем, есть ли уже запись
        is_exist = await Favorite.filter(user=user, idea=idea).exists()
        if not is_exist:
            await Favorite.create(user=user, idea=idea)
            return True
        else:
            return True  # Уже есть в избранном
    except DoesNotExist:
        return False

async def delete_favorite(tg_id, iid):
    try:
        user = await User.get(tg_id=tg_id)
        idea = await Idea.get(id=iid)
        favorite_record = await Favorite.filter(user=user, idea=idea).first()
        if favorite_record:
            await favorite_record.delete()
            return True
        else:
            return False
    except DoesNotExist:
        return False

async def find_best_matching_ideas(material_list):
    # Получаем все материалы из базы данных
    db_materials = await Material.all()
    db_materials_map = {material.name: material.id for material in db_materials}

    # Сопоставляем переданные материалы с материалами из БД
    matching_ids = [db_materials_map[material] for material in material_list if material in db_materials_map]

    if not matching_ids:
        return []

    # Находим идеи, связанные с совпавшими материалами
    ideas = await Idea.filter(materials__in=matching_ids).prefetch_related('materials')

    # Подсчитываем количество совпадений для каждой идеи
    idea_match_counts = Counter(idea.id for idea in ideas for material in idea.materials if material.id in matching_ids)

    # Сортируем идеи по количеству совпадений и берём топ-3
    best_matches = idea_match_counts.most_common(3)

    # Формируем список с описаниями топ-3 идей
    top_ideas = [await Idea.get(id=idea_id) for idea_id, _ in best_matches]

    return top_ideas


async def revert_idea_to_text(id: int):
    idea = await Idea.get(id=id)
    text = f'Идея: {idea.description}\n\n{idea.instruction}'
    image = idea.image
    if image:
        return text, image
    return text, False

async def get_soap_img(data):
    mapping = {
    '1': 'rose',
    '2': 'sheet',
    '3': 'heart',
    '4': 'lavand',
    '5': 'green',
    '6': 'pink',
    }
    
    first = data['color']  
    second = data['form']
    
    first_name = mapping[second]
    second_name = mapping[first]
    path = f'media/soap/{first_name}/{second_name}.webp'
    return path

async def get_soap_text(data):
    mapping = {
    '1': 'в виде розы',
    '2': 'в виде листа',
    '3': 'в виде сердца',
    '4': 'лавандового',
    '5': 'Мятно-зелёного',
    '6': 'Нежно-розового',
    '7': 'Эфирных маслов',
    '8': 'блёсток',
    '9': 'Глицерина для увлажняющего эффекта'
    }
    
    color = data['color']  
    form = data['form']
    additives = data['additives']
    
    color_text = mapping[color]
    form_text = mapping[form]
    additives_text = mapping[additives]
    
    text = f'Вот так бы выглядело ваше мыло {form_text}, {color_text} цвета с добавлением {additives_text}🔥❤️‍🔥'
    return text
        