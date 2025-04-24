import streamlit as st
import streamlit.components.v1 as components

# Ensure default language is set
if "lang" not in st.session_state:
    st.session_state["lang"] = "ru"  # Default language

# Translation map
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
Мы уверены, что обучение должно быть не только полезным, но и захватывающим. Наша цель – повысить мотивацию и
эффективность усвоения знаний через игровые механики, адаптированные к современным образовательным требованиям.

Наша команда объединяет экспертов в области образования, IT и гейм-дизайна. Используя современные технологии ИИ, включая
модели наподобие ChatGPT, мы генерируем уникальные и интересные задания, флеш-карты, викторины и интерактивные сценарии, 
превращая традиционное обучение в увлекательное приключение!
""",
        "en": """
Welcome to our platform where the school curriculum turns into interactive games for easy memorization!
We believe that learning should be not only useful but also exciting. Our goal is to increase motivation and the
efficiency of knowledge absorption through game mechanics adapted to modern educational requirements.

Our team brings together experts in education, IT, and game design. Using modern AI technologies, including
models like ChatGPT, we generate unique and interesting tasks, flashcards, quizzes, and interactive scenarios,
transforming traditional learning into an exciting adventure!
""",
        "be": """
Сардэчна запрашаем на нашу платформу, дзе школьная праграма ператвараецца ў інтэрактыўныя гульні для лёгкага запамінання!
Мы ўпэўнены, што навучанне павінна быць не толькі карысным, але і захапляльным. Наша мэта – павысіць матывацыю і
эфектыўнасць засваення ведаў праз гульнявыя механікі, адаптаваныя да сучасных адукацыйных патрабаванняў.

Наша каманда аб'ядноўвае экспертаў у галіне адукацыі, IT і гейм-дызайну. Выкарыстоўваючы сучасныя тэхналогіі ШІ, уключаючы
мадэлі накшталт ChatGPT, мы генеруем унікальныя і цікавыя заданні, флэш-карткі, віктарыны і інтэрактыўныя сцэнарыі, 
ператвараючы традыцыйнае навучанне ў захапляльнае прыгоду!
"""
    },
    "our_team": {
        "ru": "Наша команда",
        "en": "Our Team",
        "be": "Наша каманда"
    },
    "team_members": [
        {
            "name": {
                "ru": "Афанасьев Иван",
                "en": "Ivan Afanasiev",
                "be": "Іван Афанасьеў"
            },
            "role": {
                "ru": "Разработчик",
                "en": "Developer",
                "be": "Распрацоўшчык"
            },
            "image": "https://via.placeholder.com/150",
            "description": {
                "ru": "фронтенд и основной функционал.",
                "en": "Responsible for frontend and core functionality.",
                "be": "Адказвае за фронтэнд і асноўны функцыянал."
            }
        },
        {
            "name": {
                "ru": "Демешко Виктор",
                "en": "Victor Demeshko",
                "be": "Віктар Дземешка"
            },
            "role": {
                "ru": "Разработчик",
                "en": "Developer",
                "be": "Распрацоўшчык"
            },
            "image": "https://via.placeholder.com/150",
            "description": {
                "ru": "БД и АПИ взаимодействия.",
                "en": "Responsible for database and API interactions.",
                "be": "Адказвае за базу даных і API ўзаемадзеяння."
            }
        },
        {
            "name": {
                "ru": "Кузмич Максим",
                "en": "Maxim Kuzmich",
                "be": "Максім Кузьміч"
            },
            "role": {
                "ru": "Разработчик",
                "en": "Developer",
                "be": "Распрацоўшчык"
            },
            "image": "https://via.placeholder.com/150",
            "description": {
                "ru": "алгоритм генерации карточек.",
                "en": "Responsible for card generation algorithm.",
                "be": "Адказвае за алгарытм генерацыі картак."
            }
        },
        {
            "name": {
                "ru": "Старжинский Владислав",
                "en": "Vladislav Starzhinsky",
                "be": "Уладзіслаў Старжынскі"
            },
            "role": {
                "ru": "Аналитик",
                "en": "Analyst",
                "be": "Аналітык"
            },
            "image": "https://via.placeholder.com/150",
            "description": {
                "ru": "Провел анализ аналогов и среднестатистического пользователя.",
                "en": "Conducted analysis of analogs and the average user.",
                "be": "Правёў аналіз аналагаў і сярэднестатыстычнага карыстальніка."
            }
        },
        {
            "name": {
                "ru": "Мисирук Маргарита",
                "en": "Margarita Misiruk",
                "be": "Маргарыта Місірук"
            },
            "role": {
                "ru": "Аналитик",
                "en": "Analyst",
                "be": "Аналітык"
            },
            "image": "https://via.placeholder.com/150",
            "description": {
                "ru": "Провела анализ аналогов и среднестатистического пользователя.",
                "en": "Conducted analysis of analogs and the average user.",
                "be": "Правяла аналіз аналагаў і сярэднестатыстычнага карыстальніка."
            }
        },
        {
            "name": {
                "ru": "Коляда Виталий",
                "en": "Vitaliy Kolyada",
                "be": "Віталь Каляда"
            },
            "role": {
                "ru": "UI-UX дизайнер",
                "en": "UI-UX Designer",
                "be": "UI-UX дызайнер"
            },
            "image": "https://via.placeholder.com/150",
            "description": {
                "ru": "дизайн страниц.",
                "en": "Responsible for page design.",
                "be": "Адказвае за дызайн старонак."
            }
        },
        {
            "name": {
                "ru": "Смехович Константин",
                "en": "Konstantin Smekhovich",
                "be": "Канстанцін Смеховіч"
            },
            "role": {
                "ru": "UI-UX дизайнер",
                "en": "UI-UX Designer",
                "be": "UI-UX дызайнер"
            },
            "image": "https://via.placeholder.com/150",
            "description": {
                "ru": "дизайн страниц.",
                "en": "Responsible for page design.",
                "be": "Адказвае за дызайн старонак."
            }
        }
    ],
    "goals": {
        "ru": "Наши цели и принципы",
        "en": "Our Goals and Principles",
        "be": "Нашы мэты і прынцыпы"
    },
    "goals_list": {
        "ru": [
            "**Доступность:** каждый школьник должен иметь возможность найти интересный и понятный способ запоминания материала.",
            "**Инновационность:** мы активно применяем современные технологии, чтобы повысить качество образовательного процесса.",
            "**Обратная связь:** мы ценим мнение наших пользователей и постоянно работаем над улучшением платформы.",
            "**Сотрудничество:** открыты к партнёрствам с образовательными учреждениями и экспертами для развития экосистемы интерактивного образования."
        ],
        "en": [
            "**Accessibility:** every student should be able to find an interesting and approachable way to memorize material.",
            "**Innovation:** we actively use modern technologies to improve the quality of the learning process.",
            "**Feedback:** we value our users' opinions and constantly work on improving the platform.",
            "**Cooperation:** open to partnerships with educational institutions and experts to develop the interactive education ecosystem."
        ],
        "be": [
            "**Даступнасць:** кожны школьнік павінен мець магчымасць знайсці цікавы і зразумелы спосаб запамінання матэрыялу.",
            "**Інавацыйнасць:** мы актыўна ўжываем сучасныя тэхналогіі, каб павысіць якасць адукацыйнага працэсу.",
            "**Зваротная сувязь:** мы шанаваем меркаванне нашых карыстальнікаў і пастаянна працуем над паляпшэннем платформы.",
            "**Супрацоўніцтва:** адкрыты да партнёрства з адукацыйнымі ўстановамі і экспертамі для развіцця экасістэмы інтэрактыўнай адукацыі."
        ]
    },
    "contacts": {
        "ru": "Контакты",
        "en": "Contacts",
        "be": "Кантакты"
    },
    "contact_info": {
        "ru": """
