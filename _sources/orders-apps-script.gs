/**
 * =========================================================
 * Abonnement IPTV France — enregistrement des commandes
 * ---------------------------------------------------------
 * Reçoit les commandes envoyées par la fenêtre de commande du
 * site, les ajoute à la feuille Google « Abonnement iptv france
 * - Commandes » et envoie une notification par e-mail.
 *
 * La notification par e-mail reprend le format tableau HTML utilisé
 * sur les autres sites (Website, Name, Email, Phone, Country, Plan,
 * Connections, Total, Payment method, Payment link, Received).
 *
 * Colonnes attendues, dans cet ordre (déjà en place) :
 *   A Date · B Nom · C Email · D Téléphone · E Formule
 *   F Prix (€) · G Connexions · H Paiement · I Statut
 *
 * INSTALLATION
 *  1. Ouvrez la feuille → Extensions → Apps Script.
 *  2. Collez ce fichier à la place du contenu par défaut, puis
 *     enregistrez.
 *  3. Lancez une fois « testerAvecUneCommandeFictive » depuis
 *     l'éditeur : Google demandera les autorisations feuille +
 *     e-mail. Acceptez, vérifiez la ligne de test, supprimez-la.
 *  4. Déployer → Nouveau déploiement → « Application web »
 *       · Exécuter en tant que : moi
 *       · Qui a accès : tout le monde
 *  5. Copiez l'URL en /exec et collez-la dans
 *     assets/js/config.js → contact.endpoint
 *
 * Le site ouvre WhatsApp dans tous les cas : cette feuille est
 * une copie de sécurité, pas le canal principal. Si le script
 * tombe, la commande arrive quand même sur WhatsApp.
 * =========================================================
 */

var CONFIG = {
  /* Identifiant de la feuille Google. */
  feuilleId: '1a80-QGBS3dkIMDrJNSVVdcFO-h5u0iCq3Pg3eIopphE',

  /* Nom de l'onglet. Laissez vide pour utiliser le premier onglet. */
  onglet: '',

  /* Adresse recevant la notification. Videz la chaîne pour désactiver l'e-mail. */
  notification: 'xyz905391@gmail.com',

  /* Nom du site, affiché dans l'objet et dans l'en-tête de l'e-mail. */
  site: 'abonnement-iptv-france.website',

  /* Fuseau utilisé pour la colonne Date. */
  fuseau: 'Europe/Paris',

  /* Marque « Doublon » dans la colonne Statut si l'e-mail ou le
     téléphone est déjà présent dans la feuille. */
  detecterDoublons: true
};

/* Position des colonnes, 1 = A. Modifiez ici si vous réorganisez la feuille. */
var COL = {
  date: 1,
  nom: 2,
  email: 3,
  telephone: 4,
  formule: 5,
  prix: 6,
  connexions: 7,
  paiement: 8,
  statut: 9
};

var NB_COLONNES = 9;


/** Point d'entrée appelé par le site. */
function doPost(e) {
  try {
    var champs = lireChamps(e);
    var feuille = ouvrirFeuille();
    preparerFormats(feuille);

    var doublon = CONFIG.detecterDoublons ? chercherDoublon(feuille, champs) : '';

    var ligne = [];
    ligne[COL.date - 1] = Utilities.formatDate(new Date(), CONFIG.fuseau, 'dd/MM/yyyy HH:mm');
    ligne[COL.nom - 1] = champs.nom;
    ligne[COL.email - 1] = champs.email;
    ligne[COL.telephone - 1] = champs.telephone;
    ligne[COL.formule - 1] = champs.formule;
    ligne[COL.prix - 1] = champs.prix;           // nombre, pour pouvoir additionner
    ligne[COL.connexions - 1] = champs.connexions;
    ligne[COL.paiement - 1] = champs.paiement;
    ligne[COL.statut - 1] = doublon ? 'Doublon' : 'Nouvelle';

    var rang = premiereLigneVide(feuille);
    feuille.getRange(rang, 1, 1, NB_COLONNES).setValues([ligne]);
    feuille.getRange(rang, 1, 1, NB_COLONNES)
           .setBackground(doublon ? '#fff3e0' : '#eef4ff');

    notifier(champs, doublon);
    return reponse({ ok: true, ligne: rang });
  } catch (err) {
    console.error(err);
    return reponse({ ok: false, erreur: String(err) });
  }
}


