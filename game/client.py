import requests


for i in range(5000):
    requests.get("http://localhost:8000/draw-card").json()
