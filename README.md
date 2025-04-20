# Scriptify - Movie Quote Search Engine

**Scriptify** is a Flask-based web app that allows you to look through movie quotes across multiple scripts and show which movie they belong in
Pefect for researchers, fans, or to sound smart in movie trivia night

---

**Features**
- **Search** movie scripts by quote or phrase
- **See matching lines** with the name of the movie
- **New search instantly** from the results page
- Powered by **TF-IDF** to ensure only relevent lines are present

## Screenshots
![Home](./screenshots/home.png) | [Results](./screenshots/results.png)|

## Demo

## Tech Stack

- Python 3.11
- Flask + Jinja2
- HTML/CSS (with Bootstrap)
- Scikit-learn (`TfidfVectorizer`)
- SQLite for optional data persistence

- Movie scripts sourced from IMSDB
Made by Ivan Garcia-Mora