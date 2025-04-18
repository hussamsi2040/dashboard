import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats # Add scipy for statistical tests

# Page config
st.set_page_config(
    page_title="Oyun Analitik Paneli",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Ensure metric labels are visible */
    .stMetric label {
        color: #000 !important; /* Black color for label */
        display: block !important; /* Ensure it's displayed */
        opacity: 1 !important; /* Ensure it's not transparent */
    }
    /* Ensure metric values are visible */
    .stMetric div[data-testid="stMetricValue"] {
        color: #000 !important; /* Black color for value */
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/online_gaming_behavior_dataset.csv')
        date_columns = ['SignupDate', 'LastActiveDate']
        for col in date_columns:
            df[col] = pd.to_datetime(df[col])
        return df
    except Exception as e:
        st.error(f"Veri yükleme hatası: {e}")
        return None

df = load_data()

if df is None:
    st.error("Veri dosyası yüklenemedi. Lütfen veri dosyasını kontrol edin.")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("🎮 Oyun Analitik Paneli")
    st.info("Oyuncu davranışları ve oyun metrikleri analizi")
    
    # Date range filter
    st.subheader("📅 Tarih Aralığı")
    date_range = st.date_input(
        "Tarih Seçin",
        [df['SignupDate'].min().date(), df['SignupDate'].max().date()]
    )
    
    # --- Filters --- 
    st.subheader("⚙️ Filtreler")
    
    # Genre filter
    # st.subheader("🎲 Oyun Türü") # Combined under Filters
    genres = ["Tümü"] + sorted(df['GameGenre'].unique().tolist())
    selected_genre = st.selectbox("Oyun Türü Seçin", genres)
    
    # Difficulty filter
    difficulties = ["Tümü"] + sorted(df['GameDifficulty'].unique().tolist())
    selected_difficulty = st.selectbox("Oyun Zorluğu Seçin", difficulties)

    # Device filter
    devices = ["Tümü"] + sorted(df['Device'].unique().tolist())
    selected_device = st.selectbox("Cihaz Seçin", devices)

    # Location filter (Top 10 + Other for simplicity)
    top_locations = df['Location'].value_counts().nlargest(10).index.tolist()
    locations_list = ["Tümü"] + top_locations + ["Diğer"]
    selected_location = st.selectbox("Lokasyon Seçin", locations_list)
    
    # Apply filters
    df_filtered = df.copy()
    if selected_genre != "Tümü":
        df_filtered = df_filtered[df_filtered['GameGenre'] == selected_genre]
    if selected_difficulty != "Tümü":
        df_filtered = df_filtered[df_filtered['GameDifficulty'] == selected_difficulty]
    if selected_device != "Tümü":
        df_filtered = df_filtered[df_filtered['Device'] == selected_device]
    if selected_location != "Tümü":
        if selected_location == "Diğer":
            df_filtered = df_filtered[~df_filtered['Location'].isin(top_locations)]
        else:
            df_filtered = df_filtered[df_filtered['Location'] == selected_location]
    
    # Navigation
    st.subheader("📊 Navigasyon")
    pages = [
        "Genel Bakış",
        "Oyuncu Analizi",
        "Gelir Analizi",
        "Oturum Analizi",
        "Başarı Takibi",
        "Teknik Performans", 
        "Sosyal Analiz",      
        "Kohort Analizi",     
        "Oyuncu Segmentasyonu", # New page
        "A/B Test Analizi" # New A/B test page
    ]
    page = st.radio("Sayfa Seçin", pages)

    st.divider()
    
    # --- Data Export ---
    st.subheader("📥 Veri İndir")
    @st.cache_data
    def convert_df_to_csv(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(df_filtered)

    st.download_button(
        label="Filtrelenmiş Veriyi CSV İndir",
        data=csv,
        file_name='filtered_gaming_data.csv',
        mime='text/csv',
    )

# Main content
if page == "Genel Bakış":
    st.title("📊 Genel Bakış")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Toplam Oyuncu",
            f"{len(df_filtered):,}",
            f"Aktif: {df_filtered['IsActive'].sum():,}"
        )
    
    with col2:
        revenue = df_filtered['TotalSpentUSD'].sum()
        arpu = revenue / len(df_filtered)
        st.metric(
            "Toplam Gelir",
            f"${revenue:,.2f}",
            f"ARPU: ${arpu:.2f}"
        )
    
    with col3:
        avg_playtime = df_filtered['PlayTimeHours'].mean()
        st.metric(
            "Ort. Oynama Süresi",
            f"{avg_playtime:.1f} saat",
            f"Haftalık: {df_filtered['SessionsPerWeek'].mean():.1f} oturum"
        )
    
    with col4:
        retention = (df_filtered['IsActive'].sum() / len(df_filtered)) * 100
        st.metric(
            "Tutundurma Oranı",
            f"%{retention:.1f}",
            f"Aktif: {df_filtered['IsActive'].sum():,} oyuncu"
        )

    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎮 Oyun Türü Dağılımı")
        genre_dist = df_filtered['GameGenre'].value_counts()
        fig = px.pie(
            values=genre_dist.values,
            names=genre_dist.index,
            title="Oyun Türlerine Göre Oyuncu Dağılımı"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Katılım Seviyesi")
        engagement_dist = df_filtered['EngagementLevel'].value_counts()
        fig = px.bar(
            x=engagement_dist.index,
            y=engagement_dist.values,
            title="Katılım Seviyesi Dağılımı",
            labels={'x': 'Seviye', 'y': 'Oyuncu Sayısı'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Player retention curve
    st.subheader("📉 Oyuncu Tutundurma Eğrisi")
    
    # Add segmentation option
    retention_segment_options = {
        "Genel": None, 
        "Cihaz": "Device", 
        "Oyun Türü": "GameGenre",
        "Etkileşim Seviyesi": "EngagementLevel"
    }
    selected_segment_label = st.selectbox(
        "Tutundurma Eğrisini Şuna Göre Segmentle:", 
        options=list(retention_segment_options.keys()),
        index=0 # Default to 'Genel'
    )
    segment_column = retention_segment_options[selected_segment_label]

    # Calculate retention data, potentially grouped
    if segment_column:
        retention_data = df_filtered.groupby([segment_column, 'DaysSinceSignup'])['IsActive'].mean().reset_index()
        retention_data['IsActive'] *= 100 # Convert to percentage
        title = f"Günlük Tutundurma Oranı ({selected_segment_label} Göre)"
    else:
        retention_data = df_filtered.groupby('DaysSinceSignup')['IsActive'].mean().reset_index()
        retention_data['IsActive'] *= 100 # Convert to percentage
        title = "Günlük Tutundurma Oranı (Genel)"
        
    fig_retention = px.line(
        retention_data,
        x='DaysSinceSignup',
        y='IsActive',
        color=segment_column, # Use segment column for color if selected
        labels={'DaysSinceSignup': 'Kayıttan Sonra Geçen Gün', 'IsActive': 'Tutundurma Oranı (%)'},
        title=title
    )
    st.plotly_chart(fig_retention, use_container_width=True)

elif page == "Oyuncu Analizi":
    st.title("👥 Oyuncu Analizi")
    
    # Player demographics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Yaş Dağılımı")
        fig = px.histogram(
            df_filtered,
            x='Age',
            title="Oyuncu Yaş Dağılımı",
            labels={'Age': 'Yaş', 'count': 'Oyuncu Sayısı'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Cinsiyet Dağılımı")
        gender_dist = df_filtered['Gender'].value_counts()
        fig = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title="Cinsiyet Dağılımı"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Player engagement analysis
    st.subheader("🎯 Oyuncu Katılımı Analizi")
    fig = px.scatter(
        df_filtered,
        x='PlayTimeHours',
        y='PlayerLevel',
        color='EngagementLevel',
        size='AchievementsUnlocked',
        hover_data=['TotalSpentUSD'],
        title="Oynama Süresi vs Seviye",
        labels={
            'PlayTimeHours': 'Oynama Süresi (Saat)',
            'PlayerLevel': 'Oyuncu Seviyesi',
            'EngagementLevel': 'Katılım Seviyesi'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Gelir Analizi":
    st.title("💰 Gelir Analizi")
    
    # Revenue metrics
    col1, col2, col3 = st.columns(3)
    
    # Calculate paying users from the filtered data
    df_paying = df_filtered[df_filtered['HasPurchased'] == 1]
    paying_users = len(df_paying)
    total_users = len(df_filtered)
    
    if total_users > 0:
        conversion = (paying_users / total_users) * 100
    else:
        conversion = 0
        
    if paying_users > 0:
        arppu = df_paying['TotalSpentUSD'].mean()
    else:
        arppu = 0
        
    if total_users > 0:
        arpu = df_filtered['TotalSpentUSD'].sum() / total_users # This is also LTV in this simple model
        ltv = arpu # Assuming LTV is average revenue per user for now
        median_ltv = df_filtered['TotalSpentUSD'].median()
    else:
        arpu = 0
        ltv = 0
        median_ltv = 0

    total_revenue = df_filtered['TotalSpentUSD'].sum()
    
    with col1:
        st.metric(
            "Ödeme Yapan Oyuncular",
            f"{paying_users:,}",
            f"Dönüşüm: {conversion:.1f}%"
        )
    
    with col2:
        st.metric(
            "ARPPU",
            f"${arppu:.2f}",
            f"Toplam: ${total_revenue:,.2f}",
            help="Ortalama Ödeme Yapan Kullanıcı Başına Gelir (Average Revenue Per Paying User)"
        )
    
    with col3:
        st.metric(
            "Ortalama LTV",
            f"${ltv:.2f}",
            f"Medyan: ${median_ltv:.2f}",
            help="Ortalama Oyuncu Yaşam Boyu Değeri (Lifetime Value) - Mevcut verilerle oyuncu başına ortalama gelir olarak hesaplanmıştır."
        )

    st.divider()
    st.subheader("📊 Gelir Segmentasyonu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Device
        revenue_by_device = df_filtered.groupby('Device')['TotalSpentUSD'].mean().reset_index().sort_values('TotalSpentUSD', ascending=False)
        fig_dev = px.bar(
            revenue_by_device,
            x='Device',
            y='TotalSpentUSD',
            title="Cihaza Göre Ortalama Harcama",
            labels={'Device': 'Cihaz', 'TotalSpentUSD': 'Ortalama Harcama ($)'}
        )
        st.plotly_chart(fig_dev, use_container_width=True)

    with col2:
        # Revenue by Engagement Level
        revenue_by_engagement = df_filtered.groupby('EngagementLevel')['TotalSpentUSD'].mean().reset_index()
         # Ensure correct order for engagement levels if needed
        engagement_order = ['Düşük', 'Orta', 'Yüksek']
        revenue_by_engagement['EngagementLevel'] = pd.Categorical(revenue_by_engagement['EngagementLevel'], categories=engagement_order, ordered=True)
        revenue_by_engagement = revenue_by_engagement.sort_values('EngagementLevel')
       
        fig_eng = px.bar(
            revenue_by_engagement,
            x='EngagementLevel',
            y='TotalSpentUSD',
            title="Etkileşim Seviyesine Göre Ortalama Harcama",
            labels={'EngagementLevel': 'Etkileşim Seviyesi', 'TotalSpentUSD': 'Ortalama Harcama ($)'}
        )
        st.plotly_chart(fig_eng, use_container_width=True)

    st.divider()
    st.subheader("💵 Ödeme Yapan Oyuncu Harcama Dağılımı")
    # Revenue distribution for paying users
    if paying_users > 0:
        fig_dist_paying = px.histogram(
            df_paying,
            x='TotalSpentUSD',
            nbins=50,
            title="Ödeme Yapan Oyuncu Başına Harcama Dağılımı",
            labels={'TotalSpentUSD': 'Toplam Harcama ($)'}
        )
        st.plotly_chart(fig_dist_paying, use_container_width=True)
    else:
        st.info("Filtrelenen veride ödeme yapan oyuncu bulunmamaktadır.")

elif page == "Oturum Analizi":
    st.title("⏱️ Oturum Analizi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Haftalık Oturum Dağılımı")
        fig = px.histogram(
            df_filtered,
            x='SessionsPerWeek',
            title="Haftalık Oturum Sayısı",
            labels={'SessionsPerWeek': 'Oturum/Hafta'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⌛ Oturum Süresi Dağılımı")
        fig = px.histogram(
            df_filtered,
            x='AvgSessionDurationMinutes',
            title="Ortalama Oturum Süresi",
            labels={'AvgSessionDurationMinutes': 'Dakika'}
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("📈 Zaman İçinde ve Gruplara Göre Etkileşim")

    col1, col2 = st.columns(2)

    with col1:
        # Playtime over Days Since Signup
        st.subheader("⏳ Kayıttan Beri Geçen Süreye Göre Oynama")
        playtime_over_time = df_filtered.groupby('DaysSinceSignup')['PlayTimeHours'].mean().reset_index()
        fig_playtime_time = px.line(
            playtime_over_time,
            x='DaysSinceSignup',
            y='PlayTimeHours',
            title="Ortalama Oynama Süresi vs Kayıttan Beri Geçen Gün",
            labels={'DaysSinceSignup': 'Kayıttan Beri Geçen Gün', 'PlayTimeHours': 'Ortalama Oynama Süresi (Saat)'}
        )
        st.plotly_chart(fig_playtime_time, use_container_width=True)

    with col2:
        # Session Duration by Guild Membership
        st.subheader("🛡️ Lonca Üyeliğine Göre Oturum Süresi")
        fig_guild_session = px.box(
            df_filtered,
            x='GuildMember',
            y='AvgSessionDurationMinutes',
            points="outliers",
            title="Lonca Üyeliğine Göre Ortalama Oturum Süresi",
            labels={'GuildMember': 'Lonca Üyesi (1=Evet, 0=Hayır)', 'AvgSessionDurationMinutes': 'Ortalama Oturum Süresi (Dakika)'}
        )
        # Update x-axis labels for clarity
        fig_guild_session.update_xaxes(ticktext=['Üye Değil', 'Üye'], tickvals=[0, 1])
        st.plotly_chart(fig_guild_session, use_container_width=True)

# --- New Pages --- 
elif page == "Teknik Performans":
    st.title("🛠️ Teknik Performans")
    # st.warning("Bu sayfa henüz geliştirilme aşamasındadır.")
    
    # Key metrics
    col1, col2 = st.columns(2)
    with col1:
        avg_fps = df_filtered['AvgFPS'].mean()
        st.metric(
            "Ortalama FPS",
            f"{avg_fps:.1f}",
            f"Min: {df_filtered['AvgFPS'].min():.1f}, Maks: {df_filtered['AvgFPS'].max():.1f}"
        )
    with col2:
        total_crashes = df_filtered['CrashCount'].sum()
        avg_crashes = df_filtered['CrashCount'].mean()
        st.metric(
            "Toplam Çökme",
            f"{total_crashes:,}",
            f"Ortalama: {avg_crashes:.2f} / oyuncu"
        )
        
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 FPS Dağılımı")
        fig = px.histogram(
            df_filtered,
            x='AvgFPS',
            title="Ortalama FPS Dağılımı",
            labels={'AvgFPS': 'Ortalama FPS', 'count': 'Oyuncu Sayısı'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💥 Çökme Sayısı Dağılımı")
        crash_counts = df_filtered['CrashCount'].value_counts().sort_index()
        fig = px.bar(
            x=crash_counts.index,
            y=crash_counts.values,
            title="Oyuncu Başına Çökme Sayısı",
            labels={'x': 'Çökme Sayısı', 'y': 'Oyuncu Sayısı'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
    # Performance by Device
    st.subheader("📱 Cihaza Göre Performans")
    perf_by_device = df_filtered.groupby('Device')[[ 'AvgFPS', 'CrashCount']].mean().reset_index()
    
    fig_fps = px.bar(
        perf_by_device,
        x='Device',
        y='AvgFPS',
        title="Cihaza Göre Ortalama FPS",
        labels={'Device': 'Cihaz', 'AvgFPS': 'Ortalama FPS'}
    )
    st.plotly_chart(fig_fps, use_container_width=True)
    
    fig_crash = px.bar(
        perf_by_device,
        x='Device',
        y='CrashCount',
        title="Cihaza Göre Ortalama Çökme Sayısı",
        labels={'Device': 'Cihaz', 'CrashCount': 'Ortalama Çökme'}
    )
    st.plotly_chart(fig_crash, use_container_width=True)

    st.divider()
    # Crashes by Guild Membership (New)
    st.subheader("🛡️ Lonca Üyeliğine Göre Çökme Sayısı")
    crashes_by_guild = df_filtered.groupby('GuildMember')['CrashCount'].mean().reset_index()
    crashes_by_guild['GuildMember'] = crashes_by_guild['GuildMember'].map({0: 'Üye Değil', 1: 'Üye'})
    fig_crash_guild = px.bar(
        crashes_by_guild,
        x='GuildMember',
        y='CrashCount',
        title="Lonca Üyeliğine Göre Ortalama Çökme Sayısı",
        labels={'GuildMember': 'Lonca Durumu', 'CrashCount': 'Ortalama Çökme Sayısı'}
    )
    st.plotly_chart(fig_crash_guild, use_container_width=True)

elif page == "Sosyal Analiz":
    st.title("🤝 Sosyal Analiz")
    # st.warning("Bu sayfa henüz geliştirilme aşamasındadır.")
    
    # Key metrics
    col1, col2 = st.columns(2)
    with col1:
        avg_friends = df_filtered['FriendsCount'].mean()
        st.metric(
            "Ortalama Arkadaş Sayısı",
            f"{avg_friends:.1f}",
            f"Maks: {df_filtered['FriendsCount'].max()}"
        )
    with col2:
        guild_members = df_filtered['GuildMember'].sum()
        guild_percentage = (guild_members / len(df_filtered)) * 100
        st.metric(
            "Lonca Üyeleri",
            f"{guild_members:,}",
            f"%{guild_percentage:.1f} oyuncu"
        )
        
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🧑‍🤝‍🧑 Arkadaş Sayısı Dağılımı")
        fig = px.histogram(
            df_filtered,
            x='FriendsCount',
            nbins=20, # Adjust bin count as needed
            title="Oyuncu Başına Arkadaş Sayısı",
            labels={'FriendsCount': 'Arkadaş Sayısı', 'count': 'Oyuncu Sayısı'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🛡️ Lonca Üyelik Durumu")
        guild_dist = df_filtered['GuildMember'].map({1: 'Üye', 0: 'Üye Değil'}).value_counts()
        fig = px.pie(
            values=guild_dist.values,
            names=guild_dist.index,
            title="Lonca Üyeliği Dağılımı",
            color_discrete_map={'Üye':'#1f77b4', 'Üye Değil':'#ff7f0e'} # Optional: Custom colors
        )
        st.plotly_chart(fig, use_container_width=True)
        
    # Engagement by Social Factors
    st.subheader("📈 Sosyal Faktörlere Göre Etkileşim ve Harcama")
    
    col1, col2 = st.columns(2)

    with col1:
        # Box plot for PlayTimeHours by GuildMember (Existing)
        fig_guild_playtime = px.box(
            df_filtered,
            x='GuildMember',
            y='PlayTimeHours',
            points="outliers",
            title="Lonca Üyeliğine Göre Oynama Süresi",
            labels={'GuildMember': 'Lonca Üyesi (1=Evet, 0=Hayır)', 'PlayTimeHours': 'Oynama Süresi (Saat)'}
        )
        # Update x-axis labels for clarity
        fig_guild_playtime.update_xaxes(ticktext=['Üye Değil', 'Üye'], tickvals=[0, 1])
        st.plotly_chart(fig_guild_playtime, use_container_width=True)
    
    with col2:
        # Box plot for Spending by GuildMember (New)
        st.subheader("💰 Lonca Üyeliğine Göre Harcama")
        spending_by_guild = df_filtered[df_filtered['TotalSpentUSD'] > 0] # Only look at spenders for distribution
        fig_guild_spending = px.box(
            spending_by_guild,
            x='GuildMember',
            y='TotalSpentUSD',
            points="outliers",
            title="Lonca Üyeliğine Göre Harcama (Ödeme Yapanlar)",
            labels={'GuildMember': 'Lonca Üyesi (1=Evet, 0=Hayır)', 'TotalSpentUSD': 'Toplam Harcama ($)'}
        )
        fig_guild_spending.update_xaxes(ticktext=['Üye Değil', 'Üye'], tickvals=[0, 1])
        st.plotly_chart(fig_guild_spending, use_container_width=True)

    # Scatter plot for FriendsCount vs PlayTimeHours (Existing)
    fig_friends_playtime = px.scatter(
        df_filtered,
        x='FriendsCount',
        y='PlayTimeHours',
        trendline="ols", # Optional: Add a trendline
        title="Arkadaş Sayısı vs Oynama Süresi",
        labels={'FriendsCount': 'Arkadaş Sayısı', 'PlayTimeHours': 'Oynama Süresi (Saat)'}
    )
    st.plotly_chart(fig_friends_playtime, use_container_width=True)

# --- Cohort Analysis Page (New) ---
elif page == "Kohort Analizi":
    st.title("⏳ Kohort Analizi (Haftalık Tutundurma)")
    st.info("Bu analiz, oyuncuların kaydoldukları haftaya göre zaman içinde ne kadar süre aktif kaldıklarını gösterir.")

    # Ensure data is sorted by PlayerID and SignupDate for consistent cohort calculation if needed
    df_cohort = df_filtered.sort_values(['PlayerID', 'SignupDate']).copy()

    # --- Weekly Cohort Calculation ---
    try:
        # 1. Get Signup Week
        # Ensure SignupDate is datetime if not already
        df_cohort['SignupDate'] = pd.to_datetime(df_cohort['SignupDate'])
        df_cohort['SignupWeek'] = df_cohort['SignupDate'].dt.to_period('W').astype(str)

        # 2. Calculate Activity Week relative to Signup Week using LastActiveDate
        df_cohort['LastActiveDate'] = pd.to_datetime(df_cohort['LastActiveDate'])
        df_cohort['CohortAgeWeeks'] = (df_cohort['LastActiveDate'].dt.to_period('W') - df_cohort['SignupDate'].dt.to_period('W')).apply(lambda x: x.n if pd.notna(x) else -1)

        # Filter out invalid ages (e.g., if LastActiveDate is NaT or precedes SignupDate)
        df_cohort = df_cohort[df_cohort['CohortAgeWeeks'] >= 0]

        # 3. Group by SignupWeek and CohortAgeWeeks
        cohort_data = df_cohort.groupby(['SignupWeek', 'CohortAgeWeeks'])['PlayerID'].nunique().reset_index()
        
        if cohort_data.empty:
             st.warning("Filtrelenen verilerle kohort analizi oluşturulamadı (veri yok veya geçersiz tarih)." )
        else:
            # 4. Pivot for Heatmap
            cohort_pivot = cohort_data.pivot_table(index='SignupWeek', columns='CohortAgeWeeks', values='PlayerID')

            # 5. Calculate Cohort Size (Total unique players per SignupWeek)
            cohort_size = df_cohort.groupby('SignupWeek')['PlayerID'].nunique()

            # 6. Calculate Retention Rate (%)
            # Ensure alignment and handle potential missing weeks
            cohort_retention = cohort_pivot.divide(cohort_size, axis=0).fillna(0) * 100

            # --- Display Heatmap ---
            st.subheader("🗓️ Haftalık Tutundurma Oranları (%)")
            
            # Limit the number of weeks shown for readability
            max_weeks_to_show = 20 
            cohort_cols = cohort_retention.columns
            if len(cohort_cols) > max_weeks_to_show:
                 display_cols = cohort_cols[:max_weeks_to_show]
            else:
                 display_cols = cohort_cols
            cohort_retention_display = cohort_retention[display_cols]
            
            fig_cohort = go.Figure(data=go.Heatmap(
                z=cohort_retention_display.values,
                x=cohort_retention_display.columns,
                y=cohort_retention_display.index,
                colorscale='Viridis', 
                colorbar=dict(title='% Aktif Oyuncu'),
                hoverongaps=False,
                text=cohort_retention_display.round(1).astype(str) + '%', # Show percentage on hover
                texttemplate="%{text}",
                hoverinfo='x+y+z'
            ))
            
            fig_cohort.update_layout(
                title='Haftalık Kohortlara Göre Oyuncu Tutundurma',
                xaxis_title='Kayıttan Sonraki Hafta Numarası',
                yaxis_title='Kayıt Haftası',
                yaxis={'type': 'category', 'categoryorder':'category descending'} # Correct value
            )
            st.plotly_chart(fig_cohort, use_container_width=True)
            
            st.subheader("👥 Kohort Büyüklükleri")
            st.dataframe(cohort_size.reset_index().rename(columns={'PlayerID':'Oyuncu Sayısı'}).sort_values('SignupWeek', ascending=False))

    except Exception as e:
        st.error(f"Kohort analizi sırasında bir hata oluştu: {e}")
        st.warning("Lütfen veri dosyasındaki tarih formatlarını kontrol edin.")

# --- Player Segmentation Page (New) ---
elif page == "Oyuncu Segmentasyonu":
    st.title("🧩 Oyuncu Segmentasyonu (K-Means)")
    st.info("Bu sayfa, oyuncuları davranışsal metriklerine göre (oynama süresi, harcama, oturumlar, başarılar) gruplara ayırır.")

    # Select features for clustering
    features = [
        'PlayTimeHours', 
        'TotalSpentUSD', 
        'SessionsPerWeek', 
        'AchievementsUnlocked',
        'AvgSessionDurationMinutes',
        'FriendsCount'
    ]
    df_cluster = df_filtered[features].copy()

    # Handle potential missing values (fill with 0 or median/mean)
    df_cluster.fillna(0, inplace=True) 

    if len(df_cluster) < 4: # K-Means needs at least n_clusters samples
        st.warning("Segmentasyon için yeterli oyuncu verisi yok (en az 4 oyuncu gerekli). Lütfen filtreleri genişletin.")
    else:
        # Scale features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(df_cluster)

        # Apply K-Means
        n_clusters = 4 # Let's start with 4 clusters
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(scaled_features)

        # Add cluster labels to the filtered dataframe
        df_filtered_clustered = df_filtered.copy()
        df_filtered_clustered['Cluster'] = cluster_labels

        # --- Define descriptive names based on cluster analysis ---
        # Analyze the cluster_summary table printed below to refine these names!
        # Example plausible mapping (adjust based on actual cluster_summary):
        cluster_summary_for_naming = df_filtered_clustered.groupby('Cluster')[features].mean()
        # Find cluster with highest spending -> 'Yüksek Değerli'
        # Find cluster with lowest engagement -> 'Düşük Etkileşimli'
        # Distinguish others based on playtime/spending balance.
        # This requires inspecting the actual cluster_summary_for_naming output.
        # For now, using placeholder logic for demonstration:
        try:
            high_spender_id = cluster_summary_for_naming['TotalSpentUSD'].idxmax()
            low_engagement_id = cluster_summary_for_naming['PlayTimeHours'].idxmin() # Example proxy for low engagement
            
            temp_names = {}
            temp_names[high_spender_id] = "Yüksek Değerli"
            temp_names[low_engagement_id] = "Düşük Etkileşimli"
            
            remaining_ids = [i for i in range(n_clusters) if i not in temp_names]
            if len(remaining_ids) > 0:
                 # Example: Assign based on playtime for the remaining
                 playtime_order = cluster_summary_for_naming.loc[remaining_ids, 'PlayTimeHours'].sort_values()
                 temp_names[playtime_order.index[0]] = "Sıradan Oyuncu" # Lower playtime among remaining
                 if len(remaining_ids) > 1:
                     temp_names[playtime_order.index[1]] = "Aktif Harcamayan" # Higher playtime among remaining

            # Ensure all clusters have names, default if logic failed
            cluster_names = {i: temp_names.get(i, f"Segment {i+1}") for i in range(n_clusters)}
        except Exception as e:
            st.warning(f"Segment isimleri otomatik atanırken hata oluştu ({e}). Varsayılan isimler kullanılıyor.")
            cluster_names = {i: f"Segment {i+1}" for i in range(n_clusters)} # Fallback
            
        df_filtered_clustered['Segment'] = df_filtered_clustered['Cluster'].map(cluster_names)
        
        st.subheader("📊 Segmentlerin Görselleştirilmesi")

        # Visualize clusters (Example: PlayTime vs Spending)
        fig_cluster_scatter = px.scatter(
            df_filtered_clustered,
            x='PlayTimeHours',
            y='TotalSpentUSD',
            color='Segment',
            size='SessionsPerWeek', # Optional: Size by another metric
            hover_data=['PlayerID', 'AchievementsUnlocked'],
            title="Oyuncu Segmentleri (Oynama Süresi vs Harcama)",
            labels={
                'PlayTimeHours': 'Oynama Süresi (Saat)',
                'TotalSpentUSD': 'Toplam Harcama ($)',
                'Segment': 'Segment'
            }
        )
        st.plotly_chart(fig_cluster_scatter, use_container_width=True)

        st.subheader("📈 Segment Özellikleri")
        # Show summary statistics per cluster
        cluster_summary = df_filtered_clustered.groupby('Segment')[features].mean().reset_index()
        st.dataframe(cluster_summary)
        
        st.subheader("👥 Segment Dağılımı")
        segment_dist = df_filtered_clustered['Segment'].value_counts().reset_index()
        segment_dist.columns = ['Segment', 'Oyuncu Sayısı']
        fig_segment_pie = px.pie(
            segment_dist, 
            values='Oyuncu Sayısı', 
            names='Segment', 
            title='Oyuncu Sayısı Dağılımı'
        )
        st.plotly_chart(fig_segment_pie, use_container_width=True)

# --- A/B Test Analysis Page (New) ---
elif page == "A/B Test Analizi":
    st.title("🧪 A/B Test Analizi")
    st.info("Bu sayfa, A ve B grupları arasındaki metrik farklılıklarını istatistiksel olarak analiz eder.")

    # Ensure AB_Group column exists
    if 'AB_Group' not in df_filtered.columns:
        st.error("Veri setinde 'AB_Group' sütunu bulunamadı. Lütfen 'generate_data.py' betiğini tekrar çalıştırıp veriyi güncelleyin.")
        st.stop()

    # --- Inputs ----
    st.subheader("📊 Analiz Edilecek Metrik")
    # Available metrics for comparison
    metric_options = {
        "Dönüşüm Oranı (HasPurchased)": "conversion",
        "Ortalama Harcama (TotalSpentUSD)": "mean_spending",
        "Ortalama Oynama Süresi (PlayTimeHours)": "mean_playtime",
        # Add more metrics here if needed
    }
    selected_metric_label = st.selectbox("Metrik Seçin:", options=list(metric_options.keys()))
    selected_metric = metric_options[selected_metric_label]

    st.divider()

    # --- Data Preparation ---
    group_a = df_filtered[df_filtered['AB_Group'] == 'A']
    group_b = df_filtered[df_filtered['AB_Group'] == 'B']

    if len(group_a) == 0 or len(group_b) == 0:
        st.warning("Filtrelenmiş veride A veya B grubunda yeterli kullanıcı bulunmuyor.")
        st.stop()

    # --- Perform Test and Display Results ---
    st.subheader("📈 Test Sonuçları")
    
    alpha = 0.05 # Significance level

    # Function to calculate Cohen's d
    def cohen_d(x, y):
        nx = len(x)
        ny = len(y)
        dof = nx + ny - 2
        pooled_std = np.sqrt(((nx - 1) * np.std(x, ddof=1) ** 2 + (ny - 1) * np.std(y, ddof=1) ** 2) / dof)
        # Handle potential zero standard deviation
        if pooled_std == 0: return 0 
        return (np.mean(x) - np.mean(y)) / pooled_std
        
    # Function to calculate Confidence Interval for mean difference
    def mean_diff_ci(x, y, alpha=0.05):
        se_x = stats.sem(x, nan_policy='omit') 
        se_y = stats.sem(y, nan_policy='omit')
        se_diff = np.sqrt(se_x**2 + se_y**2)
        # Estimate degrees of freedom using Welch–Satterthwaite equation (approximation)
        # Note: Scipy doesn't directly expose this for ttest_ind with equal_var=False, 
        # so we use a simpler large-sample approximation with z-score or basic t-score.
        # For a more precise calculation, libraries like statsmodels might be needed.
        # Using a standard normal z-score for simplicity here (assumes large enough samples)
        z_crit = stats.norm.ppf(1 - alpha/2)
        diff = np.nanmean(y) - np.nanmean(x)
        lower = diff - z_crit * se_diff
        upper = diff + z_crit * se_diff
        return lower, upper

    try:
        if selected_metric == "conversion":
            # Compare conversion rates (HasPurchased)
            conv_a = group_a['HasPurchased'].sum()
            total_a = len(group_a)
            rate_a = (conv_a / total_a) * 100 if total_a > 0 else 0
            
            conv_b = group_b['HasPurchased'].sum()
            total_b = len(group_b)
            rate_b = (conv_b / total_b) * 100 if total_b > 0 else 0

            st.metric(label="Grup A Dönüşüm Oranı", value=f"{rate_a:.2f}%", delta=f"{conv_a:,} / {total_a:,}")
            st.metric(label="Grup B Dönüşüm Oranı", value=f"{rate_b:.2f}%", delta=f"{conv_b:,} / {total_b:,}")
            
            # Chi-squared test
            contingency_table = [
                [conv_a, total_a - conv_a],
                [conv_b, total_b - conv_b]
            ]
            chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)
            difference = rate_b - rate_a
            result_text = f"Chi-kare Testi: p-değeri = {p_value:.4f}"
            
            # Effect size: Odds Ratio (approximate)
            odds_a = conv_a / (total_a - conv_a) if (total_a - conv_a) > 0 else float('inf')
            odds_b = conv_b / (total_b - conv_b) if (total_b - conv_b) > 0 else float('inf')
            effect_size = odds_b / odds_a if odds_a > 0 and odds_a != float('inf') and odds_b != float('inf') else float('nan')
            effect_label = f"Odds Oranı: {effect_size:.2f}" if not np.isnan(effect_size) else "Odds Oranı: Hesaplanamadı"
            # Confidence interval for difference in proportions (using Normal approximation)
            prop_a = conv_a / total_a
            prop_b = conv_b / total_b
            se_diff_prop = np.sqrt(prop_a * (1 - prop_a) / total_a + prop_b * (1 - prop_b) / total_b)
            z_crit = stats.norm.ppf(1 - alpha/2)
            ci_lower = (prop_b - prop_a) - z_crit * se_diff_prop
            ci_upper = (prop_b - prop_a) + z_crit * se_diff_prop
            ci_text = f"Fark Güven Aralığı (%): [{ci_lower*100:+.2f}%, {ci_upper*100:+.2f}%]"

        elif selected_metric == "mean_spending":
            # Compare mean TotalSpentUSD
            mean_a = group_a['TotalSpentUSD'].mean()
            mean_b = group_b['TotalSpentUSD'].mean()
            std_a = group_a['TotalSpentUSD'].std()
            std_b = group_b['TotalSpentUSD'].std()

            st.metric(label="Grup A Ort. Harcama", value=f"${mean_a:.2f}", delta=f"Std: {std_a:.2f}")
            st.metric(label="Grup B Ort. Harcama", value=f"${mean_b:.2f}", delta=f"Std: {std_b:.2f}")
            
            # T-test (assuming unequal variance - Welch's T-test)
            t_stat, p_value = stats.ttest_ind(group_a['TotalSpentUSD'], group_b['TotalSpentUSD'], equal_var=False, nan_policy='omit')
            difference = mean_b - mean_a
            result_text = f"T-Testi (Welch): p-değeri = {p_value:.4f}"
            
            # Effect Size: Cohen's d
            d = cohen_d(group_b['TotalSpentUSD'].dropna(), group_a['TotalSpentUSD'].dropna())
            effect_label = f"Cohen's d: {d:.2f}"
            # Confidence Interval for mean difference
            ci_lower, ci_upper = mean_diff_ci(group_a['TotalSpentUSD'], group_b['TotalSpentUSD'], alpha)
            ci_text = f"Fark Güven Aralığı ($): [${ci_lower:+.2f}, ${ci_upper:+.2f}]"

        elif selected_metric == "mean_playtime":
             # Compare mean PlayTimeHours
            mean_a = group_a['PlayTimeHours'].mean()
            mean_b = group_b['PlayTimeHours'].mean()
            std_a = group_a['PlayTimeHours'].std()
            std_b = group_b['PlayTimeHours'].std()

            st.metric(label="Grup A Ort. Oynama Süresi", value=f"{mean_a:.2f} saat", delta=f"Std: {std_a:.2f}")
            st.metric(label="Grup B Ort. Oynama Süresi", value=f"{mean_b:.2f} saat", delta=f"Std: {std_b:.2f}")
            
            # T-test (assuming unequal variance - Welch's T-test)
            t_stat, p_value = stats.ttest_ind(group_a['PlayTimeHours'], group_b['PlayTimeHours'], equal_var=False, nan_policy='omit')
            difference = mean_b - mean_a
            result_text = f"T-Testi (Welch): p-değeri = {p_value:.4f}"
            
            # Effect Size: Cohen's d
            d = cohen_d(group_b['PlayTimeHours'].dropna(), group_a['PlayTimeHours'].dropna())
            effect_label = f"Cohen's d: {d:.2f}"
            # Confidence Interval for mean difference
            ci_lower, ci_upper = mean_diff_ci(group_a['PlayTimeHours'], group_b['PlayTimeHours'], alpha)
            ci_text = f"Fark Güven Aralığı (saat): [{ci_lower:+.2f}, {ci_upper:+.2f}]"

        else:
            st.error("Seçilen metrik için analiz henüz uygulanmadı.")
            st.stop()

        # --- Interpretation ---
        st.subheader("📝 Yorum")
        
        # Determine significance
        is_significant = p_value < alpha
        
        # --- Build Interpretation String ---
        interpretation = f"**Test Sonucu:** {result_text}. "
        interpretation += f"Gözlemlenen fark (Grup B - Grup A): **{difference:+.2f}**"
        if selected_metric == "conversion": interpretation += "%"
        elif selected_metric == "mean_spending": interpretation += "$"
        elif selected_metric == "mean_playtime": interpretation += " saat"
        interpretation += ".\n\n"
        
        # Explain p-value
        if is_significant:
            interpretation += f"p-değeri ({p_value:.4f}), {alpha} anlamlılık seviyesinden küçük olduğu için, bu farkın **istatistiksel olarak anlamlı** olduğunu söyleyebiliriz. Bu, gözlemlenen farkın tamamen şans eseri ortaya çıkma olasılığının düşük olduğu anlamına gelir.\n\n"
        else:
            interpretation += f"p-değeri ({p_value:.4f}), {alpha} anlamlılık seviyesinden büyük olduğu için, bu farkın **istatistiksel olarak anlamlı olmadığını** söyleyebiliriz. Gözlemlenen fark şans eseri ortaya çıkmış olabilir.\n\n"
            
        # Explain Confidence Interval
        interpretation += f"**Güven Aralığı (%{ (1-alpha)*100:.0f}):** {ci_text}. Bu aralık, deney tekrarlansa elde edilecek farkın %{ (1-alpha)*100:.0f} olasılıkla düşeceği aralığı tahmin eder.\n\n"
        
        # Explain Effect Size
        interpretation += f"**Etki Büyüklüğü:** {effect_label}. "
        try:
            if selected_metric == "conversion" and not np.isnan(effect_size):
                 if effect_size > 1:
                     interpretation += f"Bu, Grup B'deki bir kullanıcının dönüşüm gerçekleştirme olasılığının, Grup A'dakine göre yaklaşık **{effect_size:.1f} kat daha fazla** olduğunu gösterir. "
                 elif effect_size < 1 and effect_size > 0:
                     interpretation += f"Bu, Grup B'deki bir kullanıcının dönüşüm gerçekleştirme olasılığının, Grup A'dakine göre yaklaşık **{1/effect_size:.1f} kat daha az** olduğunu gösterir. "
                 else:
                     interpretation += "Gruplar arasında dönüşüm olasılığı açısından anlamlı bir fark gözlenmemiştir. "
            elif selected_metric in ["mean_spending", "mean_playtime"]:
                abs_d = abs(d)
                if abs_d < 0.2:
                    interpretation += "Bu, etki büyüklüğünün **çok küçük** olduğunu gösterir. "
                elif abs_d < 0.5:
                    interpretation += "Bu, etki büyüklüğünün **küçük** olduğunu gösterir. "
                elif abs_d < 0.8:
                    interpretation += "Bu, etki büyüklüğünün **orta** düzeyde olduğunu gösterir. "
                else:
                    interpretation += "Bu, etki büyüklüğünün **büyük** olduğunu gösterir. "
        except:
             interpretation += "(Etki büyüklüğü yorumlanamadı). " # Fallback
             
        # --- Display Interpretation ---
        if is_significant:
            st.success(interpretation)
        else:
            st.warning(interpretation)
            
    except Exception as e:
        st.error(f"A/B testi analizi sırasında bir hata oluştu: {e}")

else:  # Achievement Tracking (ensure this is the last `elif` before the footer)
    st.title("🏆 Başarı Takibi")
    
    # Achievement metrics
    col1, col2 = st.columns(2)
    
    # Add safety checks for division by zero if df_filtered can be empty
    total_users_ach = len(df_filtered)
    ach_unlocked_sum = df_filtered['AchievementsUnlocked'].sum()
    max_possible_achievements = 50 # Assuming this is the max possible per player

    if total_users_ach > 0:
        avg_ach = df_filtered['AchievementsUnlocked'].mean()
        max_ach = df_filtered['AchievementsUnlocked'].max()
        completion_rate = (ach_unlocked_sum / (total_users_ach * max_possible_achievements)) * 100
    else:
        avg_ach = 0
        max_ach = 0
        completion_rate = 0
        ach_unlocked_sum = 0

    with col1:
        st.metric(
            "Ortalama Başarı",
            f"{avg_ach:.1f}",
            f"Maks: {max_ach}"
        )
    
    with col2:
        st.metric(
            "Tamamlama Oranı (%)", # Clarified unit
            f"{completion_rate:.1f}%", 
            f"Toplam Açılan: {ach_unlocked_sum:,}",
            help=f"Açılan toplam başarıların, oyuncu başına {max_possible_achievements} başarı varsayımıyla mümkün olan maksimum başarı sayısına oranı."
        )

    # Achievement distribution
    st.subheader("🎯 Başarı Dağılımı")
    if total_users_ach > 0:
        fig_ach_hist = px.histogram(
            df_filtered,
            x='AchievementsUnlocked',
            title="Açılan Başarı Sayısı Dağılımı",
            labels={'AchievementsUnlocked': 'Başarı Sayısı'}
        )
        st.plotly_chart(fig_ach_hist, use_container_width=True)
    else:
        st.info("Başarı dağılımı için veri yok.")

# Footer
st.markdown("""
---
<div style='text-align: center'>
    <small>© 2025 | hussam sirelkhatim</small>
</div>
""", unsafe_allow_html=True)
