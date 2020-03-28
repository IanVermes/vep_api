from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from webvep_api.serializers import PingSerializer


@api_view(["POST"])
def ping(request):
    """
    List all uploaded VCFs, or create new UploadVCF.
    """
    if request.method == "POST":
        serializer = PingSerializer(data=request.data)
        return Response(data={"data": "pong"}, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