Если у вас есть вопросы, предложения или вы хотите сотрудничать с нами, пожалуйста, свяжитесь с нами:
- Электронная почта: afanasieffivan@gmail.com
- Телефон: +375 (44) 508-85-75
- Наша GitHub страница: https://github.com/Brest-Hackathon
""",
        "en": """
If you have questions, suggestions or want to collaborate with us, please contact us:
- Email: afanasieffivan@gmail.com
- Phone: +375 (44) 508-85-75
- Our GitHub page: https://github.com/Brest-Hackathon
""",
        "be": """
Калі ў вас ёсць пытанні, прапановы або вы хочаце супрацоўнічаць з намі, калі ласка, звяжыцеся з намі:
- Электронная пошта: afanasieffivan@gmail.com
- Тэлефон: +375 (44) 508-85-75
- Наша GitHub старонка: https://github.com/Brest-Hackathon
"""
    },
    "conclusion": {
        "ru": """
Спасибо, что выбираете нас для своего образовательного пути. Вместе мы сделаем обучение интересным и доступным для каждого!
""",
        "en": """
Thank you for choosing us for your educational journey. Together we will make learning interesting and accessible for everyone!
""",
        "be": """
Дзякуй, што абралі нас для свайго адукацыйнага шляху. Разам мы зробім навучанне цікавым і даступным для кожнага!
"""
    }
}

# Helper function to get translation based on the current language
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

# Render the page
st.title(t("title"))
st.subheader(t("subheader"))
st.markdown(t("description"))

# Team Section
st.markdown(f"### {t('our_team')}")

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
    carousel_html += f"""
    <div class="team-card">
        <img src="{member['image']}" alt="{member['name']}">
        <h4>{member['name']}</h4>
        <h5>{member['role']}</h5>
        <p>{member['description']}</p>
    </div>
    """

carousel_html += "</div>"

components.html(carousel_html, height=350, scrolling=True)

# Goals
st.markdown(f"### {t('goals')}")
for item in t("goals_list"):
    st.markdown(item)

# Contacts
st.markdown(f"### {t('contacts')}")
st.markdown(t("contact_info"))

# Conclusion
st.markdown(t("conclusion"))
