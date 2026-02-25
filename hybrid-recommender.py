import pandas as pd

movie = pd.read_csv("movie.csv")                # film bilgileri: movieId, title, genres
rating = pd.read_csv("rating.csv")              # puanlar: userId, movieId, rating, timestamp
df = rating.merge(movie, how="left", on="movieId")  # ikisini movieId üzerinden birleştir

# 1000'den az oy alan filmleri çıkar
rare = df["title"].value_counts()                # her film kaç kere oylanmış
rare = rare[rare < 1000].index                   # 1000'den az olanların isimlerini al
df = df[~df["title"].isin(rare)]                 # bu filmleri veri setinden çıkar

# pivot table: satır=user, sütun=film, değer=puan
# mesela: userId=5, "Titanic" sütunu = 4.0 ise → 5 numaralı kullanıcı Titanic'e 4 puan vermiş
user_movie_df = df.pivot_table(index="userId", columns="title", values="rating")


random_user = int(pd.Series(user_movie_df.index).sample(1, random_state=45).values[0])

# bu kullanıcının izlediği filmler (NaN olmayan = izlemiş)
watched = user_movie_df.loc[random_user].dropna().index.tolist()

# pivot tablodan sadece izlenen film sütunlarını al
watched_df = user_movie_df[watched]

# her kullanıcı bu filmlerden kaçını izlemiş? (NaN olmayan hücreleri say)
counts = watched_df.notna().sum(axis=1)

# %60'ından fazlasını izleyenleri al (benzer kullanıcı adayları)
similar_users = counts[counts > len(watched) * 0.6].index

# bu kullanıcılar arasındaki korelasyonu hesapla
# korelasyon = iki kullanıcının filmlere verdiği puanlar ne kadar benzer
corr_df = watched_df.loc[similar_users].T.corr()

# seçili kullanıcıyla korelasyonu 0.65'ten yüksek olanları al
top_users = corr_df[random_user].drop(random_user)   # kendisini çıkar
top_users = top_users[top_users > 0.65].reset_index() # 0.65+ olanları filtrele
top_users.columns = ["userId", "corr"]                 # sütun isimlerini düzenle

# bu kullanıcıların rating bilgisini ekle
merged = top_users.merge(rating, on="userId")

# weighted score = korelasyon × puan
# korelasyonu yüksek kullanıcının verdiği puan daha değerli
merged["w_score"] = merged["corr"] * merged["rating"]

# her film için ortalama w_score hesapla, 3.5'ten büyük olanları al
rec = merged.groupby("movieId")["w_score"].mean().reset_index()
rec = rec[rec["w_score"] > 3.5].sort_values("w_score", ascending=False)

# film isimlerini getir ve ilk 5'i al
user_based_5 = rec.merge(movie)["title"].head(5).tolist()


# ITEM-BASED (5 film)
# mantık: bu filme benzeyen filmler hangileri 


# kullanıcının 5 puan verdiği en güncel filmi bul
user_r = rating[rating["userId"] == random_user]          # kullanıcının tüm puanları
last_id = user_r[user_r["rating"] == 5] \
    .sort_values("timestamp", ascending=False) \
    ["movieId"].values[0]                                  # 5 puan + en yeni → movieId
last_title = movie[movie["movieId"] == last_id]["title"].values[0]  # film ismini al

# bu filmle diğer filmlerin korelasyonunu hesapla
# korelasyon = iki filme puan veren kullanıcıların puanları ne kadar benzer
corrs = user_movie_df.corrwith(user_movie_df[last_title]).sort_values(ascending=False)

# kendisi hariç en yüksek korelasyonlu 5 filmi al
item_based_5 = corrs.drop(last_title).head(5).index.tolist()


# SONUÇ: 5 + 5 = 10 FİLM

print(f"Kullanıcı: {random_user}")
print(f"\nUser-Based (5 film):")
for i, f in enumerate(user_based_5, 1):
    print(f"  {i}. {f}")
print(f"\nItem-Based (5 film) - '{last_title}' baz alınarak:")
for i, f in enumerate(item_based_5, 1):
    print(f"  {i+5}. {f}")
