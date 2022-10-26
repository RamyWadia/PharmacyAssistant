from logging import PlaceHolder
from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype,
)
import pandas as pd
import streamlit as st

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")
    if not modify:
        return None

    df = df.copy()
    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter products on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Pleace, select {column} range:",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            else:
                user_text_input = right.text_input(
                    f"Please, Type {column} name:")
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

Excel_file = 'Source.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(Excel_file,engine='openpyxl',sheet_name=sheet_name,usecols='A:C',header=0)
st.dataframe(filter_dataframe(df))
















