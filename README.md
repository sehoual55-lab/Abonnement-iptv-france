# Abonnement IPTV France

Site vitrine français pour `https://abonnement-iptv-france.website`, déployé sur Vercel.

## Stack

HTML / CSS / JavaScript statiques, sans framework, sans build step et sans dépendance npm.
Ce choix vise les Core Web Vitals : aucun bundle à hydrater, une seule feuille de style,
environ 5 Ko de JavaScript non bloquant, aucune bibliothèque d'animation.

Seule ressource externe : les polices Inter et Plus Jakarta Sans, chargées de façon
non bloquante depuis Google Fonts (repli sur `system-ui` pendant le chargement).
Toutes les icônes sont des SVG originaux regroupés dans un sprite en ligne.

## Arborescence

```
/
├── index.html                          page d'accueil (toutes les sections)
├── conditions-utilisation/index.html
├── politique-confidentialite/index.html
├── politique-remboursement/index.html
├── mentions-legales/index.html
├── assets/
│   ├── css/style.css                   feuille de style unique
│   ├── js/config.js                    ← LE SEUL FICHIER À MODIFIER
│   ├── js/main.js                      menu, connexions, fenêtre de commande
│   └── img/                            og-image, logo, favicon, icône iOS
├── _sources/                           scripts de génération (non publiés)
│   ├── orders-apps-script.gs           backend Google Sheets des commandes
│   ├── build_pages.py                  régénère les 4 pages légales
│   ├── build_images.py                 régénère les images de marque
│   └── verify.py                       contrôles avant mise en ligne
├── robots.txt
├── sitemap.xml
├── site.webmanifest
└── vercel.json                         URLs propres, en-têtes, cache
```

## À faire avant la mise en ligne

1. **Moyens de contact — bloquant.** Ouvrir `assets/js/config.js` et renseigner au moins
   un champ parmi `whatsapp`, `email` ou `telegram`. Le premier canal renseigné, dans cet
   ordre, reçoit les commandes. Tant que les trois sont vides, le bouton « Envoyer ma
   commande » de la fenêtre de commande est désactivé et affiche « Commande momentanément
   indisponible » ; un avertissement est écrit dans la console du navigateur. Aucun numéro
   ni aucune adresse n'a été inventé.
   Le champ facultatif `endpoint` permet d'envoyer en plus une copie de chaque commande
   vers un backend (Google Apps Script, Formspree…).

2. **Mentions légales** — remplacer les blocs `[À compléter]` dans
   `mentions-legales/index.html`, `politique-confidentialite/index.html` et
   `politique-remboursement/index.html` (éditeur, statut, adresse, SIRET, TVA,
   adresse de contact, médiateur de la consommation, adresse de l'hébergeur).
   Ces champs sont obligatoires au titre de la LCEN et du Code de la consommation.

3. **Feuille des commandes** — déployer `_sources/orders-apps-script.gs` depuis la feuille
   Google « Abonnement iptv france - Commandes » (Extensions → Apps Script), puis coller
   l'URL en `/exec` dans `contact.endpoint`. Chaque commande crée alors une ligne dans la
   feuille et déclenche un e-mail. Les colonnes attendues sont déjà en place :
   Date · Nom · Email · Téléphone · Formule · Prix (€) · Connexions · Paiement · Statut.
   Sans endpoint, tout continue de fonctionner par WhatsApp.

4. **Search Console** — soumettre `https://abonnement-iptv-france.website/sitemap.xml`.

## Modifier le contenu

- **Barème des connexions** : `MAX_CONN` et `REMISE` en haut de `assets/js/main.js`
  (actuellement 5 connexions maximum, −15 % par connexion supplémentaire). Toute
  modification doit être reportée dans le texte de la page, la FAQ et les conditions
  d'utilisation, puis validée par `verify.py`.
- **Prix et durées** : ils figurent en clair dans `index.html`, section `#abonnements`
  (quatre blocs `<article class="plan">`), ainsi que dans la FAQ, dans le balisage
  FAQPage et dans `conditions-utilisation/index.html`. Toute modification doit être
  reportée dans ces quatre endroits, puis validée par `verify.py`.
- **Pages légales** : modifier `_sources/build_pages.py`, puis relancer le script.
- **Images de marque** : modifier `_sources/build_images.py`, puis relancer le script.

## Commandes

```bash
# Prévisualisation locale
python3 -m http.server 8000

# Contrôles (liens, ancres, titres, prix, FAQ, SEO, ressources)
python3 _sources/verify.py

# Régénération des pages légales et des images
python3 _sources/build_pages.py
python3 _sources/build_images.py
```

## Déploiement Vercel

Le dépôt se déploie tel quel : aucune commande de build, répertoire de sortie `.`.
`vercel.json` active les URLs propres avec barre oblique finale, les en-têtes de
sécurité et un cache d'un an sur `/assets/` (`config.js` reste à cache court pour
que les changements de contact soient pris en compte rapidement).
