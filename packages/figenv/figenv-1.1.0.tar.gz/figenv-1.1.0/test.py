import contextlib
import os
import typing
import unittest

from figenv import MetaConfig, strict


class TestEnv(unittest.TestCase):
    @contextlib.contextmanager
    def with_env(self, **kwargs):
        """Context manager to set temporary environment variables and then remove when done"""
        # Set environment variables
        os.environ.update(kwargs)

        # Yield to caller
        yield

        # Delete set variables
        for key in kwargs.keys():
            if key in os.environ:
                del os.environ[key]
        for key in ('ENV_LOAD_ALL', 'ENV_PREFIX'):
            if key in os.environ:
                del os.environ[key]

    def _get_test_configuration(self, env_prefix='', env_load_all=False, bases=None, **kwargs):
        """Helper to define a new configuration class using our MetaConfig"""
        if bases is None:
            bases = (object,)
        return MetaConfig('TestConfiguration', bases, dict(ENV_PREFIX=env_prefix, ENV_LOAD_ALL=env_load_all, **kwargs))

    def test_default_env_load_all(self):
        """A test to ensure that we load all environment variables by default"""
        # Configure an environment variable not defined on the configuration class
        with self.with_env(TEST_SETTING='true', DEFAULT_SETTING='set_by_env'):
            # Create our configuration object
            TestConfiguration = self._get_test_configuration(
                env_load_all=True,
                DEFAULT_SETTING='set_in_class',
            )

            self.assertEqual(TestConfiguration.DEFAULT_SETTING, 'set_by_env')

            # Assert that we only loaded defined settings from environment
            self.assertTrue(hasattr(TestConfiguration, 'TEST_SETTING'))

            with self.assertRaises(AttributeError):
                TestConfiguration.WHAT

        self.assertEqual(TestConfiguration.DEFAULT_SETTING, 'set_in_class')

    def test_default_settings(self):
        """A test to ensure that if no environment variable is set, we get the default value that is set"""
        TestConfiguration = self._get_test_configuration(DEFAULT_SETTING='default_value', BOOL_SETTING=True)
        self.assertEqual(TestConfiguration.DEFAULT_SETTING, 'default_value')
        self.assertIs(TestConfiguration.BOOL_SETTING, True)

    def test_invalid_setter(self):
        """users should not be able to set variables using attributes"""
        TestConfiguration = self._get_test_configuration(DEFAULT_SETTING='default_value', BOOL_SETTING=True)
        with self.assertRaises(NotImplementedError):
            TestConfiguration.DEFAULT_SETTING = 'hi'

    def test_coerce_settings(self):
        """A test to ensure that annotations are used to coerce variables"""

        class csv:
            @classmethod
            def _coerce(self, value):
                return value.split(',')

        class TestConfiguration(metaclass=MetaConfig):
            DEFAULT_SETTING: csv = 'default,value'
            BOOL_SETTING: bool = '1'
            FALSE_SETTING: bool = '0'
            INT_SETTING: int = '1093'
            FLOAT_SETTING: float = '1.938'
            DICT_SETTING: typing.Dict = '{"hello":"world"}'

        self.assertEqual(TestConfiguration.DEFAULT_SETTING, ['default', 'value'])
        self.assertIs(TestConfiguration.BOOL_SETTING, True)
        self.assertIs(TestConfiguration.FALSE_SETTING, False)
        self.assertEqual(TestConfiguration.INT_SETTING, 1093)
        self.assertEqual(TestConfiguration.FLOAT_SETTING, 1.938)
        self.assertEqual(TestConfiguration.DICT_SETTING, {'hello': 'world'})

    def test_inherit_settings(self):
        """A test inheriting settings"""
        Parent = self._get_test_configuration(CLASS='parent', SECONDARY='second')
        Child = self._get_test_configuration(bases=(Parent,), CLASS='child')
        assert Child.CLASS == 'child'
        assert Parent.CLASS == 'parent'
        assert Child.SECONDARY == 'second'
        assert Parent.SECONDARY == 'second'

    def test_dict_update_settings(self):
        """A configuration class can be updated in a dict"""

        def func(cls):
            return 'hi'

        test = dict()
        settings = self._get_test_configuration(NAME='test', HELLO=func)
        test.update(settings)
        assert test['HELLO'] == 'hi'
        assert test['NAME'] == 'test'
        with self.assertRaises(KeyError):
            settings['UNSET']

    def test_iterate_settings(self):
        """A configuration class can be iterable"""

        def func(cls):
            return 'hi'

        settings = self._get_test_configuration(NAME='test', HELLO=func)
        test = {key: value for key, value in settings}
        assert test['HELLO'] == 'hi'
        assert test['NAME'] == 'test'

        with self.assertRaises(KeyError):
            settings['UNSET']

    def test_override_from_env(self):
        """A test to ensure that an environment variable will override the default setting"""
        with self.with_env(DEFAULT_SETTING='set_by_env'):
            TestConfiguration = self._get_test_configuration(DEFAULT_SETTING='default_value')
            self.assertEqual(TestConfiguration.DEFAULT_SETTING, 'set_by_env')

    def test_only_set_on_env(self):
        """A test to ensure that a setting only defined by an environment variable is still available"""
        with self.with_env(NEW_SETTING='set_by_env'):
            # When configured to load all environment variables
            TestConfiguration = self._get_test_configuration(env_load_all=True)
            self.assertEqual(TestConfiguration.NEW_SETTING, 'set_by_env')

            # When configured to not load all environment variables
            TestConfiguration = self._get_test_configuration(env_load_all=False)
            self.assertFalse(hasattr(TestConfiguration, 'NEW_SETTING'))

    def test_env_prefix(self):
        """A test to ensure that the ENV_PREFIX setting functions as needed"""
        with self.with_env(TEST_DEFAULT_SETTING='set_by_env'):
            TestConfiguration = self._get_test_configuration(env_prefix='TEST_', DEFAULT_SETTING='default_value')
            self.assertEqual(TestConfiguration.DEFAULT_SETTING, 'set_by_env')

    def test_env_prefix_non_matching(self):
        """A test to ensure that the ENV_PREFIX setting does not allow non-matching settings in"""
        with self.with_env(DEFAULT_SETTING='set_by_env'):
            TestConfiguration = self._get_test_configuration(env_prefix='MYAPP_', DEFAULT_SETTING='default_value')
            self.assertEqual(TestConfiguration.DEFAULT_SETTING, 'default_value')

    def test_parsing_boolean(self):
        """A test to ensure that we properly parse booleans"""
        # DEV: We have to set the environment variable first, since they get loaded into the class on definition
        env = dict(
            IS_TRUE='true',
            IS_NOT_TRUE='true-ish',
            IS_FALSE='FALSE',
            IS_WACKY_FALSE='FaLSe',
        )
        with self.with_env(**env):
            # DEV: Set `env_load_all=True` to keep from having to make default values for each variable
            TestConfiguration = self._get_test_configuration(env_load_all=True)
            self.assertEqual(TestConfiguration.IS_TRUE, True)
            self.assertEqual(TestConfiguration.IS_NOT_TRUE, 'true-ish')
            self.assertEqual(TestConfiguration.IS_FALSE, False)
            self.assertEqual(TestConfiguration.IS_WACKY_FALSE, False)

    def test_parsing_float(self):
        """A test to ensure that we properly parse floats"""
        env = dict(
            IS_FLOAT='12.5',
            TRAILING_DOT='12.',
            LEADING_DOT='.12',
            IS_NOT_FLOAT='This is 6.5',
        )
        with self.with_env(**env):
            # DEV: Set `env_load_all=True` to keep from having to make default values for each variable
            TestConfiguration = self._get_test_configuration(env_load_all=True)
            self.assertEqual(TestConfiguration.IS_FLOAT, 12.5)
            self.assertEqual(TestConfiguration.TRAILING_DOT, 12.0)
            self.assertEqual(TestConfiguration.LEADING_DOT, 0.12)
            self.assertEqual(TestConfiguration.IS_NOT_FLOAT, 'This is 6.5')

    def test_parsing_int(self):
        """A test to ensure that we properly parse integers"""
        env = dict(
            IS_INT='12',
            IS_ZERO='0',
            IS_NOT_INT='12fa',
        )
        with self.with_env(**env):
            # DEV: Set `env_load_all=True` to keep from having to make default values for each variable
            TestConfiguration = self._get_test_configuration(env_load_all=True)
            self.assertEqual(TestConfiguration.IS_INT, 12)
            self.assertEqual(TestConfiguration.IS_ZERO, 0)
            self.assertEqual(TestConfiguration.IS_NOT_INT, '12fa')

    def test_parsing_version_string(self):
        """A test to ensure that we properly parse integers"""
        env = dict(VERSION_STRING='1.0.2')
        with self.with_env(**env):
            # DEV: Set `env_load_all=True` to keep from having to make default values for each variable
            TestConfiguration = self._get_test_configuration(env_load_all=True)
            self.assertEqual(TestConfiguration.VERSION_STRING, '1.0.2')

    def test_classmethod_functions(self):
        """A test to ensure that we properly parse integers"""

        def func(cls):
            return cls.DATA + '123'

        TestConfiguration = self._get_test_configuration(DATA='blah', FUNC=func)
        self.assertEqual(TestConfiguration.FUNC, 'blah123')
        assert 'FUNC' in dir(TestConfiguration)

    def test_override_from_env_functions(self):
        """A test to ensure that functions are overridden with environment values"""

        def func(cls):
            return cls.DATA + ' world'

        with self.with_env(GREETING='hola mundo'):
            TestConfiguration = self._get_test_configuration(DATA='hello', GREETING=func)
            assert 'GREETING' in dir(TestConfiguration)
            self.assertEqual(TestConfiguration.GREETING, 'hola mundo')

    def test_strict_functions(self):
        """A test to ensure that strict functions are NOT overridden with environment values"""

        @strict
        def func(cls):
            return cls.DATA + ' world'

        with self.with_env(GREETING='hola mundo'):
            TestConfiguration = self._get_test_configuration(DATA='hello', GREETING=func)
            assert 'GREETING' in dir(TestConfiguration)
            self.assertEqual(TestConfiguration.GREETING, 'hello world')


if __name__ == '__main__':
    unittest.main()
