from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
@login_required()
def profile_view(request):
    return Response({
        'test': 'yey'
    })
