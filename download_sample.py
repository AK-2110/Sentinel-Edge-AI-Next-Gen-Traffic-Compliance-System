import requests

url = "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/bus.jpg"
response = requests.get(url)

with open("sample_traffic.jpg", "wb") as f:
    f.write(response.content)

print("Downloaded sample_traffic.jpg")
