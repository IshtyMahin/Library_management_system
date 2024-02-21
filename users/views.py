from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import UserRegistrationForm,UserUpdateForm,CustomPasswordChangeForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class UserRegistrationView(FormView):
    template_name="user_registration.html"
    form_class = UserRegistrationForm
    success_url =reverse_lazy('home')
    
    def  form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name="user_login.html"
    def get_success_url(self) -> str:
        return reverse_lazy('home')
    
    
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect(reverse_lazy('home'))
        
        
class UserAccountUpdateView(View):

    template_name = 'profile.html'
    
    def get(self,request):
        form = UserUpdateForm(instance=request.user)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = UserUpdateForm(request.POST,instance=request.user)
        if  form.is_valid():
            form.save()
            return redirect(reverse_lazy('profile'))
        
        return render(request,self.template_name,{'form':form})
    
    
class PasswordChangeView(LoginRequiredMixin,View):
    
    def get(self,request):
        form = CustomPasswordChangeForm(user=request.user)
        print(form)
        return render(request,'pass_change.html',{'form': form})
    

    def post(self,request):
        form = CustomPasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated successfully')
            return redirect('profile')
        return render(request, 'pass_change.html', {'form': form})  