from setuptools import setup

setup(
    name="Piper",
    version="0.1",
    description="Pipe based crawler",
    author="Tulga Ariuntuya",
    author_email="sw06d103@gmail.com",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    python_requires='>=3.6',
    install_requires=[
        "recordclass==0.5",
        "requests==2.18.4",
        "lxml",
        "cssselect",
    ],
    packages=["piper"],
)
