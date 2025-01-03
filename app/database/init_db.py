import logging

from app.database.models import Material, Idea, Question, Answers


logger = logging.getLogger(__name__)

materials_data = [
    {"name": "Бисер 🧵", "category": "Украшения"},
    {"name": "Ленты 🎀", "category": "Украшения"},
    {"name": "Леска 🎣", "category": "Украшения"},
    {"name": "Замки для браслетов 🔒", "category": "Украшения"},
    {"name": "Декоративные цветы 🌸", "category": "Декор"},
    {"name": "Клей 🧴", "category": "Инструменты"},
    {"name": "Картон 📦", "category": "Декор"},
    {"name": "Пряжа 🧶", "category": "Декор"},
    {"name": "Проволока 🪡", "category": "Инструменты"},
    {"name": "Воск 🕯️", "category": "Декор"},
    {"name": "Сухоцветы 🌾", "category": "Декор"},
    {"name": "Краситель 🎨", "category": "Инструменты"},
    {"name": "Бумага 📄", "category": "Декор"},
    {"name": "Нитки 🧶", "category": "Инструменты"},
    {"name": "Камни 🪨", "category": "Декор"},
    {"name": "Краска 🎨", "category": "Инструменты"},
    {"name": "Лак 💅", "category": "Инструменты"},
    {"name": "Стеклянные банки 🏺", "category": "Декор"},
    {"name": "Гирлянды ✨", "category": "Декор"},
    {"name": "Шишки 🌰", "category": "Декор"},
    {"name": "Пластиковые бутылки 🍼", "category": "Декор"},
    {"name": "Ткань 🧵", "category": "Декор"},
]

