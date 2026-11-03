# [DOC-07] Automatisations

Les automatisations sont des scénarios linéaires : un déclencheur, puis jusqu'à 5 actions à la suite.

## Déclencheurs
Création d'une opportunité, changement d'étape, devis envoyé, ouvert, accepté ou expiré, facture en retard, date précise.

## Actions
Envoyer un e-mail à partir d'un modèle, créer une tâche, modifier un champ, notifier un utilisateur (e-mail ou notification dans l'application), attribuer à un utilisateur, appeler un webhook (offres Équipe et Entreprise).

## Conditions et délais
- Une seule condition de type « si / alors » par scénario. Les branches multiples (« si / sinon ») ne sont pas disponibles.
- Délai d'attente entre deux actions : de 1 heure à 30 jours.

## Quotas d'automatisations actives
5 (Essentiel), 25 (Équipe), illimité (Entreprise).

## Ce qui n'est pas inclus
- Rédaction d'e-mails assistée par intelligence artificielle : non disponible.
- Envoi d'e-mails en masse à une liste de contacts : non (DOC-01).
