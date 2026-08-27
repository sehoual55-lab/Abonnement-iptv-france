#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère les pages légales d'Abonnement IPTV France à partir d'un gabarit unique.
Usage :  python3 _sources/build_pages.py      (à lancer depuis la racine du site)
"""

import os

DOMAIN = "https://abonnement-iptv-france.website"
MAJ = "27 août 2026"

SHELL = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{domain}/{slug}/">
<meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#070b16">
<meta property="og:type" content="article">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Abonnement IPTV France">
<meta property="og:url" content="{domain}/{slug}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{domain}/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{domain}/assets/img/og-image.png">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap"></noscript>
<link rel="stylesheet" href="/assets/css/style.css">\n<script>document.documentElement.classList.add("js");</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Accueil", "item": "{domain}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "{h1}", "item": "{domain}/{slug}/" }}
  ]
}}
</script>
</head>
<body>
<a class="skip-link" href="#contenu">Aller au contenu principal</a>

<header class="header">
  <div class="container header-inner">
    <a class="logo" href="/" aria-label="Abonnement IPTV France — retour à l’accueil">
      <span class="logo-mark" aria-hidden="true"><svg class="logo-glyph" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="lgh-body" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f7dff"/><stop offset=".55" stop-color="#1a56d6"/><stop offset="1" stop-color="#0b2258"/></linearGradient><clipPath id="lgh-socle"><rect x="14" y="38.5" width="20" height="5" rx="2.5"/></clipPath></defs><rect x="3" y="6" width="42" height="29" rx="6.5" fill="url(#lgh-body)"/><path d="M19.5 14.5 33 21.5 19.5 28.5z" fill="#f4f7ff"/><rect x="22.4" y="35" width="3.2" height="4" fill="#1a56d6"/><g clip-path="url(#lgh-socle)"><rect x="14" y="38.5" width="6.7" height="5" fill="#2f7dff"/><rect x="20.7" y="38.5" width="6.7" height="5" fill="#f4f7ff"/><rect x="27.4" y="38.5" width="6.6" height="5" fill="#e2504a"/></g></svg></span>
        <span class="logo-text">
          <small>Abonnement</small>
          <b>IPTV France</b>
        </span>
    </a>

    <button class="burger" type="button" data-burger aria-expanded="false" aria-controls="navigation-principale" aria-label="Ouvrir le menu de navigation">
      <span class="burger-bars" aria-hidden="true"><i></i><i></i><i></i></span>
    </button>

    <nav class="nav" id="navigation-principale" aria-label="Navigation principale">
      <ul class="nav-list">
        <li><a href="/">Accueil</a></li>
        <li><a href="/#avantages">Avantages</a></li>
        <li><a href="/#abonnements">Abonnements</a></li>
        <li><a href="/#appareils">Appareils</a></li>
        <li><a href="/#installation">Installation</a></li>
        <li><a href="/#faq">FAQ</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
      <div class="nav-cta"><a class="btn btn--primary" href="/#abonnements">Voir les abonnements</a></div>
    </nav>

    <div class="header-cta"><a class="btn btn--primary btn--sm" href="/#abonnements">Voir les abonnements</a></div>
  </div>
</header>

<main id="contenu">
  <section class="page-hero">
    <div class="container">
      <nav aria-label="Fil d’Ariane">
        <ol class="breadcrumb">
          <li><a href="/">Accueil</a></li>
          <li>{h1}</li>
        </ol>
      </nav>
      <h1>{h1}</h1>
      <p>{intro}</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p class="update-date">Dernière mise à jour : {maj}</p>
      <div class="prose">
{body}
      </div>
    </div>
  </section>
</main>

<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true" focusable="false">
  <defs>
    <g id="i-whatsapp"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.174.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884a9.82 9.82 0 0 1 6.988 2.896 9.83 9.83 0 0 1 2.893 6.994c-.003 5.45-4.437 9.885-9.885 9.885M20.52 3.449C18.24 1.245 15.24 0 12.045 0 5.463 0 .104 5.36.101 11.945c0 2.096.549 4.14 1.595 5.945L0 24l6.335-1.652a11.9 11.9 0 0 0 5.71 1.454h.006c6.585 0 11.946-5.36 11.949-11.945a11.9 11.9 0 0 0-3.480-8.408"/></g>
  </defs>
</svg>

<!-- ============ WIDGET WHATSAPP ============ -->
<div class="wa" data-wa hidden>
  <div class="wa-panel" id="wa-panel" data-wa-panel role="dialog" aria-modal="false" aria-labelledby="wa-panel-title" hidden>
    <div class="wa-head">
      <span class="wa-avatar" aria-hidden="true">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><use href="#i-whatsapp"/></svg>
      </span>
      <span class="wa-head-text">
        <b id="wa-panel-title">Assistance IPTV France</b>
        <small>Réponse par WhatsApp</small>
      </span>
      <button class="wa-close" type="button" data-wa-close aria-label="Fermer la discussion WhatsApp">
        <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5.5 5.5 18.5 18.5M18.5 5.5 5.5 18.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>

    <div class="wa-body">
      <p class="wa-bubble">Bonjour&nbsp;! Dites-nous ce dont vous avez besoin et nous vous répondons sur WhatsApp.</p>
      <p class="wa-label">Sujets fréquents</p>
      <div class="wa-chips">
        <button class="wa-chip" type="button" data-wa-topic="Bonjour, j’aimerais un conseil pour choisir entre les formules Bronze, Gold, Platinium et Exclusif.">Choisir une formule</button>
        <button class="wa-chip" type="button" data-wa-topic="Bonjour, mon appareil est compatible avec votre service ?">Compatibilité de mon appareil</button>
        <button class="wa-chip" type="button" data-wa-topic="Bonjour, j’ai besoin d’aide pour installer et configurer mon application de lecture.">Aide à l’installation</button>
        <button class="wa-chip" type="button" data-wa-topic="Bonjour, je souhaite ajouter des connexions supplémentaires à mon abonnement.">Connexions supplémentaires</button>
      </div>
    </div>

    <div class="wa-foot">
      <a class="btn btn--wa btn--block" href="#" data-wa-link target="_blank" rel="noopener">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-whatsapp"/></svg>
        Démarrer la discussion
      </a>
      <p class="wa-note">Vous serez redirigé vers WhatsApp. Aucune donnée bancaire n’est demandée.</p>
    </div>
  </div>

  <button class="wa-fab" type="button" data-wa-toggle aria-expanded="false" aria-controls="wa-panel" aria-label="Ouvrir la discussion WhatsApp">
    <svg class="wa-fab-icon" width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-whatsapp"/></svg>
    <svg class="wa-fab-x" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5.5 5.5 18.5 18.5M18.5 5.5 5.5 18.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
    </svg>
    <span class="wa-fab-dot" aria-hidden="true"></span>
  </button>
</div>

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="logo" href="/">
          <span class="logo-mark" aria-hidden="true"><svg class="logo-glyph" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="lgf-body" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f7dff"/><stop offset=".55" stop-color="#1a56d6"/><stop offset="1" stop-color="#0b2258"/></linearGradient><clipPath id="lgf-socle"><rect x="14" y="38.5" width="20" height="5" rx="2.5"/></clipPath></defs><rect x="3" y="6" width="42" height="29" rx="6.5" fill="url(#lgf-body)"/><path d="M19.5 14.5 33 21.5 19.5 28.5z" fill="#f4f7ff"/><rect x="22.4" y="35" width="3.2" height="4" fill="#1a56d6"/><g clip-path="url(#lgf-socle)"><rect x="14" y="38.5" width="6.7" height="5" fill="#2f7dff"/><rect x="20.7" y="38.5" width="6.7" height="5" fill="#f4f7ff"/><rect x="27.4" y="38.5" width="6.6" height="5" fill="#e2504a"/></g></svg></span>
        <span class="logo-text">
          <small>Abonnement</small>
          <b>IPTV France</b>
        </span>
        </a>
        <p>Comparez nos formules et consultez nos informations pour choisir un abonnement adapté à vos appareils et à votre utilisation.</p>
      </div>
      <nav aria-labelledby="footer-nav-titre">
        <h3 id="footer-nav-titre">Navigation</h3>
        <ul>
          <li><a href="/">Accueil</a></li>
          <li><a href="/#avantages">Avantages</a></li>
          <li><a href="/#abonnements">Abonnements</a></li>
          <li><a href="/#appareils">Appareils</a></li>
          <li><a href="/#installation">Installation</a></li>
          <li><a href="/#faq">FAQ</a></li>
          <li><a href="/#contact">Contact</a></li>
        </ul>
      </nav>
      <nav aria-labelledby="footer-legal-titre">
        <h3 id="footer-legal-titre">Informations légales</h3>
        <ul>
          <li><a href="/conditions-utilisation/">Conditions d’utilisation</a></li>
          <li><a href="/politique-confidentialite/">Politique de confidentialité</a></li>
          <li><a href="/politique-remboursement/">Politique de remboursement</a></li>
          <li><a href="/mentions-legales/">Mentions légales</a></li>
        </ul>
      </nav>
    </div>
    <div class="footer-bottom">
      <p>© 2026 Abonnement IPTV France. Tous droits réservés.</p>
      <p>Les marques et noms d’appareils cités appartiennent à leurs propriétaires respectifs et sont mentionnés à titre informatif.</p>
    </div>
  </div>
</footer>

<script src="/assets/js/config.js"></script>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""

TODO = '<span class="todo">[À compléter]</span>'

PAGES = [
    {
        "slug": "conditions-utilisation",
        "title": "Conditions d’utilisation | Abonnement IPTV France",
        "h1": "Conditions d’utilisation",
        "description": "Conditions d’utilisation du site Abonnement IPTV France : objet, commandes, durée des formules, obligations de l’utilisateur et responsabilités.",
        "intro": "Les présentes conditions encadrent l’utilisation du site et la commande des formules qui y sont présentées.",
        "body": """
