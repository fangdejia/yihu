from django.db import models
from django.utils.timezone import now
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table

class WpUsers(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user_login = models.CharField(max_length=60)
    user_pass = models.CharField(max_length=255)
    user_nicename = models.CharField(max_length=50)
    user_email = models.CharField(max_length=100)
    user_url = models.CharField(max_length=100)
    user_registered = models.DateTimeField()
    user_activation_key = models.CharField(max_length=255)
    user_status = models.IntegerField()
    display_name = models.CharField(max_length=250)

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_users'


class WpBpCronConfig(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    token = models.CharField(max_length=200, blank=True, null=True)
    open = models.IntegerField()

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_bp_cron_config'


class WpBpProfile(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    token = models.CharField(max_length=200, blank=True, null=True)
    count = models.SmallIntegerField()

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_bp_profile'


class WpCommentmeta(models.Model):
    meta_id = models.BigAutoField(primary_key=True)
    comment_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_commentmeta'



class WpLinks(models.Model):
    link_id = models.BigAutoField(primary_key=True)
    link_url = models.CharField(max_length=255)
    link_name = models.CharField(max_length=255)
    link_image = models.CharField(max_length=255)
    link_target = models.CharField(max_length=25)
    link_description = models.CharField(max_length=255)
    link_visible = models.CharField(max_length=20)
    link_owner = models.BigIntegerField()
    link_rating = models.IntegerField()
    link_updated = models.DateTimeField()
    link_rel = models.CharField(max_length=255)
    link_notes = models.TextField()
    link_rss = models.CharField(max_length=255)

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_links'


class WpMessages(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.BigIntegerField()
    receiver = models.BigIntegerField()
    content = models.TextField()
    status = models.IntegerField()
    time = models.IntegerField()

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_messages'


class WpOptions(models.Model):
    option_id = models.BigAutoField(primary_key=True)
    option_name = models.CharField(unique=True, max_length=191)
    option_value = models.TextField()
    autoload = models.CharField(max_length=20)

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_options'



class WpPosts(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    post_author = models.ForeignKey(WpUsers,db_column='post_author',on_delete=models.SET_NULL,null=True)
    post_date = models.DateTimeField()
    post_date_gmt = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(max_length=20)
    comment_status = models.CharField(max_length=20)
    ping_status = models.CharField(max_length=20)
    post_password = models.CharField(max_length=255)
    post_name = models.CharField(max_length=200)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField()
    post_modified_gmt = models.DateTimeField()
    post_content_filtered = models.TextField()
    post_parent = models.BigIntegerField()
    guid = models.CharField(max_length=255)
    menu_order = models.IntegerField()
    post_type = models.CharField(max_length=20)
    post_mime_type = models.CharField(max_length=100)
    comment_count = models.BigIntegerField()

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_posts'


class WpPostmeta(models.Model):
    meta_id = models.BigAutoField(primary_key=True)
    post_id = models.ForeignKey(WpPosts,db_column='post_id',on_delete=models.SET_NULL,null=True)
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_postmeta'

class WpComments(models.Model):
    comment_id = models.BigAutoField(db_column='comment_ID', primary_key=True)  # Field name made lowercase.
    comment_post = models.ForeignKey(WpPosts,db_column='comment_post_ID',on_delete=models.CASCADE)  # Field name made lowercase.
    comment_author = models.TextField()
    comment_author_email = models.CharField(max_length=100)
    comment_author_url = models.CharField(max_length=200)
    comment_author_ip = models.CharField(db_column='comment_author_IP', max_length=100)  # Field name made lowercase.
    comment_date = models.DateTimeField(default=now)
    comment_date_gmt = models.DateTimeField(default=now)
    comment_content = models.TextField()
    comment_karma = models.IntegerField(default=0)
    comment_approved = models.CharField(max_length=20,default='1')
    comment_agent = models.CharField(max_length=255)
    comment_type = models.CharField(max_length=20,default='')
    comment_parent = models.BigIntegerField()
    user_id = models.BigIntegerField()

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_comments'


class WpTermRelationships(models.Model):
    object_id = models.BigIntegerField(primary_key=True)
    term_taxonomy_id = models.BigIntegerField()
    term_order = models.IntegerField()

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_term_relationships'
        unique_together = (('object_id', 'term_taxonomy_id'),)


class WpTermTaxonomy(models.Model):
    term_taxonomy_id = models.BigAutoField(primary_key=True)
    term_id = models.BigIntegerField()
    taxonomy = models.CharField(max_length=32)
    description = models.TextField()
    parent = models.BigIntegerField()
    count = models.BigIntegerField()

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_term_taxonomy'
        unique_together = (('term_id', 'taxonomy'),)


class WpTermmeta(models.Model):
    meta_id = models.BigAutoField(primary_key=True)
    term_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_termmeta'


class WpTerms(models.Model):
    term_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    term_group = models.BigIntegerField()

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_terms'


class WpUsermeta(models.Model):
    umeta_id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'wordpress'
        db_table = 'wp_usermeta'



#用于存储微信的api调用凭证
class WxCredential(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    appid=models.CharField(max_length=100)
    secret=models.CharField(max_length=100)
    comment=models.CharField(max_length=100,default="")
    class Meta:
        db_table = 'wx_credential'

#用于存储微信小程序的token
class WxToken(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    access_token=models.CharField(max_length=255)
    expires_time=models.DateTimeField()
    wx_credential=models.ForeignKey(WxCredential, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'wx_token'

#用于存储微信小程序的token
class WxSession(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    token=models.CharField(max_length=36)#用户跟小程序交互的token
    session_key=models.CharField(max_length=30)#会话密钥
    open_id=models.CharField(max_length=28)
    union_id=models.CharField(max_length=29)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wx_session'
