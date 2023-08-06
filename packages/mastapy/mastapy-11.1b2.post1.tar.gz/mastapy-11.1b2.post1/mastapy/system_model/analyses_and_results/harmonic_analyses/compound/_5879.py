'''_5879.py

DatumCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2163
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5688
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5853
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'DatumCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundHarmonicAnalysis',)


class DatumCompoundHarmonicAnalysis(_5853.ComponentCompoundHarmonicAnalysis):
    '''DatumCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2163.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5688.DatumHarmonicAnalysis]':
        '''List[DatumHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5688.DatumHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5688.DatumHarmonicAnalysis]':
        '''List[DatumHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5688.DatumHarmonicAnalysis))
        return value
