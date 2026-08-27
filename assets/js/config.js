/* =========================================================
   Abonnement IPTV France — configuration du site
   ---------------------------------------------------------
   SEUL FICHIER À MODIFIER pour renseigner vos moyens de
   contact. Le premier canal renseigné (WhatsApp, puis e-mail,
   puis Telegram) reçoit les commandes envoyées depuis la
   fenêtre de commande. Tant que les trois restent vides, le
   bouton d'envoi est désactivé et un avertissement est affiché
   dans la console du navigateur.
   ========================================================= */

window.SITE_CONFIG = {
  /* Remise appliquée à chaque connexion supplémentaire (voir aussi assets/js/main.js).
     Valeur actuelle : 15 %, maximum 5 connexions par formule. */

  contact: {
    /* Numéro WhatsApp au format international, sans « + »,
       sans espace et sans zéro initial. Exemple : "33612345678" */
    whatsapp: "16615413954",

    /* Affichage lisible du même numéro (widget et fenêtre de commande). */
    whatsappAffiche: "+1 (661) 541-3954",

    /* Adresse e-mail de commande. Exemple : "contact@abonnement-iptv-france.website" */
    email: "",

    /* Lien Telegram complet. Exemple : "https://t.me/votre_compte" */
    telegram: "",

    /* Copie de chaque commande vers la feuille Google
       « Abonnement iptv france - Commandes ».
       Collez ici l'URL en /exec obtenue au déploiement du script
       _sources/orders-apps-script.gs. Vide = envoi désactivé.
       La messagerie reste dans tous les cas le canal principal. */
    endpoint: "https://script.google.com/macros/s/AKfycbwRb4xjKKFAGRR5E4GMBLpY26J7plXfZGDIH5n6wjT3m-5eNAsdDjB0PiPvEKfC_WRNig/exec"
  },


  /* Objet de l'e-mail lorsque la commande passe par mailto:.
     {formule} est remplacé par le nom de la formule choisie.
     Les messages envoyés ne contiennent volontairement ni lien
     vers le site ni le mot « IPTV ». */
  objetEmail: "Commande — {formule}"
};
