from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    embed_url = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id','title','description','video_url','playlist_url','created_at','embed_url']
    def get_embed_url(self, obj):
        return obj.get_embed_url()    