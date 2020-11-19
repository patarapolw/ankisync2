import json
import urllib.request


def _ankiconnect_request(action, **params):
    return {"action": action, "params": params, "version": 6}


def ankiconnect(action: str, **params):
    """Invoke Ankiconnect's API

    Anki needs to be opened, and has Ankiconnect plugin installed.

    https://foosoft.net/projects/anki-connect/
    """

    requestJson = json.dumps(_ankiconnect_request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", requestJson)
        )
    )
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])

    return response["result"]
