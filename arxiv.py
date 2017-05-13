import urllib
import re
import requests
import pickle
import os


def parse(data, tag):
    pattern = "<" + tag + ">([\s\S]*?)<\/" + tag + ">"
    if all:
        obj = re.findall(pattern, data)
    return obj


def search_and_send(query, start, ids, api_url):
    while True:
        url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=' + str(start) + '&max_results=100&sortBy=lastUpdatedDate&sortOrder=descending'
        data = urllib.urlopen(url).read()
        entries = parse(data, "entry")
        print(len(entries))
        counter = 0
        for entry in entries:
            # print(counter)
            url = parse(entry, "id")[0]
            if not(url in ids):
                title = parse(entry, "title")[0]
                abstract = parse(entry, "summary")[0]
                date = parse(entry, "published")[0]
                message = "\n".join(["=" * 10, "No." + str(counter + 1), "Title  " + title, "Abs " + abstract[:1000], "URL " + url, "Published " + date])
                requests.post(api_url, json={"text": message})
                ids.append(url)
                counter = counter + 1
                if counter == 3:
                    return 0
        if counter == 0 and len(entries) < 100:
            requests.post(api_url, json={"text": "Currently, there is no available papers"})
            return 0
        elif counter == 0 and len(entries) == 100:
            # When there is no available paper and full query
            start = start + 100


if __name__ == "__main__":
    api_url = "WRITE Your URL of Incoming WebHooks API"
    if os.path.exists("published.pkl"):
        ids = pickle.load(open("published.pkl"))
    else:
        ids = []
    query = "(cat:stat.ML+OR+cat:cs.CV+OR+cs.HC+cs.IR)+AND+((abs:emotion)+OR+(abs:ECG)+OR+(abs:time\ series))"
    start = 0
    requests.post(api_url, json={"text": "Good morning!!"})
    search_and_send(query, start, ids, api_url)
    pickle.dump(ids, open("published.pkl", "wb"))
