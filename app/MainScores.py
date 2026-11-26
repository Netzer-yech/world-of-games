# The score web service: shows the saved score in a browser, while the games stay in the console
from flask import Flask

import Score

# The web application object; Flask uses __name__ to find files that belong to it
app = Flask(__name__)
# The port Flask listens on; Docker maps host port 8777 to it (documented in the README)
INTERNAL_PORT = 5000

# Build the whole page around the score element; one copy of the HTML for both pages
def _page(score_element):
    return f"""<html>
  <head><title>Scores Game</title></head>
  <body>
    <h1>The score is {score_element}</h1>
  </body>
</html>"""

# The home page: reads the score again on every request, so a new win shows after a refresh
@app.route("/")
def show_score():
    try:
        # missing_ok=False: on the web, no file means missing data, never a fake 0
        score = Score.read_score(missing_ok=False)
    # Missing or broken data: the reason in red with a failure status, never a fake number
    except Score.ScoreError as error:
        return _page(f'<span id="score" style="color:red">{error}</span>'), 500
    return _page(f'<span id="score">{score}</span>')

# Start the web server; it keeps running and answering requests until Ctrl+C
def score_server():
    # 0.0.0.0 = listen on every network interface, so Docker can forward requests in;
    # debug stays off because its error pages expose code and file paths
    app.run(host="0.0.0.0", port=INTERNAL_PORT, debug=False)


# Run only when started directly, not when imported (e.g. by tests)
if __name__ == "__main__":
    score_server()
