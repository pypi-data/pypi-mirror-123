from setuptools import find_packages
from setuptools import setup

__version__ = "0.0.1"

setup(
    name="morstar_flask_restful",
    version=__version__,
    author="Tachi",  # 作者
    author_email="294350192@qq.com",  # 邮箱
    description="Encapsulate flask_restful",  # 代码描述
    long_description="Encapsulate flask_restful",  # 代码详细描述
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-restful",
        "flask-migrate",
        "flask-jwt-extended",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        "python-dotenv",
        "passlib",
        "apispec[yaml]",
        "apispec-webframeworks",
    ],
    entry_points={"flask.commands": ["app = app.manage:cli"]},
)
