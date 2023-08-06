import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="baiduindex",
    version="0.0.1",
    author="hongyizhu",
    author_email="472739561@qq.com",
    description="scary of baidu index",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhyzhyzhy123/baiduindex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)