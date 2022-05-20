from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from tester.serializers import UserSerializer, ManagerSerializer, ReviewSerializer, RoomSerializer
from tester.models import User, Manager, Review, Room

class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(self, request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class ManagerViewSets(ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def retrieve(self, request, *args, **kwargs):
        data = request.GET['m_tel']
        print(data)
        instance = Manager.objects.get(m_tel=data)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(self, request, args, kwargs)

    def tere(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class UserRetrieveViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def search(self, request, *args, **kwargs):
        data = User.objects.get(u_nickname=request.data['u_nickname'])
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class ReviewViewSets(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(self, request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class RoomViewSets(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(self, request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)
