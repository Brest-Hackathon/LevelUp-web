import streamlit as st
import sqlite3
import os

AVATAR_PLACEHOLDER = "https://via.placeholder.com/80"

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

# --- Интерфейс ---
st.title("🔎 Поиск пользователей")

search_query = st.text_input("Введите никнейм для поиска")

if search_query:
    users = search_users_by_nickname(search_query)
    if users:
        for username, nickname, avatar_path in users:
            col1, col2 = st.columns([1, 5])
            with col1:
                if avatar_path and os.path.exists(avatar_path):
                    st.image(avatar_path, width=80)
                else:
                    st.image(AVATAR_PLACEHOLDER, width=80)
            with col2:
                st.subheader(nickname or username)
                st.write(f"[@{username}](?user={username})")
                if st.button(f"🔍 Открыть профиль {nickname or username}", key=username):
                    st.query_params["user"] = username
                    st.switch_page("pages/public_profile.py")
    else:
        st.info("Пользователь не найден.")
else:
    st.info("Введите часть никнейма для поиска.")
