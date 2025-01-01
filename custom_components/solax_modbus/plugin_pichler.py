import logging
from dataclasses import dataclass
from homeassistant.components.number import NumberEntityDescription
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.button import ButtonEntityDescription
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder, Endian
from custom_components.solax_modbus.const import *
from homeassistant.const import *
from time import time

_LOGGER = logging.getLogger(__name__)

LG150 = 0x0100
LG250 = 0x0200
ALL_LG_GROUP = LG150 | LG250

ALLDEFAULT = 0  # should be equivalent to LG150 | LG250

# ======================= end of bitmask handling code =============================================

SENSOR_TYPES = []

# =================================================================================================


@dataclass
class PichlerModbusButtonEntityDescription(BaseModbusButtonEntityDescription):
    allowedtypes: int = ALLDEFAULT  # maybe 0x0000 (nothing) is a better default choice


@dataclass
class PichlerModbusNumberEntityDescription(BaseModbusNumberEntityDescription):
    allowedtypes: int = ALLDEFAULT  # maybe 0x0000 (nothing) is a better default choice


@dataclass
class PichlerModbusSelectEntityDescription(BaseModbusSelectEntityDescription):
    allowedtypes: int = ALLDEFAULT  # maybe 0x0000 (nothing) is a better default choice


@dataclass
class PichlerModbusSensorEntityDescription(BaseModbusSensorEntityDescription):
    allowedtypes: int = ALLDEFAULT  # maybe 0x0000 (nothing) is a better default choice
    # order16: int = Endian.BIG
    # order32: int = Endian.LITTLE
    unit: int = REGISTER_U16
    register_type: int = REG_HOLDING


# ====================================== Computed value functions  =================================================


def value_function_temperature(initval, descr, datadict):
    return round(initval / 10 - 100.0, 1)

def value_function_temperature_inverse(initval, descr, datadict):
    return round((initval + 100.0) * 10, 1)

# def value_function_gen_hours(initval, descr, datadict):
#     return f"{initval:02d}:00"


# def valuefunction_firmware_g3(initval, descr, datadict):
#     return f"3.{initval}"


# def valuefunction_firmware_g4(initval, descr, datadict):
#     return f"1.{initval}"


# def value_function_remotecontrol_autorepeat_remaining(initval, descr, datadict):
#     return autorepeat_remaining(datadict, "remotecontrol_trigger", time())


# ================================= Button Declarations ============================================================

BUTTON_TYPES = [
    PichlerModbusButtonEntityDescription(
        name="Filter Timer Reset",
        key="filter_timer_reset",
        register=33,
        command=1,
        allowedtypes=LG150 | LG250,
        write_method=WRITE_SINGLE_MODBUS,
        icon="mdi:timer-refresh-outline",
    ),
    PichlerModbusButtonEntityDescription(
        name="Filter Timer Snooze",
        key="filter_timer_snooze",
        register=33,
        command=2,
        allowedtypes=LG150 | LG250,
        write_method=WRITE_SINGLE_MODBUS,
        entity_registry_enabled_default=False,
        icon="mdi:timer-refresh-outline",
    ),
]

# ================================= Number Declarations ============================================================


