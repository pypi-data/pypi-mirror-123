'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._925 import HypoidGearDesign
    from ._926 import HypoidGearMeshDesign
    from ._927 import HypoidGearSetDesign
    from ._928 import HypoidMeshedGearDesign