/** Permet de vérifier le déploiement depuis un navigateur. */
function doGet() {
  return reponse({ ok: true, message: 'Service actif' });
}


/**
 * Extrait les champs. Le site poste en application/x-www-form-urlencoded,
 * donc e.parameter est rempli ; le repli JSON couvre un envoi manuel.
 */
function lireChamps(e) {
  var brut = {};

  if (e && e.parameter && Object.keys(e.parameter).length) {
    brut = e.parameter;
  } else if (e && e.postData && e.postData.contents) {
    try {
      brut = JSON.parse(e.postData.contents);
    } catch (ignore) {
      brut = {};
    }
  }

  var indicatif = String(brut.indicatif || '').trim();
  var numero = String(brut.telephone || '').trim();

  return {
    nom: String(brut.nom || '').trim(),
    email: String(brut.email || '').trim().toLowerCase(),
    telephone: numero ? (indicatif + ' ' + numero).trim() : '',
    numeroSeul: numero.replace(/\D/g, ''),
    formule: String(brut.formule || '').trim(),
    prix: enNombre(brut.total),
    prixAffiche: String(brut.total || '').trim(),
    connexions: parseInt(brut.connexions || '1', 10) || 1,
    paiement: String(brut.paiement || '').trim(),
    pays: String(brut.pays || '').trim(),
    lienPaiement: String(brut.lienPaiement || '').trim()
  };
}


/** « 92,48 € » devient 92.48 pour que la colonne reste additionnable. */
function enNombre(valeur) {
  var texte = String(valeur || '').replace(/[^\d,.-]/g, '').replace(',', '.');
  var nombre = parseFloat(texte);
  return isNaN(nombre) ? '' : nombre;
}


/** Ouvre la feuille par son identifiant. */
function ouvrirFeuille() {
  var classeur = SpreadsheetApp.openById(CONFIG.feuilleId);
  var feuille = CONFIG.onglet
    ? classeur.getSheetByName(CONFIG.onglet)
    : classeur.getSheets()[0];

  if (!feuille) {
    throw new Error('Onglet introuvable : ' + CONFIG.onglet);
  }
  return feuille;
}


/**
 * Force la colonne Téléphone en texte brut : sans cela, Google Sheets
 * interprète « +33 6 12 … » comme le début d'une formule. Fixe aussi le
 * format monétaire de la colonne Prix.
 */
function preparerFormats(feuille) {
  feuille.getRange(2, COL.telephone, feuille.getMaxRows() - 1, 1).setNumberFormat('@');
  feuille.getRange(2, COL.prix, feuille.getMaxRows() - 1, 1).setNumberFormat('#,##0.00\u00a0"€"');
}


/** Première ligne réellement vide, en ignorant les lignes mises en forme. */
function premiereLigneVide(feuille) {
  var dernier = feuille.getLastRow();
  if (dernier < 1) return 2;

  var valeurs = feuille.getRange(1, 1, dernier, NB_COLONNES).getValues();
  for (var i = valeurs.length - 1; i >= 1; i--) {
    if (valeurs[i].join('').trim() !== '') {
      return i + 2;
    }
  }
  return 2;
}


/** Renvoie un motif si l'e-mail ou le téléphone existe déjà. */
function chercherDoublon(feuille, champs) {
  var dernier = feuille.getLastRow();
  if (dernier < 2) return '';

  var donnees = feuille.getRange(2, 1, dernier - 1, NB_COLONNES).getValues();
  var motifs = [];

  for (var i = 0; i < donnees.length; i++) {
    var mail = String(donnees[i][COL.email - 1]).trim().toLowerCase();
    if (champs.email && mail === champs.email && motifs.indexOf('e-mail') === -1) {
      motifs.push('e-mail');
    }
    var tel = String(donnees[i][COL.telephone - 1]).replace(/\D/g, '');
    if (champs.numeroSeul && tel && tel === champs.numeroSeul && motifs.indexOf('téléphone') === -1) {
      motifs.push('téléphone');
    }
  }

  return motifs.length ? motifs.join(' + ') : '';
}


