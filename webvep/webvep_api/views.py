from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from webvep_api.serializers import PingSerializer, VcfSerializer
from helpers.vep_helper import ProcessVcfForm
from helpers.vep_parser import parser


@api_view(["POST"])
def ping_view(request):
    """Ping pong API - to check basic functionality"""
    if request.method == "POST":
        serializer = PingSerializer(data=request.data)
        if serializer.is_valid():
            return Response(data={"data": "pong"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def vcf_view(request):
    """VCF API - check if uploaded VCF files are valid"""
    if request.method == "POST":
        serializer = VcfSerializer(data=request.data)
        if serializer.is_valid():
            _ = serializer.save()
            response_payload = {"is_valid": True}
            return Response(data=response_payload, status=status.HTTP_201_CREATED)
        else:
            response_payload = {"is_valid": False}
            return Response(data=response_payload, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def vep_view(request):
    if request.method == "POST":
        serializer = VcfSerializer(data=request.data)
        if serializer.is_valid():
            vcf_form = serializer.save()
            vcf_processor = ProcessVcfForm()
            vep_form = vcf_processor.pipeline(vcf_form)
            parsed_result = parser(vep_form)
            response_payload = parsed_result.to_json()
            return Response(data=response_payload, status=status.HTTP_201_CREATED)
        else:
            response_payload = {"is_valid": False}
            return Response(data=response_payload, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
