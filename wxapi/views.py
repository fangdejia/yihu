import requests
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils import timezone
from wxapi.models import WxCredential,WxToken,WpPosts
def index(request):
    rep='''
    <html>
        <head><title>接口例示</title></head>
        <body>
            <a href="/wxapi/access_token/wx00c933316eb2b679/">获取access_token</a></br>
            <a href="/wxapi/posts/">获取文章列表</a></br>
            <a href="/wxapi/posts/197">获取文章详情</a></br>
        </body>
    </html>

    '''
    return HttpResponse(rep)

def get_access_token(request,appid):
    rep={'access_token':''}
    cs=WxCredential.objects.filter(appid=appid)
    if cs:
        cs=cs[0]
        tokens=WxToken.objects.filter(wx_credential=cs)
        if tokens:
            tk=tokens[0]
            nt=timezone.now()
            if tk.expires_time>nt:
                rep['access_token']=tk.access_token
            else:
                data=requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(appid,cs.secret)).json()
                rep['access_token']=data['access_token']
                tk.access_token,tk.expires_time=data['access_token'],nt+timedelta(seconds=data['expires_in']-300)
                tk.save()
        else:
            data=requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(appid,cs.secret)).json()
            rep['access_token']=data['access_token']
            WxToken(access_token=data['access_token'],expires_time=nt+timedelta(seconds=data['expires_in']-300),wx_credential=cs).save()
    return JsonResponse(rep)

def get_post_titles(request):
    current_page=int(request.GET.get('page' ,'1'))
    page_size=int(request.GET.get('page_size' ,'25'))
    limit=page_size*current_page
    offset=limit-page_size
    posts=WpPosts.objects.filter(post_type='post',post_status='publish')[offset:limit]
    for p in posts:
        tb=p.wppostmeta_set.filter(meta_key='_thumbnail_id')
        if tb:
            p.thumb_url=WpPosts.objects.get(id=int(tb[0].meta_value)).guid
        else:
            p.thumb_url=''
    return JsonResponse({'data':[{"id":p.id,'title':p.post_title,'post_date':p.post_date,'post_author':p.post_author.display_name,'post_thumbnail_url':p.thumb_url} for p in posts]})

def get_post_detail(request,post_id):
    p=WpPosts.objects.get(id=post_id)
    tb=p.wppostmeta_set.filter(meta_key='_thumbnail_id')
    if tb:
        p.thumb_url=WpPosts.objects.get(id=int(tb[0].meta_value)).guid
    else:
        p.thumb_url=''
    return JsonResponse({"id":p.id,'title':p.post_title,'post_date':p.post_date,'post_author':p.post_author.display_name,'post_content':p.post_content,'post_thumbnail_url':p.thumb_url})
