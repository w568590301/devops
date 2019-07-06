from functools import wraps
from django.http import JsonResponse

def handle_save_data(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            code = e.args[0]
            if code == 1062:
                status = -1
                msg = e.args[1]
            else:
                status = -2
                msg = e.args[0]
            return JsonResponse({'status':status, 'msg':msg})
    return wrapper



