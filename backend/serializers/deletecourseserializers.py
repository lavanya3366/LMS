# to be taken from priya
from rest_framework import serializers
from backend.models.allmodels import Choice, CourseStructure
class DeleteCourseStructureSerializer(serializers.Serializer):
    instance_id = serializers.IntegerField(        required=True,
        min_value=1,
        error_messages={
            "required": "Choice ID is required.",
            "min_value": "Choice ID must be a positive integer."
        })

    def validate_instance_id(self, value):
         # Check if the quiz with the provided ID exists
        if not CourseStructure.objects.filter(pk=value).exists():
            raise serializers.ValidationError("coursestructure with the provided ID does not exist.")
        return value
    
class DeleteChoiceSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "Choice ID is required.",
            "min_value": "Choice ID must be a positive integer."
        }
    )

    def validate_quiz_id(self, value):
        # Check if the quiz with the provided ID exists
        if not Choice.objects.filter(pk=value).exists():
            raise serializers.ValidationError("choice with the provided ID does not exist.")
        return value