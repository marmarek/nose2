from nose2 import events, loader, session
from nose2.plugins.loader import generators
from nose2.tests._common import TestCase


class TestGeneratorUnpack(TestCase):
    tags = ['unit']

    def setUp(self):
        self.session = session.Session()
        self.loader = loader.PluggableTestLoader(self.session)
        self.expect = [(0, ('call', (0, 1))),
                       (1, ('call', (1, 2))),
                       (2, ('call', (2, 3))),]
        self.plugin = generators.Generators(session=self.session)

    def test_unpack_handles_nose_style_generators(self):
        def gen():
            for i in range(0, 3):
                yield 'call', i, i + 1
        out = list(self.plugin.unpack(gen()))
        self.assertEqual(out, self.expect)

    def test_unpack_handles_unittest2_style_generators(self):
        def gen():
            for i in range(0, 3):
                yield 'call', (i, i + 1)
        out = list(self.plugin.unpack(gen()))
        self.assertEqual(out, self.expect)

    def test_ignores_ordinary_functions(self):
        class Mod(object):
            pass
        def test():
            pass
        m = Mod()
        m.test = test
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        self.assertEqual(len(event.extraTests), 0)

    def test_can_load_tests_from_generator_functions(self):
        class Mod(object):
            pass
        def check(x):
            assert x == 1
        def test():
            yield check, 1
            yield check, 2
        m = Mod()
        m.test = test
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        self.assertEqual(len(event.extraTests), 2)