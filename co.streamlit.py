import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.collections as mcollections
import numpy as np
import matplotlib.cm as cm

# 데이터 로드 (실제 사용 시 CSV 파일 경로를 수정하세요)
data = pd.read_csv('co.csv')  # 'data'로 명명된 완성된 데이터프레임

# 분석에 사용할 국가 목록
selected_countries = [
    'China', 'United States', 'India', 'Russia', 'Japan', 'Germany',
    'Brazil', 'Canada', 'South Korea', 'Indonesia', 'Mexico', 'Saudi Arabia',
    'Australia', 'Iran', 'United Kingdom', 'France', 'Italy', 'Turkey',
    'South Africa', 'Spain'
]

def plot_top_countries_by_year(year):
    # 입력받은 연도에 가장 탄소 배출량이 높은 나라 5곳
    top_countries = data[data['Year'] == year].nlargest(5, 'CO2 Emissions')
    st.write(f"{year}년의 탄소 배출량이 가장 높은 나라 5곳:")
    st.dataframe(top_countries)
    
    # 각 막대의 색상을 다르게 설정
    colors = cm.viridis(np.linspace(0, 1, len(top_countries)))
    
    # 탄소 배출량 시각화
    fig, ax = plt.subplots(figsize=(15, 8))  # 가로로 길게 설정
    ax.bar(top_countries['Country'], top_countries['CO2 Emissions'], color=colors)
    ax.set_xlabel('Country', fontsize=14, color='red')
    ax.set_ylabel('CO2 Emissions', fontsize=14, color='blue')
    ax.tick_params(axis='x', labelsize=12)  # x축 틱 라벨 크기 설정
    ax.set_title(f'Top 5 CO2 Emissions by Country in {year}', fontsize=20)
    st.pyplot(fig)

def plot_emissions_over_time(country):
    # 입력 받은 나라의 1850년~2022년 까지의 탄소 배출량 변화 그래프
    country_data = data[data['Country'] == country]
    st.write(f"{country}의 탄소 배출량 변화 (1850-2022):")
    
    # 탄소 배출량 변화 시각화
    fig, ax = plt.subplots(figsize=(15, 8))  # 가로로 길게 설정
    
    # 그라데이션 색상 설정
    points = np.array([country_data['Year'], country_data['CO2 Emissions']]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(country_data['CO2 Emissions'].min(), country_data['CO2 Emissions'].max())
    lc = mcollections.LineCollection(segments, cmap='viridis', norm=norm)
    lc.set_array(country_data['CO2 Emissions'])
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    fig.colorbar(line, ax=ax)

    ax.set_xlabel('Year', fontsize=14, color='red')  # x축 글씨 크기 설정
    ax.set_ylabel('CO2 Emissions', fontsize=14, color='blue')  # y축 글씨 크기 설정
    ax.set_title(f'CO2 Emissions Over Time in {country}', fontsize=20)  # 제목 글씨 크기 설정
    ax.tick_params(axis='x', labelsize=12)  # x축 틱 라벨 크기 설정
    
    ax.set_xlim(country_data['Year'].min(), country_data['Year'].max())
    ax.set_ylim(country_data['CO2 Emissions'].min(), country_data['CO2 Emissions'].max())
    
    st.pyplot(fig)

# Streamlit 앱 설정
st.set_page_config(page_title="CO2 Emissions Analysis")

# 페이지 제목
st.title("CO2 Emissions Analysis")

# 설명 추가
st.markdown("""
<strong>이 프로그램은 1850-2022년 까지의 기간 동안 연도별 및 국가별 탄소 배출량을 분석하고 시각화합니다.</strong><br>
1) 연도를 입력하시면 해당 연도의 탄소배출량이 높은 다섯 국가의 Bar Plot으로 보여드립니다.<br>
2) 국가를 선택하시면 해당 국가의 1850~2022년의 탄소배출량 추이를 Line Plot으로 보여드립니다.<br> 즐감하세요 >_< 😎
""", unsafe_allow_html=True)

# 연도 입력
year_input = st.text_input('Year (1850-2022)')

# 나라 입력
country = st.selectbox('Select a Country', [''] + selected_countries)

# 분석 버튼
if st.button('Analysis'):
    year = None
    if year_input.isdigit():
        year = int(year_input)
    
    if year and country:
        st.write(f"Year: {year}, Country: {country}")
        plot_top_countries_by_year(year)
        plot_emissions_over_time(country)
    elif year:
        st.write(f"Year: {year}")
        plot_top_countries_by_year(year)
    elif country:
        st.write(f"Country: {country}")
        plot_emissions_over_time(country)
    else:
        st.write("Enter a Country or Year please ❤")

