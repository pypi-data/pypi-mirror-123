import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# 
setup(
    name="awsee",
    version="0.0.28",
    description="Utility to help me manage my AWS CLI Session with Profiles, Roles and MFA",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://ualter.github.io/awsee-site/",
    author="Ualter Otoni Pereira",
    author_email="ualter.junior@gmail.com",
    keywords = ['aws', 'cloud', 'awsee', 'boto3', 'ec2', 'vpc'],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["awsee"],
    include_package_data=True,
    install_requires=[            
        'botocore>=1.21.62',
        'boto3>=1.18.62',
        'Pygments>=2.3.1',
        'arnparse>=0.0.2',
        'tinydb>=4.5.2',
        'clipboard>=0.0.4',
        'pyreadline',
        'pytz>=2019.3',
        'python-dateutil>=2.8.2',
        'XlsxWriter>=1.3.7',
        'prompt_toolkit>=2.0.10'
    ],
    scripts=[
        'shell_scripts/awsee.bat',
        'shell_scripts/awsee'
    ],
    entry_points={
        "console_scripts": [
            "awseepy=awsee.awseepy:main",
        ]
    },
)