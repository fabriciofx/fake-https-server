# SPDX-FileCopyrightText: Copyright (C) 2025-2026 Fabrício Barros Cabral
# SPDX-License-Identifier: MIT
import http.client
import ssl
from pathlib import Path

from fake_https_server.request import (
    ContentGet,
    ContentPost,
    Fail,
    FileContentGet,
)
from fake_https_server.server import Daemon, FakeHttpServer, FakeHttpsServer


def test_file_content_get() -> None:
    ca_file = Path(__file__).parent.parent / "certificates" / "ca.crt"
    content_file = Path(__file__).parent / "contents" / "hello-world.txt"
    server = Daemon(FakeHttpsServer(FileContentGet(content_file)))
    server.start()
    client = http.client.HTTPSConnection(
        "localhost",
        server.port(),
        context=ssl.create_default_context(cafile=ca_file),
    )
    client.request("GET", "/")
    response = client.getresponse()
    content = response.read().decode()
    server.stop()
    assert content == "Hello World!\n"


def test_large_file() -> None:
    ca_file = Path(__file__).parent.parent / "certificates" / "ca.crt"
    content_file = Path(__file__).parent / "contents" / "large.html"
    content = Path(content_file).read_text(encoding="utf-8")
    server = Daemon(FakeHttpsServer(FileContentGet(content_file)))
    server.start()
    client = http.client.HTTPSConnection(
        "localhost",
        server.port(),
        context=ssl.create_default_context(cafile=ca_file),
    )
    client.request("GET", "/")
    response = client.getresponse()
    html = response.read().decode()
    server.stop()
    assert content == html


def test_fail() -> None:
    retries = 1
    msg = "It works!"
    server = Daemon(FakeHttpServer(Fail(ContentGet(msg), retries)))
    server.start()
    try:
        client = http.client.HTTPConnection("localhost", server.port())
        client.request("GET", "/")
        response = client.getresponse()
    except Exception:
        client = http.client.HTTPConnection("localhost", server.port())
        client.request("GET", "/")
        response = client.getresponse()
    assert response.read().decode() == msg
    server.stop()


def test_content_post() -> None:
    ca_file = Path(__file__).parent.parent / "certificates" / "ca.crt"
    msg = "Hello World!"
    server = Daemon(FakeHttpsServer(ContentPost(msg)))
    server.start()
    client = http.client.HTTPSConnection(
        "localhost",
        server.port(),
        context=ssl.create_default_context(cafile=ca_file),
    )
    client.request("POST", "/")
    response = client.getresponse()
    content = response.read().decode()
    server.stop()
    assert content == msg
