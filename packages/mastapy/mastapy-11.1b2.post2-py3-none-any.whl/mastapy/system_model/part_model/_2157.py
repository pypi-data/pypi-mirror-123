'''_2157.py

Bolt
'''


from mastapy.bolts import _1264
from mastapy._internal import constructor
from mastapy.system_model.part_model import _2158, _2159
from mastapy._internal.python_net import python_net_import

_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')


__docformat__ = 'restructuredtext en'
__all__ = ('Bolt',)


class Bolt(_2159.Component):
    '''Bolt

    This is a mastapy class.
    '''

    TYPE = _BOLT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Bolt.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bolt(self) -> '_1264.LoadedBolt':
        '''LoadedBolt: 'LoadedBolt' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1264.LoadedBolt)(self.wrapped.LoadedBolt) if self.wrapped.LoadedBolt is not None else None

    @property
    def bolted_joint(self) -> '_2158.BoltedJoint':
        '''BoltedJoint: 'BoltedJoint' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2158.BoltedJoint)(self.wrapped.BoltedJoint) if self.wrapped.BoltedJoint is not None else None
