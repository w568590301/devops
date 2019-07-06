from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View,TemplateView,ListView
from django.http import JsonResponse,QueryDict
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import *
from utils.baseviews import BaseListView,APIBaseView
from utils.wrappers import handle_save_data

# Create your views here.
class IdcView(BaseListView):
    model = Idc
    template_name = 'cmdb/idcs.html'
    template_detail = 'cmdb/idc_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        search = self.request.GET.get('search','')
        if search:
            queryset = queryset.filter(Q(name__contains=search)|Q(address__contains=search))
        qs = [i.to_dict for i in queryset]
        # print(qs)
        return qs

class APIIDCView(APIBaseView):
    model = Idc

class RackView(BaseListView):
    model = Rack
    template_name = 'cmdb/racks.html'
    template_detail = 'cmdb/racks_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        idc_id = self.request.GET.get('idc_id')
        if idc_id:
            queryset = queryset.filter(idc_id=idc_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__contains=search) | Q(number__contains=search) | Q(size__contains=search))
        qs = [i.to_dict for i in queryset]
        return qs

class APIRackView(APIBaseView):
    model = Rack

class ServerView(BaseListView):
    model = Server
    template_name = 'cmdb/servers.html'
    template_detail = 'cmdb/server_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        rack_id = self.request.GET.get('rack_id')
        if rack_id:
            queryset = queryset.filter(rack_id=rack_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(ip__contains=search) | Q(server_type__icontains=search) | Q(remark__icontains=search) | Q(os__icontains=search))

        qs = [i.to_dict for i in queryset]
        return qs

class APIServerView(APIBaseView):
    model = Server

    def post(self,request,*args,**kwargs):
        data = QueryDict(request.body).dict()
        name = data.get('hostname')
        uuid = data.get('uuid')
        server_type = data.get('server_type')
        cpu = data.get('server_cpu')
        memory = data.get('server_mem')
        disk = data.get('server_disk')
        daq = str(data)
        ip = data.get('ip_info')
        os = data.get('os')
        server_data = {
            'name':name,
            'cpu':cpu,
            'memory':memory,
            'disk':disk,
            'uuid':uuid,
            'server_type':server_type,
            'ip': ip,
            'daq':daq,
            'os':os
        }

        qs_instance = self.model.objects.filter(uuid=uuid,server_type=server_type)
        if qs_instance:
            qs_instance.update(**server_data)
            qs_instance.first().save()
        else:
            self.model.objects.create(**server_data)
        return JsonResponse({})

class DashBoardView(TemplateView):
    template_name = 'dashboard.html'

class APIDashBoardView(View):
    def get(self, request):
        data = {}
        idc_list = Idc.objects.all()
        rack_list = Rack.objects.all()
        server_list = Server.objects.all()
        data_site = []
        data_pie = []
        for idc in idc_list:
            servers = 0
            site_idc = {}
            racks = idc.rack_set.all()
            total_site = racks.count() * 10
            for rack in racks:
                servers += rack.server_set.count()
            site_idc['id'] = idc.id
            site_idc['name'] = idc.name
            site_idc['total_site'] = total_site
            site_idc['site'] = servers
            data_site.append(site_idc)
            data_pie.append([idc.name, servers])
        data['data_pie'] = data_pie
        data['data_site'] = data_site
        data['counts'] = {
            'idcs':idc_list.count(),
            'racks':rack_list.count(),
            'servers':server_list.count()
        }
        print(data)
        return JsonResponse(data)