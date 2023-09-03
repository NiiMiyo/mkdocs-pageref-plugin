from mkdocs.plugins import BasePlugin
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs_pageref.helper import replace_matches
from mkdocs_pageref.pageref_config import PageRefConfig

from os import path

class PageRefPlugin(BasePlugin[PageRefConfig]):
	def on_page_markdown(self, markdown: str, *,
			page: Page, config: MkDocsConfig, **_) -> str | None:

		for c in self.config.matches:
			origin = path.join(config.docs_dir ,page.file.src_uri)
			destination = c.page

			markdown = replace_matches(markdown, c.pattern, origin, destination)

		return markdown
