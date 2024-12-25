from django.http import JsonResponse
from django.views import View
from .models import Promocode

class ValidatePromocodeView(View):
    def post(self, request):
        code = request.POST.get('code', None)
        user = request.POST.get('user', None)

        if not code or not user:
            return JsonResponse({'error': 'Code and user information are required.'}, status=400)

        try:
            promocode = Promocode.objects.get(code=code)
        except Promocode.DoesNotExist:
            return JsonResponse({'error': 'Invalid promocode.'}, status=404)

        if promocode.used_by:
            return JsonResponse({'error': 'This promocode has already been used.'}, status=400)
        promocode.used_by = user
        promocode.save()

        return JsonResponse({
            'message': 'Promocode applied successfully.',
            'category': promocode.category,
            'point': promocode.point,
        })
