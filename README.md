# Oyun Analitik Paneli (Game Analytics Dashboard)

## Açıklama (Description)

Bu proje, çevrimiçi oyun platformları için oyuncu davranışlarını, katılımını, gelirini ve teknik performansını analiz etmek amacıyla tasarlanmış interaktif bir web paneli (dashboard) içerir. Panel, Streamlit kullanılarak oluşturulmuştur ve çeşitli metrikleri ve görselleştirmeleri keşfetmek için filtreleme yetenekleri sunar. Hedef, oyun geliştiricilere ve analistlere oyuncu tabanlarını anlamaları ve veriye dayalı kararlar almaları için değerli içgörüler sağlamaktır.

(This project contains an interactive web dashboard designed to analyze player behavior, engagement, revenue, and technical performance for online gaming platforms. Built with Streamlit, the dashboard offers filtering capabilities to explore various metrics and visualizations. The goal is to provide game developers and analysts with valuable insights to understand their player base and make data-driven decisions.)

## Özellikler (Features)

*   **İnteraktif Panel:** Streamlit ile oluşturulmuş, kullanıcı dostu bir web arayüzü.
*   **Kapsamlı Metrikler:** Oyuncu demografisi, oynama süresi, oturum sıklığı, gelir (ARPU, ARPPU, LTV), başarımlar, sosyal etkileşim (arkadaşlar, loncalar) ve teknik performans (FPS, çökmeler) gibi temel metrikleri içerir.
*   **Gelişmiş Analiz Sayfaları:**
    *   **Genel Bakış:**
        *   Temel performans göstergeleri (KPI): Toplam oyuncu, aktif oyuncu sayısı, toplam gelir, ARPU (Oyuncu Başına Ortalama Gelir), ortalama oynama süresi, haftalık oturum sayısı ve genel tutundurma oranı.
        *   Oyuncu dağılımları: Oyun türü ve katılım seviyesine (Engagement Level) göre oyuncu sayılarının görselleştirilmesi (pasta ve çubuk grafikler).
        *   Segmentlenebilir tutundurma eğrisi: Oyuncuların kayıttan sonraki günlere göre aktif kalma oranlarını gösteren çizgi grafik. Bu eğri, cihaz, oyun türü veya etkileşim seviyesi gibi faktörlere göre filtrelenebilir.
    *   **Oyuncu Analizi:**
        *   Demografik dağılımlar: Oyuncuların yaş ve cinsiyet dağılımlarını gösteren histogram ve pasta grafikleri.
        *   Detaylı katılım analizi: Oyuncuların oynama süresi ile oyuncu seviyesi arasındaki ilişkiyi gösteren dağılım grafiği (scatter plot). Noktaların rengi katılım seviyesini, boyutu ise açılan başarı sayısını temsil eder.
    *   **Gelir Analizi:**
        *   Monetizasyon metrikleri: Ödeme yapan oyuncu sayısı, dönüşüm oranı (%), ARPPU (Ödeme Yapan Oyuncu Başına Ortalama Gelir) ve LTV (Yaşam Boyu Değer - mevcut veriyle ARPU olarak hesaplanır).
        *   Harcama segmentasyonu: Ortalama harcamanın cihaz türü ve etkileşim seviyesine göre nasıl değiştiğini gösteren çubuk grafikler.
        *   Ödeme yapan kullanıcı harcama dağılımı: Ödeme yapmış olan oyuncuların toplam harcama miktarlarının dağılımını gösteren histogram.
    *   **Oturum Analizi:**
        *   Oturum metrikleri: Haftalık oturum sayısı ve ortalama oturum süresi (dakika) dağılımlarını gösteren histogramlar.
        *   Zaman içinde etkileşim: Kayıttan beri geçen gün sayısına göre ortalama oynama süresinin nasıl değiştiğini gösteren çizgi grafik.
        *   Gruplara göre etkileşim: Lonca üyesi olan ve olmayan oyuncuların ortalama oturum sürelerini karşılaştıran kutu grafiği (box plot).
    *   **Başarı Takibi:**
        *   Başarı metrikleri: Ortalama açılan başarı sayısı, maksimum açılan başarı sayısı ve genel başarı tamamlama oranı (%).
        *   Başarı dağılımı: Oyuncuların ne kadar başarı açtığını gösteren histogram.
    *   **Teknik Performans:**
        *   Performans metrikleri: Ortalama FPS (Kare Hızı) ve toplam/ortalama çökme sayısı.
        *   Dağılımlar: Ortalama FPS ve oyuncu başına düşen çökme sayısının dağılımlarını gösteren histogram ve çubuk grafikler.
        *   Cihaz ve Lonca Bazında Performans: Ortalama FPS ve çökme sayısının farklı cihaz türlerine ve lonca üyeliği durumuna göre karşılaştırılması (çubuk grafikler).
    *   **Sosyal Analiz:**
        *   Sosyal metrikler: Ortalama arkadaş sayısı ve lonca üyeliği oranı.
        *   Dağılımlar: Arkadaş sayısı dağılımı (histogram) ve lonca üyeliği durumu (pasta grafiği).
        *   Sosyal Faktörlerin Etkisi: Lonca üyeliğinin oynama süresi ve harcama üzerindeki etkisini gösteren kutu grafikleri. Arkadaş sayısı ile oynama süresi arasındaki ilişkiyi gösteren dağılım grafiği.
    *   **Kohort Analizi:**
        *   Haftalık tutundurma: Oyuncuların kaydoldukları haftaya (kohort) göre, sonraki haftalarda ne kadarının aktif kaldığını gösteren ısı haritası (heatmap).
        *   Kohort büyüklükleri: Her bir kayıt haftasındaki toplam oyuncu sayısını gösteren tablo.
    *   **Oyuncu Segmentasyonu:**
        *   K-Means kümeleme: Oyuncuları oynama süresi, harcama, oturum sıklığı gibi davranışsal metrikler kullanarak otomatik olarak gruplara (segmentlere) ayırma.
        *   Segment görselleştirmesi: Oluşturulan segmentlerin oynama süresi ve harcama gibi eksenlerde nasıl konumlandığını gösteren dağılım grafiği.
        *   Segment profilleri: Her bir segmentin ortalama metrik değerlerini gösteren özet tablo.
        *   Segment dağılımı: Toplam oyuncu tabanının segmentlere göre dağılımını gösteren pasta grafiği.
