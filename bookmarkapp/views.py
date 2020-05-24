from django.views.generic import ListView, DetailView, CreateView
from .models import TopListModel, DetailListModel, SubDetailListModel


# 旅行一覧ページ用View
class IndexView(ListView):
    template_name = "bookmarkapp/index.html"

    def get_queryset(self):
        return TopListModel.objects.order_by('date_from').reverse()

index = IndexView.as_view()

class DetailView(DetailView):
    template_name = "bookmarkapp/detail.html"
    model = DetailListModel
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_info"] = TopListModel.objects.filter(detaillistmodel__detail_id=self.kwargs['pk']).get()
        context["sub_detail_list"] = SubDetailListModel.objects.filter(detail_id=self.kwargs['pk'])
        return context


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["detail"] = DetailListModel.objects.get(pk=1)
    #     return context

    # def get_queryset(self):
    #     # return DetailListModel.objects.filter(top_id__exact=1).order_by('date').reverse()
    #     return DetailListModel.objects.order_by('subdetaillistmodel__time')
    # def get_context_data(self, *args, **kwargs):
    #     context = super(DetailView, self).get_context_data(*args, **kwargs)
    #     context['detail_objects'] = DetailListModel.objects.filter(top_id__exact=1).order_by('date').reverse()
    #     context['sub_detail_objects'] = SubDetailListModel.objects.filter(detail_id__exact=1).order_by('date').reverse()
    #     return context

detail = DetailView.as_view()

class TopCreateView(CreateView):
    template_name = "bookmarkapp/top_create.html"
    model = TopListModel
    fields = ('title', 'memo', 'date_from', 'date_to')

    def get_queryset(self):
        return TopListModel.objects.all()

top_create = CreateView.as_view()