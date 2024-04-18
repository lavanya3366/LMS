# to be taken from priya
from rest_framework import serializers
class PatchCourseStructureSerializer(serializers.Serializer):
    instance_id = serializers.IntegerField(required=True)

    def validate_instance_id(self, value):
        """
        Ensure that instance_id is provided and is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Instance ID must be a positive integer")
        return value
    
class PatchChoiceSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField(required=True)

    def validate_choice_id(self, value):
        """
        Ensure that choice_id is provided and is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Choice ID must be a positive integer")
        return value