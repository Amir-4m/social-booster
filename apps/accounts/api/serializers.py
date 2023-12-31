import re
from datetime import datetime
from random import randint

from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.settings import api_settings

from khayyam import JalaliDate

from apps.accounts.models import User, UserProfile
from utils.utils import number_converter
from utils.validators import validate_phone_number


class LifeTimeTokenSerializer:

    def validate(self, attrs):
        # adding lifetime to data
        data = super().validate(attrs)
        data['lifetime'] = int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds())
        data['user_id'] = token_backend.decode(data['access'])['user_id']

        return data


class TokenObtainLifetimeSerializer(LifeTimeTokenSerializer, TokenObtainPairSerializer):
    pass


class TokenRefreshLifetimeSerializer(LifeTimeTokenSerializer, TokenRefreshSerializer):
    pass


class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=120)
    has_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'has_password')
        extra_kwargs = {'phone_number': {'validators': None}}

    def get_has_password(self, obj):
        return obj.has_usable_password()

    def validate_phone_number(self, value):
        try:
            phone_number_matches = re.findall(validate_phone_number.regex, str(value).translate(number_converter))
            phone_number_match = phone_number_matches[0]
        except:
            raise serializers.ValidationError(validate_phone_number.message)
        return phone_number_match

    def create(self, validated_data):
        if not settings.DEVEL:
            verify_code = randint(settings.VERIFY_CODE_MIN, settings.VERIFY_CODE_MAX)
        else:
            verify_code = 11111
        phone_number = int(validated_data['phone_number'])

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone_number=phone_number
            )

        if user.has_usable_password():
            return user
        user.set_verify_code(verify_code)
        return user


class RelatedUserProfileInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', )


class UserProfileSerializer(serializers.ModelSerializer):

    has_password = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'avatar', 'gender', 'birth_date', 'email_address', 'has_password']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        birth_date = attrs.get('birth_date')
        # Convert Jalali date to A.D date
        if birth_date:
            birth_date = JalaliDate(birth_date.year, birth_date.month, birth_date.day).todate()
            attrs['birth_date'] = birth_date
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        birth_date = data.get('birth_date')
        avatar = data.get('avatar')
        # Convert A.D date to Jalali date
        if birth_date:
            string_to_date = datetime.strptime(birth_date, '%Y-%m-%d')
            to_jalali_date = JalaliDate(string_to_date).strftime('%Y-%m-%d')
            data['birth_date'] = to_jalali_date
        else:
            data['birth_date'] = ""
        if avatar is None:
            data['avatar'] = ""
        return data

    def get_has_password(self, obj):
        return obj.user.has_usable_password()

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def create(self, validated_data):
        user = validated_data.pop('user')
        instance, _created = UserProfile.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        request = self.context.get("request")
        instance.user.first_name = request.POST.get('first_name', instance.user.first_name)
        instance.user.last_name = request.POST.get('last_name', instance.user.last_name)
        instance.user.save()
        return instance


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    'new_password':
                        _('New password and confirm password are not matched.')
                }
            )
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        if user.has_usable_password():
            raise serializers.ValidationError(_("This user has already set password before"))
        user.set_password(validated_data['new_password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    'new_password':
                        _('New password and confirm password are not matched.')
                }
            )
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        if not user.check_password(validated_data['old_password']):
            raise PermissionDenied()
        user.set_password(validated_data['new_password'])
        user.save()
        return user


class ForgetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=120)

    def validate(self, attrs):
        raw_phone_number = attrs.get('phone_number')
        try:
            phone_number_matches = re.findall(
                validate_phone_number.regex,
                str(raw_phone_number).translate(number_converter)
            )
            phone_number_match = phone_number_matches[0]
        except:
            raise serializers.ValidationError(validate_phone_number.message)

        if not settings.DEVEL:
            verify_code = randint(settings.VERIFY_CODE_MIN, settings.VERIFY_CODE_MAX)
        else:
            verify_code = 11111

        try:
            user = User.objects.get(phone_number=phone_number_match)
        except User.DoesNotExist:
            raise NotFound()
        cache.set(f'forget_password_{user.phone_number}_{verify_code}', True, 6.5 * 60 * 60)
        user.set_verify_code(verify_code)
        data = super().validate(attrs)
        return data
