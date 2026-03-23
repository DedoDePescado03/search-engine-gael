from flask import Flask, render_template, request
from engine.search_engine import SearchEngine
import time

app = Flask(__name__)

engine = SearchEngine("data/corpus.json")


@app.route("/", methods=["GET", "POST"])
def index():

    #Default values for when there is no active search
    results = []
    query = ""
    search_time = 0

    if request.method == "POST":
        #Get the query entered by the user from the HTML form
        query = request.form["query"]

        #Measure search time to display it in the UI.
        start = time.time()
        results = engine.search(query)
        search_time = time.time() - start

    return render_template(
        "index.html",
        results=results,
        query=query,
        #Total number of documents indexed in the corpus
        total_docs=engine.indexer.N,
        #Number of unique terms in the index
        vocab_size=len(engine.indexer.index),
        #Time taken to execute the search (in seconds)
        search_time=search_time,
        #Number of results found for the current query
        len_results=len(results)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)