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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
    # Handle GET requests separately for unauthenticated users
        if self.request.method == 'GET':
            if self.request.user.is_authenticated:
                # Authenticated users see all products
                return Product.objects.all()
            else:
                # Unauthenticated users see only active products
                return Product.objects.filter(is_active=True)

        # For non-GET methods, return the default queryset (all products)
        return super().get_queryset()

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
