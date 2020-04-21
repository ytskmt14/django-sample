from django.views.generic import TemplateView

# 旅行一覧ページ用View
class IndexView(TemplateView):
    template_name = "bookmarkapp/index.html"

index = IndexView.as_view()