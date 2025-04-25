# --- START OF FILE resources.py ---

import streamlit as st
import sqlite3
import os
import base64
from datetime import datetime

# --- Constants ---
RESOURCES_DB = "resources.db"
RESOURCES_DIR = "resource_files"
os.makedirs(RESOURCES_DIR, exist_ok=True)

# --- Language Setup ---
if "lang" not in st.session_state:
    st.session_state["lang"] = "ru"

# --- Session State Initialization ---
if 'editing_resource_id' not in st.session_state:
    st.session_state.editing_resource_id = None

# --- Translations (Keep relevant keys) ---
texts = {
    # ... (translations remain the same) ...
    "page_title": {"ru": "📚 Учебные материалы", "en": "📚 Educational Resources", "by": "📚 Навучальныя матэрыялы"},
    "search_label": {"ru": "🔍 Поиск по названию или описанию:", "en": "🔍 Search by title or description:", "by": "🔍 Пошук па назве або апісанні:"},
    "no_results": {"ru": "Материалы не найдены.", "en": "No resources found.", "by": "Матэрыялы не знойдзены."},
    "download_tooltip": {"ru": "Скачать файл", "en": "Download file", "by": "Спампаваць файл"},
    "edit_tooltip": {"ru": "Редактировать запись", "en": "Edit entry", "by": "Рэдагаваць запіс"},
    "delete_tooltip": {"ru": "Удалить запись", "en": "Delete entry", "by": "Выдаліць запіс"},
    "save_button": {"ru": "💾 Сохранить", "en": "💾 Save", "by": "💾 Захаваць"},
    "cancel_button": {"ru": "❌ Отмена", "en": "❌ Cancel", "by": "❌ Адмена"},
    "file_missing": {"ru": "Файл не найден на сервере.", "en": "File not found on server.", "by": "Файл не знойдзены на серверы."},
    "add_resource_title": {"ru": "➕ Добавить новый ресурс (Админ)", "en": "➕ Add New Resource (Admin)", "by": "➕ Дадаць новы рэсурс (Адмін)"},
    "edit_resource_title": {"ru": "✏️ Редактирование ресурса", "en": "✏️ Editing Resource", "by": "✏️ Рэдагаванне рэсурсу"},
    "title_label": {"ru": "Название:", "en": "Title:", "by": "Назва:"},
    "description_label": {"ru": "Описание (обязательно):", "en": "Description (required):", "by": "Апісанне (абавязкова):"},
    "file_upload_label": {"ru": "Загрузить PDF файл:", "en": "Upload PDF file:", "by": "Загрузіць PDF файл:"},
    "add_button": {"ru": "Добавить ресурс", "en": "Add Resource", "by": "Дадаць рэсурс"},
    "add_success": {"ru": "Ресурс успешно добавлен!", "en": "Resource added successfully!", "by": "Рэсурс паспяхова дададзены!"},
    "update_success": {"ru": "Ресурс успешно обновлен!", "en": "Resource updated successfully!", "by": "Рэсурс паспяхова абноўлены!"},
    "add_error": {"ru": "Ошибка при добавлении ресурса.", "en": "Error adding resource.", "by": "Памылка пры даданні рэсурсу."},
    "update_error": {"ru": "Ошибка при обновлении ресурса.", "en": "Error updating resource.", "by": "Памылка пры абнаўленні рэсурсу."},
    "delete_success": {"ru": "Ресурс удален.", "en": "Resource deleted.", "by": "Рэсурс выдалены."},
    "delete_error": {"ru": "Ошибка при удалении ресурса.", "en": "Error deleting resource.", "by": "Памылка пры выдаленні рэсурсу."},
    "error_file_save": {"ru": "Ошибка при сохранении файла.", "en": "Error saving file.", "by": "Памылка пры захаванні файла."},
    "error_file_delete": {"ru": "Ошибка при удалении файла.", "en": "Error deleting file.", "by": "Памылка пры выдаленні файла."},
    "error_db_insert": {"ru": "Ошибка при добавлении записи в БД.", "en": "Error inserting record into DB.", "by": "Памылка пры даданні запісу ў БД."},
    "error_db_update": {"ru": "Ошибка при обновлении записи в БД.", "en": "Error updating record in DB.", "by": "Памылка пры абнаўленні запісу ў БД."},
    "warning_missing_fields_add": {"ru": "Пожалуйста, укажите название, описание и загрузите PDF файл.", "en": "Please provide a title, description, and upload a PDF file.", "by": "Калі ласка, укажыце назву, апісанне і загрузіце PDF файл."},
    "warning_missing_fields_edit": {"ru": "Название и описание не могут быть пустыми.", "en": "Title and description cannot be empty.", "by": "Назва і апісанне не могуць быць пустымі."},
}

