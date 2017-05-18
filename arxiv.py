import re
import requests
import pickle
import os


def parse(data, tag):

    # parse atom file
    # e.g. Input :<tag>XYZ </tag> -> Output: XYZ

    pattern = "<" + tag + ">([\s\S]*?)<\/" + tag + ">"
    if all:
        obj = re.findall(pattern, data)
    return obj


def search_and_send(query, start, ids, api_url):
    while True:
        counter = 0
        # url of arXiv API
        # If you want to customize, please change here.
        # detail is shown here, https://arxiv.org/help/api/user-manual
        url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=' + str(start) + '&max_results=100&sortBy=lastUpdatedDate&sortOrder=descending'
        # Get returned value from arXiv API
        data = requests.get(url).text
        # Parse the returned value
        entries = parse(data, "entry")
        for entry in entries:
            # Parse each entry
            url = parse(entry, "id")[0]
            if not(url in ids):
                title = parse(entry, "title")[0]
                # abstract = parse(entry, "summary")[0]
                date = parse(entry, "published")[0]
                message = "\n".join(["=" * 10, "No." + str(counter + 1), "Title:  " + title, "URL: " + url, "Published: " + date])
                requests.post(api_url, json={"text": message})
                ids.append(url)
                counter = counter + 1
                if counter == 10:
                    return 0
        if counter == 0 and len(entries) < 100:
            requests.post(api_url, json={"text": "Currently, there is no available papers"})
            return 0
        elif counter == 0 and len(entries) == 100:
            # When there is no available paper and full query
            start = start + 100


if __name__ == "__main__":
    print("Publish")
    # Set URL of API
    # Please change here
    api_url = API_URL
    # Load log of published data
    if os.path.exists("published.pkl"):
        ids = pickle.load(open("published.pkl"))
    else:
        ids = []
    # Query for arXiv API
    # Please change here
    query = "(cat:stat.ML+OR+cat:cs.CV+OR+cs.HC+OR+cs.IR)+AND+((abs:emotion)+OR+(abs:ECG)+OR+(abs:time\ series))"
    start = 0
    # Post greeting to your Slack
    requests.post(api_url, json={"text": "Hello!!"})
    # Call function
    search_and_send(query, start, ids, api_url)
    # Update log of published data
    pickle.dump(ids, open("published.pkl", "wb"))
