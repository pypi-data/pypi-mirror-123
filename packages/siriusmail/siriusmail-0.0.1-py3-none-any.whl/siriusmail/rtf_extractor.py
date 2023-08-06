import logging
import re
from typing import List, Optional


logger = logging.getLogger(__name__)


def remove_rtf(text: str, extra_tags: List[Optional[str]]=[]) -> str:
    """Simple regex to remove rtf tags, plan to create a proper parser according
    to rtf specs, stay tune for that

    Args:
        text: string with rtf tags
    
    Returns:
        str: string without rtf tags

    """
    rtf_tags = [
        r"(\\+html[A-z0-9]+)",
        r"(\\+pard)",
        r"(\\+par)",
        r"(\\+plain)",
        r"(\\+sb[0-9]+)",
        r"(\\+intbl)",
        r"(\\+trowd)",
        r"(\\+cbpat[0-9]+)",
        r"(\\+irow[A-z0-9]+)",
        r"(\\+clpad[A-z0-9]+)",
        r"(\\+lang[A-z0-9]+)",
        r"(\\+f[A-z0-9]+)",
        r"(\\+q[A-z0-9]+)",
        r"(\\+)",
        r"(\r\n)",
        r"(\{\*)",
        r"(\{)",
        r"(\})",
    ]

    if len(extra_tags) != 0:
        for tag in extra_tags:
            rtf_tags.insert(0, tag)

    for rtf_tag in rtf_tags:
        text = re.sub(rtf_tag, "", text)

    return text
