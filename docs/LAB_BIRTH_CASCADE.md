# Lab Birth Cascade — checklist post-generation

> Quando il **meta-prototyper** genera un nuovo lab (o quando si converte un lab esistente),
> lo scaffold cognitivo (8 file: `mml.json` + `config.json` + `seed_tensions.json` +
> `tension_to_category.json` + `context.md` + `about.md` + `about.en.md` + `README.md` +
> `assertions.py` + `tools/exp_*.py`) è **solo l'inizio**. Per fare entrare il lab nel
> sistema visibilmente servono touch point distribuiti sulle superfici
> dichiarate dall'installazione: sito lab, sito principale, docs e memoria.
>
> Questo runbook è la cascade completa da seguire dopo `dnd init <lab>` (o equivalente).
> Cristallizzato dopo una cascade manuale di dominio e tradotto in regola
> riusabile.

## 0. Cosa è automatico (gratis, niente da fare)

Filesystem scan + dynamic API lo coprono al boot:

- `core.cli list` mostra il nuovo dominio
- `core.cli inspect --domain <lab>` lo valida
- `dnd-lab-describe.sh <lab>` produce report self-awareness
- `/api/domains` API endpoint lista include il dominio
- `/n/` master + `/n/<lab>/` index + `/n/<lab>/<ts>` narrative singole appaiono al primo cycle
- Movement registry (`narrative_writer`, `aeternitas`, `veritas_score`, ecc.) si applica universalmente se enabled in `config.json`

## 1. Validazione scaffold (subito, ~5 min)

Lab dir: `${DND_LAB_ROOT}/domains/<lab>/`

- [ ] **M1-M6 validator**: `python3 ${DND_LAB_ROOT}/domains/_meta-prototyper/tools/lab_template_validator.py ${DND_LAB_ROOT}/domains/<lab>/` → atteso `TEMPLATE_VALID 6/6 PASS`
- [ ] **Assertions standalone**: `cd ${DND_LAB_ROOT} && .venv/bin/python3 domains/<lab>/assertions.py` → atteso N/N PASS
- [ ] **Tools custom standalone**: `cd ${DND_LAB_ROOT} && .venv/bin/python3 domains/<lab>/tools/exp_*.py --json` per ogni tool dichiarato in `mml.json:tools_custom`
- [ ] **Inspect movements**: `core.cli inspect --domain <lab>` → vedi quali movement sono enabled
- [ ] **Identifica gap structurale**: il lab ha `narrative_writer` enabled in `config.json`? Se no, aggiungi (oggi è universal expected)

Se uno di questi step fallisce, **STOP**: il lab non è pronto per la cascade. Fix scaffold prima di propagare.

## 2. Integrazione lab.d-nd.com (TM3 lane, ~1-2h)

Tutto in `/opt/lab-d-nd-site/` — repo statico, modifiche dirette + IT/EN parità.

### 2.1 Landing `index.html`

- [ ] **Hero lead** (`hero.lead`): se elenca i lab attivi per nome, aggiungi/cita il nuovo
- [ ] **"Lab attivi" widget** (`hero.console.title`): se cita lab specifici, aggiorna
- [ ] **"Sei campi di applicazione" cards** (sezione `#templates`):
  - Aggiungi nuova `<article class="template-card" data-domain="<lab>">` con chip + h3 + description + meta chips (3 keyword tag)
  - Se lab è "live" usa chip emerald con CTA `<a href="/n/<lab>/">Vedi cycle live →</a>`
  - Se lab è "template" usa chip default senza CTA cycle
  - Aggiorna count titolo ("Sei campi" → "Sette campi" se aggiungi senza rimuovere) o lascia "Sei campi" se rimpiazzi un placeholder
- [ ] **Section lead `templates.lead`**: aggiorna se cita lab live per nome (es. "Finance e bio-rhythms sono lab vivi" → aggiungi <lab>)

### 2.2 `d-nd-lab.html`

- [ ] **"Demo del lab che pensa" card** (sezione `#dashboard`): se cita lab live per nome, aggiorna (`dndlab.dash.card1.p`)
- [ ] **CTA Cycle narrati**: se la card ha `cta2` verso `/n/`, va bene (è universale)
- [ ] **Architecture / movements**: se la nuova entità (es. nuovo movement custom del lab) cambia la pipeline pubblicizzata, riflettere

