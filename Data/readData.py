# %%
import os
coinSpotApiKey = os.environ['coinSpotReadAPIKey']
coinSpotSecretKey = os.environ['coinspotSecretKey']

import requests
import hmac
import hashlib
import time

# Your API key and secret

api_key = coinSpotApiKey
secret_key = coinSpotSecretKey

# API endpoint
url = 'https://www.coinspot.com.au/api/v2/ro/my/balances'

def myBalance():

    # Create a nonce (must be unique and incrementing)
    nonce = int(time.time() * 1000)

    # Prepare the data payload
    data = f'{{"nonce":"{nonce}"}}'

    # Convert the data to JSON and encode as bytes
    post_data = data.encode('utf-8')

    # Create the HMAC signature
    signature = hmac.new(
        secret_key.encode('utf-8'),
        post_data,
        hashlib.sha512
    ).hexdigest()

    # Set up headers
    headers = {
        'key': api_key,
        'sign': signature,
        'Content-Type': 'application/json',
    }

    # Make the POST request

    response = requests.post(url, headers=headers, data=f'{{"nonce":"{nonce}"}}')

    return(response)
