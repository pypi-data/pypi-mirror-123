import setuptools

setuptools.setup(
    name="uniqpy",
    version="0.1.2",
    author="D.N. Konanov",
    author_email="konanovdmitriy@gmail.com",
    description="UNIQUAC-based tool for multicomponent VLEs",
    long_description="uniqpy",
    long_description_content_type="",
    url="https://github.com/DNKonanov/uni_cli",
    project_urls={
        "Bug Tracker": "https://github.com/DNKonanov/uni_cli",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    packages=['uniqpy'],
    install_requires=[
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'uniqpy=uniqpy.uni_cli:main'
        ]
    }
)
