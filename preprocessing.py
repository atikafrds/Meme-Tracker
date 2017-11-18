import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


load_data = pickle.load(open("quotes_02_sample.dat", "rb" ))

# Make a numeric version of edge table
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

	print(string_container, file=open("edge_table_numeric.csv","w"))

	string_container = "Index,P\n"
	for i,l in enumerate(link_dictionary):
		string_container += str(i) + "," + str(l) + "\n"

	print(string_container, file=open("node_dictionary.csv","w"))

	pickle.dump(link, open("sample_dictionary.dat", "wb"))


rich_data_list = []

# Get list of quotes
def get_rich_data():
	rich_data = []

	for data in load_data:
		if data.get('Q'):
			rich_data.append(data.get('Q'))
			rich_data_list.append(data)

	return rich_data

dataset = get_rich_data()
convert_to_numeric()

# Stop Words
prestopwords = pd.read_csv("stopwords.csv")
stopwords = [a[0] for a in prestopwords.values.tolist()]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(dataset)

true_k = 2
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

# print("\n")
# print("Prediction")

for data in load_data:
	if data.get('Q'):
		Y = vectorizer.transform([data['Q']])
		prediction = model.predict(Y)
		data['C'] = int(prediction)
		print(data['C'])
	else:
		data['C'] = -1
		print(data['C'])

print("\n")
print("\n")
print(load_data)

# Save Binary data
pickle.dump(load_data, open("quotes_02_clustered_sample.dat", "wb"))

# Y = vectorizer.transform(["chrome browser to open."])
# prediction = model.predict(Y)
# print(prediction)
#
# Y = vectorizer.transform(["My cat is hungry."])
# prediction = model.predict(Y)
# print(prediction)
