'''_3187.py

StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2259
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3185, _3186, _3098
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3057
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed',)


class StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed(_3098.BevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed):
    '''StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2259.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2259.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def straight_bevel_diff_gears_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3185.StraightBevelDiffGearCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelDiffGearCompoundSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelDiffGearsCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3185.StraightBevelDiffGearCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_diff_meshes_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3186.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelDiffMeshesCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3186.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3057.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3057.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3057.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3057.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed))
        return value
