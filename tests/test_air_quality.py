import air_quality
from _util import setup_I2C_bus
import pytest

def test_fails_on_init_with_no_bus():
    with pytest.raises(ValueError):
        air_quality.SGP30()

def test_init_with_bus():
    with setup_I2C_bus() as i2c:
        assert air_quality.SGP30(bus=i2c)

def test_setup_with_alt_device_addr():
    with setup_I2C_bus() as i2c:
        assert air_quality.SGP30(address=0xA0, bus=i2c)



