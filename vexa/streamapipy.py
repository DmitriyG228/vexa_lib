import httpx


async def get_connections(service_token,streamapi_port):

    url = f"http://host.docker.internal:{streamapi_port}/list_connections"
    params = {
            "service_token": service_token
        }
    headers = {
        "Content-Type": "application/json"
    }


    async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=2)
    
    return response.json()['connections']


async def flush_stream_cache(service_token,streamapi_port):

    url = f"http://host.docker.internal:{streamapi_port}/flush_cache"
    params = {
            "service_token": service_token
        }
    headers = {
        "Content-Type": "application/json"
    }


    async with httpx.AsyncClient() as client:
            response = await client.post(url, params=params, headers=headers, timeout=2)
    
    return response.json()


async def fetch_chunks(connection_id: str, num_chunks: int,service_token,streamapi_port):
    # Define the URL to your API endpoint
    url = f"http://host.docker.internal:{streamapi_port}/get_next_chunks/{connection_id}"
    
    # Define the parameters
    params = {
        "service_token": service_token,
        "num_chunks": num_chunks
    }

    # Use an asynchronous client from httpx
    async with httpx.AsyncClient() as client:
        try:
            # Perform the GET request
            response = await client.get(url, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                if response.json() == {'message': 'No more chunks available for this connection'}:
                    print(response.json())
                    return
                else:
                    return response.json()  # Return the JSON response from the API
            else:
                return {"error": "Failed to fetch chunks", "status_code": response.status_code, "details": response.text}
        except httpx.RequestError as e:
            return {"error": "An error occurred while requesting chunks", "exception": str(e)}

