# Oyun Analitik Paneli (Game Analytics Dashboard)

## Açıklama (Description)

Bu proje, çevrimiçi oyun platformları için oyuncu davranışlarını, katılımını, gelirini ve teknik performansını analiz etmek amacıyla tasarlanmış interaktif bir web paneli (dashboard) içerir. Panel, Streamlit kullanılarak oluşturulmuştur ve çeşitli metrikleri ve görselleştirmeleri keşfetmek için filtreleme yetenekleri sunar. Hedef, oyun geliştiricilere ve analistlere oyuncu tabanlarını anlamaları ve veriye dayalı kararlar almaları için değerli içgörüler sağlamaktır.

(This project contains an interactive web dashboard designed to analyze player behavior, engagement, revenue, and technical performance for online gaming platforms. Built with Streamlit, the dashboard offers filtering capabilities to explore various metrics and visualizations. The goal is to provide game developers and analysts with valuable insights to understand their player base and make data-driven decisions.)

## Özellikler (Features)

*   **İnteraktif Panel:** Streamlit ile oluşturulmuş, kullanıcı dostu bir web arayüzü.
*   **Kapsamlı Metrikler:** Oyuncu demografisi, oynama süresi, oturum sıklığı, gelir (ARPU, ARPPU, LTV), başarımlar, sosyal etkileşim (arkadaşlar, loncalar) ve teknik performans (FPS, çökmeler) metriklerini içerir.
*   **Gelişmiş Analiz Sayfaları:**
    *   **Genel Bakış:** Temel metrikler, tür/etkileşim dağılımları ve segmentlenebilir tutundurma eğrisi.
    *   **Oyuncu Analizi:** Demografik dağılımlar (yaş, cinsiyet) ve katılım analizi (oynama süresi vs seviye).
    *   **Gelir Analizi:** Dönüşüm oranı, ARPPU, LTV, harcama segmentasyonu (cihaz, etkileşim) ve ödeme yapan kullanıcı harcama dağılımı.
    *   **Oturum Analizi:** Oturum sıklığı/süresi dağılımları, zaman içindeki etkileşim ve lonca üyeliğine göre oturum analizi.
    *   **Başarı Takibi:** Ortalama başarı sayısı, tamamlama oranı ve başarı dağılımı.
    *   **Teknik Performans:** Ortalama FPS, çökme sayısı, cihaza ve lonca üyeliğine göre performans.
    *   **Sosyal Analiz:** Arkadaş sayısı, lonca üyeliği dağılımları, sosyal faktörlere göre etkileşim ve harcama.
    *   **Kohort Analizi:** Oyuncuların kayıt haftasına göre haftalık tutundurma oranlarını gösteren ısı haritası (heatmap).
    *   **Oyuncu Segmentasyonu:** Davranışsal metrikler kullanılarak K-Means kümeleme ile oyuncu segmentleri oluşturma ve analiz etme.
*   **Filtreleme:** Tarih aralığı, oyun türü, oyun zorluğu, cihaz ve lokasyona göre verileri filtreleme imkanı.
*   **Veri İndirme:** Filtrelenmiş verileri CSV formatında indirme butonu.
*   **Türkçe Dil Desteği:** Panel arayüzü ve metrikler Türkçe olarak sunulmaktadır.

## Veri Seti (Dataset)

Panel, `data/online_gaming_behavior_dataset.csv` dosyasını kullanır. Bu CSV dosyası, `generate_data.py` betiği (script) çalıştırılarak oluşturulur. Betik, aşağıdaki gibi çeşitli metrikleri içeren sentetik (yapay) oyuncu verileri üretir:

*   `PlayerID`, `Age`, `Gender`, `Location`, `Device`
*   `SignupDate`, `LastActiveDate`, `DaysSinceSignup`, `IsActive` (Tutundurma)
*   `GameGenre`, `GameDifficulty`
*   `PlayTimeHours`, `SessionsPerWeek`, `AvgSessionDurationMinutes` (Etkileşim)
*   `HasPurchased`, `TotalSpentUSD` (Gelir)
*   `PlayerLevel`, `AchievementsUnlocked` (İlerleme)
*   `FriendsCount`, `GuildMember` (Sosyal)
*   `AvgFPS`, `CrashCount` (Teknik)
*   `EngagementLevel` (Hesaplanmış Katılım Seviyesi)

## Kurulum (Setup)

1.  **Depoyu Klonlayın (Clone the repository):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2.  **Python:** Proje için Python 3.9 veya üstü önerilir.
3.  **Sanal Ortam Oluşturun (Create a Virtual Environment):** Sistemin Python kurulumunu etkilememek için bir sanal ortam kullanılması şiddetle tavsiye edilir.
    ```bash
    python3 -m venv .venv
    ```
4.  **Sanal Ortamı Aktifleştirin (Activate the Virtual Environment):**
    *   Linux/macOS: `source .venv/bin/activate`
    *   Windows: `.venv\Scripts\activate`
5.  **Gerekli Paketleri Yükleyin (Install Dependencies):**
    ```bash
    pip install pandas numpy streamlit plotly scikit-learn
    ```
    *(Alternatif olarak, eğer bir `requirements.txt` dosyası oluşturulursa: `pip install -r requirements.txt`)*

## Paneli Çalıştırma (Running the Dashboard)

1.  **Sanal Ortamın Aktif Olduğundan Emin Olun.** (Ensure the virtual environment is activated.)
2.  **(İsteğe Bağlı) Veri Setini Oluşturun/Güncelleyin (Optional - Generate/Update Dataset):** Eğer `data/online_gaming_behavior_dataset.csv` dosyası yoksa veya güncel değilse, aşağıdaki komutla oluşturun:
    ```bash
    python3 generate_data.py
    ```
    Bu komut, `data` klasörünün mevcut olmasını gerektirir (`mkdir data` ile oluşturabilirsiniz).
3.  **Streamlit Uygulamasını Başlatın (Start the Streamlit App):**
    ```bash
    streamlit run app.py
    ```
4.  Terminalde gösterilen URL'yi (genellikle `http://localhost:8501`) web tarayıcınızda açın.

## Dosya Yapısı (File Structure)

```
.
├── .venv/                  # Sanal ortam klasörü (Virtual environment directory)
├── data/
│   └── online_gaming_behavior_dataset.csv  # Oluşturulan veri seti (Generated dataset)
├── app.py                  # Streamlit panel uygulaması kodu (Dashboard application code)
├── generate_data.py        # Sentetik veri oluşturma betiği (Data generation script)
└── README.md               # Bu dosya (This file)
```

## Gelecekteki Olası Geliştirmeler (Potential Future Enhancements)

*   K-Means segmentlerine daha anlamlı isimler verme (ör. "Yüksek Değerli Oyuncular").
*   Daha fazla segmentasyon ve filtreleme seçeneği ekleme.
*   Grafiklere daha fazla etkileşim ekleme (ör. tıklayınca filtreleme).
*   Daha gelişmiş makine öğrenimi modelleri entegre etme (ör. churn tahmini).
*   Veritabanı entegrasyonu. 