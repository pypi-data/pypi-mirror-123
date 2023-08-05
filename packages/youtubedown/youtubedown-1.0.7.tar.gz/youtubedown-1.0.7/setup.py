import setuptools
import os

path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

requirements = []
with open(f"{path}/requirements.txt", encoding="UTF8") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="youtubedown",
    version="1.0.7",
    license='MIT',
    author="babihoba",
    author_email="hobabot@gmail.com",
    description="Allows you to asynchronously download Youtube_dl.",
    long_description=open('README.md').read(),
    install_requires=requirements,
    long_description_content_type="text/markdown",
    url="https://github.com/8954sood/youtubedown",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)