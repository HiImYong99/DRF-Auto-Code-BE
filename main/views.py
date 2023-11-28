from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserInputSerializer
from .models import UserInput
from rest_framework.permissions import IsAuthenticated

from dotenv import load_dotenv
import os
from openai import OpenAI

# Create your views here.
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class UserInputGetAPIView(APIView):
    '''
    DB에 저장된 요청 및 응답 값 로드
    '''

    def get(self, request, format=None):
        qs = UserInput.objects.filter(user=self.request.user)
        serializer = UserInputSerializer(qs, many=True)
        return Response(serializer.data)


class UserInputRequestAPIView(APIView):
    '''
    OpenAI api 연결 및 요청 및 응답 값 DB저장
    '''
    Permission_claases = [IsAuthenticated]  # 로그인을 한 유저만 사용 가능
    throttle_scope = 'request'  # 각 유저당 하루 5번만 요청 가능

    def post(self, request, format=None):
        language = request.data.get('language')
        purpose = request.data.get('purpose')
        detail = request.data.get('detail')

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
            UserInput.objects.create(
                user=user, language=language, purpose=purpose, detail=detail, answer=response)
        return Response({'language': language, 'purpose': purpose, 'detail': detail, 'answer': response}, status=status.HTTP_200_OK)

    def throttle_failure(self, rate_limit, scope):
        return Response(
            {"error": "Throttle limit exceeded. Please wait before trying again."},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )


class UserInputDeleteAPIView(APIView):
    '''
    DB에 저장된 값 삭제 
    '''
    Permission_claases = [IsAuthenticated]  # 로그인을 한 유저만 사용 가능

    def delete(self, request, pk, format=None):
        user_input = UserInput.objects.get(
            id=pk, user=self.request.user)
        user_input.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserInputDeleteAllAPIView(APIView):
    '''
    DB에 저장된 값 전체 삭제
    '''
    Permission_claases = [IsAuthenticated]  # 로그인을 한 유저만 사용 가능

    def delete(self, request, format=None):
        user_input = UserInput.objects.all()
        user_input.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
