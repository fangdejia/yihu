import logging
import requests
import uuid
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils import timezone
from wxapi.models import WxCredential,WxToken,WxSession,WpPosts,WpComments,WpUsers
logger = logging.getLogger(__name__)
def index(request):
    rep='''
    <html>
        <head><title>接口例示</title></head>
        <body>
            <a href="/wxapi/login/wx00c933316eb2b679/">小程序登录(需post方法发送code到服务器)</a></br>
            <a href="/wxapi/access_token/wx00c933316eb2b679/">获取access_token</a></br>
            <a href="/wxapi/posts/">获取文章列表</a></br>
            <a href="/wxapi/posts/197/">获取文章详情</a></br>
            <a href="/wxapi/comments/187/">根据post_id获取评论列表</a></br>
            <a href="/wxapi/comments/187/add/">根据post_id添加评论:需要post的数据至少有例子:({'comment_author':'令, 狐冲','comment_content':'测试测试'}),其他字段对应数据库字段为选填</a></br>
        </body>
    </html>

    '''
    return HttpResponse(rep)

def login(request,appid):
    code=request.POST.get('code' ,None)
    rep={'success':False,'token':''}
    if code:
        cs=WxCredential.objects.filter(appid=appid)
        logger.info(cs)
        if cs:
            cs=cs[0]
            data=requests.get("https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code"%(appid,cs.secret,code)).json()
            logger.info(data)
            if data.get("session_key",None):
                token=str(uuid.uuid1())
                rep={'success':True,'token':token}
                WxSession(token=token,session_key=data.get("session_key",""),open_id=data.get("openid",""),union_id=data.get("unionid","")).save()

    return JsonResponse(rep)


def get_access_token(request,appid):
    rep={'access_token':''}
    cs=WxCredential.objects.filter(appid=appid)
    if cs:
        cs=cs[0]
        tokens=WxToken.objects.filter(wx_credential=cs)
        nt=timezone.now()
        if tokens:
            tk=tokens[0]
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
    posts=WpPosts.objects.filter(post_type='post',post_status='publish').order_by("-id")[offset:limit]
    for p in posts:
        tb=p.wppostmeta_set.filter(meta_key='_thumbnail_id')
        if tb:
            p.thumb_url=WpPosts.objects.get(id=int(tb[0].meta_value)).guid
        else:
            p.thumb_url=''
        try:
            p.display_name=p.post_author.display_name
        except:
            p.display_name="unknown"
    return JsonResponse({'data':[{"id":p.id,'title':p.post_title,'post_date':p.post_date,'post_author':p.display_name ,'post_thumbnail_url':p.thumb_url} for p in posts]})

def get_post_detail(request,post_id):
    p=WpPosts.objects.get(id=post_id)
    tb=p.wppostmeta_set.filter(meta_key='_thumbnail_id')
    if tb:
        p.thumb_url=WpPosts.objects.get(id=int(tb[0].meta_value)).guid
    else:
        p.thumb_url=''
    return JsonResponse({"id":p.id,'title':p.post_title,'post_date':p.post_date,'post_author':p.post_author.display_name,'post_content':p.post_content,'post_thumbnail_url':p.thumb_url})

def get_post_comment(request,post_id):
    cms=WpComments.objects.filter(comment_post__id=post_id)
    data=[{'comment_author':c.comment_author,'comment_content':c.comment_content,'comment_date':c.comment_date,'comment_id':c.comment_id,'comment_parent':c.comment_parent} for c in cms]
    return JsonResponse({'data':data})

def add_comment(requests,post_id):
    comment_parent=int(requests.POST.get('comment_parent' ,'0'))
    comment_author=requests.POST.get('comment_author' ,'')
    comment_content=requests.POST.get('comment_content' ,'')
    comment_author_email=requests.POST.get('comment_author_email' ,'')
    comment_author_ip=requests.POST.get('comment_author_ip' ,'')
    comment_agent=requests.POST.get('comment_agent' ,'')
    comment_author_url=requests.POST.get('comment_author_url' ,'')
    rep={'success':False}
    p=WpPosts.objects.filter(id=post_id)
    if p and comment_content and comment_author:
        user=WpUsers.objects.filter(display_name=comment_author)
        user_id=user[0].id if user else 0
        WpComments(comment_author=comment_author,comment_content=comment_content,comment_author_url=comment_author_url,comment_author_email=comment_author_email,comment_author_ip=comment_author_ip,comment_agent=comment_agent,comment_post=p[0],user_id=user_id,comment_parent=comment_parent).save()
        rep={'success':True}
    return JsonResponse(rep)



