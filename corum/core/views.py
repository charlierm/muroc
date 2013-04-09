# Create your views here.
from django.views.generic import ListView, View, DetailView
from django.views.generic.edit import CreateView
from core.models import Case,UserTarget,HostTarget
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from core.forms import CaseForm
import json


class CaseListView(ListView):
    """
    ListView for displaying the list of current Cases.
    """
    model = Case
    paginate_by = 2
    template_name = "core/case_list.html"
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = super(CaseListView, self).get_queryset().filter(parent_case=None)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CaseListView, self).dispatch(request, *args, **kwargs)


class DefaultCaseView(View):
    def get(self, request, case_name):
        case = Case.objects.get(slug=case_name)
        request.user.current_case = case
        request.user.save()
        return HttpResponse(json.dumps({'result': True}))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DefaultCaseView, self).dispatch(request, *args, **kwargs)


class CreateCaseView(CreateView):
    model = Case
    form_class = CaseForm

    def get_initial(self):
        self.initial.update({'owner': self.request.user})
        return super(CreateCaseView, self).get_initial()


class CaseDetailView(DetailView):

    model = Case

    # def get_queryset(self):
    #     queryset = super(CaseListView, self).get_queryset().filter(parent_case=None)
    #     return queryset

class UserTargetDetailView(DetailView):
    
    model=UserTarget

class HostTargetDetailView(DetailView):
    
    model=HostTarget