import re
from typing import Any
from bs4 import BeautifulSoup

from .pageref_config import PageReference

StringRange = tuple[int, int]

LINK_PATTERN = re.compile(r"<a( [^>]*)?>[^<]*</a>")

def match_to_range(match: re.Match[Any]) -> StringRange:
	return match.start(), match.end()

def is_range_between(outer: StringRange, inner: StringRange) -> bool:
	return outer[0] <= inner[0] and outer[1] >= inner[1]

def get_links(html: str) -> list[StringRange]:
	return [
		match_to_range(m)
		for m in LINK_PATTERN.finditer(html)
	]

def get_match_replacement(text: str, destination: str) -> str:
	return f"<a href={destination}>{text}</a>"

def replace_matches(html: str, references: list[PageReference]) -> str:
	soup = BeautifulSoup(html, "html.parser")
	main = soup.find(None, {"role": "main"})

	if main is None:
		return html

	main_str = str(main)

	links = get_links(main_str)
	for ref in references:
		all_matches = ref.pattern.finditer(main_str)

		while True:
			match = next(all_matches, None)
			if match is None: break

			match_range = match_to_range(match)

			is_inside_link = any( is_range_between(l, match_range) for l in links )
			if is_inside_link: continue

			replacement = get_match_replacement(match.group(0), ref.destination)
			main_str = main_str[:match_range[0]] + replacement + main_str[match_range[1]:]

			all_matches = ref.pattern.finditer(main_str)
			links = get_links(main_str)

	main.replace_with(BeautifulSoup(main_str, "html.parser"))
	return str(soup)
