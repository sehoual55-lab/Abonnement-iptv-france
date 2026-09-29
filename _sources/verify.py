#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôles automatiques du site avant mise en ligne."""

import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.getcwd()
ERRORS = []
WARN = []
OK = []


def err(msg):
    ERRORS.append(msg)


def ok(msg):
    OK.append(msg)


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr", "path", "circle", "rect",
        "use", "stop", "line", "polygon", "ellipse"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = set()
        self.hrefs = []
        self.headings = []
        self.imbalance = []
        self.aria_controls = []
        self.buttons_without_label = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:
                err("id dupliqué : #%s" % a["id"])
            self.ids.add(a["id"])
        if a.get("href"):
            self.hrefs.append(a["href"])
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
        if a.get("aria-controls"):
            self.aria_controls.append(a["aria-controls"])
        if tag not in VOID and not self.get_starttag_text().endswith("/>"):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.imbalance.append("fermeture orpheline </%s>" % tag)
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        else:
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.imbalance.append("balise non fermée <%s>" % self.stack.pop())
                if self.stack:
                    self.stack.pop()
            else:
                self.imbalance.append("fermeture orpheline </%s>" % tag)


pages = sorted(glob.glob("index.html") + glob.glob("*/index.html"))
if len(pages) != 5:
    err("5 pages HTML attendues, %d trouvées" % len(pages))

all_ids = {}
for page in pages:
    html = open(page, encoding="utf-8").read()
    c = Checker()
    c.feed(html)
    all_ids[page] = c.ids

    for problem in c.imbalance:
        err("%s : %s" % (page, problem))

    # Langue
    if 'lang="fr"' not in html:
        err("%s : attribut lang français manquant" % page)

    # Titre / description / canonical
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    if not title:
        err("%s : <title> manquant" % page)
    desc = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
    if not desc:
        err("%s : meta description manquante" % page)
    elif not (110 <= len(desc.group(1)) <= 175):
        WARN.append("%s : meta description de %d caractères" % (page, len(desc.group(1))))
    if 'rel="canonical"' not in html:
        err("%s : canonical manquant" % page)
    if 'property="og:title"' not in html or 'name="twitter:card"' not in html:
        err("%s : métadonnées sociales incomplètes" % page)

    # Titres
    h1s = html.count("<h1")
    if h1s != 1:
        err("%s : %d balises h1 (1 attendue)" % (page, h1s))
    prev = 0
    for level in c.headings:
        if prev and level > prev + 1:
            err("%s : saut de niveau de titre h%d après h%d" % (page, level, prev))
        prev = level

    # aria-controls pointe vers un id réel
    for target in c.aria_controls:
        if target not in c.ids:
            err("%s : aria-controls=\"%s\" sans cible" % (page, target))

    # Liens internes
    for href in c.hrefs:
        if href.startswith("#"):
            anchor = href[1:]
            if anchor and anchor not in c.ids:
                err("%s : ancre interne cassée %s" % (page, href))
        elif href.startswith("/") and not href.startswith("//"):
            target = href.split("#")[0].split("?")[0]
            if target.endswith("/"):
                candidate = os.path.join(ROOT, target.strip("/"), "index.html")
            else:
                candidate = os.path.join(ROOT, target.lstrip("/"))
            if not os.path.exists(candidate):
                err("%s : lien interne cassé %s" % (page, href))

    # JSON-LD valide
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(block)
        except Exception as exc:
            err("%s : JSON-LD invalide (%s)" % (page, exc))

    # Pas de texte de remplissage
    for bad in ("lorem ipsum", "Lorem ipsum", "TODO", "placeholder text", "XXXX"):
        if bad in html:
            err("%s : texte de remplissage détecté (%s)" % (page, bad))

ok("%d pages analysées, structure HTML équilibrée" % len(pages))

# ---- Règles propres à la page d'accueil ----
home = open("index.html", encoding="utf-8").read()

for section in ["accueil", "avantages", "abonnements", "appareils", "installation", "faq", "contact"]:
    if 'id="%s"' % section not in home:
        err("section #%s absente" % section)
