from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import About, Content, Home
from .forms import AboutForm, ContentForm, HomeForm

# Create your views here.

def home(request):
    posts = Home.objects.all().order_by('-id')
    context = {'posts': posts}
    return render(request, 'healthcenter/home.html', context)

class HomeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create new Home page content - requires admin/staff login"""
    model = Home
    form_class = HomeForm
    template_name = 'healthcenter/home_form.html'
    success_url = reverse_lazy('healthcenter:home')
    login_url = '/secure-admin/login/'

    def test_func(self):
        """Only allow staff and superuser"""
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        """Handle successful form submission"""
        messages.success(self.request, 'Home page content created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors"""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

def content(request):
    """Display all content entries"""
    contents = Content.objects.all().order_by('-updated_at')
    return render(request, 'healthcenter/content.html', {'contents': contents})

class ContentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create new Content - requires admin/staff login"""
    model = Content
    form_class = ContentForm
    template_name = 'healthcenter/content_form.html'
    success_url = reverse_lazy('healthcenter:content')
    login_url = '/secure-admin/login/'

    def test_func(self):
        """Only allow staff and superuser"""
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        """Handle successful form submission"""
        messages.success(self.request, 'Content created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors"""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update existing Content - requires admin/staff login"""
    model = Content
    form_class = ContentForm
    template_name = 'healthcenter/content_form.html'
    success_url = reverse_lazy('healthcenter:content')
    login_url = '/secure-admin/login/'

    def test_func(self):
        """Only allow staff and superuser"""
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        """Handle successful form submission"""
        messages.success(self.request, 'Content updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors"""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ContentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete Content - requires admin/staff login"""
    model = Content
    template_name = 'healthcenter/content_confirm_delete.html'
    success_url = reverse_lazy('healthcenter:content')
    context_object_name = 'content'
    login_url = '/secure-admin/login/'

    def test_func(self):
        """Only allow staff and superuser"""
        return self.request.user.is_staff or self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        """Handle deletion with success message"""
        messages.success(self.request, 'Content deleted successfully!')
        return super().delete(request, *args, **kwargs)
# About CRUD Views
class AboutListView(ListView):
    """Display list of all About Us entries"""
    model = About
    template_name = 'healthcenter/about_list.html'
    context_object_name = 'about_list'
    ordering = ['-updated_at']
    paginate_by = 10  # Optional: Add pagination if needed

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return About.objects.all().order_by('-updated_at')
        return About.objects.filter(is_active=True).order_by('-updated_at')

class AboutDetailView(DetailView):
    """Display detailed information about a specific About Us entry"""
    model = About
    template_name = 'healthcenter/about_detail.html'
    context_object_name = 'about'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not (user.is_staff or user.is_superuser) and not obj.is_active:
            # If not admin/staff and entry is not active, show 404
            from django.http import Http404
            raise Http404("About entry not found.")
        return obj

class AboutCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create new About Us information - requires admin/staff login"""
    model = About
    form_class = AboutForm
    template_name = 'healthcenter/about_form.html'
    success_url = reverse_lazy('healthcenter:about_list')
    login_url = '/secure-admin/login/'

    def test_func(self):
        """Only allow staff and superuser"""
        return self.request.user.is_staff or self.request.user.is_superuser

    # Removed restriction to allow multiple About entries

    def form_valid(self, form):
        """Handle successful form submission"""
        messages.success(self.request, 'About Us information created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors"""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class AboutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update existing About Us information - requires admin/staff login"""
    model = About
    form_class = AboutForm
    template_name = 'healthcenter/about_form.html'
    success_url = reverse_lazy('healthcenter:about_list')
    login_url = '/secure-admin/login/'

    def test_func(self):
        """Only allow staff and superuser"""
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        """Handle successful form submission"""
        messages.success(self.request, 'About Us information updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors"""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class AboutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete About Us information - requires admin/staff login"""
    model = About
    template_name = 'healthcenter/about_confirm_delete.html'
    success_url = reverse_lazy('healthcenter:about_list')
    context_object_name = 'about'
    login_url = '/secure-admin/login/'

    def test_func(self):
        """Only allow staff and superuser"""
        return self.request.user.is_staff or self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        """Handle deletion with success message"""
        messages.success(self.request, 'About Us information deleted successfully!')
        return super().delete(request, *args, **kwargs)