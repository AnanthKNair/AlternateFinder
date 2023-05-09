import urllib.request
import json
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

##input_url = "https://www.boysnextdoor-apparel.co/collections/all/products.json"

def FindAlternateGroups(input_url):
    your_url = input_url

    with urllib.request.urlopen(your_url) as url:
        data = json.loads(url.read().decode())

    df = pd.DataFrame(data)

    file = []

    for i in range(len(df)):
        file.append(df.products[i]['title'])

    def similarity(X, Y):
        X_list = word_tokenize(X)
        Y_list = word_tokenize(Y)


        sw = stopwords.words('english')
        l1 = [];
        l2 = []


        X_set = {w for w in X_list if not w in sw}
        Y_set = {w for w in Y_list if not w in sw}


        rvector = X_set.union(Y_set)
        for w in rvector:
            if w in X_set:
                l1.append(1)  # create a vector
            else:
                l1.append(0)
            if w in Y_set:
                l2.append(1)
            else:
                l2.append(0)

        c = 0


        for i in range(len(rvector)):
            c = c + (l1[i] * l2[i])
        cosine = c / float((sum(l1)*sum(l2)) ** 0.5)

        return cosine

    checker = []
    master = []
    for i in range(len(file)):
        store = []

        for j in range(len(file)):

            similarity1 = similarity(file[i], file[j])

            if similarity1 > 0.5:  # tuning needed
                store.append(input_url + df.products[j]['handle'])


        odo = {"product alternates": store}

        if len(store) > 1:
            master.append(odo)

    checker = []
    new_store = []
    for i in master:
        count = 0
        for j in i["product alternates"]:

            tracker = len(i["product alternates"])

            if j not in checker:
                checker.append(j)
                count += 1

        if int(count) == int(tracker):
            new_store.append(i)

    return new_store


output = FindAlternateGroups(input("Enter the link. ")+'/products.json')


print(output)

json.dumps(output)