from rest_framework import serializers
from super_admin.models import User


class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"