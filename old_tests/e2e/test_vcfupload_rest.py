import pytest

from django.conf import settings
from vcfupload.models import UploadVcf

## Constants

API_ROOT_URL = "/api/vcfs/"

## Fixture


@pytest.fixture(scope="class")
def api_client(request):
    from rest_framework.test import APIClient

    request.cls.api_client = APIClient()
    yield request
    return


@pytest.fixture()
def post_file(db, mock_MEDIA_ROOT, vcf_file):
    url = API_ROOT_URL
    file = vcf_file

    # Callback
    def do_post(cls):
        with open(file, "rb") as handle:
            response = cls.api_client.post(url, {"file": handle}, format="multipart")
        return response

    yield do_post


@pytest.fixture()
def delete_file(db):

    # Callback
    def do_delete(cls, url):
        response = cls.api_client.delete(url)
        return response

    yield do_delete


## Tests


@pytest.mark.incremental
@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.usefixtures("api_client", "django_db_keepdb")
class TestRestApi_Responses:
    def test_GET_to_API_ROOT_before_POST(self):
        # Given
        url = API_ROOT_URL

        # When
        response = self.api_client.get(url)

        # Side-effect
        model_count = len(UploadVcf.objects.all())

        # Then
        assert response.status_code == 200
        assert model_count == 0

    def test_GET_to_API_ITEM_before_POST(self):
        # Given
        expected_primary_key = 1
        url = f"{API_ROOT_URL}{expected_primary_key}"

        # When
        response = self.api_client.get(url)

        # Side-effect
        model_count = len(UploadVcf.objects.all())

        # Then
        assert response.status_code == 404
        assert model_count == 0

    def test_POST_to_API_ROOT(self, mock_MEDIA_ROOT, vcf_file):
        # Given
        url = API_ROOT_URL

        # When
        with open(vcf_file, "rb") as handle:
            response = self.api_client.post(url, {"file": handle}, format="multipart")

        # Side-effect
        model_count = len(UploadVcf.objects.all())

        # Then
        assert response.status_code == 201
        assert model_count == 1

    def test_GET_to_API_ROOT_after_POST(self, post_file):
        # Given
        post_file(self)
        url = API_ROOT_URL

        # When
        response = self.api_client.get(url)

        # Side-effect
        model_count = len(UploadVcf.objects.all())

        # Then
        assert response.status_code == 200
        assert model_count == 1

    def test_GET_to_API_ITEM_after_POST(self, post_file):
        # Given
        post_file(self)
        expected_primary_key = 1
        url = f"{API_ROOT_URL}{expected_primary_key}"

        # When
        response = self.api_client.get(url)

        # Side-effect
        models = UploadVcf.objects.all()
        model_count = len(models)
        if model_count:
            actual_pk = models[0].pk
        else:
            actual_pk = -1

        # Then
        assert response.status_code == 200
        assert model_count == 1
        assert actual_pk == expected_primary_key

    def test_DELETE_to_API_ITEM_after_POST(self, post_file):
        # Given
        post_file(self)
        expected_primary_key = 1
        url = f"{API_ROOT_URL}{expected_primary_key}"

        # When
        response = self.api_client.delete(url)

        # Side-effect
        models = UploadVcf.objects.all()
        model_count = len(models)

        # Then
        assert response.status_code == 204
        assert model_count == 0

    def test_GET_to_API_ITEM_after_DELETE(self, post_file, delete_file):
        # Given
        post_file(self)
        primary_key_of_deleted_item = 1
        url = f"{API_ROOT_URL}{primary_key_of_deleted_item}"
        delete_file(self, url)

        # When
        response = self.api_client.get(url)

        # Side-effect
        models = UploadVcf.objects.all()
        model_count = len(models)

        # Then
        assert response.status_code == 404
        assert model_count == 0

    def test_POST_again_to_API_ROOT(self, post_file, delete_file):
        # Given
        url = API_ROOT_URL
        post_file(self)
        primary_key_of_deleted_item = 1
        delete_file(self, f"{API_ROOT_URL}{primary_key_of_deleted_item}")

        # When
        response = post_file(self)

        # Side-effect
        model_count = len(UploadVcf.objects.all())

        # Then
        assert response.status_code == 201
        assert model_count == 1

    def test_GET_to_API_ITEM_after_second_POST(self, post_file, delete_file):
        # Given
        post_file(self)
        primary_key_of_deleted_item = 1
        delete_file(self, f"{API_ROOT_URL}{primary_key_of_deleted_item}")
        post_file(self)
        expected_primary_key = 2
        url = f"{API_ROOT_URL}{expected_primary_key}"

        # When
        response = self.api_client.get(url)

        # Side-effect
        models = UploadVcf.objects.all()
        model_count = len(models)
        if model_count:
            actual_pk = models[0].pk
        else:
            actual_pk = -1

        # Then
        assert response.status_code == 200
        assert model_count == 1
        assert actual_pk == expected_primary_key
