'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1169 import ElementPropertyClass
    from ._1170 import MaterialPropertyClass
