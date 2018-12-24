from django.db import models
import datetime

# 施工業者情報
class ConstractorInfo(models.Model):
    username = models.CharField('ユーザー名', max_length=32)
    password = models.CharField('パスワード', max_length=32)
    registered = models.DateTimeField('登録日', default=datetime.datetime.now)
    constractor = models.CharField('会社名', max_length=256)
    representative = models.CharField('代表者　職氏名', max_length=256)
    address = models.CharField('所在地', max_length=512)
    tel = models.CharField('電話番号', max_length=16)

    def __str__(self):
        return str(self.id) + ': ' + self.constractor

# 工事申請情報
class RequestInfo(models.Model):
    username = models.CharField('ユーザー名', max_length=32) # 施工業者の識別ユーザー名
    registered = models.DateTimeField('提出日', auto_now_add=True)
    client = models.CharField('申請人', max_length=256)
    address = models.CharField('申請人 住所', max_length=512)
    tel = models.CharField('申請人 電話番号', max_length=16)
    constract = models.CharField('工事種別', max_length=1, choices=(('0', '新設'), ('1', '改造'), ('2', '増設')))
    place = models.CharField('施工場所', max_length=512)
    start = models.DateField('工事開始日')
    end = models.DateField('工事完了日')
    # 行政側操作項目
    condition = models.IntegerField('状態（0:申請中、1:要訂正、2:訂正済、3:許可済、4:完了済）', default=0)
    findings = models.TextField('指摘事項', blank=True)

    def __str__(self):
        return str(self.id) + ': ' + self.place