<h2>1. Objet</h2>
<p>Les présentes conditions d’utilisation définissent les règles applicables à la consultation du site Abonnement IPTV France et à la commande des formules présentées sur la page d’accueil. En naviguant sur ce site ou en passant commande, l’utilisateur reconnaît en avoir pris connaissance et les accepter.</p>

<h2>2. Description des formules</h2>
<p>Le site présente quatre formules d’abonnement, dont les caractéristiques sont indiquées de façon transparente dans la section « Nos abonnements » :</p>
<ul>
  <li>Pack Bronze — 39,99 € — 12 mois — 1 connexion</li>
  <li>Pack Gold — 49,99 € — 15 mois — 1 connexion — +3 mois offerts</li>
  <li>Pack Platinium — 59,99 € — 15 mois — 1 connexion — +3 mois offerts</li>
  <li>Pack Exclusif — 84,99 € — 24 mois — 1 connexion — +3 mois offerts</li>
</ul>
<p>Les prix ci-dessus s’entendent pour une connexion et pour la durée totale indiquée. Une connexion correspond à un seul flux utilisé simultanément : l’utilisation de plusieurs appareils en même temps sur une même connexion peut entraîner l’interruption de la lecture en cours.</p>
<p>Jusqu’à cinq connexions peuvent être commandées pour une même formule. La première connexion est facturée au prix normal et chaque connexion supplémentaire bénéficie d’une remise de 15 % sur ce prix. Le montant total est recalculé et affiché sur la carte de la formule avant la commande.</p>

