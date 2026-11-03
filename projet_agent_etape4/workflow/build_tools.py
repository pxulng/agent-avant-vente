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

# ------------------------------------------- 2 et 3. offres et intégrations
# Les fichiers JSON de data/tools/ sont la source de vérité : on les modifie, puis on relance ce script.
P = json.load(open(TOOLS + "/offres.json", encoding="utf-8"))["plans"]
offres = json.load(open(TOOLS + "/offres.json", encoding="utf-8"))["attributs"]
integrations = json.load(open(TOOLS + "/integrations.json", encoding="utf-8"))

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
return JSON.stringify({ statut: 'non_documente', message: 'Cet outil n\'apparaît pas dans la documentation de compatibilité de Brevaro. Ne pas le présenter comme disponible, ni affirmer qu\'il est impossible : à confirmer auprès de l\'éditeur avant de répondre au client.' });
"""

open(CODE + "/search_docs.js", "w", encoding="utf-8").write(search_js)
open(CODE + "/get_plan_limits.js", "w", encoding="utf-8").write(plans_js)
open(CODE + "/check_integration.js", "w", encoding="utf-8").write(integ_js)
print(len(chunks), "passages;", len(offres), "attributs;", len(integrations), "intégrations")
