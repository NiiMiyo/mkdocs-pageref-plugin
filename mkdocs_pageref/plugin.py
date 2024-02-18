import frontmatter # type: ignore - No stub file
import logging
from mkdocs.plugins import BasePlugin
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from .replace import replace_matches, page_url
from .pageref_config import PageRefConfig, PageReference
from .constants import PAGEREF_PATTERNS_META_KEY, PAGEREF_SUBPATTERNS_META_KEY

logger = logging.getLogger(f"mkdocs.plugin.{__name__}")

def get_pageref_patterns(meta: dict[str, object]) -> list[str]:
	value = meta.get(PAGEREF_PATTERNS_META_KEY, None)
	if isinstance(value, str):
		return [value]
	elif isinstance(value, list):
		return [ str(p) for p in value ] # type: ignore - p is Unknown
	return list()

def get_pageref_subpatterns(meta: dict[str, object]) -> dict[str, list[str]]:
	subpatterns = meta.get(PAGEREF_SUBPATTERNS_META_KEY, None)
	if not isinstance(subpatterns, dict):
		return {}

	result: dict[str, list[str]] = dict()
	for element, patterns in subpatterns.items(): # type: ignore - element and patterns is Unknown
		if not isinstance(element, str):
			continue
		elif isinstance(patterns, str):
			result[element] = [patterns]
		elif isinstance(patterns, list):
			result[element] = [str(p) for p in patterns] # type: ignore - p is Unknown

	return result

class PageRefPlugin(BasePlugin[PageRefConfig]):
	references: list[PageReference]

	def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
		logger.debug("Adding global references")
		self.references = list()

		for m in self.config.matches:
			self.references.extend([
				PageReference(mention, m.page)
				for mention in m.patterns
			])

	def on_files(self, files: Files, *, config: MkDocsConfig) -> Files | None:
		for mkdocs_file in files:
			if not mkdocs_file.is_documentation_page():
				continue

			url = page_url(mkdocs_file)
			src_url = config.docs_dir + "/" + url

			with open(src_url, mode='r', encoding='utf8') as file:
				meta = frontmatter.load(file).metadata

				self.references.extend([
					PageReference(m, url)
					for m in get_pageref_patterns(meta)
				])

				for element, subpatterns in get_pageref_subpatterns(meta).items():
					if not element.startswith("#"):
						element = "#" + element

					self.references.extend([
						PageReference(sub, url, element)
						for sub in subpatterns
					])

	def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, **_) -> str | None:
		logger.debug(f"Applying references to {page.file.src_uri}")

		references = [
			ref
			for ref in self.references
			if ref.destination != page_url(page)
		]

		return replace_matches(markdown, page, references)
