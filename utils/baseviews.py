from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView,View
from django.shortcuts import render
from django.http import JsonResponse,QueryDict
from utils.wrappers import handle_save_data

class BaseListView(LoginRequiredMixin,ListView):
    model = None
    template_detail = None
    paginate_by = 10

    def handle_page(self, page, object_list):
        paginator = Paginator(object_list, self.paginate_by,1)
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            paginator_data = paginator.page(1)
        except EmptyPage:
            paginator_data = paginator.page(paginator.num_pages)
        # print(paginator_data.object_list)
        return paginator_data

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                instance = self.model.objects.get(pk=pk)
                # print(type(instance.to_dict['daq']))
                # print(instance.to_dict)
                return render(request,self.template_detail,instance.to_dict)
            except self.model.DoesNotExist:
                return JsonResponse({'data':'id {} not exist'.format(pk)})
        object_list = self.get_queryset()
        page = self.request.GET.get('page')
        search = self.request.GET.get('search','')
        rack_id = self.request.GET.get('rack_id')
        queryset = self.model.objects.all()
        count = self.model.objects.all().count()
        if rack_id:
            count = queryset.filter(rack_id=rack_id).count()
        if search:
            count = queryset.filter(Q(name__icontains=search) | Q(ip__contains=search) | Q(server_type__icontains=search) | Q(remark__icontains=search) | Q(os__icontains=search)).count()
            # print(count)
        paginator_data = self.handle_page(page,object_list)
        return render(request, self.template_name, {'paginator_data': paginator_data,'count':count})

    @handle_save_data
    def post(self,request,*args,**kwargs):
        data = QueryDict(request.body).dict()
        self.model.objects.create(**data)
        return JsonResponse({'status':1})

    def delete(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).delete()
        return JsonResponse({})

    @handle_save_data
    def put(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        data = QueryDict(request.body).dict()
        self.model.objects.filter(id=pk).update(**data)
        return JsonResponse({'status':'1'})

class APIBaseView(View):
    model = None

    def get_query(self):
        queryset = self.model.objects.all()
        qs = [i.to_dict for i in queryset]
        return qs

    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                instance = self.model.objects.get(pk=pk).to_dict

            except Exception as e:
                instance = e.args[0]
            return JsonResponse({'data':instance,'status':1})
        return JsonResponse({'data':self.get_query(),'status':1})
