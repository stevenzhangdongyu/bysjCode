import requests

resp = requests.post("http://localhost:5000/predict",
                     files={"file": open('testImages/doubleGreenLight.jpg','rb')})
print(resp)