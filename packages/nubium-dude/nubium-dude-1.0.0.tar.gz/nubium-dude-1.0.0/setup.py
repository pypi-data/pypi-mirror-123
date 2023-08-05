import setuptools

with open("README.md", "r") as file_obj:
    long_description = file_obj.read()

install_requires = [
    "nubium-utils[confluent]>=0.27.0a",
    "nubium-schemas>=1.1.2a",
    "click>=8.0.1",
    "virtualenv>=20.4.7",
    "virtualenv-api>=2.1.18",
    "python-dotenv>=0.19.0",
]

dev_requires = install_requires

packages = setuptools.find_packages()

setuptools.setup(
    name="nubium-dude",
    version="1.0.0",
    author="Red Hat Marketing Operations Data Engineering",
    author_email="mo-de-notifications@redhat.com",
    description="Developer utilities to help manage nubium applications and other typical maintenance tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.corp.redhat.com/mkt-ops-de/dude.git",
    packages=packages,
    install_requires=install_requires,
    extras_require={"dev": install_requires},
    entry_points={
        'console_scripts': [
            'dude = dude.__main__:dude_cli',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
