'''_3995.py

WormGearMeshCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2044
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3865
from mastapy.system_model.analyses_and_results.power_flows.compound import _3930
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'WormGearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshCompoundPowerFlow',)


class WormGearMeshCompoundPowerFlow(_3930.GearMeshCompoundPowerFlow):
    '''WormGearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2044.WormGearMesh':
        '''WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2044.WormGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def connection_design(self) -> '_2044.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2044.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3865.WormGearMeshPowerFlow]':
        '''List[WormGearMeshPowerFlow]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_3865.WormGearMeshPowerFlow))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3865.WormGearMeshPowerFlow]':
        '''List[WormGearMeshPowerFlow]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_3865.WormGearMeshPowerFlow))
        return value
