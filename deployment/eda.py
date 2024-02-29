import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

def run():

    # title
    st.title('Dashboard Monitoring and Ecommerce Analysis')

    # deskripsi
    st.write('Created by: [Dwi Putra Satria Utama](https://www.linkedin.com/in/dwiputra3500/)')

    # garis pembatas
    st.markdown('---')

    # dataframe
    df_user=pd.read_csv('data/userclean.csv', sep=',')
    df_produk=pd.read_csv('data/produkclean.csv', sep=',')
    df_transaksi=pd.read_csv('data/transaksiclean.csv', sep=',')


    st.subheader(''' Bagaimana kondisi penjualan dari perusahaan?
                 ''')
    
    df_transaksi.set_index('DATE', inplace=True)
    # Menggunakan groupby untuk menjumlahkan 'Quantity' per hari
    df_daily_sum = df_transaksi.groupby(df_transaksi.index)['QUANTITY'].sum()

    
    # Membuat plotly figure
    fig = go.Figure()

    # Menambahkan trace garis untuk jumlah penjualan
    fig.add_trace(go.Scatter(x=df_daily_sum.index, 
                            y=df_daily_sum.values, 
                            mode='lines+markers', 
                            name='Jumlah Penjualan', 
                            line=dict(color='blue')))

    # Menambahkan layout dan label
    fig.update_layout(
        title='Tren Penjualan Harian',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Jumlah Penjualan'),
        showlegend=True,
        width=800,  
        height=800  
    )

    # Menampilkan plot
    st.plotly_chart(fig)

    st.write('''- Fluktuasi Penjualan: Terdapat fluktuasi yang signifikan dalam penjualan harian, ditunjukkan oleh puncak dan lembah yang tajam pada grafik. Ini menunjukkan bahwa penjualan sangat bervariasi dari hari ke hari.
- Trend Musiman: Puncak pembelian selalu ada di pertengahan bulan (tanggal 10 sampai tanggal 15), penurunan pembelian terendah ada di awal dan akhir bulan
             ''')


    st.subheader(''' Bagaimana distribusi pelanggan yang membeli produk perusahaan?
                 ''')
    # Menggabungkan df_transaksi dengan df_user berdasarkan 'User_ID'
    df = pd.merge(df_transaksi, df_user[['USER_ID', 'AGE', 'STATUS']], on='USER_ID', how='left')

    # Menentukan harga berdasarkan PRODUCT_ID
    df['HARGA_SATUAN'] = np.where(df['PRODUCT_ID'] == 'A', 5000,
                                np.where(df['PRODUCT_ID'] == 'B', 3500,
                                        np.where(df['PRODUCT_ID'] == 'C', 12000,
                                                    np.where(df['PRODUCT_ID'] == 'D', 15000,
                                                            np.where(df['PRODUCT_ID'] == 'E', 9500, 0)
                                                            )
                                                )
                                        )
                                )

    # Menghitung nilai transaksi (NILAI_TRANSAKSI)
    df['NILAI_TRANSAKSI'] = df['QUANTITY'] * df['HARGA_SATUAN']

    # Mengganti urutan kolom
    df = df[['USER_ID', 'AGE', 'STATUS', 'TRANSACTION_ID', 'PRODUCT_ID', 'HARGA_SATUAN', 'QUANTITY', 'NILAI_TRANSAKSI']]


    # Mengelompokkan data berdasarkan Product_ID dan menjumlahkan quantity
    pembelian_user = df.groupby(['USER_ID', 'STATUS'])[['QUANTITY', 'NILAI_TRANSAKSI']].sum().reset_index()
    pembelian_user = pembelian_user.sort_values('NILAI_TRANSAKSI', ascending=False)
    pembelian_user = pembelian_user.reset_index().drop(columns=['index'])
    # Mengubah 'USER_ID' menjadi tipe data object
    pembelian_user['USER_ID'] = pembelian_user['USER_ID'].astype('str')
    
    # Membuat bar chart
    fig = px.bar(pembelian_user, 
                x='USER_ID', 
                y='NILAI_TRANSAKSI',  
                color='STATUS', 
                hover_data=['QUANTITY'],
                title='Distribusi Pelanggan Berdasarkan Status, Quantity, dan Nilai Transaksi',
                color_discrete_map={'premium': 'blue', 'basic': 'orange'},
                category_orders={'USER_ID': pembelian_user.sort_values('NILAI_TRANSAKSI', ascending=False)['USER_ID'].tolist()}  # Menyertakan urutan yang diinginkan
                )

    # Menyesuaikan label sumbu x dan y
    fig.update_layout(
        xaxis_title='USER ID',
        yaxis_title='NILAI TRANSAKSI',
    )

    # Menampilkan plot
    st.plotly_chart(fig)

    st.write('''- Pelanggan dengan status `premium` memiliki jumlah pembelian dan nilai transaksi yang lebih tinggi dibandingkan dengan pelanggan `basic`.
- Pelanggan dengan status `premium` memiliki kontribusi yang signifikan terhadap total nilai transaksi perusahaan.
- Beberapa pelanggan dengan USER_ID tertentu, seperti USER_ID 1, 16, 8, dan 19, memiliki jumlah pembelian dan nilai transaksi yang tinggi. Ini menunjukkan bahwa sebagian pelanggan tersebut memberikan kontribusi besar terhadap pendapatan perusahaan.
- Status `premium` tidak hanya terkait dengan jumlah pembelian yang lebih tinggi tetapi juga dengan nilai transaksi yang lebih besar. Pelanggan dengan status `premium` cenderung melakukan pembelian dengan nilai yang lebih tinggi.
- Meskipun pelanggan dengan status `basic` memiliki jumlah pembelian dan nilai transaksi yang lebih rendah dibandingkan dengan pelanggan `premium`, mereka masih berkontribusi pada pendapatan perusahaan. Strategi pemasaran dan retensi pelanggan dapat difokuskan untuk meningkatkan kontribusi dari pelanggan `basic`.
- Meskipun mayoritas pelanggan memiliki status `premium`, tidak selalu berarti nilai transaksi yang dihasilkan oleh pelanggan `premium` lebih tinggi daripada pelanggan dengan status `basic`. Beberapa pelanggan dengan status `basic` juga menunjukkan nilai transaksi yang cukup signifikan, bahkan  melebihi beberapa pelanggan dengan status `premium`. Ini menunjukkan bahwa tidak selalu status pelanggan yang menentukan nilai transaksi yang dihasilkan.
-  Distribusi pelanggan dapat dilihat dari nilai-nilai kuantitas pembelian dan nilai transaksi. Pelanggan dengan nilai kuantitas dan nilai transaksi yang tinggi dapat dianggap sebagai pelanggan utama yang berkontribusi besar terhadap pendapatan perusahaan.
             ''')

    st.subheader('''Bagaimana kondisi ketersediaan produk di gudang? Apakah masih terpenuhi aman atau harus segera dilakukan pengisian ulang?
                 ''')
    # Plotly Bar Chart
    fig = px.bar(df_produk, 
                x=df_produk['PRODUCT_ID'], 
                y='HARUS_RESTOCK_BILA_JUMLAH_GUDANG_TERSISA', 
                color='PRODUCT_ID',
                labels={'HARUS_RESTOCK_BILA_JUMLAH_GUDANG_TERSISA': 'Batas Restock'},
                title='Kondisi Ketersediaan Produk di Gudang',
                color_discrete_map={ 'a': 'orange', 'b': 'orange', 'c': 'orange', 'd': 'orange', 'e': 'orange'})

    # Menambahkan bar tambahan
    fig.add_bar(x=df_produk['PRODUCT_ID'], 
                y=df_produk['JUMLAH_DIGUDANG'],
                name='Tersedia',
                marker_color='blue')

    fig.update_layout(xaxis_title='PRODUCT_ID', yaxis_title='Jumlah')
    st.plotly_chart(fig)
    
    st.write('''Berdasarkan data yang ada bahwa ketersediaan di gudang masih aman karena masih diatas batas peraturan restock. Sehingga tidak diperlukannya pengisian ulang. 
             ''')


    st.subheader('''Produk mana yang mendapatkan performa penjualan terbaik dan yang kurang baik?
                 ''')
    # Mengelompokkan data berdasarkan Product_ID dan menjumlahkan quantity
    produk_terjual = df_transaksi.groupby('PRODUCT_ID')['QUANTITY'].sum().reset_index()
    produk_terjual = produk_terjual.sort_values('QUANTITY', ascending=False)
    produk_terjual.reset_index().drop(columns=['index'])

    # Membuat pie chart
    fig = px.bar(produk_terjual, 
                x='PRODUCT_ID', 
                y='QUANTITY',
                color='PRODUCT_ID', 
                title='Distribusi Quantity Berdasarkan Product_ID')

    # Menyesuaikan label sumbu x dan y
    fig.update_layout(
        xaxis_title='PRODUCT ID',
        yaxis_title='QUANTITY',
    )

    st.plotly_chart(fig)
    st.write('''Berdasarkan data yang ada didapatkan produk D memiliki kuantitas penjualan terbaik/tertinggi dengan jumlah 166, diikuti oleh B sebanyak 154, E sebanyak 150, A sebanyak 143 (performa kurang baik), dan C sebanyak 126 (performa kurang baik).
             ''')
    
    st.subheader(''' Bagaimana cara meningkatkan penjualan dari perusahaan?
                 ''')
    st.write('''1. Mengingat adanya tren musiman, perusahaan dapat mengembangkan strategi pemasaran yang berfokus pada periode puncak waktu pertengahan bulan, seperti menawarkan promosi khusus di pertengahan bulan untuk merangsang lebih banyak pembelian pada periode ini. Di periode rendah, fokus pada retensi pelanggan dan membangun loyalitas.

2.  Dengan memahami bahwa pelanggan dengan status premium memberikan kontribusi besar, perusahaan dapat mengembangkan program loyalitas atau penawaran eksklusif untuk mempertahankan dan menarik pelanggan dengan status ini.

3. Mengembangkan strategi untuk meningkatkan penjualan produk C dan A (performa kurang baik), dengan melakukan bundling  agar terjadinya peningkatan penjualan produk C dan A melalui program bundling tersebut. 

4. D adalah winning produk sehingga perluasan produksi, distribusi, dan pemasaran dapat membantu memperluas pangsa pasar dan keuntungan melalui Produk D. Meskipun produk D sukses, tidak ada jaminan bahwa tren akan tetap berlangsung selamanya. Pertimbangkan untuk mengembangkan produk potensian (B dan E) untuk mengurangi risiko ketergantungan pada satu produk.

5. Khusus pada profile pelanggan status basic dengan USER ID 8, perlu diperhatikan lebih lanjut. Karena user ini sangat potensial, mengingat walaupun statusnya basic tetapi quantitas pembeliannya sangat tinggi jika dibandingkan dengan user yang lain pada status yang sama. User seperti ini perlu dipertahankan dengan cara tetap mempertahankan dan meningkatkan kualitas produk layanan yang sudah ada.

             ''')

if __name__ == '__main__':
    run()
