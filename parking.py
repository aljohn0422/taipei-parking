import json

import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")

with open('./taipei_parking.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data['park'])
df["ChargingStation"] = df['ChargingStation'].fillna('0')
df = df.drop(columns=[
    'id',
    'type',
    'type2',
    'serviceTime',
    'tw97x',
    'tw97y',
    'totalmotor',
    'totalbike',
    'totalbus',
    'ChargeStation',
    'Handicap_First', 'totallargemotor', 
    'Taxi_OneHR_Free', 'AED_Equipment', 'CellSignal_Enhancement',
    'Accessibility_Elevator', 'Phone_Charge', 'Child_Pickup_Area',
    'FareInfo', 'EntranceCoord'
    ])
df = df.rename(columns={
        'area': '行政區',
        'name': '名稱',
        'address': '地址',
        'payex': '計費模式',
        'tel': '聯絡電話',
        'totalcar': '小型車車位',
        'Pregnancy_First': '婦幼車位',
        'ChargingStation': '電動車位',
    })
show = df

st.title('臺北市停車資訊搜尋')
col0, col1, col2 = st.columns(3)
with col0:
    if st.checkbox('包含月票'):
        show = show[show['計費模式'].str.contains('月')]
with col1:
    selected = st.multiselect('行政區', pd.unique(df['行政區']))
    if selected:
        show = show[show['行政區'].isin(selected)]
with col2:
    search = st.text_input('關鍵字搜尋(名稱與地址)')
    if search:
        show = show[show['名稱'].str.contains(search) | show['地址'].str.contains(search)]

st.text(f'共{len(show)}個符合條件')
st.dataframe(show)
st.text('資料來源: https://marktoast.com/taipeiparking/index.html')