<h2>3. Commande</h2>
<p>La commande s’effectue en sélectionnant une formule puis en contactant le vendeur par le moyen indiqué dans la section Contact. Les informations de configuration sont transmises après confirmation de la commande. Aucune donnée bancaire n’est collectée directement sur ce site.</p>

<h2>4. Application de lecture</h2>
<p>L’application utilisée pour lire un flux et l’abonnement lui-même constituent deux services distincts. Certaines applications sont gratuites, d’autres peuvent demander un achat ou des frais d’activation qui ne sont pas inclus dans le prix affiché sur ce site.</p>

<h2>5. Prérequis techniques</h2>
<p>Le service nécessite une connexion Internet fonctionnelle et un appareil compatible disposant d’une application de lecture. La disponibilité des applications dépend du modèle, du système d’exploitation, du pays et de la boutique d’applications de l’appareil. Les débits mentionnés sur le site constituent des recommandations générales et non des garanties de performance.</p>

<h2>6. Obligations de l’utilisateur</h2>
<p>L’utilisateur s’engage à :</p>
<ul>
  <li>fournir des informations exactes lors de sa commande ;</li>
  <li>utiliser le service dans le respect de la législation française et européenne applicable ;</li>
  <li>respecter les droits de propriété intellectuelle et les droits de diffusion des ayants droit ;</li>
  <li>ne pas partager, revendre ou rediffuser ses informations de connexion ;</li>
  <li>ne pas tenter de contourner une mesure technique de protection ou de restriction d’accès.</li>
