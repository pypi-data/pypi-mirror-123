import json as __mod_json
import os
import pprint

import requests


__metas = {
    "gec": {},
    "hate-speech": {},
    "gender-nouns": {},
    "gender-pronouns": {},
    "infinitive": {},
    "healthy-communication": {},
    "confidence": {},
    "parallelism": {},
    "paragraph": {
        "sentenceComplexity": 8,
        "vocabulary": 8,
        "paragraphLength": "medium",
    },
    "punctuation": {"punctuation": True, "oxfordComma": "use", "emDashSpaces": "use",},
    "casing": {"useSentenceCase": "use"},
    "acronym": {"commonAcronymCheck": True},
    "sensitivity": {
        "age": True,
        "disability": True,
        "genderIdentity": True,
        "raceEthnicityNationality": True,
        "sexualOrientation": True,
        "substanceUse": True,
    },
    # inclusivity/sensitivity are the same
    "inclusivity": {
        "age": True,
        "disability": True,
        "genderIdentity": True,
        "raceEthnicityNationality": True,
        "sexualOrientation": True,
        "substanceUse": True,
    },
    "sentence-complexity": {
        "debug": True,
        "sentenceComplexity": 8,
        "vocabulary": 8,
        "paragraphLength": "medium",
    },
    "readability": {
        "grade": 4,
        "index": "flesch-kincaid-grade-level",
        "ignore": ["financial"],
    },
    "plain-language": {
        "passiveVoice": True,
        "wordiness": True,
        "unclearReferences": True,
    },
    "vocabulary": {
        "debug": True,
        "sentenceComplexity": 8,
        "vocabulary": 8,
        "paragraphLength": "medium",
    },
}


def __build_qai_payload(
    segment: str, meta: dict = {}, category: str = "TEST-CATEGORY"
) -> dict:
    qai_payload = {
        "request": {
            "organizationId": 1,
            "workspaceId": 1,
            "personaId": 94,
            "documentId": "61845063-809a-4398-b741-b841c77c6676",
            "version": 1,
            "userId": 1,
            "clientId": 1,
            "segments": [
                {
                    "category": category,
                    "content": {
                        "segmentId": "95ea2705-6a0d-48c0-9eeb-78dcf69cef79",
                        "tpe": "document",
                        "segment": "segment",
                        "from": 10,
                    },
                    "meta": meta,
                }
            ],
        }
    }
    qai_payload["request"]["segments"][0]["content"]["segment"] = segment
    qai_payload["request"]["segments"][0]["meta"] = meta
    return qai_payload


def test_qai(segment: str, meta: dict = {}, url: str = "http://localhost:5000"):
    """for testing a qai service by URL
    if it is an established service, you can use like
    test_qai("segment to test", "gec", 8080)
    where `"gec"` tells it what meta to use
    and 8080 means localhost port 8080

    if this is a new service, or you want to specify the meta, then use

    test_qai("segment to test", {"something": 10}, 5000)

    for testing via k8s proxy, use name_test_qai
    """
    if isinstance(meta, str):
        meta = __metas.get(meta, {})
    qai_payload = __build_qai_payload(segment, meta)
    if isinstance(url, int):
        url = f"http://localhost:{url}"
    response = requests.post(url, json=qai_payload)
    try:
        return response.json()
    except Exception as e:
        print("something went wrong with the request...")
        print(e)
        print(response)
        print(response.text)


def name_test_qai(segment: str, name: str, meta: dict = None):
    """
    For testing qai services via the k8s proxy (kubectl proxy)

    usage:
    name_test_qai("testing string", "gec")

    appropriate meta will be injected based on service name,
    you can override this by using the meta kwarg
    """
    if meta is None:
        meta = __metas.get(name, {})
    url = f"http://127.0.0.1:8001/api/v1/namespaces/default/services/{name}:80/proxy/v2"
    return test_qai(segment, meta, url)


def test_grammar_script(rules: str, json: bool = False, show: bool = False):
    """call grammar-script in k8s, get json from yaml-like or file
    params:
        - rules: a string of yaml-like grammarScript rules, or path to such a file
        - json: whether to return JSON format (alternative is python dict)
        - show: whether to print or return (True means print, don't return)
    """
    if "rule:" not in rules:
        if os.path.isfile(rules):
            with open(rules) as f:
                rules = "".join([l for l in f])
        else:
            raise ValueError(
                "argument must be grammar-script rules string or path to such a file"
            )
    url = "http://127.0.0.1:8001/api/v1/namespaces/default/services/grammar-script:80/proxy/"
    response = requests.post(url, json={"rules": rules})
    payload = response.json()
    # does anyone need tests?
    md, tests = payload.get("dict", {}), payload.get("tests", {})
    if json:
        if show:
            print(__mod_json.dumps(md, indent=2))
            return
        else:
            return __mod_json.dumps(md)
    if show:
        pprint.pprint(md)
        return
    else:
        return md
