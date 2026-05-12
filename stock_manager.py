import streamlit as st

import pandas as pd

import json

import os

FILE = "sample_stock.json"

def load_stock():

if not os.path.exists(FILE):

return []

with open(FILE, "r") as f:

return json.load(f)

def save_stock(data):

with open(FILE, "w") as f:

json.dump(data, f)

def stock_page():

st.header(" Sheet Stock Manager")

stock = load_stock()

thickness = st.number_input("Thickness", value=5.0)

material = st.selectbox("Material", ["MS", "SS"])

width = st.number_input("Sheet Width", value=2440)

height = st.number_input("Sheet Height", value=1220) "material": material,

"thickness": thickness,

"width": width,

"height": height,

"qty": qty

})

save_stock(stock)

if stock:

df = pd.DataFrame(stock)

st.dataframe(df)
