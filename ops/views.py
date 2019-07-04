from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView


class LoginView(TemplateView):

    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        kwargs['next'] = self.request.GET.get('next')
        return super(LoginView,self).get_context_data(**kwargs)

    def post(self,request,*args,**kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            status = 0
        else:
            status = 1
        return JsonResponse({'status':status })


class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect("/login/")

class IndexPage(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'

