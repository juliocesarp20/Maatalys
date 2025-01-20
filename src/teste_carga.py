import json
from concurrent.futures import ThreadPoolExecutor

import requests

url = "http://localhost:8000/investigation"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZTMiLCJleHAiOjE3Mzc1Njk2NzN9.U_oXTBoSJAjxRVGkrKpz_3ijFlKbr6ZmN6ftutm9iqo",
}
payload = {
    "name": "Investigation Example",
    "searches": [
        {
            "source": "Source 1",
            "parameters": [
                {"name": "param_1_name", "value": "param_1_value"},
                {"name": "param_2_name", "value": "param_2_value"},
            ],
        }
    ],
}


def send_request(i):
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Request {i}: Status Code {response.status_code}")


# Send 100 requests in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(1, 101):
        executor.submit(send_request, i)
