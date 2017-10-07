
def params_from_request(request):
    """Change the format of the HTTP request parameters so that they may be more easily used."""
    params_dict = {}
    for key, value in request.arguments.items():
        if len(value) == 1:
            params_dict[key] = value[0].decode('UTF-8')
        else:
            params_dict[key] = []
            for part in value:
                params_dict[key].append(part.decode('UTF-8'))
    return params_dict
