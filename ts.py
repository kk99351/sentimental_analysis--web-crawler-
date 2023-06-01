from sklearn.datasets import fetch_20newsgroups
twnety_train = fetch_20newsgroups(subset='train',categories='categories', shuffle=True, random_state=42)
print(twnety_train)