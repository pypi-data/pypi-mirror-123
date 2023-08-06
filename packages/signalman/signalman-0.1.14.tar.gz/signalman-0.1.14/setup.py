import setuptools


setuptools.setup(
    name="signalman",
    version="0.1.14",
    author="Joseph Ryan-Palmer",
    author_email="joseph@ryan-palmer.com",
    description="A small application to poll for response code or text",
    long_description=open('README.md', "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JosephRPalmer/signalman",
    project_urls={
        "Bug Tracker": "https://github.com/JosephRPalmer/signalman/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"signalman": "signalman"},
    packages=["signalman"],
    python_requires=">=3.6",
    install_requires=[
        'requests',
        'interruptingcow',
        'retrying',
    ],
    entry_points={
        "console_scripts": ["signalman=signalman.signalman:main"]
    },
)
