from setuptools import setup

# TODO(shiying): 去找个愿意帮忙写README的苦工，奥！苦工竟是我自己！
# with open("./soraha_utils/README.md", "r") as f:
#    long_des = f.read()

setup(
    name="soraha_utils",
    version="0.0.1",
    author="shiying",
    author_email="839778960@qq.com",
    description="soraha_utils",
    long_description="是羽衣在杂物间辛苦一天一夜找出来的各种小东西！请好好的使用吧！不要再随意丢弃了！(未完待续……预计0.0.2将会更新README.md)",
    long_description_content_type="text/markdown",
    url="https://www.github.com/LYshiying/soraha_utils",
    packages=["soraha_utils"],
    install_requires=[
        "httpx>=0.19.0",
        "ujson>=4.1.0",
        "loguru>=0.5.3",
        "requests>=2.26.0",
        "aiofiles>=0.7.0",
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    python_requires=">=3.6",
)
