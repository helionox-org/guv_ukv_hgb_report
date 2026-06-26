from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in guv_ukv_hgb_report/__init__.py
from guv_ukv_hgb_report import __version__ as version

setup(
	name="guv_ukv_hgb_report",
	version=version,
	description="HGB Paragraph 275 Cost of Sales Method Profit and Loss Report",
	author="Helionox GmbH",
	author_email="contact@helionox.eu",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
