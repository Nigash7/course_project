from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect


class MyAdminSite(AdminSite):
    site_header = "Course Admin"

    def login(self, request, extra_context=None):
        response = super().login(request, extra_context)

        if request.user.is_authenticated:
            return HttpResponseRedirect("/home/")

        return response