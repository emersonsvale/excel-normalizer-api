from setuptools import setup, find_packages

setup(
    name="excel-normalizer-api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "numpy==1.21.6",
        "pandas==1.3.5",
        "openpyxl==3.1.2",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0"
    ],
) 