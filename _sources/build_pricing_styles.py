#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère une page de comparaison présentant quatre mises en page possibles
pour la section « Nos abonnements ». Page autonome, hors du site livré.

Usage : python3 _sources/build_pricing_styles.py
"""

import os

PLANS = [
    dict(slug="bronze", nom="Bronze", base=39.99, duree="12 mois", bonus="", badge="", ton="neutre",
         chaines="25 000+", films="100 000+"),
    dict(slug="gold", nom="Gold", base=49.99, duree="15 mois", bonus="+3 mois offerts",
         badge="Le plus populaire", ton="bleu", chaines="25 000+", films="100 000+"),
    dict(slug="platinium", nom="Platinium", base=59.99, duree="15 mois", bonus="+3 mois offerts",
         badge="", ton="neutre", chaines="25 000+", films="100 000+"),
    dict(slug="exclusif", nom="Exclusif", base=84.99, duree="24 mois", bonus="+3 mois offerts",
         badge="Meilleur rapport", ton="vert", chaines="130 000+", films="140 000+"),
]

COMMUNES = [
    "Qualité 4K / FHD / HD",
    "Chaînes internationales",
    "Compatible avec de nombreux appareils",
    "Guide TV (EPG)",
    "Contenus à la demande (VOD)",
    "Serveurs surveillés en continu",
    "Support technique 24/7",
    "Livraison immédiate",
]


def euro(v):
    return ("%.2f" % v).replace(".", ",") + "\u00a0€"


CHECK = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5 9 17.5 20 6.5" fill="none" '
         'stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def stepper(slug, variante):
    return ('<div class="conn" data-plan="%s" data-base="%.2f" data-var="%s">'
            '<button type="button" data-step="-1" aria-label="Retirer une connexion">−</button>'
            '<span data-label>1 connexion</span>'
            '<button type="button" data-step="1" aria-label="Ajouter une connexion">+</button>'
            '</div>' % (slug, plan_base(slug), variante))


def plan_base(slug):
    return next(p["base"] for p in PLANS if p["slug"] == slug)


def badge(p):
    if not p["badge"]:
        return ""
    return '<span class="badge badge--%s">%s</span>' % (p["ton"], p["badge"])


def prix(p, variante):
    return ('<p class="prix"><b data-total="%s" data-var="%s">%s</b>'
            '<span>/ %s</span></p>' % (p["slug"], variante, euro(p["base"]), p["duree"]))


# ---------------------------------------------------------------- variante A
def variante_a():
    entetes = "".join(
        '<th class="%s">%s%s<span class="th-nom">Pack %s</span>'
        '<span class="th-duree">%s%s</span>'
        '<span class="th-prix" data-total="%s" data-var="a">%s</span>'
        '%s'
        '<a class="btn btn--%s" href="#">Choisir</a></th>'
        % ("col-vedette" if p["ton"] == "bleu" else "",
           badge(p), "" if p["badge"] else "",
           p["nom"], p["duree"].upper(),
           ' <em>%s</em>' % p["bonus"] if p["bonus"] else "",
           p["slug"], euro(p["base"]),
           stepper(p["slug"], "a"),
           p["ton"])
        for p in PLANS)

    def ligne(label, valeurs, fort=False):
        cells = "".join(
            '<td class="%s">%s</td>' % ("col-vedette" if PLANS[i]["ton"] == "bleu" else "", v)
            for i, v in enumerate(valeurs))
        return '<tr class="%s"><th scope="row">%s</th>%s</tr>' % ("ligne-forte" if fort else "", label, cells)

    lignes = [
        ligne("Durée", [p["duree"] for p in PLANS], True),
        ligne("Mois offerts", [p["bonus"].replace("+", "") if p["bonus"] else "—" for p in PLANS], True),
        ligne("Chaînes TV", [p["chaines"] for p in PLANS], True),
        ligne("Films et séries", [p["films"] for p in PLANS], True),
    ] + [ligne(f, [CHECK] * 4) for f in COMMUNES]

    return '''    <div class="tableau-wrap">
      <table class="tableau">
        <thead><tr><th scope="col" class="coin">Comparatif</th>%s</tr></thead>
        <tbody>%s</tbody>
      </table>
    </div>''' % (entetes, "".join(lignes))


# ---------------------------------------------------------------- variante B
def variante_b():
    cartes = "".join(
        '''<article class="carte-mini carte--%s">%s
          <h3>Pack %s</h3>
          <p class="duree">%s%s</p>
          %s
          %s
          <a class="btn btn--%s btn--block" href="#">Choisir %s</a>
        </article>''' % (
            p["ton"], badge(p), p["nom"], p["duree"],
            ' <em>%s</em>' % p["bonus"] if p["bonus"] else "",
            prix(p, "b"), stepper(p["slug"], "b"), p["ton"], p["nom"])
        for p in PLANS)

    communes = "".join('<li>%s %s</li>' % (CHECK, f) for f in
                       ["25 000+ chaînes TV", "100 000+ films et séries"] + COMMUNES)

    return '''    <div class="grille-mini">%s</div>
    <div class="bloc-commun">
      <h3>Inclus dans les quatre formules</h3>
      <ul class="liste-commune">%s</ul>
      <p class="note-commune">Le Pack Exclusif donne accès à un catalogue élargi : 130 000+ chaînes et 140 000+ films et séries.</p>
    </div>''' % (cartes, communes)


# ---------------------------------------------------------------- variante C
def variante_c():
    lignes = "".join(
        '''<article class="rangee rangee--%s">
          <div class="rangee-id">
            <h3>Pack %s</h3>
            <p>%s%s</p>
            %s
          </div>
          <ul class="rangee-points">
            <li>%s chaînes TV</li><li>%s films et séries</li><li>4K / FHD / HD</li><li>Support 24/7</li>
          </ul>
          <div class="rangee-action">
            %s
            %s
            <a class="btn btn--%s" href="#">Choisir</a>
          </div>
        </article>''' % (
            p["ton"], p["nom"], p["duree"],
            ' · <em>%s</em>' % p["bonus"] if p["bonus"] else "",
            badge(p), p["chaines"], p["films"],
            prix(p, "c"), stepper(p["slug"], "c"), p["ton"])
        for p in PLANS)
    return '    <div class="rangees">%s</div>' % lignes


# ---------------------------------------------------------------- variante D
def variante_d():
    onglets = "".join(
        '<button class="seg%s" type="button" data-seg="%s"%s>Pack %s<small>%s</small></button>'
        % (" is-on" if i == 1 else "", p["slug"], ' aria-pressed="true"' if i == 1 else ' aria-pressed="false"',
           p["nom"], p["duree"])
        for i, p in enumerate(PLANS))

    panneaux = "".join(
        '''<div class="panneau" data-pan="%s"%s>
          <div class="panneau-haut">
            <div>%s<h3>Pack %s</h3><p class="duree">%s%s</p></div>
            %s
          </div>
          %s
          <ul class="panneau-liste">%s</ul>
          <a class="btn btn--%s btn--block" href="#">Choisir le Pack %s</a>
        </div>''' % (
            p["slug"], "" if p["ton"] == "bleu" else " hidden",
            badge(p), p["nom"], p["duree"],
            ' <em>%s</em>' % p["bonus"] if p["bonus"] else "",
            prix(p, "d"), stepper(p["slug"], "d"),
            "".join('<li>%s %s</li>' % (CHECK, f) for f in
                    ["%s chaînes TV" % p["chaines"], "%s films et séries" % p["films"]] + COMMUNES),
            p["ton"], p["nom"])
        for p in PLANS)

    return '''    <div class="segmente" role="group" aria-label="Choisissez une formule">%s</div>
    <div class="panneaux">%s</div>''' % (onglets, panneaux)


VARIANTES = [
    ("A", "Tableau comparatif",
     "Une ligne par caractéristique. Le visiteur compare d’un coup d’œil et repère tout de suite ce qui change vraiment entre les formules. Le plus dense, idéal sur ordinateur.",
     variante_a()),
    ("B", "Cartes compactes + socle commun",
     "Les cartes ne portent que ce qui distingue les formules ; les dix caractéristiques identiques descendent dans un bloc unique. Divise la hauteur de la section par trois.",
     variante_b()),
    ("C", "Lignes horizontales",
     "Une formule par ligne pleine largeur. Lecture naturelle de haut en bas, très à l’aise sur mobile, et le prix reste toujours aligné à droite.",
     variante_c()),
    ("D", "Sélecteur + carte unique",
     "Un sélecteur segmenté en haut, une seule formule affichée à la fois. Zéro répétition, mise en avant maximale, mais oblige à cliquer pour comparer.",
     variante_d()),
]


CSS = """
:root{--bg:#070b16;--panel:#0d1730;--panel2:#101c3a;--line:rgba(140,172,228,.14);
--line2:rgba(140,172,228,.3);--text:#eef3fc;--muted:#94a4c6;--muted2:#7686a8;
--blue:#2f7dff;--blue2:#1a56d6;--cyan:#5fd9ff;--red:#e2504a;--green:#3ed598;
--fd:"Plus Jakarta Sans",ui-sans-serif,system-ui,sans-serif;
--fb:"Inter",ui-sans-serif,system-ui,sans-serif}
*,*::before,*::after{box-sizing:border-box}
html{overflow-x:clip}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--fb);line-height:1.6;
-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:var(--fd);font-weight:800;letter-spacing:-.022em;line-height:1.15;margin:0 0 .5em}
em{font-style:normal;color:var(--green);font-weight:700}

