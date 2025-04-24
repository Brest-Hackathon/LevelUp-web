import streamlit as st
import streamlit.components.v1 as components

# Заголовок
st.title("О платформе")
st.subheader("Наша миссия: сделать обучение увлекательным и эффективным")

# Описание проекта
st.markdown("""
Добро пожаловать на нашу платформу, где школьная программа превращается в интерактивные игры для легкого запоминания!
Мы уверены, что обучение должно быть не только полезным, но и захватывающим. Наша цель – повысить мотивацию и
эффективность усвоения знаний через игровые механики, адаптированные к современным образовательным требованиям.

Наша команда объединяет экспертов в области образования, IT и гейм-дизайна. Используя современные технологии ИИ, включая
модели наподобие ChatGPT, мы генерируем уникальные и интересные задания, флеш-карты, викторины и интерактивные сценарии, 
превращая традиционное обучение в увлекательное приключение!
""")

# Команда
st.markdown("### Наша команда")

# Define team members
team_members = [
    {
        "name": "Афанасьев Иван",
        "role": "Разработчик",
        "image": "https://via.placeholder.com/150",
        "description": "Отвечает за фронтенд и основной функционал."
    },
    {
        "name": "Демешко Виктор",
        "role": "Разработчик",
        "image": "https://via.placeholder.com/150",
        "description": "Отвечает за БД и АПИ взаимодействия."
    },
    {
        "name": "Кузмич Максим",
        "role": "Разработчик",
        "image": "https://via.placeholder.com/150",
        "description": "Отвечает за алгоритм генерации карточек."
    },
    {
        "name": "Старжинский Владислав",
        "role": "Аналитик",
        "image": "https://via.placeholder.com/150",
        "description": "Провел анализ аналогов и среднестатистического пользователя."
    },
    {
        "name": "Мисирук Маргарита",
        "role": "Аналитик",
        "image": "https://via.placeholder.com/150",
        "description": "Провела анализ аналогов и среднестатистического пользователя."
    },
    {
        "name": "Коляда Виталий",
        "role": "UI-UX дизайнер",
        "image": "https://via.placeholder.com/150",
        "description": "Отвечает за дизайн страниц."
    },
    {
        "name": "Смехович Константин",
        "role": "UI-UX дизайнер",
        "image": "https://via.placeholder.com/150",
        "description": "Отвечает за дизайн страниц."
    }
]

# Build the HTML for the horizontal carousel
carousel_html = """
<style>
.carousel-container {
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 15px;
}
.team-card {
    display: inline-block;
    background: #f5f5f5;
    border-radius: 8px;
    padding: 10px;
    margin-right: 15px;
    width: 200px;
    vertical-align: top;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.team-card img {
    width: 100%;
    border-radius: 4px;
}
.team-card h4 {
    margin: 8px 0 2px 0;
    font-size: 16px;
}
.team-card h5 {
    font-size: 14px;
    margin: 2px 0 8px 0;
    color: #555;
    font-weight: normal;
}
.team-card p {
    font-size: 13px;
}
</style>

<div class="carousel-container">
"""

# Append each team member as a card
for member in team_members:
    carousel_html += f"""
    <div class="team-card">
        <img src="{member['image']}" alt="{member['name']}">
        <h4>{member['name']}</h4>
        <h5>{member['role']}</h5>
        <p>{member['description']}</p>
    </div>
    """

carousel_html += "</div>"

# Render the HTML as an iframe using components.html
components.html(carousel_html, height=325, scrolling=True)

# Наши цели и принципы
st.markdown("### Наши цели и принципы")
st.markdown("""
- **Доступность:** каждый школьник должен иметь возможность найти интересный и понятный способ запоминания материала.
- **Инновационность:** мы активно применяем современные технологии, чтобы повысить качество образовательного процесса.
- **Обратная связь:** мы ценим мнение наших пользователей и постоянно работаем над улучшением платформы.
- **Сотрудничество:** открыты к партнёрствам с образовательными учреждениями и экспертами для развития экосистемы интерактивного образования.
""")

# Контакты
st.markdown("### Контакты")
st.markdown("""
Если у вас есть вопросы, предложения или вы хотите сотрудничать с нами, пожалуйста, свяжитесь с нами:
- Электронная почта: afanasieffivan@gmail.com
- Телефон: +375 (44) 508-85-75
- Наша GitHub страница: https://github.com/Brest-Hackathon
""")

# Заключение
st.markdown("""
Спасибо, что выбираете нас для своего образовательного пути. Вместе мы сделаем обучение интересным и доступным для каждого!
""")