ok("les 7 sections de navigation existent")

# Prix et durées
expected = [
    ("Pack Bronze", "39,99", "12 mois", False),
    ("Pack Gold", "49,99", "15 mois", True),
    ("Pack Platinium", "59,99", "15 mois", True),
    ("Pack Exclusif", "84,99", "24 mois", True),
]
cards = re.findall(r'<article class="plan.*?</article>', home, re.S)
if len(cards) != 4:
    err("%d cartes tarifaires trouvées (4 attendues)" % len(cards))
else:
    for card, (name, price, duration, bonus) in zip(cards, expected):
        if name not in card:
            err("carte tarifaire : %s introuvable" % name)
        if price not in card:
            err("%s : prix %s absent" % (name, price))
        if duration not in card:
            err("%s : durée %s absente" % (name, duration))
        if ("+3 mois offerts" in card) != bonus:
            err("%s : mention « +3 mois offerts » incorrecte" % name)
        if 'data-conn-label>1 connexion' not in card:
            err("%s : sélecteur de connexions absent ou non initialisé à 1" % name)
        if 'data-base="%s"' % price.replace(",", ".") not in card:
            err("%s : data-base ne correspond pas au prix affiché" % name)
    ok("4 formules : prix, durées, connexions et bonus conformes")

if "+3 mois offerts" in cards[0]:
    err("Bronze affiche « +3 mois offerts »")
else:
    ok("Bronze n’affiche pas « +3 mois offerts »")

# Orthographe imposée
if "Platinium" not in home or "Platinum" in home:
    err("orthographe « Platinium » non respectée")
else:
    ok("orthographe « Platinium » respectée")

# Garanties interdites
for banned in ["zéro coupure", "100 % légal", "meilleur de France", "sans coupure garanti",
               "garantie 100", "stabilité absolue garantie"]:
    hits = [m.start() for m in re.finditer(re.escape(banned), home)]
    for pos in hits:
        context = home[max(0, pos - 260):pos]
        # autorisé uniquement dans l'encadré de mise en garde
        if "Méfiez-vous" not in context:
            err("promesse interdite employée comme argument : %s" % banned)
ok("aucune garantie absolue employée comme argument commercial")

# Boutons de commande
for label in ["Choisir Bronze", "Choisir Gold", "Choisir Platinium", "Choisir Exclusif"]:
    if label not in home:
        err("bouton « %s » manquant" % label)
if home.count('data-plan="Pack') != 4:
    err("les 4 boutons de formule ne portent pas tous data-plan")
if 'id="checkout"' not in home or 'data-checkout-form' not in home:
    err("la fenêtre de commande est absente")
for hook in ["data-checkout-close", "data-checkout-submit", "data-recap-plan",
             "data-recap-conn", "data-recap-total", "data-checkout-ask", 'name="paiement"']:
    if hook not in home:
        err("point d’ancrage manquant dans la fenêtre de commande : %s" % hook)
if "[À compléter]" in home or "À compléter" in home:
    err("un encadré « À compléter » subsiste sur la page d’accueil")
ok("fenêtre de commande présente et complète ; plus d’encadré « À compléter » en page d’accueil")

# FAQ : cohérence entre le visible et le JSON-LD
faq_ld = re.search(r'"@type": "FAQPage".*?\n</script>', home, re.S).group(0)
questions = re.findall(r'"name": "(.*?)"', faq_ld)
if len(questions) != 8:
    err("%d questions dans le JSON-LD FAQ (8 attendues)" % len(questions))
visible = re.findall(r"<summary><h3>(.*?)</h3></summary>", home)
if len(visible) != 8:
    err("%d questions visibles dans la FAQ (8 attendues)" % len(visible))
for q in questions:
    if q not in home.replace("&amp;", "&"):
        err("question du JSON-LD absente de la page : %s" % q)
ok("FAQ : 8 questions visibles, identiques au balisage FAQPage")

# Logos de marque fournis
brands = ["samsung", "lg", "sony", "amazon", "android", "apple",
          "appletv", "chromecast", "roku", "xbox", "windows", "linux"]
