import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="patch-tracking",
  version="1.0.0",
  author="tushenmei",
  author_email="tushenmei@huawei.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitee.com/openeuler/patch-tracking",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
