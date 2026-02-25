# 🛒 Armut - Association Rule Learning ile Hizmet Öneri Sistemi

## 🇹🇷 Türkçe

### Proje Hakkında
Armut hizmet platformunun kullanıcı verisi üzerinde **Birliktelik Kuralı Analizi (ARL)** uygulanarak, bir hizmeti alan kullanıcıya başka hangi hizmetlerin önerilebileceği belirlenmiştir.

### Veri Seti
| Değişken | Açıklama |
|----------|----------|
| `UserId` | Kullanıcı numarası |
| `ServiceId` | Anonimleştirilmiş hizmet numarası |
| `CategoryId` | Anonimleştirilmiş kategori numarası |
| `CreateDate` | Hizmetin satın alındığı tarih |

- **162.523** işlem kaydı | **50** farklı hizmet | **71.220** benzersiz sepet

### Metodoloji
1. **Veri Hazırlama:** ServiceId + CategoryId → Hizmet, UserId + Ay → SepetID
2. **Pivot Table:** Sepet × Hizmet tablosu (0/1)
3. **Birliktelik Kuralları:** Support, Confidence, Lift hesaplama
4. **Öneri:** `arl_recommender` fonksiyonu ile hizmet önerisi

### Sonuç
`2_0` hizmeti alan kullanıcıya öneriler:

| Sıra | Hizmet | Lift |
|------|--------|------|
| 1 | 22_0 | 2.68 |
| 2 | 25_0 | 2.40 |
| 3 | 15_1 | 2.15 |

### Kullanım
```bash
pip install pandas
python armut_arl.py
```

---

## 🇬🇧 English

### About
**Association Rule Learning (ARL)** applied to Armut service platform data to recommend services to users based on co-purchase patterns.

### Methodology
1. **Data Prep:** Created Service (ServiceId_CategoryId) and BasketID (UserId_Month)
2. **Pivot Table:** Basket × Service binary matrix
3. **Association Rules:** Calculated Support, Confidence, Lift
4. **Recommendation:** `arl_recommender` function for service suggestions

### Result
Recommendations for a user who purchased service `2_0`: **22_0**, **25_0**, **15_1**

### Tech Stack
Python, Pandas, Collections, Itertools






# 🎬 Hybrid Recommender System - Movie Recommendation

---

## 🇹🇷 Türkçe

### Proje Hakkında

Bu projede **MovieLens** veri seti üzerinde **User-Based** ve **Item-Based** yöntemleri birleştirerek bir **Hybrid Recommender System** geliştirilmiştir. Verilen bir kullanıcıya toplam 10 film önerisi yapılmaktadır.

### Veri Seti

MovieLens tarafından sağlanan veri seti 138.493 kullanıcı ve 27.278 film üzerinde 20.000.263 derecelendirme içermektedir.

**movie.csv**

| Değişken | Açıklama |
|----------|----------|
| `movieId` | Eşsiz film numarası |
| `title` | Film adı |
| `genres` | Film türü |

**rating.csv**

| Değişken | Açıklama |
|----------|----------|
| `userId` | Eşsiz kullanıcı numarası |
| `movieId` | Eşsiz film numarası |
| `rating` | Kullanıcının filme verdiği puan |
| `timestamp` | Değerlendirme tarihi |

### Metodoloji

#### Veri Hazırlama
- movie ve rating tabloları `movieId` üzerinden birleştirildi
- 1000'den az oy alan filmler veri setinden çıkarıldı
- Kullanıcı × Film pivot tablosu oluşturuldu

#### User-Based Recommendation (5 film)
- Rastgele bir kullanıcı seçildi
- Bu kullanıcının izlediği filmlerin %60'ından fazlasını izleyen benzer kullanıcılar bulundu
- Kullanıcılar arası korelasyon hesaplanarak 0.65+ olanlar filtrelendi
- **Weighted Score = Korelasyon × Puan** formülü ile ağırlıklı puanlama yapıldı
- En yüksek weighted score'a sahip 5 film önerildi

#### Item-Based Recommendation (5 film)
- Kullanıcının 5 puan verdiği en güncel film seçildi
- Bu film ile diğer filmlerin korelasyonu hesaplandı
- En yüksek korelasyona sahip 5 film önerildi

#### Sonuç: Hybrid (10 film)
- User-Based 5 film + Item-Based 5 film = **10 film önerisi**

### Kullanılan Teknolojiler

- Python 3
- Pandas

### Nasıl Çalıştırılır

```bash
pip install pandas
python hybrid_recommender.py
```


---

## 🇬🇧 English

### About the Project

In this project, a **Hybrid Recommender System** was developed on the **MovieLens** dataset by combining **User-Based** and **Item-Based** methods. A total of 10 movie recommendations are generated for a given user.

### Dataset

The dataset provided by MovieLens contains 20,000,263 ratings across 138,493 users and 27,278 movies.

### Methodology

#### Data Preparation
- movie and rating tables were merged on `movieId`
- Movies with fewer than 1000 ratings were removed
- A User × Movie pivot table was created

#### User-Based Recommendation (5 movies)
- A random user was selected
- Similar users who watched 60%+ of the same movies were identified
- User-to-user correlation was calculated, filtering for 0.65+
- **Weighted Score = Correlation × Rating** was used for ranking
- Top 5 movies by weighted score were recommended

#### Item-Based Recommendation (5 movies)
- The user's most recent 5-star rated movie was selected
- Correlation between this movie and all others was calculated
- Top 5 most correlated movies were recommended

#### Result: Hybrid (10 movies)
- User-Based 5 + Item-Based 5 = **10 movie recommendations**

### Technologies Used

- Python 3
- Pandas

### How to Run

```bash
pip install pandas
python hybrid_recommender.py
```

> **Note:** movie.csv and rating.csv can be downloaded from [MovieLens](https://grouplens.org/datasets/movielens/).

---


```
## 📥 Veri Seti / Dataset

📎 (https://www.kaggle.com/datasets/ibrahimsalihreisolu/movie-rating)






