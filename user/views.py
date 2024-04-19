from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
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
            return Response({'error': 'User is already authenticated'}, status=400)
        return Response({})

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'User is already authenticated'}, status=400)
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
        return Response({})


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
    if user:
        user.is_active = True
        user.save()
    return Response({"success": "activation completed"}, status=200)


def _logout(request):
    logout(request)
    return redirect('register')