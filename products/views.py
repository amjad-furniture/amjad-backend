from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from categories.models import Category
from support.models import Support
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.exceptions import NotFound
from django.db.models import Q


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == ["GET", "PATCH"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        # Base queryset
        queryset = Product.objects.all()

        # Get query parameters
        name = self.request.query_params.get("name")
        price = self.request.query_params.get("price")
        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")
        color = self.request.query_params.get("color")
        category_id = self.request.query_params.get("category")
        order_by_price = self.request.query_params.get("order_by_price")
        search = self.request.query_params.get("search")  # New search parameter

        # Apply filters dynamically

        # If 'name' is provided, filter by product name
        if name:
            queryset = queryset.filter(name__icontains=name)

        if price:
            queryset = queryset.filter(price=price)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if color:
            queryset = queryset.filter(color__icontains=color)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Search functionality: filter across name and description
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(color__icontains=search)
            )

        # Apply ordering by price
        if order_by_price == "max":
            queryset = queryset.order_by("-price")  # Order by descending price
        elif order_by_price == "min":
            queryset = queryset.order_by("price")  # Order by ascending price

        # Handle unauthenticated users to return only active products
        if self.request.method == "GET" and not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)

        return queryset

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('image_files')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # Save and validate images
        for image in images:
            image_serializer = ProductImageSerializer(data={'image': image})
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save(product=product)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        images = request.FILES.getlist('image_files')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        if images:
            # Uncomment this line to delete existing images before adding new ones
            # instance.images.all().delete()
            for image in images:
                image_serializer = ProductImageSerializer(data={'image': image})
                image_serializer.is_valid(raise_exception=True)
                image_serializer.save(product=product)

        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def toggle_status(self, request, pk=None):
        """Endpoint to toggle the visibility of a product."""
        product = self.get_object()
        product.is_active = not product.is_active
        product.save()
        status_message = "activated" if product.is_active else "deactivated"
        return Response(
            {"detail": f"Product '{product.name}' has been {status_message}."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def add_images(self, request, pk=None):
        product = self.get_object()
        images = request.FILES.getlist('images')

        if not images:
            return Response(
                {"detail": "No images provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        image_paths = []
        for image in images:
            image_serializer = ProductImageSerializer(data={'image': image})
            if image_serializer.is_valid(raise_exception=True):
                product_image = image_serializer.save(product=product)
                image_paths.append(product_image.image.url)

        return Response(
            {
                "detail": f"{len(images)} images added to product {product.name}.",
                "image_paths": image_paths
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['delete'])
    def delete_images(self, request, pk=None):
        """Endpoint to delete multiple images from a product."""
        product = self.get_object()
        image_ids = request.data.get('image_ids', [])

        if not image_ids:
            return Response(
                {"detail": "No image IDs provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count, _ = ProductImage.objects.filter(id__in=image_ids, product=product).delete()
        return Response(
            {"detail": f"{deleted_count} images deleted from product {product.name}."},
            status=status.HTTP_200_OK
        )


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from products.models import Product
from categories.models import Category
from products.serializers import ProductSerializer  # Assuming you have a serializer


class ProductsByCategoryView(APIView):
    """
    API View to retrieve all products for a specific category.
    """

    def get(self, request, category_id, *args, **kwargs):
        try:
            # Get the category by ID
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise NotFound(detail="Category not found")

        # Retrieve all products for this category 
        products = Product.objects.filter(category=category)

        # Serialize the products
        serializer = ProductSerializer(products, many=True)

        return Response({"category": category.name, "products": serializer.data})


class DashboardStatsView(APIView):
    """
    API View to provide dashboard statistics.
    """

    def get(self, request, *args, **kwargs):
        # 1. All products
        total_products = Product.objects.count()

        # 2. All active products
        active_products = Product.objects.filter(is_active=True).count()

        # 3. All inactive products
        inactive_products = Product.objects.filter(is_active=False).count()

        # 4. All categories
        total_categories = Category.objects.count()

        # 5. Number of products for each category
        categories = Category.objects.all()
        category_stats = [
            {
                "category_name": category.name,
                "product_count": Product.objects.filter(category=category).count(),
            }
            for category in categories
        ]

        # 6. All messages
        total_support_messages = Support.objects.count()

        # 7. New messages (last 24 hours)
        new_support_messages = Support.objects.filter(
            created_at__gte=now() - timedelta(days=1)
        ).count()

        # Prepare response data
        data = {
            "total_products": total_products,
            "active_products": active_products,
            "inactive_products": inactive_products,
            "total_categories": total_categories,
            "category_stats": category_stats,
            "total_support_messages": total_support_messages,
            "new_support_messages": new_support_messages,
        }

        return Response(data)
