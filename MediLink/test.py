import unittest
import os


class TestASGIConfig(unittest.TestCase):
    def test_asgi_config_syntax(self):
        print("\nRunning: test for asgi")
        asgi_file_path = os.path.join(os.path.dirname(__file__), "asgi.py")
        with open(asgi_file_path, "rb") as asgi_file:
            compile(asgi_file.read(), asgi_file_path, "exec")
        print("Complete: test for asgi")


class TestWSGIConfig(unittest.TestCase):
    def test_wsgi_config_syntax(self):
        print("\nRunning: test for wsgi")
        wsgi_file_path = os.path.join(os.path.dirname(__file__), "wsgi.py")
        with open(wsgi_file_path, "rb") as wsgi_file:
            compile(wsgi_file.read(), wsgi_file_path, "exec")
        print("Complete: test for wsgi")
