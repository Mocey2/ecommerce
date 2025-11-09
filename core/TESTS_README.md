# Tests - Application E-commerce

## Lancement des tests

### Avec Django
```bash
python manage.py test
```

### Avec Pytest (recommandé)
```bash
pip install pytest pytest-django pytest-cov
pytest -v
```

## Couverture
```bash
pytest --cov=. --cov-report=html
```

## Structure
- `produit/tests/test_models.py` - Tests unitaires modèles
- `produit/tests/test_views.py` - Tests d'intégration vues
- `pytest.ini` - Configuration Pytest

**Coverage: 80% - 66 tests**
