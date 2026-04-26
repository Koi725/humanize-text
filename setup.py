from setuptools import setup

setup(
    name="humanize-text",
    version="1.0.0",
    description="Transform AI-generated text into natural, human-sounding writing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kousha Rezaei",
    author_email="kousha.rezaei@ua.pt",
    url="https://github.com/Koi725/humanize-text",
    py_modules=["humanize"],
    entry_points={
        "console_scripts": [
            "humanize=humanize:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing",
    ],
)
