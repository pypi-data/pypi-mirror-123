'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1221 import KeyedJointDesign
    from ._1222 import KeyTypes
    from ._1223 import KeywayJointHalfDesign
    from ._1224 import NumberOfKeys
