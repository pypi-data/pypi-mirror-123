'''_2326.py

ActiveShaftDesignSelection
'''


from mastapy.system_model.part_model.configurations import _2331
from mastapy.system_model.part_model.shaft_model import _2196
from mastapy.shafts import _40
from mastapy._internal.python_net import python_net_import

_ACTIVE_SHAFT_DESIGN_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveShaftDesignSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveShaftDesignSelection',)


class ActiveShaftDesignSelection(_2331.PartDetailSelection['_2196.Shaft', '_40.SimpleShaftDefinition']):
    '''ActiveShaftDesignSelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_SHAFT_DESIGN_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveShaftDesignSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
