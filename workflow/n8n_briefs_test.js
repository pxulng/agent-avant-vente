// Nœud Code « Briefs » — JEU DE TEST (30 briefs)
// Mode : Run Once for All Items. Renvoie un élément par brief : { id, brief }.

const BRIEFS = [
 {
  "id": "T01",
  "brief": "Bonjour, nous sommes une entreprise de chauffage de 8 salariés. Nos commerciaux préparent leurs devis à partir de notre liste de produits et services, et proposent souvent des options (un adoucisseur, par exemple) que le client accepte ou non. Une fois le devis accepté, nous voulons le transformer en facture, avec un acompte à la commande. Est-ce que Brevaro sait faire cela ?"
 },
 {
  "id": "T02",
  "brief": "Nous sommes une agence de communication de 12 personnes, toutes sur Gmail. Nous voulons retrouver nos échanges de mails dans les fiches clients, être prévenus sur Slack dès qu'un devis est accepté, et envoyer automatiquement une relance quand un devis reste sans réponse. Pouvez-vous nous confirmer que c'est possible ?"
 },
 {
  "id": "T03",
  "brief": "Distributeur de matériel électrique de 25 personnes. Une partie de nos clients est en Espagne et au Royaume-Uni. Nous voulons faire des devis en espagnol, les chiffrer en livres sterling et en euros, et charger notre catalogue d'environ 2 000 références depuis un fichier CSV."
 },
 {
  "id": "T04",
  "brief": "Cabinet de conseil de 6 consultants. Nous modifions beaucoup nos propositions chiffrées avant la signature : il faut garder les différentes versions d'un devis et pouvoir faire des remises ligne par ligne et sur le total. Nos clients sont sensibles à la sécurité : où sont hébergées les données, et la double authentification est-elle possible ?"
 },
 {
  "id": "T05",
  "brief": "Organisme de formation de 30 personnes. Chaque mois nous importons des listes de contacts depuis Excel et nous craignons les doublons. Nous devons aussi émettre des factures électroniques au format Factur-X à partir de nos devis acceptés."
 },
 {
  "id": "T06",
  "brief": "Installateur de panneaux solaires, 18 salariés dont 10 commerciaux souvent chez les clients avec un téléphone ou une tablette. Ils doivent consulter les fiches et créer des devis sur place. Nous voulons aussi savoir si les données sont chiffrées et si Brevaro propose un accompagnement à la mise en place."
 },
 {
  "id": "T07",
  "brief": "Cabinet d'architectes de 10 personnes sous Outlook. Nous voulons synchroniser mails et rendez-vous, garder l'historique des révisions de chaque devis (nous en faisons parfois une quinzaine pour un même projet) et facturer par acomptes selon l'avancement des chantiers."
 },
 {
  "id": "T08",
  "brief": "Grossiste en boissons, 40 personnes. Nous voulons des remises en pourcentage ou en montant, par ligne et sur le total du devis. Quelques clients nous paient en livres sterling. Notre DSI demande la double authentification et un hébergement dans l'Union européenne."
 },
 {
  "id": "T09",
  "brief": "Bureau d'études de 15 personnes qui travaille sous Gmail et Slack. Nous voulons importer nos contacts depuis un CSV sans créer de doublons, synchroniser Gmail, recevoir des notifications Slack sur les nouvelles opportunités et relancer automatiquement les devis expirés."
 },
 {
  "id": "T10",
  "brief": "Agence événementielle de 20 personnes. Nos devis sont construits depuis un catalogue de prestations, nos factures doivent être au format Factur-X, nos chargés de compte voudraient une application mobile, et nous aimerions un pack de formation pour toute l'équipe."
 },
 {
  "id": "T11",
  "brief": "Société de services de 4 personnes. Nous voulons faire signer les devis en ligne par nos clients et leur envoyer un lien pour payer par carte bancaire. Quelle offre faut-il prendre, et combien cela nous coûterait-il par mois ?"
 },
 {
  "id": "T12",
  "brief": "Entreprise de 60 utilisateurs. Notre DSI exige l'authentification unique SAML avec notre annuaire et un journal d'audit de toutes les actions. Quelle offre est nécessaire ?"
 },
 {
  "id": "T13",
  "brief": "Nous sommes 15 commerciaux. Nous voulons connecter Brevaro à notre site web et à Zapier. Nous estimons faire environ 3 000 appels d'API par jour. Est-ce possible, et avec quelle offre ?"
 },
 {
  "id": "T14",
  "brief": "Distributeur de 20 commerciaux avec trois gammes de produits vendues par des équipes distinctes. Nous voulons trois pipelines séparés, répartir automatiquement les nouvelles opportunités entre commerciaux et créer environ huit rapports personnalisés."
 },
 {
  "id": "T15",
  "brief": "Nous utilisons HubSpot (12 personnes). Nous voulons garder HubSpot synchronisé avec Brevaro pendant six mois de transition, puis basculer. Pouvez-vous aussi migrer nos données pour nous ?"
 },
 {
  "id": "T16",
  "brief": "Petite société de conseil, deux associés. Nous voulons des relances automatiques de nos factures impayées. Quelle offre faut-il ?"
 },
 {
  "id": "T17",
  "brief": "Dix commerciaux terrain souvent sans réseau. Ils doivent pouvoir créer des devis hors connexion et faire signer le client sur leur écran pendant le rendez-vous."
 },
 {
  "id": "T18",
  "brief": "Nous sommes 45 utilisateurs et envisageons l'offre Équipe. Quel serait notre budget annuel ? Une remise est-elle possible ?"
 },
 {
  "id": "T19",
  "brief": "Réseau de franchises de 80 points de vente avec une maison mère et des filiales. Nous voulons voir les comptes en arborescence (groupe, filiale, magasin) et que les fiches soient enrichies automatiquement (numéro SIREN, effectifs)."
 },
 {
  "id": "T20",
  "brief": "Nous devons émettre des factures électroniques transmises via une plateforme agréée dès l'an prochain. Brevaro sera-t-il prêt ? À quelle date ?"
 },
 {
  "id": "T21",
  "brief": "Société de 30 personnes qui vend aux États-Unis, en Suisse et en Allemagne. Nous avons besoin de gérer les taxes à la vente américaines, de faire des devis en francs suisses et en allemand, et d'avoir des taux de change mis à jour automatiquement."
 },
 {
  "id": "T22",
  "brief": "Clinique privée de 90 salariés. Nous manipulons des données de santé. Il nous faut un hébergement certifié pour les données de santé, une certification ISO 27001, un hébergement garanti en France et, idéalement, la qualification SecNumCloud."
 },
 {
  "id": "T23",
  "brief": "ESN de 50 personnes. Nous utilisons SAP et Salesforce et voulons des connecteurs natifs avec les deux, des notifications dans Microsoft Teams et un connecteur avec notre logiciel de comptabilité."
 },
 {
  "id": "T24",
  "brief": "Éditeur de logiciels de 25 personnes. Pouvez-vous nous dire si vous prévoyez des fonctions d'IA l'an prochain, si Brevaro fonctionne avec Odoo ou Zoho, et si vous proposez déjà des prévisions de ventes par intelligence artificielle ?"
 },
 {
  "id": "T25",
  "brief": "Société de services de 35 personnes qui vend des abonnements mensuels. Nous voulons des devis récurrents, une facturation récurrente et le prélèvement SEPA automatique."
 },
 {
  "id": "T26",
  "brief": "Nous répondons à un appel d'offres : engagement de disponibilité contractuel de 99,5 %, support téléphonique 24 h sur 24 et 7 jours sur 7, et objectifs de reprise après sinistre (RTO et RPO) chiffrés."
 },
 {
  "id": "T27",
  "brief": "Bonjour, nous cherchons un outil pour mieux vendre. Que proposez-vous ?"
 },
 {
  "id": "T28",
  "brief": "Nous avons déjà un CRM, mais il ne nous convient plus. Brevaro pourrait-il le remplacer ?"
 },
 {
  "id": "T29",
  "brief": "Nous voulons de l'intelligence artificielle et de l'automatisation dans notre prospection commerciale. Brevaro peut-il le faire ?"
 },
 {
  "id": "T30",
  "brief": "Combien coûte Brevaro pour notre entreprise ?"
 }
];

return BRIEFS.map(b => ({ json: b }));
