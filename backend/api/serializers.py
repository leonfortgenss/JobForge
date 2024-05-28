from rest_framework import serializers
from api.models import PersonalLetter
from django.contrib.auth import authenticate
from api.utils import send_prompt_to_api, get_related_skills, write_clear
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import requests
from bs4 import BeautifulSoup
from src.query_and_visualize import get_query_text, main as visualize_main

def scrape_job_listing(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text(separator='\n', strip=True)
        markdown_text = f"```\n{page_text}\n```"
        return {'page_text': markdown_text}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job listing: {e}")
        return {'page_text': 'N/A'}

class PersonalLetterCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalLetter
        fields = ("id", "user", "name", "age", "traits", "programming_language", "employer_link", "skill_match", "output")
        extra_kwargs = {
            "output": {"read_only": True},
            "user": {"read_only": True}, 
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user 

        name = validated_data.get('name')
        age = validated_data.get('age')
        traits = validated_data.get('traits')
        programming_language = validated_data.get('programming_language')
        employer_link = validated_data.get('employer_link')
        job_listing_details = scrape_job_listing(employer_link)
        print('joblistingdetails', job_listing_details)

        clean_text = write_clear(job_listing_details['page_text'])
        print('cleantext', clean_text)
        output = send_prompt_to_api(name, age, traits, clean_text)
        job_matches = get_related_skills(programming_language)
        print("job matches", job_matches)

        validated_data['output'] = output
        validated_data['skill_match'] = job_matches

        pl = PersonalLetter.objects.create(**validated_data)
        return pl
    
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)
        return user

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