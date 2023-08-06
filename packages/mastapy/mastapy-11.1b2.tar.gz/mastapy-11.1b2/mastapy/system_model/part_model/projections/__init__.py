'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2198 import SpecifiedConcentricPartGroupDrawingOrder
    from ._2199 import SpecifiedParallelPartGroupDrawingOrder
