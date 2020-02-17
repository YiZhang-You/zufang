# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class District(models.Model):
    distid = models.IntegerField(primary_key=True)
    parent = models.ForeignKey(to='self', on_delete=models.DO_NOTHING, db_column='pid', null=True)
    name = models.CharField(max_length=255)
    ishot = models.BooleanField(default=False)
    intro = models.CharField(max_length=255, default='')

    class Meta:
        managed = False
        db_table = 'tb_district'


class Agent(models.Model):
    agentid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    servstar = models.IntegerField()
    realstar = models.IntegerField()
    profstar = models.IntegerField()
    certificated = models.IntegerField()
    estates = models.ManyToManyField(to='Estate', through='AgentEstate')

    class Meta:
        managed = False
        db_table = 'tb_agent'


class Estate(models.Model):
    estateid = models.AutoField(primary_key=True)
    district = models.ForeignKey(to=District, on_delete=models.DO_NOTHING, db_column='distid')
    name = models.CharField(max_length=255)
    hot = models.IntegerField(default=0)
    intro = models.CharField(max_length=511, default='')
    agents = models.ManyToManyField(to='Agent', through='AgentEstate')

    class Meta:
        managed = False
        db_table = 'tb_estate'


class AgentEstate(models.Model):
    agent_estate_id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(to=Agent, on_delete=models.DO_NOTHING, db_column='agentid')
    estate = models.ForeignKey(to=Estate, on_delete=models.DO_NOTHING, db_column='estateid')

    class Meta:
        managed = False
        db_table = 'tb_agent_estate'
        unique_together = (('agent', 'estate'), )


class TbHouseInfo(models.Model):
    houseid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    area = models.IntegerField()
    floor = models.IntegerField()
    totalfloor = models.IntegerField()
    direction = models.CharField(max_length=10)
    price = models.IntegerField()
    priceunit = models.CharField(max_length=10)
    detail = models.CharField(max_length=511, blank=True, null=True)
    mainphoto = models.CharField(max_length=255)
    pubdate = models.DateField()
    street = models.CharField(max_length=255)
    hassubway = models.IntegerField(blank=True, null=True)
    isshared = models.IntegerField(blank=True, null=True)
    hasagentfees = models.IntegerField(blank=True, null=True)
    typeid = models.IntegerField()
    userid = models.IntegerField()
    distid2 = models.IntegerField()
    distid3 = models.IntegerField()
    estateid = models.IntegerField(blank=True, null=True)
    agentid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_house_info'


class TbHousePhoto(models.Model):
    photoid = models.AutoField(primary_key=True)
    houseid = models.IntegerField()
    path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tb_house_photo'


class TbHouseTag(models.Model):
    house_tag_id = models.AutoField(primary_key=True)
    houseid = models.IntegerField()
    tagid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_house_tag'
        unique_together = (('houseid', 'tagid'),)


class TbHouseType(models.Model):
    typeid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tb_house_type'


class TbLoginLog(models.Model):
    logid = models.BigAutoField(primary_key=True)
    userid = models.IntegerField()
    ipaddr = models.CharField(max_length=255)
    logdate = models.DateTimeField(blank=True, null=True)
    devcode = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_login_log'


class TbPrivilege(models.Model):
    privid = models.AutoField(primary_key=True)
    method = models.CharField(max_length=15)
    url = models.CharField(max_length=1024)
    detail = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_privilege'


class TbRecord(models.Model):
    recordid = models.BigAutoField(primary_key=True)
    userid = models.IntegerField()
    houseid = models.IntegerField()
    recorddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_record'
        unique_together = (('userid', 'houseid'),)


class TbRole(models.Model):
    roleid = models.AutoField(primary_key=True)
    rolename = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tb_role'


class TbRolePrivilege(models.Model):
    role_priv_id = models.AutoField(primary_key=True)
    roleid = models.IntegerField()
    privid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_role_privilege'
        unique_together = (('roleid', 'privid'),)


class TbTag(models.Model):
    tagid = models.AutoField(primary_key=True)
    content = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tb_tag'


class TbUser(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=32)
    realname = models.CharField(max_length=20)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(unique=True, max_length=20)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    regdate = models.DateTimeField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    lastvisit = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_user'


class TbUserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    userid = models.IntegerField()
    roleid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_user_role'
        unique_together = (('userid', 'roleid'),)
