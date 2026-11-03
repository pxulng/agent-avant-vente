#!/usr/bin/env python3
"""Référence 1 : recherche par mots-clés, sans IA, sans racines ni synonymes (réglage SMART = false).
Pour chaque besoin de la clé qui a une page source, on interroge la recherche avec le brief entier et on regarde si
une des pages attendues figure parmi les 4 passages renvoyés (mesure indulgente : une seule page attendue suffit).
Cette référence ne produit aucune réponse : elle ne dit ni statut, ni offre, ni calcul, ni question.
Usage : python3 run_reference1.py test"""
import csv, json, os, re, subprocess, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jeu = sys.argv[1] if len(sys.argv) > 1 else 'test'
code = open(ROOT + '/workflow/code_outils/search_docs.js', encoding='utf-8').read().replace('const SMART = true;', 'const SMART = false;')
assert 'const SMART = false;' in code
fmap = {r['id']: r for r in csv.DictReader(open(ROOT + '/evaluation/carte_fonctionnalites_CLE.csv', encoding='utf-8'), delimiter=';')}
briefs = {r['id']: r['brief'] for r in csv.DictReader(open(f'{ROOT}/data/briefs_{jeu}.csv', encoding='utf-8'), delimiter=';')}
cle = list(csv.DictReader(open(f'{ROOT}/evaluation/cle_briefs_{jeu}.csv', encoding='utf-8'), delimiter=';'))

queries = []
for r in cle:
    f = fmap.get(r['feature_id'])
    if not f or not f['source']: continue
    queries.append(dict(brief=r['brief_id'], cat=r['categorie'], docs=sorted(set(re.findall(r'DOC-\d+', f['source']))), query=briefs[r['brief_id']]))
harness = "const code=process.argv[1];const qs=JSON.parse(require('fs').readFileSync(0,'utf8'));" \
          "const out=qs.map(q=>{const r=JSON.parse(new Function('query',code)(q));return Array.isArray(r)?r.map(x=>x.doc||x.id.split('#')[0]):[];});console.log(JSON.stringify(out));"
p = subprocess.run(['node', '-e', harness, code], input=json.dumps([q['query'] for q in queries]), capture_output=True, text=True, check=True)
res = json.loads(p.stdout)
tot = collections.Counter(); hit = collections.Counter()
for q, r in zip(queries, res):
    for key in ('TOUS', q['cat']):
        tot[key] += 1
        hit[key] += any(d in r for d in q['docs'])
print(f'Jeu {jeu} : {tot["TOUS"]} besoins avec page source (les besoins non documentés, les calculs et les questions n\'en ont pas)')
for key in ('TOUS', 'couvert', 'partiel', 'hors_perimetre', 'vague'):
    if tot[key]: print(f'{key:15s} {tot[key]:3d} besoins | bonne page parmi les 4 passages : {hit[key]:3d} = {100*hit[key]/tot[key]:.0f} %')
