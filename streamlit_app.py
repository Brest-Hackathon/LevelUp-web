import streamlit as st

# Set default language if not already set
if 'lang' not in st.session_state:
    st.session_state["lang"] = "ru"

# Define the translation dictionary
translations = {
    "en": {
        "language_selection": "Language selection",
        "current_language": "Current language is",
        "home": "Home",
        "your_account": "Your account",
        "resources": "Resources",
        "learn_about_us": "Learn about us",
        "create_your_account": "Enter your account",
        "manage_your_account": "Manage your account",
        "try_it_out": "Try it out",
        "community": "Community",
        "join_chat": "Join our chat",
        "forum": "Forum",
        "cards": "Cards",
        "study_space": "Studying Space",
        "community": "🌐 Community"
    },
    "ru": {
        "language_selection": "Выбор языка",
        "current_language": "Текущий язык",
        "home": "Главная",
        "your_account": "Ваш аккаунт",
        "resources": "Ресурсы",
        "learn_about_us": "Узнайте о нас",
        "create_your_account": "Войти в аккаунт",
        "manage_your_account": "Управление аккаунтом",
        "try_it_out": "Попробуйте",
        "community": "Сообщество",
        "join_chat": "Присоединяйтесь к чату",
        "forum": "Форум",
        "cards": "Карточки",
        "study_space": "Место для учебы",
        "community": "🌐 Сообщество",
    },
    "by": {
        "language_selection": "Выбар мовы",
        "current_language": "Бягучая мова",
        "home": "Галоўная",
        "your_account": "Ваш уліковы запіс",
        "resources": "Рэсурсы",
        "learn_about_us": "Даведайцеся пра нас",
        "create_your_account": "Стварыць уліковы запіс",
        "manage_your_account": "Кіраванне ўліковым запісам",
        "try_it_out": "Паспрабуйце",
        "community": "Супольнасць",
        "join_chat": "Далучайцеся да чату",
        "forum": "Форум",
        "cards": "Карточкі",
        "study_space": "Месца для вучобы",
        "community": "🌐 Супольнасць",
    },
}

# Translation function
def t(key):
    lang = st.session_state["lang"]
    return translations.get(lang, {}).get(key, key)

# Sidebar language selection
with st.sidebar:
    lang_map = {
        "EN 🇬🇧": "en",
        "RU 🇷🇺": "ru",
        "BY 🇧🇾": "by"
    }
    selected = st.radio(t("language_selection"), list(lang_map.keys()), index=list(lang_map.values()).index(st.session_state["lang"]))
    new_lang = lang_map[selected]
    
    if st.session_state["lang"] != new_lang:
        st.session_state["lang"] = new_lang
        st.rerun()  # This triggers instant rerun to apply language

# Define your pages
pages = {
    t("home"): [
        st.Page("pages/about.py", title=t("learn_about_us")),
    ],
    t("your_account"): [
        st.Page("pages/account.py", title=t("Account settings")),
    ],
    t("community"): [
        st.Page("pages/community.py", title=t("join_chat")),
        st.Page("pages/forum.py", title=t("forum")),
    ],
    t("study_space"): [
        st.Page("pages/cards.py", title=t("cards"))
    ]
}

pg = st.navigation(pages)
pg.run()
