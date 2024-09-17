import json

def prettify_json(data):
    if isinstance(data, (dict, list)):
        # Convert dict or list to JSON string
        data = json.dumps(data)
    elif not isinstance(data, (str, bytes, bytearray)):
        raise TypeError("The input data must be a JSON serializable type")

    obj = json.loads(data)
    json_formatted_str = json.dumps(obj, indent=4)

    return json_formatted_str