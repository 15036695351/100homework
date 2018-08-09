class BaseResponse(object):
    def __init__(self):
        self.code = 1000
        self.data = None
        self.error = None

    @property
    def dict(self):  # 该方法将实例化的对象变成字典，以便响应给前端
        return self.__dict__