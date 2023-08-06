'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1167 import ProSolveMpcType
    from ._1168 import ProSolveSolverType
