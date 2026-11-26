from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProfileView(LoginRequiredMixin, TemplateView):
    """ A view that can only display a logged-in user's profile"""
    
    template_name = 'profiles/profile.html'
