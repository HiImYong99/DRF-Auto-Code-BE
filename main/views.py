from django.http import HttpResponseForbidden
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserInputSerializer
from .models import UserInput
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated


from django.views import View
from dotenv import load_dotenv
import os
from openai import OpenAI

# Create your views here.
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class UserInputRequestAPIView(APIView):
    def get(self, request, format=None):
        #  language, purpose 및 입력한 detail을 가져오기
        qs = UserInput.objects.filter(user=self.request.user)
        serializer = UserInputSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        permission_claases = [IsAuthenticated]
        # 사용자 입력 받아오기
        language = request.data.get('language')
        purpose = request.data.get('purpose')
        detail = request.data.get('detail')

        # 현재 로그인한 사용자 확인
        user = request.user
        model_engine = "text-davinci-003"
        prompt = f"Language: {language}\nPurpose: {purpose}\nDetail: {detail}\n"

        completion = client.completions.create(
            model=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=5,
            stop=None,
            temperature=0.5
        )

        response = completion.choices[0].text.strip()
        if response:
            # UserInput 모델에 저장
            user_input = UserInput.objects.create(
                user=user, language=language, purpose=purpose, detail=detail, answer=response)
        # AIOutput 모델에 응답 저장
        # 세션에 선택한 language, purpose, detail 저장
        request.session['language'] = language
        request.session['purpose'] = purpose
        request.session['detail'] = detail

        return Response({'language': language, 'purpose': purpose, 'detail': detail, 'answer': response}, status=status.HTTP_200_OK)


class UserInputDeleteAPIView(APIView):
    def delete(self, request, pk, format=None):
        user_input = UserInput.objects.get(
            id=pk, user=self.request.user)
        user_input.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
