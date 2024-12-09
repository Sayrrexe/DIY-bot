import logging
import re

from typing import List

from tortoise.exceptions import DoesNotExist
from app.database.models import Favorite, User, Material, Idea
from collections import Counter
from tortoise.expressions import Q


logger = logging.getLogger(__name__)


# ----- ПОЛЬЗОВАТЕЛЬ -----------
async def create_user(tg_id: int):  # создание пользователя
    user = await User.get_or_create(tg_id=tg_id)
    return

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

async def add_to_favorite(tg_id: int,iid: int):  # создание пользователя
    try:
        idea = await Idea.get(id=iid)
        user = await User.get(tg_id=tg_id)
    except DoesNotExist:
        return False
    await Favorite.get_or_create(user=user,idea=idea)
    return True
    
async def delete_favorite(tg_id: int,iid: int):  # создание пользователя
    try:
        idea = await Idea.get(id=iid)
        user = await User.get(tg_id=tg_id)
    except DoesNotExist:
        return False
    favorite = await Favorite.get(user=user,idea=idea)
    if favorite:
        await favorite.delete()
    return True
        