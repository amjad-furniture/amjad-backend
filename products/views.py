from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Material, Product, ProductImage
from .serializers import CategorySerializer, MaterialSerializer, ProductSerializer, ProductImageSerializer
from dynamic_rest.viewsets import DynamicModelViewSet


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        # Custom handling for multiple images on product creation
        images = request.FILES.getlist('image_files')  # Get list of uploaded files with 'image_files' key
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # Save images
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # Custom handling for multiple images on product update
        images = request.FILES.getlist('image_files')  # Get list of uploaded files with 'image_files' key
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # Optionally clear existing images or append new ones
        if images:
            # Uncomment the next line if you want to remove existing images on each update
            # instance.images.all().delete()
            
            for image in images:
                ProductImage.objects.create(product=product, image=image)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_images(self, request, pk=None):
        """Endpoint to add multiple images to an existing product and return their paths."""
        product = self.get_object()
        images = request.FILES.getlist('images')
        
        if not images:
            return Response(
                {"detail": "No images provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_paths = []
        for image in images:
            product_image = ProductImage.objects.create(product=product, image=image)
            image_paths.append(product_image.image.url)  # Collect the image URL

        return Response(
            {
                "detail": f"{len(images)} images added to product {product.name}.",
                "image_paths": image_paths
            },
            status=status.HTTP_201_CREATED
        )
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
