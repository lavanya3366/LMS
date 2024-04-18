
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from django.utils import timezone
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from core.custom_mixins import (
    SuperAdminMixin)
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import status
from backend.serializers.deletecourseserializers import  PatchChoiceSerializer
from django.contrib import messages


from backend.models.allmodels import (
    Choice,
    Course,
    CourseStructure,
    Progress,
    Quiz,
    Question,
    QuizAttemptHistory,
)
from backend.serializers.createcourseserializers import (
    CreateChoiceSerializer,
    QuizSerializer, 
)
from backend.serializers.courseserializers import (
    CourseStructureSerializer,

)
import pandas as pd
from backend.forms import (
    QuestionForm,
)
from backend.models.coremodels import *
from backend.serializers.courseserializers import *
from rest_framework.response import Response
from django.views.generic import (
    FormView,
)
from backend.forms import (
    QuestionForm,
)

class QuestionView(SuperAdminMixin, APIView):
    """
    GET API for super admin to list of questions of specific quiz
    
    POST API for super admin to create new instances of question for the quiz
    
    """
    def get(self, request, quiz_id, format=None):
        try:
            if not self.has_super_admin_privileges(request) :
                return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
            questions = Question.objects.filter(
                quizzes__id=quiz_id, 
                active=True, 
                deleted_at__isnull=True
            )
            serializer = QuestionListPerQuizSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
                if isinstance(e, ValidationError):
                    return Response({"error": "Validation Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, course_id, *args, **kwargs):
        if not self.has_super_admin_privileges(request) :
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        course = Course.objects.get(pk=course_id)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        if course.active:
            return Response({"error": "Course is active, cannot proceed"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        if not data:
            return Response({"error": "Request body is empty"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Validate and save quiz
            requested_data = request.data.copy()
            requested_data['courses'] = [course_id]
            serializer = QuizSerializer(data=requested_data)
            if serializer.is_valid():
                quiz = serializer.save()
                # If original_course is null, only save quiz
                if course.original_course is None:
                    return Response({"message": "Quiz created successfully"}, status=status.HTTP_201_CREATED)
                else:
                    # If original_course is not null, also create a CourseStructure entry
                    try:
                        last_order_number = CourseStructure.objects.filter(course=course).latest('order_number').order_number
                    except CourseStructure.DoesNotExist:
                        last_order_number = 0
                    # Create new CourseStructure instance
                    course_structure_data = {
                        'course': course_id,
                        'order_number': last_order_number + 1,
                        'content_type': 'quiz',
                        'content_id': quiz.pk
                    }
                    course_structure_serializer = CourseStructureSerializer(data=course_structure_data)
                    if course_structure_serializer.is_valid():
                        course_structure_serializer.save()
                        return Response({"message": "Quiz created successfully"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"error": course_structure_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                if isinstance(e, ValidationError):
                    return Response({"error": "Validation Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChoicesView(SuperAdminMixin, APIView):
    """
    GET API for super admin to list of choices of specific question
    
    POST API for super admin to create new instances of choice for the question
    
    """
    
    def get(self, request, question_id, format=None):
        try:
            if not self.has_super_admin_privileges(request) :
                return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
            choices = Choice.objects.filter(
                question__id=question_id, 
                active=True, 
                deleted_at__isnull=True
            )
            serializer = ChoicesListPerQuestionSerializer(choices, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
                if isinstance(e, ValidationError):
                    return Response({"error": "Validation Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, question_id, *args, **kwargs):
        if not self.has_super_admin_privileges(request) :
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        question = Question.objects.get(pk=question_id)
        if not question:
            return  Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            serializer = CreateChoiceSerializer(data=request.data, context={'question_id': question_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
                if isinstance(e, ValidationError):
                    return Response({"error": "Validation Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, question_id):
        try:
            serializer = PatchChoiceSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            choice_id = serializer.validated_data.get('choice_id')
            choice = Choice.objects.get(id=choice_id, question_id=question_id)
            # Check if the choice instance has already been soft deleted
            if choice.deleted_at:
                return Response({'error': 'Choice already soft deleted'}, status=status.HTTP_400_BAD_REQUEST)
            # Soft delete the choice instance by marking it as deleted
            choice.deleted_at = timezone.now()
            choice.active = False
            choice.save()
            # Return success response
            return Response({'message': 'Choice soft deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except (ValueError, Choice.DoesNotExist) as e:
            error_message = 'Choice not found for the given question'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

    

# @method_decorator([login_required], name="dispatch")
class QuizTake(FormView):
    form_class = QuestionForm
    template_name = "question.html"
    result_template_name = "result.html"

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, slug=self.kwargs["quiz_slug"])
        self.course = get_object_or_404(Course, pk=self.kwargs["pk"])
        quiz_questions_count = self.quiz.questions.count()
        course = get_object_or_404(Course, pk=self.kwargs["pk"])

        if quiz_questions_count <= 0:
            messages.warning(request, f"Question set of the quiz is empty. try later!")
            return redirect("course-structure", self.course.id) # redirecting to previous page as this quiz can't be started.
# send here SingleCourseStructureListDisplayView
        # =================================================================
        user_header = request.headers.get("user")
        enrolled_user = get_object_or_404(User, pk=13)
        # ===============================
        # enrolled_user = request.user
        self.sitting = QuizAttemptHistory.objects.user_sitting(
            enrolled_user,
            self.quiz, 
            self.course
        )

        if self.sitting is False:
            messages.info(
                request,
                f"You have already sat this exam and only one sitting is permitted",
            )
            return redirect("course-structure", self.course.id)

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        self.question = self.sitting.get_first_question()
        self.progress = self.sitting.progress()
        form_class = self.form_class

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        self.form_valid_user(form)
        if self.sitting.get_first_question() is False:
            self.sitting.mark_quiz_complete()
            return self.final_result_user()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context["question"] = self.question
        context["quiz"] = self.quiz
        context["course"] = get_object_or_404(Course, pk=self.kwargs["pk"])
        if hasattr(self, "previous"):
            context["previous"] = self.previous
        if hasattr(self, "progress"):
            context["progress"] = self.progress
        return context

    def form_valid_user(self, form):
        # =================================================================
        user_header = self.request.headers.get("user")
        enrolled_user = get_object_or_404(User, pk=13)
        # ===============================
        # enrolled_user = request.user
        progress, _ = Progress.objects.get_or_create(enrolled_user=enrolled_user)
        guess = form.cleaned_data["answers"]
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {
                "previous_answer": guess,
                "previous_outcome": is_correct,
                "previous_question": self.question,
                "answers": self.question.get_choices(),
                "question_type": {self.question.__class__.__name__: True},
            }
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            "course": get_object_or_404(Course, pk=self.kwargs["pk"]),
            "quiz": self.quiz,
            "score": self.sitting.get_current_score,
            "max_score": self.sitting.get_max_score,
            "percent": self.sitting.get_percent_correct,
            "sitting": self.sitting,
            "previous": self.previous,
            "course": get_object_or_404(Course, pk=self.kwargs["pk"]),
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results["questions"] = self.sitting.get_questions(with_answers=True)
            results["incorrect_questions"] = self.sitting.get_incorrect_questions

        if (
            self.quiz.exam_paper is False
        ):
            self.sitting.delete()

        return render(self.request, self.result_template_name, results)

def dummy_quiz_index(request, course_id):
    course = Course.objects.get(pk=course_id)
    return render(request, 'quiz_index.html', {'course_id': course_id, 'course': course})



