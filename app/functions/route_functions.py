import requests
# https://docs.inrix.com/traffic/routing/#get-findroute

def find_route_fetch(pointA: str, pointB: str, pointC: str, pointD: str, bearerToken: str):
    wp_1 = pointA.replace(',', '%2C')
    wp_2 = pointB.replace(',', '%2C')
    wp_3 = pointC.replace(',', '%2C')
    wp_4 = pointD.replace(',', '%2C')
    URL = f'https://api.iq.inrix.com/findRoute?wp_1={wp_1}&wp_2={wp_2}&wp_3={wp_3}&wp_4={wp_4}&format=json'
    headers = {
    "Authorization": f"Bearer {bearerToken}"
    }

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json()

        return data, response.status_code

    except requests.exceptions.RequestException as e:
        return f'Request failed with error: {e}', None
    except (KeyError, ValueError) as e:
        return f'Error parsing JSON: {e}', None
    
def get_route_fetch(route_id: str, bearerToken: str):
    URL = f'https://api.iq.inrix.com/route?routeId={route_id}&format=json'
    headers = {
    "Authorization": f"Bearer {bearerToken}"
    }

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json()

        return data, response.status_code

    except requests.exceptions.RequestException as e:
        return f'Request failed with error: {e}', None
    except (KeyError, ValueError) as e:
        return f'Error parsing JSON: {e}', None