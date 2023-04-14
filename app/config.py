import streamlit as st

hide_streamlit_style = """
    <style> 
        footer {visibility: hidden;} 
        footer:after { 
            content:' ';  
            visibility: visible; 
            display: block; 
            position: relative; 
            #background-color: red; 
            padding: 5px; 
            top: 2px;
        }

        .css-1y4p8pa {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>"""
