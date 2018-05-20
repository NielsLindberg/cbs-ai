g = open('reviews.txt','r') # What we know!
reviews = list(map(lambda x:x[:-1],g.readlines()))
g.close()

for idx, each in enumerate(reviews[:10]):
	with open("data/review_" + str(idx) + ".txt", "w") as text_file:
		text_file.write(str(each))