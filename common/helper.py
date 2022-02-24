def get_type(path):
    permission_type = path.split("/")[1]
    return permission_type


def check_company_admin_permissions(request):
    permission_type = get_type(request.path)
    if permission_type in ["employee"]:
        return True
    return False


def check_employee_permissions(request):
    permission_type = get_type(request.path)
    if permission_type in ["employee","project"]:
        return True
    return False