for b in brands:
    if 'id="b-%s"' % b not in home:
        err("logo manquant dans le sprite : %s" % b)
    if 'href="#b-%s"' % b not in home:
        err("logo non utilisé dans la section appareils : %s" % b)
ok("12 logos de marque fournis intégrés et utilisés")

# Cohérence du barème de connexions
js = open("assets/js/main.js", encoding="utf-8").read()
if "REMISE = 0.15" not in js:
    err("la remise par connexion supplémentaire n’est plus de 15 %")
if "MAX_CONN = 5" not in js:
    err("le maximum de connexions n’est plus de 5")
for txt in ["15 % moins ch", "jusqu’à cinq connexions"]:
    if txt not in home:
        err("règle de connexions non expliquée sur la page : %s" % txt)
ok("barème des connexions : 1 à 5, −15 % par connexion supplémentaire, expliqué sur la page")

# Aucune promesse absolue réintroduite par les listes de fonctionnalités
for banned in ["100 % stable", "Netflix", "Prime Video", "tous les appareils", "toutes les chaînes"]:
    for m in re.finditer(re.escape(banned), home):
        ctx = home[max(0, m.start() - 260):m.start()]
        if "Méfiez-vous" not in ctx:
            err("mention à revoir dans les fonctionnalités : %s" % banned)
ok("listes de fonctionnalités exemptes de promesses absolues et de services tiers")

# Widget WhatsApp présent sur toutes les pages
for page in pages:
    h = open(page, encoding="utf-8").read()
    for hook in ['data-wa-toggle', 'data-wa-link', 'id="i-whatsapp"']:
        if hook not in h:
            err("%s : élément manquant (%s)" % (page, hook))
    # Le logo est inliné deux fois avec des identifiants propres à chaque instance
    # (un dégradé référencé depuis un <use> n'est pas résolu par Safari).
    if h.count('class="logo-glyph"') != 2:
        err("%s : le logo doit être inliné deux fois (en-tête et pied de page)" % page)
    for ident in ["lgh-body", "lgh-socle", "lgf-body", "lgf-socle"]:
        if h.count('id="%s"' % ident) != 1:
            err("%s : identifiant de logo absent ou dupliqué (%s)" % (page, ident))
    if "#logo-mark" in h:
        err("%s : référence <use> vers le logo encore présente" % page)
ok("widget WhatsApp et logo inliné (identifiants uniques) sur les 5 pages")

# Aucun champ bancaire nulle part
for page in pages:
    h = open(page, encoding="utf-8").read().lower()
    # on n'inspecte que les vrais champs de saisie : <input>, <select>, <textarea>
    # (« Liban » contient « iban », la balise meta twitter:card contient « card »…)
    for tag in re.findall(r"<(?:input|select|textarea)\b[^>]*>", h):
        for motif in ["card", "cvv", "cvc", "iban", "expiry", "cc-num", "autocomplete=\"cc-"]:
            if motif in tag:
                err("%s : champ de paiement détecté (%s)" % (page, tag[:70]))
if "aucune donnée de carte" not in home.lower():
    err("la mention « aucune donnée de carte » est absente de la fenêtre de commande")
ok("aucun champ bancaire sur le site ; mention de sécurité présente")

# Indicatifs téléphoniques et modes de paiement
indicatifs = re.findall(r'<option value="(\+\d+)"', home)
if len(indicatifs) < 200:
    err("seulement %d indicatifs téléphoniques (liste mondiale attendue)" % len(indicatifs))
if 'value="+33" selected' not in home:
    err("l’indicatif France +33 n’est pas sélectionné par défaut")
paiements = re.findall(r'name="paiement" value="([^"]+)"', home)
if paiements != ["Carte bancaire"]:
    err("modes de paiement inattendus : %s" % paiements)
ok("%d indicatifs (France par défaut) ; paiement : Carte bancaire" % len(indicatifs))

# Guides d'installation par appareil
guides = re.findall(r'data-guide-panel="([a-z]+)"', home)
attendus = ["smarttv", "android", "ios", "desktop", "formuler", "mag"]
if guides != attendus:
    err("guides d’installation inattendus : %s" % guides)
