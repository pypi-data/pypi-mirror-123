'''_4008.py

BearingParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2155
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6507
from mastapy.bearings.bearing_results import _1676
from mastapy.system_model.analyses_and_results.system_deflections import _2406
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4036
from mastapy._internal.python_net import python_net_import

_BEARING_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BearingParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingParametricStudyTool',)


class BearingParametricStudyTool(_4036.ConnectorParametricStudyTool):
    '''BearingParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BEARING_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2155.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2155.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6507.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6507.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def bearing_duty_cycle_results(self) -> 'List[_1676.LoadedBearingDutyCycle]':
        '''List[LoadedBearingDutyCycle]: 'BearingDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BearingDutyCycleResults, constructor.new(_1676.LoadedBearingDutyCycle))
        return value

    @property
    def planetaries(self) -> 'List[BearingParametricStudyTool]':
        '''List[BearingParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingParametricStudyTool))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2406.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2406.BearingSystemDeflection))
        return value
