from typing import Any, Dict, List, Union


def make_issue(
    segment: str,
    start: int,
    end: int,
    issue_type: str,
    description: str,
    simpleDescription: str,
    suggestions: List[str] = [],
    subCategory: str = "",
    learnMore: str = "",
    paragraph: bool = False,
    header: str = "",
    metaDict: Dict[str, Any] = {},
    accept_all_changes: bool = False,
    score: Union[float, int] = 0,
    debug: bool = False,
    visible: bool = True,
) -> Dict[str, Any]:
    """
    Turn a bunch of parameters into Writer's dictionary issue format
    old reference:
    https://qordoba.atlassian.net/wiki/spaces/HOME/pages/840368141/Content-AI

    update as of ~May 2021: we are now using v2 issues only,
    and should default to utf16 string indexing, but allow python-unicode
    string-indexing just for debugging

    WARNING this now takes `segment` as the first parameter.
    YOU HAVE TO PASS THE WHOLE SEGMENT to get the utf16 indexes right
    if you do not want to convert to utf16 indices (for debugging):
        - you still need to pass the whole segment, sorry
        - pass make_issue(..., unicode_convert=None)
    """
    issue = {
        "issueType": issue_type,
        "from": start,
        "until": end,
        "score": score,
        "suggestions": suggestions,
        "description": description,
        "simpleDescription": simpleDescription,
        "meta": {"paragraph": paragraph},
        "visible": visible,
    }
    # for Doris/analytics, who can see the meta but not the visible field
    issue["meta"]["visible"] = visible

    if subCategory:
        issue["meta"]["subCategory"] = subCategory
    if learnMore:
        issue["meta"]["learnMore"] = learnMore
    if header:
        issue["meta"]["header"] = header
    if accept_all_changes:
        issue["meta"]["acceptAllChanges"] = accept_all_changes

    if debug:
        # log warnings if meta_dict overwrites issue["meta"]
        common = [value for value in metaDict.keys() if value in issue["meta"]]
        for c in common:
            if metaDict[c] != issue["meta"][c]:
                print(
                    f"Meta_dict {c}:{metaDict[c]} is overwriting issue meta {c}:{issue['meta'][c]}"
                )
        # also generate new_segment
        suggestion = suggestions[0] if len(suggestions) else ""
        issue["new_segment"] = segment[:start] + suggestion + segment[end:]
    # this has to come after the if debug warning
    issue["meta"].update(metaDict)
    return issue
