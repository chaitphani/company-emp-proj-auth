from project.models import Project
from project.serializers import ProjectSerializer
from company.models import Company
from rest_framework import viewsets,status
from rest_framework.response import Response

# from operator import truediv
# from company.serializers import CompanySerializer
# from super_admin.models import User
# from employee.serializers import EmployeSerializer
# from employee.helper import generate_password
# from django.db import transaction
# import logging
# from swagger.documentation import swagger_wrapper
# from drf_yasg import openapi


class ProjectAPI(viewsets.ViewSet):

    serializer_class = ProjectSerializer
    http_method_names = ["post", "get", "put", "delete", "head", "options"]

    # @swagger_wrapper({
    #     "project_title" : openapi.TYPE_STRING,
    #     "project_description" : openapi.TYPE_STRING,
    #     "project_deadline_date" : openapi.TYPE_STRING,
    #     "comments" : openapi.TYPE_STRING
    # })
    def create(self, request, *args, **kwargs):
        try:
            try:
                Project.objects.get(project_title=request.data["project_title"])
                return Response({"Project title already exist"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Project.DoesNotExist:
                pass

            project = Project(
                project_title=request.data["project_title"],
                project_description=request.data["project_description"],
                project_deadline_date=request.data["project_deadline_date"],
                comments=request.data["comments"],
                is_active=True,
            )
            project.save()
            return Response(
                self.serializer_class(project).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as err:
            print(f"ProjectAPI create: {err}")
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            project_list = Company.objects.filter(is_active=True)
            return Response(
                self.serializer_class(project_list, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as err:
            # logging.error(f"ProjectAPI list: {err}", exc_info=True)
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @swagger_wrapper({
    #     "project_title" : openapi.TYPE_STRING,
    #     "project_description" : openapi.TYPE_STRING,
    #     "project_deadline_date" : openapi.TYPE_STRING,
    #     "comments" : openapi.TYPE_STRING
    # })
    def update(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs["pk"],is_active=True)
            serializer = self.serializer_class(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            # logging.error(f"ProjectAPI update: {err}", exc_info=True)
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #here doing soft delete
    def destroy(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs["pk"])
            project.is_active = request.data["is_active"]
            project.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            # logging.error(f"ProjectAPI delete: {err}", exc_info=True)
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





