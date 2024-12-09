from email.mime import image
import logging

from app.database.models import Material, Idea, Question, Answers


logger = logging.getLogger(__name__)

materials_data = [
    {'name': 'Бисер 🧵', 'category': 'Украшения'},
    {'name': 'Ленты 🎀', 'category': 'Украшения'},
    {'name': 'Леска 🎣', 'category': 'Украшения'},
    {'name': 'Замки для браслетов 🔒', 'category': 'Украшения'},
    {'name': 'Декоративные цветы 🌸', 'category': 'Декор'},
    {'name': 'Клей 🧴', 'category': 'Инструменты'},
    {'name': 'Картон 📦', 'category': 'Декор'},
    {'name': 'Пряжа 🧶', 'category': 'Декор'},
    {'name': 'Проволока 🪡', 'category': 'Инструменты'},
    {'name': 'Воск 🕯️', 'category': 'Декор'},
    {'name': 'Сухоцветы 🌾', 'category': 'Декор'},
    {'name': 'Краситель 🎨', 'category': 'Инструменты'},
    {'name': 'Бумага 📄', 'category': 'Декор'},
    {'name': 'Нитки 🧶', 'category': 'Инструменты'},
    {'name': 'Камни 🪨', 'category': 'Декор'},
    {'name': 'Краска 🎨', 'category': 'Инструменты'},
    {'name': 'Лак 💅', 'category': 'Инструменты'},
    {'name': 'Стеклянные банки 🏺', 'category': 'Декор'},
    {'name': 'Гирлянды ✨', 'category': 'Декор'},
    {'name': 'Шишки 🌰', 'category': 'Декор'},
    {'name': 'Пластиковые бутылки 🍼', 'category': 'Декор'},
    {'name': 'Ткань 🧵', 'category': 'Декор'},
    {'name': 'Резинка 🪢', 'category': 'Инструменты'}
]

ideas_data = [
    {
        'description': 'Браслет с плетением 🎀',
        'full_description': 'Лента используется как основа, на которую нанизывается бисер, создавая узоры.',
        'instruction': 'Материалы:\n- Атласная лента (30 см)\n- Бисер в выбранной цветовой гамме\n- Игла и нитка\n\nИнструкция:\n1. Отрежьте ленту нужной длины, обработайте края зажигалкой. \n2. Проденьте нитку в иглу и закрепите её узелком. \n3. Начните с одного конца ленты: проткните иглой ленту сверху вниз, наберите бисерину и снова проткните ленту снизу вверх. \n4. Продолжайте до заполнения ленты, оставляя 2–3 см свободными. \n5. Закрепите нитку узелками, завяжите концы ленты в бантики.',
        'materials': ['Бисер 🧵', 'Ленты 🎀'],
        'image': 'media/idea/1.png'
    },
    {
        'description': 'Колье "Воздушное плетение" ✨',
        'full_description': 'Леска используется для создания многослойного колье с хаотично нанизанными бисеринами.',
        'instruction': 'Материалы:\n- Леска (несколько отрезков по 40–50 см)\n- Бисер разного размера и цвета\n- Застежка для колье\n\nИнструкция:\n1. Нанижите бисер на каждый отрезок лески в хаотичном порядке, чередуя размеры и цвета. \n2. Оставляйте промежутки между группами бисера для создания воздушного эффекта. \n3. Закрепите концы лески узелками или зажимами. \n4. Соберите все отрезки вместе и прикрепите к застежке.',
        'materials': ['Леска 🎣', 'Бисер 🧵'],
        'image': 'media/idea/2.png'
    },
    {
        'description': 'Панно из цветов 🌸',
        'full_description': 'Цветы приклеиваются на Картон , создавая объемную декоративную композицию.',
        'instruction': 'Материалы:\n- Декоративные цветы \n- Картон 📦\n- Клей  (горячий или универсальный)\n- Дополнительный декор (ленты, стразы)\n\nИнструкция:\n1. Вырежьте основу из Картон а нужной формы (круг, квадрат). ✂️\n2. Разложите цветы на основе для предварительной композиции. 🌼\n3. ПриКлей 🧴те цветы, начиная с центра и двигаясь к краям. \n4. Добавьте декоративные элементы для финального образа. ',
        'materials': ['Декоративные цветы 🌸', 'Картон 📦', 'Клей 🧴'],
        'image': 'media/idea/3.png'
    },
    {
        'description': 'Декоративные шары из пряжи 🧶',
        'full_description': 'Пряжа  используется для создания объемных шаров с помощью клея и воздушного шара.',
        'instruction': 'Материалы:\n- Пряжа \n- Воздушный шар\n- Клей  ПВА (разбавленный водой 2:1)\n- Ножницы\n\nИнструкция:\n1. Надуйте воздушный шар до желаемого размера и завяжите его. 🎈\n2. Пропитайте пряжу клеем и начните обматывать шар, создавая узор. \n3. Оставьте шар сохнуть на 12–24 часа. \n4. Проколите воздушный шар и удалите его изнутри. ',
        'materials': ['Пряжа 🧶', 'Клей 🧴'],
        'image': 'media/idea/4.png'
    },
    {
        'description': 'Декоративная свеча с сухоцветами 🕯️',
        'full_description': 'Воск заливается в форму с добавлением сухих цветов для украшения.',
        'instruction': 'Материалы:\n- Воск (парафин или пчелиный)\n- Краситель\n- Сухоцветы\n- Форма для свечи\n- Фитиль\n\nИнструкция:\n1. Растопите Воск  на водяной бане, следя за температурой. \n2. Добавьте краситель и перемешайте. \n3. Закрепите фитиль в форме. \n4. Выложите сухоцветы вдоль стенок формы и залейте Воск \n5. Оставьте свечу застывать на 4–6 часов, затем извлеките её из формы.',
        'materials': ['Воск 🕯️', 'Сухоцветы 🌾', 'Краситель 🎨'],
        'image': 'media/idea/5.png'
    },
    {
        'description': 'Модные серьги из бисера 🌟',
        'full_description': 'Бисер используется для создания стильных и ярких серег с использованием металлической основы.',
        'instruction': 'Материалы:\n- Бисер\n- Металлические серьги-основы\n- Нитка\n- Игла\n\nИнструкция:\n1. Проденьте нитку в иглу и закрепите её узелком.\n2. Нанижите бисер на нитку, чередуя цвета и размеры.\n3. Закрепите бисер на серьгах, аккуратно обвязывая металлическую основу. \n4. Завяжите узелок и обрежьте лишнюю нитку.',
        'materials': ['Бисер 🧵'],
        'image': 'media/idea/6.jpg'
    },
    {
        'description': 'Рамка для фото с декором 🌿',
        'full_description': 'Деревянная рамка украшается природными элементами: листьями, цветами, шишками.',
        'instruction': 'Материалы:\n- Деревянная рамка\n- Природные элементы (листья, Шишки, цветы)\n- Клей (горячий или универсальный)\n\nИнструкция:\n1. Очистите рамку от пыли и грязи.\n2. Разложите природные элементы для предварительной композиции. 🌱\n3. Приклейте элементы к рамке, создавая желаемый узор. \n4. Дайте клею высохнуть и вставьте фото.',
        'materials': ['Декоративные цветы 🌸', 'Картон 📦', 'Клей 🧴'],
        'image': 'media/idea/7.jpg'
    },
    {
        'description': 'Подставка для телефона из дерева 🌳',
        'full_description': 'Деревянная подставка для телефона с гравировкой или декором.',
        'instruction': 'Материалы:\n- Деревянная заготовка\n- Гравер или краски\n- Клей \n\nИнструкция:\n1. Подготовьте деревянную заготовку под подставку. \n2. Сделайте гравировку или покрасьте поверхность. \n3. Соберите подставку и закрепите части клеем. \n4. Дайте подставке высохнуть и используйте для телефона.',
        'materials': ['Картон 📦'],
        'image': 'media/idea/8.jpg'
    },
]

