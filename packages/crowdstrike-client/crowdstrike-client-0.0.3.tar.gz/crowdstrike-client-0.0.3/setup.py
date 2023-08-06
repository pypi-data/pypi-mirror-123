import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crowdstrike-client",
    version="0.0.3",
    author="Pyperanger",
    description="A Non-oficial crowdstrike client api",
    url="https://github.com/pyperanger/crowdstrike-client",
    project_urls={
        "Bug Tracker": "https://github.com/pyperanger/crowdstrike-client/issues",
    },
    package_dir={"": "crowdstrikeclient"},
    packages=setuptools.find_packages(where="crowdstrikeclient"),
    python_requires=">=3.6",
)