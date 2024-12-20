import logging
from collections import Counter

from tortoise.exceptions import DoesNotExist
from app.database.models import Favorite, User, Material, Idea

logger = logging.getLogger(__name__)


# ----- ПОЛЬЗОВАТЕЛЬ -----------
async def create_user(tg_id: int):
    """
    Создание или получение пользователя по tg_id.
    """
    await User.get_or_create(tg_id=tg_id)


async def is_user_auth(tg_id: int) -> bool:
    """
    Проверка, авторизован ли пользователь.
    """
    try:
        user = await User.get(tg_id=tg_id)
        if user:
            return True
    except DoesNotExist:
        return False


async def delete_my_account(tg_id: int) -> bool:
    """
    Удаление аккаунта и связанных избранных записей пользователя.
    """
    try:
        user = await User.get(tg_id=tg_id)
        await Favorite.filter(user=user).delete()
        await user.delete()
        return True
    except DoesNotExist:
        return False


async def get_count_user_favorite(tg_id: int):
    """
    Получение количества избранных идей пользователя.
    """
    try:
        user = await User.get(tg_id=tg_id)
        if user:
            return await Favorite.filter(user=user).count()
        return False
    except DoesNotExist:
        return False


async def is_idea_favorite(tg_id: int, iid: int) -> bool:
    """
    Проверка, является ли данная идея избранной для пользователя.
    """
    try:
        user = await User.get(tg_id=tg_id)
        idea = await Idea.get(id=iid)
        if user:
            is_favorite = await Favorite.get(user=user, idea=idea)
            return bool(is_favorite)
        return False
    except DoesNotExist:
        return False


async def add_to_favorite(tg_id: int, iid: int) -> bool:
    """
    Добавление идеи в избранное.
    """
    try:
        user = await User.get(tg_id=tg_id)
        idea = await Idea.get(id=iid)
        is_exist = await Favorite.filter(user=user, idea=idea).exists()
        if not is_exist:
            await Favorite.create(user=user, idea=idea)
        return True
    except DoesNotExist:
        return False


async def delete_favorite(tg_id: int, iid: int) -> bool:
    """
    Удаление идеи из избранного.
    """
    try:
        user = await User.get(tg_id=tg_id)
        idea = await Idea.get(id=iid)
        favorite_record = await Favorite.filter(user=user, idea=idea).first()
        if favorite_record:
            await favorite_record.delete()
            return True
        return False
    except DoesNotExist:
        return False


async def find_best_matching_ideas(material_list: list):
    """
    Поиск лучших подходящих идей по списку материалов.
    """
    db_materials = await Material.all()
    db_materials_map = {material.name: material.id for material in db_materials}

    # Фильтруем входящие материалы по тем, что есть в БД
    matching_ids = [db_materials_map[m] for m in material_list if m in db_materials_map]

    if not matching_ids:
        return []

    ideas = await Idea.filter(materials__in=matching_ids).prefetch_related("materials")
    idea_match_counts = Counter(
        idea.id
        for idea in ideas
        for material in idea.materials
        if material.id in matching_ids
    )

    # Получаем топ-3 идей
    best_matches = idea_match_counts.most_common(3)
    top_ideas = [await Idea.get(id=idea_id) for idea_id, _ in best_matches]

    return top_ideas


async def revert_idea_to_text(idea_id: int):
    """
    Возвращает текстовое описание и изображение для заданной идеи.
    """
    idea = await Idea.get(id=idea_id)
    text = f"Идея: {idea.description}\n\n{idea.instruction}"
    image = idea.image
    if image:
        return text, image
    return text, False


async def get_soap_img(data: dict) -> str:
    """
    Генерирует путь к изображению мыла по данным выбора.
    """
    mapping = {
        "1": "rose",
        "2": "sheet",
        "3": "heart",
        "4": "lavand",
        "5": "green",
        "6": "pink",
    }

    first = data["color"]
    second = data["form"]

    first_name = mapping[second]
    second_name = mapping[first]
    path = f"media/soap/{first_name}/{second_name}.webp"
    return path


async def get_soap_text(data: dict) -> str:
    """
    Генерирует описание выбранных параметров мыла.
    """
    mapping = {
        "1": "в виде розы",
        "2": "в виде листа",
        "3": "в виде сердца",
        "4": "лавандового",
        "5": "Мятно-зелёного",
        "6": "Нежно-розового",
        "7": "Эфирных масел",
        "8": "блёсток",
        "9": "Глицерина для увлажняющего эффекта",
    }

    color = data["color"]
    form = data["form"]
    additives = data["additives"]

    color_text = mapping[color]
    form_text = mapping[form]
    additives_text = mapping[additives]

    text = f"Вот так бы выглядело ваше мыло {form_text}, {color_text} цвета с добавлением {additives_text}🔥❤️‍🔥"
    return text
