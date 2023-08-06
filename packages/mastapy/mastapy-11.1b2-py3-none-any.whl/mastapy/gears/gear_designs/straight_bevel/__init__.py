'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._905 import StraightBevelGearDesign
    from ._906 import StraightBevelGearMeshDesign
    from ._907 import StraightBevelGearSetDesign
    from ._908 import StraightBevelMeshedGearDesign
