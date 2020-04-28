from django.views.generic import ListView, DetailView, TemplateView

# 旅行一覧ページ用View
# class IndexView(ListView):
class IndexView(TemplateView):
    template_name = "bookmarkapp/index.html"

index = IndexView.as_view()

class DetailView(TemplateView):
    template_name = "bookmarkapp/detail.html"

detail = DetailView.as_view()