ideas_data = [
    {
        "description": "Браслет с плетением ✌️",
        "full_description": "Лента используется как основа, на которую нанизывается бисер, создавая узоры.",
        "instruction": "Подготовьте материалы:\n    -Атласную ленту длиной 30 см (шириной 1–2 см, в зависимости от вашего вкуса).\n    -Бисер в выбранной цветовой гамме.\n    -Иглу с тонкой ниткой, подходящей по цвету к ленте.\n\n1. Отрежьте ленту нужной длины, обожгите края зажигалкой или свечой, чтобы они не растрепались.\n2. На нитку проденьте иглу и закрепите её узелком.\n3. Начните с одного конца ленты, отступив 2–3 см от края:\n4. Проткните иглой ленту сверху вниз, закрепляя нитку.\n5. Нанижите первую бисерину и проткните иглой ленту снизу вверх.\n6. Повторяйте эти шаги, оставляя равные промежутки между бисеринками (примерно 1–2 см).\n7. Продолжайте до тех пор, пока не заполните центр ленты бисером, оставляя 2–3 см свободной ленты сдругого конца.\n8. Закрепите нитку:\n\nСделайте несколько узелков, чтобы бисер крепко держался.\nОбрежьте излишки нитки.\nЗавяжите концы ленты в бантики, чтобы создать удобную застежку.\n\nВаш браслет готов! Вы можете дополнить его подвесками или другим декором по желанию.",
        "materials": ["Бисер 🧵", "Ленты 🎀"],
        "image": "media/idea/1.png",
    },
    {
        "description": "Колье \"Воздушное плетение\" 💍",
        "full_description": "Леска используется для создания многослойного колье, на которое хаотично нанизываются бисерины.",
        "instruction": "Подготовьте материалы:\n    -Леску (несколько отрезков длиной 40–50 см).\n    -Бисер разного размера и цвета.\n    -Застежку для колье.\n\n1. На каждом отрезке лески начните хаотично нанизывать бисер, чередуя размеры и цвета.\n2. Убедитесь, что между группами бисера есть небольшие промежутки, чтобы создать воздушный эффект.\n3. Закрепите бисер на концах лески с помощью узлов или специальных зажимов.\n4. Повторите процесс для всех отрезков лески.\n5. Соберите все отрезки вместе и прикрепите их к застежке.\n\nВаше колье готово! Оно выглядит легким и объемным благодаря воздушной технике.\n",
        "materials": ["Леска 🎣", "Бисер 🧵"],
        "image": "media/idea/2.png",
    },
    {
        "description": "Панно из цветов 🌸",
        "full_description": "Цветы приклеиваются на картон в виде объемной композиции.",
        "instruction": "Подготовьте материалы:\n    -Лист плотного картона или фанеры (основа).\n    -Декоративные цветы (искусственные или высушенные).\n    -Горячий клей или клей-пистолет.\n    -Дополнительные элементы для декора (ленты, стразы).\n\n1. Вырежьте основу нужной формы (круг, квадрат, сердце).\n2. Разложите цветы на основе, чтобы увидеть будущую композицию.\n3. Начните с крупных цветов, размещая их в центре.\n4. Дополните мелкими цветами и декоративными элементами.\n5. Приклейте цветы к основе горячим клеем, начиная с центральных элементов и постепенно двигаясь к краям.\n6. Добавьте финальные детали (стразы, бантики) для завершения образа.\n\nВаше панно готово! Вы можете разместить его на стене или подарить.\n",
        "materials": ["Декоративные цветы 🌸", "Картон 📦", "Клей 🧴"],
        "image": "media/idea/3.png",
    },
    {
        "description": "Декоративные шары из пряжи 🧶",
        "full_description": "Шары из пряжи создаются с использованием клея и формы (например, воздушного шара).",
        "instruction": "Подготовьте материалы:\n    -Пряжу (лучше хлопковую или акриловую).\n    -Воздушный шар.\n    -Клей ПВА (разбавьте его водой в соотношении 2:1).\n    -Ножницы.\n\n1. Надуйте воздушный шар до желаемого размера и завяжите его.\n2. Отрежьте длинные куски пряжи и пропитайте их клеем.\n3. Начните обматывать пряжей воздушный шар, создавая плотный или ажурный рисунок.\n4. Дайте шару полностью высохнуть (около 12–24 часов).\n5. После высыхания проколите воздушный шар и аккуратно удалите его изнутри.\n\nГотовый шар можно использовать как декор или основу для гирлянды.\n",
        "materials": ["Пряжа 🧶", "Клей 🧴"],
        "image": "media/idea/4.png",
    },
    {
        "description": "Декоративная свеча с сухоцветами 🕯️",
        "full_description": "Воск заливается в форму с добавлением сухих цветов для украшения.",
        "instruction": "Подготовьте материалы:\n    -Воск (парафин или пчелиный).\n    -Краситель для свечей.\n    -Сухоцветы.\n    -Форма для свечи.\n    -Фитиль.\n\n1. Растопите воск на водяной бане, следя за тем, чтобы он не перегрелся.\n2. Добавьте краситель, хорошо перемешав его.\n3. Закрепите фитиль в центре формы (например, с помощью палочки и скотча).\n4. Выложите сухоцветы вдоль стенок формы.\n5. Аккуратно залейте воск в форму, оставив немного места до края.\n6. Дайте свече остыть и застынуть (4–6 часов).\n7. Извлеките свечу из формы и обрежьте фитиль до нужной длины.\n\nГотово!",
        "materials": ["Воск 🕯️", "Сухоцветы 🌾", "Краситель 🎨"],
        "image": "media/idea/5.png",
    },
    {
        "description": "Открытка с объемным декором 🦋",
        "full_description": "Ленты и бумага используются для создания красивого дизайна.",
        "instruction": "Подготовьте материалы:\n    -Лист плотной бумаги или картона для основы.\n    -Цветную бумагу для декора.\n    -Ленты, стразы, декоративные наклейки.\n    -Ножницы и клей.\n\n1. Сложите основу пополам, чтобы получилась открытка.\n2. Вырежьте декоративные элементы из цветной бумаги (цветы, сердечки, узоры).\n3. Приклейте их на переднюю часть открытки, создавая композицию.\n4. Украсьте открытку лентами и стразами, добавляя объемные элементы.\n5. Внутри напишите пожелание или приклейте распечатанный текст.\n\nВы можете подарить эту открытку своим близким",
        "materials": ["Бумага 📄", "Ленты 🎀", "Клей 🧴"],
        "image": "media/idea/6.png",
    },
    {
        "description": "Роспись на камнях 🍥",
        "full_description": "Создайте декоративные камни с рисунками.",
        "instruction": "Подготовьте материалы:\n    -Камни (гладкие, среднего размера, лучше круглые или овальные).\n    -Акриловые краски и кисти разной толщины.\n    -Белую акриловую краску (для базового слоя).\n    -Лак для фиксации рисунка (матовый или глянцевый).\n\n1. Очистите камни:\nТщательно вымойте их с мылом, чтобы удалить грязь.\nВысушите камни перед нанесением краски.\n\n2. Нанесите базовый слой:\nПокройте всю поверхность камня белой акриловой краской.\nОставьте до полного высыхания (около 20–30 минут).\n\n3. Создайте рисунок:\nИспользуйте карандаш, чтобы слегка наметить узор (если требуется).\nНанесите основной цвет кистью средней толщины.\nДобавьте детали тонкой кистью, такие как узоры, контуры, точки.\nДайте рисунку высохнуть (20–30 минут).\n\n4. Закрепите рисунок лаком:\nРавномерно распылите или нанесите лак кистью на всю поверхность камня.\nДайте высохнуть в течение нескольких часов.\n\nИспользуйте готовый камень для украшения интерьера, сада или в качестве подарка.\n",
        "materials": ["Камни 🪨", "Краска 🎨", "Лак 💅"],
        "image": "media/idea/7.png",
    },
    {
        "description": "Ночник из банки 🥫",
        "full_description": "Банка используется как абажур, а гирлянды создают освещение.",
        "instruction": "Подготовьте материалы:\n\n    -Стеклянная банка (подойдет банка из-под варенья или с широким горлышком).\n    -Ленты, джутовая нить или кружево для украшения.\n    -Маленькая светодиодная гирлянда на батарейках.\n    -Клей (горячий клей или прозрачный универсальный).\n    -Декоративные элементы (бусины, блестки, искусственные цветы).\n\nОчистка банки:\n1. Снимите этикетки и промойте банку с мылом, удаляя остатки клея.\n2. Просушите банку, чтобы она была абсолютно сухой.\n\nУкрашение банки:\n3. Начните с верхней части банки. Обмотайте горлышко джутовой нитью или приклейте ленты.\n4. На внешнюю поверхность банки приклейте кружево или декоративные элементы. Например:\n5. Создайте узор из бусин или блесток.\n6. Прикрепите небольшие искусственные цветы или листочки.\n7. Если хотите, можете оставить часть банки прозрачной для эффекта свечения.\n\nПодготовка гирлянды:\n8. Разместите гирлянду внутри банки, уложив её по спирали для создания интересного эффекта.\n9. Убедитесь, что блок с батарейками остается доступным (например, прижмите его к стенке банки или оставьте рядом).\n\nФинальная сборка:\n10. Закройте крышку банки, если это возможно, или украсьте верхний край банта из ленты.\n11. Проверьте, чтобы гирлянда включалась и свет равномерно распределялся по банке.\n\nГотово:\nВключите гирлянду и используйте ночник для создания уютной атмосферы в комнате.\n\nСоветы:\nДля зимнего декора внутрь банки можно добавить искусственный снег, шишки или миниатюрные игрушки.Используйте банки разного размера для создания серии ночников.",
        "materials": ["Стеклянные банки 🏺", "Ленты 🎀", "Гирлянды ✨"],
        "image": "media/idea/8.png",
    },
    {
        "description": "Венок на дверь 🚪",
        "full_description": "Шишки приклеиваются к круглой основе и украшаются лентами.",
        "instruction": "Создание основы:\n1. Для основы используйте картон или гибкую проволоку. Если вы выбрали картон, вырежьте круг нужного диаметра. Чтобы сделать венок из проволоки, согните проволоку в круг, закрепив концы с помощью клея или скотча.\n\nПриклеивание шишек:\n2. Подготовьте шишки, очищенные от грязи и пыльцы. Используйте горячий клей или клеевой пистолет, чтобы приклеивать шишки к основе. Начните с внешнего края и постепенно двигайтесь к центру, заполняя все пространство шишками. Старайтесь, чтобы шишки располагались плотно друг к другу, но при этом не перекрывали друг друга.\n\nУкрашение венка:\n3. После того как шишки приклеены, украсьте венок лентами. Вы можете использовать атласные или бархатные ленты для создания бантиков, которые можно прикрепить к венку в различных местах. Также добавьте декоративные элементы, такие как искусственные ягоды, маленькие шишки или блестки, чтобы придать венку более праздничный вид.\n\nПоследние штрихи:\n4. Если хотите, можно добавить маленькие фонарики или искусственные снежинки, чтобы венок выглядел еще более ярко и празднично. Не забудьте прикрепить на верхнюю часть венка ленточку для подвешивания.\n\n",
        "materials": ["Шишки 🌰", "Клей 🧴", "Ленты 🎀"],
        "image": "media/idea/9.png",
    },
    {
        "description": "Подсвечник 🔥",
        "full_description": "Бутылка разрезается и украшается для создания декоративного подсвечника.",
        "instruction": "Подготовка бутылки:\nВозьмите пластиковую бутылку (например, от напитков или воды). С помощью ножниц или ножа аккуратно разрежьте бутылку, оставив нижнюю часть. Оставшийся кусок будет основой для подсвечника, его высоту можно подкорректировать в зависимости от желаемого размера.\n\nОкраска основы:\nОбработайте поверхность бутылки акриловой краской. Выберите цвет, который вам нравится: золотой, серебряный, белый или любой другой оттенок. Наносите краску равномерно, используя кисточку или губку, чтобы создать красивый ровный слой. Для яркости можно сделать несколько слоев краски, давая каждому слою высохнуть перед нанесением следующего.\n\nУкрашение подсвечника:\nКогда краска высохнет, приступайте к украшению. Покройте бутылку блестками для праздничного сияния или приклейте кружево по краю. Ленты можно использовать для обвязывания нижней части подсвечника или для создания декоративных бантиков. Вы можете также добавить маленькие элементы, такие как бусины, стразы или искусственные цветы для дополнительной красоты.\n\nРазмещение свечи:\nВ центре подсвечника разместите небольшую свечу. Лучше всего использовать чайные свечи, так как они идеально помещаются в нижнюю часть бутылки. Если подсвечник имеет высокие стенки, можно использовать свечи на батарейках для безопасности.\n\nФинишные детали:\nЕсли вы хотите, можете украсить верхнюю часть бутылки, добавив дополнительные элементы декора, такие как маленькие фигурки, искусственный снег или ягоды.",
        "materials": ["Пластиковые бутылки 🍼", "Краска 🎨"],
        "image": "media/idea/10.png",
    },
    {
        "description": "Теру Бодзу ☀️",
        "full_description": "Теру Бодзу — японская кукла-талисман для привлечения хорошей погоды.",
        "instruction": "Шаги:\n\n1. Подготовка основы для головы\nВозьмите шарик (вату, бумажный комок или мячик) и поместите его в центр ткани или бумаги. Это будет голова теру бодзу.\n\n2. Формирование головы\nОберните шарик тканью или бумагой так, чтобы он оказался в центре. Оставьте свисающий край для \"тела\".\nПлотно закрепите основание головы ниткой, лентой или резинкой.\n\n3. Рисование лица\n\nНарисуйте маркером или фломастером лицо на голове. Это может быть:Улыбающееся лицо, чтобы пожелать солнечной погоды.\nПечальное лицо, если вы хотите дождя.\n\n4. Украшение (опционально)\nЕсли хотите, добавьте ленты или нарядите теру бодзу в маленький плащ.\nМожно написать пожелание на свисающей части ткани, например: \"Пусть будет солнечно!\"\n\n5. Подвешивание\nПривяжите верёвочку к верхней части головы или проделайте отверстие в ткани.\nПовесьте теру бодзу у окна, балкона или на улице.\n\nСоветы:\nЕсли вы хотите, чтобы дождь прекратился, повесьте теру бодзу лицом наружу.\nЕсли вы желаете дождя, повесьте её вверх ногами.\nИспользуйте натуральные материалы, чтобы сохранить связь с традицией.\n",
        "materials": ["Бумага 📄", "Ткань 🧵", "Нитки 🧶", "Ленты 🎀"],
        "image": "media/idea/11.png",
    },
    {
        "description": "Елочные игрушки из шишек 🎄",
        "full_description": "Создание оригинальных украшений для елки из шишек и краски.",
        "instruction": "Подготовка шишек:\nСоберите шишки подходящего размера.\nОчистите их от грязи и пыли с помощью щетки или мягкой ткани. Если шишки влажные, оставьте их сушиться на несколько дней в теплом месте.\nПри необходимости прокалите шишки в духовке (100–120°C на 20–30 минут) для уничтожения микробов и раскрытия лепестков.\n\nОкрашивание:\nИспользуйте акриловые или аэрозольные краски золотого, серебряного, белого или любого другого праздничного цвета.\nНаносите краску равномерно, можно покрыть всю поверхность шишки или только ее края для создания эффекта инея.\nДля дополнительного блеска, пока краска не высохла, обсыпьте шишку мелкими блестками.\n\nДекорирование:\nПосле высыхания краски украсьте шишки.\nНамотайте цветную пряжу или декоративные ленты вокруг основания шишки, создавая аккуратные узоры.\nНа макушке шишки прикрепите небольшой декоративный бант из атласной ленты с помощью горячего клея.\n\nСоздание подвеса:\nВозьмите ленту или отрезок прочной пряжи длиной около 10 см.\nПриклейте один конец петли к верхушке шишки или закрепите с помощью горячего клея.\nУбедитесь, что петля надежно держится, чтобы игрушку можно было подвесить на елочную ветку.\n\nФинишные штрихи:\nДля дополнительного праздничного эффекта можно приклеить маленькие стразы, искусственные ягоды или миниатюрные снежинки.\nПокройте готовое изделие тонким слоем прозрачного лака, чтобы закрепить блестки и сохранить яркость краски.\n\nИтог:\nЭти елочные игрушки из шишек добавят натурального шарма и уюта вашему праздничному декору. Каждый элемент можно персонализировать под свою елку, используя разные цвета и украшения.\n",
        "materials": ["Шишки 🌰", "Краска 🎨", "Ленты 🎀"],
        "image": "media/idea/12.png",
    },
    {
        "description": "Миниатюрные цветочные горшки",
        "full_description": "Горшки из пластиковых бутылок с сухоцветами и декором.",
        "instruction": "1. Подготовка основы:\n 1.1. Возьмите пластиковую бутылку и с помощью ножниц или канцелярского ножа отрежьте нижнюю часть. Это будет основа горшочка.\n 1.2. Подкорректируйте высоту основы, в зависимости от желаемого размера горшка (рекомендуемая высота – 4–7 см).\n 1.3. При желании края можно сделать волнистыми, фигурными или закругленными. Для безопасности можно обработать срезы наждачной бумагой.\n\n2. Декорирование пряжей:\n 2.1. Нанесите полоску клея вдоль края или спиралью вокруг всей основы.\n 2.2. Начинайте обмотку пряжей снизу вверх или наоборот. Постепенно добавляйте клей для закрепления. Выбирайте цвета пряжи, подходящие к вашему интерьеру или создайте градиент, комбинируя несколько оттенков.\n 2.3. После завершения обмотки обрежьте пряжу и закрепите конец клеем.\n\n3. Украшение сухоцветами:\n 3.1. Выберите маленькие сухоцветы или отдельные элементы (листочки, веточки, бутоны).\n 3.2. Приклейте их к поверхности горшка в выбранных местах. Вы можете расположить композицию в одном месте или равномерно распределить по всей поверхности.\n 3.3. Если хотите, добавьте бусины или мелкие декоративные элементы для дополнительного акцента.\n\n4. Размещение композиции:\n 4.1. Внутрь горшка можно поместить миниатюрные искусственные растения, декоративный мох или использовать его как вазочку для маленького букета сухоцветов.\n 4.2. Для устойчивости внутрь можно насыпать немного мелких камешков или песка.\n\n5. Финальные штрихи:\n 5.1. Если хотите добавить яркости, украсьте верхний край горшка бантиком из атласной ленты или раскрасьте его акриловой краской.\n 5.2. Покройте изделие тонким слоем лака, чтобы продлить срок службы.\n\nРезультат: Миниатюрные горшки получаются стильными, уютными и функциональными. Они подходят как для домашнего использования, так и для подарков ручной работы. \n",
        "materials": ["Пластиковые бутылки 🍼", "Сухоцветы 🌾", "Пряжа 🧶", "Клей 🧴"],
        "image": "media/idea/13.png",
    },
    {
        "description": "Ключница из декоративных цветов",
        "full_description": "Создайте ключницу с декором из искусственных цветов и картона.",
        "instruction": "1. Подготовка основы: 1.1. Вырежьте из картона прямоугольную или квадратную основу для ключницы. Размеры зависят от того, сколько крючков вы планируете разместить. Обычно размер основы варьируется от 20 см до 30 см в ширину.\n 1.2. Если хотите, можно покрасить картон в желаемый цвет акриловой краской, чтобы он соответствовал интерьеру. Оставьте основу до полного высыхания краски.\n\n2. Декорирование декоративными цветами: 2.1. Выберите декоративные цветы, которые хотите использовать для украшения ключницы. Это могут быть искусственные цветы, высушенные растения или даже элементы из ткани.\n 2.2. Разместите цветы на основе, экспериментируя с их расположением. Можно украсить только один угол, всю поверхность или создать композицию, в центре которой будет большой цветок, а вокруг – маленькие.\n 2.3. После того как выбрали расположение, приклейте цветы на картон с помощью универсального клея или горячего клеевого пистолета. Дайте времени для полного высыхания.\n\n3. Закрепление крючков: 3.1. Из проволоки сделайте маленькие крючки для ключей. Для этого можно просто загнуть проволоку в форме буквы \"S\" или создать небольшие петельки для более декоративного вида.\n 3.2. Прикрепите эти крючки к картону. Для этого с помощью клеевого пистолета или с помощью небольшой скобы можно зафиксировать каждый крючок. Если хотите сделать крючки более устойчивыми, можно также использовать небольшие металлические скобы или гвозди.\n 3.3. Убедитесь, что крючки расположены на нужной высоте и они достаточно крепко зафиксированы.\n\n4. Финальные штрихи: 4.1. Если хотите добавить дополнительный декор, можно приклеить бусины, маленькие ленты или бантики на края картонной основы или рядом с цветами.\n 4.2. Дайте ключнице полностью высохнуть, прежде чем использовать ее для подвешивания ключей.\n",
        "materials": ["Декоративные цветы 🌸", "Картон 📦", "Проволока 🪡", "Клей 🧴"],
        "image": "media/idea/14.png",
    },
    {
        "description": "Ловец света из бисера",
        "full_description": "Создайте декоративный ловец из проволоки и бисера.",
        "instruction": "1. Подготовка основы для шара:\n1.1. Если у вас пенопластовый шарик, его можно использовать как основу.\n 1.2. Если основы нет, сделайте шар самостоятельно. Скатайте тугой шар из мягкого наполнителя, например, синтепона или ткани, затем обмотайте его обычными нитками, чтобы придать форму.\n\n\n 1.3. Убедитесь, что шар ровный и плотный, чтобы удобно вышивать.\n\n2. Обмотка шара пряжей:\n2.1. Начните обматывать основу плотной пряжей, чтобы закрыть всю поверхность шара. Это придаст емугладкость и необходимую текстуру для работы.\n 2.2. Обматывайте шар в разных направлениях, чтобы не оставалось просветов.\n 2.3. Закрепите конец пряжи узелком, спрятав его между витками.\n\n3. Разметка шара:\n3.1. С помощью линейки и карандаша нанесите на шар линии разметки. Обычно разметку делают в виде меридианов, сходящихся на полюсах шара.\n 3.2. Разделите шар на равные сегменты (например, 8 или 12 частей). Чем больше сегментов, тем сложнее будет узор.\n 3.3. Для удобства временно закрепите булавками точки, где линии должны пересекаться.\n\n4. Вышивка узора:\n4.1. Возьмите иглу с большим ушком и вденьте в нее цветное мулине.\n 4.2. Начинайте вышивать узор, следуя линии разметки. Популярные узоры включают звезды, ромбы, цветы и спирали.\n 4.3. Закрепляйте нити, аккуратно прошивая их вокруг витков пряжи. Постепенно двигайтесь от центра узора к краям шара.\n 4.4. Для сложных узоров используйте контрастные цвета нитей, чтобы узор был более выразительным.\n\n5. Завершение работы:\n5.1. После завершения узора спрячьте концы ниток, аккуратно заправив их между витками пряжи илизакрепив с изнанки.\n 5.2. Убедитесь, что узор симметричен и все нити надежно закреплены.\n 5.3. Если хотите, можно пришить маленькую петлю или ленточку, чтобы шар можно было подвесить.\n\nРезультат:\nТемари — это изысканное изделие, которое можно использовать как декоративный элемент, сувенир или даже игрушку. Такие шары символизируют радость и гармонию и могут стать оригинальным подарком, сделанным своими руками!",
        "materials": ["Бисер 🧵", "Проволока 🪡", "Краска 🎨"],
        "image": "media/idea/15.png",
    },
]

