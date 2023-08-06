'''_5634.py

ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2267
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5632, _5633, _5524
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5505
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5524.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2267.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2267.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2267.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2267.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def zerol_bevel_gears_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5632.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation]: 'ZerolBevelGearsCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5632.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def zerol_bevel_meshes_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5633.ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'ZerolBevelMeshesCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5633.ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5505.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5505.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5505.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5505.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value
