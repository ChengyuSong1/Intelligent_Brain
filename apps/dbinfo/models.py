# import time
# from django.db import models
#
#
# class DbInfos(models.Model):
#     """
#     """
#     id = models.CharField(max_length=35, primary_key=True)
#     host = models.CharField(max_length=35, default="")
#     port = models.IntegerField(default=3306)
#     username = models.CharField(max_length=35, default="")
#     password = models.CharField(max_length=35, default="")
#     update_time = models.CharField(max_length=20, default="2099-01-01 00:00:00")
#     state = models.IntegerField(default=1)
#
#     def update(self, **kwargs):
#         kwargs["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         self.update(**kwargs)
#
#     def getDetails(self):
#         result = {
#             "id": self.id,
#             "host": self.host,
#             "port": self.port,
#             "username": self.username,
#             "password": self.password,
#             "update_time": str(self.update_time),
#             "state": self.state,
#         }
#         return result
#
#     def __unicode__(self):
#         return self.host + "<>" + str(self.port)
#
