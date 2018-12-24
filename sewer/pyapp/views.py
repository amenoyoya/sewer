from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ConstractorInfo, RequestInfo
from .forms import LoginForm, ConstractorForm, RequestForm

# ログイン判定デコレーター
def is_login(func):
    def wrapper(request, *args):
        username = request.session.get('username')
        if username is None: # ユーザー名がセッションに保存されていなければloginページにリダイレクト
            return redirect('pyapp:login')
        try:
            obj = ConstractorInfo.objects.get(username=username)
            return func(request, obj, *args)
        except ConstractorInfo.DoesNotExist: # 有効なユーザー名でなければloginページにリダイレクト
            return redirect('pyapp:login')
    return wrapper


# ログインページ
def login(request):
    args = {
        'message': '',
        'form': LoginForm(),
    }
    if request.method == 'POST':
        try:
            obj = ConstractorInfo.objects.get(username=request.POST['username'])
            if obj.password == request.POST['password']: # ログイン成功
                request.session['username'] = obj.username # ユーザー名をセッションに保存
                print(request.session['username'])
                return redirect('pyapp:mypage')
        except ConstractorInfo.DoesNotExist: # ログイン失敗
            args['message'] = '<p class="alert alert-warning" role="alert">ユーザー名もしくはパスワードが違います</p>'
    return render(request, 'login.html', args)


# ログアウトページ
def logout(request):
    request.session.clear() # セッションクリア
    return render(request, 'logout.html')


# マイページ
@is_login
def mypage(request, constractor):
    args = {
        'constractor': constractor,
        'form': ConstractorForm(instance=constractor), # ログイン中の施工業者の情報を編集可能に
        'message': '',
    }
    try:
        args['problem_requests'] = RequestInfo.objects.filter(username=constractor.username).filter(condition=1).order_by('id')
        args['allowed_requests'] = RequestInfo.objects.filter(username=constractor.username).filter(condition=3).order_by('id')
        args['recieved_requests'] = RequestInfo.objects.filter(username=constractor.username).filter(condition=0).order_by('id')
        args['exam_requests'] = RequestInfo.objects.filter(username=constractor.username).filter(condition=2).order_by('id')
    except RequestInfo.DoesNotExist:
        args['problem_requests'] = [] # 要訂正申請書
        args['allowed_requests'] = [] # 許可済み申請書
        args['recieved_requests'] = [] # 収受済み申請書（審査中申請書）
        args['exam_requests'] = [] # 訂正済み申請書（審査中申請書）
    
    if request.method == 'POST': # POST送信で業者情報の変更
        for key, post in request.POST.items():
            setattr(constractor, key, post) # POST情報を全てモデルに反映
        constractor.save() # 業者情報更新
        args['form'] = ConstractorForm(instance=constractor) # フォームの内容が変わっているため更新
        args['message'] = '<p class="alert alert-success" role="alert">業者情報を更新しました</p>'
    return render(request, 'mypage.html', args)


# GET['id']で指定された申請書が編集可能か判定
# return [True/False, RequestInfo]
def is_editable(request, constractor):
    ID = request.GET.get('id')
    if ID is None:
        return False, None
    else:
        try:
            obj = RequestInfo.objects.get(id=ID)
            return obj.username == constractor.username and obj.condition == 1, obj
        except RequestInfo.DoesNotExist:
            return False, None

# GET['id']で指定された申請書が閲覧可能か判定
# return [True/False, RequestInfo]
def is_redable(request, constractor):
    ID = request.GET.get('id')
    if ID is None:
        return False, None
    else:
        try:
            obj = RequestInfo.objects.get(id=ID)
            return obj.username == constractor.username, obj
        except RequestInfo.DoesNotExist:
            return False, None

# 申請書編集・追加ページ
@is_login
def request_constract(request, constractor):
    args = {
        'id': 0, # GETで渡すID（0ならGETなし）
        'constractor': constractor,
        'form': RequestForm(),
        'btn_tag': '<input class="btn btn-primary form-control" type="submit" value="追加">',
        'message': '',
    }
    editabled, req = is_editable(request, constractor)
    if editabled: # ログイン中の業者が申請した申請書のみ編集可能
        args['form'] = RequestForm(instance=req)
        args['btn_tag'] = '<input class="btn btn-primary form-control" type="submit" value="決定">'
        # 指摘事項を表示
        args['message'] = '<p class="alert alert-warning" role="alert">' + req.findings + '</p>'
        # POST送信するときに渡すGET['id']
        args['id'] = request.GET.get('id')
    
    if request.method == 'POST':  # POST送信で申請書の追加・修正
        if editabled: # 申請書の修正
            for key, post in request.POST.items():
                print(key, post)
                setattr(req, key, post)
            req.condition = 2
            req.save()
            args['message'] = '<p class="alert alert-success" role="alert">申請書を訂正しました</p>'
        else: # 申請書の追加
            RequestInfo.objects.create(
                username = constractor.username,
                client = request.POST['client'],
                address = request.POST['address'],
                tel = request.POST['tel'],
                constract = request.POST['constract'],
                place = request.POST['place'],
                start = request.POST['start'],
                end = request.POST['end'],
                condition = 0
            )
            args['message'] = '<p class="alert alert-success" role="alert">新しい申請書を受理しました</p>'
        # 送信ボタンを押せなくする
        args['btn_tag'] = '<input class="btn btn-primary form-control disabled" type="submit" value="現在審査中です" aria-diabled="true">'
    return render(request, 'request.html', args)


# 申請書閲覧ページ
@is_login
def preview_constract(request, constractor):
    readabled, obj = is_redable(request, constractor)
    constract = ['新設', '改造', '増設']
    return render(request, 'preview.html', {
        'constractor': constractor,
        'client': obj.client if readabled else '－',
        'address': obj.address if readabled else '－',
        'tel': obj.tel if readabled else '－',
        'constract': constract[int(obj.constract)] if readabled else '－',
        'place': obj.place if readabled else '－',
        'start': obj.start if readabled else '－',
        'end': obj.end if readabled else '－',
        'findings': obj.findings if readabled else '－',
    })