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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            username TEXT PRIMARY KEY,
            nickname TEXT,
            status TEXT,
            avatar_path TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS task_stats (
            username TEXT,
            date TEXT,
            solved_tasks INTEGER
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

# --- Получение профиля пользователя ---
def get_user_profile(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT nickname, status, avatar_path FROM user_profiles WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row if row else ("", "", "")

# --- Сохранение профиля пользователя ---
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

# --- Получение статистики задач ---
def get_task_stats(username):
    conn = sqlite3.connect("users.db")
    df = pd.read_sql_query("SELECT date, solved_tasks FROM task_stats WHERE username = ?", conn, params=(username,))
    conn.close()
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
    return df

# --- Инициализация ---
init_db()
ensure_user_profiles_columns()

# --- Проверка авторизации ---
if "username" not in st.session_state:
    st.warning("⚠️ Вы не авторизованы. Пожалуйста, войдите в систему.")
    st.stop()

username = st.session_state["username"]
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
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        avatar_path = os.path.join(AVATAR_DIR, f"{username}{ext}")
        with open(avatar_path, "wb") as f:
            f.write(uploaded_file.read())
        save_user_profile(username, nickname, status, avatar_path)
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

# --- Кнопка выхода ---
st.divider()
if st.button("🚪 Выйти из аккаунта"):
    st.session_state.clear()
    st.success("Вы вышли из аккаунта!")
