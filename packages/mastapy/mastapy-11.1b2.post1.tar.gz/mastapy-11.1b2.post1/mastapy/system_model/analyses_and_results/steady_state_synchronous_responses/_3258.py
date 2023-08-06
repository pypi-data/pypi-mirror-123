'''_3258.py

CylindricalGearSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2238, _2240
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6548, _6553
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3270
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'CylindricalGearSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSteadyStateSynchronousResponse',)


class CylindricalGearSteadyStateSynchronousResponse(_3270.GearSteadyStateSynchronousResponse):
    '''CylindricalGearSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2238.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2238.CylindricalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6548.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6548.CylindricalGearLoadCase.TYPE not in self.wrapped.ComponentLoadCase.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to CylindricalGearLoadCase. Expected: {}.'.format(self.wrapped.ComponentLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentLoadCase.__class__)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def planetaries(self) -> 'List[CylindricalGearSteadyStateSynchronousResponse]':
        '''List[CylindricalGearSteadyStateSynchronousResponse]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearSteadyStateSynchronousResponse))
        return value
