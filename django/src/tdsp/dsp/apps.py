from django.apps import AppConfig


class DspConfig(AppConfig):
    """
    Configuration class for the 'dsp' app within the 'tdsp' project.

    This class sets the default auto field to 'BigAutoField' for the models in the 'dsp' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tdsp.dsp'
