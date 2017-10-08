import log
import unittest


class TestLogMethods(unittest.TestCase):
    def test_error(self):
        log.err("test")

    def test_warn(self):
        log.warn("test")

    def test_info(self):
        log.info("test")

    def test_success(self):
        log.success("test")

    def test_properties(self):
        log.properties.add_func(lambda: 5)
        log.info("e")



if __name__ == '__main__':
    unittest.main()
