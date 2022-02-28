import logging
from django.views import View
from django import http
from areas.models import Area
from MeiDuoMall.utils.response_code import RETCODE

# 创建日志输出器
logger = logging.getLogger('django')

# 在此处创建你的视图.
class AreasView(View):
    def get(self,requst):
        area_id = requst.GET.get('area_id')
        if not area_id:
            # 提供省份数据
            try:
                # 查询省份数据
                # Area.objects.filter(属性名__条件表达式=值)
                province_model_list = Area.objects.filter(parent__isnull=True)

                # 序列化省级数据
                province_list = []
                for province_model in province_model_list:
                    province_list.append({'id': province_model.id, 'name': province_model.name})
                    # 响应省份数据
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})
            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '省份数据错误'})
        else:
            # 提供市或区数据
            try:
                parent_model = Area.objects.get(id=area_id)  # 查询市或区的父级
                sub_model_list = parent_model.subs.all()

                # 序列化市或区数据
                sub_list = []
                for sub_model in sub_model_list:
                    sub_list.append({'id': sub_model.id, 'name': sub_model.name})

                sub_data = {
                    'id': parent_model.id,  # 父级pk
                    'name': parent_model.name,  # 父级name
                    'subs': sub_list  # 父级的子集
                }
                # 响应市或区数据
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'sub_data': sub_data}) 
            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '城市或区数据错误'})
    