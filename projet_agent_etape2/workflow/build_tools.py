#!/usr/bin/env python3
"""Génère les données et le code JavaScript des trois outils de l'agent (n8n Code Tool)."""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "data/docs")
TOOLS = os.path.join(ROOT, "data/tools")
CODE = os.path.join(ROOT, "workflow/code_outils")

# ---------------------------------------------------------------- 1. chunks
chunks = []
for f in sorted(glob.glob(DOCS + "/DOC-*.md")):
    doc = re.search(r"DOC-\d+", os.path.basename(f)).group()
    text = open(f, encoding="utf-8").read()
    title = re.search(r"^# \[DOC-\d+\] (.+)$", text, re.M).group(1)
    parts = re.split(r"(?m)^(?=## )", text)
    for i, p in enumerate(parts):
        p = p.strip()
        if not p:
            continue
        m = re.match(r"## (.+)", p)
        section = m.group(1) if m else "Introduction"
        chunks.append({
            "id": f"{doc}#{i}",
            "doc": doc,
            "titre": f"{title} — {section}",
            "texte": re.sub(r"^# .+\n+", "", p) if not m else p,
        })
json.dump(chunks, open(TOOLS + "/docs_chunks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- 2. offres
P = ["Essentiel", "Équipe", "Entreprise"]
def a(cle, libelle, mots, e, q, n, source):
    return {"cle": cle, "libelle": libelle, "mots_cles": mots,
            "valeurs": {"Essentiel": e, "Équipe": q, "Entreprise": n}, "source": source}

OUI, NON = "oui", "non"
offres = [
    a("prix", "Prix par utilisateur et par mois (HT, engagement annuel)", ["prix", "tarif", "cout", "combien", "euro", "abonnement", "budget"], "19 €", "39 €", "sur devis", "DOC-12"),
    a("utilisateurs", "Nombre d'utilisateurs", ["utilisateur", "licence", "siege", "poste", "salarie", "commercial", "taille"], "1 à 5", "3 à 50", "à partir de 20", "DOC-12"),
    a("devis_mois", "Nombre de devis par mois", ["devis"], "100", "illimité", "illimité", "DOC-12"),
    a("pipelines", "Nombre de pipelines de vente", ["pipeline", "entonnoir"], "1", "3", "10", "DOC-04, DOC-12"),
    a("champs", "Champs personnalisés", ["champ", "personnalise"], "20", "50", "100", "DOC-05, DOC-12"),
    a("automatisations", "Automatisations actives", ["automatisation", "scenario", "workflow", "relance"], "5", "25", "illimité", "DOC-07, DOC-12"),
    a("stockage", "Stockage", ["stockage", "espace", "go", "fichier"], "5 Go", "50 Go", "500 Go", "DOC-12"),
    a("api", "API : appels par jour", ["api", "rest", "appel", "integration"], "aucun accès", "1 000", "20 000", "DOC-09, DOC-12"),
    a("webhooks", "Webhooks", ["webhook"], NON, "oui (20 types d'événements)", "oui (20 types d'événements)", "DOC-09, DOC-12"),
    a("signature", "Signature électronique simple des devis (pas de signature avancée ni qualifiée)", ["signature", "signer", "eidas", "electronique"], NON, OUI, OUI, "DOC-02, DOC-12"),
    a("signature_mobile", "Signature sur l'écran du client en rendez-vous (application mobile)", ["mobile", "tablette", "rendez-vous"], NON, OUI, OUI, "DOC-15"),
    a("relances_factures", "Relances automatiques des factures impayées (3 niveaux)", ["impaye", "recouvrement", "facture"], NON, OUI, OUI, "DOC-06, DOC-12"),
    a("paiement_carte", "Lien de paiement par carte bancaire", ["paiement", "carte", "payer"], NON, OUI, OUI, "DOC-06"),
    a("sso", "Authentification unique SSO (SAML)", ["sso", "saml", "authentification", "annuaire"], NON, NON, OUI, "DOC-10, DOC-12"),
    a("audit", "Journal d'audit (conservé 12 mois)", ["audit", "journal", "tracabilite"], NON, NON, OUI, "DOC-10, DOC-12"),
    a("double_auth", "Double authentification", ["double", "2fa", "mfa", "totp"], OUI, OUI, OUI, "DOC-10"),
    a("support", "Support", ["support", "assistance", "reponse", "chat", "telephone"], "e-mail, réponse sous 2 jours ouvrés", "e-mail et chat (9 h à 18 h, heure de Paris, jours ouvrés), réponse sous 1 jour ouvré", "gestionnaire de compte dédié, réponse sous 4 heures ouvrées pour les incidents critiques", "DOC-14, DOC-12"),
    a("sla", "SLA contractuel de disponibilité 99,5 % avec crédits de service", ["sla", "disponibilite", "engagement", "uptime"], NON, NON, OUI, "DOC-14"),
    a("rapports", "Rapports personnalisés", ["rapport", "reporting", "tableau"], "aucun (6 tableaux de bord prédéfinis)", "10 (et 6 tableaux de bord prédéfinis)", "illimités (et 6 tableaux de bord prédéfinis)", "DOC-04"),
    a("equipes", "Équipes (groupes d'utilisateurs)", ["equipe", "groupe"], "aucune", "jusqu'à 10", "illimitées", "DOC-11"),
    a("roles", "Rôles disponibles (pas de rôles personnalisés sur aucune offre)", ["role", "droit", "permission", "acces"], "Administrateur et Commercial seulement", "Administrateur, Manager, Commercial, Lecture seule", "Administrateur, Manager, Commercial, Lecture seule", "DOC-11"),
    a("grilles_prix", "Grilles de prix par client ou segment", ["grille", "segment", "tarification"], NON, OUI, OUI, "DOC-03"),
    a("validation_devis", "Validation d'un devis à une étape par un manager (pas de validation à plusieurs niveaux)", ["validation", "approbation", "circuit", "remise"], NON, OUI, OUI, "DOC-02"),
    a("attribution_auto", "Attribution automatique des opportunités (tour de rôle)", ["attribution", "repartition", "round"], NON, OUI, OUI, "DOC-04"),
    a("objectifs", "Objectifs de vente par commercial", ["objectif", "quota"], NON, OUI, OUI, "DOC-04"),
    a("zapier_make", "Zapier et Make (via API et webhooks)", ["zapier", "make", "automatisation"], NON, OUI, OUI, "DOC-08"),
    a("bac_a_sable", "Environnement de test (bac à sable) de l'API", ["sandbox", "bac", "test", "recette"], NON, NON, OUI, "DOC-09"),
    a("migration_assistee", "Migration de données assistée par les équipes de Brevaro", ["migration", "reprise", "import"], NON, NON, "oui, sur devis", "DOC-13"),
    a("accompagnement", "Pack d'accompagnement de 2 jours (configuration et formation en visioconférence), 2 400 € HT", ["accompagnement", "formation", "onboarding", "deploiement", "pack"], OUI, OUI, OUI, "DOC-13"),
    a("remise_volume", "Remise sur volume", ["remise", "volume", "degressif", "negociation"], "aucune remise publiée", "aucune remise publiée", "aucune remise publiée ; se discute dans le devis Entreprise", "DOC-12"),
    a("nombre_contacts", "Nombre maximal de contacts", ["contact", "limite", "maximum"], "non documenté", "non documenté", "non documenté", "DOC-12 (la documentation ne donne pas de limite : ce n'est pas une garantie d'illimité)"),
]
json.dump({"plans": P, "attributs": offres}, open(TOOLS + "/offres.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- 3. intégrations
def i(nom, alias, statut, detail, offres_txt, source):
    return {"nom": nom, "alias": alias, "statut": statut, "detail": detail, "offres": offres_txt, "source": source}

integrations = [
    i("Google Workspace (Gmail, Google Agenda)", ["google", "gmail", "google agenda", "google calendar", "g suite", "gsuite"], "natif", "Synchronisation dans les deux sens des e-mails et des rendez-vous.", "la documentation ne restreint pas par offre", "DOC-08"),
    i("Microsoft 365 (Outlook, Calendrier)", ["microsoft 365", "office 365", "outlook", "microsoft calendar", "calendrier microsoft", "m365"], "natif", "Synchronisation dans les deux sens des e-mails et des rendez-vous.", "la documentation ne restreint pas par offre", "DOC-08"),
    i("Slack", ["slack"], "natif", "Notifications d'événements uniquement (nouvelle opportunité, devis accepté).", "la documentation ne restreint pas par offre", "DOC-08"),
    i("Zapier", ["zapier"], "via_api_ou_automatisation", "Connexion via l'API et les webhooks.", "Équipe et Entreprise", "DOC-08"),
    i("Make", ["make", "integromat"], "via_api_ou_automatisation", "Connexion via l'API et les webhooks.", "Équipe et Entreprise", "DOC-08"),
    i("HubSpot", ["hubspot"], "migration_ponctuelle", "Import CSV guidé, une seule fois. Pas de synchronisation continue.", "la documentation ne restreint pas par offre", "DOC-08"),
    i("Pipedrive", ["pipedrive"], "migration_ponctuelle", "Import CSV guidé, une seule fois. Pas de synchronisation continue.", "la documentation ne restreint pas par offre", "DOC-08"),
    i("Salesforce", ["salesforce"], "non_disponible", "Aucun connecteur. Le client ou un intégrateur peut utiliser l'API (aucun accès API sur Essentiel).", "—", "DOC-08, DOC-09"),
    i("SAP", ["sap", "erp sap", "s/4hana", "s4hana"], "non_disponible", "Aucun connecteur. Le client ou un intégrateur peut utiliser l'API (aucun accès API sur Essentiel).", "—", "DOC-08, DOC-09"),
    i("Microsoft Dynamics", ["dynamics", "dynamics 365"], "non_disponible", "Aucun connecteur. Le client ou un intégrateur peut utiliser l'API (aucun accès API sur Essentiel).", "—", "DOC-08, DOC-09"),
    i("Microsoft Teams", ["teams", "microsoft teams"], "non_disponible", "Pas de notifications Teams.", "—", "DOC-08"),
    i("Logiciels de comptabilité", ["comptabilite", "comptable", "logiciel comptable", "expert comptable", "export comptable"], "non_disponible", "Aucun connecteur natif. Export CSV des factures et des paiements uniquement.", "—", "DOC-06, DOC-08"),
    i("Téléphonie", ["telephonie", "telephone", "voip", "appel", "standard telephonique"], "non_disponible", "Pas de téléphonie intégrée ni d'enregistrement des appels. Le clic pour appeler ouvre l'application téléphone de l'utilisateur.", "—", "DOC-05, DOC-08"),
]
json.dump(integrations, open(TOOLS + "/integrations.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- code JS
COMMON = r"""
const norm = s => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
const STOP = new Set(['de','du','la','le','les','un','une','des','et','ou','en','au','aux','par','pour','sur','est','il','elle','que','qui','dans','avec','sans','ce','se','sa','son','ses','ca','cela','ne','pas','plus','peut','faut','vous','nous','on','y','a','ont','sont','etre','avoir','fait','faire']);
const stem = w => (w.length > 3 ? w.replace(/(s|x)$/, '') : w);
const toks = s => norm(s).split(' ').filter(w => w.length > 1 && !STOP.has(w)).map(stem);
"""

SEARCH_COMMON = COMMON + r"""
// Réglage : false = recherche par mots exacts seulement (référence « mots-clés » de l'évaluation).
const SMART = true;
// Racine approximative d'un mot (les 5 premières lettres), pour rapprocher restaurer / restauration.
const root = w => (SMART && w.length > 5 ? w.slice(0, 5) : w);
// Petit dictionnaire de synonymes, appliqué à la requête seulement. Rédigé à la main, donc limité.
const SYN = {
  europe: ['union', 'europeenne', 'hebergement'], hebergees: ['hebergement'], donnees: ['donnees'],
  chiffrees: ['chiffrement'], chiffrement: ['chiffrement', 'aes', 'tls'], securite: ['securite', 'chiffrement'],
  restaurer: ['restauration', 'sauvegarde'], recuperer: ['sauvegarde', 'export', 'import', 'migration'], perdre: ['sauvegarde', 'restauration'],
  payer: ['paiement', 'carte'], reglement: ['paiement'], virement: ['sepa', 'paiement'], prelevement: ['sepa'],
  rappeler: ['relance', 'automatisation'], relancer: ['relance', 'automatisation'], rappel: ['relance'],
  erp: ['sap', 'connecteur', 'salesforce', 'dynamics', 'api'], crm: ['salesforce', 'hubspot', 'pipedrive', 'migration'],
  former: ['formation', 'accompagnement', 'webinaire'], formation: ['accompagnement', 'webinaire', 'pack'], apprendre: ['formation'],
  exporter: ['export', 'csv'], quitter: ['export', 'csv', 'donnees'], sortir: ['export', 'csv'],
  signer: ['signature'], signature: ['electronique'], tablette: ['mobile', 'tablette'], iphone: ['ios', 'mobile', 'application'], android: ['mobile'],
  telephone: ['mobile', 'telephonie'], smartphone: ['mobile', 'ios', 'android'], application: ['mobile', 'ios', 'android'],
  internet: ['connexion', 'hors'], deplacement: ['mobile', 'hors'], offline: ['hors', 'connexion'],
  fiscale: ['facture', 'electronique', 'plateforme', 'agreee'], administration: ['plateforme', 'agreee'], dematerialisation: ['plateforme', 'factur'],
  langue: ['francais', 'anglais', 'espagnol'], annuaire: ['sso', 'saml', 'authentification'], azure: ['sso', 'saml', 'authentification'], okta: ['sso', 'saml'],
  maximum: ['limite', 'nombre'], formule: ['offre', 'essentiel', 'equipe', 'entreprise'], base: ['essentiel'], gamme: ['offre'],
  cout: ['prix', 'tarif'], combien: ['prix', 'nombre'], tarif: ['prix'], budget: ['prix'],
  chiffre: ['prevision', 'montant', 'objectif'], affaires: ['prevision', 'montant'], trimestre: ['prevision', 'trimestrielle'], ventes: ['opportunite', 'pipeline'],
  site: ['api', 'webhook'], appeler: ['api', 'webhook'], developpeur: ['api', 'webhook', 'sdk'],
  accord: ['validation', 'manager'], responsable: ['manager', 'validation'], approbation: ['validation', 'manager'],
  doublons: ['doublon', 'fusion'], authentification: ['authentification', 'double'], panne: ['incident', 'disponibilite', 'support'],
  ia: ['intelligence', 'artificielle'], 'intelligence': ['ia'], certification: ['iso', 'soc'], rgpd: ['rgpd', 'dpa', 'consentement', 'effacement']
};
const toksQ = s => {
  const base = norm(s).split(' ').filter(w => w.length > 1 && !STOP.has(w));
  const extra = SMART ? base.flatMap(w => SYN[w] || []) : [];
  return [...new Set([...base, ...extra].map(w => root(stem(w))))];
};
const toksD = s => [...new Set(norm(s).split(' ').filter(w => w.length > 1 && !STOP.has(w)).map(w => root(stem(w))))];
"""

search_js = "// OUTIL 1 : search_docs — recherche dans la documentation Brevaro (n8n Code Tool, JavaScript)\n" \
    "// Entrée : `query` (texte). Sortie : les 4 passages les plus proches, avec leur identifiant.\n" \
    "// Méthode : correspondance de mots (racines de 5 lettres) pondérée par rareté, plus un petit dictionnaire de synonymes. Pas de recherche sémantique.\n" \
    + SEARCH_COMMON + "\nconst CHUNKS = " + json.dumps(chunks, ensure_ascii=False) + ";\n" + r"""
const q = toksQ(query);
if (q.length === 0) return JSON.stringify({ resultat: 'requête vide' });
const sets = CHUNKS.map(c => new Set(toksD(c.titre + ' ' + c.texte)));
const N = CHUNKS.length;
const idf = {};
for (const t of q) { const df = sets.filter(s => s.has(t)).length; idf[t] = Math.log(1 + N / (1 + df)); }
const scored = CHUNKS.map((c, k) => ({ c, score: q.reduce((acc, t) => acc + (sets[k].has(t) ? idf[t] : 0), 0) }))
  .filter(x => x.score > 0).sort((a, b) => b.score - a.score).slice(0, 4);
if (scored.length === 0) return JSON.stringify({ resultat: 'aucun passage trouvé', conseil: 'reformuler avec d\'autres mots ; si rien ne correspond, le point n\'est pas documenté' });
return JSON.stringify(scored.map(x => ({ id: x.c.id, titre: x.c.titre, texte: x.c.texte, score: Math.round(x.score * 100) / 100 })));
"""

plans_js = "// OUTIL 2 : get_plan_limits — offres, prix et limites (n8n Code Tool, JavaScript)\n" \
    "// Entrée : `query` (texte libre : nom d'offre et/ou sujet, ex. « Équipe API » ou « signature »). Sortie : valeurs par offre.\n" \
    + COMMON + "\nconst DATA = " + json.dumps({"plans": P, "attributs": offres}, ensure_ascii=False) + ";\n" + r"""
const nq = norm(query);
const planKeys = { essentiel: 'Essentiel', equipe: 'Équipe', entreprise: 'Entreprise' };
let plans = Object.entries(planKeys).filter(([k]) => nq.split(' ').includes(k)).map(([, v]) => v);
const planAsked = plans.length > 0;
if (!planAsked) plans = DATA.plans;
const q = [...new Set(toks(query))].filter(t => !Object.keys(planKeys).includes(t));
const scored = DATA.attributs.map(a => {
  const kw = new Set(a.mots_cles.map(w => stem(norm(w))));
  return { a, score: q.filter(t => kw.has(t)).length };
}).filter(x => x.score > 0).sort((x, y) => y.score - x.score).slice(0, 5);
const pick = a => ({ attribut: a.libelle, source: a.source, valeurs: Object.fromEntries(plans.map(p => [p, a.valeurs[p]])) });
if (scored.length > 0) return JSON.stringify(scored.map(x => pick(x.a)));
if (planAsked) return JSON.stringify(DATA.attributs.map(pick));
return JSON.stringify({ resultat: 'attribut non trouvé dans la table des offres', attributs_disponibles: DATA.attributs.map(a => a.libelle) });
"""

integ_js = "// OUTIL 3 : check_integration — compatibilité avec un outil tiers (n8n Code Tool, JavaScript)\n" \
    "// Entrée : `query` (nom d'un outil, ex. « Salesforce » ou « Outlook »). Sortie : statut documenté, ou « non_documente ».\n" \
    + COMMON + "\nconst INTEGRATIONS = " + json.dumps(integrations, ensure_ascii=False) + ";\n" + r"""
const nq = ' ' + norm(query) + ' ';
let best = null, bestLen = 0;
for (const it of INTEGRATIONS) {
  for (const al of [it.nom, ...it.alias]) {
    const na = norm(al);
    if (na.length > bestLen && nq.includes(' ' + na + ' ')) { best = it; bestLen = na.length; }
  }
}
if (best) return JSON.stringify({ nom: best.nom, statut: best.statut, detail: best.detail, offres: best.offres, source: best.source });
return JSON.stringify({ statut: 'non_documente', message: 'Cet outil n\'apparaît pas dans la documentation de compatibilité de Brevaro. Ne pas conclure ni oui ni non : à vérifier auprès de l\'éditeur.' });
"""

open(CODE + "/search_docs.js", "w", encoding="utf-8").write(search_js)
open(CODE + "/get_plan_limits.js", "w", encoding="utf-8").write(plans_js)
open(CODE + "/check_integration.js", "w", encoding="utf-8").write(integ_js)
print(len(chunks), "passages;", len(offres), "attributs;", len(integrations), "intégrations")
