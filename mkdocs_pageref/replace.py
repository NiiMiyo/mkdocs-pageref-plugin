import re
from typing import Any
from bs4 import BeautifulSoup
from mkdocs.structure.pages import Page
from os.path import relpath
from .pageref_config import PageRefConfig, PageReference

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

def page_url(page: Page) -> str:
	return "/" + page.url

def get_match_replacement(text: str, origin: Page, destination: PageReference, reference_class: str) -> str:
	if destination.destination.startswith("/"):
		href = relpath(destination.destination, page_url(origin)) + (destination.element_id or "")
	else:
		href = destination.destination

	tag = BeautifulSoup().new_tag( # type: ignore
		"a", None, None, {
			"href": href,
			"class": reference_class,
		}
	)
	tag.string = text
	return str(tag)

def replace_matches(html: str, origin: Page, references: list[PageReference], config: PageRefConfig) -> str:
	soup = BeautifulSoup(html, "html.parser")
	main = soup.select_one(config.main_selector)

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

			replacement = get_match_replacement(match.group(0), origin, ref, config.reference_class)
			main_str = main_str[:match_range[0]] + replacement + main_str[match_range[1]:]

			all_matches = ref.pattern.finditer(main_str)
			links = get_links(main_str)

	main.replace_with(BeautifulSoup(main_str, "html.parser"))
	return str(soup)
