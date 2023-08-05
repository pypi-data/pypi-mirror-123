=====
eq-dj-test-back
=====

'eq-dj-test-back' is a Django reusable app to help you make unit tests easier.

Requirements
------------
1. djangorestframework

Quick start
-----------
1. pip install eq-dj-test-back==<version>
2. Add "eq_dj_test_back" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'eq_dj_test_back',
        ...
    ]

3. Import the module like this:

    from eq_dj_test_back.base_test_view import ViewsTestBase (or whatever TestBase you need)

And that's all.

Usage
-----

1. Testing a model functionality:
    - Import the module:
        from eq_dj_test_back.base_test_model import ModelTestBase

    - Make a class for every class you need to test:
        class TestSomeModel(ModelTestBase):
            fixtures = ['some_model.json']

            def setUp(self):
                > Include the objects or what you feel necesary for the tests

            def test_some_method(self):
                self.base_test_model('method_name', 'maybe an assertion value', kwargs_of_method)
                > This will make an assertion with the specified data

-----
2. Testing a serializer functionality:
    - Import the module:
        from eq_dj_test_back.base_test_serializer import SerializerTestBase
    
    - Make a class for every class you need to test:
        class TestSomeSerializer(SerializerTestBase):
            fixtures = ['some_serializer.json']

            def setUp(self):
                self.data = {required data for feed a serializer class}
                self.serializer = SerializerClass
                > Include the objects or what you feel necesary for the tests

            def test_some_method(self):
                self.assertEqual(
                                self.base_test_ser('method_name', kwargs_of_method),
                                'assertion_value or something')
                > This will make a separated assertion using the instance or whatever the method returns

-----
3. Testing a view functionality:
    - Import the module:
        from eq_dj_test_back.base_test_view import ViewsTestBase
    
    - Make a class for every class you need to test:
        class TestSomeView(ViewsTestBase):
            fixtures = ['some_view.json']

            def setUp(self):
                self.user_pk = The pk used to authenticate the request
                self.to_path = 'identifier to feed the reverse method' for the url path
                self.data = {required data for generate a request}
                self.view = SomeView.as_view() the view that you want to test itself
                super(TestSomeView, self).setUp() used to extends the module's setUp method with the attrs before mentioned
            
            def test_some_method(self):
                self.base_test_view(
                    'method', data, status_code_to_assert,
                    self.get_path(self.to_path, kwargs to reverse function), kwargs to view function)