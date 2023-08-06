from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import GecoUser
from rest_auth.registration.serializers import RegisterSerializer
import os
from django.conf import settings

#UserModel = get_user_model()

class GecoUserSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = GecoUser
        fields = ('project_user')
        read_only_fields = ('user',)

class GecoRegisterSerializer(RegisterSerializer):


    def save(self, request):
        data = request.data
        project_dir = f'{settings.BASE_DIR}/{data.get("username")}/'
        if not os.path.exists(project_dir):
            os.mkdir(project_dir)
        
        user = super().save(request)
        geco_user = GecoUser(project_dir=project_dir, user=user)
        geco_user.save()
        return user