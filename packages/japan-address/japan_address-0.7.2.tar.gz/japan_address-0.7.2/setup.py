import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="japan_address",
    version="0.7.2",
    license='MIT',
    author="kzthrk",
    author_email="kzthrk@gmail.com",
    description="Japan address utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kzthrk/japan_address",
    # packages=setuptools.find_packages(),
    packages=['japan_address'],
    package_dir={'japan_address': 'japan_address'},
    package_data={'japan_address': ['data/*.csv']},
    keywords='japan, japanese, address',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)