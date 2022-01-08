# Created by BaiJiFeiLong@gmail.com at 2022/1/8 21:49

import distutils.log
import logging
import os

import colorlog
import setuptools.dist
from pathlib3x import Path


def main():
    initLogging()
    doBuild()
    logging.info("Generated files:")
    for path in Path("target").glob("**/dist/*"):
        logging.info(f"\t{path} %.2f MB", path.stat().st_size / 1024 / 1024)


def initLogging():
    consoleLogPattern = "%(log_color)s%(asctime)s %(levelname)8s %(name)-16s %(message)s"
    logging.getLogger().handlers = [logging.StreamHandler()]
    logging.getLogger().handlers[0].setFormatter(colorlog.ColoredFormatter(consoleLogPattern))
    logging.getLogger().setLevel(logging.DEBUG)


def doBuild():
    readme = Path("README.md").read_text(encoding="utf8")
    os.chdir(f"target")
    for path in Path().glob("*"):
        if path.name != "IceSpringPathLib":
            path.rmtree()

    distutils.log.set_verbosity(1)
    for command in ["sdist", "bdist_wheel"]:
        setuptools.dist.Distribution(attrs=dict(
            script_name="",
            name='IceSpringPathLib',
            url="https://github.com/baijifeilong/IceSpringPathLib",
            license='MIT',
            author='BaiJiFeiLong',
            author_email='baijifeilong@gmail.com',
            version='1.0.0',
            description='`pathlib` Wrapper with **UTF-8 first** and **LineFeed first**, based on `pathlib3x`.',
            packages=["IceSpringPathLib"],
            package_data={"IceSpringPathLib": ['*.pyi']},
            long_description=readme,
            long_description_content_type='text/markdown'
        )).run_command(command)
    os.chdir("..")


if __name__ == '__main__':
    main()
