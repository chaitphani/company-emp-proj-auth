from company.serializers import CompanySerializer
from super_admin.models import User
from company.models import Company
from rest_framework import viewsets,status
from rest_framework.response import Response
# from django.db import transaction
# import logging
from swagger.documentation import swagger_wrapper
from drf_yasg import openapi


class CompanyAPI(viewsets.ViewSet):

    serializer_class = CompanySerializer
    http_method_names = ["post", "get", "put", "delete", "head", "options"]

    @swagger_wrapper({
        "company_email" : openapi.TYPE_STRING,
        "company_name" : openapi.TYPE_STRING,
        "company_phonenumber" : openapi.TYPE_STRING,
        "password" : openapi.TYPE_STRING,
        "company_address" : openapi.TYPE_STRING,
        "company_website" : openapi.TYPE_STRING,
    })
    def create(self, request, *args, **kwargs):
        try:
            try:
                Company.objects.get(company_email=request.data["company_email"])
                return Response({"Company already created with same email"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Company.DoesNotExist:
                pass

            user = User(
                first_name=request.data["company_name"],
                last_name=request.data["company_name"],
                email=request.data["company_email"],
                phone=request.data["company_phonenumber"],
                is_active=True,
                user_type=User.UserTypes.COMPANY_ADMIN,
            )
            user.set_password("password")
            user.save()
            company = Company(
                company_name = request.data["company_name"],
                company_address = request.data["company_address"],
                company_email = request.data["company_email"],
                company_phonenumber = request.data["company_phonenumber"],
                company_website = request.data["company_website"],
                user = user,
                is_active=True
            )
            company.save()
            return Response(
                self.serializer_class(company).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as err:
            # print("error : ",err)
            # logging.error(f"CompanyAPI create: {err}", exc_info=True)
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            company_list = Company.objects.filter(is_active=True)
            return Response(
                self.serializer_class(company_list, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as err:
            # logging.error(f"FormApi list: {err}", exc_info=True)
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_wrapper({
        "company_email" : openapi.TYPE_STRING,
        "company_name" : openapi.TYPE_STRING,
        "company_phonenumber" : openapi.TYPE_STRING,
        "company_address" : openapi.TYPE_STRING,
        "company_website" : openapi.TYPE_STRING,
    })
    def update(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(id=kwargs["pk"])
            serializer = self.serializer_class(company, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            # logging.error(f"CompanyAPI update: {err}", exc_info=True)
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #We are doing soft delete to ensure the company details are with us for future promotional purpose
    def destroy(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(id=kwargs["pk"])
            company.is_active = request.data["is_active"]
            company.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            # logging.error(f"CompanyAPI delete: {err}", exc_info=True)
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

