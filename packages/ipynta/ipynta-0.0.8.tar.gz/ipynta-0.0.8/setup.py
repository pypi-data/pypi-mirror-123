from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("./README.md").read_text()

setup(name='ipynta',
      version='0.0.8',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description="A Python library for different image processing tasks.",
      packages=find_packages(),
      author="Allan Chua",
      install_requires=["pathlib"],
      author_email="allanchua.officefiles@gmail.com",
      keywords=["python", "images", "image utilities"],
      classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
      ],
      zip_safe=False)