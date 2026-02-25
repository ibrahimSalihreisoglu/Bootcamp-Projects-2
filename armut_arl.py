import pandas as pd
from collections import Counter
from itertools import combinations


# VERİYİ OKU
df = pd.read_csv("armut_data.csv")


# HİZMET OLUŞTUR → "ServiceId_CategoryId"
df["Hizmet"] = df["ServiceId"].astype(str) + "_" + df["CategoryId"].astype(str)


# SEPET OLUŞTUR → "UserId_Yıl-Ay"
df["CreateDate"] = pd.to_datetime(df["CreateDate"])
df["SepetID"] = df["UserId"].astype(str) + "_" + df["CreateDate"].dt.to_period("M").astype(str)


# ADIM 1: PİVOT TABLE
# satır: sepet, sütun: hizmet, değer: 0 veya 1
pivot = df.groupby(["SepetID", "Hizmet"])["Hizmet"].count().unstack().fillna(0)
pivot = pivot.map(lambda x: 1 if x > 0 else 0)
print(pivot.iloc[:5, :5])

# ADIM 2: BİRLİKTELİK KURALLARI

# her sepetteki hizmetleri topla (2+ hizmet olanlar)
sepetler = []
for sid, row in pivot.iterrows():
    items = set(row[row == 1].index)
    if len(items) > 1:
        sepetler.append(items)

# her hizmetin ve her çiftin kaç sepette geçtiğini say
tek = Counter()
cift = Counter()
for s in sepetler:
    for i in s:
        tek[i] += 1
    for p in combinations(sorted(s), 2):
        cift[p] += 1

# kuralları hesapla
toplam = len(pivot)
kurallar = []
for (a, b), n in cift.items():
    sup = n / toplam
    kurallar.append({"Onceki": a, "Sonraki": b, "support": sup, "confidence": n/tek[a], "lift": (n/tek[a]) / (tek[b]/toplam)})
    kurallar.append({"Onceki": b, "Sonraki": a, "support": sup, "confidence": n/tek[b], "lift": (n/tek[b]) / (tek[a]/toplam)})

rules = pd.DataFrame(kurallar).sort_values("lift", ascending=False)
print(rules.head(10).to_string(index=False))


# ADIM 3: 2_0 İÇİN ÖNERİ
def arl_recommender(rules, hizmet, n=5):
    r = rules[rules["Onceki"] == hizmet].sort_values("lift", ascending=False)
    return list(r["Sonraki"].head(n))

print("\n2_0 için öneriler:", arl_recommender(rules, "2_0"))
