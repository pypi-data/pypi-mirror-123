import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="borgo",
    version="0.0.7",
    author="Team Borgo",
    description="Library for sending requests to the Borgo app.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["borgo"],
    package_dir={'': 'borgo/src'},
    install_requires=['python-socketio', 'python-socketio[client]']
)
