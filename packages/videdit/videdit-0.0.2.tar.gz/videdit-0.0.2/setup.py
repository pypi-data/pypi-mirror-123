import setuptools

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name="videdit",
    description="Set of commands used to edit video files",
    version="0.0.2",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "videdit=videdit.__main__:main"
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
