import setuptools as SetUpToolS

with open("README.md", "r",encoding="UTF-8") as fh:
  long_description = fh.read()

SetUpToolS.setup(
  name="civilianM",
  version="2.6.97",
  author="AC97",
  author_email="ehcemc@hotmail.com",
  description="Common functions,More will be added in the future,Look forward to your use",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="",
  packages=SetUpToolS.find_packages(),
  requires=[
      'BeautifulSoup4',
      'requests',
      'lxml',
      ],
  install_requires=[
      'BeautifulSoup4',
      'requests',
      'lxml',
      ],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
