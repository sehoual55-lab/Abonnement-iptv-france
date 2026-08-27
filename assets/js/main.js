/* =========================================================
   Abonnement IPTV France — comportements de l'interface
   Aucun framework, aucune dépendance externe.
   ========================================================= */
(function () {
  "use strict";

  var cfg = window.SITE_CONFIG || {};
  var contact = cfg.contact || {};
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var MAX_CONN = 5;
  var REMISE = 0.15; /* chaque connexion supplémentaire : -15 % */

  function euro(value) {
    return value.toFixed(2).replace(".", ",") + " €";
  }

  function totalFor(base, connections) {
    return base * (1 + (1 - REMISE) * (connections - 1));
  }

  /* ---------- 1. Menu mobile ---------- */
  var burger = document.querySelector("[data-burger]");
  var nav = document.getElementById("navigation-principale");

  function closeMenu() {
    if (!burger || !nav) return;
    nav.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false");
    burger.setAttribute("aria-label", "Ouvrir le menu de navigation");
  }

  if (burger && nav) {
    burger.addEventListener("click", function () {
      if (burger.getAttribute("aria-expanded") === "true") {
        closeMenu();
      } else {
        nav.classList.add("is-open");
        burger.setAttribute("aria-expanded", "true");
        burger.setAttribute("aria-label", "Fermer le menu de navigation");
      }
    });

    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeMenu();
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 980) closeMenu();
    });
  }

  /* ---------- 2. État de l'en-tête au défilement ---------- */
  var header = document.querySelector(".header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- 3. Lien de navigation actif ---------- */
  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll('#navigation-principale a[href^="#"]')
  );
  var watched = navLinks
    .map(function (a) { return document.querySelector(a.getAttribute("href")); })
    .filter(Boolean);

  if (watched.length && "IntersectionObserver" in window) {
    var spy = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          navLinks.forEach(function (a) {
            if (a.getAttribute("href") === "#" + entry.target.id) a.setAttribute("aria-current", "true");
            else a.removeAttribute("aria-current");
          });
        });
      },
      { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
    );
    watched.forEach(function (el) { spy.observe(el); });
  }

  /* ---------- 4. Révélation douce des sections ---------- */
  var revealables = document.querySelectorAll(".reveal");
  if (revealables.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(revealables, function (el) { el.classList.add("is-in"); });
    } else {
      var io = new IntersectionObserver(
        function (entries, obs) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-in");
            obs.unobserve(entry.target);
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.06 }
      );
      Array.prototype.forEach.call(revealables, function (el) { io.observe(el); });
    }
  }

  /* ---------- 5. Formules : sélecteur de connexions ---------- */
  var cards = Array.prototype.slice.call(document.querySelectorAll("[data-plan-card]"));
  var plans = [];

  cards.forEach(function (card) {
    var cta = card.querySelector("[data-plan]");
    var plan = {
      id: plans.length,
      nom: cta ? cta.getAttribute("data-plan") : "",
      duree: cta ? cta.getAttribute("data-duration") : "",
      bonus: cta ? cta.getAttribute("data-bonus") || "" : "",
      base: parseFloat(card.getAttribute("data-base")),
      connexions: 1,
      cta: cta
    };
    plans.push(plan);

    var totalEl = card.querySelector("[data-plan-total]");
    var labelEl = card.querySelector("[data-conn-label]");
    var steps = card.querySelectorAll("[data-conn-step]");

    function render() {
      totalEl.textContent = euro(totalFor(plan.base, plan.connexions));
      labelEl.textContent = plan.connexions + (plan.connexions > 1 ? " connexions" : " connexion");
      Array.prototype.forEach.call(steps, function (btn) {
        var delta = parseInt(btn.getAttribute("data-conn-step"), 10);
        btn.disabled = (delta < 0 && plan.connexions === 1) || (delta > 0 && plan.connexions === MAX_CONN);
      });
    }

    Array.prototype.forEach.call(steps, function (btn) {
      btn.addEventListener("click", function () {
        var next = plan.connexions + parseInt(btn.getAttribute("data-conn-step"), 10);
        if (next < 1 || next > MAX_CONN) return;
        plan.connexions = next;
        render();
      });
    });

    render();
  });

  /* ---------- 6. Fenêtre de commande ---------- */
  var dialog = document.getElementById("checkout");
  var form = document.querySelector("[data-checkout-form]");
  var done = document.querySelector("[data-checkout-done]");
  var doneText = document.querySelector("[data-checkout-done-text]");
  var errorBox = document.querySelector("[data-checkout-error]");
  var submitBtn = document.querySelector("[data-checkout-submit]");
  var selection = null; /* { plan, connexions } */

  function channel() {
    if (contact.whatsapp) return "whatsapp";
    if (contact.email) return "email";
    if (contact.telegram) return "telegram";
    return null;
  }

  function renderRecap() {
    if (!selection) return;
    var plan = selection.plan;
    var n = selection.connexions;
    var nom = plan.nom.replace(/^Pack /, "");

    document.querySelector("[data-recap-plan]").textContent =
      nom + " — " + plan.duree + (plan.bonus ? " (" + plan.bonus + ")" : "");
    document.querySelector("[data-recap-conn]").textContent =
      n > 1 ? n + " connexions simultanées" : "1 connexion simultanée";
    document.querySelector("[data-recap-total]").textContent = euro(totalFor(plan.base, n));
  }

  function buildMessage() {
    var plan = selection.plan;
    var n = selection.connexions;
    var data = new FormData(form);
    var tel = String(data.get("telephone") || "").trim();

    var lines = [
      "Nouvelle commande",
      "",
      "Abonnement : " + plan.nom.replace(/^Pack /, "") + " — " + plan.duree +
        (plan.bonus ? " (" + plan.bonus + ")" : ""),
      "Connexions : " + n + (n > 1 ? " (flux simultanés)" : " (flux simultané)"),
      "Total à régler : " + euro(totalFor(plan.base, n)),
      "Mode de paiement : " + data.get("paiement"),
      "",
      "Nom : " + String(data.get("nom") || "").trim(),
      "E-mail : " + String(data.get("email") || "").trim()
    ];
    if (tel) lines.push("Téléphone : " + data.get("indicatif") + " " + tel);
    return lines.join("\n");
  }

  function showError(message) {
    if (!errorBox) return;
    errorBox.textContent = message;
    errorBox.hidden = false;
  }

  function clearError() {
    if (errorBox) errorBox.hidden = true;
  }

  function openCheckout(plan, connexions) {
    if (!dialog || !plan) return;
    selection = { plan: plan, connexions: connexions || 1 };
    clearError();
    if (form) form.hidden = false;
    if (done) done.hidden = true;
    renderRecap();

    if (typeof dialog.showModal === "function") {
      if (!dialog.open) dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
    }

    window.setTimeout(function () {
      var first = form && form.querySelector("#co-nom");
      if (first) first.focus();
    }, reduceMotion ? 0 : 180);
  }

  function closeCheckout() {
    if (!dialog) return;
    if (typeof dialog.close === "function" && dialog.open) dialog.close();
    else dialog.removeAttribute("open");
  }

  if (dialog && form) {
    /* Le bouton de chaque formule ouvre la fenêtre avec son état courant */
    plans.forEach(function (plan) {
      var cta = plan.cta;
      if (!cta) return;
      cta.addEventListener("click", function (e) {
        e.preventDefault();
        openCheckout(plan, plan.connexions);
      });
    });

    Array.prototype.forEach.call(document.querySelectorAll("[data-checkout-close]"), function (btn) {
      btn.addEventListener("click", closeCheckout);
    });

    dialog.addEventListener("click", function (e) {
      if (e.target === dialog) closeCheckout();
    });

    /* Repli de sélection pour les navigateurs sans :has() */
    var payOpts = Array.prototype.slice.call(form.querySelectorAll(".pay-opt"));
    function syncPay() {
      payOpts.forEach(function (opt) {
        opt.classList.toggle("is-checked", opt.querySelector("input").checked);
      });
    }
    payOpts.forEach(function (opt) {
      opt.querySelector("input").addEventListener("change", syncPay);
    });
    syncPay();

    /* Ligne « Une question ? WhatsApp … » */
    var ask = document.querySelector("[data-checkout-ask]");
    if (ask && contact.whatsapp) {
      var num = String(contact.whatsapp).replace(/\D/g, "");
      ask.querySelector("[data-checkout-wa]").href =
        "https://wa.me/" + num + "?text=" +
        encodeURIComponent("Bonjour, j’ai une question avant de commander.");
      ask.querySelector("[data-checkout-wa-num]").textContent = contact.whatsappAffiche || ("+" + num);
      ask.hidden = false;
    }

    if (!channel() && submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Commande momentanément indisponible";
      if (window.console && console.warn) {
        console.warn(
          "[Abonnement IPTV France] Aucun moyen de contact configuré : renseignez " +
          "contact.whatsapp, contact.email ou contact.telegram dans assets/js/config.js."
        );
      }
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      clearError();

      var nom = form.querySelector("#co-nom");
      var email = form.querySelector("#co-email");
      nom.removeAttribute("aria-invalid");
      email.removeAttribute("aria-invalid");

      if (!nom.value.trim()) {
        nom.setAttribute("aria-invalid", "true");
        nom.focus();
        showError("Merci d’indiquer votre nom.");
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) {
        email.setAttribute("aria-invalid", "true");
        email.focus();
        showError("Merci d’indiquer une adresse e-mail valide.");
        return;
      }

      var canal = channel();
      if (!canal) {
        showError("La prise de commande n’est pas encore active. Merci de réessayer plus tard.");
        return;
      }

      var message = buildMessage();
      var plan = selection.plan;
      var url;

      if (canal === "whatsapp") {
        url = "https://wa.me/" + String(contact.whatsapp).replace(/\D/g, "") +
          "?text=" + encodeURIComponent(message);
      } else if (canal === "email") {
        var sujet = String(cfg.objetEmail || "Commande — {formule}").replace(/\{formule\}/g, plan.nom);
        url = "mailto:" + contact.email +
          "?subject=" + encodeURIComponent(sujet) + "&body=" + encodeURIComponent(message);
      } else {
        url = contact.telegram;
      }

      /* Copie vers la feuille Google. Le corps est encodé en
         application/x-www-form-urlencoded : Apps Script ne sait pas lire
         un multipart/form-data, e.parameter resterait vide. */
      if (contact.endpoint && window.fetch && window.URLSearchParams) {
        var payload = new URLSearchParams();
        var champs = new FormData(form);
        champs.forEach(function (valeur, cle) { payload.append(cle, valeur); });
        payload.append("formule", plan.nom);
        payload.append("connexions", String(selection.connexions));
        payload.append("total", euro(totalFor(plan.base, selection.connexions)));
        /* Nom du pays choisi dans le sélecteur d'indicatif, pour la notification */
        var optPays = form.querySelector("#co-indicatif");
        if (optPays && optPays.selectedIndex >= 0) {
          payload.append("pays", optPays.options[optPays.selectedIndex].textContent.replace(/\s*\+\d+$/, "").trim());
        }
        fetch(contact.endpoint, { method: "POST", body: payload, mode: "no-cors" })
          .catch(function () { /* la messagerie reste le canal principal */ });
      }

      window.open(url, canal === "email" ? "_self" : "_blank", "noopener");

      if (doneText && canal === "telegram") {
        doneText.textContent =
          "Telegram s’ouvre dans un nouvel onglet. Collez-y le récapitulatif de votre commande pour la transmettre.";
      }

      form.hidden = true;
      if (done) {
        done.hidden = false;
        var closeBtn = done.querySelector("[data-checkout-close]");
        if (closeBtn) closeBtn.focus();
      }
    });
  }


  /* ---------- 7. Guides d'installation par appareil ---------- */
  (function () {
    var picker = document.querySelector("[data-guide-picker]");
    if (!picker) return;

    var trigger = picker.querySelector(".picker-trigger");
    var menu = picker.querySelector(".picker-menu");
    var options = Array.prototype.slice.call(menu.querySelectorAll("[data-guide-value]"));
    var current = picker.querySelector("[data-guide-current]");
    var icone = document.querySelector("[data-guide-icon]");
    var panels = Array.prototype.slice.call(document.querySelectorAll("[data-guide-panel]"));

    var ICONES = {
      smarttv: "#i-tv",
      android: "#i-phone",
      ios: "#i-tablet",
      desktop: "#i-laptop",
      formuler: "#i-box",
      mag: "#i-stick"
    };

    var actif = 0;      /* option survolée au clavier */
    var choisi = 0;     /* option retenue */

    function setActive(index, scroll) {
      actif = Math.max(0, Math.min(options.length - 1, index));
      options.forEach(function (opt, i) {
        opt.classList.toggle("is-active", i === actif);
      });
      menu.setAttribute("aria-activedescendant", options[actif].id);
      if (scroll !== false) options[actif].scrollIntoView({ block: "nearest" });
    }

    function open() {
      menu.hidden = false;
      trigger.setAttribute("aria-expanded", "true");
      setActive(choisi);
      menu.focus();
    }

    function close(rendreFocus) {
      menu.hidden = true;
      trigger.setAttribute("aria-expanded", "false");
      menu.removeAttribute("aria-activedescendant");
      options.forEach(function (opt) { opt.classList.remove("is-active"); });
      if (rendreFocus) trigger.focus();
    }

    function choose(index) {
      choisi = index;
      var opt = options[index];
      var slug = opt.getAttribute("data-guide-value");
      var nom = opt.querySelector(".picker-opt-name").textContent;

      options.forEach(function (o, i) {
        o.setAttribute("aria-selected", i === index ? "true" : "false");
      });

      current.textContent = nom;
      trigger.setAttribute("aria-label",
        "Appareil sélectionné : " + nom + ". Choisissez votre appareil pour afficher le guide d’installation.");
      if (icone && ICONES[slug]) icone.setAttribute("href", ICONES[slug]);

      panels.forEach(function (panel) {
        panel.hidden = panel.getAttribute("data-guide-panel") !== slug;
      });
    }

    trigger.addEventListener("click", function () {
      if (menu.hidden) open();
      else close(true);
    });

    trigger.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp" || e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        open();
      }
    });

    menu.addEventListener("keydown", function (e) {
      switch (e.key) {
        case "ArrowDown": e.preventDefault(); setActive(actif + 1); break;
        case "ArrowUp": e.preventDefault(); setActive(actif - 1); break;
        case "Home": e.preventDefault(); setActive(0); break;
        case "End": e.preventDefault(); setActive(options.length - 1); break;
        case "Enter":
        case " ": e.preventDefault(); choose(actif); close(true); break;
        case "Escape": e.preventDefault(); close(true); break;
        case "Tab": close(false); break;
        default: break;
      }
    });

    options.forEach(function (opt, i) {
      opt.addEventListener("click", function () {
        choose(i);
        close(true);
      });
      opt.addEventListener("mousemove", function () {
        if (actif !== i) setActive(i, false);
      });
    });

    document.addEventListener("click", function (e) {
      if (!menu.hidden && !picker.contains(e.target)) close(false);
    });

    choose(0);
  })();

  /* ---------- 8. Widget WhatsApp ---------- */
  (function () {
    var wrap = document.querySelector("[data-wa]");
    if (!wrap) return;

    /* Sans numéro configuré, le widget n'est pas affiché du tout. */
    if (!contact.whatsapp) return;

    var numero = String(contact.whatsapp).replace(/\D/g, "");
    var panel = wrap.querySelector("[data-wa-panel]");
    var toggle = wrap.querySelector("[data-wa-toggle]");
    var link = wrap.querySelector("[data-wa-link]");
    var chips = Array.prototype.slice.call(wrap.querySelectorAll("[data-wa-topic]"));
    var defaut = "Bonjour, je souhaite des informations sur vos abonnements.";

    function setMessage(texte) {
      link.href = "https://wa.me/" + numero + "?text=" + encodeURIComponent(texte);
    }

    function open() {
      panel.hidden = false;
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Fermer la discussion WhatsApp");
    }

    function close() {
      panel.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Ouvrir la discussion WhatsApp");
    }

    chips.forEach(function (chip) {
      chip.setAttribute("aria-pressed", "false");
      chip.addEventListener("click", function () {
        chips.forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
        chip.setAttribute("aria-pressed", "true");
        setMessage(chip.getAttribute("data-wa-topic"));
        link.focus();
      });
    });

    toggle.addEventListener("click", function () {
      if (toggle.getAttribute("aria-expanded") === "true") {
        close();
      } else {
        open();
        window.setTimeout(function () { link.focus(); }, reduceMotion ? 0 : 160);
      }
    });

    Array.prototype.forEach.call(wrap.querySelectorAll("[data-wa-close]"), function (btn) {
      btn.addEventListener("click", function () {
        close();
        toggle.focus();
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        close();
        toggle.focus();
      }
    });

    document.addEventListener("click", function (e) {
      if (toggle.getAttribute("aria-expanded") !== "true") return;
      if (!wrap.contains(e.target)) close();
    });

    setMessage(defaut);
    wrap.hidden = false;
  })();
})();
