from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, F
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView

from apps.forms import AuthForm, ProfileForm, ChangePasswordForm, OrderForm
from apps.models import User, Region, District, Category, Product, Wishlist, AdminSetting, Order


def district_list_view(request):
    region_id = request.GET.get('region_id')
    districts = District.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProfileFormView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('auth')
    form_class = ProfileForm
    template_name = 'apps/auth/profile.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['regions'] = Region.objects.all()
        return data

    def form_valid(self, form):
        form.update(self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


class AuthFormView(FormView):
    form_class = AuthForm
    template_name = 'apps/auth/auth.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        data = form.cleaned_data
        phone_number = data.get('phone_number')
        password = form.data.get('password')
        users = User.objects.filter(phone_number=phone_number)
        if users.exists():
            user = users.first()
            if check_password(password, user.password):
                login(self.request, user)
            else:
                messages.error(self.request, 'Password hato.')
                return redirect('auth')
        else:
            user = form.save()
            login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for erorr in form.errors.values():
            messages.error(self.request, erorr)
        return super().form_invalid(form)


class ChangePasswordFormView(FormView):
    form_class = ChangePasswordForm
    template_name = 'apps/auth/auth.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        session_password = self.request.user.password
        old_password = form.cleaned_data.get('old')
        if not check_password(session_password, old_password):
            messages.error(self.request, 'Password hato.')
        else:
            form.update(self.request.user)
        return redirect('profile')