</ul>
<p>Tout manquement peut entraîner la suspension de l’accès, sans que cela ouvre droit à un remboursement.</p>

<h2>7. Cadre légal</h2>
<p>La technologie IPTV est en elle-même licite. En revanche, la diffusion ou l’utilisation de contenus protégés sans l’autorisation des ayants droit peut constituer une infraction. La légalité d’un service dépend du fournisseur, des licences détenues, des contenus proposés et de l’usage qui en est fait. Il appartient à l’utilisateur de s’assurer que son utilisation respecte la législation applicable dans son pays de résidence.</p>

<h2>8. Disponibilité et limites de responsabilité</h2>
<p>Le service peut être temporairement interrompu pour des raisons de maintenance, de mise à jour ou pour des causes extérieures : panne du fournisseur d’accès à Internet, défaillance de l’équipement de l’utilisateur, saturation du réseau ou événement de force majeure. Aucune garantie de disponibilité permanente, de stabilité absolue ou de qualité 4K continue sur l’ensemble des contenus n’est formulée.</p>
<p>La responsabilité ne saurait être engagée pour les dommages indirects résultant de l’utilisation ou de l’impossibilité d’utiliser le service.</p>

<h2>9. Propriété intellectuelle</h2>
<p>La structure du site, ses textes, sa charte graphique et ses éléments visuels originaux sont protégés. Toute reproduction sans autorisation est interdite. Les marques et noms d’appareils cités sur le site appartiennent à leurs propriétaires respectifs et sont mentionnés uniquement à titre informatif, à des fins de compatibilité.</p>

<h2>10. Modification des conditions</h2>
<p>Ces conditions peuvent être modifiées à tout moment. La version applicable est celle publiée sur cette page à la date de la commande.</p>

<h2>11. Droit applicable</h2>
<p>Les présentes conditions sont soumises au droit français. En cas de litige, une solution amiable sera recherchée en priorité. À défaut, les tribunaux compétents seront saisis conformément aux règles de droit commun.</p>

<h2>12. Contact</h2>
<p>Pour toute question relative à ces conditions, utilisez le moyen de contact indiqué dans la section Contact de la page d’accueil. Coordonnées de l’éditeur : {todo}.</p>
""",
    },
    {
        "slug": "politique-confidentialite",
        "title": "Politique de confidentialité | Abonnement IPTV France",
        "h1": "Politique de confidentialité",
        "description": "Politique de confidentialité d’Abonnement IPTV France : données collectées, finalités, durée de conservation et droits RGPD des utilisateurs.",
        "intro": "Cette politique explique quelles données sont collectées lors de votre visite ou de votre commande, pourquoi, et quels sont vos droits.",
        "body": """
<h2>1. Principe général</h2>
<p>Ce site est conçu pour limiter la collecte de données au strict nécessaire. Il ne comporte aucun formulaire d’inscription, aucun espace client et aucun système de paiement intégré. Aucune donnée bancaire n’y est saisie ni stockée.</p>

<h2>2. Données collectées</h2>
<h3>2.1 Données transmises volontairement</h3>
<p>Lorsque vous nous contactez pour commander une formule, vous transmettez les informations nécessaires au traitement de votre demande : la formule choisie, un moyen de vous recontacter et, le cas échéant, le type d’appareil utilisé. Ces informations circulent via le canal de messagerie que vous choisissez.</p>
<h3>2.2 Données techniques</h3>
<p>L’hébergeur du site peut enregistrer des données techniques de connexion (adresse IP, type de navigateur, pages consultées, horodatage) à des fins de sécurité et de fonctionnement du service. Ce traitement relève de l’hébergeur.</p>

