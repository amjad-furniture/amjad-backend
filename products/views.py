from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

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
