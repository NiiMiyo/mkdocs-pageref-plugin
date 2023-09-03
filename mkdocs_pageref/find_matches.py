import re

from os.path import relpath, join
from typing import Iterable

LINK_PATTERN = r"!?\[[^\]\n]*\]\([^\)\n]*\)"

def get_links(markdown: str):
	return re.finditer(LINK_PATTERN, markdown)

def get_match_replacement(text: str, from_file: str, to_file: str) -> str:
	origin_dir = join(from_file, '..')
	destination = relpath(to_file, origin_dir).replace("\\", "/")

	return f"[{text}]({destination})"

def is_in_range(match: re.Match[str], check: tuple[int, int]) -> bool:
	return (match.start() >= check[0]) and (match.end() <= check[1])

def is_in_range_array(
		match: re.Match[str],
		checks: Iterable[tuple[int, int]]) -> bool:

	return any((is_in_range(match, c) for c in checks))
