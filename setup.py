from setuptools import setup

setup(
    name="blacklist_pre_commit_hook",
    version="0.0.0",
    packages=["blacklist"],
    entry_points={"console_scripts": ["blacklist=blacklist:main"]},
)
