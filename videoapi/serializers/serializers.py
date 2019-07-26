from rest_framework import serializers
from ..models import UserFiles


class APIRequestSerializer(serializers.Serializer):
   user_id = serializers.IntegerField()
   file_size = serializers.IntegerField()
   video_file =  serializers.FileField(allow_empty_file=False,max_length=500)

class VideoSerializer(serializers.Serializer):
   user_id = serializers.IntegerField()
   video_name = serializers.CharField(max_length=200)
   video_size = serializers.IntegerField()

class UserFilesSerializer(serializers.ModelSerializer):
   class Meta:
      model = UserFiles
      fields = '__all__'
