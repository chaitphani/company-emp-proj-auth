from rest_framework import viewsets,status
from rest_framework.response import Response

from employee.helper import generate_password
from super_admin.models import User
from employee.serializers import EmployeSerializer
from company.models import Company


class EmployeeAPI(viewsets.ViewSet):

    serializer_class = EmployeSerializer
    http_method_names = ["post", "get", "put", "delete", "head", "options"]

    def create(self, request, *args, **kwargs):
        try:
            try:
                User.objects.get(email=request.data["email"],user_type=User.UserTypes.ADMIN)
                return Response({"Employee already exist cannot create another"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except User.DoesNotExist:
                pass

            user = User(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                email=request.data["email"],
                phone=request.data["phone"],
                is_active=True,
                user_type=User.UserTypes.EMPLOYEE,
            )

            if request.data["password_type"] == "auto":
                #send this password to employee email
                password = generate_password()
                user.set_password(password)
            user.set_password(request.data["password"])
            user.save()
            return Response(
                self.serializer_class(user).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as err:
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            employee_list = Company.objects.filter(user__user_type=User.UserTypes.EMPLOYEE, is_active=True)
            return Response(
                self.serializer_class(employee_list, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as err:
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            employee = User.objects.get(id=kwargs["pk"],is_active=True,user_type=User.UserTypes.EMPLOYEE)
            serializer = self.serializer_class(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #here doing soft delete to ensure the employee details are with us for future promotional purpose
    def destroy(self, request, *args, **kwargs):
        try:
            employee = User.objects.get(id=kwargs["pk"],user_type=User.UserTypes.EMPLOYEE)
            employee.is_active = request.data["is_active"]
            employee.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





