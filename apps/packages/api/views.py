from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.packages.api.serializers import PackageSerializer, PackageCategorySerializer
from apps.packages.models import Package, PackageCategory


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated, ]


class ListCreateCategoriesView(APIView):

    def get(self, request, pk=-1, format=None):
        try:
            category = PackageCategory.objects.get(id=pk)
            response = PackageCategorySerializer(category, many=False).data
            response['parents'] = PackageCategorySerializer(category.parents, many=True).data
            response['children'] = PackageCategorySerializer(category.children, many=True).data
            response['siblings'] = PackageCategorySerializer(category.siblings, many=True).data
            return Response(response)
        except PackageCategory.DoesNotExist:
            return Response({'message': 'The requested category does not exists'}, status=status.HTTP_404_NOT_FOUND)