def t(key):
    lang = st.session_state.get("lang", "ru")
    return texts.get(key, {}).get(lang, texts.get(key, {}).get("ru", key))

# --- Database Functions (Remain the same) ---
# ... (Keep all DB functions: init_resources_db, add_resource, update_resource, delete_resource, search_resources, get_all_resources, get_resource_by_id) ...
def init_resources_db():
    """Initializes the resources database and table, ensuring all columns exist."""
    conn = sqlite3.connect(RESOURCES_DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            file_name TEXT NOT NULL UNIQUE,
            upload_date DATETIME DEFAULT CURRENT_TIMESTAMP
            -- last_updated will be added below if needed
        )
    """)
    cur.execute("PRAGMA table_info(resources)")
    existing_columns = {row[1] for row in cur.fetchall()}
    if "last_updated" not in existing_columns:
        try:
            cur.execute("ALTER TABLE resources ADD COLUMN last_updated DATETIME DEFAULT CURRENT_TIMESTAMP")
        except sqlite3.OperationalError as e:
            print(f"Could not add 'last_updated' column: {e}")
    conn.commit()
    conn.close()

def add_resource(title, description, file_name):
    """Adds a new resource record to the database."""
    if not description:
        st.error("Описание не может быть пустым.")
        return False
    conn = sqlite3.connect(RESOURCES_DB)
    cur = conn.cursor()
    now = datetime.now()
    try:
        cur.execute(
            "INSERT INTO resources (title, description, file_name, upload_date, last_updated) VALUES (?, ?, ?, ?, ?)",
            (title, description, file_name, now, now)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed: resources.file_name' in str(e):
             st.error(f"Ошибка: Файл с именем '{file_name}' уже существует в базе данных.")
        elif 'NOT NULL constraint failed: resources.description' in str(e):
             st.error("Ошибка: Описание не может быть пустым (DB constraint).")
        else:
            st.error(f"{t('error_db_insert')}: {e}")
        return False
    except Exception as e:
        st.error(f"{t('error_db_insert')}: {e}")
        return False
    finally:
        conn.close()

def update_resource(resource_id, title, description):
    """Updates an existing resource's title and description."""
    if not description:
        st.error("Описание не может быть пустым.")
        return False
    conn = sqlite3.connect(RESOURCES_DB)
    cur = conn.cursor()
    now = datetime.now()
    try:
        cur.execute(
            "UPDATE resources SET title = ?, description = ?, last_updated = ? WHERE id = ?",
            (title, description, now, resource_id)
        )
        conn.commit()
        return conn.total_changes > 0
    except sqlite3.IntegrityError as e:
         if 'NOT NULL constraint failed: resources.description' in str(e):
             st.error("Ошибка: Описание не может быть пустым (DB constraint).")
         else:
            st.error(f"{t('error_db_update')}: {e}")
         return False
    except Exception as e:
        st.error(f"{t('error_db_update')}: {e}")
        return False
    finally:
        conn.close()

def delete_resource(resource_id):
    conn = sqlite3.connect(RESOURCES_DB)
    cur = conn.cursor()
    try:
        cur.execute("SELECT file_name FROM resources WHERE id = ?", (resource_id,))
        result = cur.fetchone()
        if not result:
            st.error("Resource not found in database.")
            return False
        file_name = result[0]
        cur.execute("DELETE FROM resources WHERE id = ?", (resource_id,))
        conn.commit()
        file_path = os.path.join(RESOURCES_DIR, file_name)
        if os.path.exists(file_path):
            try: os.remove(file_path)
            except OSError as e: st.error(f"{t('error_file_delete')}: {e}")
        return True
    except Exception as e:
        st.error(f"{t('delete_error')}: {e}")
        return False
    finally:
        conn.close()

