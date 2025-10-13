from rest_framework import serializers


class SecretSerializer(serializers.Serializer):
    secret = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=10000,
        help_text="The secret message to hide"
    )
    
    def validate_secret(self, value):
        if not value.strip():
            raise serializers.ValidationError("Secret cannot be empty or just whitespace")
        return value


class SecretResponseSerializer(serializers.Serializer):
    key = serializers.CharField(help_text="Unique key to access the secret")
    message = serializers.CharField(help_text="Status message")
    expires_in = serializers.CharField(
        help_text="Expiration time",
        required=False
    )


class RevealResponseSerializer(serializers.Serializer):
    secret = serializers.CharField(help_text="The revealed secret message")
    message = serializers.CharField(help_text="Status message")