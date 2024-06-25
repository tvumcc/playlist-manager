import requests
import os

"""Gets a new access token using the client credentials found in client_info.txt to call Spotify's API"""
def acquire_new_access_token() -> str:
    # Get client's credentials
    client_id = ""
    client_secret = ""
    try:
        with open("client_info.txt", "r") as client_info_file:
            (client_id, client_secret) = tuple(client_info_file.readlines())
    except:
        return None
    
    # POST for a new access token
    access_token_url = "https://accounts.spotify.com/api/token"
    access_token_header = {"Content-Type" : "application/x-www-form-urlencoded"}
    access_token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id.strip(),
        "client_secret": client_secret.strip(),
    }
    access_token_response = requests.post(access_token_url, headers=access_token_header, data=access_token_data)

    # Ensure that the token provided is valid
    if access_token_response.ok:
        with open("token.txt", "w") as access_token_file:
            access_token_file.write(access_token_response.json()["access_token"])
        return access_token_response.json()["access_token"]
    else:
        return None

"""Uses the user's client ID and secret to construct a new client_info.txt. Returns true if the credentials are valid and false otherwise."""
def load_client_credentials(client_id: str, client_secret) -> bool:
    with open("client_info.txt", "w") as client_info_file:
        client_info_file.write(client_id + "\n" + client_secret)

    token = acquire_new_access_token()
    return token is not None

"""Gets the user's access token either from the token.txt cache or by calling Spotify's API if the cached token is expired"""
def get_access_token() -> str:
    token = None
    if os.path.isfile("token.txt"):
        with open("token.txt", "r") as access_token_file:
            token = access_token_file.read()
    if not validate_token(token): token = acquire_new_access_token()

    return token 

"""Returns true if the given access token is valid and false otherwise"""
def validate_token(token: str) -> bool:
    validation_url = "https://api.spotify.com/v1/tracks/2JIdZFF6ActYiGG7o7W3AA"
    validation_response = requests.get(validation_url, headers={"Authorization" : f"Bearer {token}"})
    return validation_response.ok