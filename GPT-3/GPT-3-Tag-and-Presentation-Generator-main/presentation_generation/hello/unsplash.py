import requests


def get_unsplash_image(query, api_key, width, height, orientation="landscape"):
    results = requests.get("https://api.unsplash.com/search/photos?client_id=" + api_key + "&query="
                           + query + "&per_page=1&orientation" + orientation)
    if results.status_code != 200 or len(results.json()["results"]) == 0:
        return "https://images.unsplash.com/photo-1616441064900-e0adeacda4f3" + "&w=" + str(width) + "&h=" +\
               str(height) + "&fit=crop"
    data = results.json()
    url = data["results"][0]["urls"]["raw"] + "&w=" + str(width) + "&h=" + str(height) + "&fit=crop"
    credits = "Photo by <a href=" + data["results"][0]["user"]["links"]["html"] + \
              "?utm_source=GPT3_makeathon_zesavi&utm_medium=referral\">" + data["results"][0]["user"]["name"] + \
              "</a> on <a href=\"https://unsplash.com/?utm_source=your_app_name&utm_medium=referral\">Unsplash</a>"
    return url, credits
