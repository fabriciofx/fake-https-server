# SPDX-FileCopyrightText: Copyright (C) 2025-2026 Fabrício Barros Cabral
# SPDX-License-Identifier: MIT
from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler
from pathlib import Path


class Request(ABC):
    @abstractmethod
    def action(self, handler: BaseHTTPRequestHandler) -> None:
        pass


class ContentGet(Request):
    def __init__(self, content: str) -> None:
        self.__content = content

    def action(self, handler: BaseHTTPRequestHandler) -> None:
        handler.send_response(200)
        handler.send_header("Content-type", "text/html")
        handler.end_headers()
        handler.wfile.write(self.__content.encode())


class ContentPost(Request):
    def __init__(self, content: str) -> None:
        self.__content = content

    def action(self, handler: BaseHTTPRequestHandler) -> None:
        handler.send_response(200)
        handler.send_header("Content-type", "text/html")
        handler.end_headers()
        handler.wfile.write(self.__content.encode())


class FileContentGet(Request):
    def __init__(self, filename: str | Path) -> None:
        self.__filename = filename

    def action(self, handler: BaseHTTPRequestHandler) -> None:
        handler.send_response(200)
        handler.send_header("Content-type", "text/html; charset=utf8")
        handler.end_headers()
        buffer = Path(self.__filename).read_bytes()
        handler.wfile.write(buffer)


class Fail(Request):
    def __init__(self, request: Request, retries: int) -> None:
        self.__origin = request
        self.__retries = retries

    def action(self, handler: BaseHTTPRequestHandler) -> None:
        if self.__retries > 0:
            handler.connection.close()
            self.__retries -= 1
        else:
            self.__origin.action(handler)