<h2>3. Finalités et bases légales</h2>
<ul>
  <li><strong>Répondre à vos demandes et traiter les commandes</strong> — base légale : exécution de mesures précontractuelles ou du contrat.</li>
  <li><strong>Assurer la sécurité et le bon fonctionnement du site</strong> — base légale : intérêt légitime.</li>
  <li><strong>Respecter les obligations légales et comptables</strong> — base légale : obligation légale.</li>
</ul>

<h2>4. Cookies et mesure d’audience</h2>
<p>Ce site ne dépose aucun cookie publicitaire et n’utilise aucun traceur de suivi comportemental. Les polices de caractères sont chargées depuis un service tiers (Google Fonts), qui peut recevoir votre adresse IP au moment de la requête. Si un outil de mesure d’audience est ajouté ultérieurement, cette page sera mise à jour et un dispositif de recueil du consentement sera mis en place.</p>

<h2>5. Destinataires</h2>
<p>Vos données ne sont ni vendues, ni louées, ni transmises à des fins commerciales. Elles peuvent être traitées par les prestataires techniques strictement nécessaires au fonctionnement du site (hébergement, messagerie), dans la limite de leur mission.</p>

<h2>6. Durée de conservation</h2>
<p>Les échanges liés à une commande sont conservés pendant la durée de l’abonnement concerné, puis pendant la durée nécessaire au respect des obligations légales applicables. Les demandes n’ayant pas donné lieu à une commande sont supprimées dans un délai raisonnable.</p>

<h2>7. Transferts hors Union européenne</h2>
<p>Certains prestataires techniques peuvent être établis en dehors de l’Union européenne. Dans ce cas, les transferts sont encadrés par les garanties prévues par le RGPD, notamment les clauses contractuelles types de la Commission européenne.</p>

<h2>8. Vos droits</h2>
<p>Conformément au Règlement général sur la protection des données (RGPD) et à la loi « Informatique et Libertés », vous disposez des droits suivants :</p>
<ul>
  <li>droit d’accès à vos données ;</li>
  <li>droit de rectification ;</li>
  <li>droit à l’effacement ;</li>
  <li>droit à la limitation du traitement ;</li>
  <li>droit d’opposition ;</li>
  <li>droit à la portabilité ;</li>
  <li>droit de définir des directives relatives au sort de vos données après votre décès.</li>
</ul>
<p>Pour exercer ces droits, adressez votre demande au responsable de traitement : {todo}. Une réponse vous sera apportée dans un délai d’un mois.</p>

<h2>9. Réclamation</h2>
<p>Si vous estimez que vos droits ne sont pas respectés, vous pouvez introduire une réclamation auprès de la Commission nationale de l’informatique et des libertés (CNIL), 3 place de Fontenoy, TSA 80715, 75334 Paris Cedex 07, ou sur son site officiel.</p>

<h2>10. Sécurité</h2>
<p>Le site est diffusé via une connexion chiffrée (HTTPS). Des mesures raisonnables sont appliquées pour protéger les informations reçues contre l’accès non autorisé, la perte ou la divulgation.</p>

<h2>11. Responsable de traitement</h2>
<p>Identité et coordonnées du responsable de traitement : {todo}.</p>

<h2>12. Mise à jour</h2>
<p>Cette politique peut être modifiée pour tenir compte d’évolutions légales ou techniques. La date de dernière mise à jour figure en haut de cette page.</p>
""",
    },
    {
        "slug": "politique-remboursement",
        "title": "Politique de remboursement | Abonnement IPTV France",
        "h1": "Politique de remboursement",
        "description": "Politique de remboursement d’Abonnement IPTV France : conditions d’éligibilité, cas exclus, délais de traitement et démarche à suivre.",
        "intro": "Cette page précise dans quels cas un remboursement peut être demandé, comment procéder et quels sont les délais applicables.",
        "body": """
