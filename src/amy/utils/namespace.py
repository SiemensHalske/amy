class ConfigNamespace:
    """
    A custom namespace for dynamic attribute assignment,
    dictionary-like access, and optional validation.
    """

    def __init__(self, **kwargs):
        """
        Initialize the namespace with dynamic attributes from keyword arguments.
        """
        self.__dict__.update(kwargs)

    def __getitem__(self, key):
        """
        Allow dictionary-like access to attributes.
        """
        return getattr(self, key)

    def __setitem__(self, key, value):
        """
        Allow dictionary-like assignment of attributes.
        """
        setattr(self, key, value)

    def __delitem__(self, key):
        """
        Allow dictionary-like deletion of attributes.
        """
        delattr(self, key)

    def __contains__(self, key):
        """
        Check if an attribute exists in the namespace.
        """
        return key in self.__dict__

    def to_dict(self):
        """
        Convert the namespace to a dictionary.
        """
        return self.__dict__.copy()

    def update(self, **kwargs):
        """
        Dynamically update attributes with new values.
        """
        self.__dict__.update(kwargs)

    def __repr__(self):
        """
        Provide a readable representation of the namespace.
        """
        return f"ConfigNamespace({self.__dict__})"

    # method for dynamic returning of attributes
    def __getattr__(self, name):
        """
        Allow dynamic retrieval of attributes.
        """
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")
