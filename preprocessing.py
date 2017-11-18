import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


load_data = pickle.load(open("quotes_02_sample.dat", "rb" ))

def convert_to_numeric():
	idx_data = len(load_data)

	string_container = "Source,Target\n"

	link_dictionary = []
	for x in range(0,len(load_data)):
		link_dictionary.append("dummy")

	for i,data in enumerate(load_data):
		link_dictionary[i] = data['P']
		for link in data['L']:
			# For Numeric Preprocess
			string_container += str(i) + "," + str(idx_data) + "\n"
			idx_data += 1
			# For Numeric Dictionary
			link_dictionary.append(link)

	print(string_container, file=open("nodetable_numeric.csv","w"))

	string_container = "index,P\n"
	for i,l in enumerate(link_dictionary):
		string_container += str(i) + "," + str(l) + "\n"

	print(string_container, file=open("node_dict.csv","w"))

	pickle.dump(link, open("sample_dictionary.dat", "wb"))

def get_rich_data():
	rich_data = []

	for data in load_data:
		if data.get('Q'):
			rich_data.append(data.get('Q'))

	return rich_data


dataset = get_rich_data()

# Stop Words
prestopwords = pd.read_csv("stopwords.csv")
stopwords = [a[0] for a in prestopwords.values.tolist()]


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(dataset)

true_k = 12
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print


print("\n")
print("Prediction")

Y = vectorizer.transform(["chrome browser to open."])
prediction = model.predict(Y)
print(prediction)

Y = vectorizer.transform(["My cat is hungry."])
prediction = model.predict(Y)
print(prediction)
