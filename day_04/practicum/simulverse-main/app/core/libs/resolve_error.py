
def resolve_error(error:str):
    if error == '401':
        return 'HTTP 401 UNAUTHORIZED'
    if error == 'c01':
        return "Contents missing"

    return "I Don't Know"