import pickle

fname = "samples.txt"
with open(fname) as f:
	content = f.readlines()

list_of_data = []
data = {}
list_of_L = []
for line in content:
	pro_line = line.split("\t")

	if pro_line[0] == 'P':
		data['L'] = list_of_L
		list_of_data.append(data)
		data = {}
		list_of_L = []
	elif pro_line[0] == 'L':
		list_of_L.append(pro_line[1][:-1])


	if len(pro_line) == 1:
		continue
	else:
		data[pro_line[0]] = pro_line[1][:-1]

data['L'] = list_of_L
list_of_data.append(data)
list_of_data = list_of_data[1:]

# print(list_of_data[7])
# Save Binary data
pickle.dump(list_of_data, open("quotes_02_sample.dat", "wb"))

# Load Binary Data
# load_data = pickle.load(open("quotes_02_sample.dat", "rb" ))

list_of_edge = []

for line in list_of_data:
	if (len(line['L'])!=0):
		for l in line['L']:
			list_of_edge.append((line['P'],l))

buffer_to_write = "Source,Timestamp,Quote,Target\n"
for edge in list_of_data:
	if edge.get("P"):
		val_P = edge["P"]
	else:
		val_P = ""

	if edge.get("T"):
		val_T = edge["T"]
	else:
		val_T = ""

	if edge.get("Q"):
		val_Q = edge["Q"]
	else:
		val_Q = ""

	if edge.get("L"):
		val_L = edge["L"]
	else:
		val_L = ""

	buffer_to_write += "'"+val_P+"','"+val_T+"','"+val_Q+"','"+" ".join(val_L)+"'\n"

print(buffer_to_write, file=open("node_table.csv","w"))

buffer_to_write = "Source,Target\n"
for i,edge in enumerate(list_of_edge):
	buffer_to_write += edge[0]+","+edge[1]+"\n"

print(buffer_to_write, file=open("edge_table.csv","w"))

# {
# 	'P': 'http://boston.com/news/local/rhode_island/articles/2009/01/31/mass_daily?rss_id=boston.com+--+latest+news',
# 	'T': '2009-02-01 02:12:41',
# 	'Q': 'massachusetts daily lottery',
# 	'L': [
# 		'http://boards.boston.com/javascript:openwindow(',
# 		'http://boston.com/news/local/rhode_island/articles/2009/01/31/mass_daily?mode=pf',
# 		'http://boards.boston.com/#', 'http://boston.com/news/local/rhode_island/?camp=related-articles:on:link:article-page:more'
# 		]
# }
