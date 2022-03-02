from project.models import Project
from project.serializers import ProjectSerializer
from company.models import Company
from rest_framework import viewsets,status
from rest_framework.response import Response



class ProjectAPI(viewsets.ViewSet):

    serializer_class = ProjectSerializer
    http_method_names = ["post", "get", "put", "delete", "head", "options"]

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
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs["pk"],is_active=True)
            serializer = self.serializer_class(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #here doing soft delete
    def destroy(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs["pk"])
            project.is_active = request.data["is_active"]
            project.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





