from datetime import datetime
from django.core.exceptions import ValidationError

def validate_card_data(data):
    # Valida o número do cartão
    if not data.get("number") or len(data["number"]) != 16 or not data["number"].isdigit():
        raise ValidationError("Número do cartão inválido. Deve ter 16 dígitos.")

    # Valida o mês e ano de validade
    current_year = datetime.now().year % 100  # pega os últimos dois dígitos do ano
    current_month = datetime.now().month

    if not data.get("exp_month") or not (1 <= int(data["exp_month"]) <= 12):
        raise ValidationError("Mês de validade inválido. Deve ser entre 01 e 12.")

    if not data.get("exp_year") or not (int(data["exp_year"]) >= current_year and int(data["exp_year"]) <= current_year + 10):
        raise ValidationError("Ano de validade inválido. Deve ser maior ou igual ao ano atual.")

    if int(data["exp_year"]) == current_year and int(data["exp_month"]) < current_month:
        raise ValidationError("Data de validade expirada.")

    # Valida o nome no cartão
    if not data.get("name"):
        raise ValidationError("Nome impresso no cartão é obrigatório.")

    # Valida o apelido do cartão
    if not data.get("nickname"):
        raise ValidationError("Apelido do cartão é obrigatório.")