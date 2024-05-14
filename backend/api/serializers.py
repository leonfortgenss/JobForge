from rest_framework import serializers
from api.models import PersonalLetter
from django.contrib.auth import authenticate
from api.utils import send_prompt_to_api
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Man behöver i django serializa data/beareta datan för att den ska vara användful och synas.

class PersonalLetterCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalLetter
        fields = ("id", "name", "age", "traits", "output")
        extra_kwargs = {
            "output": {"read_only":True}
        }

# Gjorde om standard create functionen så den passar oss och här skickar den in datan till OpenAIs API och sedan sparar det.

    def create(self, validated_data):
        pl = PersonalLetter(**validated_data)

        name = validated_data.get('name')
        age = validated_data.get('age')
        traits = validated_data.get('traits')

        output = send_prompt_to_api(name, age, traits)
        pl.output = output
        pl.save()
        return pl
    
# Basic user som kommer med django

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {
            "password": {"write_only":True}
        }

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

# Krypterar lösenord

        Token.objects.create(user=user)
        return user

# För att få token får att få access till att kunna skriva promts authenticatar vi username och lösen och skickar tillbaka token

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), username=username, password=password)
        if not user:
            message = "Your username or password did not match!"
            raise serializers.ValidationError(message, code="authentication")
        attrs["user"] = user
        return attrs