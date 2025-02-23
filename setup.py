from setuptools import setup, find_packages

setup(
    name="nutritional_analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        "paddleocr",
        "groq"
    ],
    entry_points={
        "console_scripts": [
            "nutritional_analysis = nutritional_analysis.gui:main"
        ]
    },
)
