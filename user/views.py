from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import render_to_string
from django_short_url.models import ShortURL
from django_short_url.views import get_surl
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import *
# Create your views here.


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_decoder_handler = api_settings.JWT_DECODE_HANDLER


class RegistrationView(GenericAPIView):

    serializer_class = RegistrationSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'User is already authenticated'}, status=401)
        return Response({})

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'User is already authenticated'}, status=401)
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # JWT
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response = jwt_response_payload_handler(token, user)
        surl = get_surl(str(token))
        z = surl.split("/")
        mail_subject = 'greeting from fundoo ,Activate your account by clicking below link'
        mail_message = render_to_string('user/email_validation.html', {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'surl': z[2]
        })
        recipient_email = user.email
        subject, from_email, to = mail_subject, settings.EMAIL_HOST, recipient_email
        msg = EmailMultiAlternatives(subject, mail_message, from_email, [to])
        msg.attach_alternative(mail_message, "text/html")
        msg.send()
        return Response({"message": "Registration is completed, please complete email verification"}, status=201)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializers

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'details': 'User is already authenticated'}, status=401)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        qs = User.objects.filter(
            Q(username__iexact=username) or
            Q(email__iexact=username)
        ).distinct()
        if qs.count() == 0:
            return Response("User Credentials are not matching", status=404)
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                # cache.set(user.username, token)
                # print(cache.get(user.username))
                return Response('login successful', status=200)
            return Response("Wrong password.Check password again", status=404)
        return Response("multiple users are present with this username", status=300)


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        data = request.data
        email = data['email']
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist as e:
            return Response({'email': 'No user with this email id', 'error': str(e)}, status=400)
        except MultipleObjectsReturned as e:
            return Response({'email': 'Multiple users are registered with this email id', 'error': str(e)}, status=400)

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        surl = get_surl(str(token))
        z = surl.split('/')
        domain = get_current_site(request).domain
        mail_subject = 'greeting from Fundo ,Reset your account password by clicking below link'
        mail_message = render_to_string('user/password_reset.html', {
            'user': user.username,
            'domain': domain,
            'surl': z[2]
        })
        recipient_email = user.email
        subject, from_email, to = mail_subject, settings.EMAIL_HOST, recipient_email
        msg = EmailMultiAlternatives(subject, mail_message, from_email, [to])
        msg.attach_alternative(mail_message, "text/html")
        print("http://" + domain + '/user/reset_password/'+str(z[2]))
        msg.send()
        return Response({"message": 'Reset password link sent'}, status=200)


@api_view(['GET'])
def activate(request, surl):
    tokenobject = ShortURL.objects.get(surl=surl)
    token = tokenobject.lurl
    user_obj = jwt_decoder_handler(token)
    user_id = user_obj.get('user_id')
    try:
        user = User.objects.get(id=user_id, is_active=False)
    except User.DoesNotExist as e:
        return Response({"Error": "Validation is incomplete use to some error"}, status=400)
    if user:
        user.is_active = True
        user.save()
    return Response({"success": "activation completed"}, status=200)


@api_view(['GET'])
def reset_password(request, surl):
    tokenobject = ShortURL.objects.get(surl=surl)
    token = tokenobject.lurl
    user_obj = jwt_decoder_handler(token)
    user_id = user_obj.get('user_id')
    try:
        user = User.objects.get(id=user_id, is_active=False)
    except User.DoesNotExist as e:
        return Response({"Error": "Validation is incomplete use to some error"}, status=400)
    request.session['previous_page'] = 'reset_password'
    return redirect('change_password', user_id=user_id)


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request, user_id):
        print(request.__dict__)
        if request.session['previous_page'] != 'reset_password':
            return Response({"Error": "Not able to access this page"}, status=404)
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data['password']
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist as e:
            return Response({'email': 'No user with this user id', 'error': str(e)}, status=400)
        except MultipleObjectsReturned as e:
            return Response({'email': 'Multiple users are registered with this user id', 'error': str(e)}, status=400)
        user.set_password(password)
        user.save()
        return Response({"Message": "Change Password completed"}, status=200)


def user_logout(request):
    logout(request)
    return redirect('login')