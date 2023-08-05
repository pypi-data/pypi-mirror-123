import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PROJECT_NAME = "DS_start"
USER_NAME = 'TengHoo3'

setuptools.setup(
    name=f"DS-basic-start",
    version="0.0.9",
    author=USER_NAME,
    author_email="tenghoo3@gmail.com",
    description="Start your DS projects with some basic analysis using this package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NAME}/{PROJECT_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{USER_NAME}/{PROJECT_NAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "scipy",
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        'sklearn',
    ]
)
