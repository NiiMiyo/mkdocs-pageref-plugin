from re import Pattern
from mkdocs.config.base import Config
from mkdocs.config import config_options

from typing import NamedTuple

class _PluginMatch(Config):
	pattern = config_options.Type(str)
	page =    config_options.Type(str)

class PageRefConfig(Config):
	matches = config_options.ListOfItems(
		config_options.SubConfig(_PluginMatch), default=[]
	)
	reference_class = config_options.Type(str, default="pageref-reference")
	main_selector = config_options.Type(str, default='[role="main"]')

class PageReference(NamedTuple):
	pattern: Pattern[str]
	destination: str
	element_id: str | None = None

	def __str__(self) -> str:
		return f"/{self.pattern}/ -> {self.destination + (self.element_id or "")}"

	def __repr__(self) -> str:
		return f"PageReference({self.pattern}, {self.destination}, {self.element_id})"
