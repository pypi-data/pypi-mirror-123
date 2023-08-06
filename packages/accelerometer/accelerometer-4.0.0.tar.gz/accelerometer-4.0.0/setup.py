import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="accelerometer",
    version="4.0.0",
    author="Aiden Doherty",
    author_email="aiden.doherty@ndph.ox.ac.uk",
    description="A package to extract meaningful health information from large accelerometer datasets e.g. how much time individuals spend in sleep, sedentary behaviour, walking and moderate intensity physical activity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/activityMonitoring/biobankAccelerometerAnalysis",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'pandas>=1.2.5',
        'scikit-learn>=0.24.2',
        'joblib',
        'statsmodels',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": [
            "accProcess=accelerometer.accProcess:main",
            "accPlot=accelerometer.accPlot:main"
        ]
    },
)