### 2.3 `assets/js/translations.js`

Per ogni nuova chiave HTML aggiunta sopra:

- [ ] **IT** version: chiave aggiunta nel blocco IT
- [ ] **EN** version: chiave aggiunta nel blocco EN (parità obbligatoria)

Pattern naming chiavi:
```
templates.card.<lab>.h3   = "<Lab Name>"
templates.card.<lab>.chip = "live" | "template" | "master"
templates.card.<lab>.p    = description
templates.card.<lab>.cycles = "Cycle reali su <data source>."   # solo se live
templates.card.<lab>.cta  = "Vedi cycle live →" | "See live cycles →"
```

### 2.4 `scoperte.html` + `applications.html`

Generalmente **niente da fare** — quelle pagine caricano dinamicamente da `data/` (publishing pipeline). Sono già linkate al flow SSP.

Se il lab produrrà finding promovibili, la pipeline auto-sync (backlog tecnica) li popolerà a tempo debito.

### 2.5 SEO + meta tags

- [ ] **Sitemap.xml**: aggiungi `https://lab.d-nd.com/n/<lab>/` come URL nuovo (se sitemap statica esiste)
- [ ] **OG image dedicata**: opzionale, default è il logo 90px (ok per ora)
- [ ] **robots.txt**: nessun cambio necessario

## 3. Integrazione d-nd.com (TM1 lane, copy/contenuto)

**Vincolo critico**: copy d-nd.com via Siteman CMS API, NON da repo direct (vedi `feedback_protocollo_content_cms_authority.md`).

TM3 NON tocca questi. Manda **brief a TM1 via Sinapsi** con quel che serve:

- [ ] **Concepts KB** (`/opt/THIA/data/concepts_kb.json`): se il lab introduce concetti propri (es. `regime_bio_cardiaco` per bio-rhythms, `regime_volatilità` per finance), TM1 aggiunge entry con `definition_it` + `definition_en`
- [ ] **Pagina dominio-specifica** (es. `/finance` o `/bio-rhythms` su d-nd.com): se il funnel marketing prevede landing dedicata, TM1 la prepara (Siteman CMS)
- [ ] **Manifesto / narrazione**: se il nuovo lab cambia la storia che il sito principale racconta (es. "ora abbiamo 5 lab attivi"), TM1 aggiorna
- [ ] **llms.txt / llms-full.txt** (`/opt/d-nd_com/public/`): TM1 aggiorna LLM-readable summary se il dominio è significativo

Sinapsi brief format consigliato:
```
[message] TM3 → TM1: nuovo lab <lab> integrato lato sandbox.

Cosa serve a livello copy d-nd.com:
- concepts_kb: <elenco concetti nuovi se applicabile>
- pagina dedicata: <yes/no, brief se yes>
- manifesto: <bozza modifica suggerita>
- llms.txt: <riga suggerita per il summary>

Vincolo: copy via Siteman CMS API, non repo direct.
```

## 4. Docs cascade

- [ ] **`d-nd-seed/docs/LAB_PATTERN.md`**: case study o esempio se il nuovo lab dimostra un pattern interessante (auto-falsifica, integra dati live, ecc.). Non obbligatorio.
- [ ] **`${DND_LAB_ROOT}/README.md`**: aggiornamento elenco domini supportati
- [ ] **`${DND_LAB_ROOT}/docs/INSTALL_PROCEDURE.md`**: aggiornamento esempi se il lab ha pattern installazione speciale
- [ ] **`/opt/d-nd-seed/README.md`**: solo se il lab introduce features radicalmente nuove (raro)

## 5. Memory crystallization

- [ ] **`cristallo_<lab>_born_<YYYY-MM-DD>.md`** in `/root/.claude/projects/-opt/memory/`: nascita del lab, atto di generazione (chi/quando/come), template_valid 6/6, primo cycle (se già fatto), eventuali sorprese
- [ ] **`MEMORY.md` index**: voce nuova con descrizione 150-200 char
- [ ] **Aggiornamento crystal pre-esistenti che citano "5 lab"**: se aggiungi il 6° lab, gli elenchi vanno aggiornati

## 6. Comunicazioni

