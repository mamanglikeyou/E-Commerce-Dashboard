import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    full_df = pd.read_csv('data/full_df.csv')
    rfm = pd.read_csv('data/rfm.csv')
    return full_df, rfm

full_df, rfm = load_data()


st.title("📊 E-Commerce Data Analysis Dashboard")
st.markdown("""
Dashboard ini menampilkan hasil analisis data e-commerce berdasarkan
segmentasi pelanggan (RFM) dan distribusi geografis.
""")

st.sidebar.header("Filter Data")

segment_option = st.sidebar.multiselect(
    "Pilih Segment Pelanggan:",
    options=rfm['segment'].unique(),
    default=rfm['segment'].unique()
)

filtered_rfm = rfm[rfm['segment'].isin(segment_option)]


st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Pelanggan", filtered_rfm['customer_id'].nunique())
col2.metric("Total Revenue", f"{filtered_rfm['monetary'].sum():,.0f}")
col3.metric("Jumlah Segmen", filtered_rfm['segment'].nunique())


st.subheader("Segmentasi Pelanggan (RFM)")

fig1, ax1 = plt.subplots()
sns.countplot(
    data=filtered_rfm,
    x='segment',
    order=filtered_rfm['segment'].value_counts().index,
    ax=ax1
)
ax1.set_xlabel("Segmen")
ax1.set_ylabel("Jumlah Pelanggan")
ax1.set_title("Distribusi Segmentasi Pelanggan")
plt.xticks(rotation=30)
st.pyplot(fig1)


st.subheader("Revenue per Segmen")

segment_revenue = (
    filtered_rfm.groupby('segment')['monetary']
    .sum()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots()
segment_revenue.plot(kind='bar', ax=ax2)
ax2.set_xlabel("Segmen")
ax2.set_ylabel("Total Revenue")
ax2.set_title("Total Revenue Berdasarkan Segmen")
plt.xticks(rotation=30)
st.pyplot(fig2)


st.subheader("Top 10 State Berdasarkan Revenue")

state_revenue = (
    full_df.groupby('customer_state')['payment_value']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig3, ax3 = plt.subplots()
state_revenue.plot(kind='bar', ax=ax3)
ax3.set_xlabel("State")
ax3.set_ylabel("Total Revenue")
ax3.set_title("Top 10 State Berdasarkan Revenue")
plt.xticks(rotation=30)
st.pyplot(fig3)


st.markdown("---")
st.caption("")