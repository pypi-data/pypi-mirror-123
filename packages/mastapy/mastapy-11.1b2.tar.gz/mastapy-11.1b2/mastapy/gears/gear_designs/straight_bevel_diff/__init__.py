'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._901 import StraightBevelDiffGearDesign
    from ._902 import StraightBevelDiffGearMeshDesign
    from ._903 import StraightBevelDiffGearSetDesign
    from ._904 import StraightBevelDiffMeshedGearDesign