- [ ] **Telegram notify operatore**: messaggio breve "lab <lab> generato + integrato lab.d-nd.com + brief inviato a TM1 per copy d-nd.com"
- [ ] **Sinapsi message TM1** (vedi sez. 3): copy brief
- [ ] **(Opzionale) LinkedIn announcement**: solo dopo che TM1 ha integrato copy d-nd.com e il lab ha almeno 1 cycle live narrato. Non immediato.

## 7. Primo cycle + verifica end-to-end

Dopo l'integrazione (sez. 1-6), lancia un cycle reale:

- [ ] **Cycle 1**: `cd ${DND_LAB_ROOT} && .venv/bin/python3 -m core.cli run --domain <lab>` (o via scheduler se notturno)
- [ ] **Verifica narrative**: file `data/<lab>/narratives/narrative_<ts>.md` esiste, frontmatter completo, 200 parole circa
- [ ] **Verifica pagina pubblica**: `https://lab.d-nd.com/n/<lab>/<ts>` rendering HTML pulito
- [ ] **Verifica Aeternitas**: `data/<lab>/aeternitas/aeternitas_<ts>.json` ha `decision` settato
- [ ] **Verifica Veritas**: `data/<lab>/veritas/veritas_<ts>_*.json` ha `rho` calcolato
- [ ] **Verifica trajectory_log**: `data/<lab>/trajectory_log.jsonl` ha entry nuova

Se uno di questi è vuoto/missing, debug il movement specifico prima di considerare il lab integrato.

## 8. Checklist riassuntiva (TLDR)

```
Phase 1 — Validazione scaffold (5 min)
  □ M1-M6 PASS  □ Assertions PASS  □ Tools standalone OK

Phase 2 — lab.d-nd.com (TM3, 1-2h)
  □ index.html: hero + lab attivi widget + Sei campi card
  □ d-nd-lab.html: card + CTA cycle narrati
  □ translations.js: IT + EN parità
  □ Sitemap (opzionale)

Phase 3 — d-nd.com (TM1, copy via Siteman CMS)
  □ Sinapsi brief inviato

Phase 4 — Docs cascade
  □ README del lab root se elenco domini cambia

Phase 5 — Memory
  □ cristallo_<lab>_born + MEMORY.md index

Phase 6 — Comunicazioni
  □ Telegram operatore
  □ Sinapsi TM1

Phase 7 — End-to-end
  □ Primo cycle  □ Narrative pubblica  □ Aeternitas+Veritas+Trajectory log
```

## Anti-patterns

- **Generare il lab e dimenticare la cascade**: il lab esiste filesystem ma è invisibile a chi guarda il sito. Brutta UX, lavoro sprecato.
- **Aggiornare solo IT senza EN** (o viceversa): rompe parità lingua su lab.d-nd.com — visitatore EN vede testo IT mismatched.
- **Toccare copy d-nd.com da repo direct**: viola `feedback_protocollo_content_cms_authority.md`. d-nd.com ha CMS dedicato (Siteman API).
- **Saltare Phase 1**: se M1-M6 non passa, tutta la cascade poggia su scaffold rotto. Fix prima.
- **LinkedIn senza cycle reale**: hyped announcement prima del primo cycle live = brutta narrativa. Cycle reale prima, comunicazione dopo.

## Tempo totale realistico

- Fase 1 (validazione): 5-10 min
- Fase 2 (lab.d-nd.com): 1-2h
- Fase 3 (Sinapsi brief TM1): 15 min (poi TM1 lavora in parallelo, settimane suo timing)
- Fase 4 (docs): 15-30 min
- Fase 5 (memory): 15 min
- Fase 6 (comunicazioni): 5 min
- Fase 7 (cycle + verify): 10-15 min cycle execution + 5 min verify

**Totale TM3 lane**: ~2-3h dopo lo scaffold. Da pianificare quando si genera un lab nuovo, non un'aggiunta dopo.

## Versioning di questo runbook

| Versione | Data | Cambia |
|----------|------|--------|
| 1.0.0 | 2026-05-06 | Cristallizzazione iniziale dopo conversione di dominio |

Future evoluzioni: quando il prossimo lab nasce, aggiungere note "cosa è cambiato vs questa lista". Se la cascade diventa più meccanica → considerare automazione (script post-generation che fa Phase 2 stub + Phase 5+6 auto).
