from setuptools import setup, find_packages

setup(
    name="ais-dom-frontend",
    version="20211007.1",
    description="AIS dom frontend",
    url="https://ai-speaker.com",
    author="The Authors of the AI-Speaker.com project",
    author_email="info@ai-speaker.com",
    license="Apache License 2.0",
    packages=find_packages(include=["hass_frontend", "hass_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)
