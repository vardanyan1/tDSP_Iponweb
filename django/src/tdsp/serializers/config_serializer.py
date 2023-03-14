from rest_framework import serializers

from ..dsp.models.game_config_model import ConfigModel


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigModel
        fields = '__all__'


class ConfigCreateSerializer(ConfigSerializer):
    class Meta:
        model = ConfigModel
        exclude = ('current',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('rounds_left', None)
        return data
