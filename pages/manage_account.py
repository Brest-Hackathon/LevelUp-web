import streamlit as st
import sqlite3
import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

# --- Константы ---
AVATAR_DIR = "avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)

# --- Инициализация БД ---
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    # Таблица профиля
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            username TEXT PRIMARY KEY,
            nickname TEXT,
            status TEXT,
            avatar_path TEXT
        )
    """)
    # Таблица статистики задач
    cur.execute("""
        CREATE TABLE IF NOT EXISTS task_stats (
            username TEXT,
            date TEXT,
            solved_tasks INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Вспомогательные функции ---
def get_user_profile(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT nickname, status, avatar_path FROM user_profiles WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row if row else ("", "", "")

def save_user_profile(username, nickname, status, avatar_path=None):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    if avatar_path:
        cur.execute("""
            INSERT INTO user_profiles (username, nickname, status, avatar_path)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET nickname=excluded.nickname, status=excluded.status, avatar_path=excluded.avatar_path
        """, (username, nickname, status, avatar_path))
    else:
        cur.execute("""
            INSERT INTO user_profiles (username, nickname, status)
            VALUES (?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET nickname=excluded.nickname, status=excluded.status
        """, (username, nickname, status))
    conn.commit()
    conn.close()

def get_task_stats(username):
    conn = sqlite3.connect("users.db")
    df = pd.read_sql_query("SELECT date, solved_tasks FROM task_stats WHERE username = ?", conn, params=(username,))
    conn.close()
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
    return df

# --- Проверка авторизации ---
if "username" not in st.session_state:
    st.warning("⚠️ Вы не авторизованы. Пожалуйста, войдите в систему, чтобы просматривать и редактировать свой профиль.")
    st.stop()

# --- Получение текущего пользователя ---
username = st.session_state.username

# --- Загрузка данных профиля ---
nickname, status, avatar_path = get_user_profile(username)

st.title("👤 Управление аккаунтом")
st.write(f"Добро пожаловать, **{username}**!")

# --- Разметка профиля ---
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Аватар")
    if avatar_path and os.path.exists(avatar_path):
        st.image(avatar_path, width=120)
    else:
        st.image("https://via.placeholder.com/120", width=120)

    uploaded_file = st.file_uploader("Загрузить аватар", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        avatar_path = os.path.join(AVATAR_DIR, f"{username}.png")
        with open(avatar_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("Аватар обновлён!")

with col2:
    st.subheader("Информация профиля")
    with st.form("profile_form"):
        nickname_input = st.text_input("Никнейм", value=nickname)
        status_input = st.text_input("Статус", value=status, help="Например: 'Начинающий разработчик'")

        save_profile = st.form_submit_button("💾 Сохранить изменения")
        if save_profile:
            save_user_profile(username, nickname_input, status_input, avatar_path)
            st.success("Профиль успешно сохранён!")

# --- Статистика решённых задач ---
st.subheader("📈 Статистика решённых задач")

task_stats_df = get_task_stats(username)

if not task_stats_df.empty:
    task_stats_df = task_stats_df.sort_values("date")
    fig, ax = plt.subplots()
    ax.plot(task_stats_df["date"], task_stats_df["solved_tasks"], marker="o", linestyle="-")
    ax.set_title("Прогресс по решённым задачам")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Количество задач")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("Нет данных о решённых задачах. Начните решать задачи, чтобы увидеть прогресс!")

# --- Выход из аккаунта ---
st.divider()
logout = st.button("🚪 Выйти из аккаунта")
if logout:
    st.session_state.clear()
    st.success("Вы вышли из аккаунта!")
