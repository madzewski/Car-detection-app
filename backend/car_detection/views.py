from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import UploadedImageSerializer
from .models import UploadedImage
from .detector import detect_cars

class CarDetectionView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            image_instance = serializer.save()
            image_path = image_instance.image.path
            result_image_path, car_count = detect_cars(image_path)

            return Response({
                'message': 'Detection complete',
                'car_count': car_count,
                'processed_image': request.build_absolute_uri('/media/' + result_image_path)
            })
        return Response(serializer.errors, status=400)

# Create your views here.
def index(request):
    return render(request, 'index.html')