from django.core.management.base import BaseCommand
from api.models import Product

# Lista de productos de ejemplo
PRODUCTS = [
    {"name": "Camiseta básica", "description": "Camiseta 100% algodón", "price": 12.50, "stock": 30, "image_url": ""},
    {"name": "Pantalón vaquero", "description": "Vaqueros slim fit", "price": 39.90, "stock": 12, "image_url": ""},
    {"name": "Auriculares inalámbricos", "description": "Bluetooth 5.0", "price": 59.99, "stock": 8, "image_url": ""},
    {"name": "Taza personalizada", "description": "Taza con logo", "price": 7.99, "stock": 50, "image_url": ""},
    {"name": "Base para móvil", "description": "Soporte plegable", "price": 9.50, "stock": 22, "image_url": ""},
]

class Command(BaseCommand):
    help = "Puebla la base de datos con productos de ejemplo"

    def handle(self, *args, **options):
        created = 0
        for p in PRODUCTS:
            # Usamos solo el nombre para identificar duplicados
            obj, was_created = Product.objects.get_or_create(
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