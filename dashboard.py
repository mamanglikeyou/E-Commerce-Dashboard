import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

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

full_df['order_purchase_timestamp'] = pd.to_datetime(
    full_df['order_purchase_timestamp']
)

min_date = full_df['order_purchase_timestamp'].min().date()
max_date = full_df['order_purchase_timestamp'].max().date()


st.title("📊 E-Commerce Data Analysis Dashboard")
st.markdown("""
Dashboard ini menampilkan hasil analisis data e-commerce berdasarkan
segmentasi pelanggan (RFM) dan distribusi geografis.
""")

# SIDEBAR FILTER
st.sidebar.header("Filter Data")

# Filter Tanggal
st.sidebar.subheader("Filter Tanggal")

start_date = st.sidebar.date_input(
    "Tanggal Mulai",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "Tanggal Akhir",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# Filter Segmen
st.sidebar.subheader("Filter Segmen Pelanggan")

segment_list = ['All Segments'] + sorted(rfm['segment'].unique().tolist())

selected_segment = st.sidebar.selectbox(
    "Pilih Segmen",
    options=segment_list,
    index=0
)

# Filter tanggal (untuk transaksi & geografi)
filtered_full_df = full_df[
    (full_df['order_purchase_timestamp'].dt.date >= start_date) &
    (full_df['order_purchase_timestamp'].dt.date <= end_date)
]

# Filter segmen (untuk RFM)
if selected_segment == 'All Segments':
    filtered_rfm = rfm.copy()
else:
    filtered_rfm = rfm[rfm['segment'] == selected_segment]


st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Pelanggan", filtered_rfm['customer_id'].nunique())
col2.metric("Total Revenue", f"{filtered_rfm['monetary'].sum():,.0f}")
col3.metric("Jumlah Segmen", filtered_rfm['segment'].nunique())

st.caption(f"Periode data: {start_date} sampai {end_date}")

# VISUALISASI: JUMLAH PELANGGAN PER SEGMEN
st.subheader("Segmentasi Pelanggan (RFM)")

fig1, ax1 = plt.subplots(figsize=(6.5,4))
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

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.pyplot(fig1)


# VISUALISASI : TOTAL REVENUE PER SEGMEN 
st.subheader("Revenue per Segmen")

segment_revenue = (
    filtered_rfm.groupby('segment')['monetary']
    .sum()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots(figsize=(6.5,4))
segment_revenue.plot(kind='bar', ax=ax2)

ax2.set_xlabel("Segmen")
ax2.set_ylabel("Total Revenue (Juta)")
ax2.set_title("Total Revenue Berdasarkan Segmen")
ax2.yaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f'{x/1_000_000:.1f}M')
)

plt.xticks(rotation=30)
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.pyplot(fig2)

# VISUALISASI: TOP 10 STATE BERDASARKAN Jumlah Pelanggan
customer_state = (
    filtered_full_df.groupby('customer_state')['customer_id']
    .nunique()
    .reset_index(name='total_customers')
)

st.subheader("Top 10 State Berdasarkan Jumlah Pelanggan")

top_customer_state = customer_state.sort_values(
    by='total_customers', ascending=False
).head(10)

fig3, ax3 = plt.subplots(figsize=(7,4))
sns.barplot(
    data=top_customer_state,
    x='customer_state',
    y='total_customers',
    ax=ax3
)

ax3.set_title("Top 10 State Berdasarkan Jumlah Pelanggan")
ax3.set_xlabel("State")
ax3.set_ylabel("Jumlah Pelanggan")
plt.xticks(rotation=30)

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.pyplot(fig3)


# VISUALISASI: TOP 10 STATE BERDASARKAN REVENUE
st.subheader("Top 10 State Berdasarkan Revenue")

state_revenue = (
    filtered_full_df.groupby('customer_state')['payment_value']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig4, ax4 = plt.subplots(figsize=(7,4))
state_revenue.plot(kind='bar', ax=ax4)

ax4.set_xlabel("State")
ax4.set_ylabel("Total Revenue (Juta)")
ax4.set_title("Top 10 State Berdasarkan Revenue")
ax4.yaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f'{x/1_000_000:.1f}M')
)

plt.xticks(rotation=30)
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.pyplot(fig4)


st.markdown("---")
st.caption("")
