from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product, Review

class Command(BaseCommand):
    help = 'Seeds the database with categories, products, and reviews'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Seeding database...'))

        # Create demo users
        demo_user, _ = User.objects.get_or_create(
            username='alex',
            defaults={
                'email': 'alex@example.com',
                'first_name': 'Alex',
                'last_name': 'Morgan',
            }
        )
        if _:
            demo_user.set_password('password123')
            demo_user.save()
            if hasattr(demo_user, 'profile'):
                demo_user.profile.address = '742 Evergreen Terrace'
                demo_user.profile.city = 'Springfield'
                demo_user.profile.postal_code = '97477'
                demo_user.profile.phone = '+1 (555) 019-2834'
                demo_user.profile.save()

        user2, _ = User.objects.get_or_create(
            username='sarah',
            defaults={
                'email': 'sarah@example.com',
                'first_name': 'Sarah',
                'last_name': 'Connor',
            }
        )
        if _:
            user2.set_password('password123')
            user2.save()

        # Categories
        categories_data = [
            {
                'name': 'Audio & Headphones',
                'description': 'Studio quality sound, noise-canceling headphones, and wireless earbuds.',
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
                'icon': 'Headphones'
            },
            {
                'name': 'Smart Wearables',
                'description': 'Advanced fitness tracking, smartwatches, and stylish wearable tech.',
                'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
                'icon': 'Watch'
            },
            {
                'name': 'Laptops & Computers',
                'description': 'High performance laptops, mechanical keyboards, and precision monitors.',
                'image': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&auto=format&fit=crop&q=80',
                'icon': 'Laptop'
            },
            {
                'name': 'Gaming Gear',
                'description': 'Ultra-fast refresh rate gear, ergonomic controllers, and RGB peripherals.',
                'image': 'https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=800&auto=format&fit=crop&q=80',
                'icon': 'Gamepad2'
            },
            {
                'name': 'Photography & Cameras',
                'description': 'Mirrorless cameras, prime lenses, and cinema-grade stabilizers.',
                'image': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop&q=80',
                'icon': 'Camera'
            },
            {
                'name': 'Smart Home & Living',
                'description': 'Intelligent lighting, smart speakers, and automated home climate controls.',
                'image': 'https://images.unsplash.com/photo-1558002038-1055907df827?w=800&auto=format&fit=crop&q=80',
                'icon': 'Home'
            }
        ]

        cat_map = {}
        for cdata in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cdata['name'],
                defaults=cdata
            )
            cat_map[cdata['name']] = cat

        # Products
        products_data = [
            {
                'category': cat_map['Audio & Headphones'],
                'name': 'AeroPulse ANC Wireless Headphones',
                'description': 'Immerse yourself in crystal-clear acoustic fidelity. Featuring hybrid active noise cancellation (up to -42dB), 45-hour battery life, ultra-plush memory foam ear cups, and multi-device Bluetooth 5.3 connection.',
                'price': 299.99,
                'discount_price': 249.99,
                'stock': 24,
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
                'badge': 'Best Seller',
                'is_featured': True,
                'rating': 4.9,
                'num_reviews': 38,
            },
            {
                'category': cat_map['Audio & Headphones'],
                'name': 'SonicBuds Pro Spatial Audio',
                'description': 'True wireless earbuds engineered with dynamic head tracking, transparency mode, custom high-excursion drivers, and IPX7 water resistance for intense workouts.',
                'price': 179.99,
                'discount_price': 149.99,
                'stock': 40,
                'image': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80',
                'badge': 'Popular',
                'is_featured': True,
                'rating': 4.7,
                'num_reviews': 24,
            },
            {
                'category': cat_map['Smart Wearables'],
                'name': 'Nova Titanium Smartwatch Gen 5',
                'description': 'Aerospace-grade titanium chassis with sapphire crystal AMOLED display. Continuous ECG heart rate monitoring, SPO2 sensor, GPS navigation, and 7-day battery endurance.',
                'price': 399.00,
                'discount_price': 349.00,
                'stock': 18,
                'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
                'badge': 'Featured',
                'is_featured': True,
                'rating': 4.8,
                'num_reviews': 19,
            },
            {
                'category': cat_map['Smart Wearables'],
                'name': 'Zenith Pulse Fitness Band',
                'description': 'Ultra-lightweight sleep and recovery tracker with haptic coaching, swim-proof design, and stress analytics without any monthly subscription fees.',
                'price': 89.99,
                'discount_price': None,
                'stock': 50,
                'image': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&auto=format&fit=crop&q=80',
                'badge': 'Hot',
                'is_featured': False,
                'rating': 4.6,
                'num_reviews': 12,
            },
            {
                'category': cat_map['Laptops & Computers'],
                'name': 'Apex Pro 16 Ultra Laptop',
                'description': 'Supercharged with 12-core silicon, 32GB unified RAM, 1TB NVMe Gen4 SSD, and a breathtaking 3.2K 120Hz Mini-LED Liquid Retina screen designed for creators and developers.',
                'price': 1999.00,
                'discount_price': 1849.00,
                'stock': 10,
                'image': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&auto=format&fit=crop&q=80',
                'badge': 'Flagship',
                'is_featured': True,
                'rating': 4.9,
                'num_reviews': 45,
            },
            {
                'category': cat_map['Laptops & Computers'],
                'name': 'Vanguard 75% Custom Mechanical Keyboard',
                'description': 'Gasket-mounted CNC aluminum keyboard with hot-swappable lubed linear switches, PBT dye-sub keycaps, per-key RGB backlighting, and acoustic dampening foam.',
                'price': 169.99,
                'discount_price': 139.99,
                'stock': 30,
                'image': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80',
                'badge': 'Sale',
                'is_featured': True,
                'rating': 4.9,
                'num_reviews': 28,
            },
            {
                'category': cat_map['Gaming Gear'],
                'name': 'Spectre Elite Wireless Gaming Controller',
                'description': 'Zero-drift Hall Effect analog sticks, mechanical tactile buttons, swappable back paddles, and customizable trigger stops for competitive supremacy on PC and console.',
                'price': 129.99,
                'discount_price': 109.99,
                'stock': 22,
                'image': 'https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=800&auto=format&fit=crop&q=80',
                'badge': 'Top Rated',
                'is_featured': True,
                'rating': 4.8,
                'num_reviews': 31,
            },
            {
                'category': cat_map['Gaming Gear'],
                'name': 'HyperShift 4K Ergonomic Gaming Mouse',
                'description': 'Ultralight 52g magnesium alloy honeycomb shell, 26,000 DPI optical sensor, optical switches rated for 90M clicks, and 4000Hz polling rate wireless receiver.',
                'price': 119.00,
                'discount_price': None,
                'stock': 35,
                'image': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80',
                'badge': 'New',
                'is_featured': False,
                'rating': 4.7,
                'num_reviews': 16,
            },
            {
                'category': cat_map['Photography & Cameras'],
                'name': 'Lumina 4K Mirrorless Cinema Camera',
                'description': 'Full-frame 33MP BSI CMOS sensor with 10-bit 4:2:2 4K 120fps recording, 5-axis IBIS in-body stabilization, real-time eye autofocus, and dual card slots.',
                'price': 1499.00,
                'discount_price': 1399.00,
                'stock': 8,
                'image': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop&q=80',
                'badge': 'Pro Choice',
                'is_featured': True,
                'rating': 4.9,
                'num_reviews': 14,
            },
            {
                'category': cat_map['Smart Home & Living'],
                'name': 'Aura Ambient Smart LED Lightbar',
                'description': 'Dynamic reactive backlighting syncs seamlessly with your display screen audio and visuals. Over 16 million colors, voice control via Alexa/Google, and customizable scenes.',
                'price': 79.99,
                'discount_price': 59.99,
                'stock': 45,
                'image': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=80',
                'badge': 'Sale',
                'is_featured': False,
                'rating': 4.6,
                'num_reviews': 21,
            },
            {
                'category': cat_map['Smart Home & Living'],
                'name': 'OmniSound Studio 360 Smart Speaker',
                'description': 'Room-filling spatial acoustics powered by dual passive radiators and downward-firing subwoofer. Built-in Matter smart home hub and private microphone mute switch.',
                'price': 199.00,
                'discount_price': 169.00,
                'stock': 20,
                'image': 'https://images.unsplash.com/photo-1543512214-318c7553f230?w=800&auto=format&fit=crop&q=80',
                'badge': 'Staff Pick',
                'is_featured': True,
                'rating': 4.8,
                'num_reviews': 17,
            },
            {
                'category': cat_map['Audio & Headphones'],
                'name': 'Retro Hi-Fi Valve Desktop DAC & Amp',
                'description': 'Audiophile tube headphone amplifier with dual ESS Sabre DAC chips, balanced 4.4mm output, warmth and dynamic range for high-impedance headphones.',
                'price': 349.99,
                'discount_price': None,
                'stock': 12,
                'image': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80',
                'badge': 'Audiophile',
                'is_featured': False,
                'rating': 5.0,
                'num_reviews': 9,
            }
        ]

        for pdata in products_data:
            prod, created = Product.objects.get_or_create(
                name=pdata['name'],
                defaults=pdata
            )
            # Create a sample review
            if created:
                Review.objects.get_or_create(
                    product=prod,
                    user=demo_user,
                    defaults={
                        'rating': 5,
                        'comment': 'Outstanding build quality and exceeded my expectations! Fast delivery and works like a charm.'
                    }
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully with categories, products, and sample reviews!'))
