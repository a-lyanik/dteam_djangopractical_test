import json
from openai import OpenAI
from django.conf import settings
from django.forms.models import model_to_dict
from .models import CVInstance


def translate_text(cv_id: int, language: str):
    """
    Call OpenAi to translate a CV data
    """
    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
    )

    cv_instance = CVInstance.objects.get(pk=cv_id)
    cv_dict = model_to_dict(cv_instance)
    cv_json = json.dumps(cv_dict)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content':
                    'Translate the following CV content into '  + language +
                    '(Prioritise to translate even if approximate '
                    'and with some original words! '
                    'If you cant - say why you cant translate '
                    'to that language exactly!). '
                    'Return either the json or the reason why you cant. '
                    'Don\'t ask questions.',
            },
            {'role': 'user', 'content': cv_json},
        ]
    )

    translated_cv = response.choices[0].message.content

    # Sometimes gpt cant translate we can show the user why.
    try:
        translated_cv = json.loads(translated_cv)
    except ValueError as e:
        translated_cv = {"error": response.choices[0].message.content}

    return translated_cv
