import requests

def validate (username, password, dbpassword):
    r = requests.get('https://api.github.com/users', auth=(username, password))
    is_valid = r.status_code == 200
    return is_valid