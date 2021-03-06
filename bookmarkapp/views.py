from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import TopListModel, DetailListModel, SubDetailListModel
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views import generic
from .forms import TopForm, DetailForm, SubDetailForm

# 旅行一覧ページ用View
class IndexView(ListView):
    template_name = "bookmarkapp/index.html"
    def get_queryset(self):
        return TopListModel.objects.order_by('date_from').reverse()

index = IndexView.as_view()

# 旅行詳細ページ用View
class DetailView(DetailView):
    template_name = "bookmarkapp/detail.html"
    model = TopListModel
    context_object_name = 'top_info'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_list"] = DetailListModel.objects.filter(top__id=self.kwargs['pk']).order_by('date')
        context["sub_detail_list"] = SubDetailListModel.objects.filter(detail__top=self.kwargs['pk']).order_by('detail__date')
        return context

detail = DetailView.as_view()

# 旅行メイン情報作成用View
class TopCreateView(CreateView):
    template_name = "bookmarkapp/top_create.html"
    model = TopListModel
    form_class = TopForm
    success_url = reverse_lazy("bookmarkapp:index")

    # メッセージの表示
    def form_valid(self, form):
        # バリデーションに成功した時
        self.object = post = form.save()
        messages.success(self.request, f'旅のしおりを作成しました。 タイトル:{post.title}')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # バリデーションに失敗した時
        messages.error(self.request, "登録できませんでした。")
        return super().form_invalid(form)
        
top_create = TopCreateView.as_view()

