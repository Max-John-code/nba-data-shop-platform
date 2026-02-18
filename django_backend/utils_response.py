# utils/response.py
def success_response(data=None, message='成功'):
    """统一成功响应格式"""
    return {
        'code': 0,
        'message': message,
        'data': data or {}
    }


def error_response(message='错误', code=1):
    """统一错误响应格式"""
    return {
        'code': code,
        'message': message
    }
