from unittest import TestCase

from landshark.controllers import controller


class TestController(TestCase):
    def test_init(self):
        class foo(controller):
            def required_keys(self):
                return ['foo']
        class bar(controller):
            def required_keys(self):
                return ['bar', 'bar2']
        class foobar(foo, bar):
            def required_keys(self):
                return ['bar', 'foobar']

        initcase0 = {"foo": 1, "bar": 1, "bar2": 1, "foobar": 1}
        fb = foobar(initcase0)
        self.assertEqual(fb.foo, 1)

        initcase1 = ("bar", "bar2", "foobar")
        initcase2 = ("foo", "bar", "foobar")
        initcase3 = ("foo", "bar", "bar2")
        initcases = {
            initcase1: 'foo',
            initcase2: 'bar2',
            initcase3: 'foobar',
        }  

        for case, error_key in initcases.items():
            with self.assertRaisesRegex(KeyError, f"Missing needed keys .*{error_key}"):
                foobar({key: 1 for key in case})

        initcase4 = {"foo": 1, "bar": 1, "bar2": 1, "foobar": 1, 'required_keys': 1}
        with self.assertRaisesRegex(Exception, "Conflicting definition.*required_keys"):
            foobar(initcase4)

