import logging
import re

from typing import List

from tortoise.exceptions import DoesNotExist
from app.database.models import Favorite, User, Material, Idea


logger = logging.getLogger(__name__)


# ----- ПОЛЬЗОВАТЕЛЬ -----------
async def create_user(tg_id: int):  # создание пользователя
    user = await User.get_or_create(tg_id=tg_id)
    return

# Функция для удаления эмодзи
def remove_emoji(text: str) -> str:
    return re.sub(r'[^\w\s]', '', text)  

async def find_similar_crafts(materials: List[str]):
    materials = [remove_emoji(material) for material in materials]
    query_materials = await Material.filter(name__in=materials)

    for material in query_materials:
        material.name = remove_emoji(material.name)

    crafts = await Idea.all().prefetch_related('materials')

    def similarity_score(craft_materials, query_materials):
        craft_material_names = [remove_emoji(material.name) for material in craft_materials]
        common_materials = set(craft_material_names) & set(material.name for material in query_materials)
        return len(common_materials) 

    sorted_crafts = sorted(crafts, key=lambda craft: similarity_score(craft.materials, query_materials), reverse=True)

    return sorted_crafts[:3]


async def revert_idea_to_text(id: int):  # создание пользователя
    idea = await Idea.get(id=id)
    text = f'Идея: {idea.description}\n\n{idea.instruction}'
    return text

async def add_to_favorite(tg_id: int,iid: int):  # создание пользователя
    try:
        idea = await Idea.get(id=iid)
        user = await User.get(tg_id=tg_id)
    except DoesNotExist:
        return False
    await Favorite.get_or_create(user=user,idea=idea)
    return 
    
async def delete_favorite(tg_id: int,iid: int):  # создание пользователя
    try:
        idea = await Idea.get(id=iid)
        user = await User.get(tg_id=tg_id)
    except DoesNotExist:
        return False
    favorite = await Favorite.get(user=user,idea=idea)
    if favorite:
        favorite.delete()
    return True
        