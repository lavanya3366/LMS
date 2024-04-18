from rest_framework import serializers
from backend.models.allmodels import (
    Choice,
    Course, 
    CourseStructure, 
    Question, 
    Quiz, 
    UploadReadingMaterial, 
    UploadVideo
)
from backend.models.coremodels import (
    User,
    Customer
)


class CourseDisplaySerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """
    original_course = serializers.CharField(source='original_course.title', read_only=True, allow_null=True)
    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    def get_updated_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['title', 'created_at', 'updated_at', 'active', 'original_course', 'version_number']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = Course
        fields = ['id', 'title', 'created_at', 'updated_at', 'active', 'original_course', 'version_number']
        ordering = ['-updated_at']


class ActiveCourseDisplaySerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """
    original_course = serializers.CharField(source='original_course.title', read_only=True, allow_null=True)
    updated_at = serializers.SerializerMethodField()

    def get_updated_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id','title','updated_at', 'active','original_course', 'version_number']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = Course
        fields = ['id', 'title', 'updated_at','original_course', 'version_number']


class InActiveCourseDisplaySerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """
    original_course = serializers.CharField(source='original_course.title', read_only=True, allow_null=True)
    updated_at = serializers.SerializerMethodField()

    def get_updated_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id','title','updated_at', 'active','original_course', 'version_number']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = Course
        fields = ['id', 'title', 'updated_at','original_course', 'version_number']


class CourseSerializer(serializers.ModelSerializer):
    
    original_course = serializers.CharField(source='original_course.title', read_only=True, allow_null=True)
    updated_at = serializers.SerializerMethodField()
    
    def get_updated_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'title', 'summary', 'updated_at', 'original_course', 'version_number']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = Course
        fields = ['id', 'title', 'summary', 'updated_at', 'original_course', 'version_number']


class CourseStructureSerializer(serializers.ModelSerializer):
    """
    Serializer for the CourseStructure model.
    """
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'course', 'order_number', 'content_type', 'content_id']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = CourseStructure
        fields = ['id', 'order_number', 'content_type', 'content_id']


class ReadingMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for the UploadReadingMaterial model.
    """
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'title', 'reading_content']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = UploadReadingMaterial
        fields = ['id', 'title', 'reading_content']


class VideoMaterialSerializer(serializers.ModelSerializer):

    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'title', 'video']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = UploadVideo
        fields = ['id', 'title', 'video', 'summary']


class QuizSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'title', 'description']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description']


class ReadingMaterialListPerCourseSerializer(serializers.ModelSerializer):

    uploaded_at = serializers.SerializerMethodField()
    
    def get_uploaded_at(self, obj):
        return obj.uploaded_at.strftime("%Y-%m-%d")
    
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'title', 'uploaded_at']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = UploadReadingMaterial
        fields = ['id', 'title', 'uploaded_at']


class VideoMaterialListPerCourseSerializer(serializers.ModelSerializer):

    uploaded_at = serializers.SerializerMethodField()
    
    def get_uploaded_at(self, obj):
        return obj.uploaded_at.strftime("%Y-%m-%d")
    
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'title', 'uploaded_at']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = UploadVideo
        fields = ['id', 'title', 'uploaded_at']


class QuizListPerCourseSerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField()
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'title', 'created_at']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = UploadVideo
        fields = ['id', 'title', 'created_at']


class QuestionListPerQuizSerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField()
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'content', 'created_at']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = Question
        fields = ['id', 'content', 'created_at']

class ChoicesListPerQuestionSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        # Field Existence and Null Field Handling
        required_fields = ['id', 'choice', 'correct']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data
    class Meta:
        model = Choice
        fields = ['id', 'choice', 'correct']
