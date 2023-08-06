'''_4107.py

RingPinsParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2283
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6634
from mastapy.system_model.analyses_and_results.system_deflections import _2502
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4085
from mastapy._internal.python_net import python_net_import

_RING_PINS_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'RingPinsParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsParametricStudyTool',)


class RingPinsParametricStudyTool(_4085.MountableComponentParametricStudyTool):
    '''RingPinsParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2283.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2283.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6634.RingPinsLoadCase':
        '''RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6634.RingPinsLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2502.RingPinsSystemDeflection]':
        '''List[RingPinsSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2502.RingPinsSystemDeflection))
        return value
