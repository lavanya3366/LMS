from rest_framework import serializers

class ActiveEnrolledUserCountSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(required=True)

    def validate_customer_id(self, value):
        """
        Ensure that customer_id is provided and is a positive integer.
        """
        if value is None:
            raise serializers.ValidationError("Customer ID is required")
        if value <= 0:
            raise serializers.ValidationError("Customer ID must be a positive integer")
        return value
from backend.models.coremodels import Customer
class RegisteredCourseCountSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()

    def validate_customer_id(self, value):
        """
        Ensure that customer_id is provided and is a positive integer.
        """
        if value is None:
            raise serializers.ValidationError("Customer ID is required")
        if value <= 0:
            raise serializers.ValidationError("Customer ID must be a positive integer")
        if not Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError("Customer does not exist")
        return value

class ProgressDataSerializer(serializers.Serializer):
    course_title = serializers.CharField()
    completion_count = serializers.IntegerField(min_value=0)
    in_progress_count = serializers.IntegerField(min_value=0)
    not_started_count = serializers.IntegerField(min_value=0)

    # Add any additional fields or customization as needed