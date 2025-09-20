
# apps/business/views/landing_views.py

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from apps.business.models import Landing, Business


class LandingListView(ListView):
    model = Landing
    template_name = "business/landing/landing_list.html"
    context_object_name = "landings"

    def get_queryset(self):
        business = get_object_or_404(Business, slug=self.kwargs["business_slug"])
        return Landing.objects.filter(business=business, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["business"] = get_object_or_404(Business, slug=self.kwargs["business_slug"])
        return context


class LandingDetailView(DetailView):
    model = Landing
    template_name = "business/landing/landing_detail.html"
    context_object_name = "landing"

    def get_object(self):
        business = get_object_or_404(Business, slug=self.kwargs["business_slug"])
        return get_object_or_404(Landing, slug=self.kwargs["landing_slug"], business=business, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["business"] = get_object_or_404(Business, slug=self.kwargs["business_slug"])
        return context
