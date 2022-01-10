# Created by BaiJiFeiLong@gmail.com at 2022/1/8 13:37

from __future__ import annotations

import importlib.util
import logging
import typing

import colorlog
import libcst
from pathlib3x import Path

if typing.TYPE_CHECKING:
    from typing import *
    from libcst import *


def main():
    initLogging()
    root = Path("target/IceSpringPathLib")
    root.rmtree(ignore_errors=True)
    root.mkdir(parents=True)
    for path in Path(importlib.util.find_spec("pathlib3x").origin).parent.glob("*.py*"):
        newText = processScript(path)
        newPath = root / path.name.replace("pathlib3x", "IceSpringPathLib")
        newPath.write_text(newText, encoding="utf8")


def processScript(path) -> str:
    text = path.read_text("utf8")
    text = "\n".join([x.replace("pathlib3x", "IceSpringPathLib") if "import" in x else x for x in text.splitlines()])
    if path.name in ["pathlib3x.py", "pathlib3x.pyi"]:
        text = libcst.parse_module(text).visit(PyTransformer(isStub=path.suffix == ".pyi")).code
    return "\n".join(['"""', "\n\n".join([
        "`pathlib` Wrapper with **UTF-8 first** and **LineFeed first**, based on `pathlib3x`.",
        "Home: https://baijifeilong.github.io/2022/01/08/ice-spring-path-lib/index.html",
        "Github: https://github.com/baijifeilong/IceSpringPathLib",
        "PyPI(IceSpringPathLib): https://pypi.org/project/IceSpringPathLib",
        "PyPI(pathlib3x): https://pypi.org/project/pathlib3x",
        "Generated by BaiJiFeiLong@gmail.com",
        "License: MIT"
    ]), '"""']) + "\n\n" + text


def initLogging():
    consolePattern = "%(log_color)s%(asctime)s %(levelname)8s %(name)-16s %(message)s"
    logging.getLogger().handlers = [logging.StreamHandler()]
    logging.getLogger().handlers[0].setFormatter(colorlog.ColoredFormatter(consolePattern))
    logging.getLogger().setLevel(logging.DEBUG)


class PyTransformer(libcst.CSTTransformer):
    currentClass = None
    currentMethod = None
    isStub: bool

    def __init__(self, isStub: bool):
        super().__init__()
        self.isStub = isStub

    @property
    def fileType(self) -> str:
        return "stub" if self.isStub else "source"

    def visit_ClassDef_name(self, node: "ClassDef") -> None:
        self.currentClass = node.name.value

    def visit_FunctionDef_name(self, node: "FunctionDef") -> None:
        self.currentMethod = node.name.value

    def leave_Param(self, original_node: "Param", updated_node: "Param") \
            -> Union["Param", "MaybeSentinel", FlattenSentinel["Param"], RemovalSentinel]:
        currentParameter = original_node.name.value
        if self.currentClass == "Path" and self.currentMethod in ["open", "read_text", "write_text"] \
                and currentParameter == "encoding":
            logging.info(f"Processing {self.fileType} %s.%s: set utf8 default", self.currentClass, self.currentMethod)
            return updated_node.with_changes(default=libcst.SimpleString("'utf8'"))
        return updated_node

    def leave_Parameters(self, original_node: "Parameters", updated_node: "Parameters") -> "Parameters":
        if self.currentClass == "Path" and self.currentMethod in ["read_text", "write_text"]:
            logging.info(f"Processing {self.fileType} %s.%s: add newline parameter", self.currentClass,
                self.currentMethod)
            default = libcst.SimpleString(r"'\n'") if self.currentMethod == "write_text" else libcst.Name(value="None")
            return updated_node.with_changes(params=list(updated_node.params) + [libcst.Param(
                name=libcst.Name(value="newline"),
                annotation=libcst.Annotation(annotation=libcst.Subscript(
                    value=libcst.Name(value="Optional"),
                    slice=[libcst.SubscriptElement(slice=libcst.Index(value=libcst.Name(value="str")))]
                )) if self.isStub else None,
                default=default
            )])
        return updated_node

    def leave_Call(self, original_node: "Call", updated_node: "Call") -> "BaseExpression":
        if self.currentClass == "Path" and self.currentMethod in ["read_text", "write_text"]:
            func = original_node.func
            if isinstance(func, libcst.Attribute) and isinstance(func.value,
                    libcst.Name) and func.value.value == "self" and func.attr.value == "open":
                logging.info(f"Processing {self.fileType} %s.%s: add newline argument", self.currentClass,
                    self.currentMethod)
                return updated_node.with_changes(args=list(updated_node.args) + [libcst.Arg(
                    keyword=libcst.Name(value="newline"), value=libcst.Name(value='newline'))])
        return updated_node


if __name__ == '__main__':
    main()
