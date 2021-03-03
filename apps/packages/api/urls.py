from django.urls import path

from apps.packages.api.views import PackageViewSet, ListCreateCategoriesView

package_list = PackageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

package_detail = PackageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('package-list/', package_list, name='package-list'),
    path('package-detail/<int:pk>/', package_detail, name='package-detail'),
    path('', ListCreateCategoriesView.as_view(), name='get-categories'),
]

