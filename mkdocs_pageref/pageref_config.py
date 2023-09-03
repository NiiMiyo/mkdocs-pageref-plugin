from mkdocs.config.base import Config
from mkdocs.config import config_options

class _PluginMatch(Config):
	pattern = config_options.Type(str)
	page =    config_options.File()

class PageRefConfig(Config):
	matches = config_options.ListOfItems(
		config_options.SubConfig(_PluginMatch), default=[]
	)
