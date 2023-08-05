import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="pkgship",
  version="2.1.0",
  author="tushenmei",
  author_email="tushenmei@huawei.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitee.com/openeuler/pkgship",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