opts = re.findall(r'data-guide-value="([a-z]+)"', home)
if opts != attendus:
    err("le sélecteur d’appareil ne correspond pas aux guides : %s" % opts)
if home.count('role="option"') != len(attendus) or 'role="listbox"' not in home:
    err("le sélecteur d’appareil n’expose pas un listbox accessible")
if home.count('aria-selected="true"') < 1:
    err("aucune option d’appareil marquée comme sélectionnée")
caches = len(re.findall(r'data-guide-panel="[a-z]+" hidden', home))
if caches != len(attendus) - 1:
    err("un seul guide doit être visible au chargement (%d masqués)" % caches)
ok("6 guides d’installation par appareil, sélecteur synchronisé")

# Contenu des messages sortants : ni lien vers le site, ni « IPTV »
main_js = open("assets/js/main.js", encoding="utf-8").read()
for interdit in ["Envoyé depuis", "Envoyée depuis", "cfg.domaine", "window.location.origin"]:
    if interdit in main_js:
        err("un message sortant contient encore une référence au site (%s)" % interdit)

# chaînes littérales injectées dans un message (sujets du widget + message par défaut)
sujets = re.findall(r'data-wa-topic="([^"]+)"', home)
sujets.append(re.search(r'var defaut = "([^"]+)"', main_js).group(1))
for sujet in sujets:
    if "IPTV" in sujet or "http" in sujet:
        err("message pré-rempli à corriger : %s" % sujet)
if len(sujets) != 5:
    err("%d messages pré-remplis trouvés (4 sujets + 1 défaut attendus)" % len(sujets))

# corps de la commande
for ligne in re.findall(r'"([^"\\]{4,})"', main_js[main_js.index("function buildMessage"):main_js.index("function showError")]):
    if "IPTV" in ligne or "http" in ligne:
        err("ligne de commande à corriger : %s" % ligne)
ok("messages sortants : aucun lien vers le site, aucune mention « IPTV »")

# Longueur du titre
t = re.search(r"<title>(.*?)</title>", home).group(1)
if len(t) > 62:
    WARN.append("titre de %d caractères (> 60)" % len(t))
else:
    ok("titre de %d caractères" % len(t))

# Équilibre du CSS (les media queries doivent être refermées)
css_txt = open("assets/css/style.css", encoding="utf-8").read()
depth = 0
for ch in css_txt:
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth < 0:
            break
if depth != 0:
    err("accolades CSS déséquilibrées (profondeur finale %d)" % depth)
else:
    ok("CSS équilibré : %d blocs ouverts et refermés" % css_txt.count("{"))

# Fichiers annexes
for f in ["robots.txt", "sitemap.xml", "vercel.json", "site.webmanifest",
          "assets/css/style.css", "assets/js/main.js", "assets/js/config.js",
          "assets/img/og-image.png", "assets/img/favicon.svg",
          "assets/img/apple-touch-icon.png", "assets/img/logo.png"]:
    if not os.path.exists(f):
        err("fichier manquant : %s" % f)
ok("fichiers de configuration et ressources présents")

# Aucune ressource externe hors polices
externals = set(re.findall(r'(?:src|href)="(https?://[^"]+)"', home))
allowed = ("https://fonts.googleapis.com", "https://fonts.gstatic.com",
           "https://abonnement-iptv-france.website", "https://schema.org",
           "https://openapi.vercel.sh")
for url in externals:
    if not url.startswith(allowed):
        err("ressource externe inattendue : %s" % url)
ok("aucune dépendance externe en dehors des polices Google")

# ---- Sortie ----
print("\n== CONTRÔLES RÉUSSIS ==")
for line in OK:
    print("  ✓", line)
if WARN:
    print("\n== AVERTISSEMENTS ==")
    for line in WARN:
        print("  !", line)
print("\n== ERREURS ==")
if ERRORS:
    for line in ERRORS:
        print("  ✗", line)
    sys.exit(1)
print("  aucune")