/** Envoie la notification au format tableau HTML. */
function notifier(champs, doublon) {
  if (!CONFIG.notification) return;

  var recu = Utilities.formatDate(new Date(), CONFIG.fuseau, "EEE dd MMM yyyy HH:mm:ss") +
             ' (' + CONFIG.fuseau + ')';
  var lienFeuille = 'https://docs.google.com/spreadsheets/d/' + CONFIG.feuilleId + '/edit';

  var lignes = [
    ['Website', CONFIG.site],
    ['Name', echapper(champs.nom)],
    ['Email', champs.email ? lien('mailto:' + champs.email, champs.email) : ''],
    ['Phone', echapper(champs.telephone)],
    ['Country', echapper(champs.pays)],
    ['Plan', echapper(champs.formule)],
    ['Connections', String(champs.connexions)],
    ['Total', echapper(champs.prixAffiche || champs.prix)],
    ['Payment method', echapper(champs.paiement)],
    ['Payment link', champs.lienPaiement ? lien(champs.lienPaiement, champs.lienPaiement) : ''],
    ['Received', recu]
  ];

  var corpsHtml =
    '<div style="font-family:Arial,Helvetica,sans-serif;color:#111;max-width:640px">' +
      (doublon
        ? '<p style="margin:0 0 16px;padding:10px 14px;border-radius:6px;background:#fff3e0;' +
          'border:1px solid #e0a03a;color:#8a5300;font-size:14px">' +
          'Customer already in the sheet (' + echapper(doublon) + ')</p>'
        : '') +
      '<h2 style="margin:0 0 18px;font-size:20px">New order — ' + echapper(CONFIG.site) + '</h2>' +
      '<table cellspacing="0" cellpadding="0" style="border-collapse:collapse;width:100%;' +
      'border:1px solid #d9d9d9;font-size:14px">' +
      lignes.map(function (l, i) {
        return '<tr style="background:' + (i % 2 ? '#ffffff' : '#f7f7f7') + '">' +
          '<th style="text-align:left;padding:11px 14px;border:1px solid #d9d9d9;' +
          'width:170px;font-weight:bold">' + l[0] + '</th>' +
          '<td style="padding:11px 14px;border:1px solid #d9d9d9">' + l[1] + '</td></tr>';
      }).join('') +
      '</table>' +
      '<p style="margin:20px 0 0">' +
      '<a href="' + lienFeuille + '" style="display:inline-block;padding:10px 18px;' +
      'border-radius:6px;background:#1a56d6;color:#fff;text-decoration:none;font-size:14px">' +
      'Open the orders sheet</a></p>' +
    '</div>';

  var corpsTexte = lignes.map(function (l) {
    return l[0] + ' : ' + String(l[1]).replace(/<[^>]*>/g, '');
  }).join('\n');

  var objet = 'New order [' + CONFIG.site + '] : ' + champs.formule +
              ' — ' + (champs.prixAffiche || champs.prix) +
              (champs.nom ? ' (' + champs.nom + ')' : '') +
              (doublon ? ' [duplicate]' : '');

  MailApp.sendEmail({
    to: CONFIG.notification,
    subject: objet,
    body: corpsTexte,
    htmlBody: corpsHtml
  });
}


/** Lien HTML sûr. */
function lien(href, texte) {
  return '<a href="' + echapper(href) + '" style="color:#1a56d6">' + echapper(texte) + '</a>';
}


/** Neutralise les caractères pouvant casser le HTML de l'e-mail. */
function echapper(valeur) {
  return String(valeur == null ? '' : valeur)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}


/** Réponse JSON. */
function reponse(objet) {
  return ContentService
    .createTextOutput(JSON.stringify(objet))
    .setMimeType(ContentService.MimeType.JSON);
}


/**
 * À lancer une fois depuis l'éditeur pour accorder les autorisations et
 * vérifier feuille + e-mail, sans passer par le site. Pensez à supprimer
 * la ligne de test ensuite.
 */
function testerAvecUneCommandeFictive() {
  var res = doPost({
    parameter: {
      nom: 'Test — à supprimer',
      pays: 'France',
      email: 'test@example.com',
      indicatif: '+33',
      telephone: '6 12 34 56 78',
      formule: 'Pack Gold',
      total: '92,48 €',
      connexions: '2',
      paiement: 'PayPal'
    }
  });
  Logger.log(res.getContent());
}
