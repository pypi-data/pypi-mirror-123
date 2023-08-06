from setuptools import setup

if __name__ == '__main__':
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setup(
        name="sqltest",
        install_requires=["openpyxl >= 3.0.9", "pandas >= 1.3.3"]
    )
