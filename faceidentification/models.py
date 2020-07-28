from django.db import models
# todo журнал посещения
# todo база данных с доступом


class Info_about_face(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', verbose_name="Имя", max_length=255)
    status = models.CharField(db_column='status', verbose_name="Доступ",
                              help_text="Укажите номера офисов резидента", max_length=255)
    path_screen = models.CharField(db_column='path_screen', max_length=255)
    date = models.DateTimeField(auto_now=False)
    path_image = models.CharField(db_column='path_image', max_length=255)

    def __str__(self):
        return f'{self.name} - {self.status}'

    class Meta:
        # managed = False
        db_table = 'journal'


class  Access_status(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', verbose_name='Имя', help_text='Введите имя резидента', max_length=255)
    status = models.CharField(db_column='status', verbose_name='Уровень допуска',
                              help_text="Укажете номера офисов, к которым у резидента есть доступ", max_length=255)
    # path_image = models.CharField(db_column='path_image', max_length=255)
    path_download = models.ImageField(upload_to='media/', verbose_name="Фотография резидента")

    def __str__(self):
        return f"{self.name} - {self.status}"

    class Meta:
        # managed = False
        verbose_name = "Резидент"
        verbose_name_plural = "Резиденты"
        db_table = 'access'
        ordering = ['id']

# class Names(models.Model):
#     id
# class Addon(models.Model):
#     image = models.FileField(upload_to='media/', null=True)
#     addon_name = models.CharField(max_length=100, null=False, blank=False)
#
# class Image_model(models.Model):
#     img = models.ImageField(blank=True, upload_to='media/roman.jpg',
#                             help_text='150x150px', verbose_name='Ссылка картинки')