NUMBER_TYPES = [
    ###
    #
    #  Normal number types (holding register)
    #
    ###
    PichlerModbusNumberEntityDescription(
        name="Luftstrom Lüftungsstufe 1",
        key="volumenstrom_luftungsstufe_1",
        register=9,
        fmt="i",
        scale=10,
        native_min_value=30,
        native_max_value=400,
        native_step=1,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan-speed-1",
    ),
    PichlerModbusNumberEntityDescription(
        name="Luftstrom Lüftungsstufe 2",
        key="volumenstrom_luftungsstufe_2",
        register=10,
        fmt="i",
        scale=10,
        native_min_value=30,
        native_max_value=400,
        native_step=1,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan-speed-2",
    ),
    PichlerModbusNumberEntityDescription(
        name="Luftstrom Lüftungsstufe 3",
        key="volumenstrom_luftungsstufe_3",
        register=11,
        fmt="i",
        scale=10,
        native_min_value=30,
        native_max_value=400,
        native_step=1,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan-speed-3",
    ),
    PichlerModbusNumberEntityDescription(
        name="Luftstrom Grundlüftung",
        key="volumenstrom_grundluftung",
        register=12,
        fmt="i",
        scale=10,
        native_min_value=30,
        native_max_value=400,
        native_step=1,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan",
    ),
    PichlerModbusNumberEntityDescription(
        name="Lüftungsstufe 3 Timer",
        key="timer_luftungsstufe_3",
        register=70,
        fmt="i",
        scale=1,
        native_min_value=0,
        native_max_value=65000,
        native_step=1,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan-clock",
    ),
    PichlerModbusNumberEntityDescription(
        name="Soll Zulufttemperatur",
        key="soll_zulufttemperatur",
        register=22,
        fmt="f",
        scale=value_function_temperature_inverse,
        # write_scale=value_function_temperature_inverse,
        native_min_value=-20,
        native_max_value=50,
        native_step=0.1,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        unit=REGISTER_S16,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusNumberEntityDescription(
        name="Soll Raumlufttemperatur",
        key="soll_raumlufttemperatur",
        register=23,
        fmt="f",
        scale=value_function_temperature_inverse,
        # write_scale=value_function_temperature_inverse,
        native_min_value=-20,
        native_max_value=50,
        native_step=0.1,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        unit=REGISTER_S16,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusNumberEntityDescription(
        name="Soll Ablufttemperatur",
        key="soll_ablufttemperatur",
        register=24,
        fmt="f",
        scale=value_function_temperature_inverse,
        # write_scale=value_function_temperature_inverse,
        native_min_value=-20,
        native_max_value=50,
        native_step=0.1,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        unit=REGISTER_S16,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusNumberEntityDescription(
        name="Luftfeuchtigkeit Maximum",
        key="luftfeuchtigkeit_maximum",
        register=45,
        fmt="i",
        native_min_value=0,
        native_max_value=100,
        # native_step=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        unit=REGISTER_S16,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusNumberEntityDescription(
        name="CO2 Maximum",
        key="co2_maximum",
        register=40,
        fmt="i",
        native_min_value=800,
        native_max_value=2000,
        # native_step=1,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        device_class=SensorDeviceClass.CO2,
        unit=REGISTER_S16,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
]

# ================================= Select Declarations ============================================================

SELECT_TYPES = [
    ###
    #
    #  Normal select types (holding register, coil)
    #
    ###
    PichlerModbusSelectEntityDescription(
        name="Betriebsmodus Sommer/Winter",
        key="betriebsmodus_sommer_winter",
        register=1,
        option_dict={
            1: "Sommer",
            2: "Winter",
        },
        allowedtypes=LG150 | LG250,
        icon="mdi:dip-switch",
    ),
    PichlerModbusSelectEntityDescription(
        name="Lüftungsstufe",
        key="luftungsstufe",
        register=2,
        option_dict={
            0: "Standby",
            1: "Stufe 1",
            2: "Stufe 2",
            3: "Stufe 3",
            4: "Grundlüftung",
        },
        allowedtypes=LG150 | LG250,
        icon="mdi:stairs",
    ),
    PichlerModbusSelectEntityDescription(
        name="Temperaturregelungsart",
        key="temperaturregelungsart",
        register=7,
        option_dict={
            1: "Abluft",
            2: "Zuluft",
            3: "Raum",
        },
        allowedtypes=LG150 | LG250,
        icon="mdi:thermometer-lines",
    ),
    PichlerModbusSelectEntityDescription(
        name="Luftfeuchtigkeit Regelung",
        key="luftfeuchtigkeit_regelung",
        register=44,
        option_dict={
            0: "Aus",
            1: "An",
        },
        allowedtypes=LG150 | LG250,
        entity_registry_enabled_default=False,
        icon="mdi:dip-switch",
    ),
    PichlerModbusSelectEntityDescription(
        name="CO2 Regelung",
        key="co2_regelung",
        register=39,
        option_dict={
            0: "Aus",
            1: "An",
        },
        allowedtypes=LG150 | LG250,
        entity_registry_enabled_default=False,
        icon="mdi:dip-switch",
    ),
]

# ================================= Sensor Declarations ============================================================

SENSOR_TYPES_MAIN: list[PichlerModbusSensorEntityDescription] = [
    ###
    #
    # Holding
    #
    ###
    PichlerModbusSensorEntityDescription(
        name="Betriebsmodus Sommer/Winter",
        key="betriebsmodus_sommer_winter",
        register=1,
        unit=REGISTER_U16,
        scale={
            1: "Sommer",
            2: "Winter",
        },
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:dip-switch",
    ),
    PichlerModbusSensorEntityDescription(
        name="Lüftungsstufe",
        key="luftungsstufe",
        register=2,
        scale={
            0: "Standby",
            1: "Stufe 1",
            2: "Stufe 2",
            3: "Stufe 3",
            4: "Grundlüftung",
        },
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan",
    ),
    PichlerModbusSensorEntityDescription(
        name="Temperaturregelungsart",
        key="temperaturregelungsart",
        register=7,
        scale={
            1: "Abluft",
            2: "Zuluft",
            3: "Raum",
        },
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:thermometer-lines",
    ),
    PichlerModbusSensorEntityDescription(
        name="Luftstrom Lüftungsstufe 1",
        key="volumenstrom_luftungsstufe_1",
        register=9,
        scale=10,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan-speed-1",
    ),
    PichlerModbusSensorEntityDescription(
        name="Luftstrom Lüftungsstufe 2",
        key="volumenstrom_luftungsstufe_2",
        register=10,
        scale=10,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan-speed-2",
    ),
    PichlerModbusSensorEntityDescription(
        name="Luftstrom Lüftungsstufe 3",
        key="volumenstrom_luftungsstufe_3",
        register=11,
        scale=10,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan-speed-3",
    ),
    PichlerModbusSensorEntityDescription(
        name="Luftstrom Grundlüftung",
        key="volumenstrom_grundluftung",
        register=12,
        scale=10,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan",
    ),
    PichlerModbusSensorEntityDescription(
        name="Lüftungsstufe 3 Timer",
        key="timer_luftungsstufe_3",
        register=70,
        scale=1,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan-clock",
    ),

    PichlerModbusSensorEntityDescription(
        name="Soll Zulufttemperatur",
        key="soll_zulufttemperatur",
        register=22,
        scale=value_function_temperature,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="Soll Raumlufttemperatur",
        key="soll_raumlufttemperatur",
        register=23,
        scale=value_function_temperature,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="Soll Ablufttemperatur",
        key="soll_ablufttemperatur",
        register=24,
        scale=value_function_temperature,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="Luftfeuchtigkeit Regelung",
        key="luftfeuchtigkeit_regelung",
        register=44,
        unit=REGISTER_U16,
        scale={
            0: "Aus",
            1: "An",
        },
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:dip-switch",
    ),
    PichlerModbusSensorEntityDescription(
        name="CO2 Regelung",
        key="co2_regelung",
        register=39,
        unit=REGISTER_U16,
        scale={
            0: "Aus",
            1: "An",
        },
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        icon="mdi:dip-switch",
    ),

    PichlerModbusSensorEntityDescription(
        name="Luftfeuchtigkeit Maximum",
        key="luftfeuchtigkeit_maximum",
        register=45,
        # native_step=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="CO2 Maximum",
        key="co2_maximum",
        register=40,
        # native_step=1,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        device_class=SensorDeviceClass.CO2,
        entity_registry_enabled_default=False,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),

    ###
    #
    # Input
    #
    ###
    PichlerModbusSensorEntityDescription(
        name="Temperatur Raum Display",
        key="temperatur_raum_display",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        register=29,
        scale=value_function_temperature,
        rounding=1,
        register_type=REG_INPUT,
        unit=REGISTER_S16,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="Temperatur Außenluft",
        key="temperatur_aussenluft",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        register=30,
        scale=value_function_temperature,
        rounding=1,
        register_type=REG_INPUT,
        unit=REGISTER_S16,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="Temperatur Fortluft",
        key="temperatur_fortluft",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        register=31,
        scale=value_function_temperature,
        rounding=1,
        register_type=REG_INPUT,
        unit=REGISTER_S16,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="Abluft Temperatur",
        key="temperatur_abluft",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        register=32,
        scale=value_function_temperature,
        rounding=1,
        register_type=REG_INPUT,
        unit=REGISTER_S16,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="Zuluft Temperatur",
        key="temperatur_zuluft",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        register=33,
        scale=value_function_temperature,
        rounding=1,
        register_type=REG_INPUT,
        unit=REGISTER_S16,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="Temperatur Nachheizregister Zuluft",
        key="temperatur_nachheizregister_zuluft",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        register=34,
        scale=value_function_temperature,
        rounding=1,
        entity_registry_enabled_default=False,
        register_type=REG_INPUT,
        unit=REGISTER_S16,
        allowedtypes=LG150 | LG250,
        # icon="mdi:thermometer",
    ),
    PichlerModbusSensorEntityDescription(
        name="Zuluft Ventilatordrehzahl",
        key="zuluftventilator_drehzahl",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        register=39,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan",
    ),
    PichlerModbusSensorEntityDescription(
        name="Abluft Ventilatordrehzahl",
        key="abluftventilator_drehzahl",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        register=40,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan",
    ),
    PichlerModbusSensorEntityDescription(
        name="Zuluft Ventilatorleistung",
        key="zuluftventilator",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        register=44,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan",
    ),
    PichlerModbusSensorEntityDescription(
        name="Abluft Ventilatorleistung",
        key="abluftventilator",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        register=45,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:fan",
    ),
    PichlerModbusSensorEntityDescription(
        name="Zuluft Luftstrom",
        key="zuluftvolumenstrom",
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        register=46,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:air-filter",
    ),
    PichlerModbusSensorEntityDescription(
        name="Abluft Luftstrom",
        key="abluftvolumenstrom",
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        register=47,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:air-filter",
    ),
    PichlerModbusSensorEntityDescription(
        name="Betriebsstatus",
        key="betriebsstatus",
        register=48,
        scale={
            0: "CPU startup",
            1: "Standby",
            2: "Anlauf",
            3: "Betrieb",
            4: "Nachlauf",
            5: "Standby Powersafe",
            6: "Testmodus",
        },
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:state-machine",
    ),
    PichlerModbusSensorEntityDescription(
        name="Filter Reststandzeit",
        key="filter_reststandzeit",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL,
        register=50,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:timer-sand",
    ),
    PichlerModbusSensorEntityDescription(
        name="Aktuelle Lüftungsstufe",
        key="aktuelle_luftungsstufe",
        register=59,
        scale={
            0: "Standby",
            1: "Stufe 1",
            2: "Stufe 2",
            3: "Stufe 3",
            4: "Grundlüftung",
            6: "AUS von extern",
            7: "Fehler",
        },
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:stairs",
    ),
    PichlerModbusSensorEntityDescription(
        name="Lüfter 1 Stunden",
        key="lufter_1_stunden",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL,
        register=87,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:timer-sand",
    ),
    PichlerModbusSensorEntityDescription(
        name="Lüfter 2 Stunden",
        key="lufter_2_stunden",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL,
        register=81,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:timer-sand",
    ),
    PichlerModbusSensorEntityDescription(
        name="Lüfter 3 Stunden",
        key="lufter_3_stunden",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL,
        register=82,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:timer-sand",
    ),
    PichlerModbusSensorEntityDescription(
        name="Lüfter Grund Stunden",
        key="lufter_grund_stunden",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL,
        register=83,
        scale=1,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:timer-sand",
    ),
    PichlerModbusSensorEntityDescription(
        name="Heizelement Stunden",
        key="heizelement_stunden",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL,
        register=85,
        scale=1,
        entity_registry_enabled_default=False,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:timer-sand",
    ),
    PichlerModbusSensorEntityDescription(
        name="Position Bypassklappe",
        key="position_bypassklappe",
        register=51,
        scale={
            1: "Wärmerückgewinnung",
            2: "Bypass",
            3: "Vorheizregister",
            4: "Fehler",
        },
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        icon="mdi:valve",
    ),
    PichlerModbusSensorEntityDescription(
        name="Feuchtesensor 1",
        key="feuchtesensor_1",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.HUMIDITY,
        register=91,
        scale=1,
        entity_registry_enabled_default=False,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        # icon="mdi:water",
    ),
    PichlerModbusSensorEntityDescription(
        name="Feuchtesensor 2",
        key="feuchtesensor_2",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.HUMIDITY,
        register=92,
        scale=1,
        entity_registry_enabled_default=False,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        # icon="mdi:water",
    ),
    PichlerModbusSensorEntityDescription(
        name="CO2 Sensor 1",
        key="co2_ensor_1",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.CO2,
        register=89,
        scale=1,
        entity_registry_enabled_default=False,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        # icon="mdi:water",
    ),
    PichlerModbusSensorEntityDescription(
        name="CO2 Sensor 2",
        key="co2_ensor_2",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.CO2,
        register=90,
        scale=1,
        entity_registry_enabled_default=False,
        register_type=REG_INPUT,
        allowedtypes=LG150 | LG250,
        # icon="mdi:water",
    ),
]

# ============================ plugin declaration =================================================


@dataclass
class pichler_plugin(plugin_base):
    async def async_determineInverterType(self, hub, configdict):
        # TOOD: get serial number and selecrt between LG250 and LG150
        return LG150

    def matchInverterWithMask(
        self, inverterspec, entitymask, serialnumber="not relevant", blacklist=None
    ):
        # returns true if the entity needs to be created for a ventilator
        lgmatch = ((inverterspec & entitymask & ALL_LG_GROUP) != 0) or (
            entitymask & ALL_LG_GROUP == 0
        )
        blacklisted = False
        if blacklist:
            for start in blacklist:
                if serialnumber.startswith(start):
                    blacklisted = True
        return lgmatch and not blacklisted


plugin_instance = pichler_plugin(
    plugin_name="Pichler",
    plugin_manufacturer="Pichler",
    SENSOR_TYPES=SENSOR_TYPES_MAIN,
    NUMBER_TYPES=NUMBER_TYPES,
    BUTTON_TYPES=BUTTON_TYPES,
    SELECT_TYPES=SELECT_TYPES,
    SWITCH_TYPES=[],
    block_size=100,
    order16=Endian.BIG,
    order32=Endian.LITTLE,
    auto_block_ignore_readerror=True,
)