*   **Filtreleme:** Tarih aralığı, oyun türü, oyun zorluğu, cihaz ve lokasyona (ilk 10 ve diğerleri) göre verileri filtreleme imkanı.
*   **Veri İndirme:** Filtrelenmiş güncel verileri CSV formatında indirme butonu.
*   **Türkçe Dil Desteği:** Panel arayüzü ve metrikler Türkçe olarak sunulmaktadır.

## Öneriler (Recommendations)

Paneldeki analizlere dayanarak, Ürün ve Pazarlama ekiplerinin aşağıdaki noktaları dikkate alması önerilir:

1.  **Gözlem:** Oyuncuların önemli bir kısmı ilk birkaç hafta içinde oyunu bırakmaktadır (Kohort Analizi).
    **Öneri:** İlk 1-2 hafta içinde hedeflenmiş başlangıç kampanyaları, görevler ve ödüller uygulayarak erken dönem etkileşimi artırın ve başlangıçtaki oyuncu kaybını (churn) azaltın.
2.  **Gözlem:** Lonca üyeliği, daha yüksek etkileşim ve harcama ile ilişkili görünmektedir (Sosyal Analiz, Gelir Analizi).
    **Öneri:** Lonca bulma ve katılma özelliklerini oyun içinde daha belirgin hale getirin. Bu sosyal faktörü daha da güçlendirmek için lonca ile ilgili daha fazla aktivite ve ödül eklemeyi düşünün.
3.  **Gözlem:** Harcamalar belirli bir oyuncu segmentinde yoğunlaşmakta ve genel dönüşüm oranı mütevazı seviyededir (Gelir Analizi).
    **Öneri:** K-Means ile belirlenen yüksek harcama segmentlerine özel IAP (uygulama içi satın alma) teklifleri geliştirin. İlk satın almayı teşvik etmek ve genel dönüşüm oranını artırmak için başlangıç teklifleri veya paketlerle deneyler yapın.
4.  **Gözlem:** Farklı davranışlara sahip belirgin oyuncu segmentleri mevcuttur (Oyuncu Segmentasyonu).
    **Öneri:** Oyuncu segmentlerine göre farklılaştırılmış özellikler, iletişim stratejileri veya etkinlik katılım yolları tasarlayın (örneğin, etkileşimli ancak harcama yapmayan oyuncular için kozmetik teklifler, yüksek değerli oyuncular için rekabetçi etkinlikler).
5.  **Gözlem:** Harcama ve performans cihaza göre değişiklik göstermektedir (Gelir Analizi, Teknik Performans).
    **Öneri:** Cihazlar arasındaki harcama farklılıklarının nedenlerini araştırın (ör. arayüz farklılıkları, ödeme kolaylığı). Özellikle düşük metrikler gösteren cihazlarda performansı (FPS, çökme oranları) optimize edin.

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
5.  **Gerekli Paketleri Yükleyin (Install Dependencies):** `requirements.txt` dosyası sağlandığı için:
    ```bash
    pip install -r requirements.txt
    ```
    *(Eğer `requirements.txt` yoksa veya güncel değilse: `pip install pandas numpy streamlit plotly scikit-learn`)*

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
├── requirements.txt        # Gerekli Python paketleri (Required Python packages)
└── README.md               # Bu dosya (This file)
```

## Gelecekteki Olası Geliştirmeler (Potential Future Enhancements)

*   K-Means segmentlerine işlevsel isimler verme (ör. "Yüksek Harcama Yapan Aktif Oyuncular", "Sosyal Oyuncular").
*   Daha fazla segmentasyon ve filtreleme seçeneği ekleme (ör. kayıt tarihine göre, belirli başarıları açanlara göre).
*   Grafiklere daha fazla etkileşim ekleme (ör. grafikte bir bölüme tıklayınca diğer grafiklerin filtrelenmesi).
*   Daha gelişmiş makine öğrenimi modelleri entegre etme (ör. Churn (terk etme) tahmini, LTV tahmini).
*   Gerçek zamanlı veri akışı için veritabanı entegrasyonu.
*   A/B testi sonuçlarını analiz etmek için modüller ekleme. 