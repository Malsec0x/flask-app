# Python file (app.py)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '''
<html>
<body>
<center>
<h1>ACS Project"Building a Kubernetes Cloud Security Infrastructure" .</h1> <br>
<br>
</center>
</body>
</html>
'''
