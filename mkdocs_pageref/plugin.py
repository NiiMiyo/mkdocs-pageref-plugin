import re
from mkdocs.plugins import BasePlugin
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from .replace import replace_matches
from .pageref_config import PageRefConfig, PageReference

def get_pageref_pattern(page: Page) -> str | None:
	value = page.meta.get("pageref-pattern", None)
	if value is None:
		return None
	return str(value)

def get_pageref_subpatterns(page: Page) -> dict[str, str]:
	subpatterns = page.meta.get("pageref-subpatterns", None)
	if not isinstance(subpatterns, dict):
		return {}

	return {
		str(k): str(v)                  # type: ignore
		for k, v in subpatterns.items() # type: ignore
	}

class PageRefPlugin(BasePlugin[PageRefConfig]):
	references: list[PageReference]

	def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
		self.references = []

	def on_files(self, files: Files, *, config: MkDocsConfig) -> Files | None:
		self.references.extend([
			PageReference(re.compile(m.pattern), m.page)
			for m in self.config.matches
		])

	def on_page_markdown(self, markdown: str, *, page: Page, **_) -> str | None:
		pattern = get_pageref_pattern(page)
		page_path = page.abs_url

		if page_path is None:
			return

		if pattern is not None:
			self.references.append( PageReference(re.compile(pattern), page_path) )

		subpatterns = get_pageref_subpatterns(page)
		for element_id, pattern in subpatterns.items():
			if len(pattern) == 0 or len(element_id) == 0:
				continue

			if not element_id.startswith("#"):
				element_id = "#" + element_id

			self.references.append(PageReference(re.compile(pattern), page_path, element_id))

	def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> str | None:
		references = [ref for ref in self.references if ref.destination != page.abs_url]
		return replace_matches(output, references, self.config.reference_class)
