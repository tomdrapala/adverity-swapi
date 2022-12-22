from rest_framework import serializers

from people.models import Character

EMPTY_VALUE = ['unknown', 'n/a']


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        exclude = ()

    def empty_value_list_validation(self, value):
        if value[0] in EMPTY_VALUE:
            return list()
        return value

    def empty_value_validation(self, value):
        if value in EMPTY_VALUE:
            return None
        return value

    def validate_skin_color(self, value):
        return self.empty_value_list_validation(value)

    def validate_eye_color(self, value):
        return self.empty_value_list_validation(value)

    def validate_hair_color(self, value):
        return self.empty_value_list_validation(value)

    def validate_birth_year(self, value):
        return self.empty_value_validation(value)

    def validate_gender(self, value):
        return self.empty_value_validation(value)

    def validate_homeworld(self, value):
        return self.empty_value_validation(value)

    def to_internal_value(self, data):
        if data.get('height') in EMPTY_VALUE:
            data.pop('height')
        if data.get('mass') in EMPTY_VALUE:
            data.pop('mass')
        if data.get('mass'):
            data['mass'] = data['mass'].replace(',', '').replace('.', '')
        if data.get('birth_year'):
            data['birth_year'] = data['birth_year'].replace(',', '').replace('.', '')
        if data.get('skin_color'):
            data['skin_color'] = data['skin_color'].split(',')
        if data.get('eye_color'):
            data['eye_color'] = data['eye_color'].split(',')
        if data.get('hair_color'):
            data['hair_color'] = data['hair_color'].split(',')
        return super().to_internal_value(data)
