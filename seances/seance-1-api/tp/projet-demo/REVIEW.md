# Review de la ressource reservations

| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Codes de statut 201, 404, 409 | OK | |
| `response_model` sur les 4 routes | OK | |
| Validation `date_fin > date_debut` dans Pydantic | OK | |
| Aucun accès au stockage de `items` | OK | |
| Pas d'`async def` sans `await` | OK | |
| Aucune dépendance inutile ajoutée | OK | |
| Routes littérales avant routes paramétrées | OK | |
| `POST /reservations/999/annuler` renvoie 404 | OK | |