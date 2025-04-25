import streamlit as st
import sqlite3
import os
from PIL import Image

# --- Константы ---
AVATAR_DIR = "avatars"

def get_user_data_by_nickname(nickname):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT u.login, p.nickname, p.status, p.avatar_path, u.signup_date, u.last_login, p.about_me
        FROM users u
        JOIN user_profiles p ON u.login = p.username
        WHERE p.nickname = ?
    """, (nickname,))
    row = cur.fetchone()
    conn.close()
    return row

st.title("🔍 Поиск пользователя по никнейму")

search_nickname = st.text_input("Введите никнейм:")

if search_nickname:
    user_data = get_user_data_by_nickname(search_nickname)
    if user_data:
        login, nickname, status, avatar_path, signup_date, last_login, about_me = user_data

        st.subheader(f"👤 Профиль: {nickname}")
        col1, col2 = st.columns([1, 3])

        with col1:
            if avatar_path and os.path.exists(avatar_path):
                st.image(avatar_path, width=120)
            else:
                st.image("https://via.placeholder.com/120", width=120)

        with col2:
            st.markdown(f"**Username:** @{login}")
            st.markdown(f"**Статус:** {status or 'Не указан'}")

            st.markdown("### Дополнительная информация")
            st.markdown(f"📅 **Дата регистрации:** {signup_date or 'Не указана'}")
            st.markdown(f"🕒 **Последний вход:** {last_login or 'Не был выполнен'}")
            st.markdown(f"📝 **Описание:** {about_me or 'Отсутствует'}")
    else:
        st.warning("Пользователь с таким никнеймом не найден.")
