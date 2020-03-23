from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from vcfupload.models import UploadVcf
from vcfupload_rest.serializers import UploadVcfSerializer


@api_view(["GET", "POST"])
def vcf_list(request):
    """
    List all uploaded VCFs, or create new UploadVCF.
    """
    if request.method == "GET":
        vcfs = UploadVcf.objects.all()
        serializer = UploadVcfSerializer(vcfs, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = UploadVcfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
def vcf_detail(request, pk):
    """
    Retrieve, update or delete an uploaded vcf.
    """
    try:
        vcf = UploadVcf.objects.get(pk=pk)
    except UploadVcf.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UploadVcfSerializer(vcf)
        return Response(serializer.data)

    elif request.method == "DELETE":
        vcf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
