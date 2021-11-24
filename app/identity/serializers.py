from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users obj"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it

        Parameters
        ----------
        validated_data
            valid user input

        Returns
        ------
            created user
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update user's name and password

        Parameters
        ----------
        instancd
            instance objcet
        validated_data
            valid user input

        Returns
        ------
            created user
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth obj"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user

        Parameters
        ------
        attrs
            attributes that going to be validated

        Returns
        ---
        attrs
            attributes validated
        """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        # if not able to authenticate user, raise error
        if not user:
            raise serializers.ValidationError(
                _('Unable to authenticate with provided credentials'),
                code='authentication'
            )
        attrs['user'] = user
        return attrs
