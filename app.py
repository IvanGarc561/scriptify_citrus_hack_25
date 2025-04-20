from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
def load_scripts(script_folder = 'scripts'):
    script_data = []
    for filename in os.listdir(script_folder):
        if filename.endswith('.txt'):
            movie_title = filename.replace('.txt', '').replace("_", '').title()
            file_path = os.path.join(script_folder, filename)

            with open(file_path, 'r', encoding ='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.isupper():
                        continue
                    script_data.append({ "movie": movie_title, "line": line})
    return script_data

script_lines = load_scripts()

# Build Search index once when app starts
def build_tfidf_index(lines):
    vectorizer = TfidfVectorizer()
    docs = [line['line'] for line in lines]
    matrix = vectorizer.fit_transform(docs)
    return vectorizer, matrix, lines

# When user seraches
def search_with_tfidf(query, vectorizer, matrix, lines):
    q_vec = vectorizer.transform([query])
    scores = (q_vec @ matrix.T).toarray()[0]
    scored_lines = [
        (score, lines[i]) for i, score in enumerate(scores) if score > 0
    ]
    scored_lines.sort(reverse = True)
    return [line for score, line in scored_lines]

vectorizer, matrix, lines_for_tfidf = build_tfidf_index(script_lines)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/search")
def search():
    query = request.args.get("query", "")
    results = search_with_tfidf(query, vectorizer, matrix, lines_for_tfidf)
    if not results:
        results = search_script_lines(query, script_lines)
    return render_template("results.html", results=results, query=query)

def search_script_lines(query, scripts):
    return [
        entry for entry in scripts
        if query.lower() in entry['line'].lower()
    ]

# comment
if __name__ == "__main__":
    app.run(debug=True)
