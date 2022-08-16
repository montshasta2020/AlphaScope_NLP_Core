import requests
import time


def find_best_match_cond(data, condition):
    max_priority_i = -1
    for i, res in enumerate(data):
        if res["premium"] == 0 and condition(res) and \
                (max_priority_i == -1 or res["priority"] > data[max_priority_i]["priority"]):
            max_priority_i = i
    return max_priority_i


def find_best_match_for_result(results):
    if results.status_code != 200 or len(results.json()["data"]) == 0:
        return -1
    data = results.json()["data"]

    best_i = find_best_match_cond(data, lambda r: r["style_name"] == "Flat")
    if best_i < 0:
        best_i = find_best_match_cond(data, lambda r: True)
    return best_i


class FlatIconParser:

    def __init__(self, apikey):
        self.apikey = apikey
        self.headers = None
        self.expires = None

    def reconnect(self):
        res = requests.post("https://api.flaticon.com/v2/app/authentication",
                            data={"apikey": self.apikey})
        assert res.status_code == 200
        self.headers = {"Authorization": "Bearer " + res.json()["data"]["token"]}
        self.expires = res.json()["data"]["expires"]

    def verify_connection(self):
        # no auth yet or token will be valid for less than 60 seconds from now on
        if self.headers is None or self.expires - time.time() < 60:
            self.reconnect()

    def find_best_match(self, query):
        self.verify_connection()
        results = requests.get("https://api.flaticon.com/v2/search/icons?q=" + query + "&color=2", headers=self.headers)
        best_i = find_best_match_for_result(results)
        if best_i < 0:
            results = requests.get("https://api.flaticon.com/v2/search/icons?q=" + query, headers=self.headers)
            best_i = find_best_match_for_result(results)
        if best_i < 0:
            if " " in query:
                return self.find_best_match(query.split(" ")[0])
            else:
                return "https://image.flaticon.com/icons/png/512/2496/2496846.png", ""
        data = results.json()["data"]
        credit_string = ""
        return data[best_i]["images"]["png"]["512"], credit_string


def print_urls(data):
    for i in range(len(data)):
        print(str(i) + " (" + data[i]["priority"] + "): " + data[i]["images"]["png"]["512"])


def print_styles(headers):
    res = requests.get("https://api.flaticon.com/v2/search/icons?q=money&styleId=8&color=2",
                       headers=headers)
    print(res.json())
