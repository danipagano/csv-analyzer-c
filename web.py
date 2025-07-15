from flask import Flask, render_template_string, request
import subprocess
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CSV Analyzer </title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <style>
    body { background: #f5f7fa; }
    .container { max-width: 480px; margin-top: 40px; }
    .output-box { font-family: 'Fira Mono', monospace; background: #fff; border-radius: 6px; padding: 1em; border: 1px solid #eee; }
  </style>
</head>
<body>
<div class="container shadow bg-white p-4 rounded">
  <h2 class="mb-3">CSV Analyzer <small class="text-muted">(main)</small></h2>
  <form method="post" enctype="multipart/form-data">
    <div class="mb-3">
      <label for="csvfile" class="form-label">CSV File</label>
      <input class="form-control" type="file" name="csvfile" id="csvfile" required>
    </div>
    <div class="mb-3">
      <label class="form-label me-2">Type</label>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="radio" name="type" value="r" id="row" checked>
        <label class="form-check-label" for="row">Row</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="radio" name="type" value="c" id="col">
        <label class="form-check-label" for="col">Column</label>
      </div>
    </div>
    <div class="mb-3">
      <label for="index" class="form-label">Index (0-based)</label>
      <input class="form-control" type="number" min="0" name="index" id="index" required>
    </div>
    <button type="submit" class="btn btn-primary w-100">Analyze</button>
  </form>
  {% if output %}
    <div class="mt-4">
      <label class="form-label">Result:</label>
      <div class="output-box">{{ output }}</div>
    </div>
  {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        file = request.files["csvfile"]
        if file:
            filepath = "uploaded.csv"
            file.save(filepath)
            row_or_col = request.form["type"]
            index = request.form["index"]
            try:
                result = subprocess.run(
                    ["./main", filepath, row_or_col, str(index)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output = result.stdout.strip()
            except Exception as e:
                output = f"Error: {e}"
            os.remove(filepath)
    return render_template_string(HTML, output=output)

if __name__ == "__main__":
    app.run(debug=True)
