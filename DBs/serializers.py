from rest_framework import serializers
from DBs.models import User, Manager, Review, Room, Icon, Recommend, Report, CommonInfo, Image


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

    uNickname = serializers.CharField(source='uId.uNickname', read_only=True)
    uEmail = serializers.EmailField(source='uId.uEmail', read_only=True)
    rAddress = serializers.CharField(source='rId.address', read_only=True)
    includedIcon = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='icon-detail'
    )
    recommendedOn = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='recommend-detail'
    )
    reportedOn = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='report-detail'
    )

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer2(serializers.ModelSerializer):

    uNickname = serializers.CharField(source='uId.uNickname', read_only=True)
    uEmail = serializers.EmailField(source='uId.uEmail', read_only=True)
    rAddress = serializers.CharField(source='rId.address', read_only=True)
    includedIcon = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    commonInfo = serializers.ListField(
        child=serializers.IntegerField()
    )

    class Meta:
        model = Room
        fields = '__all__'


class IconSerializer(serializers.ModelSerializer):

    class Meta:
        model = Icon
        fields = '__all__'


class RecommendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recommend
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'


class CommonInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommonInfo
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'
