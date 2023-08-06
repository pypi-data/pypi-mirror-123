# setup.py
# Setup installation for the application

from setuptools import find_namespace_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

required_packages = ["onnxruntime", "Pillow"]

dev_packages = ["black", "flake8", "isort", "jupyterlab", "pre-commit", "mypy"]

setup(
    name="dogsvscats",
    version="0.2.0",
    license="Apache",
    description="Solution for Kaggle competition https://www.kaggle.com/c/dogs-vs-cats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alberto Burgos",
    author_email="albertoburgosplaza@gmail.com",
    url="https://github.com/albertoburgosplaza/dogs-vs-cats",
    keywords=[
        "machine-learning",
        "artificial-intelligence",
        "computer-vision",
        "kaggle",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
    ],
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
        "dev": dev_packages,
    },
)
