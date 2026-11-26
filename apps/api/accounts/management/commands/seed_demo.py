from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from listings.models import Listing
from locations.models import Locality, State


class Command(BaseCommand):
    help = "Seed demo Sudanese locations, farmer accounts, and trader accounts for testing."

    def handle(self, *args, **options):
        states_data = [
            {"code": "001", "name_ar": "الخرطوم", "name_en": "Khartoum"},
            {"code": "002", "name_ar": "البحر الأحمر", "name_en": "Red Sea"},
            {"code": "003", "name_ar": "الجزيرة", "name_en": "Gezira"},
            {"code": "004", "name_ar": "القضارف", "name_en": "Gedaref"},
        ]
        states = {}
        for item in states_data:
            state, _ = State.objects.update_or_create(
                code=item["code"],
                defaults={"name_ar": item["name_ar"], "name_en": item["name_en"]},
            )
            states[item["code"]] = state

        localities_data = [
            {"state_code": "001", "name_ar": "أمدرمان", "name_en": "Omdurman"},
            {"state_code": "002", "name_ar": "بورتسودان", "name_en": "Port Sudan"},
            {"state_code": "003", "name_ar": "ود مدني", "name_en": "Wad Madani"},
            {"state_code": "004", "name_ar": "القضارف", "name_en": "Gedaref"},
        ]
        localities = {}
        for item in localities_data:
            locality, _ = Locality.objects.update_or_create(
                state=states[item["state_code"]],
                name_en=item["name_en"],
                defaults={"name_ar": item["name_ar"]},
            )
            localities[item["name_en"]] = locality

        demo_accounts = [
            {
                "username": "farmer1",
                "phone": "+249911111111",
                "password": "demo1234",
                "arabic_full_name": "أحمد محمد إبراهيم",
                "account_type": User.AccountType.FARMER,
                "allow_whatsapp": True,
                "whatsapp_number": "+249911111111",
                "allow_call": True,
                "call_phone": "+249911111111",
                "locality": localities["Wad Madani"],
                "bio": "مزارع ذرة وسمسم — مشروع الجزيرة",
            },
            {
                "username": "farmer2",
                "phone": "+249922222222",
                "password": "demo1234",
                "arabic_full_name": "عثمان عبد الله حسن",
                "account_type": User.AccountType.FARMER,
                "allow_whatsapp": False,
                "whatsapp_number": "",
                "allow_call": True,
                "call_phone": "+249922222222",
                "locality": localities["Gedaref"],
                "bio": "إنتاج السمسم والفول السوداني — القضارف",
            },
            {
                "username": "trader1",
                "phone": "+249933333333",
                "password": "demo1234",
                "arabic_full_name": "شركة النيل للمستلزمات الزراعية",
                "account_type": User.AccountType.TRADER,
                "allow_whatsapp": True,
                "whatsapp_number": "+249933333333",
                "allow_call": True,
                "call_phone": "+249933333333",
                "locality": localities["Omdurman"],
                "bio": "توفير الحبوب والتقاوي والجوالات وشراء المحاصيل الزراعية",
            },
            {
                "username": "trader2",
                "phone": "+249944444444",
                "password": "demo1234",
                "arabic_full_name": "سوق البركة للتجارة الزراعية",
                "account_type": User.AccountType.TRADER,
                "allow_whatsapp": True,
                "whatsapp_number": "+249944444444",
                "allow_call": False,
                "call_phone": "",
                "locality": localities["Port Sudan"],
                "bio": "بيع الجوالات والأسمدة وشراء الذرة والسمسم للتصدير",
            },
        ]

        for account in demo_accounts:
            password = account.pop("password")
            user, created = User.objects.update_or_create(
                username=account["username"],
                defaults=account,
            )
            user.set_password(password)
            user.save()

        # Seed sample listings if none exist
        if not Listing.objects.exists():
            farmer1 = User.objects.get(username="farmer1")
            farmer2 = User.objects.get(username="farmer2")
            trader1 = User.objects.get(username="trader1")
            trader2 = User.objects.get(username="trader2")
            now = timezone.now()
            expiry = now + timedelta(days=30)

            demo_listings = [
                {
                    "author": farmer1,
                    "listing_type": Listing.ListingType.SELL,
                    "product_category": Listing.ProductCategory.SESAME,
                    "product_name": "سمسم أبيض كركدي ممتاز",
                    "price": 120000,
                    "quantity": 50,
                    "unit": Listing.Unit.SACK,
                    "description": "محصول الموسم الحالي، نظيف ومخزن بعناية في ود مدني، جاهز للشحن الفوري.",
                    "expires_at": expiry,
                },
                {
                    "author": farmer2,
                    "listing_type": Listing.ListingType.SELL,
                    "product_category": Listing.ProductCategory.GROUNDNUT,
                    "product_name": "فول سوداني مقشور حبة عريضة",
                    "price": 95000,
                    "quantity": 100,
                    "unit": Listing.Unit.SACK,
                    "description": "فول سوداني درجة أولى من حقول القضارف، جودة عالية للتصدير أو السوق المحلي.",
                    "expires_at": expiry,
                },
                {
                    "author": trader1,
                    "listing_type": Listing.ListingType.SELL,
                    "product_category": Listing.ProductCategory.SACKS,
                    "product_name": "جوالات خيش جديدة للتعبئة",
                    "price": 3500,
                    "quantity": 2000,
                    "unit": Listing.Unit.PIECE,
                    "description": "جوالات خيش متينة ومناسبة لتعبئة الذرة والسمسم، التوصيل متاح لمختلف الولايات.",
                    "expires_at": expiry,
                },
                {
                    "author": trader2,
                    "listing_type": Listing.ListingType.BUY,
                    "product_category": Listing.ProductCategory.SORGHUM,
                    "product_name": "مطلوب شراء ذرة طابت بكميات كبيرة",
                    "price": 85000,
                    "quantity": 300,
                    "unit": Listing.Unit.SACK,
                    "description": "نبحث عن موردين ومزارعين لشراء ذرة طابت درجة أولى، الدفع كاش عند الاستلام.",
                    "expires_at": expiry,
                },
            ]
            for item in demo_listings:
                Listing.objects.create(**item)

        self.stdout.write(self.style.SUCCESS("Seeded demo locations, farmers, traders, and listings successfully."))
