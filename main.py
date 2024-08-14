import lottery
from flask import Flask, request

app = Flask(__name__)

# Simple Flask web site for holding a lotter for a fixed number of
# concert seats.

@app.route("/", methods=["GET", "POST"])
def upload_file():
    print(request)
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            # Process the file content as needed
            output = f"<pre>{lottery.lottery(file)}</pre>"
        else:
            output = "Please click on <strong>Choose file</strong><br>"
        return f'{output}\n\n<a href="/">Upload another file</a>'
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Upload File</title>
</head>
<body>
    <p>
    Click on <strong>Choose File</strong> and navigate to the input file.<br>
    Then click on <strong>Upload</Strong>.<br>
    Each line of the uploaded file should contain the number<br>
    of seats requested, a space, followed by the name of the requestor.
</p>
    <form method="POST" enctype="multipart/form-data" action="/">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
