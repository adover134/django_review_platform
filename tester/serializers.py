from rest_framework import serializers
from tester.models import User, Manager, Review, Room


class UserSerializer(serializers.ModelSerializer):

    writer = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='review-detail'
    )

    class Meta:
        model = User
        # fields = '__all__'
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    u_nickname = serializers.CharField(source='u_id.u_nickname', read_only=True)
    r_name = serializers.CharField(source='r_id.r_name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'
