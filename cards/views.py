import json
from django.http import JsonResponse
from .models import validate_card_data
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from datetime import datetime

@method_decorator(csrf_exempt, name='dispatch')
class AddCardView(APIView):
    def post(self, request):
        data = json.loads(request.body)

        try:
            validate_card_data(data)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        try:
            exp_month = int(data.get('exp_month', ''))
            exp_year = int(data.get('exp_year', ''))
        except ValueError:
            return JsonResponse({"error": "Mês ou ano de expiração inválidos."}, status=400)

        # Salvar dados no MongoDB
        card_data = {
            "client_id": data["client_id"],
            "number": data["number"],
            "exp_month": exp_month,
            "exp_year": exp_year,
            "name": data["name"],
            "nickname": data["nickname"],
            "created_at": datetime.now()
        }

        settings.MONGO_DB.cards.insert_one(card_data)
        return JsonResponse({"message": "Cartão adicionado com sucesso!"}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class GetValidCardsView(APIView):
    def get(self, request, client_id):
        current_year = datetime.now().year % 100
        current_month = datetime.now().month

        cards = list(settings.MONGO_DB.cards.find({
            "client_id": client_id,
            "exp_year": {"$gte": current_year},
            "$or": [
                {"exp_year": {"$gt": current_year}},
                {"exp_month": {"$gte": current_month}}
            ]
        }, {"_id": 0, "number": 1, "exp_month": 1, "exp_year": 1, "name": 1, "nickname": 1}))

        return JsonResponse({"valid_cards": cards}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class GetCardDetailsView(APIView):
    def get(self, request, client_id, number):
        card = settings.MONGO_DB.cards.find_one({
            "client_id": client_id,
            "number": number
        }, {"_id": 0})

        if not card:
            return JsonResponse({"error": "Cartão não encontrado."}, status=404)

        return JsonResponse({"card_details": card}, status=200)