ideas_data.extend([
    {
        'description': 'Открытка с объемным декором 🎉',
        'full_description': 'Ленты и Бумага используются для создания красивого дизайна.',
        'instruction': 'Материалы:\n- Лист плотной бумаги или Картона для основы\n- Цветная Бумага для декора\n- Ленты, стразы, декоративные наклейки\n- Ножницы и Клей \n\nИнструкция:\n1. Сложите основу пополам, чтобы получилась открытка. ✂️\n2. Вырежьте декоративные элементы из цветной бумаги (цветы, сердечки, узоры). \n3. Приклейте их на переднюю часть открытки, создавая композицию.\n4. Украсьте открытку лентами и стразами, добавляя объемные элементы. \n5. Внутри напишите пожелание или приклейте распечатанный текст. ',
        'materials': ['Бумага 📄', 'Ленты 🎀', 'Клей 🧴'],
        'image': 'media/idea/9.png'
    },
    {
        'description': 'Роспись на камнях 🎨',
        'full_description': 'Создайте декоративные Камни  с рисунками.',
        'instruction': 'Материалы:\n- Камни  (гладкие, среднего размера, лучше круглые или овальные)\n- Акриловые краски и кисти разной толщины\n- Белая акриловая Краска (для базового слоя)\n- Лак для фиксации рисунка (матовый или глянцевый)\n\nИнструкция:\n1. Очистите Камни  с мылом, тщательно высушите их. \n2. Нанесите белый базовый слой краски, дайте высохнуть (20-30 мин). \n3. Создайте рисунок, сначала наметив узор карандашом. \n4. Покрасьте Камни  акриловыми красками, добавьте детали тонкой кистью. 🖌️\n5. Закрепите рисунок лаком и дайте ему высохнуть. \n6. Используйте Камни  для декора или как подарок. 🎁',
        'materials': ['Камни 🪨', 'Краска 🎨', 'Лак 💅'],
        'image': 'media/idea/10.png'
    },
    {
        'description': 'Ночник из банки 💡',
        'full_description': 'Банка используется как абажур, а Гирлянды создают освещение.',
        'instruction': 'Материалы:\n- Стеклянная банка (например, из-под варенья)\n- Ленты, джутовая нить или кружево для украшения\n- Маленькая светодиодная гирлянда на батарейках\n- Клей (горячий или универсальный)\n- Декоративные элементы (бусины, блестки, искусственные цветы)\n\nИнструкция:\n1. Снимите этикетки и промойте банку с мылом. \n2. Украсьте банку лентами и декоративными элементами (бусины, цветы). \n3. Разместите гирлянду внутри банки, убедитесь, что блок с батарейками доступен. \n4. Закройте крышку или украсьте верх бантом. \n5. Включите гирлянду, создайте уютную атмосферу. ',
        'materials': ['Стеклянные банки 🏺', 'Ленты 🎀', 'Гирлянды ✨'],
        'image': 'media/idea/11.png'
    },
    {
        'description': 'Венок на дверь 🎄',
        'full_description': 'Шишки  приклеиваются к круглой основе из Картон а или проволоки, украшаются лентами.',
        'instruction': 'Материалы:\n- Шишки 🌰\n- Клей  (горячий или универсальный)\n- Ленты для украшения\n\nИнструкция:\n1. Для основы используйте Картон или проволоку. Согните проволоку в круг.\n2. Приклейте Шишки, начиная с внешнего края.\n3. Украсьте венок лентами, добавьте декоративные элементы (ягоды, блестки).\n4. Повесьте венок на дверь, добавьте веревочку для подвешивания.',
        'materials': ['Шишки 🌰', 'Клей 🧴', 'Ленты 🎀'],
        'image': 'media/idea/12.png'
    },
    {
        'description': 'Подсвечник из пластиковых бутылок 🕯️',
        'full_description': 'Бутылка разрезается и украшается для создания декоративного подсвечника.',
        'instruction': 'Материалы:\n- Пластиковая бутылка\n- Краска (акриловая)\n- Ленты и декор для украшения\n\nИнструкция:\n1. Аккуратно разрежьте пластиковую бутылку, оставив основу. \n2. Покрасьте бутылку акриловой краской. \n3. Украсьте подсвечник лентами, блестками и бусинами. \n4. Разместите свечу в центре подсвечника. \n5. Добавьте декор по желанию. ',
        'materials': ['Пластиковые бутылки 🍼', 'Краска 🎨'],
        'image': 'media/idea/13.png'
    },
    {
        'description': 'Теру Бодзу 🌞',
        'full_description': 'Теру Бодзу — японская кукла-талисман для привлечения хорошей погоды.',
        'instruction': 'Материалы:\n- Бумага или Ткань для тела и головы\n- Нитки или ленты для закрепления\n- Маркеры для лица\n\nИнструкция:\n1. Возьмите шарик (вату или мячик) для головы и оберните Тканью. \n2. Закрепите Ткань  ниткой или лентой, чтобы форма головы была плотной. \n3. Нарисуйте лицо на голове (улыбку для солнечной погоды или печаль для дождя). \n4. Повесьте куклу у окна или на балконе для исполнения пожелания. 🌞🌧️',
        'materials': ['Бумага 📄', 'Ткань 🧵', 'Нитки 🧶', 'Ленты 🎀'],
        'image': 'media/idea/14.png'
    },
])


