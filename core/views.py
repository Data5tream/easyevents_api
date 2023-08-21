from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnerOrAdmin
from .serializers import UserSerializer


class ProfileView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