def search_resources(query):
    conn = sqlite3.connect(RESOURCES_DB)
    cur = conn.cursor()
    search_term = f"%{query}%"
    cur.execute(
        "SELECT id, title, description, file_name FROM resources WHERE title LIKE ? OR description LIKE ? ORDER BY title",
        (search_term, search_term)
    )
    results = cur.fetchall()
    conn.close()
    return results

def get_all_resources():
    conn = sqlite3.connect(RESOURCES_DB)
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, file_name FROM resources ORDER BY title")
    results = cur.fetchall()
    conn.close()
    return results

def get_resource_by_id(resource_id):
    conn = sqlite3.connect(RESOURCES_DB)
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, file_name FROM resources WHERE id = ?", (resource_id,))
    result = cur.fetchone()
    conn.close()
    return result

# --- Helper Function for Downloads (Remains the same) ---
def create_download_button(file_path, tooltip_text, key):
    """Generates an icon-only download button for a file."""
    try:
        with open(file_path, "rb") as f:
            bytes_data = f.read()
        st.download_button(
            label="📥",
            data=bytes_data,
            file_name=os.path.basename(file_path),
            mime='application/pdf',
            key=key,
            help=tooltip_text,
            use_container_width=True
        )
    except FileNotFoundError:
        st.error(" ", icon="⚠️")
    except Exception as e:
        st.error(f"Error generating download link: {e}", icon="🔥")


# --- Initialize Database ---
init_resources_db()

# --- Streamlit Page Content ---
st.title(t("page_title"))

# --- CSS for Cards (Updated for stricter height control) ---
# --- CSS for Cards (Using Line Clamp for Truncation) ---
card_css = """
<style>
/* Target the container Streamlit creates for st.container(border=True) */
div[data-testid="stVerticalBlock"] div[data-testid="element-container"] > div[data-testid="stVerticalBlock"] {
    /* === Fixed Height & Flex Layout === */
    height: 250px !important;      /* --- ADJUST FIXED HEIGHT HERE --- */
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important; /* Push title up, buttons down */
    padding: 12px 15px !important;
    overflow: hidden !important;   /* Hide overflow from the main card */
    margin-bottom: 15px !important;
    border: 1px solid rgba(49, 51, 63, 0.2);
    border-radius: 0.5rem;
}

/* Style for the title (h5) inside the card */
div[data-testid="stVerticalBlock"] div[data-testid="element-container"] > div[data-testid="stVerticalBlock"] h5 {
    font-size: 1.1em;
    font-weight: 600;
    margin-bottom: 8px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    line-height: 1.3;
    flex-shrink: 0; /* Title should not shrink */
}

/* Style for the description (st.caption -> div.stCaption) inside the card */
div[data-testid="stVerticalBlock"] div[data-testid="element-container"] > div[data-testid="stVerticalBlock"] .stCaption {
    /* --- Line Clamp Properties --- */
    overflow: hidden !important;
    text-overflow: ellipsis; /* Fallback for browsers not supporting line-clamp fully */
    display: -webkit-box !important;
    -webkit-line-clamp: 3 !important; /* --- ADJUST MAX NUMBER OF LINES HERE --- */
    -webkit-box-orient: vertical !important;
    /* --- End Line Clamp --- */

    /* Remove properties related to scrolling/growing */
    /* Remove: flex-grow: 1; */
    /* Remove: overflow-y: auto; */
    /* Remove: min-height: 0; */

    margin-bottom: 12px;    /* Space between description and buttons */
    line-height: 1.4;
    font-size: 0.9em;
    color: #ccc;
}

/* Container for the buttons (stHorizontalBlock) */
div[data-testid="stVerticalBlock"] div[data-testid="element-container"] > div[data-testid="stVerticalBlock"] [data-testid="stHorizontalBlock"] {
     gap: 0.5rem;
     flex-shrink: 0; /* Buttons row should not shrink */
     width: 100%;
}


/* Style for the individual buttons inside the card */
div[data-testid="stVerticalBlock"] div[data-testid="element-container"] > div[data-testid="stVerticalBlock"] .stButton>button {
    padding: 5px 8px !important;
    font-size: 1.1em;
    height: auto;
    min-height: 30px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%; /* Button fills its column */
}

</style>
"""
st.markdown(card_css, unsafe_allow_html=True) # Inject the CSS
# --- Admin Section to Add Resources (Keep as before) ---
with st.expander(t("add_resource_title"), expanded=False):
    # ... (add resource form remains the same) ...
    with st.form("add_resource_form", clear_on_submit=True):
        new_title = st.text_input(t("title_label"))
        new_description = st.text_area(t("description_label"))
        uploaded_file = st.file_uploader(t("file_upload_label"), type=["pdf"])
        submitted = st.form_submit_button(t("add_button"))
        if submitted:
            if new_title and new_description and uploaded_file:
                file_name = uploaded_file.name
                save_path = os.path.join(RESOURCES_DIR, file_name)
                try:
                    with open(save_path, "wb") as f: f.write(uploaded_file.getbuffer())
                except Exception as e: st.error(f"{t('error_file_save')}: {e}")
                else:
                    if add_resource(new_title, new_description, file_name):
                        st.success(t("add_success"))
                        st.rerun()
                    else:
                        if os.path.exists(save_path):
                             try: os.remove(save_path)
                             except: pass
            else: st.warning(t("warning_missing_fields_add"))