answers = ['в виде розы', 'в виде листа', 'в виде сердца','Лавандовый','Мятно-зелёный','Нежно-розовый', 'Эфирные масла','блёстки','Глицерин']

questions = [
    {
        'text': 'Какую форму хотите?',
        'answers': ['в виде розы', 'в виде листа', 'в виде сердца']
    },
    {
        'text': 'Какой хотите цвет?',
        'answers': ['Лавандовый', 'Мятно-зелёный', 'Нежно-розовый']
    },
    {
        'text': 'Какие дополнительные элементы хотите добавить?',
        'answers': ['Эфирные масла', 'блёстки', 'Глицерин']
    }
]


async def create_data():
    materials = {material['name']: await Material.create(**material) for material in materials_data}

    # Добавляем идеи
    for idea_data in ideas_data:
        # Получаем материалы для каждой идеи
        idea_materials = [materials[material_name] for material_name in idea_data['materials']]
        idea = await Idea.create(description=idea_data['description'], instruction=idea_data['instruction'], image=idea_data['image'])
        await idea.materials.add(*idea_materials)
        
    answer_objects = {}
    for ans in answers:
        answer_obj = await Answers.create(answer=ans)
        answer_objects[ans] = answer_obj

    # Теперь создаём вопросы и прикрепляем к ним ответы
    for q_data in questions:
        q_obj = await Question.create(text=q_data['text'])
        # Получаем объекты ответов для данного вопроса
        q_answers = [answer_objects[a] for a in q_data['answers']]
        await q_obj.answers.add(*q_answers)

    logger.info("Успешное заполнение БД!")

