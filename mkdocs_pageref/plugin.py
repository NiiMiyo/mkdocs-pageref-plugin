from mkdocs.plugins import BasePlugin
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs_pageref.find_matches import get_links, get_match_replacement, is_in_range_array
from mkdocs_pageref.pageref_config import PageRefConfig

from os.path import join
import re

class PageRefPlugin(BasePlugin[PageRefConfig]):
	def on_page_markdown(self, markdown: str, *,
			page: Page, config: MkDocsConfig, **_) -> str | None:

		links = [(l.start(), l.end()) for l in get_links(markdown)]

		for config_match in self.config.matches:
			destination_dir = join(config.docs_dir, config_match.page)

			while True:
				match = re.search(config_match.regex, markdown)

				if match is None: break
				if is_in_range_array(match, links): break

				text = markdown[match.start(): match.end()]
				replace_with = get_match_replacement(text, page.file.src_uri, destination_dir)

				markdown = markdown[:match.start()] + replace_with + markdown[match.end():]
				links.append((match.start(), match.end()))

		return markdown
