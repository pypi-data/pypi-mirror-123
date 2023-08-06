'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5370 import AbstractAssemblyStaticLoadCaseGroup
    from ._5371 import ComponentStaticLoadCaseGroup
    from ._5372 import ConnectionStaticLoadCaseGroup
    from ._5373 import DesignEntityStaticLoadCaseGroup
    from ._5374 import GearSetStaticLoadCaseGroup
    from ._5375 import PartStaticLoadCaseGroup
