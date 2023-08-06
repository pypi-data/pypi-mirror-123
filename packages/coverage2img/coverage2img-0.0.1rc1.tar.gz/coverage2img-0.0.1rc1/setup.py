import setuptools

setuptools.setup(
    name="coverage2img",
    url="https://github.com/fwani/CoverageToImg",
    version="0.0.1rc1",
    author="fwani",
    author_email="seungfwani@gmail.com",
    description="This is a tool for converting coverage.json to image.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=['coverage2img'], exclude=['tests']),
    install_requires=[
        "kaleido==0.2.1",
        "plotly==5.3.1",
        "pandas==1.3.3",
        "click==8.0.3",
    ],
    entry_points={
        'console_scripts': [
            'coverage2img = coverage2img.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
