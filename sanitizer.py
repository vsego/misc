"""
A simple example to make a "sanitizer" decorator.

The intention for this is to be able to create an instance attribute that can
be set by the user, with the value validated or sanitised. The initial data is
given as an argument of the sanitizer, and the data itself is held in the
instance's dynamically created `__sanitizer_values` dictionary.

The only way "sanitized" properties are meant to be accessed is through their
given name, without the need for `self._name` type of attributes.
"""


def _get_sanitizer_values(obj):
    """
    Return a dictionary of sanitizer's values for the object `obj`.
    """
    try:
        return getattr(obj, "__sanitizer_values")
    except AttributeError:
        result = dict()
        setattr(obj, "__sanitizer_values", result)
        return result


def sanitizer_set_values(obj, **kwargs):
    """
    Set sanitizer's values for the object `obj`.
    """
    _get_sanitizer_values(obj).update(kwargs)


def sanitizer(*args, ignore_set_errors=False, **kwargs):
    """
    Return a property with identity getter and sanitizer setter.

    Sanitizer is a function that takes the new value, validates it, and
    processes it. It needs to return the processed value or raise an exception.

    Sanitizers have no `del` support because they always provide a default
    value if not set (so, deleting them serves no purpose).

    :param args: Positional arguments. There can be at most one and, if given,
        it is used as the default value.
    :param ignore_set_errors: Sanitizer is supposed to raise an exception if
        the new value doesn't pass validation. If `ignore_set_errors` is set to
        `True`, that exception is ignored (without changing the attribute's
        value). If `ignore_set_errors` is set to `False`, the exception is
        propagated.
    :param default: The default value for the sanitized argument before the
        setter is called for the first time. If this value is not given, the
        getter will fail with `AttributeError` exception when requested values
        of unset attributes.
        *Note:* Sanitizers with default will always have a value (reset to
        default if the attribute is deleted). Those without a given default
        will lose the value when deleted, even if that value was initially set
        with `sanitizer_set_values`.
    :return: A `property` with getter and setter properly set.
    """
    def wrapper(f):
        def getter(self):
            try:
                return _get_sanitizer_values(self)[attrib_name]
            except KeyError:
                try:
                    return kwargs["default"]
                except KeyError:
                    raise AttributeError(
                        "the value of '{obj}.{name}' was not set'".format(
                            obj=self.__class__.__name__,
                            name=attrib_name,
                        ),
                    )

        def setter(self, new_value):
            try:
                new_value = f(self, new_value)
            except Exception:
                if ignore_set_errors:
                    return
                else:
                    raise
            else:
                _get_sanitizer_values(self)[attrib_name] = new_value

        def deleter(self):
            try:
                del _get_sanitizer_values(self)[attrib_name]
            except KeyError as e:
                raise AttributeError(e)

        try:
            default = args[0]
        except IndexError:
            pass
        else:
            if len(args) > 1:
                raise TypeError(
                    "sanitizer() takes 1 positional argument but {cnt} were"
                    " given".format(cnt=len(args)),
                )
            if "default" in kwargs:
                raise TypeError(
                    "sanitizer() got multiple values for argument 'default'",
                )
            kwargs["default"] = default

        invalid_kwargs = set(kwargs) - {"default"}
        if invalid_kwargs:
            raise TypeError(
                "sanitizer() got an unexpected keyword argument {name}".format(
                    name=repr(key for key in kwargs if key in invalid_kwargs),
                ),
            )

        attrib_name = f.__name__
        return property(getter, setter, deleter, doc=f.__doc__)

    return wrapper


class X:

    def __init__(self):
        sanitizer_set_values(self, odd_preset=13)

    # This defines instance attribute `self.x` that is read as
    #     print(self.x)
    # and set as
    #     self.x = new_value
    # The method below validates and/or sanitizes the new value before it is
    # saved in `self.__sanitizer_values`.
    @sanitizer(17)
    def x(self, new_value):
        """
        `x` is a cool value.
        """
        return 2 * new_value

    @sanitizer(default="a")
    def vowel1(self, new_value):
        """
        `x` is a cool value.
        """
        if len(new_value) != 1 or new_value not in set("aeiou"):
            raise ValueError("non-vowel")
        return new_value

    @sanitizer(default="a", ignore_set_errors=True)
    def vowel2(self, new_value):
        """
        `x` is a cool value.
        """
        if len(new_value) != 1 or new_value not in set("aeiou"):
            raise ValueError("non-vowel")
        return new_value

    @sanitizer()
    def odd_preset(self, new_value):
        if new_value % 2 == 0:
            raise ValueError(
                "which part of the name 'ODD preset' is confusing to you? :-P",
            )
        return new_value

    @sanitizer()
    def even_preset(self, new_value):
        if new_value % 2 == 1:
            raise ValueError(
                "which part of the name 'EVEN preset' is confusing to you?"
                " :-P",
            )
        return new_value


if __name__ == "__main__":
    x = X()

    print("\nPart 1")
    print("x.x =", x.x)
    print("Setting x.x to 19...")
    x.x = 19
    print("x.x =", x.x)

    print("\nPart 2")
    print("x.vowel1 =", x.vowel1)
    try:
        print("Setting x.vowel1 to 'b'...")
        x.vowel1 = "b"
    except ValueError as e:
        print("Failed:", e)
    else:
        print("No error!")
    print("x.vowel1 =", x.vowel1)

    print("\nPart 3")
    print("x.vowel2 =", x.vowel2)
    try:
        print("Setting x.vowel2 to 'c'...")
        x.vowel2 = "c"
    except ValueError as e:
        print("Failed:", e)
    else:
        print("No error!")
    print("x.vowel2 =", x.vowel2)

    print("\nPart 4")
    print("Setting vowels to 'e' and 'o'...")
    x.vowel1 = "e"
    x.vowel2 = "o"
    print("x.vowel1 =", x.vowel1)
    print("x.vowel2 =", x.vowel2)

    print("\nPart 5")
    print("Deleting x.vowel1...")
    del x.vowel1
    print("x.vowel1 =", x.vowel1)

    print("\nPart 6")
    try:
        print("x.odd_preset =", x.odd_preset)
    except AttributeError as e:
        print("(1) Error getting x.odd_preset:", e)

    print("\nPart 7")
    print("Setting x.odd_preset to 1719...")
    x.odd_preset = 1719
    print("x.odd_preset =", x.odd_preset)
    print("Deleting x.odd_preset...")
    del x.odd_preset
    try:
        print("x.odd_preset =", x.odd_preset)
    except AttributeError as e:
        print("(2) Error getting x.odd_preset:", e)

    print("\nPart 8")
    try:
        print("x.even_preset =", x.even_preset)
    except AttributeError as e:
        print("Error getting x.even_preset:", e)
