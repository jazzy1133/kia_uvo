"""Tests for the climate preset and the token-check auth counter."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed
from hyundai_kia_connect_api import ClimateRequestOptions, Vehicle
from hyundai_kia_connect_api.exceptions import (
    AuthenticationInvalidCredentialsError,
    AuthenticationTokenExpiredError,
)
import pytest

from custom_components.kia_uvo.button import BUTTON_DESCRIPTIONS
from custom_components.kia_uvo.coordinator import (
    HyundaiKiaConnectDataUpdateCoordinator,
)


def _coordinator(options: dict[str, Any] | None = None, unit: str = "C"):
    coordinator = HyundaiKiaConnectDataUpdateCoordinator.__new__(
        HyundaiKiaConnectDataUpdateCoordinator
    )
    coordinator._config_options = options or {}
    coordinator._consecutive_auth_failures = 0
    coordinator.scan_interval = 1800
    coordinator.force_refresh_interval = 86400
    coordinator.no_force_refresh_hour_start = 22
    coordinator.no_force_refresh_hour_finish = 7
    vehicle = SimpleNamespace(id="v1", _air_temperature_unit=unit)
    coordinator.vehicle_manager = SimpleNamespace(vehicles={"v1": vehicle})
    return coordinator


def test_preset_defaults_celsius() -> None:
    """The shipped preset is the winter start: 10 min, max heat, all on."""
    preset = _coordinator().climate_preset_options("v1")
    assert preset.duration == 10
    assert preset.set_temp == 30
    assert preset.climate is True
    assert preset.defrost is True
    assert preset.heating == 4
    assert preset.steering_wheel == 2
    assert preset.front_left_seat == 8
    assert preset.front_right_seat == 8
    assert preset.rear_left_seat is None
    assert preset.rear_right_seat is None


def test_preset_defaults_fahrenheit() -> None:
    """A Fahrenheit vehicle gets 82, not a blind 30."""
    preset = _coordinator(unit="F").climate_preset_options("v1")
    assert preset.set_temp == 82


def test_preset_options_override_defaults() -> None:
    """Configured options win over the defaults, rear seats included."""
    preset = _coordinator(
        {
            "climate_preset_duration": 15,
            "climate_preset_temperature": 22.0,
            "climate_preset_defrost": False,
            "climate_preset_rear_left_seat": 6,
        }
    ).climate_preset_options("v1")
    assert preset.duration == 15
    assert preset.set_temp == 22
    assert preset.defrost is False
    assert preset.rear_left_seat == 6


async def test_first_token_deleted_is_transient_second_prompts_reauth() -> None:
    """First AuthenticationError from the token check retries, second escalates."""
    coordinator = _coordinator()
    coordinator.async_check_and_refresh_token = AsyncMock(  # type: ignore[method-assign]
        side_effect=AuthenticationTokenExpiredError("Access token is deleted")
    )

    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()
    with pytest.raises(ConfigEntryAuthFailed):
        await coordinator._async_update_data()


async def test_invalid_credentials_prompt_reauth_immediately() -> None:
    """Bad credentials are not retried: re-auth on the first failure."""
    coordinator = _coordinator()
    coordinator.async_check_and_refresh_token = AsyncMock(  # type: ignore[method-assign]
        side_effect=AuthenticationInvalidCredentialsError("7404")
    )

    with pytest.raises(ConfigEntryAuthFailed):
        await coordinator._async_update_data()


def test_winter_start_button_description() -> None:
    """The Winter Start button exists and starts climate with the preset."""
    descriptions = {d.key: d for d in BUTTON_DESCRIPTIONS}
    assert "winter_start" in descriptions
    assert descriptions["winter_start"].press_action == "async_start_climate_preset"
    vehicle = Vehicle(id="v1", name="test", model="test")
    vehicle.air_control_is_on = False
    assert descriptions["winter_start"].exists_fn(vehicle) is True


async def test_climate_entity_seeds_preset_fields() -> None:
    """Turning the climate entity on carries preset duration/seats/steering."""
    from custom_components.kia_uvo.climate import HyundaiKiaCarClimateControlSwitch
    from homeassistant.components.climate.const import HVACMode

    vehicle = Vehicle(id="v1", name="test", model="test")
    vehicle.air_control_is_on = False
    vehicle.air_temperature = (21, "C")
    vehicle.defrost_is_on = False
    vehicle.steering_wheel_heater_is_on = False
    vehicle.back_window_heater_is_on = False

    coordinator = MagicMock()
    coordinator.climate_preset_options.return_value = ClimateRequestOptions(
        duration=10,
        set_temp=30.0,
        climate=True,
        defrost=True,
        heating=4,
        steering_wheel=2,
        front_left_seat=8,
        front_right_seat=8,
    )
    coordinator.async_start_climate = AsyncMock()
    coordinator.async_stop_climate = AsyncMock()

    entity = HyundaiKiaCarClimateControlSwitch(coordinator, vehicle)
    entity.hass = MagicMock()
    entity.async_write_ha_state = MagicMock()

    await entity.async_set_hvac_mode(HVACMode.AUTO)

    _vehicle_id, options = coordinator.async_start_climate.call_args.args
    assert options.duration == 10
    assert options.defrost is True
    assert options.heating == 4
    assert options.steering_wheel == 2
    assert options.front_left_seat == 8
    assert options.front_right_seat == 8
    # The vehicle's own setpoint still wins over the preset temperature.
    assert options.set_temp == 21
