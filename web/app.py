from flask import Flask, render_template, request
from engine.search_engine import SearchEngine
import time

app = Flask(__name__)

engine = SearchEngine("data/corpus.json")

@app.route("/", methods=["GET", "POST"])
def index():

    results = []
    query = ""
    search_time = 0

    if request.method == "POST":
        query = request.form["query"]

        start = time.time()
        results = engine.search(query)
        search_time = time.time() - start

    return render_template(
        "index.html",
        results=results,
        query=query,
        total_docs = engine.indexer.N,
        vocab_size = len(engine.indexer.index),
        search_time=search_time,
        len_results = len(results)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)