import streamlit as st
import hashlib
from xata.client import Client

# Ensure language is set
if 'lang' not in st.session_state:
    st.session_state["lang"] = "ru"

if 'salt' not in st.session_state:
    st.session_state["salt"] = st.secrets["salt"]

# Initialize Xata client
xata = Client.from_url('https://<your_workspace>.xata.sh/<your_region>/<your_database>', api_key="<your_api_key>")

# Localized text
texts = {
    "signup": {"ru": "Регистрация", "en": "Sign Up", "by": "Рэгістрацыя"},
    "signin": {"ru": "Вход", "en": "Log In", "by": "Увайсці"},
    "login": {"ru": "Логин", "en": "Login", "by": "Лагін"},
    "email": {"ru": "Электронная почта", "en": "Email", "by": "Электронная пошта"},
    "password": {"ru": "Пароль", "en": "Password", "by": "Пароль"},
    "submit_signup": {"ru": "Зарегистрироваться", "en": "Sign Up", "by": "Зарэгістравацца"},
    "submit_signin": {"ru": "Войти", "en": "Log In", "by": "Увайсці"},
    "success_signup": {"ru": "Вы успешно зарегистрированы!", "en": "You have successfully signed up!", "by": "Вы паспяхова зарэгістраваліся!"},
    "success_signin": {"ru": "Вход выполнен успешно!", "en": "Logged in successfully!", "by": "Уваход выкананы паспяхова!"},
    "error_signin": {"ru": "Неверный логин или пароль.", "en": "Invalid login or password.", "by": "Няправільны лагін або пароль."}
}

def t(key):
    lang = st.session_state["lang"]
    return texts.get(key, {}).get(lang, key)

# UI tabs
tab1, tab2 = st.tabs([t("signin"), t("signup")])

# --- LOG IN TAB ---
with tab1:
    st.header(t("signin"))
    with st.form("signin_form"):
        login = st.text_input(t("login"), key="signin_login")
        password = st.text_input(t("password"), type="password", key="signin_password")
        submit = st.form_submit_button(t("submit_signin"))

        if submit:
            # Query Xata database for the user
            result = xata.db.users.filter(login=login).get()
            if result:
                user = result[0]
                salted_pass = st.session_state["salt"] + password
                password_hash = hashlib.sha256(salted_pass.encode()).hexdigest()
                if password_hash == user["password_hash"]:
                    st.success(t("success_signin"))
                else:
                    st.error(t("error_signin"))
            else:
                st.error(t("error_signin"))

# --- SIGN UP TAB ---
with tab2:
    st.header(t("signup"))
    with st.form("signup_form"):
        login = st.text_input(t("login"), key="signup_login")
        email = st.text_input(t("email"), key="signup_email")
        password = st.text_input(t("password"), type="password", key="signup_password")
        submit = st.form_submit_button(t("submit_signup"))

        if submit:
            # Check if login already exists
            result = xata.db.users.filter(login=login).get()
            if result:
                st.error(f"{t('login')} {login} {t('error_signin')}")
            else:
                salted_pass = st.session_state["salt"] + password
                password_hash = hashlib.sha256(salted_pass.encode()).hexdigest()
                # Insert new user into the Xata database
                xata.db.users.create({
                    "login": login,
                    "email": email,
                    "password_hash": password_hash
                })
                st.success(t("success_signup"))
