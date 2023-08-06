import re
from typing import Any, Dict, List


def filter_no_ops(segment: str, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    filter issues to drop 0-distance edits
    :param issues: issues to filter
    :return: filter issues
    """
    filtered_issues = []
    for issue in issues:
        if issue["suggestions"]:
            suggestions = []
            for suggestion in issue["suggestions"]:
                # different keys because of utf-16 indexing
                # which means from and until indexes aren't usable in python
                f = issue.get("_from_p", None)
                if not f:
                    f = issue.get("from")
                u = issue.get("_until_p", None)
                if not u:
                    u = issue.get("until")
                if (segment[f:u]) == suggestion:
                    continue
                suggestions.append(suggestion)

            if suggestions:
                issue["suggestions"] = suggestions
                filtered_issues.append(issue)
        else:  # some services don't offer suggestions, so no need to check
            filtered_issues.append(issue)
    return filtered_issues


def fix_extra_space(segment: str, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    modify issues in which a deletion would cause a double space
    :param segment: the segment with issues
    :param issues: issues to potentially modify
    :return: modified issues
    """
    modified_issues = []
    for issue in issues:
        # we only care about pure deletes
        # which for us means one suggestion that is the empty string
        # possibly want to cover impure deletes, but gets much harder
        if len(issue["suggestions"]) == 1 and issue["suggestions"][0] == "":
            # different keys because of utf-16 indexing
            # which means from and until indexes aren't usable in python
            f = issue.get("_from_p", None)
            if not f:
                f = issue.get("from")
            u = issue.get("_until_p", None)
            if not u:
                u = issue.get("until")
            # check if either side has spaces
            causes_double_space = (
                f > 0
                and segment[f - 1] == " "
                and len(segment) > u
                and segment[u] == " "
            )
            if causes_double_space:
                # we have a double space issue
                # so extend forward (which is always possible)
                issue["until"] += 1
                if issue.get("_until_p", None) is not None:
                    issue["_until_p"] += 1
            # check if issue is preceded by space and succeeded by SEP
            causes_space_sep = (
                f > 0
                and segment[f - 1] == " "
                and len(segment) == u + 1
                and segment[u] in [".", "?", "!", ",", ";", ":"]
            )
            if causes_space_sep:
                # extend back one char (always possible) to catch extra space
                issue["from"] -= 1
                if issue.get("_from_p", None) is not None:
                    issue["_from_p"] -= 1

        # don't touch most issues
        modified_issues.append(issue)
    return modified_issues


class Validator:
    html_pattern = re.compile("<.*?>")
    non_letter_pattern = re.compile("[^a-zA-Z'\-\s]")

    def __init__(self, ignore_html=True, ignore_token_fraction=0.5):
        self.ignore_html = ignore_html
        self.acceptable_fraction_of_ignorable_tokens = ignore_token_fraction

    def _has_html(self, segment: str) -> bool:
        return self.html_pattern.match(segment) != None

    def _has_non_letter(self, segment: str):
        return self.non_letter_pattern.match(segment) != None

    def _is_empty(self, segment: str):
        return len(segment.strip()) == 0

    def _is_unacceptable(self, segment: str):
        if self._is_empty(segment):
            print("segment is empty")
            return True
        if self.ignore_html and self._has_html(segment):
            print("segment has HTML")
            return True
        return False

    def _is_ignored_tokens(self, token: str) -> bool:
        return self._has_non_letter(token)

    def _has_too_many_ignore_tokens(self, segment: str) -> bool:
        tokens = segment.strip().split(" ")
        token_length = len(tokens)
        ignored_tokens = [t for t in tokens if self._is_ignored_tokens(t)]
        ignored_length = len(ignored_tokens)
        if token_length == 0:
            return False
        else:
            return (
                ignored_length / token_length
                > self.acceptable_fraction_of_ignorable_tokens
            )

    def __call__(self, segment: str):
        if self._is_unacceptable(segment):
            return False
        if self._has_too_many_ignore_tokens(segment):
            print(f"too many non-letter tokens in {segment}")
            return False
        return True
