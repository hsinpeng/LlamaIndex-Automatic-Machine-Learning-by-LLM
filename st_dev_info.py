import streamlit as st
import time, random

# Streaming word by word of a line
def stream_words(line):
    for word in line.split():
        yield word + " "
        time.sleep(random.uniform(0.02, 0.05))

# Display developer's information
def developer_info_stream(app_title:str="The application", author:str="Sheldon Hsin-Peng Lin", email:str="hsinpeng168@gmail.com", github:str="https://github.com/hsinpeng"):
    time.sleep(2)
    st.write(stream_words(f":grey[{app_title} is developed with ❤️ by *{author}*.]")) 
    st.write(stream_words(f":grey[Please feel free to contact me via] :blue[{email}] :grey[or] :blue[[GitHub]({github})]:grey[.]"))

def developer_info_static(app_title:str="The application", author:str="Sheldon Hsin-Peng Lin", email:str="hsinpeng168@gmail.com", github:str="https://github.com/hsinpeng"):
    st.write(f":grey[{app_title} is developed with ❤️ by *{author}*.]")
    st.write(f":grey[Please feel free to contact me via] :blue[{email}] :grey[or] :blue[[GitHub]({github})]:grey[.]")

def developer_info_simple_stream(author:str="Sheldon Hsin-Peng Lin", email:str="hsinpeng168@gmail.com", github:str="https://github.com/hsinpeng"):
    time.sleep(2)
    st.write(stream_words(f":grey[Developed with ❤️ by *{author}*. Contact me via] :blue[{email}] :grey[or] :blue[[GitHub]({github})]:grey[.]"))

def developer_info_simple_static(author:str="Sheldon Hsin-Peng Lin", email:str="hsinpeng168@gmail.com", github:str="https://github.com/hsinpeng"):
    st.write(f":grey[Developed with ❤️ by *{author}*. Contact me via] :blue[{email}] :grey[or] :blue[[GitHub]({github})]:grey[.]")

def developer_info_simple_html(author:str="Sheldon Hsin-Peng Lin", email:str="hsinpeng168@gmail.com"):
    footer_html = f"""<div style='text-align: center;'>
    <p>Developed with ❤️ by <i>{author}</i> (<a href= "mailto: {email}">{email}</a>)</p>
    </div>"""
    st.markdown(footer_html, unsafe_allow_html=True)