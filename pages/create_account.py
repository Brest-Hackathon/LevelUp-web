import streamlit as st
import hashlib
import sqlite3

# --- Language setup ---
if 'lang' not in st.session_state:
    st.session_state["lang"] = "ru"

if 'salt' not in st.session_state:
    st.session_state["salt"] = st.secrets["salt"]

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

# --- Database setup ---
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            login TEXT PRIMARY KEY,
            email TEXT,
            password_hash TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            username TEXT PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()

def ensure_user_profiles_columns():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(user_profiles)")
    existing_columns = {row[1] for row in cur.fetchall()}

    columns_to_add = {
        "nickname": "TEXT",
        "status": "TEXT",
        "avatar_path": "TEXT"
    }

    for column, definition in columns_to_add.items():
        if column not in existing_columns:
            cur.execute(f"ALTER TABLE user_profiles ADD COLUMN {column} {definition}")
    
    conn.commit()
    conn.close()

def create_user(login, email, password_hash):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (login, email, password_hash) VALUES (?, ?, ?)", (login, email, password_hash))
        cur.execute("INSERT INTO user_profiles (username) VALUES (?)", (login,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(login, password_hash):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE login = ? AND password_hash = ?", (login, password_hash))
    user = cur.fetchone()
    conn.close()
    return user is not None

# Initialize DB and ensure schema is complete
init_db()
ensure_user_profiles_columns()

# --- UI Tabs ---
tab1, tab2 = st.tabs([t("signin"), t("signup")])

# --- LOG IN TAB ---
with tab1:
    st.header(t("signin"))
    with st.form("signin_form"):
        login = st.text_input(t("login"), key="signin_login")
        password = st.text_input(t("password"), type="password", key="signin_password")
        submit = st.form_submit_button(t("submit_signin"))

        if submit:
            salted_pass = st.session_state["salt"] + password
            password_hash = hashlib.sha256(salted_pass.encode()).hexdigest()
            if authenticate_user(login, password_hash):
                st.session_state["username"] = login
                st.success(t("success_signin"))
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
            salted_pass = st.session_state["salt"] + password
            password_hash = hashlib.sha256(salted_pass.encode()).hexdigest()
            success = create_user(login, email, password_hash)
            if success:
                st.session_state["username"] = login
                st.success(t("success_signup"))
            else:
                st.error(f"{t('login')} {login} {t('error_signin')}")
