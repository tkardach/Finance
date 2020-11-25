

def authenticate(
    client, email, password, endpoint=None, **kwargs
):
    data = dict(email=email, password=password, remember="y")
    return client.post(endpoint or "/login", data=data, **kwargs)