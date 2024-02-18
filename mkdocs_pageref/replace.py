import re
import logging
from typing import Any
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File
from os.path import relpath
from .pageref_config import PageReference

logger = logging.getLogger(f"mkdocs.plugin.{__name__}")

StringRange = tuple[int, int]

LINK_PATTERN = re.compile(r"!?\[[^\]\n]*\]\([^\)\n]*\)")

def match_to_range(match: re.Match[Any]) -> StringRange:
	return match.start(), match.end()

def is_range_between(outer: StringRange, inner: StringRange) -> bool:
	return outer[0] <= inner[0] and outer[1] >= inner[1]

def get_skip_patterns(html: str) -> list[StringRange]:
	return [
		match_to_range(m)
		for m in LINK_PATTERN.finditer(html)
	]

def page_url(page: Page | File) -> str:
	if isinstance(page, File):
		return "/" + page.src_uri
	else:
		return page_url(page.file)

def find_all_in_string(outer: str, inner: str):
	start = 0
	inner_len = len(inner)

	while True:
		start = outer.find(inner, start)
		if start == -1: return None

		end = start + inner_len
		yield outer[start:end], (start, end)

		start += inner_len

def get_match_replacement(text: str, origin: Page, reference: PageReference) -> str:
	if reference.destination.startswith(("/", "./", "../", ".\\", "..\\")):
		href = relpath(reference.destination, page_url(origin) + "/..")
		href = href.replace('\\', '/')
		if reference.element_id is not None:
			href += reference.element_id
	else:
		href = reference.destination

	return f"[{text}]({href})"

def replace_matches(markdown: str, origin: Page, references: list[PageReference]) -> str:
	skip_matches = get_skip_patterns(markdown)

	for ref in references:
		all_matches = find_all_in_string(markdown, ref.pattern)

		while True:
			match = next(all_matches, None)
			if match is None: break

			match_text, match_range = match

			should_skip_match = any( is_range_between(m, match_range) for m in skip_matches )
			if should_skip_match: continue

			replacement = get_match_replacement(match_text, origin, ref)
			markdown = markdown[:match_range[0]] + replacement + markdown[match_range[1]:]

			all_matches = find_all_in_string(markdown, ref.pattern)
			skip_matches = get_skip_patterns(markdown)

	return markdown
