"""
En esta pagina debe poder visualizarse la cara de Hewo.
En el navbar podemos poner sliders para los valores de la cara.
La cara se visualiza en la ventana principal.
Debajo de la ventana habrá un input para escribir el nombre de la expresión. Junto a un botón para guardar la expresión.
La expresion se almacena en un dataframe, que puede ser consultado justo debajo de la ventana de visualización de la cara.
"""
import streamlit as st


class ExpressionEditor:
    def __init__(self):
        st.title("HeWo Expression Editor")
        st.write("""
        ### Instructions:
        - Use the sliders in the navbar to change the expression of HeWo's face. 
        - Save the emotion by typing the name of the expression in the input box and clicking the save button.
        """)
        self.emotion_var_sliders()

    def emotion_var_sliders(self):
        st.sidebar.title("Emotion Variables")
        st.sidebar.slider("Happiness", 0, 100, 50)

if __name__ == '__main__':
    ExpressionEditor()
