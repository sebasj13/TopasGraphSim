import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topasgraphsim",
    version="23.0.2",
    author="Sebastian Schäfer",
    author_email="sebastian.schaefer@student.uni-halle.de",
    description="GUI to analyze the results of a Monte-Carlo radiation simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sebasj13/TopasGraphSim",
    project_urls={"Bug Tracker": "https://github.com/sebasj13/TopasGraphSim/issues",},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "customtkinter",
        "requests",
        "numpy",
        "scipy",
        "pynput",
        "opencv-python",
        "Pillow",
        "matplotlib",
        "topas2numpy",
        "pymedphys",
        "python-tkdnd"
    ],
    packages=[
        "topasgraphsim",
        "topasgraphsim.src",
        "topasgraphsim.src.classes",
        "topasgraphsim.src.functions",
    ],
    scripts=["topasgraphsim/topasgraphsim.py"],
    entry_points={
        "console_scripts": ["topasgraphsim=topasgraphsim.topasgraphsim:TopasGraphSim"],
    },
    keywords=["topas", "monte-carlo", "python", "simulation"],
    python_requires=">=3.10",
)