from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from .models import TopListModel, DetailListModel, SubDetailListModel, DetailWork
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views import generic
from .forms import TopForm, DetailForm, SubDetailForm, DetailWorkForm, DetailIdForm
from django.db.models import Max

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

# 旅行情報作成用View（３STEP）
class TopCreateStepView(FormView):
    template_name = "bookmarkapp/top_create.html"
    form_class = TopForm

    # post実行時のvalueによって処理を分岐
    def post(self, request, *args, **kwargs):
        ctx = {}
        # top_infoをセッションから取得し、条件分岐に応じて追加で処理を行う
        if request.POST.get('next', '') in ('back_top', 'back_detail', 'edit_top', 'detail_confirm', 'detail_edit', 'detail_update', 'detail_delete', 'save_and_add'):
            if 'top_info' in request.session:
                top_info = request.session['top_info']
                top_form = TopForm(top_info)
                ctx['top_info'] = top_form
                # top編集画面に戻った場合は画面表示のみ
                if request.POST.get('next', '') == 'back_top':
                    return render(request, self.template_name, ctx)
                # detail編集画面に戻った場合はwork情報を取得し表示
                elif request.POST.get('next', '') == 'back_detail':
                    ctx['detail_work'] = DetailWork.objects.all().order_by('date')
                    return render(request, 'bookmarkapp/detail_step.html', ctx)
                # top編集画面を修正する場合はボタンを制御するためにconfirmed_flgを立てる
                elif request.POST.get('next', '') == 'edit_top':
                    ctx['confirmed'] = '1'
                    return render(request, self.template_name, ctx)
                # detail編集画面から確認画面に遷移する場合はwork情報を取得し表示
                elif request.POST.get('next', '') == 'detail_confirm':
                    ctx['detail_work'] = DetailWork.objects.all().order_by('date')
                    return render(request, 'bookmarkapp/confirm_step.html', ctx)
                # detail編集画面でwork情報を編集する場合はwork情報と選択行の情報を取得
                elif request.POST.get('next', '') == 'detail_edit':
                    detail_id_form = DetailIdForm(request.POST)
                    if detail_id_form.is_valid():
                        ctx['detail_work'] = DetailWork.objects.all().order_by('date')
                        ctx['selected_detail'] = DetailWork.objects.filter(id=detail_id_form.cleaned_data['detail_id'])
                        return render(request, 'bookmarkapp/detail_step.html', ctx) 
                # detail編集画面で選択したwork情報を更新する場合は更新処理を行い、表示のため更新後work情報を取得
                elif request.POST.get('next', '') == 'detail_update':
                    detail_id_form = DetailIdForm(request.POST)
                    if detail_id_form.is_valid():
                        selected_detail = get_object_or_404(DetailWork, id=detail_id_form.cleaned_data['detail_id'])
                        detail_work_form = DetailWorkForm(request.POST, instance=selected_detail)
                        if detail_work_form.is_valid():
                            detail_work_form.save()
                            messages.success(self.request, f'予定を修正しました。')
                            ctx['detail_work'] = DetailWork.objects.all().order_by('date')
                            return render(request, 'bookmarkapp/detail_step.html', ctx) 
                # detail編集画面で選択したwork情報を削除する場合は削除処理を行い、表示のため更新後work情報を取得
                elif request.POST.get('next', '') == 'detail_delete':
                    detail_id_form = DetailIdForm(request.POST)
                    if detail_id_form.is_valid():
                        DetailWork.objects.filter(id=detail_id_form.cleaned_data['detail_id']).delete()
                        messages.success(self.request, f'予定を削除しました。')
                        ctx['detail_work'] = DetailWork.objects.all().order_by('date')
                        return render(request, 'bookmarkapp/detail_step.html', ctx) 
                # detail編集画面でワーク情報を登録する場合
                elif request.POST.get('next', '') == 'save_and_add':
                    detail_work_form = DetailWorkForm(request.POST)
                    if detail_work_form.is_valid():
                        # ワークテーブルに登録
                        date = detail_work_form.cleaned_data['date']
                        main_content=detail_work_form.cleaned_data['main_content']
                        detail_work_form.save()
                        # ワークテーブルを取得
                        ctx['detail_work'] = DetailWork.objects.all().order_by('date')
                        messages.success(self.request, f'予定を作成しました。  日付:{date},　やること:{main_content}')
                        return render(request, 'bookmarkapp/detail_step.html', ctx)
                    else:
                        messages.error(self.request, "値に不正があります。")
                        return render(request, 'bookmarkapp/detail_step.html', ctx)

        # top編集画面からdetail編集画面または確認画面に遷移した場合
        elif request.POST.get('next', '') in ('create_detail','top_confirm'):
            form = TopForm(request.POST)
            if form.is_valid():
                ctx = {'top_info': form}
                # セッションに編集したtop情報を保存
                top_info = {
                    'title': form.cleaned_data['title'],
                    'memo': form.cleaned_data['memo'],
                    'date_from': form.cleaned_data['date_from'].isoformat(),
                    'date_to': form.cleaned_data['date_to'].isoformat(),
                }
                request.session['top_info'] = top_info
                if request.POST.get('next', '') == 'create_detail':
                    # ワーク情報を削除
                    DetailWork.objects.all().delete()
                    # 戻るボタンを表示させるためフラグを立てる
                    ctx['top_to_detail'] = 1
                    return render(request, 'bookmarkapp/detail_step.html', ctx)
                else:
                    # ワーク情報を取得
                    ctx["detail_work"] = DetailWork.objects.all().order_by('date')
                    return render(request, 'bookmarkapp/confirm_step.html', ctx)
                
            else:
                messages.error(self.request, "値に不正があります。")
                return render(request, self.template_name, {'top_info': form})

        # 確認画面でデータを登録する場合
        elif request.POST.get('next', '') == 'create':
            if 'top_info' in request.session:
                title = request.session['top_info']['title']
                # top_infoの値をセッションから取得し登録
                TopListModel.objects.create_top_list(
                    title=title,
                    memo=request.session['top_info']['memo'],
                    date_from=request.session['top_info']['date_from'],
                    date_to=request.session['top_info']['date_to'],
                )
                # detailの情報をワークから取得し登録
                detail_works = DetailWork.objects.all().order_by('date')
                top = TopListModel.objects.all().aggregate(Max('id'))
                for detail in detail_works:
                    DetailListModel.objects.create_detail_list(
                        date=detail.date,
                        main_content=detail.main_content,
                        top_id=top['id__max']
                    )
                # ワークテーブルの削除
                DetailWork.objects.all().delete()
                messages.success(self.request, f'旅のしおりを作成しました。 タイトル:{title}')
                # セッションに保管した情報の削除
                request.session.pop('top_info')

                return redirect(reverse_lazy('bookmarkapp:index'))

top_create = TopCreateStepView.as_view()