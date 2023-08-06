import setuptools

require_depend = ['pybase64>=1.2.0,<5', 'requests>=2.25,<3', 'pyparsing>=2.4,<3', 'jsons>=1.5.1,<3']
setuptools.setup(
    name="nctevnhn",
    version="2021.10.1",
    author="@trumxuquang",
    author_email="trumxuquang@gmail.com",
    description="https://vnhass.blogspot.com/",
    long_description="https://vnhass.blogspot.com/",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=require_depend,
)