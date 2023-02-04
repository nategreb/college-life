from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from colleges.models import Professor, College, CollegeClass
from colleges.forms import SearchForm


class ProfessorSearchView(ListView):
    """
    filter objects and autocomplete
    get and post method
    - get filters based on the naem
    - post takes the name + id to get the object

    """
    template_name = 'professors/ProfessorSearch.html'
    model = Professor
    context_object_name = 'objects'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['college'] = self.college
        context['form'] = SearchForm()
        context['form'].fields['search'].widget.attrs['placeholder'] = f'Search for a {self.model.__name__.lower()}'

        # transform queryset into choices for form
        arr = []
        for obj in context['objects']:
            arr.append((obj.__str__, obj.id))
        context['form'].fields['search'].choices = arr

        return context

    def get_queryset(self):
        self.college = get_object_or_404(College, id=self.kwargs['college_id'])
        return self.model.objects.filter(college=self.college)

    def dispatch(self, request, *args, **kwargs):
        if request.POST:
            #   TODO: is validation needed?
            search_query = request.POST['search']

            objs = self.model.objects.annotate(
                search=SearchVector('first_name', 'last_name')
            ).filter(Q(search__icontains=search_query) | Q(search=search_query))

            if objs.count() == 1:
                kwargs.update({'professor_id': objs[0].id, 'professor_slug': objs[0].slug})
                return redirect(reverse_lazy('colleges:professor', kwargs=kwargs))
            else:

                paginate = Paginator(objs, 15)  # show 15 reviews per page
                page_number = request.GET.get('page')
                page_obj = paginate.get_page(page_number)

                return TemplateResponse(
                    request=request,
                    template='SearchResults.html',
                    context={
                        'page_obj': page_obj,
                        'college': College.approved_colleges.get(id=self.kwargs['college_id']),
                        'content_type': 'professor'
                    }
                )
        else:
            return super(ProfessorSearchView, self).dispatch(request, *args, **kwargs)


class ClassesSearchView(ProfessorSearchView):
    template_name = 'courses/CourseSearch.html'
    model = CollegeClass

    def dispatch(self, request, *args, **kwargs):
        if request.POST:
            #   TODO: is validation needed?
            search_query = request.POST['search']

            objs = self.model.objects.filter(class_name__icontains=search_query)

            if objs.count() == 1:
                kwargs.update({'course_id': objs[0].id})  # , 'course_slug': objs[0].slug})
                return redirect(reverse_lazy('colleges:class', kwargs=kwargs))
            else:

                paginate = Paginator(objs, 15)  # show 15 reviews per page
                page_number = request.GET.get('page')
                page_obj = paginate.get_page(page_number)

                return TemplateResponse(
                    request=request,
                    template='SearchResults.html',
                    context={
                        'page_obj': page_obj,
                        'college': College.approved_colleges.get(id=self.kwargs['college_id']),
                        'content_type': 'class'

                    }
                )
        else:
            return super(ProfessorSearchView, self).dispatch(request, *args, **kwargs)
