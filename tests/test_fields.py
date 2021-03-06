import datetime
from django.test import TestCase
from project.geo_fields import PointField
from rest_framework import serializers
from project.fields import Base64ImageField


class UploadedBase64Image(object):
    def __init__(self, file=None, created=None):
        self.file = file
        self.created = created or datetime.datetime.now()


class UploadedBase64ImageSerializer(serializers.Serializer):
    file = Base64ImageField(required=False)
    created = serializers.DateTimeField()

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.file = attrs['file']
            instance.created = attrs['created']
            return instance
        return UploadedBase64Image(**attrs)

class Base64ImageSerializerTests(TestCase):

    def test_create(self):
        """
        Test for creating Base64 image in the server side
        """
        now = datetime.datetime.now()
        file = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
        serializer = UploadedBase64ImageSerializer(data={'created': now, 'file': file})
        uploaded_image = UploadedBase64Image(file=file, created=now)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.object.created, uploaded_image.created)
        self.assertFalse(serializer.object is uploaded_image)

    def test_validation_error_with_non_file(self):
        """
        Passing non-base64 should raise a validation error.
        """
        now = datetime.datetime.now()
        errmsg = "Please upload a valid image."
        serializer = UploadedBase64ImageSerializer(data={'created': now, 'file': 'abc'})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {'file': [errmsg]})


    def test_remove_with_empty_string(self):
        """
        Passing empty string as data should cause image to be removed
        """
        now = datetime.datetime.now()
        file = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
        uploaded_image = UploadedBase64Image(file=file, created=now)
        serializer = UploadedBase64ImageSerializer(instance=uploaded_image, data={'created': now, 'file': ''})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.object.created, uploaded_image.created)
        self.assertIsNone(serializer.object.file)


class SavePoint(object):
    def __init__(self, point=None, created=None):
        self.point = point
        self.created = created or datetime.datetime.now()


class PointSerializer(serializers.Serializer):
    point = PointField(required=False)
    created = serializers.DateTimeField()

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.point = attrs['point']
            instance.created = attrs['created']
            return instance
        return SavePoint(**attrs)

class PointSerializerTest(TestCase):

    def test_create(self):
        """
        Test for creating Point field in the server side
        """
        now = datetime.datetime.now()
        point = {
        "latitude": 49.8782482189424,
         "longitude": 24.452545489
        }
        serializer = PointSerializer(data={'created': now, 'point': point})
        saved_point = SavePoint(point=point, created=now)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.object.created, saved_point.created)
        self.assertFalse(serializer.object is saved_point)

    def test_validation_error_with_non_file(self):
        """
        Passing non-dict contains latitude and longitude should raise a validation error.
        """
        now = datetime.datetime.now()
        serializer = PointSerializer(data={'created': now, 'point': '123'})
        self.assertFalse(serializer.is_valid())


    def test_remove_with_empty_string(self):
        """
        Passing empty string as data should cause point to be removed
        """
        now = datetime.datetime.now()
        point = {
        "latitude": 49.8782482189424,
         "longitude": 24.452545489
        }
        saved_point = SavePoint(point=point, created=now)
        serializer = PointSerializer(data={'created': now, 'point': ''})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.object.created, saved_point.created)
        self.assertIsNone(serializer.object.point)
