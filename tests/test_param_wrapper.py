from dms_datastore_ui.param_wrapper import object_to_param_class, get_attributes, get_methods

def test_param_wrapper():

    # Example usage
    class MyClass:
        def __init__(self):
            self.my_int = 10
            self.my_str = "Hello"

        def example_method(self):
            return "This is a method of MyClass"

    # Create a parameterized class from an instance of MyClass
    my_obj = MyClass()
    MyParamClass = object_to_param_class(my_obj, ['my_int', 'my_str'], ['example_method'])

    # Create an instance of the parameterized class
    param_instance = MyParamClass()

    # Accessing parameter
    assert param_instance.my_int == 10

    param_instance.my_int = 20
    assert param_instance.my_int == 20
    assert my_obj.my_int == 20

    # Calling delegated method
    assert param_instance.example_method() == "This is a method of MyClass"

    assert get_methods(my_obj) == ['example_method']    

    assert get_attributes(my_obj) == ['my_int', 'my_str']