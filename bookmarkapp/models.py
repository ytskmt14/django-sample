from django.db import models

class TopListModel(models.Model):
    top_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    memo = models.CharField(max_length=100)
    date_from = models.DateField(auto_now=False)
    date_to = models.DateField(auto_now=False)
    # 未実装
    # image_path = models.FilePathField
    def __str__(self):
        return self.title

class DetailListModel(models.Model):
    detail_id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=False)
    main_content = models.CharField(max_length=100)
    top_id = models.ForeignKey(TopListModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.main_content

class SubDetailListModel(models.Model):
    sub_detail_id = models.AutoField(primary_key=True)
    time = models.TimeField(auto_now=False)
    main_content = models.CharField(max_length=100)
    hp_url = models.CharField(max_length=200, null=True, blank=True)
    map_url = models.CharField(max_length=200, null=True, blank=True)
    root_url = models.CharField(max_length=200, null=True, blank=True)
    content1 = models.CharField(max_length=100, null=True, blank=True)
    content2 = models.CharField(max_length=100, null=True, blank=True)
    content3 = models.CharField(max_length=100, null=True, blank=True)
    content4 = models.CharField(max_length=100, null=True, blank=True)
    content5 = models.CharField(max_length=100, null=True, blank=True)
    content6 = models.CharField(max_length=100, null=True, blank=True)
    content7 = models.CharField(max_length=100, null=True, blank=True)
    content8 = models.CharField(max_length=100, null=True, blank=True)
    content9 = models.CharField(max_length=100, null=True, blank=True)
    content10 = models.CharField(max_length=100, null=True, blank=True)
    detail_id = models.ForeignKey(DetailListModel, on_delete=models.CASCADE)
                 
    # 未実装
    # image_path = models.FilePathField
    def __str__(self):
        return self.main_content

