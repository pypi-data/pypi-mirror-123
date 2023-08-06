import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="very-gui",
  version="0.0.2",
  author="xxx",
  author_email="e2662020@outlook.com",
  description="This is a great GUI library for beginners",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ZhengHaotian2010/gui.py",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
