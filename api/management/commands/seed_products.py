from django.core.management.base import BaseCommand
from api.models import Product

# Lista de productos de ejemplo
PRODUCTS = [
    {
        "name": "Camiseta básica",
        "description": "Camiseta 100% algodón",
        "price": 12.50,
        "stock": 30,
        "image_url": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRjWttf68uHZujhaOv2RtWOBVZzqNz8gwWzWxeTqsitL85ryIaM0XQJaMvpuPLQdTmVmIYk27VD3yiE82X5uIWqTE5BjC8jv9nbtN4qEvny85cJXTgHJEuvk_6B"
    },
    {
        "name": "Pantalón vaquero",
        "description": "Vaqueros slim fit",
        "price": 39.90,
        "stock": 12,
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQM3nT0fgYOelVAKHvJrg6-qahUCayysFmMBw&s"
    },
    {
        "name": "Gorro de lana",
        "description": "gorro 100% de lana",
        "price": 9.99,
        "stock": 8,
        "image_url": "https://eu-images.contentstack.com/v3/assets/blt7dcd2cfbc90d45de/blt01f0a7f1268f9f8a/60dc07e1a37ada0f2cd0d19b/9-1_copy_5-1.jpg?format=pjpg&auto=webp&quality=75%2C90&width=640"
    },
    {
        "name": "Zapatillas",
        "description": "zapatillas nike",
        "price": 100,
        "stock": 50,
        "image_url": "https://cdn-images.farfetch-contents.com/12/96/03/49/12960349_13486594_600.jpg"
    },
    {
        "name": "Calcetines",
        "description": "",
        "price": 2.99,
        "stock": 22,
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3OY3nuAv4uJHT-OLMulNlj5bplwiYe9B-og&s"
    },
]

class Command(BaseCommand):
    help = "Puebla la base de datos con productos de ejemplo"

    def handle(self, *args, **options):
        created = 0
        for p in PRODUCTS:
            # Usamos solo el nombre para identificar duplicados
            obj, was_created = Product.objects.update_or_create(
                name=p['name'],
                defaults={
                    'description': p['description'],
                    'price': p['price'],
                    'stock': p['stock'],
                    'image_url': p['image_url'],
                }
            )

            # Mensajes por consola
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Creado: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Ya existía: {obj.name}"))

        self.stdout.write(self.style.SUCCESS(f"Seeder finalizado. {created} productos creados."))