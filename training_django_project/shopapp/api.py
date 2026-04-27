"""
API ViewSets for ShopApp models.

Models: `Order`, `Product`.
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from shopapp.models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для работы с продуктами в API.

    Полный CRUD функционал для модели `Product`.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = [
        "name",
        "description",
    ]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(
                description="Empty response, product by ID not found",
            ),
        },
    )
    def retrieve(self, *args, **kwargs):
        """
        Получение одного продукта по его идентификатору.

        :param args:
        :param kwargs:
        :return:
        """
        return super().retrieve(*args, **kwargs)


class OrderViewSet(ModelViewSet):
    """
    Набор представлений для работы с заказами в API.

    Полный CRUD функционал для модели `Order`.
    """

    queryset = Order.objects.select_related("user").prefetch_related("products")
    serializer_class = OrderSerializer
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = [
        "delivery_address",
        "products",
    ]
    ordering_fields = [
        "created_at",
    ]
