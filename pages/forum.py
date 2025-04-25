import streamlit as st
import sqlite3
import os
from datetime import datetime

AVATAR_PLACEHOLDER = "https://via.placeholder.com/80"

# --- Создание новых колонок в таблице user_profiles, если они еще не существуют ---
def add_columns_to_user_profiles():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Добавляем колонки, если их нет
    try:
        cur.execute("""
        ALTER TABLE user_profiles
        ADD COLUMN last_login TEXT;
        """)
    except sqlite3.OperationalError:
        pass  # Игнорируем ошибку, если колонка уже существует

    try:
        cur.execute("""
        ALTER TABLE user_profiles
        ADD COLUMN signup_date TEXT;
        """)
    except sqlite3.OperationalError:
        pass  # Игнорируем ошибку, если колонка уже существует

    try:
        cur.execute("""
        ALTER TABLE user_profiles
        ADD COLUMN description TEXT;
        """)
    except sqlite3.OperationalError:
        pass  # Игнорируем ошибку, если колонка уже существует

    conn.commit()
    conn.close()

add_columns_to_user_profiles()

# --- Получение пользователей с фильтрацией ---
def search_users_by_nickname(query):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT username, nickname, avatar_path FROM user_profiles
        WHERE nickname LIKE ?
        ORDER BY nickname COLLATE NOCASE
    """, (f"%{query}%",))
    results = cur.fetchall()
    conn.close()
    return results

# --- Получение информации о пользователе ---
def get_user_info(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT username, nickname, avatar_path, status, last_login, signup_date, description
        FROM user_profiles
        WHERE username = ?
    """, (username,))
    result = cur.fetchone()
    conn.close()
    return result

# --- Регистрация нового пользователя ---
def register_user(username, nickname, password, status):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    signup_date = datetime.now().strftime('%Y-%m-%d')
    last_login = signup_date  # Устанавливаем last_login в момент регистрации
    description = ""  # Default description if not provided

    cur.execute("""
    INSERT INTO user_profiles (username, nickname, password, status, signup_date, last_login, description)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, nickname, password, status, signup_date, last_login, description))

    conn.commit()
    conn.close()

# --- Обновление времени последнего входа пользователя ---
def update_last_login(username):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur.execute("""
    UPDATE user_profiles
    SET last_login = ?
    WHERE username = ?
    """, (last_login, username))

    conn.commit()
    conn.close()

# --- Интерфейс ---
st.title("🔎 Поиск пользователей")

# Проверяем, на какой странице мы находимся
if "selected_user" in st.session_state:
    username = st.session_state["selected_user"]
    
    # Добавим кнопку "Назад"
    if st.button("◀️ Назад к поиску"):
        del st.session_state["selected_user"]
        st.rerun()

    # Отображаем информацию о профиле
    user = get_user_info(username)
    if user:
        username, nickname, avatar_path, status, last_login, signup_date, description = user
        
        # Используем колонки для красивого отображения
        col1, col2 = st.columns([1, 5])
        with col1:
            if avatar_path and os.path.exists(avatar_path):
                st.image(avatar_path, width=100)
            else:
                st.image(AVATAR_PLACEHOLDER, width=100)
        
        with col2:
            st.title(f"👤 Профиль: {nickname or username}")
            st.markdown(f"**Никнейм:** {nickname}")
            st.markdown(f"**Username:** @{username}")
            st.markdown(f"**Статус:** {status}")

            # Отображение дополнительных данных
            st.subheader("Дополнительная информация")

            # Safely display dates
            if signup_date:
                try:
                    st.markdown(f"**Дата регистрации:** {datetime.strptime(signup_date, '%Y-%m-%d').strftime('%d %B %Y')}")
                except ValueError:
                    st.markdown("**Дата регистрации:** Не корректная дата")
            else:
                st.markdown("**Дата регистрации:** Не указана")

            if last_login:
                try:
                    st.markdown(f"**Последний вход:** {datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S').strftime('%d %B %Y, %H:%M')}")
                except ValueError:
                    st.markdown("**Последний вход:** Не корректная дата")
            else:
                st.markdown("**Последний вход:** Не был выполнен")

            # Safely handle description
            if description:
                st.markdown(f"**Описание:** {description}")
            else:
                st.markdown("**Описание:** Отсутствует")

    else:
        st.error("Пользователь не найден.")
else:
    # Страница поиска пользователей
    search_query = st.text_input("Введите никнейм для поиска")

    if search_query:
        users = search_users_by_nickname(search_query)
        if users:
            st.subheader("Результаты поиска:")
            for username, nickname, avatar_path in users:
                col1, col2 = st.columns([1, 5])
                with col1:
                    if avatar_path and os.path.exists(avatar_path):
                        st.image(avatar_path, width=80)
                    else:
                        st.image(AVATAR_PLACEHOLDER, width=80)
                with col2:
                    st.subheader(nickname or username)
                    st.write(f"@{username}")
                    if st.button(f"🔍 Открыть профиль {nickname or username}", key=username):
                        st.session_state["selected_user"] = username
                        st.rerun()  # Перезагружаем страницу, чтобы показать профиль
        else:
            st.info("Пользователь не найден.")
    else:
        st.info("Введите часть никнейма для поиска.")
