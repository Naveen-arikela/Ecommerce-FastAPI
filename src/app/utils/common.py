

def wrap_response(code, msg, data=""):
    response = {
        "status_code": code,
        "detail": msg
    }
    if data:
        response["data"] = data
    
    return response