# 旅行詳細情報作成用View
class DetailCreateView(CreateView):
    template_name = "bookmarkapp/detail_create.html"
    model = DetailListModel
    form_class = DetailForm
    context_object_name = 'detail_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_info'] = TopListModel.objects.filter(id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse("bookmarkapp:detail", kwargs={"pk": self.kwargs['pk']})

    # メッセージの表示
    def form_valid(self, form):
        # バリデーションに成功した時
        self.object = post = form.save()
        messages.success(self.request, f'旅のしおり詳細を作成しました。  日付:{post.date},　やること:{post.main_content}')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # バリデーションに失敗した時
        messages.error(self.request, "登録できませんでした。")
        return super().form_invalid(form)
    

detail_create = DetailCreateView.as_view()

# 旅行副詳細情報作成用View
class SubDetailCreateView(CreateView):
    template_name = "bookmarkapp/sub_detail_create.html"
    model = SubDetailListModel
    form_class = SubDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_info'] = TopListModel.objects.filter(id=self.kwargs['top_pk'])
        context["detail_list"] = DetailListModel.objects.filter(detail_id=self.kwargs['detail_pk'])
        return context

    def get_success_url(self):
        return reverse("bookmarkapp:detail", kwargs={"pk": self.kwargs['top_pk']})

    # メッセージの表示
    def form_valid(self, form):
        # バリデーションに成功した時
        self.object = post = form.save()
        messages.success(self.request, f'旅のしおり副詳細を修正しました。 日付:{post.detail.date},　時間:{post.time},　やること:{post.main_content}')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # バリデーションに失敗した時
        messages.error(self.request, "登録できませんでした。")
        return super().form_invalid(form)
        
sub_detail_create = SubDetailCreateView.as_view()

# 旅行メイン情報修正用View
class TopUpdateView(UpdateView):
    template_name = "bookmarkapp/top_update.html"
    model = TopListModel
    form_class = TopForm
    success_url = reverse_lazy("bookmarkapp:index")
    context_object_name = 'top_info'

    # メッセージの表示
    def form_valid(self, form):
        # バリデーションに成功した時
        self.object = post = form.save()
        messages.success(self.request, f'旅のしおりを修正しました。 タイトル:{post.title}')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # バリデーションに失敗した時
        messages.error(self.request, "更新できませんでした。")
        return super().form_invalid(form)

top_update = TopUpdateView.as_view()    

# 旅行詳細情報修正用View
class DetailUpdateView(UpdateView):
    template_name = "bookmarkapp/detail_update.html"
    model = DetailListModel
    form_class = DetailForm
    context_object_name = 'detail_list'

    def get_queryset(self):
        return super().get_queryset().select_related('top')

    def get_success_url(self):
        return reverse("bookmarkapp:detail", kwargs={"pk": self.kwargs['top_pk']})

    # メッセージの表示
    def form_valid(self, form):
        # バリデーションに成功した時
        self.object = post = form.save()
        messages.success(self.request, f'旅のしおりを修正しました。  日付:{post.date},　やること:{post.main_content}')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # バリデーションに失敗した時
        messages.error(self.request, "更新できませんでした。")
        return super().form_invalid(form)

detail_update = DetailUpdateView.as_view()

# 旅行副詳細情報修正用View
class SubDetailUpdateView(UpdateView):
    template_name = "bookmarkapp/sub_detail_update.html"
    model = SubDetailListModel
    form_class = SubDetailForm
    context_object_name = 'sub_detail_list'

    def get_queryset(self):
        return super().get_queryset().select_related('detail__top')

    def get_success_url(self):
        return reverse("bookmarkapp:detail", kwargs={"pk": self.kwargs['top_pk']})

    # メッセージの表示
    def form_valid(self, form):
        # バリデーションに成功した時
        self.object = post = form.save()
        message = f'旅のしおり副詳細を修正しました。 日付:{post.detail.date},　時間:{post.time},　やること:{post.main_content}'
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # バリデーションに失敗した時
        messages.error(self.request, "更新できませんでした。")
        return super().form_invalid(form)

sub_detail_update = SubDetailUpdateView.as_view()


# 旅行メイン情報削除用View
class TopDeleteView(DeleteView):
    template_name = "bookmarkapp/top_delete.html"
    model = TopListModel
    success_url = reverse_lazy("bookmarkapp:index")

    # メッセージの表示
    def delete(self, request, *args, **kwargs):
        # 削除に成功したとき
        self.object = post = self.get_object()
        message = f'旅のしおりを削除しました。 タイトル:{post.title}'
        post.delete()
        messages.success(self.request, message)
        return redirect(self.get_success_url())

top_delete = TopDeleteView.as_view()

# 旅行詳細情報削除用View
class DetailDeleteView(DeleteView):
    template_name = "bookmarkapp/detail_delete.html"
    model = DetailListModel
    context_object_name = 'detail_list'

    def get_queryset(self):
        return super().get_queryset().select_related('top')

    def get_success_url(self):
        return reverse("bookmarkapp:detail", kwargs={"pk": self.kwargs['top_pk']})

    # メッセージの表示
    def delete(self, request, *args, **kwargs):
        # 削除に成功したとき
        self.object = post = self.get_object()
        message = f'旅のしおり詳細を削除しました。 日付:{post.date},　やること:{post.main_content}'
        post.delete()
        messages.success(self.request, message)
        return redirect(self.get_success_url())

detail_delete = DetailDeleteView.as_view()

# 旅行副詳細情報削除用View
class SubDetailDeleteView(DeleteView):
    template_name = "bookmarkapp/sub_detail_delete.html"
    model = SubDetailListModel
    context_object_name = 'sub_detail_list'

    def get_queryset(self):
        return super().get_queryset().select_related('detail__top')

    def get_success_url(self):
        return reverse("bookmarkapp:detail", kwargs={"pk": self.kwargs['top_pk']})

    # メッセージの表示
    def delete(self, request, *args, **kwargs):
        # 削除に成功したとき
        self.object = post = self.get_object()
        message = f'旅のしおり副詳細を削除しました。 日付:{post.detail.date},　時間:{post.time},　やること:{post.main_content}'
        post.delete()
        messages.success(self.request, message)
        return redirect(self.get_success_url())

sub_detail_delete = SubDetailDeleteView.as_view()
