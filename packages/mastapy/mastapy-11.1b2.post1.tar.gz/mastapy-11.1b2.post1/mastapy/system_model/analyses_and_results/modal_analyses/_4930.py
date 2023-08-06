'''_4930.py

WormGearSetModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2265
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6676
from mastapy.system_model.analyses_and_results.system_deflections import _2545
from mastapy.system_model.analyses_and_results.modal_analyses import _4929, _4928, _4855
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'WormGearSetModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetModalAnalysis',)


class WormGearSetModalAnalysis(_4855.GearSetModalAnalysis):
    '''WormGearSetModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2265.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2265.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6676.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6676.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2545.WormGearSetSystemDeflection':
        '''WormGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2545.WormGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def worm_gears_modal_analysis(self) -> 'List[_4929.WormGearModalAnalysis]':
        '''List[WormGearModalAnalysis]: 'WormGearsModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsModalAnalysis, constructor.new(_4929.WormGearModalAnalysis))
        return value

    @property
    def worm_meshes_modal_analysis(self) -> 'List[_4928.WormGearMeshModalAnalysis]':
        '''List[WormGearMeshModalAnalysis]: 'WormMeshesModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesModalAnalysis, constructor.new(_4928.WormGearMeshModalAnalysis))
        return value
