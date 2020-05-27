from django.views.generic import ListView, DetailView, CreateView
from .models import TopListModel, DetailListModel, SubDetailListModel


# 旅行一覧ページ用View
class IndexView(ListView):
    template_name = "bookmarkapp/index.html"
    model = TopListModel

index = IndexView.as_view()

class DetailView(DetailView):
    template_name = "bookmarkapp/detail.html"
    model = TopListModel
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_list"] = DetailListModel.objects.filter(top__id=self.kwargs['pk']).order_by('date')
        context["sub_detail_list"] = SubDetailListModel.objects.filter(detail__top=self.kwargs['pk']).order_by('detail__date')
        context["top_info"] = context["sub_detail_list"][0].detail.top
        return context


detail = DetailView.as_view()

class TopCreateView(CreateView):
    template_name = "bookmarkapp/top_create.html"
    model = TopListModel
    fields = ('title', 'memo', 'date_from', 'date_to')

    def get_queryset(self):
        return TopListModel.objects.all()

top_create = CreateView.as_view()