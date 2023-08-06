'''_1677.py

LoadedBearingResults
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results import _1688
from mastapy.math_utility.measured_vectors import _1347
from mastapy.bearings.bearing_designs import (
    _1853, _1854, _1855, _1856,
    _1857
)
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_designs.rolling import (
    _1858, _1859, _1860, _1861,
    _1862, _1863, _1865, _1870,
    _1871, _1872, _1874, _1879,
    _1880, _1881, _1882, _1885,
    _1886, _1889, _1890, _1891,
    _1892, _1893, _1894
)
from mastapy.bearings.bearing_designs.fluid_film import (
    _1907, _1909, _1911, _1913,
    _1914, _1915
)
from mastapy.bearings.bearing_designs.concept import _1917, _1918, _1919
from mastapy.bearings.bearing_results.rolling import _1792
from mastapy.bearings import _1608
from mastapy._internal.python_net import python_net_import

_LOADED_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBearingResults',)


class LoadedBearingResults(_1608.BearingLoadCaseResultsLightweight):
    '''LoadedBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle_of_gravity_from_z_axis(self) -> 'float':
        '''float: 'AngleOfGravityFromZAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngleOfGravityFromZAxis

    @property
    def signed_relative_angular_velocity(self) -> 'float':
        '''float: 'SignedRelativeAngularVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SignedRelativeAngularVelocity

    @property
    def relative_angular_velocity(self) -> 'float':
        '''float: 'RelativeAngularVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeAngularVelocity

    @property
    def inner_ring_angular_velocity(self) -> 'float':
        '''float: 'InnerRingAngularVelocity' is the original name of this property.'''

        return self.wrapped.InnerRingAngularVelocity

    @inner_ring_angular_velocity.setter
    def inner_ring_angular_velocity(self, value: 'float'):
        self.wrapped.InnerRingAngularVelocity = float(value) if value else 0.0

    @property
    def outer_ring_angular_velocity(self) -> 'float':
        '''float: 'OuterRingAngularVelocity' is the original name of this property.'''

        return self.wrapped.OuterRingAngularVelocity

    @outer_ring_angular_velocity.setter
    def outer_ring_angular_velocity(self, value: 'float'):
        self.wrapped.OuterRingAngularVelocity = float(value) if value else 0.0

    @property
    def duration(self) -> 'float':
        '''float: 'Duration' is the original name of this property.'''

        return self.wrapped.Duration

    @duration.setter
    def duration(self, value: 'float'):
        self.wrapped.Duration = float(value) if value else 0.0

    @property
    def orientation(self) -> '_1688.Orientations':
        '''Orientations: 'Orientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Orientation)
        return constructor.new(_1688.Orientations)(value) if value is not None else None

    @orientation.setter
    def orientation(self, value: '_1688.Orientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def specified_radial_internal_clearance(self) -> 'float':
        '''float: 'SpecifiedRadialInternalClearance' is the original name of this property.'''

        return self.wrapped.SpecifiedRadialInternalClearance

    @specified_radial_internal_clearance.setter
    def specified_radial_internal_clearance(self, value: 'float'):
        self.wrapped.SpecifiedRadialInternalClearance = float(value) if value else 0.0

    @property
    def specified_axial_internal_clearance(self) -> 'float':
        '''float: 'SpecifiedAxialInternalClearance' is the original name of this property.'''

        return self.wrapped.SpecifiedAxialInternalClearance

    @specified_axial_internal_clearance.setter
    def specified_axial_internal_clearance(self, value: 'float'):
        self.wrapped.SpecifiedAxialInternalClearance = float(value) if value else 0.0

    @property
    def axial_displacement_preload(self) -> 'float':
        '''float: 'AxialDisplacementPreload' is the original name of this property.'''

        return self.wrapped.AxialDisplacementPreload

    @axial_displacement_preload.setter
    def axial_displacement_preload(self, value: 'float'):
        self.wrapped.AxialDisplacementPreload = float(value) if value else 0.0

    @property
    def force_results_are_overridden(self) -> 'bool':
        '''bool: 'ForceResultsAreOverridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceResultsAreOverridden

    @property
    def relative_axial_displacement(self) -> 'float':
        '''float: 'RelativeAxialDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeAxialDisplacement

    @property
    def relative_radial_displacement(self) -> 'float':
        '''float: 'RelativeRadialDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeRadialDisplacement

    @property
    def force_on_inner_race(self) -> '_1347.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'ForceOnInnerRace' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1347.VectorWithLinearAndAngularComponents)(self.wrapped.ForceOnInnerRace) if self.wrapped.ForceOnInnerRace is not None else None

    @property
    def bearing(self) -> '_1853.BearingDesign':
        '''BearingDesign: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1853.BearingDesign.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to BearingDesign. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_detailed_bearing(self) -> '_1854.DetailedBearing':
        '''DetailedBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1854.DetailedBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to DetailedBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_dummy_rolling_bearing(self) -> '_1855.DummyRollingBearing':
        '''DummyRollingBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1855.DummyRollingBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to DummyRollingBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_linear_bearing(self) -> '_1856.LinearBearing':
        '''LinearBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1856.LinearBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to LinearBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_non_linear_bearing(self) -> '_1857.NonLinearBearing':
        '''NonLinearBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1857.NonLinearBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to NonLinearBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_angular_contact_ball_bearing(self) -> '_1858.AngularContactBallBearing':
        '''AngularContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1858.AngularContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AngularContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_angular_contact_thrust_ball_bearing(self) -> '_1859.AngularContactThrustBallBearing':
        '''AngularContactThrustBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1859.AngularContactThrustBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AngularContactThrustBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_asymmetric_spherical_roller_bearing(self) -> '_1860.AsymmetricSphericalRollerBearing':
        '''AsymmetricSphericalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1860.AsymmetricSphericalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AsymmetricSphericalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_axial_thrust_cylindrical_roller_bearing(self) -> '_1861.AxialThrustCylindricalRollerBearing':
        '''AxialThrustCylindricalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1861.AxialThrustCylindricalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AxialThrustCylindricalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_axial_thrust_needle_roller_bearing(self) -> '_1862.AxialThrustNeedleRollerBearing':
        '''AxialThrustNeedleRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1862.AxialThrustNeedleRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AxialThrustNeedleRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_ball_bearing(self) -> '_1863.BallBearing':
        '''BallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1863.BallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to BallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_barrel_roller_bearing(self) -> '_1865.BarrelRollerBearing':
        '''BarrelRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1865.BarrelRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to BarrelRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_crossed_roller_bearing(self) -> '_1870.CrossedRollerBearing':
        '''CrossedRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1870.CrossedRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to CrossedRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_cylindrical_roller_bearing(self) -> '_1871.CylindricalRollerBearing':
        '''CylindricalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1871.CylindricalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to CylindricalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_deep_groove_ball_bearing(self) -> '_1872.DeepGrooveBallBearing':
        '''DeepGrooveBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1872.DeepGrooveBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to DeepGrooveBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_four_point_contact_ball_bearing(self) -> '_1874.FourPointContactBallBearing':
        '''FourPointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1874.FourPointContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to FourPointContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_multi_point_contact_ball_bearing(self) -> '_1879.MultiPointContactBallBearing':
        '''MultiPointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1879.MultiPointContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to MultiPointContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_needle_roller_bearing(self) -> '_1880.NeedleRollerBearing':
        '''NeedleRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1880.NeedleRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to NeedleRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_non_barrel_roller_bearing(self) -> '_1881.NonBarrelRollerBearing':
        '''NonBarrelRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1881.NonBarrelRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to NonBarrelRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_roller_bearing(self) -> '_1882.RollerBearing':
        '''RollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1882.RollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to RollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_rolling_bearing(self) -> '_1885.RollingBearing':
        '''RollingBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1885.RollingBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to RollingBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_self_aligning_ball_bearing(self) -> '_1886.SelfAligningBallBearing':
        '''SelfAligningBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1886.SelfAligningBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to SelfAligningBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_spherical_roller_bearing(self) -> '_1889.SphericalRollerBearing':
        '''SphericalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1889.SphericalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to SphericalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_spherical_roller_thrust_bearing(self) -> '_1890.SphericalRollerThrustBearing':
        '''SphericalRollerThrustBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1890.SphericalRollerThrustBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to SphericalRollerThrustBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_taper_roller_bearing(self) -> '_1891.TaperRollerBearing':
        '''TaperRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1891.TaperRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to TaperRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_three_point_contact_ball_bearing(self) -> '_1892.ThreePointContactBallBearing':
        '''ThreePointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1892.ThreePointContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ThreePointContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_thrust_ball_bearing(self) -> '_1893.ThrustBallBearing':
        '''ThrustBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1893.ThrustBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ThrustBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_toroidal_roller_bearing(self) -> '_1894.ToroidalRollerBearing':
        '''ToroidalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1894.ToroidalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ToroidalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_pad_fluid_film_bearing(self) -> '_1907.PadFluidFilmBearing':
        '''PadFluidFilmBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1907.PadFluidFilmBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PadFluidFilmBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_plain_grease_filled_journal_bearing(self) -> '_1909.PlainGreaseFilledJournalBearing':
        '''PlainGreaseFilledJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1909.PlainGreaseFilledJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainGreaseFilledJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_plain_journal_bearing(self) -> '_1911.PlainJournalBearing':
        '''PlainJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1911.PlainJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_plain_oil_fed_journal_bearing(self) -> '_1913.PlainOilFedJournalBearing':
        '''PlainOilFedJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1913.PlainOilFedJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainOilFedJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_tilting_pad_journal_bearing(self) -> '_1914.TiltingPadJournalBearing':
        '''TiltingPadJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1914.TiltingPadJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to TiltingPadJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_tilting_pad_thrust_bearing(self) -> '_1915.TiltingPadThrustBearing':
        '''TiltingPadThrustBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1915.TiltingPadThrustBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to TiltingPadThrustBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_concept_axial_clearance_bearing(self) -> '_1917.ConceptAxialClearanceBearing':
        '''ConceptAxialClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1917.ConceptAxialClearanceBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptAxialClearanceBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_concept_clearance_bearing(self) -> '_1918.ConceptClearanceBearing':
        '''ConceptClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1918.ConceptClearanceBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptClearanceBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def bearing_of_type_concept_radial_clearance_bearing(self) -> '_1919.ConceptRadialClearanceBearing':
        '''ConceptRadialClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1919.ConceptRadialClearanceBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptRadialClearanceBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing is not None else None

    @property
    def ring_results(self) -> 'List[_1792.RingForceAndDisplacement]':
        '''List[RingForceAndDisplacement]: 'RingResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingResults, constructor.new(_1792.RingForceAndDisplacement))
        return value
