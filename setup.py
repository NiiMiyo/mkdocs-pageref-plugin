from setuptools import find_packages, setup

setup(
	name="mkdocs-pageref-plugin",
	version="0.1",
	install_requires = [
		'mkdocs>=1.5.2'
	],
	packages=find_packages(),

	entry_points = {
		'mkdocs.plugins': [
			'pageref = mkdocs_pageref.plugin:PageRefPlugin',
		]
	}
)
