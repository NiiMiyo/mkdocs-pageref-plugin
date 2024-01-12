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

class PageReference(NamedTuple):
	pattern: Pattern[str]
	destination: str
