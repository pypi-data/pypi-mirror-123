import itertools
import math
import multiprocessing
from pathlib import Path
from typing import Any, Dict


def _ucp_to_utf16_charmap(s: str):
    """
    mostly copied from
    https://stackoverflow.com/questions/56280011/keeping-java-string-offsets-with-unicode-consistent-in-python
    converts from python indices (unicode code points) to indices
    """
    encoding = "UTF-16LE"
    chrLengths = [len(bytearray(ch, encoding)) // 2 for ch in s]
    utf16indices = [0] + list(itertools.accumulate(chrLengths))
    return utf16indices


def convert_issue_spans_to_utf16(s: str, issue: Dict[str, Any]) -> Dict[str, Any]:
    # modifies in place but also returns
    charmap = _ucp_to_utf16_charmap(s)
    f = charmap[issue["from"]]
    u = charmap[issue["until"]]
    # store these if needed for python string manipulation
    issue["_from_p"] = issue["from"]
    issue["_until_p"] = issue["until"]
    # but set the public values to utf-16
    issue["from"] = f
    issue["until"] = u
    return issue


def get_cpu_quota_within_docker():
    """
    By default, we use mp.cpu_count()
    HOWEVER, if there are cpu limits in certain paths, we assume those are
    from k8s/docker and override with those values
    """
    cpu_cores = multiprocessing.cpu_count()

    cpu_shares = Path("/sys/fs/cgroup/cpu/cpu.shares")

    if cpu_shares.exists():
        with cpu_shares.open("rb") as r:
            request_cpu_shares = int(r.read().strip())
            cpu_cores = (
                math.ceil(request_cpu_shares / 1024)
                if request_cpu_shares > 0
                else multiprocessing.cpu_count()
            )
            print(
                f"CPU request limit: {round(request_cpu_shares / 1024, 2)}, will spin {cpu_cores} worker(s)."
            )
    else:
        print(f"CPU_shares not found, will spin {cpu_cores} worker(s).")
    return cpu_cores
