'''_1921.py

MastaSettings
'''


from mastapy.bearings.bearing_results.rolling import _1702
from mastapy._internal import constructor
from mastapy.bearings import _1612, _1624
from mastapy.bolts import _1251, _1253, _1258
from mastapy.cycloidal import _1240, _1246
from mastapy.gears import _281, _282, _308
from mastapy.gears.gear_designs.cylindrical import (
    _951, _955, _956, _957
)
from mastapy.gears.gear_designs import _885, _891
from mastapy.gears.gear_set_pareto_optimiser import (
    _863, _864, _867, _868,
    _870, _871, _873, _874,
    _876, _877, _878, _879
)
from mastapy.gears.ltca.cylindrical import _798
from mastapy.gears.manufacturing.bevel import _754
from mastapy.gears.manufacturing.cylindrical.cutters import (
    _677, _683, _688, _689
)
from mastapy.gears.manufacturing.cylindrical import _569, _580
from mastapy.gears.materials import (
    _540, _542, _543, _544,
    _547, _550, _553, _554,
    _561
)
from mastapy.gears.rating.cylindrical import _424, _431
from mastapy.materials import (
    _218, _219, _238, _241
)
from mastapy.nodal_analysis import _45, _46, _64
from mastapy.nodal_analysis.geometry_modeller_link import _148
from mastapy.shafts import _25, _37
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6271
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5716
from mastapy.system_model.analyses_and_results.mbd_analyses import _5159
from mastapy.system_model.analyses_and_results.modal_analyses import _4873
from mastapy.system_model.analyses_and_results.power_flows import _3827, _3785
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _3577
from mastapy.system_model.analyses_and_results.static_loads import _6559
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3316
from mastapy.system_model.analyses_and_results.system_deflections import _2534
from mastapy.system_model.drawing import _1966
from mastapy.system_model.optimization import _1946, _1955
from mastapy.system_model.part_model.gears.supercharger_rotor_set import _2277
from mastapy.system_model.part_model import _2184
from mastapy.utility.cad_export import _1582
from mastapy.utility.databases import _1577
from mastapy.utility import _1373, _1374
from mastapy.utility.scripting import _1497
from mastapy.utility.units_and_measurements import _1383
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MASTA_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel', 'MastaSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('MastaSettings',)


