from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View,TemplateView,ListView
from django.http import JsonResponse,QueryDict
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import *
from utils.dbcrypt import prpcrypt
from utils.baseviews import BaseListView,APIBaseView
from utils.wrappers import handle_save_data
# Create your views here.



#数据库配置
class DBview(BaseListView):
    model = DBConf
    template_name = 'sqlmng/dbconfig.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        search = self.request.GET.get('search','')
        if search:
            return self.model.objects.filter(name__contains=search)
        return queryset

    def post(self,request,*args,**kwargs):
        data = QueryDict(request.body).dict()
        password = data.get('password')
        #对password加密
        cry_password = prpcrypt.encrypt(password)
        data['password'] = cry_password
        #写入数据库
        self.model.objects.create(**data)
        return JsonResponse({'status': 0})

    def delete(self,request,*args,**kwargs):
        self.model.objects.get(pk=kwargs.get('pk')).delete()
        return JsonResponse({'status': 0})

    def put(self,request,*args,**kwargs):
        #密码的修改逻辑：如果密码没变化就直接保存，有变化就加密后保存
        data = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        obj = self.model.objects.get(pk=pk)
        password = data.get('password')
        if obj.password != password:
            data['password'] = prpcrypt.encrypt(password)
        self.model.objects.filter(pk=pk).update(**data)
        return JsonResponse({'status': 0})

class APISelectView(View):

    model_db = DBConf
    def post(self,request):
        data = QueryDict(request.body).dict()
        # print(data)
        env = data.get('env')
        ret = dict()
        ret['dbs'] = [db.name for db in self.model_db.objects.filter(env=env)]
        user = request.user
        # print(user)
        username = user.username
        print(username)
        if user.is_superuser: #超级用户，执行是自己
            ret['treater_list'] = [username]
            return JsonResponse(ret)
        role = user.role
        if env == '2': #测试环境，执行人就是自己
            treater_list = [username]
        elif env == '1':#生产环境
            if role in ['1','2']: #经理/总监，执行人是自己
                treater_list = [username]
            elif role == '3': #研发，找出同组内的经理列表
                ug = user.groups.first()
                if ug:
                    group_users = ug.user_set.all()
                    # print(group_users)
                    treater_list = [u.username for u in group_users if u.role == '2']
                else:
                    treater_list = []
        ret['treater_list'] = treater_list

        return JsonResponse(ret)

class InceptionCheckView(TemplateView):
    model = InceptionSql
    model_db = DBConf
    template_name = 'sqlmng/inception_check.html'



