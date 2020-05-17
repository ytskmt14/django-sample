from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.views import LoginView as AuthLoginView

from .forms import LoginForm

# 旅行一覧ページ用View
# class IndexView(ListView):
class IndexView(TemplateView):
    template_name = "bookmarkapp/index.html"

index = IndexView.as_view()

class DetailView(TemplateView):
    template_name = "bookmarkapp/detail.html"

detail = DetailView.as_view()

class LoginView(AuthLoginView):
    form_class = LoginForm
    template_name = 'bookmarkapp/login.html'

login = LoginView.as_view()
