import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="win64pyinstaller",
    version="0.1",
    author="Pranav",
    author_email="pranavbairy2@gmail.com",
    description="A package for windows which installes additional and small components for modules/projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pranav578/win64installer",
    project_urls={
        "Bug Tracker": "https://github.com/Pranav578/win64py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords = ["win64pyinstall", "pywin64installer", "pysetupinstaller", "wpi64"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.5",
)
