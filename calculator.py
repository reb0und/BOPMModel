import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

def bopm(option_type: int, S_0: float, K: float, T: float, r: float, sigma: float, n: int):
    u = np.exp(sigma * np.sqrt(T/n))
    d = 1/u 
    p = (np.exp(r * T/n) - d) / (u - d)
    stock_tree = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        for j in range(i + 1):
            stock_tree[j, i] = S_0 * (u ** (i - j)) * (d ** j)
    
    option_tree = np.zeros((n + 1, n + 1))
    for j in range(n+1):
        if option_type == 0:
            option_tree[j, n] = max(0, stock_tree[j, n] - K)
        else:
            option_tree[j, n] = max(0, K - stock_tree[j, n])
    
    for i in range(n - 1, -1, -1):
        for j in range(i + 1): # iter over tree branches
            option_tree[j, i] = (np.exp(-r * (T/n))) * (p * option_tree[j, i + 1] + (1 - p) * option_tree[j + 1, i + 1])

    return stock_tree, option_tree, option_tree[0, 0]

bopm(0, 100, 100, 1, 0.05, 0.2, 1)

st.title('Binomial Tree Option Pricing Calculator')

st.write('This is a simple calculator for option pricing using the binomial tree model.')
option_type = st.selectbox('Option Type', ['Call', 'Put'])
S_0 = st.number_input('Initial Stock Price (S_0)', 100.0)
K = st.number_input('Srike Price (K)', 100.0)
T = st.number_input('Time to Maturity in years (T)', 1)
r = st.number_input('Risk-free rate (r)', 0.05)
sigma = st.number_input('Volatility (sigma)', 0.2)
n = st.number_input('Number of steps (n)', 10)
if st.button('Calculate'):
    if option_type == 'Call':
        option_type = 0
    else:
        option_type = 1

    stock_tree, option_tree, price = bopm(option_type, S_0, K, T, r, sigma, n)

    st.write(f'Theoretical option price: {price}')
    st.subheader('Stock Tree')
    st.dataframe(pd.DataFrame(stock_tree))

    st.write('Option Tree')
    st.dataframe(pd.DataFrame(option_tree))
    
    fig, ax = plt.subplots()
    cax = ax.matshow(stock_tree, cmap='viridis')
    fig.colorbar(cax)
    st.pyplot(fig)

    fig, ax = plt.subplots()
    cax = ax.matshow(option_tree, cmap='viridis')
    fig.colorbar(cax)
    st.pyplot(fig)