// Nœud Code « Lecture » — Mode : Run Once for All Items.
// Lit la réponse du modèle pour chaque brief, vérifie que c'est du JSON valide, relève la consommation de jetons.
// Renvoie UN seul élément avec le champ `resultats` (texte JSON) à copier dans un fichier.

const briefs = $('Briefs').all();
const sorties = $input.all();

const texteDe = (j) => {
  if (j && Array.isArray(j.content) && j.content.length) {
    return j.content.filter(c => c.type === 'text').map(c => c.text).join('');
  }
  return j.text ?? j.output ?? j.response ?? '';
};

const resultats = sorties.map((it, i) => {
  const id = briefs[i] ? briefs[i].json.id : `inconnu_${i}`;
  const brut = texteDe(it.json);
  let fiche = null, json_valide = false;
  try {
    const nettoye = brut.replace(/^\s*```(?:json)?/i, '').replace(/```\s*$/, '').trim();
    fiche = JSON.parse(nettoye);
    json_valide = true;
  } catch (e) { /* on garde le texte brut pour le journal d'erreurs */ }
  const u = it.json.usage || {};
  return {
    id,
    json_valide,
    jetons_entree: u.input_tokens ?? null,
    jetons_sortie: u.output_tokens ?? null,
    fiche,
    brut: json_valide ? undefined : brut,
  };
});

return [{ json: { nb: resultats.length, nb_json_invalides: resultats.filter(r => !r.json_valide).length, resultats: JSON.stringify(resultats) } }];
