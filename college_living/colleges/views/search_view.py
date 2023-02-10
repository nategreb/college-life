from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages

from colleges.models import Professor, College, CollegeClass
from colleges.forms import SearchForm


class ProfessorSearchView(ListView):
    # TODO make pagination faster
    template_name = 'ObjectSearch.html'
    object_type = 'professors'
    model = Professor
    context_object_name = 'objects'
    form_class = SearchForm
    search_results_template = 'SearchResults.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['college'] = self.college
        context['object_type'] = self.object_type

        context['form'] = SearchForm()
        context['form'].fields['search'].widget.attrs['placeholder'] = f'Search for a {self.model.__name__.lower()}'

        # transform queryset into choices for form when no search query and no pagination has been performed
        if not self.request.GET.get('search', None) and not self.request.GET.get('page', None):
            arr = []
            for obj in context['objects']:
                arr.append((obj.__str__, obj.id))
            context['form'].fields['search'].choices = arr
        else:
            context['search'] = self.request.GET.get('search', None)
            self.template_name = self.search_results_template
            objs = context['objects']
            paginate = Paginator(objs, 15)  # show 15 reviews per page
            page_number = self.request.GET.get('page')
            page_obj = paginate.get_page(page_number)
            context['page_obj'] = page_obj
        return context

    def get_queryset(self):
        self.college = get_object_or_404(College, id=self.kwargs['college_id'])
        search_query = self.request.GET.get('search', None)

        if search_query:
            return self.model.objects.annotate(
                search=SearchVector('first_name', 'last_name')
            ).filter(Q(search__icontains=search_query) | Q(search=search_query))
        else:
            return self.model.objects.filter(college=self.college)

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('search', None):
            objects = self.get_queryset()
            if objects.count() == 1:
                kwargs.update({'professor_id': objects[0].id, 'professor_slug': objects[0].slug})
                return redirect(reverse_lazy('colleges:professor', kwargs=kwargs))
            elif objects.count() == 0:
                # add info label that search didn't find anything and return to search
                messages.add_message(self.request, messages.INFO, 'No results founds')
                return redirect(reverse_lazy('colleges:professor_search', kwargs=kwargs))
        return super(ProfessorSearchView, self).dispatch(request, *args, **kwargs)


class ClassesSearchView(ProfessorSearchView):
    model = CollegeClass
    object_type = 'courses'

    def get_queryset(self):
        self.college = get_object_or_404(College, id=self.kwargs['college_id'])
        search_query = self.request.GET.get('search', None)

        if search_query:
            return self.model.objects.filter(class_name__icontains=search_query)
        else:
            return self.model.objects.filter(college=self.college)

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('search', None):
            objects = self.get_queryset()
            if objects.count() == 1:
                # add info label that search didn't find anything
                if objects.count() == 0:
                    messages.add_message(self.request, messages.INFO, 'No results founds')
                kwargs.update({'course_id': objects[0].id})
                return redirect(reverse_lazy('colleges:class', kwargs=kwargs))
            elif objects.count() == 0:
                # add info label that search didn't find anything and return to search
                messages.add_message(self.request, messages.INFO, 'No results founds')
                return redirect(reverse_lazy('colleges:course_search', kwargs=kwargs))
        return super(ClassesSearchView, self).get(request, *args, **kwargs)