answers = [
    "в виде розы",
    "в виде листа",
    "в виде сердца",
    "Лавандовый",
    "Мятно-зелёный",
    "Нежно-розовый",
    "Эфирные масла",
    "блёстки",
    "Глицерин",
]

questions = [
    {
        "text": "Какую форму хотите?",
        "answers": ["в виде розы", "в виде листа", "в виде сердца"],
    },
    {
        "text": "Какой хотите цвет?",
        "answers": ["Лавандовый", "Мятно-зелёный", "Нежно-розовый"],
    },
    {
        "text": "Какие дополнительные элементы хотите добавить?",
        "answers": ["Эфирные масла", "блёстки", "Глицерин"],
    },
]


async def create_data():
    materials = {
        material["name"]: await Material.create(**material)
        for material in materials_data
    }

    # Добавляем идеи
    for idea_data in ideas_data:
        # Получаем материалы для каждой идеи
        idea_materials = [
            materials[material_name] for material_name in idea_data["materials"]
        ]
        idea = await Idea.create(
            description=idea_data["description"],
            instruction=idea_data["instruction"],
            image=idea_data["image"],
        )
        await idea.materials.add(*idea_materials)

    answer_objects = {}
    for ans in answers:
        answer_obj = await Answers.create(answer=ans)
        answer_objects[ans] = answer_obj

    # Теперь создаём вопросы и прикрепляем к ним ответы
    for q_data in questions:
        q_obj = await Question.create(text=q_data["text"])
        # Получаем объекты ответов для данного вопроса
        q_answers = [answer_objects[a] for a in q_data["answers"]]
        await q_obj.answers.add(*q_answers)

    logger.info("Успешное заполнение БД!")
