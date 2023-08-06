import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="features_anal",
    version="0.0.2",
    author="Dipanshu Golan",
    author_email="dipanshugolan96@gmail.com",
    description="It performs feature analysis for data preprocessing or usage of data in Machine Learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DipanshuGolan/feature_analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)