<h2>1. Avant de commander</h2>
<p>Un abonnement IPTV est un service numérique dont l’accès est activé rapidement après la commande. Avant de valider votre choix, vérifiez la durée de la formule, le nombre de connexions, la compatibilité de votre appareil et le débit dont vous disposez. La section « Comment installer votre abonnement IPTV ? » et la section « Une bonne connexion pour une meilleure expérience » de la page d’accueil réunissent les informations utiles.</p>

<h2>2. Droit de rétractation et contenus numériques</h2>
<p>Conformément à l’article L221-28 du Code de la consommation, le droit de rétractation ne peut pas être exercé pour la fourniture d’un contenu numérique non fourni sur un support matériel dont l’exécution a commencé après accord préalable exprès du consommateur et renoncement exprès à son droit de rétractation. En pratique, une fois vos informations de configuration transmises et l’accès activé, le service est considéré comme exécuté.</p>
<p>Tant que l’accès n’a pas été activé, une demande d’annulation peut être adressée et sera examinée.</p>

<h2>3. Cas pouvant donner lieu à un remboursement</h2>
<ul>
  <li>Le service n’a jamais été activé et l’accès n’a pas été transmis.</li>
  <li>Une erreur de facturation ou un double paiement est constaté.</li>
  <li>Un défaut technique persistant, imputable au service, empêche toute utilisation malgré les vérifications effectuées avec le support.</li>
</ul>

<h2>4. Cas ne donnant pas lieu à un remboursement</h2>
<ul>
  <li>Connexion Internet insuffisante, instable ou inadaptée à la qualité souhaitée.</li>
  <li>Appareil incompatible, obsolète ou ne disposant d’aucune application de lecture adaptée.</li>
  <li>Absence d’un contenu particulier qui n’a pas été garanti au moment de la commande.</li>
  <li>Coupures ponctuelles liées à la source du flux, à la charge des serveurs ou aux pics d’audience lors d’événements très suivis.</li>
  <li>Changement d’avis après activation, absence d’utilisation, ou oubli d’utilisation pendant la durée souscrite.</li>
  <li>Partage des informations de connexion, revente ou usage non conforme aux conditions d’utilisation.</li>
  <li>Frais d’activation demandés par une application tierce, qui ne sont pas encaissés par nos soins.</li>
</ul>

<h2>5. Démarche à suivre</h2>
<p>Avant toute demande de remboursement, contactez le support afin qu’un diagnostic soit réalisé. La plupart des difficultés se résolvent par un changement d’application, une reconfiguration de l’appareil ou une amélioration du réseau local.</p>
<p>Si le problème persiste, adressez une demande écrite précisant :</p>
<ul>
  <li>la formule commandée et la date de commande ;</li>
  <li>l’appareil et l’application utilisés ;</li>
  <li>la description du problème rencontré ;</li>
  <li>les vérifications déjà effectuées avec le support.</li>
</ul>

<h2>6. Délais</h2>
<p>Toute demande doit être adressée dans un délai raisonnable après la constatation du problème. Les demandes recevables sont traitées dans les meilleurs délais ; le remboursement est effectué sur le moyen de paiement d’origine lorsque cela est techniquement possible. Le délai de mise à disposition des fonds dépend de l’établissement financier concerné.</p>

<h2>7. Litiges</h2>
<p>En cas de désaccord persistant, une solution amiable sera recherchée en priorité. Conformément aux articles L611-1 et suivants du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation. Coordonnées du médiateur compétent : {todo}.</p>

<h2>8. Contact</h2>
<p>Les demandes relatives à cette politique doivent être adressées par le moyen de contact indiqué dans la section Contact de la page d’accueil. Coordonnées de l’éditeur : {todo}.</p>
""",
    },
    {
        "slug": "mentions-legales",
        "title": "Mentions légales | Abonnement IPTV France",
        "h1": "Mentions légales",
        "description": "Mentions légales du site Abonnement IPTV France : identification de l’éditeur, hébergement, propriété intellectuelle et responsabilité.",
        "intro": "Informations légales relatives à l’éditeur et à l’hébergement du site, conformément à la législation française applicable.",
        "body": """
