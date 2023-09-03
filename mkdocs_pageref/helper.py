import re
from typing import Any
from os import path

LINK_PATTERN = r"!?\[[^\]\n]*\]\([^\)\n]*\)"

def range_between(outer: tuple[int, int], inner: tuple[int, int]) -> bool:
	return outer[0] <= inner[0] and outer[1] >= inner[1]

def match_range(m: re.Match[Any]) -> tuple[int, int]:
	return m.start(), m.end()

def get_links(markdown: str) -> list[tuple[int, int]]:
	return [
		match_range(l)
		for l in re.finditer(LINK_PATTERN, markdown)
	]

def get_page_relative_url(origin: str, destination: str) -> str:
	origin_dir = path.join(origin, '..')
	return path.relpath(destination, origin_dir).replace("\\", "/")

def get_match_replacement(text: str, origin: str, destination: str) -> str:
	destination_url = get_page_relative_url(origin, destination)
	return f"[{text}]({destination_url})"

def replace_matches(markdown: str, pattern: str, origin: str, destination: str) -> str:
	all_matches = re.finditer(pattern, markdown)
	links = get_links(markdown)

	while True:
		match = next(all_matches, None)
		if match is None:
			break


		match_r = match_range(match)
		is_inside_link = any((range_between(l, match_r) for l in links))
		if is_inside_link:
			continue

		replace_with = get_match_replacement(match.group(0), origin, destination)

		markdown = markdown[:match_r[0]] + replace_with + markdown[match_r[1]:]
		all_matches = re.finditer(pattern, markdown)
		links = get_links(markdown)

	return markdown
