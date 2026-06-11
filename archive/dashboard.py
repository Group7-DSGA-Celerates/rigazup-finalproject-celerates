import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import plotly.express as px

st.title('Dashboard Penjualan')

if "df" not in st.session_state:

    st.warning(
        "Silakan upload dataset terlebih dahulu."
    )

    st.stop()

df = st.session_state.df

st.subheader('Preview Dataset')
df2 = df.copy()
df2['Tanggal'] = pd.to_datetime(df2['Tanggal'])
df2['Tanggal'] = df2['Tanggal'].dt.strftime('%Y-%m-%d')
st.dataframe(df2.head(10))

df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['Tahun'] = df['Tanggal'].dt.year
df['Bulan'] = df['Tanggal'].dt.month
df['Hari'] = df['Tanggal'].dt.day

total_penjualan = f'Rp {df['Total_Penjualan'].sum()/1_000_000:.2f} Jt'
total_transaksi = f'{len(df)} Transaksi'
total_unit_terjual = f'{df['Qty_Terjual'].sum():,} Unit'
jumlah_produk = f'{len(df['Produk'].unique())} Produk'

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        'Total Penjualan',
        value=total_penjualan
    )
with col2:
    st.metric(
        'Total Transaksi',
        value=total_transaksi
    )
with col3:
    st.metric(
        'Total Unit Terjual',
        value=total_unit_terjual
    )
with col4:
    st.metric(
        'Jumlah Produk',
        value=jumlah_produk
    )

st.divider()

group1 = df.groupby(['Tahun','Bulan'])['Total_Penjualan'].sum().reset_index()

st.subheader('Total Penjualan per Bulan')

fig = px.line(
    group1,
    x='Bulan',
    y='Total_Penjualan',
    color='Tahun',
    labels={
        'Total_Penjualan' : 'Total Penjualan'
    },
    markers=True
)
fig.update_traces(
    hovertemplate=
    '<b>Bulan %{x}</b><br>' +
    'Total Penjualan: Rp %{y:,.0f}' +
    '<extra></extra>'
)
fig.update_layout(
    hovermode='x unified'
)
st.plotly_chart(fig)

totalpenjualan = df.groupby('Tahun')['Total_Penjualan'].sum()
total2023 = f'Rp {totalpenjualan.iloc[0]/1_000_000:.2f} Jt'
total2024 = f'Rp {totalpenjualan.iloc[1]/1_000_000:.2f} Jt'
total2025 = f'Rp {totalpenjualan.iloc[2]/1_000_000:.2f} Jt'

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        'Total Penjualan Tahun 2023',
        value=total2023
    )

with col2:
    st.metric(
        'Total Penjualan Tahun 2024',
        value=total2024
    )

with col3:
    st.metric(
        'Total Penjualan Tahun 2025',
        value=total2025
    )

st.divider()

col_title, col_filter = st.columns([4,1])

with col_title:
    st.subheader('Top 10 Produk Terlaris')

with col_filter:
    tahun = st.selectbox(
        'Tahun',
        ['Semua', 2023, 2024, 2025],
        label_visibility="collapsed",
        key='tahun1'
    )

group2 = df.groupby(['Tahun','Produk'])['Total_Penjualan'].sum().sort_values().reset_index()

group2_filter = None

group2_nofilter = df.groupby(['Produk'])['Total_Penjualan'].sum().sort_values().reset_index()

if tahun == 'Semua':
    group2_filter = group2_nofilter
else:
    group2_filter = group2[group2['Tahun'] == tahun]

group2_filter = group2_filter.sort_values('Total_Penjualan', ascending=False)

fig2 = px.bar(
    group2_filter.head(10),
    x='Produk',
    y='Total_Penjualan',
    color='Produk',
    labels={
        'Total_Penjualan' : 'Total Penjualan'
    },
)
fig2.update_traces(
    hovertemplate=
    '<b>%{x}</b><br>' +
    'Total Penjualan: Rp %{y:,.0f}' +
    '<extra></extra>'
)
st.plotly_chart(fig2)

