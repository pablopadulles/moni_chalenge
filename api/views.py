import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import ApplicantCredit, User, Session
from .serializers import ApplicantCreditSerializer
from django.contrib.auth.mixins import LoginRequiredMixin

class RequesCreditView(APIView):
    '''
    Save and evaluate the request credit
    '''
    permission_classes = [permissions.AllowAny]
    
    def check_scoring(self, dni) -> bool:
        headers = {'credential': 'ZGpzOTAzaWZuc2Zpb25kZnNubm5u'}
        responce = requests.get('https://api.moni.com.ar/api/v4/scoring/pre-score/' + str(dni), headers=headers)
        if responce.json().get('status', 'rejected') == 'approve':
            return True
        return False

    def get(self, request, *args, **kwargs):
        '''
        List all users
        '''
        users = ApplicantCredit.objects.filter()
        serializer = ApplicantCreditSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''
        Create User
        '''
        dni = request.data.get('dni', '')
        scoring_status = self.check_scoring(dni)
        
        data = {
            'name': request.data.get('name'), 
            'lastname': request.data.get('lastname'), 
            'dni': dni, 
            'gender': request.data.get('gender'), 
            'email': request.data.get('email'), 
            'mount': request.data.get('mount'),
            'status': scoring_status,
        }

        serializer = ApplicantCreditSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class ApplicantCreditView(APIView, LoginRequiredMixin):
    '''
    Applicant credits
    '''
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    permission_classes = [permissions.AllowAny]

    def get_applicants(self, dni) -> list[ApplicantCredit]:
        try:
            applicants = ApplicantCredit.objects.filter(dni=dni)
            return applicants
        except:
            return []

    def get(self, request, *args, **kwargs):
        dni = request.data.get('dni', '')
        applicants = self.get_applicants(dni)

        return Response({}, status=status.HTTP_201_CREATED)


class LogIn(APIView):
    '''
    Admin login
    '''
    permission_classes = [permissions.AllowAny]

    def get_user(self, login) -> User:
        try:
            user = ApplicantCredit.objects.get(login=login)
            return user
        except:
            return None

    def post(self, request, *args, **kwargs):

        user = self.get_user(request.data.get('login', ''))

        User.login(user, request.data.get('password', ''))

        return Response({}, status=status.HTTP_201_CREATED)
