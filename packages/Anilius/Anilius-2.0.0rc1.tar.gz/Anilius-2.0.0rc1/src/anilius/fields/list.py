from anilius.core.serializer_field import SerializerField


class ListField(SerializerField):
    def validate(self):
        return type(self._raw_value) is list

    def get_value(self):
        return self._raw_value
