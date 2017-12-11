import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans, DBSCAN


load_data = pickle.load(open("quotes_02_sample.dat", "rb" ))

def create_dictionary_to_csv():
	node_dictionary = {}
	# Creating list of node
	string_container = "Index,P\n"
	for i,data in enumerate(load_data):
		primary_key = str(data['P']).replace(",","")
		node_dictionary[primary_key] = i
		string_container += str(i) + "," + primary_key + "\n"
		load_data[i]["index"] = i

	list_of_edges = []
	# Creating list of edge
	for i,data in enumerate(load_data):
		# Iterate each link
		if data.get("L"):
			for link in data["L"]:
				link = str(link).replace(",","")	
				if node_dictionary.get(link):
					list_of_edges.append((i,node_dictionary.get(link)))
				# else:
				# throw Link :)

	# Creating csv for node dictionary 
	string_container = "Index,P\n"
	for k, v in node_dictionary.items():
		string_container += str(v) + "," + str(k).replace(",","") + "\n"
	print(string_container, file=open("node_dictionary.csv","w"))

	# Creating csv for list of edges
	string_container = "Source,Target\n"
	for edge in list_of_edges:
		string_container += str(edge[0]) + "," + str(edge[1]) + "\n"
	print(string_container, file=open("edge_table_numeric.csv","w"))





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

create_dictionary_to_csv()



# Stop Words
prestopwords = pd.read_csv("stopwords.csv")
stopwords = [a[0] for a in prestopwords.values.tolist()]

vectorizer = CountVectorizer(stop_words=stopwords)
X = vectorizer.fit_transform(dataset)

true_k = 33

# Using KMeans
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)

# Using DBSCAN
# model = DBSCAN(eps=0.5, min_samples=5, metric='euclidean', metric_params=None, algorithm='auto', leaf_size=30, p=None, n_jobs=1)


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

# labels = model.labels_

# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

cluster_membership = []
for i in range(0,true_k + 1):
	cluster_membership.append([])


for data in load_data:
	if data.get('Q'):
		Y = vectorizer.transform([data['Q']])
		prediction = model.predict(Y)
		# data['C'] = int(prediction)
		cluster_membership[int(prediction)].append(data)
		# print(int(prediction),Y)
	else:
		cluster_membership[-1].append(data)
		# data['C'] = -1
		# print(data['C'])
		# print("Else",data)


# Save Binary data
# pickle.dump(load_data, open("quotes_02_clustered_sample.dat", "wb"))
pickle.dump(cluster_membership, open("cluster_membership.dat", "wb"))




# Y = vectorizer.transform(["chrome browser to open."])
# prediction = model.predict(Y)
# print(prediction)
#
# Y = vectorizer.transform(["My cat is hungry."])
# prediction = model.predict(Y)
# print(prediction)
