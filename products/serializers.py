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
        
    def validate_image(self, value):
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError("Only PNG, JPG, and JPEG images are allowed.")
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image file size should not exceed 5MB.")
        return value

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
            'images', 'uploaded_images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['sku', 'slug', 'created_at', 'updated_at', 'images']

    def create(self, validated_data):
        materials = validated_data.pop('materials', [])
        images_data = validated_data.pop('uploaded_images', [])
        
        product = Product.objects.create(**validated_data)
        
        if materials:
            product.materials.set(materials)
        
        for image in images_data:
            ProductImage.objects.create(product=product, image=image)
        
        return product
    
    def update(self, instance, validated_data):
        materials = validated_data.pop('materials', None)
        images = validated_data.pop('uploaded_images', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if materials is not None:
            instance.materials.set(materials)
        
        if images:
            for image in images:
                ProductImage.objects.create(product=instance, image=image)
        
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
