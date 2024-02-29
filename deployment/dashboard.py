import streamlit as st
import pandas as pd
import plotly.express as px
import category_encoders as ce
import plotly.graph_objects as go

def run():

    # title
    st.title('Dashboard Monitoring and Ecommerce Analysis')

    # deskripsi
    st.write('Created by: [Dwi Putra Satria Utama](https://www.linkedin.com/in/dwiputra3500/)')

    # garis pembatas
    st.markdown('---')

    # dataframe
    df_produk = pd.read_csv('data/produkclean.csv', sep=',')
    df = pd.read_csv('data/df.csv', sep=',')

    df_copy = df.copy()

    # Membuat plotly figure
    fig0 = go.Figure()

    df.set_index('DATE', inplace=True)

    # Menggunakan groupby untuk menjumlahkan 'Quantity' per hari
    df_daily_sum = df.groupby(df.index)['QUANTITY'].sum()

    # Menambahkan trace garis untuk jumlah penjualan
    fig0.add_trace(go.Scatter(x=df_daily_sum.index, 
                            y=df_daily_sum.values, 
                            mode='lines+markers', 
                            name='Jumlah Penjualan', 
                            line=dict(color='blue')))

    # Menambahkan layout dan label
    fig0.update_layout(
        title='Tren Penjualan Harian',
        xaxis=dict(title='YEAR'),
        yaxis=dict(title='JUMLAH PENJUALAN'),
        showlegend=True
    )

    


    # Mengelompokkan data berdasarkan Product_ID dan menjumlahkan quantity
    pembelian_user = df.groupby(['USER_ID', 'STATUS'])[['QUANTITY', 'NILAI_TRANSAKSI']].sum().reset_index()
    pembelian_user = pembelian_user.sort_values('NILAI_TRANSAKSI', ascending=False)
    pembelian_user = pembelian_user.reset_index().drop(columns=['index'])

    # Menggunakan Category Encoder untuk mengubah 'USER_ID' menjadi kategori
    encoder = ce.OrdinalEncoder(cols=['USER_ID'])
    pembelian_user = encoder.fit_transform(pembelian_user)

    # Membuat bar chart - Chart 1
    fig1 = px.bar(pembelian_user, 
                 x='USER_ID', 
                 y='NILAI_TRANSAKSI',
                 title='Distribusi Pelanggan',  
                 color='STATUS', 
                 hover_data=['QUANTITY'],
                 color_discrete_map={'premium': 'blue', 'basic': 'orange'}
                )

    # Menyesuaikan label sumbu x dan y
    fig1.update_layout(
        xaxis_title='USER ID',
        yaxis_title='NILAI TRANSAKSI',
    )

    # Plotly Bar Chart - Chart 2
    fig2 = px.bar(df_produk, 
                  x=df_produk['PRODUCT_ID'], 
                  y='HARUS_RESTOCK_BILA_JUMLAH_GUDANG_TERSISA',
                  title='Kondisi Ketersediaan Produk di Gudang', 
                  color='PRODUCT_ID',
                  labels={'HARUS_RESTOCK_BILA_JUMLAH_GUDANG_TERSISA': 'Batas Restock'},
                  color_discrete_map={'a': 'orange', 'b': 'orange', 'c': 'orange', 'd': 'orange', 'e': 'orange'})

    # Menambahkan bar tambahan
    fig2.add_bar(x=df_produk['PRODUCT_ID'], 
                 y=df_produk['JUMLAH_DIGUDANG'],
                 name='Tersedia',
                 marker_color='blue')

    fig2.update_layout(xaxis_title='PRODUCT ID', 
                       yaxis_title='JUMLAH')

    # Mengelompokkan data berdasarkan Product_ID dan menjumlahkan quantity
    produk_terjual = df.groupby('PRODUCT_ID')['QUANTITY'].sum().reset_index()
    produk_terjual = produk_terjual.sort_values('QUANTITY', ascending=False)
    produk_terjual.reset_index().drop(columns=['index'])

    # Membuat pie chart - Chart 3
    fig3 = px.bar(produk_terjual, 
                  x='PRODUCT_ID', 
                  y='QUANTITY',
                  color='PRODUCT_ID', 
                  title='Distribusi Quantity Berdasarkan Product ID')

    # Menyesuaikan label sumbu x dan y
    fig3.update_layout(
        xaxis_title='PRODUCT ID',
        yaxis_title='QUANTITY',
    )

    
    
    # Group by month and sum the 'NILAI_TRANSAKSI'
    df_copy['DATE'] = pd.to_datetime(df_copy['DATE'])

    total_transaction_per_month = df_copy.groupby(df_copy['DATE'].dt.to_period("M"))['NILAI_TRANSAKSI'].sum().reset_index()
    total_transaction_per_month['DATE'] = total_transaction_per_month['DATE'].astype(str)

    

    # Visualize Total Nilai Transaksi Setiap Bulan - Chart 4
    fig4 = px.bar(total_transaction_per_month, 
                x='DATE', 
                y='NILAI_TRANSAKSI',
                title='Total Nilai Transaksi Setiap Bulan',
                color='DATE')

    
    fig4.update_layout(
        xaxis_title='MONTH',
        yaxis_title='Total Nilai Transaksi',
    )



    # Group by month and sum the 'QUANTITY' for each PRODUCT_ID
    total_produk_per_month = df.groupby(['DATE', 'PRODUCT_ID'])['QUANTITY'].sum().reset_index()
    # Convert 'DATE' to datetime and extract the month
    total_produk_per_month['MONTH'] = pd.to_datetime(total_produk_per_month['DATE']).dt.to_period('M')
    # Create pivot table
    pivot_table = total_produk_per_month.pivot_table(index='MONTH', columns='PRODUCT_ID', values='QUANTITY', aggfunc='sum', fill_value=0)

    # Add 'TOTAL_QUANTITY' column
    pivot_table['TOTAL QUANTITY'] = pivot_table.sum(axis=1)

    # Display pivot table
    pivot_table = pivot_table.reset_index()
    pivot_table['MONTH'] = pivot_table['MONTH'].astype(str)

    # Visualize Total Nilai Transaksi Setiap Bulan - Chart 4

    df_melted = pivot_table.melt(id_vars='MONTH', value_vars=['A', 'B', 'C', 'D', 'E', 'TOTAL QUANTITY'], var_name='PRODUCT_ID', value_name='QUANTITY')

    # Plot data menggunakan Plotly Express
    fig5 = px.bar(df_melted, 
                x='MONTH', 
                y='QUANTITY', 
                color='PRODUCT_ID',
                title='Total Quantity Setiap Bulan',
                labels={'MONTH': 'MONTH', 'QUANTITY': 'TOTAL QUANTITY', 'PRODUCT_ID': 'PRODUCT ID'})
    # fig5.update_layout(xaxis_tickangle=0)


    # Row 1
    st.plotly_chart(fig0, use_container_width=True)

    # Container for row 2
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    row2_col1.plotly_chart(fig1, use_container_width=True)
    row2_col2.plotly_chart(fig2, use_container_width=True)
    row2_col3.plotly_chart(fig3, use_container_width=True)

    # Row 3
    row3_col1, row3_col2, row3_col3 = st.columns(3)
    row3_col1.plotly_chart(fig4, use_container_width=True)
    row3_col3.plotly_chart(fig5, use_container_width=True)


if __name__ == '__main__':
    run()
