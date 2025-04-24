import streamlit as st
from st_ant_carousel import st_ant_carousel

content = [
    {
        "style": {"color": "red", "fontSize": "20px"},
        "content": "<b>1. Entry</b>"
    },
    {
        "style": {"color": "blue", "fontSize": "20px"},
        "content": "<b>2. Entry</b>"
    }
]

carousel_style = {
    "background-color": "#f0f2f5",
    "border-radius": "8px",
    "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
    "padding": "20px"
}

st_ant_carousel(content, carousel_style=carousel_style)