from requests import get

def getCat(mime='png'):
    if mime == 'png':
        response = get('https://api.thecatapi.com/v1/images/search?mime_types=png', headers={"x-api-key": "cc0eb636-fcc2-4522-ad8a-f2319898a5c3"})
        data = response.json()
    elif mime == 'jpg':
        response = get('https://api.thecatapi.com/v1/images/search?mime_types=jpg', headers={"x-api-key": "cc0eb636-fcc2-4522-ad8a-f2319898a5c3"})
        data = response.json()
    elif mime == 'gif':
        response = get('https://api.thecatapi.com/v1/images/search?mime_types=gif', headers={"x-api-key": "cc0eb636-fcc2-4522-ad8a-f2319898a5c3"})
        data = response.json()
    else:
        raise ValueError('Mime is png, jpg, or gif, not another!')
    return data[0]['url']
