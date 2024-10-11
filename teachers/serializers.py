from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(required=True, min_length=3, max_length=100, source="name")
    idade = serializers.IntegerField(required=True, min_value=18, max_value=100, source="age")
    descricao = serializers.CharField(required=True, min_length=10, max_length=500, source="description")
    password_confirmation = serializers.CharField(write_only=True)
    valor_hora = serializers.DecimalField(required=True, min_value=10,max_value=500, max_digits=5, decimal_places=2, source="hourly_price")
    
    class Meta:
        model = Teacher
        fields = ("id", "nome", "email", "idade", "descricao", "valor_hora", "created_at", "updated_at", "password", "password_confirmation")
        extra_kwargs = {"password": {"write_only":True}, "created_at": {"read_only": True}, "updated_at":{"read_only":True}}
    
    def validate_password_confirmation(self, value):
        if self.initial_data["password"] != value:
            raise serializers.ValidationError("As senhas não são iguais")
        
    def create(self, validated_data):
        del validated_data["password_confirmation"]
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if "password_confirmation" in validated_data:
          del validated_data["password_confirmation"]

        if "password" in validated_data:
          instance.password = make_password(validated_data["password"])

        for attr, value in validated_data.items():
          setattr(instance, attr, value)
        instance.save()  
        return instance