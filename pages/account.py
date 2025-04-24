import streamlit as st
import hashlib
import sqlite3
import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Константы ---
AVATAR_DIR = "avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)

# --- Язык интерфейса ---
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

# --- Инициализация БД ---
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            login TEXT PRIMARY KEY,
            email TEXT,
            password_hash TEXT,
            signup_date TEXT,
            last_login TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            username TEXT PRIMARY KEY,
            nickname TEXT,
            status TEXT,
            avatar_path TEXT,
            about_me TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS task_stats (
            username TEXT,
            date TEXT,
            solved_tasks INTEGER
        )
    """)

    # --- Миграции ---
    cur.execute("PRAGMA table_info(users)")
    user_columns = [row[1] for row in cur.fetchall()]
    if "signup_date" not in user_columns:
        cur.execute("ALTER TABLE users ADD COLUMN signup_date TEXT")
    if "last_login" not in user_columns:
        cur.execute("ALTER TABLE users ADD COLUMN last_login TEXT")

    cur.execute("PRAGMA table_info(user_profiles)")
    profile_columns = [row[1] for row in cur.fetchall()]
    if "about_me" not in profile_columns:
        cur.execute("ALTER TABLE user_profiles ADD COLUMN about_me TEXT")

    conn.commit()
    conn.close()

init_db()

# --- Аутентификация ---
def create_user(login, email, password_hash):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    try:
        cur.execute("""
            INSERT INTO users (login, email, password_hash, signup_date, last_login)
            VALUES (?, ?, ?, ?, ?)
        """, (login, email, password_hash, now, now))
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
    if user:
        now = datetime.utcnow().isoformat()
        cur.execute("UPDATE users SET last_login = ? WHERE login = ?", (now, login))
        conn.commit()
    conn.close()
    return user is not None

# --- Профиль пользователя ---
def get_user_profile(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT nickname, status, avatar_path, about_me FROM user_profiles WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row if row else ("", "", "", "")

def save_user_profile(username, nickname, status, avatar_path=None, about_me=""):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    if avatar_path:
        cur.execute("""
            INSERT INTO user_profiles (username, nickname, status, avatar_path, about_me)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET nickname=excluded.nickname, status=excluded.status, avatar_path=excluded.avatar_path, about_me=excluded.about_me
        """, (username, nickname, status, avatar_path, about_me))
    else:
        cur.execute("""
            INSERT INTO user_profiles (username, nickname, status, about_me)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET nickname=excluded.nickname, status=excluded.status, about_me=excluded.about_me
        """, (username, nickname, status, about_me))
    conn.commit()
    conn.close()

def get_task_stats(username):
    conn = sqlite3.connect("users.db")
    df = pd.read_sql_query("SELECT date, solved_tasks FROM task_stats WHERE username = ?", conn, params=(username,))
    conn.close()
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
    return df

# --- Главная логика ---
if "username" not in st.session_state:
    tab1, tab2 = st.tabs([t("signin"), t("signup")])

    with tab1:
        st.header(t("signin"))
        with st.form("signin_form"):
            login = st.text_input(t("login"))
            password = st.text_input(t("password"), type="password")
            submit = st.form_submit_button(t("submit_signin"))

            if submit:
                salted_pass = st.session_state["salt"] + password
                password_hash = hashlib.sha256(salted_pass.encode()).hexdigest()
                if authenticate_user(login, password_hash):
                    st.session_state["username"] = login
                    st.success(t("success_signin"))
                    st.rerun()
                else:
                    st.error(t("error_signin"))

    with tab2:
        st.header(t("signup"))
        with st.form("signup_form"):
            login = st.text_input(t("login"), key="signup_login")
            email = st.text_input(t("email"))
            password = st.text_input(t("password"), type="password")
            submit = st.form_submit_button(t("submit_signup"))

            if submit:
                salted_pass = st.session_state["salt"] + password
                password_hash = hashlib.sha256(salted_pass.encode()).hexdigest()
                success = create_user(login, email, password_hash)
                if success:
                    st.session_state["username"] = login
                    st.success(t("success_signup"))
                    st.rerun()
                else:
                    st.error(f"{t('login')} {login} {t('error_signin')}")
else:
    username = st.session_state["username"]
    nickname, status, avatar_path, about_me = get_user_profile(username)

    st.title("👤 Управление аккаунтом")
    st.write(f"Добро пожаловать, **{username}**!")

    # Получение даты регистрации и последнего входа
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT signup_date, last_login FROM users WHERE login = ?", (username,))
    signup_date, last_login = cur.fetchone()
    conn.close()

    st.info(f"📅 Дата регистрации: {signup_date}")
    st.info(f"🕒 Последний вход: {last_login}")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Аватар")
        if avatar_path and os.path.exists(avatar_path):
            st.image(avatar_path, width=120)
        else:
            st.image("https://via.placeholder.com/120", width=120)

        uploaded_file = st.file_uploader("Загрузить аватар", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            avatar_path = os.path.join(AVATAR_DIR, f"{username}{ext}")
            with open(avatar_path, "wb") as f:
                f.write(uploaded_file.read())
            save_user_profile(username, nickname, status, avatar_path, about_me)
            st.success("Аватар обновлён!")
            st.rerun()

    with col2:
        st.subheader("Информация профиля")
        with st.form("profile_form"):
            nickname_input = st.text_input("Никнейм", value=nickname)
            status_input = st.text_input("Статус", value=status, help="Например: 'Начинающий разработчик'")
            about_me_input = st.text_area("О себе (Markdown поддерживается)", value=about_me)
            save_profile = st.form_submit_button("💾 Сохранить изменения")
            if save_profile:
                save_user_profile(username, nickname_input, status_input, avatar_path, about_me_input)
                st.success("Профиль успешно сохранён!")
                st.rerun()

    st.subheader("📝 О себе")
    if about_me:
        st.markdown(about_me)
    else:
        st.info("Пользователь ещё не добавил информацию о себе.")

    st.divider()
    if st.button("🚪 Выйти из аккаунта"):
        st.session_state.clear()
        st.success("Вы вышли из аккаунта!")
        st.rerun()









#    st.subheader("📈 Статистика решённых задач")
#    task_stats_df = get_task_stats(username)
#
#    if not task_stats_df.empty:
#        task_stats_df = task_stats_df.sort_values("date")
#        fig, ax = plt.subplots()
#        ax.plot(task_stats_df["date"], task_stats_df["solved_tasks"], marker="o", linestyle="-")
#        ax.set_title("Прогресс по решённым задачам")
#        ax.set_xlabel("Дата")
#        ax.set_ylabel("Количество задач")
#        ax.grid(True)
#        st.pyplot(fig)
#    else:
#        st.info("Нет данных о решённых задачах. Начните решать задачи, чтобы увидеть прогресс!")


