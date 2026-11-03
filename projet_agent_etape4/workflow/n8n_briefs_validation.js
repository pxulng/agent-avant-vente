// Nœud Code « Briefs » — JEU DE VALIDATION (12 briefs) — NE LANCER QU'UNE SEULE FOIS, PROMPT GELÉ
// Mode : Run Once for All Items. Renvoie un élément par brief : { id, brief }.

const BRIEFS = [
 {
  "id": "V01",
  "brief": "Cabinet de recrutement de 9 personnes sous Outlook. Nous voulons garder l'historique des versions de nos propositions chiffrées, synchroniser Outlook et relancer automatiquement les devis restés sans réponse."
 },
 {
  "id": "V02",
  "brief": "Société de nettoyage industriel de 22 salariés dont 6 chargés d'affaires mobiles. Devis avec des options à cocher, chargés depuis un catalogue de 800 prestations en CSV, factures au format Factur-X, et une application sur smartphone."
 },
 {
  "id": "V03",
  "brief": "Négociant en textile B2B de 16 personnes. Nos devis doivent pouvoir être en dollars et en livres, rédigés en espagnol, avec chiffrement des données et double authentification."
 },
 {
  "id": "V04",
  "brief": "École de langues de 11 personnes. Nous voulons transformer les devis acceptés en factures, facturer un acompte à l'inscription, recevoir une alerte Slack quand un devis est accepté et faire former l'équipe en visioconférence."
 },
 {
  "id": "V05",
  "brief": "Entreprise de 35 personnes. Toute remise supérieure à 15 % doit être validée par un responsable commercial, et au-delà de 30 % par la direction puis par la directrice financière."
 },
 {
  "id": "V06",
  "brief": "Équipe de 8 commerciaux. Nous faisons environ 150 devis par mois, avec des tarifs différents selon les clients, et nous voulons connecter Brevaro à Make."
 },
 {
  "id": "V07",
  "brief": "Industriel de 70 utilisateurs. Nous voulons un engagement contractuel de disponibilité de 99,5 %, l'authentification unique SAML et une migration de nos données réalisée par vos équipes."
 },
 {
  "id": "V08",
  "brief": "Négoce de pièces détachées de 28 personnes. Nous voulons une gestion de stock avec alertes de rupture, un configurateur de produits avec règles de compatibilité, des devis en allemand et une signature électronique qualifiée."
 },
 {
  "id": "V09",
  "brief": "Groupe de 60 personnes. Nous voulons le provisionnement automatique des utilisateurs (SCIM), des rôles personnalisés, une certification SOC 2, un SDK officiel et une API GraphQL."
 },
 {
  "id": "V10",
  "brief": "Association de 20 personnes. Nous avons besoin de savoir si l'outil respecte les règles d'accessibilité (RGAA), de références clients dans le secteur associatif, de la taille maximale des pièces jointes et du temps de réponse de l'API."
 },
 {
  "id": "V11",
  "brief": "Nous voulons remplacer nos tableaux Excel."
 },
 {
  "id": "V12",
  "brief": "Notre direction veut moderniser la relation client et nous demande une proposition. Pouvez-vous nous aider ?"
 }
];

return BRIEFS.map(b => ({ json: b }));
