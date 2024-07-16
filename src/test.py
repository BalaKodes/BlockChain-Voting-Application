import requests

url = "https://control.msg91.com/api/v5/otp?template_id=65de0bcdd6fc0510194af8f2&mobile=917893015625&otp=1234"

payload = {
    "Param1": "value1",
    "Param2": "value2",
    "Param3": "value3"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authkey": "417166AYns3eIQ65dde945P1"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)