from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Promocode, User
import json


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')
            fullname = data.get('fullname')
            phone_number = data.get('phone_number')
            address = data.get('address')

            if not telegram_id or not fullname or not phone_number or not address:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Foydalanuvchini olish yoki yaratish
            user, created = User.objects.get_or_create(telegram_id=telegram_id)

            if not created and user.is_registered:
                return JsonResponse({'error': 'User is already registered.'}, status=400)

            # Foydalanuvchi ma'lumotlarini yangilash
            user.fullname = fullname
            user.phone_number = phone_number
            user.address = address
            user.is_registered = True
            if created:
                user.points = 5  # Ro'yxatdan o'tganda 5 ball beriladi
            user.save()

            return JsonResponse({
                'message': 'User registered successfully.',
                'points': user.points
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ValidatePromocodeView(View):
    def post(self, request):
        try:
            # JSON formatdagi ma'lumotni o'qing
            data = json.loads(request.body)
            print(data)
            code = data.get('code')
            telegram_id = data.get('telegram_id')

            if not code or not telegram_id:
                return JsonResponse({'error': 'Code and Telegram ID are required.'}, status=400)

            # Foydalanuvchini olish
            user = User.objects.filter(telegram_id=telegram_id).first()
            if not user:
                return JsonResponse({'error': 'User not found.'}, status=404)

            # Promokodni tekshirish
            try:
                promocode = Promocode.objects.get(code=code)
            except Promocode.DoesNotExist:
                return JsonResponse({'error': 'Invalid promocode.'}, status=404)

            # Promokod ishlatilganligini tekshirish
            if promocode.used_by:
                return JsonResponse({'error': 'This promocode has already been used.'}, status=400)

            # Foydalanuvchi ballarini yangilash
            promocode.used_by = user.fullname  # Foydalanuvchining to'liq ismi
            promocode.save()
            user.points += promocode.point
            user.save()

            return JsonResponse({
                'message': 'Promocode applied successfully.',
                'category': promocode.category,
                'added_points': promocode.point,
                'total_points': user.points
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
