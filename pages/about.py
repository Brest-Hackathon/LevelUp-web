import streamlit as st
import streamlit.components.v1 as components
import os
import base64

# Установка языка по умолчанию
if "lang" not in st.session_state:
    st.session_state["lang"] = "ru"

# Функция для base64-кодирования изображений
def get_base64_image(path):
    try:
        with open(path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    except FileNotFoundError:
        return "https://via.placeholder.com/150"

# Переводы
translations = {
    "title": {
        "ru": "О платформе",
        "en": "About the Platform",
        "be": "Аб платформе"
    },
    "subheader": {
        "ru": "Наша миссия: сделать обучение увлекательным и эффективным",
        "en": "Our mission: to make learning fun and effective",
        "be": "Наша місія: зрабіць навучанне цікавым і эфектыўным"
    },
    "description": {
        "ru": """
Добро пожаловать на нашу платформу, где школьная программа превращается в интерактивные игры для легкого запоминания!
... (обрезано для краткости)
""",
        "en": """Welcome to our platform where the school curriculum turns into interactive games for easy memorization!
...""",
        "be": """Сардэчна запрашаем на нашу платформу, дзе школьная праграма ператвараецца ў інтэрактыўныя гульні...
..."""
    },
    "our_team": {
        "ru": "Наша команда",
        "en": "Our Team",
        "be": "Наша каманда"
    },
    "team_members": [
        {
            "name": {"ru": "Афанасьев Иван", "en": "Ivan Afanasiev", "be": "Іван Афанасьеў"},
            "role": {"ru": "Разработчик", "en": "Developer", "be": "Распрацоўшчык"},
            "image": "ivan.jpg",
            "description": {"ru": "фронтенд и основной функционал.", "en": "Frontend and core functionality.", "be": "Фронтэнд і функцыянал."}
        },
        {
            "name": {"ru": "Демешко Виктор", "en": "Demeshko Victor", "be": "Дымешка Віктар"},
            "role": {"ru": "Разработчик", "en": "Developer", "be": "Распрацоўшчык"},
            "image": "viktor.jpg",
            "description": {"ru": "БД Взаимодействия, АПИ.", "en": "DB interactions, API.", "be": "БД узаемадзеяння, API."}
        },
        {
            "name": {"ru": "Кузмич Максим", "en": "Maxim Kuzmich", "be": "Максім Кузьміч"},
            "role": {"ru": "Разработчик", "en": "Developer", "be": "Распрацоўшчык"},
            "image": "maxim.jpg",
            "description": {"ru": "алгоритм генерации карточек.", "en": "Card generation algorithm.", "be": "Алгарытм генерацыі картак."}
        },
        {
            "name": {"ru": "Смехович Константин", "en": "Konstantin Smekhovich", "be": "Канстанцін Смеховіч"},
            "role": {"ru": "UI-UX дизайнер", "en": "UI-UX Designer", "be": "UI-UX дызайнер"},
            "image": "kostya.jpg",
            "description": {"ru": "дизайн страниц.", "en": "Page design.", "be": "Дызайн старонак."}
        },
        {
            "name": {"ru": "Мисирук Маргарита", "en": "Margarita Misiruk", "be": "Маргарыта Місірук"},
            "role": {"ru": "Аналитик", "en": "Analyst", "be": "Аналітык"},
            "image": "rita.jpg",
            "description": {"ru": "анализ пользователей.", "en": "User analysis.", "be": "Аналіз карыстальнікаў."}
        },
        {
            "name": {"ru": "Коляда Виталий", "en": "Vitaliy Kolyada", "be": "Віталь Каляда"},
            "role": {"ru": "UI-UX дизайнер", "en": "UI-UX Designer", "be": "UI-UX дызайнер"},
            "image": "Vitaly.jpg",
            "description": {"ru": "дизайн страниц.", "en": "Page design.", "be": "Дызайн старонак."}
        },
        {
            "name": {"ru": "Старжинский Владислав", "en": "Vladislav Starzhinsky", "be": "Уладзіслаў Старжынскі"},
            "role": {"ru": "Аналитик", "en": "Analyst", "be": "Аналітык"},
            "image": "vladik.jpg",
            "description": {"ru": "анализ пользователей.", "en": "User analysis.", "be": "Аналіз карыстальнікаў."}
        }
    ],
    "goals": {
        "ru": "Наши цели и принципы",
        "en": "Our Goals and Principles",
        "be": "Нашы мэты і прынцыпы"
    },
    "goals_list": {
        "ru": [
            "**Доступность:** каждый школьник должен иметь возможность найти интересный способ запоминания материала.",
            "**Инновационность:** мы применяем современные технологии.",
            "**Обратная связь:** мы ценим мнение пользователей.",
            "**Сотрудничество:** открыты к партнёрствам."
        ],
        "en": [
            "**Accessibility:** every student should find an easy way to memorize.",
            "**Innovation:** we use modern technologies.",
            "**Feedback:** we value user opinions.",
            "**Cooperation:** open for partnerships."
        ],
        "be": [
            "**Даступнасць:** кожны школьнік павінен мець цікавы спосаб запамінання.",
            "**Інавацыйнасць:** ужываем сучасныя тэхналогіі.",
            "**Зваротная сувязь:** шануем меркаванне карыстальнікаў.",
            "**Супрацоўніцтва:** адкрыты да партнёрства."
        ]
    },
    "contacts": {
        "ru": "Контакты",
        "en": "Contacts",
        "be": "Кантакты"
    },
    "contact_info": {
        "ru": """
Связаться с нами:
- Email: afanasieffivan@gmail.com
- Телефон: +375 (44) 508-85-75
- GitHub: https://github.com/LevelUP-platform
""",
        "en": """Contact us:
- Email: afanasieffivan@gmail.com
- Phone: +375 (44) 508-85-75
- GitHub: https://github.com/LevelUP-platform
""",
        "be": """Звяжыцеся з намі:
- Email: afanasieffivan@gmail.com
- Тэлефон: +375 (44) 508-85-75
- GitHub: https://github.com/LevelUP-platform
"""
    },
    "conclusion": {
        "ru": "Спасибо, что выбираете нас! Вместе мы сделаем обучение доступным!",
        "en": "Thank you for choosing us! Together we make learning accessible!",
        "be": "Дзякуй, што абралі нас! Разам зробім навучанне даступным!"
    }
}

# Функция перевода
def t(key):
    lang = st.session_state.get("lang", "ru")
    value = translations.get(key)
    if isinstance(value, dict):
        return value.get(lang, value.get("ru"))
    elif isinstance(value, list):
        if key == "team_members":
            return [
                {
                    "name": m["name"].get(lang, m["name"]["ru"]),
                    "role": m["role"].get(lang, m["role"]["ru"]),
                    "description": m["description"].get(lang, m["description"]["ru"]),
                    "image": m["image"]
                } for m in value
            ]
        return [item.get(lang, item.get("ru", "")) if isinstance(item, dict) else item for item in value]
    return value

# ===== Рендер =====

st.title(t("title"))
st.subheader(t("subheader"))
st.markdown(t("description"))

st.markdown(f"### {t('our_team')}")

# Карусель
carousel_html = """
<style>
.carousel-container {
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 15px;
}
.team-card {
    display: inline-block;
    background: #f5f5f5;
    border-radius: 8px;
    padding: 10px;
    margin-right: 15px;
    width: 200px;
    vertical-align: top;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.team-card img {
    width: 100%;
    border-radius: 4px;
}
.team-card h4 {
    margin: 8px 0 2px 0;
    font-size: 16px;
}
.team-card h5 {
    font-size: 14px;
    margin: 2px 0 8px 0;
    color: #555;
    font-weight: normal;
}
.team-card p {
    font-size: 13px;
}
</style>
<div class="carousel-container">
"""

for member in t("team_members"):
    image_path = os.path.join("images", member["image"])
    image_data = get_base64_image(image_path)
    carousel_html += f"""
    <div class="team-card">
        <img src="{image_data}" alt="{member['name']}">
        <h4>{member['name']}</h4>
        <h5>{member['role']}</h5>
        <p>{member['description']}</p>
    </div>
    """

carousel_html += "</div>"

components.html(carousel_html, height=420, scrolling=True)

# Цели
st.markdown(f"### {t('goals')}")
for item in t("goals_list"):
    st.markdown(item)

# Контакты
st.markdown(f"### {t('contacts')}")
st.markdown(t("contact_info"))

# Заключение
st.markdown(t("conclusion"))
