import streamlit as st
import pandas as pd
import numpy as np

URL = "https://www.pilio.idv.tw/lto539/list.asp"

@st.cache_data
def load_data():
    tables = pd.read_html(URL)
    df = tables[0]
    numbers = df.iloc[:,2:7]
    numbers = numbers.apply(pd.to_numeric)
    return numbers

def analyze(numbers):

    last10 = numbers.head(10)
    last30 = numbers.head(30)
    last100 = numbers.head(100)

    def freq(data):
        return pd.Series(data.values.ravel()).value_counts()

    f10 = freq(last10)
    f30 = freq(last30)
    f100 = freq(last100)

    scores = {}

    for i in range(1,40):
        scores[i] = f10.get(i,0)*4 + f30.get(i,0)*3 + f100.get(i,0)*2

    return scores


def predict(scores):

    sorted_nums = sorted(scores.items(), key=lambda x:x[1], reverse=True)

    pool = [x[0] for x in sorted_nums[:10]]

    strong6 = pool[:6]

    bets = []

    for i in range(5):
        bet = sorted(np.random.choice(pool,5,replace=False))
        bets.append(bet)

    return pool,strong6,bets


numbers = load_data()

scores = analyze(numbers)

pool,strong6,bets = predict(scores)


st.title("🎯 539 AI 預測系統")

st.header("今日最強6碼")
st.write(strong6)

st.header("高機率號碼池")
st.write(pool)

st.header("推薦5注")

for b in bets:
    st.write(b)