st.divider()

col_title, col_filter = st.columns([4,1])

with col_title:
    st.subheader('Kategori Terlaris')

with col_filter:
    tahun2 = st.selectbox(
        'Tahun',
        ['Semua', 2023, 2024, 2025],
        label_visibility="collapsed",
        key='tahun2'
    )

group3 = df.groupby(['Tahun', 'Kategori'])['Total_Penjualan'].sum().sort_values().reset_index()

group3_filter = None

group3_nofilter = df.groupby(['Kategori'])['Total_Penjualan'].sum().sort_values().reset_index()

if tahun2 == 'Semua':
    group3_filter = group3_nofilter
else:
    group3_filter = group3[group3['Tahun'] == tahun2]

fig3 = px.pie(
    group3_filter,
    names='Kategori',
    values='Total_Penjualan',
    labels={
        'Total_Penjualan' : 'Total Penjualan'
    },
    width=800,
    height=600,
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.G10
)
fig3.update_traces(
    textinfo='label+percent',
    marker=dict(
        line=dict(
            color='white',
            width=3
        )
    ),
    hovertemplate=
    '<b>%{label}</b><br>' +
    'Penjualan: Rp %{value:,.0f}<br>' +
    'Kontribusi: %{percent}'
)
st.plotly_chart(fig3)

st.divider()

col_title, col_filter = st.columns([4,1])

with col_title:
    st.subheader('Jumlah Barang Terjual per Kategori')

with col_filter:
    tahun3 = st.selectbox(
        'Tahun',
        ['Semua', 2023, 2024, 2025],
        label_visibility="collapsed",
        key='tahun3'
    )

group4 = df.groupby(['Tahun','Kategori'])['Qty_Terjual'].sum().sort_values().reset_index()

group4_filter = None

group4_nofilter = df.groupby('Kategori')['Qty_Terjual'].sum().sort_values().reset_index()

if tahun3 == 'Semua':
    group4_filter = group4_nofilter
else: 
    group4_filter = group4[group4['Tahun'] == tahun3]

group4_filter = group4_filter.sort_values('Qty_Terjual', ascending=False)

fig4 = px.bar(
    group4_filter,
    x='Kategori',
    y='Qty_Terjual',
    color='Kategori',
    labels={
        'Qty_Terjual' : 'Jumlah Terjual'
    }
) 
fig4.update_traces(
    hovertemplate=
    '<b>%{x}</b><br>' +
    'Jumlah Terjual: %{y:,.0f} Unit' +
    '<extra></extra>'
)
st.plotly_chart(fig4)

st.divider()

group5 = df.groupby(['Tahun','Bulan'])['Qty_Terjual'].sum().reset_index()

st.subheader('Total Unit Terjual per Bulan')

fig5 = px.line(
    group5,
    x='Bulan',
    y='Qty_Terjual',
    color='Tahun',
    labels={
        'Qty_Terjual' : 'Unit Terjual'
    },
    markers=True
)
fig5.update_traces(
    hovertemplate=
    '<b>Bulan %{x}</b><br>' +
    'Unit Terjual: %{y:,.0f}' +
    '<extra></extra>'
)
fig5.update_layout(
    hovermode='x unified'
)
st.plotly_chart(fig5)

totalqty = df.groupby('Tahun')['Qty_Terjual'].sum()
qty23 = f'{totalqty.iloc[0]:,} Unit'
qty24 = f'{totalqty.iloc[1]:,} Unit'
qty25 = f'{totalqty.iloc[2]:,} Unit'

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        'Total Unit Terjual Tahun 2023',
        value=qty23
    )

with col2:
    st.metric(
        'Total Unit Terjual Tahun 2024',
        value=qty24
    )

with col3:
    st.metric(
        'Total Unit Terjual Tahun 2025',
        value=qty25
    )