.intro{padding:54px 0 10px;border-bottom:1px solid var(--line)}
.intro h1{font-size:clamp(1.8rem,4vw,2.6rem)}
.intro p{color:var(--muted);max-width:70ch}

.bloc{padding:56px 0;border-bottom:1px solid var(--line)}
.bloc-tete{display:flex;align-items:flex-start;gap:16px;margin-bottom:32px}
.lettre{flex-shrink:0;width:46px;height:46px;display:grid;place-items:center;border-radius:13px;
font-family:var(--fd);font-weight:800;font-size:1.2rem;color:#04101f;
background:linear-gradient(135deg,var(--cyan),var(--blue))}
.bloc-tete h2{font-size:1.45rem;margin:0 0 .25em}
.bloc-tete p{margin:0;color:var(--muted);font-size:.95rem;max-width:80ch}

.badge{display:inline-block;font-family:var(--fd);font-size:.63rem;font-weight:800;letter-spacing:.1em;
text-transform:uppercase;padding:5px 11px;border-radius:999px;margin-bottom:10px}
.badge--bleu{background:linear-gradient(135deg,var(--cyan),var(--blue));color:#04101f}
.badge--vert{background:linear-gradient(135deg,var(--green),#22a877);color:#04241a}

.btn{display:inline-flex;align-items:center;justify-content:center;font-family:var(--fd);
font-size:.9rem;font-weight:700;padding:.8rem 1.3rem;border-radius:999px;border:1px solid transparent;
cursor:pointer;text-decoration:none;min-height:44px;transition:transform .18s,box-shadow .18s}
.btn:hover{transform:translateY(-2px)}
.btn--block{width:100%}
.btn--neutre{background:rgba(255,255,255,.04);border-color:var(--line2);color:var(--text)}
.btn--neutre:hover{background:rgba(255,255,255,.09);border-color:var(--cyan)}
.btn--bleu{background:linear-gradient(135deg,var(--blue),var(--blue2));color:#fff;
box-shadow:0 12px 28px -14px rgba(47,125,255,.9)}
.btn--vert{background:linear-gradient(135deg,var(--green),#1fa676);color:#042318;
box-shadow:0 12px 28px -14px rgba(62,213,152,.85)}

.conn{display:flex;align-items:center;gap:8px;padding:5px;border-radius:12px;border:1px solid var(--line);
background:rgba(255,255,255,.04)}
.conn button{width:32px;height:32px;flex-shrink:0;border-radius:9px;border:1px solid var(--line2);
background:rgba(47,125,255,.14);color:var(--text);font-size:1.05rem;font-weight:700;cursor:pointer}
.conn button:hover:not(:disabled){background:rgba(47,125,255,.32);border-color:var(--cyan)}
.conn button:disabled{opacity:.3;cursor:not-allowed}
.conn span{flex:1;text-align:center;font-family:var(--fd);font-weight:700;font-size:.82rem;
font-variant-numeric:tabular-nums}

.prix{display:flex;align-items:baseline;gap:.35rem;margin:0 0 14px;font-family:var(--fd);
font-variant-numeric:tabular-nums}
.prix b{font-size:1.95rem;font-weight:800;letter-spacing:-.03em}
.prix span{font-size:.85rem;color:var(--muted);font-weight:600}

svg{width:16px;height:16px;flex-shrink:0}

/* ---- A : tableau ---- */
.tableau-wrap{overflow-x:auto;border-radius:20px;border:1px solid var(--line);
background:linear-gradient(170deg,rgba(255,255,255,.04),rgba(255,255,255,.01))}
.tableau{width:100%;min-width:820px;border-collapse:collapse}
.tableau th,.tableau td{padding:13px 16px;text-align:center;border-bottom:1px solid var(--line);
font-size:.88rem}
.tableau thead th{vertical-align:top;padding:24px 16px;border-bottom:1px solid var(--line2)}
.tableau .coin{text-align:left;font-family:var(--fd);font-size:.72rem;letter-spacing:.15em;
text-transform:uppercase;color:var(--muted2);vertical-align:bottom}
.th-nom{display:block;font-family:var(--fd);font-size:1.05rem;font-weight:800}
.th-duree{display:block;font-size:.75rem;letter-spacing:.08em;color:var(--muted2);margin-bottom:12px}
.th-prix{display:block;font-family:var(--fd);font-size:1.6rem;font-weight:800;letter-spacing:-.03em;
font-variant-numeric:tabular-nums;margin-bottom:12px}
.tableau thead .conn{margin-bottom:12px}
.tableau tbody th{text-align:left;font-weight:500;color:var(--muted);font-family:var(--fb);font-size:.88rem}
.tableau td svg{color:var(--green)}
.ligne-forte td{font-family:var(--fd);font-weight:700;color:#fff}
.col-vedette{background:rgba(47,125,255,.09)}
.tableau tbody tr:last-child th,.tableau tbody tr:last-child td{border-bottom:none}

/* ---- B : cartes compactes ---- */
.grille-mini{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.carte-mini{display:flex;flex-direction:column;padding:24px 20px;border-radius:20px;
border:1px solid var(--line);background:linear-gradient(170deg,rgba(255,255,255,.05),rgba(255,255,255,.012))}
.carte--bleu{border-color:rgba(95,217,255,.5);background:linear-gradient(170deg,rgba(47,125,255,.16),rgba(10,17,34,.9))}
.carte--vert{border-color:rgba(62,213,152,.4)}
.carte-mini h3{font-size:1.1rem;margin:0 0 .15em}
.carte-mini .duree{margin:0 0 16px;font-size:.82rem;color:var(--muted)}
.carte-mini .conn{margin-bottom:18px}
.carte-mini .btn{margin-top:auto}
.bloc-commun{margin-top:22px;padding:26px 28px;border-radius:20px;border:1px solid var(--line);
background:rgba(47,125,255,.07)}
.bloc-commun h3{font-size:1rem;margin-bottom:1em}
.liste-commune{list-style:none;margin:0;padding:0;display:grid;
grid-template-columns:repeat(3,minmax(0,1fr));gap:10px 24px}
.liste-commune li{display:flex;align-items:center;gap:9px;font-size:.9rem;color:var(--muted)}
.liste-commune svg{color:var(--green)}
.note-commune{margin:18px 0 0;font-size:.86rem;color:var(--muted2)}

/* ---- C : lignes ---- */
.rangees{display:grid;gap:14px}
.rangee{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr) 260px;gap:24px;
align-items:center;padding:22px 26px;border-radius:18px;border:1px solid var(--line);
background:linear-gradient(120deg,rgba(255,255,255,.045),rgba(255,255,255,.012))}
.rangee--bleu{border-color:rgba(95,217,255,.5);background:linear-gradient(120deg,rgba(47,125,255,.16),rgba(10,17,34,.9))}
.rangee--vert{border-color:rgba(62,213,152,.4)}
.rangee-id h3{font-size:1.15rem;margin:0 0 .2em}
.rangee-id p{margin:0 0 10px;font-size:.85rem;color:var(--muted)}
.rangee-id .badge{margin:0}
.rangee-points{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:7px}
.rangee-points li{font-size:.76rem;color:var(--muted);padding:5px 11px;border-radius:999px;
border:1px solid var(--line);background:rgba(255,255,255,.03)}
.rangee-action{display:grid;gap:10px}
.rangee-action .prix{margin:0}

/* ---- D : sélecteur ---- */
.segmente{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;padding:8px;
border-radius:18px;border:1px solid var(--line);background:rgba(255,255,255,.035);margin-bottom:22px}
.seg{display:grid;gap:2px;padding:14px 10px;border-radius:12px;border:1px solid transparent;
background:transparent;color:var(--muted);font-family:var(--fd);font-weight:700;font-size:.92rem;
cursor:pointer;transition:background .16s,color .16s,border-color .16s}
.seg small{font-family:var(--fb);font-weight:500;font-size:.74rem;color:var(--muted2)}
.seg:hover{background:rgba(255,255,255,.05);color:#fff}
.seg.is-on{background:rgba(47,125,255,.18);border-color:rgba(95,217,255,.5);color:#fff}
.panneau{padding:30px;border-radius:22px;border:1px solid var(--line2);
background:linear-gradient(170deg,rgba(47,125,255,.12),rgba(10,17,34,.92))}
.panneau[hidden]{display:none}
.panneau-haut{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;flex-wrap:wrap}
.panneau-haut h3{font-size:1.5rem;margin:0 0 .15em}
.panneau-haut .duree{margin:0;color:var(--muted);font-size:.9rem}
.panneau-haut .prix b{font-size:2.4rem}
.panneau .conn{max-width:230px;margin-bottom:20px}
.panneau-liste{list-style:none;margin:0 0 22px;padding:0;display:grid;
grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 24px}
.panneau-liste li{display:flex;align-items:center;gap:9px;font-size:.9rem;color:var(--muted)}
.panneau-liste svg{color:var(--green)}
.panneau .btn{max-width:340px}

@media(max-width:980px){
  .grille-mini{grid-template-columns:repeat(2,minmax(0,1fr))}
  .liste-commune{grid-template-columns:repeat(2,minmax(0,1fr))}
  .rangee{grid-template-columns:minmax(0,1fr);gap:16px}
  .rangee-action{grid-template-columns:1fr auto;align-items:center}
  .rangee-action .btn{grid-column:2;grid-row:1/3}
  .segmente{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:640px){
  .grille-mini{grid-template-columns:minmax(0,1fr)}
  .liste-commune,.panneau-liste{grid-template-columns:minmax(0,1fr)}
  .rangee-action{grid-template-columns:minmax(0,1fr)}
  .rangee-action .btn{grid-column:1;grid-row:auto}
  .panneau{padding:22px}
}
"""

JS = """
(function(){
  var REMISE=0.15, MAX=5;
  function euro(v){return v.toFixed(2).replace(".",",")+"\\u00a0€";}
  function total(base,n){return base*(1+(1-REMISE)*(n-1));}

  Array.prototype.forEach.call(document.querySelectorAll(".conn"),function(c){
    var base=parseFloat(c.getAttribute("data-base"));
    var slug=c.getAttribute("data-plan"), v=c.getAttribute("data-var");
    var label=c.querySelector("[data-label]");
    var cible=document.querySelector('[data-total="'+slug+'"][data-var="'+v+'"]');
    var btns=c.querySelectorAll("[data-step]"), n=1;
    function draw(){
      label.textContent=n+(n>1?" connexions":" connexion");
      if(cible) cible.textContent=euro(total(base,n));
      Array.prototype.forEach.call(btns,function(b){
        var d=parseInt(b.getAttribute("data-step"),10);
        b.disabled=(d<0&&n===1)||(d>0&&n===MAX);
      });
    }
    Array.prototype.forEach.call(btns,function(b){
      b.addEventListener("click",function(){
        var next=n+parseInt(b.getAttribute("data-step"),10);
        if(next<1||next>MAX)return; n=next; draw();
      });
    });
    draw();
  });

  var segs=Array.prototype.slice.call(document.querySelectorAll("[data-seg]"));
  segs.forEach(function(s){
    s.addEventListener("click",function(){
      var slug=s.getAttribute("data-seg");
      segs.forEach(function(o){
        var on=o===s;
        o.classList.toggle("is-on",on);
        o.setAttribute("aria-pressed",on?"true":"false");
      });
      Array.prototype.forEach.call(document.querySelectorAll("[data-pan]"),function(p){
        p.hidden=p.getAttribute("data-pan")!==slug;
      });
    });
  });
})();
"""


def main():
    blocs = "".join('''  <section class="bloc">
    <div class="wrap">
      <div class="bloc-tete">
        <span class="lettre">%s</span>
        <div><h2>%s</h2><p>%s</p></div>
      </div>
%s
    </div>
  </section>
''' % (lettre, titre, desc, corps) for lettre, titre, desc, corps in VARIANTES)

    gabarit = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quatre mises en page pour la section Abonnements</title>
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap">
<style>__CSS__</style>
</head>
<body>
  <header class="intro">
    <div class="wrap">
      <h1>Quatre mises en page pour la section « Nos abonnements »</h1>
      <p>Mêmes prix, mêmes durées, mêmes caractéristiques que sur le site : seule la présentation change.
      Les sélecteurs de connexions sont actifs, le total se recalcule à −15 % par connexion supplémentaire.
      Répondez avec la lettre de celle que vous préférez.</p>
    </div>
  </header>
__BLOCS__
<script>__JS__</script>
</body>
</html>
'''
    html = (gabarit.replace("__CSS__", CSS).replace("__BLOCS__", blocs).replace("__JS__", JS))

    dest = "/mnt/user-data/outputs/styles-abonnements.html"
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("écrit : %s (%d octets)" % (dest, os.path.getsize(dest)))


if __name__ == "__main__":
    main()
