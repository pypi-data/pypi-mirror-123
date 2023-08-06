'''_2613.py

FaceGearCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2241
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2464
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2618
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'FaceGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundSystemDeflection',)


class FaceGearCompoundSystemDeflection(_2618.GearCompoundSystemDeflection):
    '''FaceGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2241.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2241.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2464.FaceGearSystemDeflection]':
        '''List[FaceGearSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2464.FaceGearSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2464.FaceGearSystemDeflection]':
        '''List[FaceGearSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2464.FaceGearSystemDeflection))
        return value
