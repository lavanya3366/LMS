from rest_framework import permissions
from backend.models.allmodels import CourseEnrollment, CourseRegisterRecord
from core.custom_mixins import ClientAdminMixin, SuperAdminMixin
from backend.models.coremodels import UserRolePrivileges

'''
allowed_resources:
1- LMS
2- Course Customer Registration
3- Course Enrollment
4- Courses
5- Course Management
6- Dashboard
'''

class SuperAdminPermission(SuperAdminMixin, permissions.BasePermission):
    def has_permission(self, request, view):
        print('SuperAdminPermission')
        privilege_response = self.has_super_admin_privileges(request)
        return privilege_response

class ClientAdminPermission(ClientAdminMixin, permissions.BasePermission):
    def has_permission(self, request, view):
        print('ClientAdminPermission')
        privilege_response = self.has_client_admin_privileges(request)
        return privilege_response
    
class SuperAdminOrGetOnly(SuperAdminMixin,permissions.BasePermission):
    """
        Permission class which allow users which are not super users to access GET request functionality only
    """
    def has_permission(self, request, view):
        print('SuperAdminOrGetOnly')
        if self.has_super_admin_privileges(request):
            return True
        if request.method == 'GET':
            # special condition for GET request in  CourseView API
            # if request.path.startswith('/lms/courses/'):
            if request.path == '/lms/courses/':
                print('did path thing worked ')
                course_id = request.query_params.get('course_id')
                filtered_display = request.query_params.get('filtered_display')
                if not course_id or filtered_display in ["inactive", "all"]:
                    return False
            return True
        return False


class CourseContentPermissions(permissions.BasePermission, SuperAdminMixin, ClientAdminMixin):
    
    def has_permission(self, request, view):
        print('CourseContentPermissions')
        if self.has_super_admin_privileges(request):
            return True
        
        if request.method == 'GET':
            user = request.data.get('user')
            course_id = request.kwargs.get('course_id')
            content_id = request.query_params.get('content_id')
            list_mode = request.query_params.get('list', '').lower() == 'true'
            if content_id or not list_mode :
                is_actively_enrolled = CourseEnrollment.objects.filter(course=course_id, user=user['id'], active=True).exists()
                if is_actively_enrolled:
                    return True
                
                if self.has_client_admin_privileges(request):
                    is_actively_registered = CourseRegisterRecord.objects.filter(course=course_id, customer=user['customer'], active=True).exists()
                    if is_actively_registered:
                        return True
        return False


# class SuperAdminOrAuthorizedOnly(permissions.BasePermission, SuperAdminMixin, ClientAdminMixin):
    
#     def has_permission(self, request, view):
#         print('SuperAdminOrAuthorizedOnly')
#         if self.has_super_admin_privileges(request):
#             return True

#         if request.method == 'GET':
#             user = request.data.get('user')
#             course_id = request.kwargs.get('course_id')
            
#             is_actively_enrolled = CourseEnrollment.objects.filter(course=course_id, user=user['id'], active=True).exists()
#             if is_actively_enrolled:
#                 return True
            
#             if self.has_client_admin_privileges(request):
#                 is_actively_registered = CourseRegisterRecord.objects.filter(course=course_id, customer=user['customer'], active=True).exists()
#                 if is_actively_registered:
#                     return True

#         return False