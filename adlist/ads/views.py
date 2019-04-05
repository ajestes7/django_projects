from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.models import Ad
from ads.forms import CreateForm

# Create your views here.

from ads.models import Ad
from ads.util import AdsListView, AdsDetailView, AdsCreateView, AdsUpdateView, AdsDeleteView

class AdListView(AdsListView):
    model = Ad
    template_name = "ad_list.html"

class AdDetailView(AdsDetailView):
    model = Ad
    template_name = "ad_detail.html"

class AdCreateView(AdsCreateView):
    model = Ad
    fields = ['title', 'text', 'price']
    template_name = "ad_form.html"

class AdUpdateView(AdsUpdateView):
    model = Ad
    fields = ['title', 'text', 'price']
    template_name = "ad_form.html"

class AdDeleteView(AdsDeleteView):
    model = Ad
    template_name = "ad_delete.html"

class AdFormView(LoginRequiredMixin, View):
    template = 'ad_form.html'
    success_url = reverse_lazy('ads')
    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
            form = CreateForm(instance=ad)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)

def stream_file(request, pk) :
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response
