from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-event-counter',
    version='0.1.1',
    description='This plugin reads how many events of defined type were triggered within defined time.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Dawid Kruk',
    author_email='krukdawid27@gmail.com',
    packages=['tracardi_event_counter'],
    install_requires=[
        'tracardi-plugin-sdk',
        'tracardi',
        'pytimeparse'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)