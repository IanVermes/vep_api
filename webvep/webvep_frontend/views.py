from django.shortcuts import render
from webvep_api.serializers import VcfSerializer
from rest_framework.decorators import api_view
from helpers.vep_helper import ProcessVcfForm
from helpers.vep_parser import parser

# Create your views here.


def home(request):
    return render(request, "home.html")


@api_view(["POST"])
def simple_upload(request):
    if request.method == "POST":
        serializer = VcfSerializer(data=request.data)
        print(f"{request.data=}")
        if serializer.is_valid():
            vcf_form = serializer.save()
            vep_form = ProcessVcfForm().pipeline(vcf_form)
            result = parser(vep_form)
            payload = {
                "is_valid": True,
                "file_name": vcf_form.filename,
                "result": {
                    "VEP_version": result.vep_version,
                    "run_date": result.run_date,
                },
                "rows": result.variants[:10],
                "na": "n/a",
                "show_hgvsp": bool(request.data.get("show_protein")),
                "show_hgvsc": bool(request.data.get("show_dna")),
            }
        else:
            payload = {"is_valid": False, "file_name": "INVALID FILE"}
        return render(request, "home.html", payload)
    return render(request, "home.html")
