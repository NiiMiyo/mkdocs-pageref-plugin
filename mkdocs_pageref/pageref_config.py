from mkdocs.config.base import Config
from mkdocs.config import config_options

from typing import NamedTuple

class _PluginMatch(Config):
	patterns = config_options.ListOfItems(config_options.Type(str), default=[])
	page =    config_options.Type(str)

class PageRefConfig(Config):
	matches = config_options.ListOfItems(
		config_options.SubConfig(_PluginMatch), default=[]
	)

class PageReference(NamedTuple):
	pattern: str
	destination: str
	element_id: str | None = None

	def __str__(self) -> str:
		return f"\"{self.pattern}\" -> {self.destination + (self.element_id or "")}"

	def __repr__(self) -> str:
		return f"PageReference({self.pattern}, {self.destination}, {self.element_id})"
