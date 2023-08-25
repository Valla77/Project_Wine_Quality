import numpy as np 
import pandas as pd 
import joblib
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

import streamlit as st
from streamlit_echarts import st_echarts

from PIL import Image
from keras.models import load_model
import tensorflow as tf
import dill
import lime
import lime.lime_tabular
from lime import lime_text
from lime.lime_text import LimeTextExplainer
# Load  model  
model = load_model('mon_modele4.h5')

with open('explainer', 'rb') as f: explainer = dill.load(f)
data = pd.read_csv('wines.csv', sep=',')


## Config
st.set_page_config(
    page_title="Wine Quality",
    page_icon="🍷",
    layout="wide"
)


st.write("""
# Wine Quality Prediction 
This app predicts the ** Quality of Wine **  using **wine features** input via the **side panel** 
""")

#read in wine image and render with streamlit
image = Image.open('20658849lpw-20659153-article-jpg_7333136_1250x625.jpg')
st.image(image, caption='wine company',use_column_width=True)

st.sidebar.header('User Input Parameters') #user input parameter collection with streamlit side bar


def get_user_input():
    """
    this function is used to get user input using sidebar slider and selectbox 
    return type : pandas dataframe
    """
    wine_type = st.sidebar.selectbox("Select Wine type",('white', 'red'))
    fixed_acidity = st.sidebar.slider('fixed acidity', 3.8, 15.9, 7.0)
    volatile_acidity = st.sidebar.slider('volatile acidity', 0.08, 1.58, 0.4)
    citric_acid  = st.sidebar.slider('citric acid', 0.0, 1.66, 0.3)
    residual_sugar  = st.sidebar.slider('residual_sugar', 0.6, 65.8, 10.4)
    chlorides  = st.sidebar.slider('chlorides', 0.009, 0.611, 0.211)
    free_sulfur_dioxide = st.sidebar.slider('free sulfur dioxide', 1, 289, 200)
    total_sulfur_dioxide = st.sidebar.slider('total sulfur dioxide', 6, 440, 150)
    density = st.sidebar.slider('density', 0.98, 1.03, 1.0)
    pH = st.sidebar.slider('pH', 2.72, 4.01, 3.0)
    sulphates = st.sidebar.slider('sulphates', 0.22, 2.0, 1.0)
    alcohol = st.sidebar.slider('alcohol', 8.0, 14.9, 13.4)
    
    
    features = {
            'fixed acidity': fixed_acidity,
            'volatile acidity': volatile_acidity,
            'citric acid': citric_acid,
            'residual sugar': residual_sugar,
            'chlorides': chlorides,
            'free sulfur dioxide': free_sulfur_dioxide,
            'total sulfur dioxide': total_sulfur_dioxide,
            'density': density,
            'pH': pH,
            'sulphates': sulphates,
            'alcohol': alcohol,
            'type': [0 if wine_type == 'white' else 1]
            }
    data = pd.DataFrame(features,index=[0])
    data_np = data.to_numpy()
    data_np = data_np.astype(np.float32)
    my_tensor = tf.constant(data_np)
    prediction = model.predict(my_tensor)
    # Convertir la prédiction en un tableau numpy de type entier
    prediction_int = prediction.astype(np.int32)
    
    
    return data, prediction_int, data_np

user_input_df = get_user_input()




st.subheader('User Input parameters')
st.write(user_input_df[0])
# st.subheader('Predictions')
# st.subheader(pd.DataFrame(user_input_df[1]).values.tolist()[0][0])

# st.metric(label="Prediction", value=pd.DataFrame(user_input_df[1]).values.tolist()[0][0])

value=pd.DataFrame(user_input_df[1]).values.tolist()[0][0]
def grade_formatter(value):
    if value == 0.875:
        return 'Grade A'
    elif value == 0.625:
        return 'Grade B'
    elif value == 0.375:
        return 'Grade C'
    elif value == 0.125:
        return 'Grade D'
    else:
        return ''


option = {
  "series": [
    {
      "type": "gauge",
      "startAngle": 180,
      "endAngle": 0,
      "center": ["50%", "75%"],
      "radius": "90%",
      "min": 0,
      "max": 10,
      "splitNumber": 10,
      "axisLine": {
        "lineStyle": {
          "width": 6,
          "color": [
            [0.3, "#FF6E76"],
            [0.7, "#FDDD60"],
            # [0.75, "#58D9F9"],
            [1, "#7CFFB2"]
          ]
        }
      },
      "pointer": {
        "icon": "path://M12.8,0.7l12,40.1H0.7L12.8,0.7z",
        "length": "12%",
        "width": 20,
        "offsetCenter": [0, "-60%"],
        "itemStyle": {
          "color": "inherit"
        }
      },
      "axisTick": {
        "length": 12,
        "lineStyle": {
          "color": "inherit",
          "width": 2
        }
      },
      "splitLine": {
        "length": 20,
        "lineStyle": {
          "color": "inherit",
          "width": 5
        }
      },
      "axisLabel": {
        "color": "#464646",
        "fontSize": 20,
        "distance": -60,
        "rotate": "tangential",
        # "formatter": grade_formatter
      },
      "title": {
        "offsetCenter": [0, "-10%"],
        "fontSize": 20
      },
      "detail": {
        "fontSize": 30,
        "offsetCenter": [0, "-35%"],
        "valueAnimation": True,
        # "formatter": "{value}",
        "color": "inherit"
      },
      "data": [
        {
          "value": value,
          "name": "Prediction"
        }
      ]
    }
  ]
}

st_echarts(option, height="500px")


data_row = user_input_df[2]
# st.write(model)
exp = explainer.explain_instance(
    data_row=data_row[0], 
    predict_fn=model.predict
 )

# afficher l'explication dans Streamlit
# exp.show_in_notebook(show_table=True)
fig = exp.as_pyplot_figure()
fig.set_facecolor('none')
st.pyplot(fig)
# st.markdown(exp.as_html(), unsafe_allow_html=True)    

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
    # AgGrid(data)
    
# Put app closer
st.markdown("---")
st.markdown("Copyright \u00A9 2023 Kamila Catoire & Valérie Muthiani & Arnold Yayi")
