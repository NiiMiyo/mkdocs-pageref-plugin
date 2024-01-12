import re
from mkdocs.plugins import BasePlugin
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from .replace import replace_matches
from .pageref_config import PageRefConfig, PageReference

def get_pageref_pattern(page: Page) -> str | None:
	return page.meta.get("pageref-pattern", None)

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
		if pattern is not None and page_path is not None:
			self.references.append( PageReference(re.compile(pattern), page_path) )

	def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> str | None:
		return replace_matches(output, [ref for ref in self.references if ref.destination != page.abs_url])
