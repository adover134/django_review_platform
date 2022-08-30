from rest_framework import serializers
from DBs.models import User, Manager, Review, Room, Icon, Recommend, Report, CommonInfo, ReviewImage, RoomImage


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

    reviewWriter = serializers.SerializerMethodField()
    representiveImage = serializers.SerializerMethodField()
    uEmail = serializers.EmailField(source='uId.email', read_only=True)
    rAddress = serializers.CharField(source='rId.address', read_only=True)

    additionalImage = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
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


    # 리뷰 작성자의 이름을 합쳐서 출력
    def get_reviewWriter(self, obj):
        return f'{obj.uId.last_name} {obj.uId.first_name}'


    def get_representiveImage(self, obj):
        a = [image.image for image in obj.additionalImage.all()]
        return a


    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer2(serializers.ModelSerializer):
    reviewWriter = serializers.SerializerMethodField()
    uEmail = serializers.EmailField(source='uId.email', read_only=True)
    rAddress = serializers.CharField(source='rId.address', read_only=True)

    additionalImage = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
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

    # 리뷰 작성자의 이름을 합쳐서 출력
    def get_reviewWriter(self, obj):
        return f'{obj.uId.last_name} {obj.uId.first_name}'

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializerString(serializers.ModelSerializer):

    reviewWriter = serializers.SerializerMethodField()
    uEmail = serializers.EmailField(source='uId.email', read_only=True)
    rAddress = serializers.CharField(source='rId.address', read_only=True)

    additionalImage = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    includedIcon = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    recommendedOn = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    reportedOn = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )

    def get_reviewWriter(self, obj):
        return f'{obj.uId.last_name}{obj.uId.first_name}'

    class Meta:
        model = Review
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    commonInfo = serializers.ListField(
        child=serializers.IntegerField()
    )
    roomImage = serializers.StringRelatedField(
        many=True,
        read_only=True,
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


class ReviewImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewImage
        fields = '__all__'


class RoomImageSerializer(serializers.ModelSerializer):

    commonInfo = serializers.ListField(
       child=serializers.IntegerField(min_value=0, max_value=10000), allow_null=True
    )

    class Meta:
        model = RoomImage
        fields = '__all__'
