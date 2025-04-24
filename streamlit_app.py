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
        st.experimental_rerun()  # This triggers instant rerun to apply language

# Define your pages
pages = {
    t("home"): [
        st.Page("pages/about.py", title=t("learn_about_us")),
    ],
    t("your_account"): [
        st.Page("pages/create_account.py", title=t("create_your_account")),
        st.Page("pages/manage_account.py", title=t("manage_your_account")),
    ],
    t("resources"): [
        st.Page("pages/demo.py", title=t("try_it_out")),
    ],
}

pg = st.navigation(pages)
pg.run()
