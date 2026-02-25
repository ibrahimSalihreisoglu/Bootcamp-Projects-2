import pandas as pd


# VERİ HAZIRLAMA

movie = pd.read_csv("movie.csv")                        # film bilgileri: movieId, title, genres
rating = pd.read_csv("rating.csv")                      # puanlar: userId, movieId, rating, timestamp
df = rating.merge(movie, how="left", on="movieId")       # ikisini movieId üzerinden birleştir

# 1000'den az oy alan filmleri çıkar
rare = df["title"].value_counts()                        # her film kaç kere oylanmış
rare = rare[rare < 1000].index                           # 1000'den az olanların isimlerini al
df = df[~df["title"].isin(rare)]                         # bu filmleri veri setinden çıkar

# pivot table: satır=user, sütun=film, değer=puan
user_movie_df = df.pivot_table(index="userId", columns="title", values="rating")


# USER-BASED RECOMMENDATION (5 film)

# rastgele kullanıcı seç
random_user = int(pd.Series(user_movie_df.index).sample(1, random_state=45).values[0])

# bu kullanıcının izlediği filmler (NaN olmayan = izlemiş)
watched = user_movie_df.loc[random_user].dropna().index.tolist()

# pivot tablodan sadece izlenen film sütunlarını al
watched_df = user_movie_df[watched]

# her kullanıcı bu filmlerden kaçını izlemiş?
counts = watched_df.notna().sum(axis=1)

# %60'ından fazlasını izleyenleri al
similar_users = counts[counts > len(watched) * 0.6].index

# kullanıcılar arası korelasyon
corr_df = watched_df.loc[similar_users].T.corr()

# korelasyonu 0.65+ olanları al
top_users = corr_df[random_user].drop(random_user)
top_users = top_users[top_users > 0.65].reset_index()
top_users.columns = ["userId", "corr"]

# rating bilgisini ekle ve weighted score hesapla
merged = top_users.merge(rating, on="userId")
merged["w_score"] = merged["corr"] * merged["rating"]

# film başına ortalama w_score → ilk 5 film
rec = merged.groupby("movieId")["w_score"].mean().reset_index()
rec = rec[rec["w_score"] > 3.5].sort_values("w_score", ascending=False)
user_based_5 = rec.merge(movie)["title"].head(5).tolist()


# ITEM-BASED RECOMMENDATION (5 film)

# kullanıcının 5 puan verdiği en güncel film
user_r = rating[rating["userId"] == random_user]
last_id = user_r[user_r["rating"] == 5] \
    .sort_values("timestamp", ascending=False)["movieId"].values[0]
last_title = movie[movie["movieId"] == last_id]["title"].values[0]

# bu filmle diğer filmlerin korelasyonu
corrs = user_movie_df.corrwith(user_movie_df[last_title]).sort_values(ascending=False)
item_based_5 = corrs.drop(last_title).head(5).index.tolist()


# SONUÇ: HYBRID 10 FİLM

print(f"Kullanıcı: {random_user}")
print(f"\nUser-Based (5 film):")
for i, f in enumerate(user_based_5, 1):
    print(f"  {i}. {f}")
print(f"\nItem-Based (5 film) - '{last_title}' baz alınarak:")
for i, f in enumerate(item_based_5, 1):
    print(f"  {i+5}. {f}")
