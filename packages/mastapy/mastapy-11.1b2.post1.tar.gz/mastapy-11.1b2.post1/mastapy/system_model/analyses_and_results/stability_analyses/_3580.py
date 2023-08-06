'''_3580.py

StraightBevelDiffGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2259
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6653
from mastapy.system_model.analyses_and_results.stability_analyses import _3581, _3579, _3488
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'StraightBevelDiffGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetStabilityAnalysis',)


class StraightBevelDiffGearSetStabilityAnalysis(_3488.BevelGearSetStabilityAnalysis):
    '''StraightBevelDiffGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2259.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6653.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6653.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def straight_bevel_diff_gears_stability_analysis(self) -> 'List[_3581.StraightBevelDiffGearStabilityAnalysis]':
        '''List[StraightBevelDiffGearStabilityAnalysis]: 'StraightBevelDiffGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsStabilityAnalysis, constructor.new(_3581.StraightBevelDiffGearStabilityAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_stability_analysis(self) -> 'List[_3579.StraightBevelDiffGearMeshStabilityAnalysis]':
        '''List[StraightBevelDiffGearMeshStabilityAnalysis]: 'StraightBevelDiffMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesStabilityAnalysis, constructor.new(_3579.StraightBevelDiffGearMeshStabilityAnalysis))
        return value
