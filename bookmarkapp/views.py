from django.views.generic import ListView, DetailView, TemplateView

# 旅行一覧ページ用View
# class IndexView(ListView):
class IndexView(TemplateView):
    template_name = "bookmarkapp/index.html"

index = IndexView.as_view()

class DetailView(TemplateView):
    template_name = "bookmarkapp/detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # サンプル用の固定データを詰める
        # 日程の一覧
        context['schedule_list'] = {
          '2020/01/01', '2020/01/02',
        }
        # 予定の時間と概要を表す変数
        context['plan_list'] = {
          '1': {
            'date': '2020/01/01',
            'estimated_time': '11:00',
            'name': 'マーケット1で買い物',
            'todos': {
              'どうしても買いたいお土産があるので買う。',
              '予算は3000円',
              '値下げ交渉をする。',
              'もっと値下げ交渉をする。',
            }
          },
          '2': {
            'date': '2020/01/01',
            'estimated_time': '12:00',
            'name': 'マーケット2で買い物',
          },
          '3': {
            'date': '2020/01/01',
            'estimated_time': '13:00',
            'name': 'マーケット3で買い物',
          },
          '4': {
            'date': '2020/01/02',
            'estimated_time': '11:00',
            'name': 'マーケット4で買い物',
          },
          '5': {
            'date': '2020/01/02',
            'estimated_time': '12:00',
            'name': 'マーケット5で買い物',
          },
          '6': {
            'date': '2020/01/02',
            'estimated_time': '13:00',
            'name': 'マーケット6で買い物',
          },
        }
        return context

detail = DetailView.as_view()
