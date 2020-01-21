from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from panel.models import (Album)


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Admin, Admin permission mixin
    """
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class indexAdminTemplateView(AdminStaffRequiredMixin, TemplateView):
    """
    Admin, Home Page (Dashboard) Page Class View: TemplateView
    """
    template_name = 'secret/index.html'


class distributionAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, Distribution Page Class View: ListView
    """
    template_name = 'secret/distribution.html'
    model = Album

    def get_queryset(self):
        return Album.objects.all().order_by('status')
