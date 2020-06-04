from django.db import models
from stdimage.models import StdImageField  #追

class TopListModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    memo = models.CharField(max_length=100)
    date_from = models.DateField(auto_now=False)
    date_to = models.DateField(auto_now=False)
    images = StdImageField(upload_to='', blank=True, null=True, variations={
        'medium': (200, 200, True),
    })

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            original_profile = TopListModel.objects.get(pk=self.pk)
            if original_profile.images:
                original_profile.images.delete(save=False)

        except self.DoesNotExist:
            pass

        super(TopListModel, self).save(*args, **kwargs)

class DetailListModel(models.Model):
    detail_id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=False)
    main_content = models.CharField(max_length=100)
    top = models.ForeignKey(TopListModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.main_content

class SubDetailListModel(models.Model):
    sub_detail_id = models.AutoField(primary_key=True)
    time = models.TimeField(auto_now=False)
    main_content = models.CharField(max_length=100)
    images = StdImageField(upload_to='', blank=True, null=True, variations={
        'medium': (200, 200, True),
    })
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
    detail = models.ForeignKey(DetailListModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.main_content

    def save(self, *args, **kwargs):
        try:
            original_profile = SubDetailListModel.objects.get(pk=self.pk)
            if original_profile.images:
                original_profile.images.delete(save=False)

        except self.DoesNotExist:
            pass

        super(SubDetailListModel, self).save(*args, **kwargs)

