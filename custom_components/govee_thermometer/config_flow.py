import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_API_KEY, CONF_TEMP_UNIT, TEMP_UNIT_CELSIUS, TEMP_UNIT_FAHRENHEIT

class GoveeThermometerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Govee Thermometer."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Simple validation to ensure API key is provided
            if not user_input.get(CONF_API_KEY):
                errors["base"] = "invalid_api_key"
            else:
                return self.async_create_entry(title="Govee Thermometer", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): cv.string,
                    vol.Required(
                        CONF_TEMP_UNIT,
                        default=TEMP_UNIT_CELSIUS,
                    ): vol.In(
                        {
                            TEMP_UNIT_CELSIUS: "Celsius (°C)",
                            TEMP_UNIT_FAHRENHEIT: "Fahrenheit (°F)",
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return GoveeThermometerOptionsFlow(config_entry)


class GoveeThermometerOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Govee Thermometer."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        # Use modern HA pattern instead of assigning self.config_entry directly
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current setting or default to Celsius
        current_unit = self._config_entry.options.get(CONF_TEMP_UNIT,config_entry.data.get(CONF_TEMP_UNIT,TEMP_UNIT_CELSIUS,),)

        options_schema = vol.Schema(
            {
                vol.Required(CONF_TEMP_UNIT, default=current_unit): vol.In(
                    {
                        TEMP_UNIT_CELSIUS: "Celsius (°C)",
                        TEMP_UNIT_FAHRENHEIT: "Fahrenheit (°F)",
                    }
                )
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
