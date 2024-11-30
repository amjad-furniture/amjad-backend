from rest_framework import serializers
from .models import Category, Product, ProductImage
from categories.serializers import CategorySerializer


class ProductImageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_at']
        read_only_fields = ['created_at']
        
    def validate_image(self, value):
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError("Only PNG, JPG, and JPEG images are allowed.")
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image file size should not exceed 5MB.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_id",
            "name",
            "sku",
            "slug",
            "description",
            "price",
            "color",
            "length_cm",
            "width_cm",
            "height_cm",
            "depth_cm",
            "stock",
            "country_of_origin",
            "wood_material",
            "fabric_material",
            "upholstery_material",
            "warranty_months",
            "images",
            "uploaded_images",
            "product_video",
            "is_best_seller",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ['sku', 'slug', 'created_at', 'updated_at', 'images']

    def validate_product_video(self, value):
        """Validate the uploaded video file."""
        if not value.name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            raise serializers.ValidationError("Only MP4, MOV, AVI, and MKV video formats are allowed.")
        if value.size > 1 * 1024 * 1024 * 1024:
            raise serializers.ValidationError("Video file size should not exceed 1GB.")
        return value

    def create(self, validated_data):
        images_data = validated_data.pop('uploaded_images', [])
        video_data = validated_data.pop('product_video', None)
        product = Product.objects.create(**validated_data)

        for image in images_data:
            ProductImage.objects.create(product=product, image=image)

        if video_data:
            product.product_video = video_data
            product.save()

        return product

    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', None)
        video_data = validated_data.pop('product_video', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images:
            for image in images:
                ProductImage.objects.create(product=instance, image=image)
        if video_data:
            instance.product_video = video_data
            instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Check if product_video exists
        if instance.product_video:
            request = self.context.get('request')
            video_url = instance.product_video.url

            # If the request context is available, build an absolute URL
            if request is not None:
                video_url = request.build_absolute_uri(video_url)

            # Set the full video URL in the response
            representation['product_video'] = video_url

        return representation
