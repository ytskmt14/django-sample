import datetime

from django.contrib import messages
from django.db.models import Max
from django.forms import formset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView

from .forms import TopForm, DetailForm, SubDetailForm, DetailIdForm
from .models import TopListModel, DetailListModel, SubDetailListModel

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

         # 保存してもう一つ追加ボタンのとき
        if 'save_and_add' in self.request.POST:
            return redirect(reverse("bookmarkapp:detail_create", kwargs={"pk": self.kwargs['pk']}))

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

                 # 保存してもう一つ追加ボタンのとき
        if 'save_and_add' in self.request.POST:
            return redirect(reverse("bookmarkapp:sub_detail_create", kwargs={"top_pk": self.kwargs['top_pk'], "detail_pk": self.kwargs['detail_pk']}))

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

def top_create(request):
    """
    旅行情報作成（Step1）のView
    TopListModelに対応するデータを扱う
    """
    if request.method == 'GET':
        top_info = request.session.get('top_info')
        detail_info = request.session.get('detail_info')
        return render(request, "bookmarkapp/top_create.html", {'top_info':top_info})
    elif request.method == 'POST':
        form = TopForm(request.POST)
        if form.is_valid():
            # セッションに編集したtop情報を保存
            top_info = {
                'title': form.cleaned_data['title'],
                'memo': form.cleaned_data['memo'],
                'date_from': form.cleaned_data['date_from'].isoformat(),
                'date_to': form.cleaned_data['date_to'].isoformat(),
            }
            request.session['top_info'] = top_info
            return redirect('bookmarkapp:plan_create')
        else:
            messages.error(request, "値に不正があります。")
            return render(request, "bookmarkapp/top_create.html", {'top_info':top_info})

def plan_create(request):
    """
    旅行情報作成（Step2）のView
    DetailListModelに対応するデータを扱う
    """
    session_top_info = request.session.get('top_info')
    if session_top_info is None:
        # セッション情報を持たなければ、step1にリダイレクト
        return redirect('bookmarkapp:top_create')
    else:
        date_from = datetime.datetime.strptime(session_top_info['date_from'], '%Y-%m-%d')
        date_to = datetime.datetime.strptime(session_top_info['date_to'], '%Y-%m-%d')
        time_delta = date_to - date_from

        DetailCreateFormSet = formset_factory(
            form=DetailForm, extra= time_delta.days + 1 ,max_num= time_delta.days + 1
        )

    if request.method == 'GET':
        formset = DetailCreateFormSet()
        date_list = []
        for i in range(time_delta.days + 1):
            date = date_from + datetime.timedelta(days=i)
            date_list.append(date.strftime("%Y-%m-%d"))

        ctx = {'formset': formset, 'top_info': session_top_info, 'time_delta': time_delta.days + 1, 'date_list': date_list}
        return render(request, 'bookmarkapp/detail_step.html', ctx)
    elif request.method == 'POST':
        formset = DetailCreateFormSet(request.POST)
        if formset.is_valid():
            detail_info = {}
            date_list = formset.data.getlist('date')
            main_content_list = formset.data.getlist('main_content')
            for index, date in enumerate(date_list):
                detail_info[index] = {
                    'date': date_list[index],
                    'main_content': main_content_list[index],
                }
            request.session['detail_info'] = detail_info
            return redirect(reverse("bookmarkapp:confirm"))
        else:
            formset = DetailCreateFormSet(request.POST)
            return render(request, 'bookmarkapp/detail_step.html', {'formset': formset})

def confirm(request):
    """
    旅行情報作成（Step3）のView
    入力情報の確認を行う。
    """
    top_info = request.session.get('top_info')
    detail_info = request.session.get('detail_info')

    if top_info is None or detail_info is None:
        print('top_info or detail_info is None')
        # セッション情報を持たなければ、step1にリダイレクト
        return redirect('bookmarkapp:top_create')
    else:
        if request.method == 'GET':
            ctx = {
                'top_info': top_info,
                'detail_info': detail_info
            }
            return render(request, "bookmarkapp/confirm_step.html", ctx)
        elif request.method == 'POST':
            return render(request, "bookmarkapp/index.html")