# SPDX-FileCopyrightText: Copyright (C) 2025-2026 Fabrício Barros Cabral
# SPDX-License-Identifier: MIT

import http.client
import ssl
from pathlib import Path

from fake_https_server.request import ContentGet
from fake_https_server.server import Daemon, FakeHttpServer, FakeHttpsServer


def test_fake_http_server() -> None:
    msg = "It works"
    server = Daemon(FakeHttpServer(ContentGet(msg)))
    server.start()
    client = http.client.HTTPConnection("localhost", server.port())
    client.request("GET", "/")
    response = client.getresponse()
    content = response.read().decode()
    server.stop()
    assert content == msg


def test_fake_https_server() -> None:
    ca_file = Path(__file__).parent.parent / "certificates" / "ca.crt"
    msg = "It works!"
    server = Daemon(FakeHttpsServer(ContentGet(msg)))
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
    assert content == msg
