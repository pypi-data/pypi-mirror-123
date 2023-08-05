from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="APIDjango",
    version="1.0",
    author="songhao",
    author_email="173077850@qq.com",
    description="django api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/songhaoi/django_api_deal.git",
    packages=["api_deal", "api_deal/middlewares"]
)
