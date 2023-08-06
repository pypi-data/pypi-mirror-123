from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Email Service Package'
LONG_DESCRIPTION = 'A package that allows to send emails with ease.'

# Setting up package settings
setup(
    name="emailservice",
    version=VERSION,
    author="Chaitanya Patil",
    author_email="<cdpgdg@gmail.com>",
    url="https://github.com/Chaitanyadp/EmailService.git",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['smtplib'],
    keywords=['email', 'smtp'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License"
    ]
)
