import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Auto_cui",                        # 这个包的名字
    version="0.0.5",                           # 版本号
    author="Cui Zy",
    author_email="1776228595@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SynchronyML/protein_lucky",
    project_urls={
        "Bug Tracker": "https://github.com/SynchronyML/protein_lucky/issues",
    },
    install_requires=["numpy==1.21.2"],         # 依赖列表，先在0.0.3版本确认此功能ok
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},                         # 资源文件的名字
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)