# --- Edit Form Section (Keep as before) ---
if st.session_state.editing_resource_id is not None:
    # ... (edit resource form remains the same) ...
    resource_data = get_resource_by_id(st.session_state.editing_resource_id)
    if resource_data:
        res_id, current_title, current_description, _ = resource_data
        st.subheader(f"{t('edit_resource_title')}: {current_title}")
        with st.form(key=f"edit_form_{res_id}"):
            edited_title = st.text_input(t("title_label"), value=current_title)
            edited_description = st.text_area(t("description_label"), value=current_description)
            col1, col2 = st.columns(2)
            with col1: save_button = st.form_submit_button(t("save_button"), use_container_width=True)
            with col2: cancel_button = st.form_submit_button(t("cancel_button"), use_container_width=True)
            if save_button:
                if edited_title and edited_description:
                    if update_resource(res_id, edited_title, edited_description):
                        st.success(t("update_success"))
                        st.session_state.editing_resource_id = None
                        st.rerun()
                    else: pass
                else: st.warning(t("warning_missing_fields_edit"))
            elif cancel_button:
                st.session_state.editing_resource_id = None
                st.rerun()
    else:
        st.error("Ресурс для редактирования не найден.")
        st.session_state.editing_resource_id = None
        st.rerun()


# --- Search Bar (Keep as before) ---
search_query = st.text_input(t("search_label"))

# --- Display Resources in Cards (Simplified Structure) ---
st.divider()

if search_query:
    resources = search_resources(search_query)
else:
    resources = get_all_resources()

if resources:
    num_resources = len(resources)
    num_cols = 4

    for i in range(0, num_resources, num_cols):
        cols = st.columns(num_cols) # 4 columns for the cards
        for j in range(num_cols):
            resource_index = i + j
            if resource_index < num_resources:
                res_id, title, description, file_name = resources[resource_index]
                file_path = os.path.join(RESOURCES_DIR, file_name)

                with cols[j]:
                    # Card container - CSS applies based on structure
                    with st.container(border=True): # border=True helps target with CSS

                        # --- Direct Content (No Wrapper Needed) ---
                        st.markdown(f"<h5>{title}</h5>", unsafe_allow_html=True)
                        st.caption(description) # CSS will truncate this directly
                        # --- End Direct Content ---

                        # --- Button Row ---
                        action_cols = st.columns(3) # 3 equal columns

                        with action_cols[0]: # Download
                            if os.path.exists(file_path):
                                create_download_button(file_path, t("download_tooltip"), key=f"dl_{res_id}")
                            else:
                                st.error(" ", icon="⚠️")

                        with action_cols[1]: # Edit
                            if st.button("✏️", key=f"edit_{res_id}", help=t("edit_tooltip"), use_container_width=True):
                                st.session_state.editing_resource_id = res_id
                                st.rerun()

                        with action_cols[2]: # Delete
                            if st.button("🗑️", key=f"del_{res_id}", type="secondary", help=t("delete_tooltip"), use_container_width=True):
                                if delete_resource(res_id):
                                    st.toast(t("delete_success"), icon="✅")
                                    if st.session_state.editing_resource_id == res_id:
                                        st.session_state.editing_resource_id = None
                                    st.rerun()
                                else:
                                    pass # Error handled in function
                        # --- End Button Row ---
else:
    st.info(t("no_results"))
# --- END OF FILE resources.py ---