class MastaSettings(_0.APIBase):
    '''MastaSettings

    This is a mastapy class.
    '''

    TYPE = _MASTA_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MastaSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def iso14179_settings_database(self) -> '_1702.ISO14179SettingsDatabase':
        '''ISO14179SettingsDatabase: 'ISO14179SettingsDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1702.ISO14179SettingsDatabase)(self.wrapped.ISO14179SettingsDatabase) if self.wrapped.ISO14179SettingsDatabase is not None else None

    @property
    def bearing_settings(self) -> '_1612.BearingSettings':
        '''BearingSettings: 'BearingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1612.BearingSettings)(self.wrapped.BearingSettings) if self.wrapped.BearingSettings is not None else None

    @property
    def rolling_bearing_database(self) -> '_1624.RollingBearingDatabase':
        '''RollingBearingDatabase: 'RollingBearingDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1624.RollingBearingDatabase)(self.wrapped.RollingBearingDatabase) if self.wrapped.RollingBearingDatabase is not None else None

    @property
    def bolt_geometry_database(self) -> '_1251.BoltGeometryDatabase':
        '''BoltGeometryDatabase: 'BoltGeometryDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1251.BoltGeometryDatabase)(self.wrapped.BoltGeometryDatabase) if self.wrapped.BoltGeometryDatabase is not None else None

    @property
    def bolt_material_database(self) -> '_1253.BoltMaterialDatabase':
        '''BoltMaterialDatabase: 'BoltMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1253.BoltMaterialDatabase)(self.wrapped.BoltMaterialDatabase) if self.wrapped.BoltMaterialDatabase is not None else None

    @property
    def clamped_section_material_database(self) -> '_1258.ClampedSectionMaterialDatabase':
        '''ClampedSectionMaterialDatabase: 'ClampedSectionMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1258.ClampedSectionMaterialDatabase)(self.wrapped.ClampedSectionMaterialDatabase) if self.wrapped.ClampedSectionMaterialDatabase is not None else None

    @property
    def cycloidal_disc_material_database(self) -> '_1240.CycloidalDiscMaterialDatabase':
        '''CycloidalDiscMaterialDatabase: 'CycloidalDiscMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1240.CycloidalDiscMaterialDatabase)(self.wrapped.CycloidalDiscMaterialDatabase) if self.wrapped.CycloidalDiscMaterialDatabase is not None else None

    @property
    def ring_pins_material_database(self) -> '_1246.RingPinsMaterialDatabase':
        '''RingPinsMaterialDatabase: 'RingPinsMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1246.RingPinsMaterialDatabase)(self.wrapped.RingPinsMaterialDatabase) if self.wrapped.RingPinsMaterialDatabase is not None else None

    @property
    def bevel_hypoid_gear_design_settings(self) -> '_281.BevelHypoidGearDesignSettings':
        '''BevelHypoidGearDesignSettings: 'BevelHypoidGearDesignSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_281.BevelHypoidGearDesignSettings)(self.wrapped.BevelHypoidGearDesignSettings) if self.wrapped.BevelHypoidGearDesignSettings is not None else None

    @property
    def bevel_hypoid_gear_rating_settings(self) -> '_282.BevelHypoidGearRatingSettings':
        '''BevelHypoidGearRatingSettings: 'BevelHypoidGearRatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_282.BevelHypoidGearRatingSettings)(self.wrapped.BevelHypoidGearRatingSettings) if self.wrapped.BevelHypoidGearRatingSettings is not None else None

    @property
    def cylindrical_gear_defaults(self) -> '_951.CylindricalGearDefaults':
        '''CylindricalGearDefaults: 'CylindricalGearDefaults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_951.CylindricalGearDefaults)(self.wrapped.CylindricalGearDefaults) if self.wrapped.CylindricalGearDefaults is not None else None

    @property
    def cylindrical_gear_design_constraints_database(self) -> '_955.CylindricalGearDesignConstraintsDatabase':
        '''CylindricalGearDesignConstraintsDatabase: 'CylindricalGearDesignConstraintsDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_955.CylindricalGearDesignConstraintsDatabase)(self.wrapped.CylindricalGearDesignConstraintsDatabase) if self.wrapped.CylindricalGearDesignConstraintsDatabase is not None else None

    @property
    def cylindrical_gear_design_constraint_settings(self) -> '_956.CylindricalGearDesignConstraintSettings':
        '''CylindricalGearDesignConstraintSettings: 'CylindricalGearDesignConstraintSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_956.CylindricalGearDesignConstraintSettings)(self.wrapped.CylindricalGearDesignConstraintSettings) if self.wrapped.CylindricalGearDesignConstraintSettings is not None else None

    @property
    def cylindrical_gear_design_settings(self) -> '_957.CylindricalGearDesignSettings':
        '''CylindricalGearDesignSettings: 'CylindricalGearDesignSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_957.CylindricalGearDesignSettings)(self.wrapped.CylindricalGearDesignSettings) if self.wrapped.CylindricalGearDesignSettings is not None else None

    @property
    def design_constraint_collection_database(self) -> '_885.DesignConstraintCollectionDatabase':
        '''DesignConstraintCollectionDatabase: 'DesignConstraintCollectionDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_885.DesignConstraintCollectionDatabase)(self.wrapped.DesignConstraintCollectionDatabase) if self.wrapped.DesignConstraintCollectionDatabase is not None else None

    @property
    def selected_design_constraints_collection(self) -> '_891.SelectedDesignConstraintsCollection':
        '''SelectedDesignConstraintsCollection: 'SelectedDesignConstraintsCollection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_891.SelectedDesignConstraintsCollection)(self.wrapped.SelectedDesignConstraintsCollection) if self.wrapped.SelectedDesignConstraintsCollection is not None else None

    @property
    def micro_geometry_gear_set_design_space_search_strategy_database(self) -> '_863.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase':
        '''MicroGeometryGearSetDesignSpaceSearchStrategyDatabase: 'MicroGeometryGearSetDesignSpaceSearchStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_863.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase)(self.wrapped.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase) if self.wrapped.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase is not None else None

    @property
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(self) -> '_864.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase':
        '''MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase: 'MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_864.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase)(self.wrapped.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase) if self.wrapped.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase is not None else None

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_867.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_867.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase is not None else None

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(self) -> '_868.ParetoCylindricalGearSetOptimisationStrategyDatabase':
        '''ParetoCylindricalGearSetOptimisationStrategyDatabase: 'ParetoCylindricalGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_868.ParetoCylindricalGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoCylindricalGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoCylindricalGearSetOptimisationStrategyDatabase is not None else None

    @property
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_870.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_870.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase is not None else None

    @property
    def pareto_face_gear_set_optimisation_strategy_database(self) -> '_871.ParetoFaceGearSetOptimisationStrategyDatabase':
        '''ParetoFaceGearSetOptimisationStrategyDatabase: 'ParetoFaceGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_871.ParetoFaceGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoFaceGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoFaceGearSetOptimisationStrategyDatabase is not None else None

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_873.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_873.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase is not None else None

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(self) -> '_874.ParetoHypoidGearSetOptimisationStrategyDatabase':
        '''ParetoHypoidGearSetOptimisationStrategyDatabase: 'ParetoHypoidGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_874.ParetoHypoidGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoHypoidGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoHypoidGearSetOptimisationStrategyDatabase is not None else None

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_876.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_876.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase is not None else None

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(self) -> '_877.ParetoSpiralBevelGearSetOptimisationStrategyDatabase':
        '''ParetoSpiralBevelGearSetOptimisationStrategyDatabase: 'ParetoSpiralBevelGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_877.ParetoSpiralBevelGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoSpiralBevelGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoSpiralBevelGearSetOptimisationStrategyDatabase is not None else None

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_878.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_878.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase is not None else None

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(self) -> '_879.ParetoStraightBevelGearSetOptimisationStrategyDatabase':
        '''ParetoStraightBevelGearSetOptimisationStrategyDatabase: 'ParetoStraightBevelGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_879.ParetoStraightBevelGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoStraightBevelGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoStraightBevelGearSetOptimisationStrategyDatabase is not None else None

    @property
    def cylindrical_gear_fe_settings(self) -> '_798.CylindricalGearFESettings':
        '''CylindricalGearFESettings: 'CylindricalGearFESettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_798.CylindricalGearFESettings)(self.wrapped.CylindricalGearFESettings) if self.wrapped.CylindricalGearFESettings is not None else None

    @property
    def manufacturing_machine_database(self) -> '_754.ManufacturingMachineDatabase':
        '''ManufacturingMachineDatabase: 'ManufacturingMachineDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_754.ManufacturingMachineDatabase)(self.wrapped.ManufacturingMachineDatabase) if self.wrapped.ManufacturingMachineDatabase is not None else None

    @property
    def cylindrical_formed_wheel_grinder_database(self) -> '_677.CylindricalFormedWheelGrinderDatabase':
        '''CylindricalFormedWheelGrinderDatabase: 'CylindricalFormedWheelGrinderDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_677.CylindricalFormedWheelGrinderDatabase)(self.wrapped.CylindricalFormedWheelGrinderDatabase) if self.wrapped.CylindricalFormedWheelGrinderDatabase is not None else None

    @property
    def cylindrical_gear_plunge_shaver_database(self) -> '_683.CylindricalGearPlungeShaverDatabase':
        '''CylindricalGearPlungeShaverDatabase: 'CylindricalGearPlungeShaverDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_683.CylindricalGearPlungeShaverDatabase)(self.wrapped.CylindricalGearPlungeShaverDatabase) if self.wrapped.CylindricalGearPlungeShaverDatabase is not None else None

    @property
    def cylindrical_gear_shaver_database(self) -> '_688.CylindricalGearShaverDatabase':
        '''CylindricalGearShaverDatabase: 'CylindricalGearShaverDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_688.CylindricalGearShaverDatabase)(self.wrapped.CylindricalGearShaverDatabase) if self.wrapped.CylindricalGearShaverDatabase is not None else None

    @property
    def cylindrical_worm_grinder_database(self) -> '_689.CylindricalWormGrinderDatabase':
        '''CylindricalWormGrinderDatabase: 'CylindricalWormGrinderDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_689.CylindricalWormGrinderDatabase)(self.wrapped.CylindricalWormGrinderDatabase) if self.wrapped.CylindricalWormGrinderDatabase is not None else None

    @property
    def cylindrical_hob_database(self) -> '_569.CylindricalHobDatabase':
        '''CylindricalHobDatabase: 'CylindricalHobDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_569.CylindricalHobDatabase)(self.wrapped.CylindricalHobDatabase) if self.wrapped.CylindricalHobDatabase is not None else None

    @property
    def cylindrical_shaper_database(self) -> '_580.CylindricalShaperDatabase':
        '''CylindricalShaperDatabase: 'CylindricalShaperDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_580.CylindricalShaperDatabase)(self.wrapped.CylindricalShaperDatabase) if self.wrapped.CylindricalShaperDatabase is not None else None

    @property
    def bevel_gear_iso_material_database(self) -> '_540.BevelGearIsoMaterialDatabase':
        '''BevelGearIsoMaterialDatabase: 'BevelGearIsoMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_540.BevelGearIsoMaterialDatabase)(self.wrapped.BevelGearIsoMaterialDatabase) if self.wrapped.BevelGearIsoMaterialDatabase is not None else None

    @property
    def bevel_gear_material_database(self) -> '_542.BevelGearMaterialDatabase':
        '''BevelGearMaterialDatabase: 'BevelGearMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_542.BevelGearMaterialDatabase)(self.wrapped.BevelGearMaterialDatabase) if self.wrapped.BevelGearMaterialDatabase is not None else None

    @property
    def cylindrical_gear_agma_material_database(self) -> '_543.CylindricalGearAGMAMaterialDatabase':
        '''CylindricalGearAGMAMaterialDatabase: 'CylindricalGearAGMAMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_543.CylindricalGearAGMAMaterialDatabase)(self.wrapped.CylindricalGearAGMAMaterialDatabase) if self.wrapped.CylindricalGearAGMAMaterialDatabase is not None else None

    @property
    def cylindrical_gear_iso_material_database(self) -> '_544.CylindricalGearISOMaterialDatabase':
        '''CylindricalGearISOMaterialDatabase: 'CylindricalGearISOMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_544.CylindricalGearISOMaterialDatabase)(self.wrapped.CylindricalGearISOMaterialDatabase) if self.wrapped.CylindricalGearISOMaterialDatabase is not None else None

    @property
    def cylindrical_gear_plastic_material_database(self) -> '_547.CylindricalGearPlasticMaterialDatabase':
        '''CylindricalGearPlasticMaterialDatabase: 'CylindricalGearPlasticMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_547.CylindricalGearPlasticMaterialDatabase)(self.wrapped.CylindricalGearPlasticMaterialDatabase) if self.wrapped.CylindricalGearPlasticMaterialDatabase is not None else None

    @property
    def gear_material_expert_system_factor_settings(self) -> '_550.GearMaterialExpertSystemFactorSettings':
        '''GearMaterialExpertSystemFactorSettings: 'GearMaterialExpertSystemFactorSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_550.GearMaterialExpertSystemFactorSettings)(self.wrapped.GearMaterialExpertSystemFactorSettings) if self.wrapped.GearMaterialExpertSystemFactorSettings is not None else None

    @property
    def isotr1417912001_coefficient_of_friction_constants_database(self) -> '_553.ISOTR1417912001CoefficientOfFrictionConstantsDatabase':
        '''ISOTR1417912001CoefficientOfFrictionConstantsDatabase: 'ISOTR1417912001CoefficientOfFrictionConstantsDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_553.ISOTR1417912001CoefficientOfFrictionConstantsDatabase)(self.wrapped.ISOTR1417912001CoefficientOfFrictionConstantsDatabase) if self.wrapped.ISOTR1417912001CoefficientOfFrictionConstantsDatabase is not None else None

    @property
    def klingelnberg_conical_gear_material_database(self) -> '_554.KlingelnbergConicalGearMaterialDatabase':
        '''KlingelnbergConicalGearMaterialDatabase: 'KlingelnbergConicalGearMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_554.KlingelnbergConicalGearMaterialDatabase)(self.wrapped.KlingelnbergConicalGearMaterialDatabase) if self.wrapped.KlingelnbergConicalGearMaterialDatabase is not None else None

    @property
    def raw_material_database(self) -> '_561.RawMaterialDatabase':
        '''RawMaterialDatabase: 'RawMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_561.RawMaterialDatabase)(self.wrapped.RawMaterialDatabase) if self.wrapped.RawMaterialDatabase is not None else None

    @property
    def pocketing_power_loss_coefficients_database(self) -> '_308.PocketingPowerLossCoefficientsDatabase':
        '''PocketingPowerLossCoefficientsDatabase: 'PocketingPowerLossCoefficientsDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_308.PocketingPowerLossCoefficientsDatabase)(self.wrapped.PocketingPowerLossCoefficientsDatabase) if self.wrapped.PocketingPowerLossCoefficientsDatabase is not None else None

    @property
    def cylindrical_gear_rating_settings(self) -> '_424.CylindricalGearRatingSettings':
        '''CylindricalGearRatingSettings: 'CylindricalGearRatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_424.CylindricalGearRatingSettings)(self.wrapped.CylindricalGearRatingSettings) if self.wrapped.CylindricalGearRatingSettings is not None else None

    @property
    def cylindrical_plastic_gear_rating_settings(self) -> '_431.CylindricalPlasticGearRatingSettings':
        '''CylindricalPlasticGearRatingSettings: 'CylindricalPlasticGearRatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_431.CylindricalPlasticGearRatingSettings)(self.wrapped.CylindricalPlasticGearRatingSettings) if self.wrapped.CylindricalPlasticGearRatingSettings is not None else None

    @property
    def bearing_material_database(self) -> '_218.BearingMaterialDatabase':
        '''BearingMaterialDatabase: 'BearingMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_218.BearingMaterialDatabase)(self.wrapped.BearingMaterialDatabase) if self.wrapped.BearingMaterialDatabase is not None else None

    @property
    def component_material_database(self) -> '_219.ComponentMaterialDatabase':
        '''ComponentMaterialDatabase: 'ComponentMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_219.ComponentMaterialDatabase)(self.wrapped.ComponentMaterialDatabase) if self.wrapped.ComponentMaterialDatabase is not None else None

    @property
    def lubrication_detail_database(self) -> '_238.LubricationDetailDatabase':
        '''LubricationDetailDatabase: 'LubricationDetailDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_238.LubricationDetailDatabase)(self.wrapped.LubricationDetailDatabase) if self.wrapped.LubricationDetailDatabase is not None else None

    @property
    def materials_settings(self) -> '_241.MaterialsSettings':
        '''MaterialsSettings: 'MaterialsSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_241.MaterialsSettings)(self.wrapped.MaterialsSettings) if self.wrapped.MaterialsSettings is not None else None

    @property
    def analysis_settings(self) -> '_45.AnalysisSettings':
        '''AnalysisSettings: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_45.AnalysisSettings)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings is not None else None

    @property
    def analysis_settings_database(self) -> '_46.AnalysisSettingsDatabase':
        '''AnalysisSettingsDatabase: 'AnalysisSettingsDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_46.AnalysisSettingsDatabase)(self.wrapped.AnalysisSettingsDatabase) if self.wrapped.AnalysisSettingsDatabase is not None else None

    @property
    def fe_user_settings(self) -> '_64.FEUserSettings':
        '''FEUserSettings: 'FEUserSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_64.FEUserSettings)(self.wrapped.FEUserSettings) if self.wrapped.FEUserSettings is not None else None

    @property
    def geometry_modeller_settings(self) -> '_148.GeometryModellerSettings':
        '''GeometryModellerSettings: 'GeometryModellerSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_148.GeometryModellerSettings)(self.wrapped.GeometryModellerSettings) if self.wrapped.GeometryModellerSettings is not None else None

    @property
    def shaft_material_database(self) -> '_25.ShaftMaterialDatabase':
        '''ShaftMaterialDatabase: 'ShaftMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_25.ShaftMaterialDatabase)(self.wrapped.ShaftMaterialDatabase) if self.wrapped.ShaftMaterialDatabase is not None else None

    @property
    def shaft_settings(self) -> '_37.ShaftSettings':
        '''ShaftSettings: 'ShaftSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_37.ShaftSettings)(self.wrapped.ShaftSettings) if self.wrapped.ShaftSettings is not None else None

    @property
    def critical_speed_analysis_draw_style(self) -> '_6271.CriticalSpeedAnalysisDrawStyle':
        '''CriticalSpeedAnalysisDrawStyle: 'CriticalSpeedAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6271.CriticalSpeedAnalysisDrawStyle)(self.wrapped.CriticalSpeedAnalysisDrawStyle) if self.wrapped.CriticalSpeedAnalysisDrawStyle is not None else None

    @property
    def harmonic_analysis_draw_style(self) -> '_5716.HarmonicAnalysisDrawStyle':
        '''HarmonicAnalysisDrawStyle: 'HarmonicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5716.HarmonicAnalysisDrawStyle)(self.wrapped.HarmonicAnalysisDrawStyle) if self.wrapped.HarmonicAnalysisDrawStyle is not None else None

    @property
    def mbd_analysis_draw_style(self) -> '_5159.MBDAnalysisDrawStyle':
        '''MBDAnalysisDrawStyle: 'MBDAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5159.MBDAnalysisDrawStyle)(self.wrapped.MBDAnalysisDrawStyle) if self.wrapped.MBDAnalysisDrawStyle is not None else None

    @property
    def modal_analysis_draw_style(self) -> '_4873.ModalAnalysisDrawStyle':
        '''ModalAnalysisDrawStyle: 'ModalAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4873.ModalAnalysisDrawStyle)(self.wrapped.ModalAnalysisDrawStyle) if self.wrapped.ModalAnalysisDrawStyle is not None else None

    @property
    def power_flow_draw_style(self) -> '_3827.PowerFlowDrawStyle':
        '''PowerFlowDrawStyle: 'PowerFlowDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3827.PowerFlowDrawStyle.TYPE not in self.wrapped.PowerFlowDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast power_flow_draw_style to PowerFlowDrawStyle. Expected: {}.'.format(self.wrapped.PowerFlowDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowDrawStyle.__class__)(self.wrapped.PowerFlowDrawStyle) if self.wrapped.PowerFlowDrawStyle is not None else None

    @property
    def stability_analysis_draw_style(self) -> '_3577.StabilityAnalysisDrawStyle':
        '''StabilityAnalysisDrawStyle: 'StabilityAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3577.StabilityAnalysisDrawStyle)(self.wrapped.StabilityAnalysisDrawStyle) if self.wrapped.StabilityAnalysisDrawStyle is not None else None

    @property
    def electric_machine_detail_database(self) -> '_6559.ElectricMachineDetailDatabase':
        '''ElectricMachineDetailDatabase: 'ElectricMachineDetailDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6559.ElectricMachineDetailDatabase)(self.wrapped.ElectricMachineDetailDatabase) if self.wrapped.ElectricMachineDetailDatabase is not None else None

    @property
    def steady_state_synchronous_response_draw_style(self) -> '_3316.SteadyStateSynchronousResponseDrawStyle':
        '''SteadyStateSynchronousResponseDrawStyle: 'SteadyStateSynchronousResponseDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3316.SteadyStateSynchronousResponseDrawStyle)(self.wrapped.SteadyStateSynchronousResponseDrawStyle) if self.wrapped.SteadyStateSynchronousResponseDrawStyle is not None else None

    @property
    def system_deflection_draw_style(self) -> '_2534.SystemDeflectionDrawStyle':
        '''SystemDeflectionDrawStyle: 'SystemDeflectionDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2534.SystemDeflectionDrawStyle)(self.wrapped.SystemDeflectionDrawStyle) if self.wrapped.SystemDeflectionDrawStyle is not None else None

    @property
    def model_view_options_draw_style(self) -> '_1966.ModelViewOptionsDrawStyle':
        '''ModelViewOptionsDrawStyle: 'ModelViewOptionsDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.ModelViewOptionsDrawStyle)(self.wrapped.ModelViewOptionsDrawStyle) if self.wrapped.ModelViewOptionsDrawStyle is not None else None

    @property
    def conical_gear_optimization_strategy_database(self) -> '_1946.ConicalGearOptimizationStrategyDatabase':
        '''ConicalGearOptimizationStrategyDatabase: 'ConicalGearOptimizationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1946.ConicalGearOptimizationStrategyDatabase)(self.wrapped.ConicalGearOptimizationStrategyDatabase) if self.wrapped.ConicalGearOptimizationStrategyDatabase is not None else None

    @property
    def optimization_strategy_database(self) -> '_1955.OptimizationStrategyDatabase':
        '''OptimizationStrategyDatabase: 'OptimizationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1955.OptimizationStrategyDatabase)(self.wrapped.OptimizationStrategyDatabase) if self.wrapped.OptimizationStrategyDatabase is not None else None

    @property
    def supercharger_rotor_set_database(self) -> '_2277.SuperchargerRotorSetDatabase':
        '''SuperchargerRotorSetDatabase: 'SuperchargerRotorSetDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.SuperchargerRotorSetDatabase)(self.wrapped.SuperchargerRotorSetDatabase) if self.wrapped.SuperchargerRotorSetDatabase is not None else None

    @property
    def planet_carrier_settings(self) -> '_2184.PlanetCarrierSettings':
        '''PlanetCarrierSettings: 'PlanetCarrierSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2184.PlanetCarrierSettings)(self.wrapped.PlanetCarrierSettings) if self.wrapped.PlanetCarrierSettings is not None else None

    @property
    def cad_export_settings(self) -> '_1582.CADExportSettings':
        '''CADExportSettings: 'CADExportSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1582.CADExportSettings)(self.wrapped.CADExportSettings) if self.wrapped.CADExportSettings is not None else None

    @property
    def database_settings(self) -> '_1577.DatabaseSettings':
        '''DatabaseSettings: 'DatabaseSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1577.DatabaseSettings)(self.wrapped.DatabaseSettings) if self.wrapped.DatabaseSettings is not None else None

    @property
    def program_settings(self) -> '_1373.ProgramSettings':
        '''ProgramSettings: 'ProgramSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1373.ProgramSettings)(self.wrapped.ProgramSettings) if self.wrapped.ProgramSettings is not None else None

    @property
    def pushbullet_settings(self) -> '_1374.PushbulletSettings':
        '''PushbulletSettings: 'PushbulletSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1374.PushbulletSettings)(self.wrapped.PushbulletSettings) if self.wrapped.PushbulletSettings is not None else None

    @property
    def scripting_setup(self) -> '_1497.ScriptingSetup':
        '''ScriptingSetup: 'ScriptingSetup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1497.ScriptingSetup)(self.wrapped.ScriptingSetup) if self.wrapped.ScriptingSetup is not None else None

    @property
    def measurement_settings(self) -> '_1383.MeasurementSettings':
        '''MeasurementSettings: 'MeasurementSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1383.MeasurementSettings)(self.wrapped.MeasurementSettings) if self.wrapped.MeasurementSettings is not None else None
