"""Constants for the Hyundai / Kia Connect integration."""

from enum import StrEnum

DOMAIN: str = "kia_uvo"

CONF_BRAND: str = "brand"
CONF_FORCE_REFRESH_INTERVAL: str = "force_refresh"
CONF_NO_FORCE_REFRESH_HOUR_START: str = "no_force_refresh_hour_start"
CONF_NO_FORCE_REFRESH_HOUR_FINISH: str = "no_force_refresh_hour_finish"
CONF_ENABLE_GEOLOCATION_ENTITY: str = "enable_geolocation_entity"
CONF_USE_EMAIL_WITH_GEOCODE_API: str = "use_email_with_geocode_api"
CONF_TOKEN: str = "token"
CONF_CLIMATE_PRESET_DURATION: str = "climate_preset_duration"
CONF_CLIMATE_PRESET_TEMPERATURE: str = "climate_preset_temperature"
CONF_CLIMATE_PRESET_DEFROST: str = "climate_preset_defrost"
CONF_CLIMATE_PRESET_HEATING: str = "climate_preset_heating"
CONF_CLIMATE_PRESET_STEERING_WHEEL: str = "climate_preset_steering_wheel"
CONF_CLIMATE_PRESET_FRONT_LEFT_SEAT: str = "climate_preset_front_left_seat"
CONF_CLIMATE_PRESET_FRONT_RIGHT_SEAT: str = "climate_preset_front_right_seat"
CONF_CLIMATE_PRESET_REAR_LEFT_SEAT: str = "climate_preset_rear_left_seat"
CONF_CLIMATE_PRESET_REAR_RIGHT_SEAT: str = "climate_preset_rear_right_seat"

REGION_EUROPE: str = "Europe"
REGION_EUROPE_CCI: str = "Europe (Beta)"
REGION_CANADA: str = "Canada"
REGION_USA: str = "USA"
REGION_CHINA: str = "China"
REGION_AUSTRALIA: str = "Australia"
REGION_INDIA: str = "India"
REGION_NZ: str = "New Zealand"
REGION_BRAZIL: str = "Brazil"
REGIONS = {
    1: REGION_EUROPE,
    2: REGION_CANADA,
    3: REGION_USA,
    4: REGION_CHINA,
    5: REGION_AUSTRALIA,
    6: REGION_INDIA,
    7: REGION_NZ,
    8: REGION_BRAZIL,
    9: REGION_EUROPE_CCI,
}
BRAND_KIA: str = "Kia"
BRAND_HYUNDAI: str = "Hyundai"
BRAND_GENESIS: str = "Genesis"
BRANDS = {1: BRAND_KIA, 2: BRAND_HYUNDAI, 3: BRAND_GENESIS}

CHARGING_CURRENTS = {1: 100, 2: 90, 3: 60}

DEFAULT_PIN: str = ""
DEFAULT_SCAN_INTERVAL: int = 30
DEFAULT_FORCE_REFRESH_INTERVAL: int = 1440
DEFAULT_NO_FORCE_REFRESH_HOUR_START: int = 22
DEFAULT_NO_FORCE_REFRESH_HOUR_FINISH: int = 7
DEFAULT_ENABLE_GEOLOCATION_ENTITY: bool = False
DEFAULT_USE_EMAIL_WITH_GEOCODE_API: bool = False
DEFAULT_CLIMATE_PRESET_DURATION: int = 10
DEFAULT_CLIMATE_PRESET_TEMPERATURE_C: float = 30
DEFAULT_CLIMATE_PRESET_TEMPERATURE_F: float = 82
DEFAULT_CLIMATE_PRESET_DEFROST: bool = True
DEFAULT_CLIMATE_PRESET_HEATING: int = 4
DEFAULT_CLIMATE_PRESET_STEERING_WHEEL: int = 2
DEFAULT_CLIMATE_PRESET_FRONT_SEAT: int = 8
DEFAULT_CLIMATE_PRESET_REAR_SEAT: int = 0

DYNAMIC_UNIT: str = "dynamic_unit"


class OffPeakChargingMode(StrEnum):
    """Off-peak charging schedule mode.

    Maps to the (charging_enabled, off_peak_charge_only_enabled) pair the API
    expects. Values are the strings exposed in services.yaml so the service
    payload converts directly: ``OffPeakChargingMode(call.data["mode"])``.
    """

    OFF = "off"
    TIME = "time"
    TARGET = "target"
