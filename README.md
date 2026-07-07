# obx-windsports

Static site for **windsports.obx.deals** — a rider's guide to wind-sports
(kiteboarding/windsurfing) vacation rentals on Hatteras Island, NC.

Part of the `obx.deals` network (see `tiddnet/rental-intel` ADR 0212).
Plain static HTML, no build step, hosted on GitHub Pages. Custom domain
via `CNAME` file + Route53 CNAME record (`terraform/main.tf` in
`rental-intel`).

## Structure

- `index.html` — hero + area picker
- `canadian-hole/`, `tri-villages/`, `island-creek/` — area guides + featured houses
- `guide/` — "what makes a trip work" practical guide

## Updating

Pages are hand-maintained (not regenerated from live data) — see ADR
0212 for what's deferred (wiring featured-house selection to the
Verified/Featured badge system). Edit HTML directly, commit, push;
GitHub Pages redeploys automatically.
