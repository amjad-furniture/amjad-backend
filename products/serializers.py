from rest_framework import serializers
from .models import Category, Material, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


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

    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    material_ids = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), source='materials', many=True, write_only=True)
    
    # New field to accept multiple images on creation/update
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
        materials_data = validated_data.pop('materials', [])
        images_data = validated_data.pop('uploaded_images', [])
        
        product = Product.objects.create(**validated_data)
        product.materials.set(materials_data)
        
        # Save each uploaded image as a ProductImage instance
        for image in images_data:
            ProductImage.objects.create(product=product, image=image)
        
        return product

    def update(self, instance, validated_data):
        materials_data = validated_data.pop('materials', [])
        images_data = validated_data.pop('uploaded_images', [])
        
        instance = super().update(instance, validated_data)
        
        if materials_data:
            instance.materials.set(materials_data)
        
        # Optionally clear existing images or append new ones
        if images_data:
            # Clear existing images if needed:
            # instance.images.all().delete()

            for image in images_data:
                ProductImage.objects.create(product=instance, image=image)
        
        return instance
