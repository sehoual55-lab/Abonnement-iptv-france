# Bien Regardé

Static site — independent comparison guides for legal TV and streaming offers in France.

No framework, no build step. Plain HTML, one stylesheet, folder-based clean URLs.

## Structure

```
index.html                                  Blog index
methode/                                    Editorial method / transparency page
guides/comparatif-abonnement-tv-streaming-2026/
guides/alternatives-canal-plus/
guides/iptv-legale-ou-illegale/
assets/css/style.css                        Single stylesheet
robots.txt, sitemap.xml
_sources/set_domain.py                      Placeholder-domain swap
```

## Before deploying

1. **Set the real domain.** Every canonical, OG tag, sitemap entry and robots line
   currently uses the placeholder `votre-domaine.fr`.

   ```bash
   python3 _sources/set_domain.py votredomaine.fr
   ```

   It prints a replacement count per file per pattern. Expect **18** in total.
   A `0` on any file means the swap missed and should be investigated before push.

2. **Write `/mentions-legales/`.** It is linked from every page footer but not yet
   created — it needs a real company name, address and SIREN. Affiliate network
   reviewers open this page first.

3. **Write `/politique-confidentialite/`.** Linked from the index footer. Required
   under RGPD once analytics or affiliate cookies are in use.

## Deploying

Vercel, Netlify, Cloudflare Pages or plain cPanel all serve this as-is — it is
static files with no server requirements. Folder-based URLs mean no rewrite rules
are needed.

## Maintenance

Every article carries a visible `Tarifs vérifiés le …` date in the masthead band.
French streaming prices moved several times in the last eighteen months, so review
quarterly and update both the figures and the date. Stale prices are the fastest
way to lose rankings on this kind of content.

Sources are listed at the foot of each article and link to the operators' own
pages. Keep it that way — the sourced figures are what distinguishes these guides
from the rest of the SERP.

## Affiliate disclosure

Each article ends with a disclosure block, and `/methode/` explains the model in
full. This is a legal requirement in France, not an optional courtesy. Do not
remove these blocks when editing.
