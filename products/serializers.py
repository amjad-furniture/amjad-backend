from rest_framework import serializers
from .models import Category, Material, Product, ProductImage
from categories.serializers import CategorySerializer

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_at']
        read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    material_ids = serializers.PrimaryKeyRelatedField(
        queryset=Material.objects.all(),
        source='materials',
        many=True,
        required=False,
        write_only=True
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
            'id', 'category', 'category_id', 'materials', 'material_ids', 'name', 'sku', 'slug', 'description', 
            'price', 'color', 'width_cm', 'height_cm', 'depth_cm', 'stock', 'country_of_origin', 
            'images', 'uploaded_images','created_at', 'updated_at'
        ]
        read_only_fields = ['sku', 'slug', 'created_at', 'updated_at', 'images']

    def create(self, validated_data):
        # Extract many-to-many and image data before creating the product
        materials = validated_data.pop('materials', [])
        images_data = validated_data.pop('uploaded_images', [])
        
        # Create the product instance
        product = Product.objects.create(**validated_data)
        
        # Handle materials
        if materials:
            product.materials.set(materials)
        
        # Handle images
        for image in images_data:
            ProductImage.objects.create(product=product, image=image)
        
        return product
    
    def update(self, instance, validated_data):
        # Extract many-to-many and image data
        materials = validated_data.pop('materials', None)
        images = validated_data.pop('uploaded_images', None)
        
        # Update the regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update materials if provided
        if materials is not None:
            instance.materials.set(materials)
        
        # Handle new images if provided
        if images:
            for image in images:
                ProductImage.objects.create(product=instance, image=image)
        
        return instance

    def to_representation(self, instance):
        """
        Override to_representation to ensure we get the full nested representation
        after create/update operations
        """
        representation = super().to_representation(instance)
        return representation