<h2>1. Éditeur du site</h2>
<p>Conformément à l’article 6-III de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l’économie numérique, les informations suivantes doivent être portées à la connaissance des utilisateurs :</p>
<ul>
  <li><strong>Nom du site</strong> : Abonnement IPTV France</li>
  <li><strong>Adresse du site</strong> : https://abonnement-iptv-france.website</li>
  <li><strong>Éditeur / responsable de la publication</strong> : {todo}</li>
  <li><strong>Statut juridique</strong> : {todo}</li>
  <li><strong>Adresse postale</strong> : {todo}</li>
  <li><strong>Numéro d’immatriculation (SIRET, RCS ou équivalent)</strong> : {todo}</li>
  <li><strong>Numéro de TVA intracommunautaire, le cas échéant</strong> : {todo}</li>
  <li><strong>Adresse de contact</strong> : {todo}</li>
</ul>
<p>Ces champs doivent être renseignés par l’exploitant du site avant toute exploitation commerciale. Aucune information d’identification n’est inventée ni affichée par défaut.</p>

<h2>2. Hébergement</h2>
<p>Le site est hébergé par Vercel Inc. Adresse postale de l’hébergeur : {todo}.</p>

<h2>3. Propriété intellectuelle</h2>
<p>La structure générale du site, ses textes, sa charte graphique, ses icônes et ses éléments visuels originaux sont protégés par le droit de la propriété intellectuelle. Toute reproduction, représentation, adaptation ou exploitation, totale ou partielle, sans autorisation écrite préalable, est interdite.</p>
<p>Les noms de marques, de modèles et de systèmes d’exploitation cités dans la section consacrée aux appareils compatibles appartiennent à leurs propriétaires respectifs. Ils sont mentionnés à titre purement informatif, afin de renseigner l’utilisateur sur la compatibilité technique, et n’impliquent aucun partenariat, aucune affiliation ni aucun parrainage.</p>

<h2>4. Nature du service et droits de diffusion</h2>
<p>Le site présente des formules d’abonnement à un service de diffusion par protocole Internet (IPTV). La technologie IPTV est licite. La diffusion ou l’utilisation de contenus protégés sans l’autorisation des ayants droit peut en revanche constituer une infraction au droit d’auteur et aux droits voisins. L’utilisateur demeure responsable de la conformité de son usage à la législation applicable dans son pays de résidence.</p>

<h2>5. Responsabilité</h2>
<p>Les informations publiées sur ce site sont fournies à titre indicatif et peuvent évoluer. Les débits, compatibilités et durées mentionnés constituent des indications générales et non des garanties de résultat. La responsabilité de l’éditeur ne saurait être engagée en cas d’indisponibilité temporaire du site, d’erreur matérielle ou de dommage indirect lié à son utilisation.</p>

<h2>6. Liens externes</h2>
<p>Le site peut renvoyer vers des services tiers, notamment des applications de messagerie utilisées pour la prise de contact. L’éditeur n’exerce aucun contrôle sur ces services et décline toute responsabilité quant à leur contenu et à leurs conditions d’utilisation.</p>

<h2>7. Données personnelles</h2>
<p>Le traitement des données personnelles est décrit dans la <a href="/politique-confidentialite/">politique de confidentialité</a>.</p>

<h2>8. Droit applicable</h2>
<p>Le présent site est soumis au droit français. Tout litige relatif à son utilisation relève de la compétence des juridictions françaises, sous réserve des règles impératives applicables aux consommateurs.</p>
""",
    },
]


def main():
    root = os.getcwd()
    written = []
    for page in PAGES:
        html = SHELL.format(
            title=page["title"],
            description=page["description"],
            slug=page["slug"],
            h1=page["h1"],
            intro=page["intro"],
            body=page["body"].format(todo=TODO).strip(),
            domain=DOMAIN,
            maj=MAJ,
        )
        folder = os.path.join(root, page["slug"])
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "index.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(path)
    for path in written:
        print("écrit :", os.path.relpath(path, root))


if __name__ == "__main__":
    main()
