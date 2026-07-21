from __future__ import annotations

import json
from typing import Protocol


class TranslatorLike(Protocol):
    def __call__(self, text: str, **values: object) -> str: ...


DASHBOARD_CSS = r"""
:root {
  color-scheme: light dark;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --panel: color-mix(in srgb, CanvasText 5%, transparent);
  --panel-strong: color-mix(in srgb, CanvasText 8%, transparent);
  --border: color-mix(in srgb, CanvasText 20%, transparent);
  --muted: color-mix(in srgb, CanvasText 68%, transparent);
  --green: #22c55e;
  --yellow: #facc15;
  --red: #ef4444;
  --blue: #3b82f6;
  --gray: #94a3b8;
}
* { box-sizing: border-box; }
html, body { width: 100%; height: 100%; min-height: 100%; margin: 0; overflow: hidden; }
body { background: Canvas; color: CanvasText; }
.page-scroll {
  width: 100%;
  height: 100%;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-y;
  overscroll-behavior-x: none;
  overscroll-behavior-y: contain;
  scrollbar-gutter: stable;
  padding: calc(1.2rem + env(safe-area-inset-top)) calc(1.2rem + env(safe-area-inset-right)) calc(1.2rem + env(safe-area-inset-bottom)) calc(1.2rem + env(safe-area-inset-left));
}
main { max-width: 1040px; margin: 0 auto; padding-bottom: .25rem; }
header, section { border: 1px solid var(--border); border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 1rem; }
h1 { margin: 0 0 .35rem; font-size: 1.7rem; }
h2 { margin: 0 0 .8rem; font-size: 1.25rem; }
h3 { margin: 1rem 0 .55rem; font-size: 1rem; }
p { line-height: 1.5; }
.meta { display: grid; grid-template-columns: repeat(auto-fit,minmax(190px,1fr)); gap: .6rem; }
.meta div { padding: .65rem; border-radius: 9px; background: var(--panel); }
.report-header { display:grid; gap:.85rem; }
.header-intro p { margin:.15rem 0 0; color:var(--muted); }
.language-switcher { display:flex; flex-wrap:wrap; gap:.4rem; margin-top:.75rem; max-width:100%; }
.language-switcher a { display:inline-flex; align-items:center; justify-content:center; min-height:2.25rem; padding:.38rem .72rem; border:1px solid var(--border); border-radius:999px; color:CanvasText; background:Canvas; text-decoration:none; font-size:.82rem; line-height:1.2; white-space:nowrap; }
.language-switcher a:hover { border-color:var(--blue); background:color-mix(in srgb,var(--blue) 6%,Canvas); }
.language-switcher a:focus-visible { outline:3px solid color-mix(in srgb,var(--blue) 76%,CanvasText); outline-offset:2px; }
.language-switcher a[aria-current="page"] { border-color:var(--blue); background:color-mix(in srgb,var(--blue) 10%,Canvas); font-weight:760; box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--blue) 20%,transparent); }
.location-details { margin:0; border:1px solid var(--border); border-radius:10px; background:color-mix(in srgb,CanvasText 2%,transparent); }
.location-details > summary { min-height:auto; padding:.62rem .75rem; justify-content:flex-start; }
.location-details > summary::after { margin-left:auto; }
.location-details > summary > span:not(.details-summary-icon) { display:grid; gap:.08rem; }
.location-details > summary strong { font-size:.84rem; }
.location-details > summary small { font-weight:400; }
.details-summary-icon { display:grid; place-items:center; width:1.75rem; height:1.75rem; border-radius:50%; background:color-mix(in srgb,var(--blue) 12%,transparent); flex:0 0 auto; }
.location-details-body { display:grid; gap:.45rem; padding:0 .85rem .8rem 3.1rem; }
.location-details-values { display:grid; gap:.16rem; }
.location-details-values span { color:var(--muted); overflow-wrap:anywhere; }
.location-details-body p { margin:0; font-size:.82rem; color:var(--muted); }
.header-resource-links { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.7rem; }
.external-map-link, .manual-link { display:flex; align-items:center; gap:.7rem; min-height:auto; padding:.62rem .75rem; color:inherit; text-decoration:none; min-width:0; }
.external-map-link:hover, .external-map-link:focus-visible, .manual-link:hover, .manual-link:focus-visible { border-color:var(--blue); background:color-mix(in srgb,var(--blue) 6%,transparent); outline:none; }
.manual-icon { background:color-mix(in srgb,var(--green) 12%,transparent); }
.external-map-copy { display:grid; gap:.08rem; min-width:0; }
.external-map-copy strong { font-size:.84rem; }
.external-map-copy small { color:var(--muted); font-weight:400; }
.external-link-mark { margin-left:auto; color:var(--muted); font-size:1rem; }
.device-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:.8rem; }
.device-card { padding:1rem; border:1px solid var(--border); border-radius:12px; background:var(--panel); min-width:0; }
.device-card.selected { border-color:var(--blue); box-shadow:0 0 0 1px color-mix(in srgb,var(--blue) 45%,transparent); }
.device-card-header { display:flex; justify-content:space-between; gap:.75rem; align-items:flex-start; margin-bottom:.8rem; }
.device-card-title { display:flex; align-items:flex-start; gap:.75rem; min-width:0; }
.device-card-title-copy { min-width:0; }
.device-card-icon { flex:0 0 auto; }
.device-card-title small { display:block; color:var(--muted); overflow-wrap:anywhere; }
.section-card-header { margin-bottom:.85rem; }
.section-card-title { margin:0; font-size:1.25rem; }
.device-card-header h3 { margin:0 0 .15rem; font-size:1.05rem; }
.device-status { display:inline-flex; align-items:center; gap:.35rem; border-radius:999px; padding:.28rem .55rem; font-size:.78rem; font-weight:750; white-space:nowrap; }
.device-status::before { content:""; width:.55rem; height:.55rem; border-radius:50%; background:currentColor; }
.device-status.online { color:var(--green); background:color-mix(in srgb,var(--green) 12%,transparent); }
.device-status.offline { color:var(--gray); background:color-mix(in srgb,var(--gray) 12%,transparent); }
.device-live { display:flex; justify-content:space-between; gap:1rem; align-items:baseline; padding:.75rem; border-radius:9px; background:var(--panel-strong); margin-bottom:.75rem; }
.device-live span { font-size:1.4rem; font-weight:780; font-variant-numeric:tabular-nums; }
.device-fields { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.55rem; }
.device-field { padding:.58rem; border-radius:8px; background:color-mix(in srgb,CanvasText 3%,transparent); min-width:0; }
.device-field strong { display:block; font-size:.72rem; text-transform:uppercase; letter-spacing:.035em; opacity:.72; margin-bottom:.2rem; }
.device-field span { display:block; overflow-wrap:anywhere; line-height:1.35; }
.device-field .field-value { display:block; font-weight:600; }
.device-field .field-detail { display:block; margin-top:.28rem; font-size:.78rem; line-height:1.4; font-weight:400; opacity:.76; }
.orientation-state { grid-column:1 / -1; display:grid; grid-template-columns:auto 1fr; gap:.8rem; align-items:center; padding:.85rem .95rem; border-radius:12px; border:1px solid color-mix(in srgb,currentColor 22%,transparent); background:color-mix(in srgb,currentColor 8%,transparent); }
.orientation-state::before { content:""; width:.8rem; height:.8rem; border-radius:50%; background:currentColor; box-shadow:0 0 0 5px color-mix(in srgb,currentColor 13%,transparent); }
.orientation-state.green { color:var(--green); }
.orientation-state.yellow { color:var(--yellow); }
.orientation-state.orange { color:#f59e0b; }
.orientation-state.blue { color:var(--blue); }
.orientation-state.red { color:var(--red); }
.orientation-state-copy strong { display:block; font-size:.78rem; text-transform:uppercase; letter-spacing:.04em; opacity:.78; }
.orientation-state-copy span { display:block; margin-top:.12rem; color:var(--text); font-size:1.04rem; font-weight:760; }
.orientation-state-copy small { display:block; margin-top:.12rem; color:var(--muted); }

.gmcmap-panel { margin-top:.75rem; padding:.72rem; border:1px solid color-mix(in srgb,var(--blue) 28%,var(--border)); border-radius:10px; background:color-mix(in srgb,var(--blue) 5%,transparent); }
.gmcmap-header { display:flex; justify-content:space-between; align-items:flex-start; gap:.75rem; margin-bottom:.65rem; }
.gmcmap-header > div { display:grid; gap:.18rem; min-width:0; }
.gmcmap-header small { color:var(--muted); line-height:1.35; }
.gmcmap-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.45rem; }
.gmcmap-grid > div { padding:.48rem; border-radius:8px; background:color-mix(in srgb,CanvasText 3%,transparent); min-width:0; }
.gmcmap-grid strong { display:block; font-size:.7rem; text-transform:uppercase; letter-spacing:.035em; opacity:.72; margin-bottom:.18rem; }
.gmcmap-grid span { display:block; overflow-wrap:anywhere; line-height:1.3; }
.gmcmap-acpm-help { display:block; margin-top:.6rem; color:var(--muted); line-height:1.4; }
.gmcmap-error { margin-top:.55rem; padding:.5rem .58rem; border-radius:8px; background:color-mix(in srgb,var(--red) 10%,transparent); color:color-mix(in srgb,var(--red) 80%,CanvasText); line-height:1.35; overflow-wrap:anywhere; }
.device-status.waiting { color:var(--blue); background:color-mix(in srgb,var(--blue) 12%,transparent); }
.device-status.error { color:var(--red); background:color-mix(in srgb,var(--red) 12%,transparent); }
.technical-value { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.78rem; }
.device-select { margin-top:.8rem; }
.status-zone { display: grid; gap: .8rem; margin-bottom: 1rem; }
.status-summary { display: grid; grid-template-columns: repeat(4,minmax(0,1fr)); gap: .65rem; }
.status-item { padding: .78rem; border-radius: 10px; background: var(--panel); border-left: 4px solid var(--gray); min-width: 0; }
.status-item.green { border-left-color: var(--green); }
.status-item.yellow { border-left-color: var(--yellow); }
.status-item.red { border-left-color: var(--red); }
.status-item.blue { border-left-color: var(--blue); }
.status-item strong { display: block; font-size: .78rem; text-transform: uppercase; letter-spacing: .035em; opacity: .75; margin-bottom: .25rem; }
.status-item .status-value { font-size: 1.32rem; font-weight: 720; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
.status-item small { display: block; margin-top: .24rem; }
.metrics { display: grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap: .65rem; }
.metric { padding: .78rem; border-radius: 9px; background: var(--panel); min-width: 0; }
.metric.priority { background: var(--panel-strong); border: 1px solid var(--border); }
.metric strong { display: block; font-size: .86rem; margin-bottom: .28rem; }
.metric .value { font-size: 1.34rem; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
.metric small { display: block; margin-top: .3rem; line-height: 1.35; }
.interpretation { margin-top: .36rem; font-size: .82rem; font-weight: 650; }
.interpretation.good { color: var(--green); }
.interpretation.notice { color: color-mix(in srgb, var(--yellow) 80%, CanvasText); }
.interpretation.alert { color: var(--red); }
.interpretation.neutral { color: var(--muted); }
.traffic-card { display: grid; grid-template-columns: auto 1fr; gap: 1rem; align-items: center; padding: 1.05rem; border-radius: 14px; border: 1px solid var(--border); background: var(--panel-strong); }
.traffic-lights { display: flex; gap: .55rem; padding: .65rem; border-radius: 999px; background: color-mix(in srgb, CanvasText 14%, transparent); }
.traffic-light { width: 2.45rem; height: 2.45rem; border-radius: 50%; opacity: .18; box-shadow: inset 0 0 0 2px color-mix(in srgb, Canvas 35%, transparent); }
.traffic-light.green { background: var(--green); }
.traffic-light.yellow { background: var(--yellow); }
.traffic-light.red { background: var(--red); }
.traffic-light.active { opacity: 1; box-shadow: 0 0 0 3px color-mix(in srgb, Canvas 75%, transparent), 0 0 22px currentColor; }
.traffic-status strong { display: block; font-size: .85rem; text-transform: uppercase; letter-spacing: .035em; opacity: .75; }
.traffic-status .headline { font-size: 1.75rem; font-weight: 760; margin: .12rem 0 .2rem; }
.traffic-status small { display: block; line-height: 1.4; }
.learning { margin-top: .7rem; }
.progress-track { height: .65rem; background: color-mix(in srgb, CanvasText 14%, transparent); border-radius: 999px; overflow: hidden; }
.progress-bar { height: 100%; background: var(--blue); border-radius: inherit; }
.progress-copy { display: flex; justify-content: space-between; gap: .75rem; margin-top: .35rem; font-size: .82rem; }

.assessment-card { border:1px solid var(--border); border-radius:14px; padding:1rem; background:var(--panel-strong); }
.assessment-card.absolute { border-color:color-mix(in srgb,var(--green) 55%,var(--border)); }
.assessment-card.baseline { border-color:color-mix(in srgb,var(--blue) 55%,var(--border)); }
.assessment-header { display:flex; gap:.75rem; align-items:flex-start; margin-bottom:.85rem; }
.assessment-icon { width:2.15rem; height:2.15rem; display:grid; place-items:center; border-radius:10px; font-size:1.25rem; background:var(--panel); flex:0 0 auto; }
.assessment-title { font-size:1.05rem; font-weight:800; text-transform:uppercase; letter-spacing:.03em; }
.assessment-subtitle { margin-top:.15rem; color:var(--muted); line-height:1.35; }
.assessment-grid { display:grid; grid-template-columns:minmax(220px,1.2fr) repeat(3,minmax(140px,1fr)); gap:.65rem; }
.assessment-grid.baseline-grid { grid-template-columns:minmax(270px,1.55fr) repeat(4,minmax(125px,1fr)); }
#adaptive-background .collapsible-card-body > .assessment-grid { grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; margin-bottom:1rem; }
#adaptive-background .collapsible-card-body > .assessment-grid .assessment-card { padding:1.15rem; min-width:0; }
#adaptive-background .collapsible-card-body > .assessment-grid .assessment-card h3 { margin:0 0 .8rem; }
#adaptive-background .collapsible-card-body > .assessment-grid .orientation-state { margin-bottom:.85rem; padding:1rem; }
#adaptive-background .collapsible-card-body > .metrics { grid-template-columns:repeat(4,minmax(0,1fr)); gap:.9rem; }
#adaptive-background .collapsible-card-body > .metrics .metric { padding:.9rem; }
#cosmic-influence .collapsible-card-body > .assessment-grid { grid-template-columns:minmax(0,1fr); gap:1rem; margin-bottom:1rem; }
#cosmic-influence .collapsible-card-body > .assessment-grid .assessment-card { padding:1.15rem; min-width:0; }
#cosmic-influence .collapsible-card-body > .assessment-grid .assessment-card h3 { margin:0 0 .8rem; }
#cosmic-influence .collapsible-card-body > .assessment-grid .orientation-state { margin-bottom:.2rem; padding:1rem; }
#cosmic-influence .collapsible-card-body > .metrics { grid-template-columns:repeat(3,minmax(0,1fr)); gap:1rem; margin-top:.1rem; }
#cosmic-influence .collapsible-card-body > .metrics .metric { padding:.95rem; min-height:100%; }
#cosmic-influence .note { margin-top:1rem; }
.assessment-primary, .assessment-stat { padding:.85rem; border-radius:11px; background:var(--panel); border:1px solid color-mix(in srgb,CanvasText 12%,transparent); min-width:0; }
.assessment-primary { display:grid; grid-template-columns:auto minmax(0,1fr); gap:.8rem; align-items:center; }
.assessment-grid.baseline-grid .assessment-primary { padding-right:1.15rem; }
.status-orb { width:4.6rem; height:4.6rem; border-radius:50%; background:var(--gray); box-shadow:0 0 0 5px color-mix(in srgb,Canvas 75%,transparent),0 8px 22px color-mix(in srgb,CanvasText 22%,transparent); }
.status-orb.green { background:var(--green); }.status-orb.yellow { background:var(--yellow); }.status-orb.red { background:var(--red); }.status-orb.blue { background:var(--blue); }.status-orb.orange { background:#f59e0b; }
.assessment-state { font-size:1.55rem; font-weight:800; line-height:1.05; }
.stability-status { display:flex; align-items:center; gap:.5rem; margin-top:.45rem; line-height:1.25; }
.stability-dot { width:.78rem; height:.78rem; border-radius:50%; flex:0 0 auto; background:var(--blue); box-shadow:0 0 0 3px color-mix(in srgb,currentColor 15%,transparent); }
.stability-dot.green { background:var(--green); color:var(--green); }
.stability-dot.yellow { background:var(--yellow); color:var(--yellow); }
.stability-dot.orange { background:#f59e0b; color:#f59e0b; }
.stability-dot.red { background:var(--red); color:var(--red); }
.stability-dot.blue { background:var(--blue); color:var(--blue); }
.stability-grid { grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; align-items:stretch; }
.stability-grid .assessment-card { min-width:0; padding:1.05rem; }
.stability-meta { display:grid; gap:.32rem; margin-top:.65rem; line-height:1.35; font-variant-numeric:tabular-nums; }
.stability-meta-line { display:block; white-space:nowrap; }
.gap-status { display:inline-flex; align-items:center; margin-left:.38rem; padding:.08rem .42rem; border-radius:999px; font-size:.72rem; font-weight:800; line-height:1.25; vertical-align:baseline; border:1px solid currentColor; }
.gap-status.warning { color:color-mix(in srgb,var(--yellow) 72%,CanvasText); background:color-mix(in srgb,var(--yellow) 14%,Canvas); }
.gap-status.critical { color:var(--red); background:color-mix(in srgb,var(--red) 10%,Canvas); }
.assessment-state.green { color:var(--green); }.assessment-state.yellow { color:color-mix(in srgb,var(--yellow) 78%,CanvasText); }.assessment-state.red { color:var(--red); }.assessment-state.blue { color:var(--blue); }.assessment-state.orange { color:#f59e0b; }
.assessment-detail { margin-top:.3rem; line-height:1.4; }
.assessment-stat strong { display:block; font-size:.76rem; text-transform:uppercase; letter-spacing:.035em; opacity:.72; margin-bottom:.25rem; }
.assessment-stat .big { font-size:1.28rem; font-weight:760; font-variant-numeric:tabular-nums; overflow-wrap:anywhere; }
.assessment-note { margin-top:.75rem; padding:.7rem .8rem; border-radius:9px; background:color-mix(in srgb,var(--blue) 8%,var(--panel)); line-height:1.45; }
.assessment-note strong { display:block; margin-bottom:.15rem; }
.combined-interpretation { display:grid; grid-template-columns:auto 1fr; gap:.8rem; align-items:start; border:1px solid color-mix(in srgb,#8b5cf6 55%,var(--border)); border-radius:14px; padding:1rem; background:color-mix(in srgb,#8b5cf6 7%,var(--panel)); margin-bottom:1rem; }
.combined-interpretation .icon { font-size:1.55rem; }
.combined-interpretation strong { display:block; margin-bottom:.25rem; text-transform:uppercase; letter-spacing:.03em; }
.recommendation-card { display:grid; grid-template-columns:auto minmax(0,1fr); gap:.6rem; align-items:start; margin:1.05rem 0 1rem; }
.recommendation-card .icon { font-size:1.15rem; line-height:1.2; }
.recommendation-card strong { display:block; }
.recommendation-card .headline { margin-top:.08rem; font-weight:720; }
.recommendation-card .detail { margin-top:.08rem; line-height:1.4; }
.cosmic-reasons { margin:.85rem 0 0; }
.cosmic-reasons .compact-list { margin:0; }
.legend-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.8rem; }
.legend-card { padding:.8rem; border-radius:10px; background:var(--panel); }
.legend-row { display:flex; align-items:center; gap:.5rem; margin:.38rem 0; }
.legend-dot { width:.75rem; height:.75rem; border-radius:50%; background:var(--gray); flex:0 0 auto; }
.legend-dot.green{background:var(--green)}.legend-dot.yellow{background:var(--yellow)}.legend-dot.orange{background:#f59e0b}.legend-dot.red{background:var(--red)}.legend-dot.blue{background:var(--blue)}
details.analysis-group, details.download-group { border: 1px solid var(--border); border-radius: 11px; margin-top: .8rem; background: color-mix(in srgb, CanvasText 2.5%, transparent); }
details.assessment-legend { margin-bottom: 1rem; }
details > summary { cursor: pointer; list-style: none; padding: .9rem 1rem; font-weight: 720; display: flex; justify-content: space-between; gap: 1rem; align-items: center; min-height: 3.15rem; }
details > summary::-webkit-details-marker { display: none; }
details > summary::after { content: "+"; font-size: 1.3rem; line-height: 1; opacity: .65; }
details[open] > summary::after { content: "−"; }
.summary-copy { display: grid; gap: .12rem; }
.summary-copy small { font-weight: 400; }
details.collapsible-card { border:1px solid var(--border); border-radius:14px; margin-bottom:1rem; overflow:hidden; }
details.collapsible-card > summary { padding:1rem 1.2rem; min-height:auto; gap:.7rem; }
details.collapsible-card > summary h2 { margin:0; font-size:1.25rem; }
details.collapsible-card > .collapsible-card-body { padding:0 1.2rem 1rem; }
details.collapsible-card:not([open]) > summary { border-radius:inherit; }
.primary-dashboard { display:flex; flex-direction:column; }
.collapsible-card.pinned-card { border-color:color-mix(in srgb,var(--blue) 62%,var(--border)); box-shadow:0 4px 14px color-mix(in srgb,var(--blue) 12%,transparent); }
.card-summary-actions { display:inline-flex; align-items:center; gap:.35rem; margin-left:auto; }
.card-summary-actions button { width:2.2rem; min-height:2.2rem; padding:0; border-radius:50%; font-size:1rem; background:transparent; box-shadow:none; }
.card-pin[aria-pressed="true"] { color:#f59e0b; border-color:#f59e0b; background:color-mix(in srgb,#f59e0b 10%,Canvas); }
.card-help-popover { white-space:pre-line; position:fixed; z-index:1000; max-width:min(32rem,calc(100vw - 2rem)); padding:.8rem .9rem; border:1px solid var(--border); border-radius:10px; background:Canvas; color:CanvasText; box-shadow:0 10px 28px color-mix(in srgb,CanvasText 24%,transparent); line-height:1.45; }
.inline-help { margin-top:.75rem; border:1px solid var(--border); border-radius:10px; background:var(--panel); }
.inline-help > summary { padding:.72rem .85rem; min-height:auto; }
.status-strip { position:static; display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.55rem; padding:.6rem; margin:0 0 1rem; border:1px solid var(--border); border-radius:14px; background:color-mix(in srgb,Canvas 96%,transparent); box-shadow:0 4px 16px color-mix(in srgb,CanvasText 10%,transparent); }
.status-strip-item { display:grid; grid-template-columns:auto minmax(0,1fr); gap:.55rem; align-items:start; min-width:0; min-height:4rem; padding:.65rem .7rem; border-radius:10px; text-decoration:none; color:CanvasText; background:var(--panel); }
.status-strip-item strong,.status-strip-item small { display:block; white-space:normal; overflow-wrap:anywhere; line-height:1.28; }
.status-strip-item strong { font-size:.86rem; }
.status-strip-item small { margin-top:.16rem; font-size:.76rem; }
.status-dot { width:.72rem; height:.72rem; border-radius:50%; background:var(--gray); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--gray) 16%,transparent); }
.status-strip-item.ok .status-dot { background:var(--green); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--green) 16%,transparent); }
.status-strip-item.warning .status-dot { background:var(--yellow); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--yellow) 16%,transparent); }
.status-strip-item.error .status-dot { background:var(--red); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--red) 16%,transparent); }
.status-strip-item.waiting .status-dot { background:var(--blue); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--blue) 16%,transparent); }
.dashboard-controls { position:sticky; top:0; z-index:50; display:flex; justify-content:space-between; align-items:center; gap:.75rem; flex-wrap:nowrap; margin:0 0 1rem; padding:.65rem .8rem; border:1px solid var(--border); border-radius:12px; background:color-mix(in srgb,Canvas 96%,transparent); box-shadow:0 3px 12px color-mix(in srgb,CanvasText 8%,transparent); backdrop-filter:blur(14px); }
.background-profile-values { display:inline-block; margin-top:.12rem; }
.jump-links,.dashboard-actions { display:flex; gap:.45rem; flex-wrap:nowrap; align-items:center; }
.jump-links { flex:1 1 auto; min-width:0; overflow-x:auto; padding:.08rem 0; scrollbar-width:thin; }
.dashboard-actions { flex:0 0 auto; }
.jump-links a,.compact-action { width:auto; min-height:2rem; padding:.38rem .7rem; border-radius:999px; font-size:.82rem; line-height:1.2; white-space:nowrap; text-decoration:none; color:CanvasText; border:1px solid var(--border); background:Canvas; }
.jump-links a.active { border-color:var(--blue); background:color-mix(in srgb,var(--blue) 10%,Canvas); font-weight:750; }
.empty-state { display:grid; justify-items:center; text-align:center; gap:.45rem; padding:1.5rem 1rem; border:1px dashed var(--border); border-radius:12px; background:var(--panel); }
.empty-state-icon { font-size:1.8rem; }
.empty-state.scanning .empty-state-icon { animation:pulse 1.4s ease-in-out infinite; }
@keyframes pulse { 50% { opacity:.35; transform:scale(.9); } }
.device-card { position:relative; border-left:5px solid var(--gray); overflow:hidden; }
.device-card.device-320 { border-left-color:#2563eb; }
.device-card.device-500 { border-left-color:#7c3aed; }
.device-card.device-320 .device-card-icon { background:color-mix(in srgb,#2563eb 12%,var(--panel)); color:#2563eb; }
.device-card.device-500 .device-card-icon { background:color-mix(in srgb,#7c3aed 12%,var(--panel)); color:#7c3aed; }
.device-card-icon { min-width:3.2rem; font-size:.82rem; font-weight:900; letter-spacing:-.03em; }
#devices,#radiation-intelligence,#analysis,#history,#workflow,#reports,#maintenance { scroll-margin-top:5rem; }
.analysis-section { scroll-margin-top:5rem; }
.analysis-heading { display:flex; align-items:center; gap:.65rem; margin-bottom:.8rem; }
.analysis-heading h2 { margin:0; min-width:0; overflow-wrap:anywhere; }
.analysis-device-badge { width:auto; min-width:3.2rem; height:2.2rem; padding:0 .65rem; display:grid; place-items:center; flex:0 0 auto; border-radius:10px; font-size:.82rem; font-weight:900; letter-spacing:-.03em; background:var(--panel); color:var(--muted); }
.analysis-device-badge.device-320 { background:color-mix(in srgb,#2563eb 12%,var(--panel)); color:#2563eb; }
.analysis-device-badge.device-500 { background:color-mix(in srgb,#7c3aed 12%,var(--panel)); color:#7c3aed; }
.device-card-title-copy small,.technical-value { overflow-wrap:anywhere; word-break:break-word; }
.device-alerts { display:grid; gap:.45rem; margin:.7rem 0; }
.device-alert { display:grid; gap:.15rem; padding:.58rem .65rem; border-radius:9px; border:1px solid var(--border); font-size:.84rem; }
.device-alert.warning { border-color:color-mix(in srgb,var(--yellow) 62%,var(--border)); background:color-mix(in srgb,var(--yellow) 9%,var(--panel)); }
.device-alert.error { border-color:color-mix(in srgb,var(--red) 62%,var(--border)); background:color-mix(in srgb,var(--red) 8%,var(--panel)); }
.device-alert.info { border-color:color-mix(in srgb,var(--blue) 52%,var(--border)); background:color-mix(in srgb,var(--blue) 7%,var(--panel)); }
.device-ok { display:flex; align-items:center; gap:.4rem; margin:.65rem 0; padding:.5rem .6rem; border-radius:9px; color:color-mix(in srgb,var(--green) 78%,CanvasText); background:color-mix(in srgb,var(--green) 7%,var(--panel)); font-size:.84rem; font-weight:650; }
.form-actions { display:flex; gap:.45rem; align-items:end; }
.form-actions button { min-width:9rem; }
.custom-form .form-grid { grid-template-columns:minmax(0,1.35fr) minmax(8rem,.65fr); }
.custom-form .form-actions { grid-column:1 / -1; display:grid; grid-template-columns:minmax(10rem,16rem); justify-content:end; align-items:stretch; }
.custom-form .form-actions button { width:100%; min-width:0; }
.custom-form label { min-width:0; }
.restore-preview { padding:.7rem .8rem; border:1px dashed var(--border); border-radius:9px; background:var(--panel); line-height:1.45; }
.restore-preview-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:.45rem; margin-top:.55rem; }
.restore-preview-grid div { padding:.5rem; border-radius:8px; background:Canvas; }
.restore-preview-grid strong,.restore-preview-grid span { display:block; }
.group-body { display:grid; gap:.9rem; padding: 0 1rem 1rem; }
.group-body > * { min-width:0; }
.group-body > [data-analysis-tier] > h3:first-child, .group-body > h3:first-child { margin-top:0; }
.formulas { margin: .8rem 0 0; padding-left: 1.2rem; }
.formulas li { margin: .35rem 0; line-height: 1.45; }
.actions { display: grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap: .65rem; }
.download-columns { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: .8rem; }
.download-card { padding: .9rem; border-radius: 10px; background: var(--panel); }
.download-card h3 { margin-top: 0; }
a.button, button {
  display:inline-flex;
  align-items:center;
  justify-content:center;
  box-sizing:border-box;
  width:100%;
  min-height:2.65rem;
  padding:.62rem 1rem;
  border-radius:999px;
  border:1px solid color-mix(in srgb,CanvasText 20%,transparent);
  text-align:center;
  text-decoration:none;
  background:Canvas;
  color:CanvasText;
  cursor:pointer;
  font:inherit;
  font-weight:560;
  line-height:1.2;
  box-shadow:0 1px 2px color-mix(in srgb,CanvasText 8%,transparent);
  transition:background .15s ease,border-color .15s ease,color .15s ease,box-shadow .15s ease,transform .12s ease;
  -webkit-tap-highlight-color:transparent;
}
a.button:hover, button:hover {
  background:color-mix(in srgb,var(--blue) 7%,Canvas);
  border-color:color-mix(in srgb,var(--blue) 48%,var(--border));
  box-shadow:0 2px 6px color-mix(in srgb,CanvasText 12%,transparent);
}
a.button:active, button:active { transform:translateY(1px); box-shadow:0 1px 2px color-mix(in srgb,CanvasText 8%,transparent); }
a.button:focus-visible, button:focus-visible { outline:3px solid color-mix(in srgb,var(--blue) 28%,transparent); outline-offset:2px; }
a.button.primary, button.primary {
  background:color-mix(in srgb,var(--blue) 11%,Canvas);
  border-color:var(--blue);
  color:color-mix(in srgb,var(--blue) 80%,CanvasText);
  font-weight:750;
  box-shadow:0 1px 3px color-mix(in srgb,var(--blue) 20%,transparent);
}
a.button.primary:hover, button.primary:hover { background:color-mix(in srgb,var(--blue) 17%,Canvas); box-shadow:0 3px 8px color-mix(in srgb,var(--blue) 24%,transparent); }
button.danger, a.button.danger {
  background:color-mix(in srgb,var(--red) 8%,Canvas);
  border-color:color-mix(in srgb,var(--red) 72%,var(--border));
  color:color-mix(in srgb,var(--red) 82%,CanvasText);
  font-weight:750;
}
button.danger:hover, a.button.danger:hover { background:color-mix(in srgb,var(--red) 14%,Canvas); box-shadow:0 3px 8px color-mix(in srgb,var(--red) 20%,transparent); }
button:disabled, a.button[aria-disabled="true"] { opacity:.5; cursor:not-allowed; transform:none; box-shadow:none; }
form { display: grid; gap: .65rem; }
.custom-periods { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: .8rem; }
.custom-form { padding: .9rem; border-radius: 10px; background: var(--panel); }
.form-grid { display: grid; grid-template-columns: 1fr 1fr auto; gap: .6rem; align-items: end; }
label { display: grid; gap: .25rem; font-size: .9rem; }
input, select { width: 100%; font: inherit; padding: .65rem; border-radius: 7px; border: 1px solid color-mix(in srgb, CanvasText 28%, transparent); background: Canvas; color: CanvasText; }
small { opacity: .8; }
.note { padding: .7rem .8rem; border-radius: 8px; background: var(--panel); line-height: 1.45; }
.relative-factor-note { margin-top: 1rem; }
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
body[data-analysis-level="summary"] .advanced-only { display:none !important; }
.quality-reasons { margin:.55rem 0 0; padding-left:1.15rem; font-size:.84rem; }
.database-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:.65rem; }
.restore-form input[type=file] { min-height:2.85rem; }
table { width: 100%; border-collapse: collapse; margin-top: .5rem; min-width: 520px; }
th, td { text-align: left; padding: .55rem .6rem; border-bottom: 1px solid color-mix(in srgb, CanvasText 16%, transparent); font-variant-numeric: tabular-nums; }
.analysis-level-panel { display:flex; align-items:center; justify-content:space-between; gap:1.15rem; padding:.9rem 1rem; margin-bottom:1rem; border:1px solid var(--border); border-radius:12px; background:var(--panel); }
.analysis-level-panel > div:first-child { display:grid; gap:.18rem; min-width:0; flex:1 1 22rem; }
.analysis-level-copy { display:grid; gap:.18rem; min-width:0; flex:1 1 22rem; }
.analysis-level-copy small { color:CanvasText; line-height:1.4; font-size:.88rem; }
.analysis-level-copy > span { color:var(--muted); line-height:1.35; font-size:.76rem; }
.analysis-level-buttons { display:flex; align-items:center; gap:.5rem; flex:0 0 auto; flex-wrap:nowrap; }
.analysis-level-button { width:auto; min-height:2.4rem; padding:.48rem .78rem; border-radius:999px; display:inline-flex; align-items:center; gap:.42rem; white-space:nowrap; background:Canvas; color:CanvasText; box-shadow:none; }
.analysis-level-button[aria-pressed="true"] { border-color:color-mix(in srgb,CanvasText 65%,transparent); background:var(--panel-strong); font-weight:760; box-shadow:inset 0 0 0 1px color-mix(in srgb,CanvasText 12%,transparent); }
.analysis-level-symbol { min-width:1.05rem; text-align:center; font-weight:800; font-size:1rem; }
body[data-analysis-level="summary"] [data-analysis-tier="analysis"],
body[data-analysis-level="summary"] [data-analysis-tier="expert"],
body[data-analysis-level="analysis"] [data-analysis-tier="expert"] { display:none !important; }
.historical-development { margin-top:.85rem; }
.historical-trends { margin-bottom:.8rem; }
.historical-chart { margin:.8rem 0; padding:.8rem; border:1px solid var(--border); border-radius:10px; background:color-mix(in srgb,CanvasText 2%,transparent); }
.historical-chart svg { display:block; width:100%; height:13rem; overflow:visible; }
.chart-axis { stroke:color-mix(in srgb,CanvasText 28%,transparent); stroke-width:.45; }
.chart-line { fill:none; stroke:CanvasText; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; }
.historical-chart figcaption { display:grid; grid-template-columns:1fr auto 1fr; gap:.7rem; align-items:center; font-size:.78rem; color:var(--muted); }
.historical-chart figcaption span:last-child { text-align:right; }
.historical-chart figcaption strong { color:CanvasText; text-align:center; }
.compact-list { margin:.2rem 0 .75rem; padding-left:1.2rem; display:grid; gap:.3rem; }
.fleet-summary { margin-bottom:.75rem; }
@media (max-width: 800px) {
  .page-scroll { padding: calc(.75rem + env(safe-area-inset-top)) calc(.75rem + env(safe-area-inset-right)) calc(.75rem + env(safe-area-inset-bottom)) calc(.75rem + env(safe-area-inset-left)); }
  .analysis-level-panel { align-items:stretch; flex-direction:column; }
  .analysis-level-panel > div:first-child { flex:0 0 auto; }
  .analysis-level-copy { flex:0 0 auto; }
  .analysis-level-buttons { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); }
  .analysis-level-button { justify-content:center; min-width:0; }
  .status-summary { grid-template-columns: repeat(2,minmax(0,1fr)); }
  .assessment-grid, .assessment-grid.baseline-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
  #adaptive-background .collapsible-card-body > .assessment-grid { grid-template-columns:repeat(2,minmax(0,1fr)); gap:.85rem; }
  #adaptive-background .collapsible-card-body > .metrics { grid-template-columns:repeat(2,minmax(0,1fr)); }
  #cosmic-influence .collapsible-card-body > .assessment-grid { grid-template-columns:1fr; gap:.85rem; }
  #cosmic-influence .collapsible-card-body > .metrics { grid-template-columns:repeat(2,minmax(0,1fr)); gap:.85rem; }
  .assessment-primary { grid-column:1 / -1; }
  .legend-grid { grid-template-columns:1fr; }
  .download-columns, .custom-periods { grid-template-columns: 1fr; }
  .dashboard-controls { position:static; flex-wrap:wrap; backdrop-filter:none; }
  .jump-links,.dashboard-actions { flex-wrap:wrap; overflow:visible; }
  .status-strip { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .form-grid { grid-template-columns: 1fr; }
  .custom-form .form-grid { grid-template-columns:1fr; }
  .custom-form .form-actions { grid-column:auto; }
  .form-actions { align-items:stretch; }
}
@media (max-width: 620px) {
  .report-format-guide { grid-template-columns:1fr; }
  .header-intro { overflow-x:hidden; }
  .analysis-level-button, a.button, button { min-height:2.75rem; }
  .header-resource-links { grid-template-columns:1fr; }
  .language-switcher { width:100%; min-width:0; flex-wrap:nowrap; overflow-x:auto; overflow-y:hidden; padding:.08rem 0 .3rem; scrollbar-width:thin; -webkit-overflow-scrolling:touch; }
  .language-switcher a { flex:0 0 auto; min-height:2.5rem; }
}
@media (max-width: 520px) {
  header, section { padding: .9rem; border-radius: 11px; }
  .analysis-level-buttons { grid-template-columns:1fr; }
  .analysis-level-button { justify-content:flex-start; }
  .historical-chart svg { height:10rem; }
  .historical-chart figcaption { grid-template-columns:1fr 1fr; }
  .historical-chart figcaption strong { grid-column:1 / -1; grid-row:1; }
  .location-details-body { padding:0 .75rem .75rem; }
  .traffic-card { grid-template-columns: 1fr; }
  .traffic-lights { width: fit-content; }
  .traffic-status .headline { font-size: 1.45rem; }
  .status-summary { grid-template-columns: repeat(2,minmax(0,1fr)); }
  .status-item .status-value { font-size: 1.12rem; }
  .metrics { grid-template-columns: 1fr; }
  .device-grid, .device-fields { grid-template-columns: 1fr; }
  .status-strip { grid-template-columns:1fr; }
  .status-strip-item strong,.status-strip-item small { white-space:normal; }
  .dashboard-controls { align-items:stretch; }
  .jump-links,.dashboard-actions { width:100%; }
  .jump-links a { flex:1 1 auto; text-align:center; }
  .dashboard-actions .compact-action { flex:1 1 auto; }
  .card-summary-actions { gap:.2rem; }
  .card-summary-actions button { width:2rem; min-height:2rem; }
  .device-card-header { align-items:flex-start; }
  .device-card-title { min-width:0; }
  .device-card-title-copy { min-width:0; }
  .device-card-title-copy h3,.device-card-title-copy small { overflow-wrap:anywhere; word-break:break-word; }
  .device-select { width:100%; }
  .form-actions { flex-direction:column; }
  .form-actions button { width:100%; min-width:0; }
  #adaptive-background .collapsible-card-body > .assessment-grid, #adaptive-background .collapsible-card-body > .metrics, #cosmic-influence .collapsible-card-body > .metrics { grid-template-columns:1fr; }
  .gmcmap-grid { grid-template-columns: 1fr; }
  .assessment-grid, .assessment-grid.baseline-grid { grid-template-columns:1fr; }
  #adaptive-background .collapsible-card-body > .assessment-grid { grid-template-columns:1fr; }
  #cosmic-influence .collapsible-card-body > .assessment-grid { grid-template-columns:1fr; }
  .assessment-primary { grid-column:auto; grid-template-columns:auto minmax(0,1fr); }
  .assessment-state { font-size:1.35rem; }
  .status-orb { width:4rem; height:4rem; }
  details > summary { padding: .85rem; }
  details.collapsible-card > summary { padding:.9rem; }
  details.collapsible-card > .collapsible-card-body { padding:0 .9rem .9rem; }
  .group-body { display:grid; gap:.85rem; padding: 0 .85rem .85rem; }
  main, header, section, .report-header, .header-intro, .header-resource-links,
  .analysis-section, .status-zone, .status-summary, .status-item, .assessment-card,
  .orientation-state, details.collapsible-card, details.collapsible-card > summary {
    min-width:0; max-width:100%;
  }
  h1, h2, h3, p, strong, small, summary { overflow-wrap:anywhere; word-break:break-word; }
  .header-intro h1 { font-size:1.5rem; overflow-wrap:normal; word-break:normal; hyphens:auto; }
  .assessment-header > div, .assessment-primary > div { min-width:0; max-width:100%; }
  .assessment-title, .assessment-subtitle, .assessment-state { overflow-wrap:anywhere; word-break:break-word; }
  .actions { grid-template-columns:1fr; }
}
.report-format-guide { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.65rem; margin:.7rem 0 1rem; }
.report-format-item { display:grid; gap:.18rem; min-width:0; padding:.72rem .78rem; border:1px solid var(--border); border-radius:10px; background:color-mix(in srgb,CanvasText 3%,transparent); }
.report-format-item strong { font-size:.84rem; }
.report-format-item small { color:var(--muted); line-height:1.35; }
.report-target-card{display:grid;gap:.45rem;padding:.85rem 1rem;margin:.85rem 0 1rem;border:1px solid var(--border);border-radius:11px;background:var(--panel)}
.report-target-card label{display:grid;gap:.4rem}.report-target-card select{max-width:32rem}
@media (max-width:620px) { .report-format-guide { grid-template-columns:1fr; } }
.history-management-status { display:grid; grid-template-columns:auto minmax(0,1fr); gap:.7rem; align-items:start; margin:.75rem 0 1rem; padding:.8rem .9rem; border:1px solid var(--border); border-radius:10px; background:var(--panel); }
.history-management-status strong,.history-management-status small { display:block; }
.history-management-status small { margin-top:.18rem; color:var(--muted); }
.history-management-status.enabled { border-color:color-mix(in srgb,var(--yellow) 55%,var(--border)); background:color-mix(in srgb,var(--yellow) 8%,Canvas); }
.history-management-status.enabled .status-dot { background:var(--yellow); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--yellow) 16%,transparent); margin-top:.25rem; }
.history-management-status.disabled .status-dot { background:var(--green); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--green) 16%,transparent); margin-top:.25rem; }
.history-management-tool { margin-top:.75rem; }
.danger-zone{margin-top:1.2rem;padding:1rem;border:2px solid #b3261e;border-radius:12px;background:rgba(179,38,30,.08)}
.danger-zone h3{color:#b3261e}.danger-zone form{display:grid;gap:.7rem;max-width:38rem}.danger{background:#b3261e!important;color:#fff!important;border-color:#b3261e!important}
"""

DASHBOARD_CSS += r"""
.analysis-result-summary { display:grid; gap:.55rem; margin-bottom:.8rem; }
.analysis-action { padding:.65rem .75rem; border-radius:9px; background:var(--panel); line-height:1.45; }
.analysis-action strong { margin-right:.25rem; }
"""


def render_dashboard_script(*, selected_serial: str, language: str, translator: TranslatorLike) -> str:
    t = translator
    return f"""
(() => {{
  const analysisDevice = {json.dumps(selected_serial)};
  const uiStorageKey = 'gmc-dashboard-usability-v1';
  const uiText = {{
    previewing: {json.dumps(t("Inspecting backup…"))},
    previewFailed: {json.dumps(t("Backup preview failed"))},
    noFile: {json.dumps(t("Select a SQLite backup file first."))},
    measurements: {json.dumps(t("Measurements"))},
    rawMeasurements: {json.dumps(t("Raw-data archive"))},
    annotations: {json.dumps(t("Annotations"))},
    devices: {json.dumps(t("Devices"))},
    dataPeriod: {json.dumps(t("Data period"))},
    schema: {json.dumps(t("Schema"))},
    fileSize: {json.dumps(t("File size"))},
    integrity: {json.dumps(t("Integrity"))},
    noData: {json.dumps(t("No data"))},
    backupReady: {json.dumps(t("Backup is compatible and ready to restore."))},
    expandAll: {json.dumps(t("Expand all"))},
    collapseAll: {json.dumps(t("Collapse all"))},
  }};

  function readJson(key, fallback) {{
    try {{ return JSON.parse(localStorage.getItem(key) || '') || fallback; }}
    catch (_error) {{ return fallback; }}
  }}
  function writeJson(key, value) {{
    try {{ localStorage.setItem(key, JSON.stringify(value)); }} catch (_error) {{}}
  }}
  const preferences = readJson(uiStorageKey, {{ cards: {{}}, groups: {{}}, pinned: [], reportForms: {{}}, lastSection: '', analysisLevel: '' }});
  const analysisLevelPanel = document.getElementById('analysis-level-panel');
  const allowedAnalysisLevels = new Set(['summary', 'analysis', 'expert']);
  function setAnalysisLevel(requestedLevel, persist = true) {{
    const fallback = analysisLevelPanel?.dataset.defaultLevel || 'analysis';
    const level = allowedAnalysisLevels.has(requestedLevel) ? requestedLevel : fallback;
    document.body.dataset.analysisLevel = level;
    let selectedDescription = '';
    document.querySelectorAll('.analysis-level-button').forEach((button) => {{
      const selected = button.dataset.analysisLevel === level;
      button.setAttribute('aria-pressed', String(selected));
      if (selected) selectedDescription = button.dataset.analysisDescription || '';
    }});
    const description = document.getElementById('analysis-level-description');
    if (description && selectedDescription) description.textContent = selectedDescription;
    if (persist) {{ preferences.analysisLevel = level; writeJson(uiStorageKey, preferences); }}
  }}
  setAnalysisLevel(preferences.analysisLevel || analysisLevelPanel?.dataset.defaultLevel || 'analysis', false);

  const toggleAllButton = document.getElementById('toggle-all-cards');
  const allDetailsSelector = 'details.collapsible-card, details.analysis-group, details.download-group';
  function updateToggleAllButton() {{
    if (!toggleAllButton) return;
    const details = [...document.querySelectorAll(allDetailsSelector)];
    const allOpen = details.length > 0 && details.every((item) => item.open);
    toggleAllButton.textContent = allOpen ? uiText.collapseAll : uiText.expandAll;
    toggleAllButton.setAttribute('aria-expanded', String(allOpen));
  }}
  function setAllCards(open) {{
    const details = [...document.querySelectorAll(allDetailsSelector)];
    preferences.cards = preferences.cards || {{}};
    preferences.groups = preferences.groups || {{}};
    details.forEach((item) => {{
      item.open = open;
      if (!item.id) return;
      if (item.classList.contains('collapsible-card')) preferences.cards[item.id] = open;
      else preferences.groups[item.id] = open;
    }});
    writeJson(uiStorageKey, preferences);
    updateToggleAllButton();
  }}
  function jumpToSection(selector) {{
    if (!selector || selector.charAt(0) !== '#') return false;
    const target = document.getElementById(selector.slice(1));
    if (!target) return false;
    if (target.classList.contains('advanced-only') && document.body.dataset.analysisLevel === 'summary') {{
      setAnalysisLevel('analysis');
    }}
    let parent = target.parentElement;
    while (parent) {{
      if (parent instanceof HTMLDetailsElement) parent.open = true;
      parent = parent.parentElement;
    }}
    const scroller = document.getElementById('page-scroll');
    if (scroller) {{
      const dashboardControls = document.getElementById('dashboard-controls');
      const stickyOffset = dashboardControls && getComputedStyle(dashboardControls).position === 'sticky'
        ? dashboardControls.getBoundingClientRect().height + 12
        : 12;
      const targetTop = target.getBoundingClientRect().top - scroller.getBoundingClientRect().top + scroller.scrollTop - stickyOffset;
      scroller.scrollTo({{ top: Math.max(0, targetTop), behavior: 'smooth' }});
    }} else {{
      target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
    preferences.lastSection = selector;
    writeJson(uiStorageKey, preferences);
    try {{
      const nextUrl = new URL(window.location.href);
      nextUrl.hash = selector;
      history.replaceState(null, '', nextUrl.pathname + nextUrl.search + nextUrl.hash);
    }} catch (_error) {{}}
    return true;
  }}
  document.addEventListener('click', (event) => {{
    const levelButton = event.target.closest('.analysis-level-button');
    if (levelButton) {{ event.preventDefault(); setAnalysisLevel(levelButton.dataset.analysisLevel || 'analysis'); return; }}
    const toggleAll = event.target.closest('#toggle-all-cards');
    if (toggleAll) {{
      event.preventDefault();
      const details = [...document.querySelectorAll(allDetailsSelector)];
      setAllCards(!(details.length > 0 && details.every((item) => item.open)));
      return;
    }}
    const jump = event.target.closest('.jump-links a[href^="#"], .status-strip a[href^="#"]');
    if (jump && jumpToSection(jump.getAttribute('href') || '')) event.preventDefault();
  }});

  document.querySelectorAll('a[href*="action=download"]').forEach((link) => {{
    const url = new URL(link.getAttribute('href'), window.location.href);
    url.searchParams.set('device', analysisDevice);
    url.searchParams.set('lang', {json.dumps(language)});
    link.setAttribute('href', url.pathname + url.search);
  }});
  document.querySelectorAll('form').forEach((form) => {{
    const actionInput = form.querySelector('input[name="action"][value="download"]');
    if (!actionInput || form.querySelector('input[name="device"]')) return;
    const input = document.createElement('input');
    input.type = 'hidden'; input.name = 'device'; input.value = analysisDevice; form.appendChild(input);
    if (!form.querySelector('input[name="lang"]')) {{
      const langInput = document.createElement('input');
      langInput.type = 'hidden'; langInput.name = 'lang'; langInput.value = {json.dumps(language)}; form.appendChild(langInput);
    }}
  }});

  const currentUrl = new URL(window.location.href);
  const savedDevice = preferences.device || '';
  const cssEscape = window.CSS && typeof window.CSS.escape === 'function'
    ? window.CSS.escape
    : (value) => String(value).replace(/[^a-zA-Z0-9_-]/g, (char) => `\\\\${{char}}`);
  if (!currentUrl.searchParams.has('device') && savedDevice && savedDevice !== analysisDevice && document.querySelector(`[data-device-serial="${{cssEscape(savedDevice)}}"]`)) {{
    currentUrl.searchParams.set('device', savedDevice);
    window.location.replace(currentUrl.toString());
    return;
  }}
  if (analysisDevice) {{ preferences.device = analysisDevice; writeJson(uiStorageKey, preferences); }}
  document.addEventListener('click', (event) => {{
    const deviceLink = event.target.closest('a.device-select');
    if (deviceLink) {{
      const card = deviceLink.closest('[data-device-serial]');
      if (card) {{ preferences.device = card.dataset.deviceSerial || ''; writeJson(uiStorageKey, preferences); }}
    }}
  }});

  const primaryDashboard = document.getElementById('primary-dashboard');
  function applyCardPreferences() {{
    const cards = [...document.querySelectorAll('details.collapsible-card')];
    cards.forEach((card, index) => {{
      if (!card.dataset.defaultOrder) card.dataset.defaultOrder = String(index);
      if (Object.prototype.hasOwnProperty.call(preferences.cards || {{}}, card.id)) card.open = Boolean(preferences.cards[card.id]);
      const pinned = (preferences.pinned || []).includes(card.id);
      card.classList.toggle('pinned-card', pinned);
      const pin = card.querySelector('.card-pin');
      if (pin) {{ pin.setAttribute('aria-pressed', String(pinned)); pin.textContent = pinned ? '★' : '☆'; }}
      if (card.parentElement === primaryDashboard) {{
        const pinIndex = (preferences.pinned || []).indexOf(card.id);
        card.style.order = pinned ? String(-100 + pinIndex) : card.dataset.defaultOrder;
      }}
    }});
  }}
  function applyGroupPreferences() {{
    document.querySelectorAll('details.analysis-group, details.download-group').forEach((group) => {{
      if (group.id && Object.prototype.hasOwnProperty.call(preferences.groups || {{}}, group.id)) {{
        group.open = Boolean(preferences.groups[group.id]);
      }}
    }});
  }}
  applyCardPreferences();
  applyGroupPreferences();
  updateToggleAllButton();

  document.addEventListener('toggle', (event) => {{
    const item = event.target;
    if (!(item instanceof HTMLDetailsElement)) return;
    if (item.classList.contains('collapsible-card')) {{
      preferences.cards = preferences.cards || {{}};
      preferences.cards[item.id] = item.open;
    }} else if (item.classList.contains('analysis-group') || item.classList.contains('download-group')) {{
      preferences.groups = preferences.groups || {{}};
      if (item.id) preferences.groups[item.id] = item.open;
    }} else {{
      return;
    }}
    writeJson(uiStorageKey, preferences);
    updateToggleAllButton();
  }}, true);

  let helpPopover = null;
  function closeHelp() {{ if (helpPopover) helpPopover.remove(); helpPopover = null; }}
  document.addEventListener('click', (event) => {{
    const pin = event.target.closest('.card-pin');
    if (pin) {{
      event.preventDefault(); event.stopPropagation();
      const card = pin.closest('details.collapsible-card');
      if (!card) return;
      preferences.pinned = preferences.pinned || [];
      const index = preferences.pinned.indexOf(card.id);
      if (index >= 0) preferences.pinned.splice(index, 1); else preferences.pinned.push(card.id);
      writeJson(uiStorageKey, preferences); applyCardPreferences(); return;
    }}
    const help = event.target.closest('.card-help');
    if (help) {{
      event.preventDefault(); event.stopPropagation(); closeHelp();
      const text = help.dataset.help || '';
      if (!text) return;
      const popover = document.createElement('div'); popover.className = 'card-help-popover'; popover.textContent = text;
      document.body.appendChild(popover); helpPopover = popover;
      const rect = help.getBoundingClientRect();
      const left = Math.min(window.innerWidth - popover.offsetWidth - 12, Math.max(12, rect.right - popover.offsetWidth));
      const top = Math.min(window.innerHeight - popover.offsetHeight - 12, rect.bottom + 8);
      popover.style.left = `${{left}}px`; popover.style.top = `${{top}}px`; return;
    }}
    if (helpPopover && !event.target.closest('.card-help-popover')) closeHelp();
  }});
  window.addEventListener('resize', closeHelp);
  const jumpLinks = [...document.querySelectorAll('.jump-links a')];
  if (!window.location.hash && preferences.lastSection) {{
    requestAnimationFrame(() => jumpToSection(preferences.lastSection));
  }}
  if ('IntersectionObserver' in window) {{
    const observer = new IntersectionObserver((entries) => {{
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      jumpLinks.forEach((link) => link.classList.toggle('active', link.getAttribute('href') === `#${{visible.target.id}}`));
    }}, {{ root: document.getElementById('page-scroll'), rootMargin: '-20% 0px -65% 0px', threshold: [0.05, 0.25] }});
    ['devices','radiation-intelligence','analysis','history','workflow','reports','maintenance'].forEach((id) => {{ const node = document.getElementById(id); if (node) observer.observe(node); }});
  }}

  document.querySelectorAll('form.report-preset-source').forEach((form) => {{
    const kind = form.dataset.presetKind || 'custom';
    const saved = (preferences.reportForms || {{}})[kind] || {{}};
    for (const [name, value] of Object.entries(saved)) {{ const field = form.elements.namedItem(name); if (field && typeof value === 'string') field.value = value; }}
    form.addEventListener('change', () => {{
      preferences.reportForms = preferences.reportForms || {{}};
      preferences.reportForms[kind] = Object.fromEntries([...new FormData(form).entries()].filter(([key]) => !['device','lang','action'].includes(key)).map(([key,value]) => [key,String(value)]));
      writeJson(uiStorageKey, preferences);
    }});
  }});


  const restoreForm = document.getElementById('restore-form');
  document.getElementById('preview-restore')?.addEventListener('click', async () => {{
    if (!restoreForm) return;
    const file = restoreForm.querySelector('input[name="backup"]')?.files?.[0];
    const output = document.getElementById('restore-preview');
    if (!file) {{ if (output) output.textContent = uiText.noFile; return; }}
    if (output) output.textContent = uiText.previewing;
    const body = new FormData(); body.append('backup', file); body.append('preview_csrf_token', restoreForm.querySelector('input[name="preview_csrf_token"]')?.value || '');
    try {{
      const response = await fetch('?action=restore-preview', {{ method:'POST', body, credentials:'same-origin', headers:{{'Accept':'application/json'}} }});
      const data = await response.json(); const previewToken = restoreForm.querySelector('input[name="preview_csrf_token"]'); if (previewToken && data.next_csrf_token) previewToken.value = data.next_csrf_token; if (!response.ok) throw new Error(data.error || uiText.previewFailed);
      const formatTime = (value) => value ? new Date(value * 1000).toLocaleString() : uiText.noData;
      const formatSize = (value) => `${{(Number(value || 0) / 1024 / 1024).toFixed(2)}} MiB`;
      if (output) {{
        output.replaceChildren();
        const headline = document.createElement('strong'); headline.textContent = uiText.backupReady; output.appendChild(headline);
        const grid = document.createElement('div'); grid.className = 'restore-preview-grid';
        const values = [
          [uiText.integrity, data.integrity], [uiText.schema, `${{data.schema_version}} / ${{data.supported_schema_version}}`],
          [uiText.measurements, Number(data.measurements || 0).toLocaleString()], [uiText.rawMeasurements, Number(data.raw_measurements || 0).toLocaleString()],
          [uiText.annotations, Number(data.annotations || 0).toLocaleString()], [uiText.devices, (data.device_serials || []).length.toLocaleString()], [uiText.fileSize, formatSize(data.size_bytes)],
          [uiText.dataPeriod, `${{formatTime(data.first_timestamp_utc)}} – ${{formatTime(data.last_timestamp_utc)}}`],
        ];
        values.forEach(([label,value]) => {{ const cell=document.createElement('div'); const title=document.createElement('strong'); title.textContent=label; const content=document.createElement('span'); content.textContent=String(value); cell.append(title,content); grid.appendChild(cell); }});
        output.appendChild(grid);
      }}
    }} catch (error) {{ if (output) output.textContent = `${{uiText.previewFailed}}: ${{error.message}}`; }}
  }});

  const deviceRefreshIntervalMs = 20000;
  const pageScroll = document.getElementById('page-scroll');
  let deviceRefreshRunning = false;
  async function refreshDeviceCards() {{
    if (deviceRefreshRunning || document.hidden) return;
    const currentSection = document.getElementById('devices'); if (!currentSection) return;
    deviceRefreshRunning = true;
    const savedScrollTop = pageScroll ? pageScroll.scrollTop : window.scrollY;
    try {{
      const currentUrl = new URL(window.location.href); const refreshUrl = new URL('./api/device-cards', currentUrl);
      for (const key of ['mode', 'lang', 'device']) {{ const value = currentUrl.searchParams.get(key); if (value !== null) refreshUrl.searchParams.set(key, value); }}
      const response = await fetch(refreshUrl, {{ cache:'no-store', credentials:'same-origin', headers:{{'Accept':'text/html'}} }});
      if (!response.ok) throw new Error(`device refresh failed: ${{response.status}}`);
      const template = document.createElement('template'); template.innerHTML = (await response.text()).trim();
      const nextSection = template.content.querySelector('#devices');
      if (nextSection) {{
        const connectedCountChanged = currentSection.dataset.connectedCount !== nextSection.dataset.connectedCount;
        const selectedDeviceChanged = currentSection.dataset.selectedSerial !== nextSection.dataset.selectedSerial;
        if (connectedCountChanged || selectedDeviceChanged) {{
          const nextSerial = nextSection.dataset.selectedSerial || ''; if (nextSerial) currentUrl.searchParams.set('device', nextSerial); else currentUrl.searchParams.delete('device');
          window.location.replace(currentUrl.toString()); return;
        }}
        nextSection.open = currentSection.open; currentSection.replaceWith(nextSection); applyCardPreferences();
      }}
    }} catch (error) {{ console.debug('GMC device display refresh skipped', error); }}
    finally {{ requestAnimationFrame(() => {{ if (pageScroll) pageScroll.scrollTop = savedScrollTop; else window.scrollTo({{top:savedScrollTop,behavior:'instant'}}); }}); deviceRefreshRunning = false; }}
  }}
  window.setInterval(refreshDeviceCards, deviceRefreshIntervalMs);
  document.addEventListener('visibilitychange', () => {{ if (!document.hidden) refreshDeviceCards(); }});
}})();
"""


DASHBOARD_CSS += r"""
.workflow-section > p,.history-section > p { margin-top:-.25rem; margin-bottom:.9rem; color:var(--muted); line-height:1.45; }
.workflow-steps { display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:.65rem; }
.workflow-step { display:grid; grid-template-columns:auto minmax(0,1fr); gap:.65rem; align-items:start; padding:.75rem; border:1px solid var(--border); border-radius:10px; background:var(--panel); }
.workflow-step.complete { border-color:color-mix(in srgb,var(--green) 40%,var(--border)); }
.workflow-step.pending { border-color:color-mix(in srgb,var(--blue) 35%,var(--border)); }
.workflow-step-icon { display:grid; place-items:center; width:1.5rem; height:1.5rem; border-radius:50%; font-weight:800; background:var(--panel-strong); }
.workflow-step.complete .workflow-step-icon { color:var(--green); }
.workflow-step.pending .workflow-step-icon { color:var(--blue); }
.workflow-step strong,.workflow-step small { display:block; }
.workflow-step small { margin-top:.18rem; line-height:1.35; }
.workflow-settings-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:.7rem; }
.toggle-row { display:flex; grid-template-columns:none; flex-direction:row; align-items:center; gap:.55rem; padding:.62rem .7rem; border:1px solid var(--border); border-radius:9px; background:var(--panel); }
.toggle-row input { width:auto; }
.comparison-form-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(155px,1fr)); gap:.65rem; align-items:end; }
.comparison-form-grid button { min-width:0; }
.comparison-results { margin-top:.2rem; }
.annotation-form-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:.65rem; }
.annotation-note-field { grid-column:1 / -1; }
textarea { width:100%; min-height:6rem; resize:vertical; font:inherit; padding:.65rem; border-radius:7px; border:1px solid color-mix(in srgb,CanvasText 28%,transparent); background:Canvas; color:CanvasText; }
.annotation-list,.managed-backup-list { display:grid; gap:.65rem; }
.generated-reports,.maintenance-subsection { margin-top:1.1rem; }
.maintenance-subsection > form { margin-bottom:.75rem; }
.maintenance-actions { margin-bottom:.4rem; }
.annotation-row,.managed-backup-row { display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; padding:.75rem; border:1px solid var(--border); border-radius:10px; background:var(--panel); }
.annotation-row p { margin:.35rem 0 0; }
.annotation-row small,.managed-backup-row small { display:block; margin-top:.16rem; color:var(--muted); }
.annotation-actions { display:flex; gap:.4rem; align-items:center; flex-wrap:wrap; }
.annotation-actions form { display:block; }
.annotation-actions button,.annotation-actions .button { width:auto; min-height:2rem; padding:.35rem .65rem; font-size:.8rem; }
.history-section-heading { display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; margin-bottom:.85rem; }
.history-section-heading h2,.history-section-heading p { margin-top:0; }
.history-period-label { display:flex; align-items:center; gap:.45rem; padding:.55rem .75rem; border:1px solid var(--border); border-radius:999px; background:var(--panel); font-size:.82rem; white-space:nowrap; }
.history-filter-grid { display:grid; grid-template-columns:minmax(10rem,1fr) minmax(10rem,1fr) minmax(13rem,1.2fr) auto; gap:.65rem; align-items:end; }
.history-raw-toggle { min-height:2.65rem; align-content:center; padding:.45rem .65rem; border:1px solid var(--border); border-radius:8px; background:var(--panel); }
.history-quick-ranges { display:flex; align-items:center; gap:.4rem; flex-wrap:wrap; margin-top:.55rem; }
.history-quick-ranges > span { margin-right:.2rem; color:var(--muted); font-size:.82rem; font-weight:650; }
.history-range-button { display:inline-flex; align-items:center; justify-content:center; min-height:2rem; padding:.3rem .7rem; border:1px solid var(--border); border-radius:999px; background:Canvas; color:CanvasText; text-decoration:none; font-size:.8rem; }
.history-range-button:hover { border-color:var(--blue); background:color-mix(in srgb,var(--blue) 7%,Canvas); }
.history-summary-metrics { margin:.9rem 0; grid-template-columns:repeat(3,minmax(0,1fr)); }
.workflow-history-chart { margin:0; padding:.85rem; border:1px solid var(--border); border-radius:12px; background:color-mix(in srgb,CanvasText 1.5%,transparent); }
.workflow-history-chart svg { display:block; width:100%; height:21rem; overflow:visible; }
.workflow-history-chart figcaption { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:.65rem; margin-top:.55rem; color:var(--muted); font-size:.8rem; }
.workflow-history-chart figcaption span { padding:.35rem .45rem; border-radius:7px; background:var(--panel); text-align:center; }
.history-grid-line { stroke:color-mix(in srgb,CanvasText 13%,transparent); stroke-width:.25; }
.history-axis-label,.history-axis-title,.history-legend-label { fill:color-mix(in srgb,CanvasText 72%,transparent); font-family:system-ui,sans-serif; }
.history-axis-label { font-size:2.35px; }
.history-axis-title { font-size:2.55px; font-weight:650; }
.history-legend-label { font-size:2.3px; }
.history-accepted-line { stroke:color-mix(in srgb,var(--blue) 72%,CanvasText); stroke-width:1.2; opacity:.68; }
.history-trend-line { fill:none; stroke:CanvasText; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; }
.event-marker { stroke:#f59e0b; stroke-width:.65; stroke-dasharray:2 1; opacity:.8; }
.raw-rejected-marker { fill:var(--red); stroke:Canvas; stroke-width:.35; opacity:.85; }
.history-chart-help { display:flex; align-items:center; gap:.4rem .6rem; flex-wrap:wrap; margin:.55rem 0 .2rem; color:var(--muted); font-size:.78rem; }
.history-key { width:1.1rem; height:.18rem; display:inline-block; border-radius:999px; }
.history-key.accepted { background:color-mix(in srgb,var(--blue) 72%,CanvasText); }
.history-key.trend { background:CanvasText; }
.history-key.event { background:#f59e0b; }
.history-key.rejected { width:.55rem; height:.55rem; border-radius:50%; background:var(--red); }
.self-test-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:.6rem; }
.self-test-item { display:grid; grid-template-columns:auto minmax(0,1fr); gap:.55rem; align-items:start; padding:.65rem .7rem; border:1px solid var(--border); border-radius:9px; background:var(--panel); }
.self-test-item .status-dot { margin-top:.25rem; }
.self-test-item.ok .status-dot { background:var(--green); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--green) 16%,transparent); }
.self-test-item.warning .status-dot { background:var(--yellow); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--yellow) 16%,transparent); }
.self-test-item.error .status-dot { background:var(--red); box-shadow:0 0 0 .22rem color-mix(in srgb,var(--red) 16%,transparent); }
.self-test-item strong,.self-test-item small { display:block; }
.self-test-item small { margin-top:.16rem; }
@media (max-width:800px) {
  .annotation-form-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .history-filter-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .history-summary-metrics { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .history-period-label { white-space:normal; }
}
@media (max-width:520px) {
  .annotation-form-grid { grid-template-columns:1fr; }
  .annotation-note-field { grid-column:auto; }
  .annotation-row,.managed-backup-row { flex-direction:column; }
  .annotation-actions { width:100%; }
  .annotation-actions form,.annotation-actions button,.annotation-actions .button { flex:1 1 auto; }
  .history-section-heading { flex-direction:column; }
  .history-period-label { width:100%; justify-content:center; }
  .history-filter-grid { grid-template-columns:1fr; }
  .history-summary-metrics { grid-template-columns:1fr; }
  .workflow-history-chart { padding:.5rem; overflow-x:auto; }
  .workflow-history-chart svg { min-width:43rem; height:16rem; }
  .workflow-history-chart figcaption { grid-template-columns:repeat(2,minmax(0,1fr)); }
}
"""

DASHBOARD_CSS += r"""
.calibration-panel { margin-top:.8rem; padding:.78rem; border:1px solid var(--border); border-radius:11px; background:color-mix(in srgb,var(--blue) 3%,var(--panel)); }
.calibration-panel-header { display:flex; justify-content:space-between; align-items:flex-start; gap:.75rem; }
.calibration-panel-header > div { display:grid; gap:.16rem; min-width:0; }
.calibration-panel-header small { color:var(--muted); line-height:1.4; overflow-wrap:anywhere; }
.calibration-status { display:inline-flex; align-items:center; border-radius:999px; padding:.28rem .55rem; font-size:.75rem; font-weight:760; white-space:nowrap; }
.calibration-status::before { content:""; width:.48rem; height:.48rem; border-radius:50%; margin-right:.35rem; background:currentColor; }
.calibration-documented .calibration-status { color:var(--green); background:color-mix(in srgb,var(--green) 12%,transparent); }
.calibration-working_values .calibration-status { color:var(--blue); background:color-mix(in srgb,var(--blue) 12%,transparent); }
.calibration-predefined .calibration-status { color:var(--green); background:color-mix(in srgb,var(--green) 12%,transparent); }
.calibration-customized .calibration-status { color:var(--blue); background:color-mix(in srgb,var(--blue) 12%,transparent); }
.calibration-incomplete .calibration-status { color:var(--yellow); background:color-mix(in srgb,var(--yellow) 14%,transparent); }
.calibration-summary { display:flex; flex-wrap:wrap; gap:.4rem .75rem; margin-top:.55rem; color:var(--muted); font-size:.82rem; }
.calibration-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.48rem; margin-top:.65rem; }
.calibration-grid > div { padding:.52rem; border-radius:8px; background:color-mix(in srgb,CanvasText 3%,transparent); min-width:0; }
.calibration-grid strong,.tube-profile-card dt { display:block; font-size:.7rem; text-transform:uppercase; letter-spacing:.035em; opacity:.72; margin-bottom:.16rem; }
.calibration-grid span { display:block; overflow-wrap:anywhere; }
.tube-profile-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.55rem; margin-top:.65rem; }
.tube-profile-card { padding:.62rem; border:1px solid var(--border); border-radius:9px; background:var(--panel); min-width:0; }
.tube-profile-card.single-profile { grid-column:1 / -1; }
.tube-profile-card.uncalibrated,.tube-profile-card.unconfigured { border-color:color-mix(in srgb,var(--yellow) 45%,var(--border)); }
.tube-profile-heading { display:flex; justify-content:space-between; gap:.6rem; align-items:baseline; margin-bottom:.5rem; }
.tube-profile-heading span { color:var(--muted); overflow-wrap:anywhere; text-align:right; }
.tube-profile-card dl { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.42rem; margin:0; }
.tube-profile-card dl > div { padding:.42rem; border-radius:7px; background:color-mix(in srgb,CanvasText 3%,transparent); min-width:0; }
.tube-profile-card dd { margin:0; overflow-wrap:anywhere; }
.tube-profile-card p { margin:.55rem 0 0; font-size:.78rem; line-height:1.4; overflow-wrap:anywhere; }
@media (max-width:700px) {
  .calibration-panel-header { align-items:stretch; flex-direction:column; }
  .calibration-status { align-self:flex-start; white-space:normal; }
  .calibration-grid,.tube-profile-grid,.tube-profile-card dl { grid-template-columns:1fr; }
  .tube-profile-card.single-profile { grid-column:auto; }
}
"""

DASHBOARD_CSS += r"""
/* 8.4 scientific detector cards */
.detector-tube-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.65rem; margin-top:.72rem; }
.detector-tube-grid > :only-child { grid-column:1/-1; }
.detector-tube-card { border:1px solid var(--border); border-radius:10px; padding:.65rem; background:color-mix(in srgb,CanvasText 2%,transparent); }
.detector-tube-card.active { border-color:color-mix(in srgb,var(--green) 55%,var(--border)); box-shadow:inset 3px 0 0 var(--green); }
.detector-tube-card.uncalibrated { box-shadow:inset 3px 0 0 var(--yellow); }
.tube-title,.load-heading { display:flex; align-items:center; justify-content:space-between; gap:.5rem; }
.active-tube-badge { font-size:.7rem; padding:.16rem .42rem; border-radius:999px; background:color-mix(in srgb,var(--green) 13%,transparent); color:var(--green); font-weight:760; }
.tube-state { display:flex; gap:.35rem; margin:.4rem 0; font-size:.8rem; color:var(--muted); }
.detector-tube-card dl { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.4rem; margin:.45rem 0 0; }
.detector-tube-card dt { font-size:.66rem; text-transform:uppercase; opacity:.7; }
.detector-tube-card dd { margin:.1rem 0 0; overflow-wrap:anywhere; font-size:.82rem; }
.measurement-quality-card { display:flex; align-items:center; justify-content:space-between; gap:.8rem; padding:.72rem; margin-top:.65rem; border-radius:10px; background:color-mix(in srgb,var(--blue) 7%,var(--panel)); }
.measurement-quality-card > div { display:grid; gap:.12rem; }
.quality-stars { font-size:1.25rem; letter-spacing:.06em; line-height:1.1; }
.quality-score { font-weight:800; font-size:1rem; white-space:nowrap; }
.detector-load-card { padding:.65rem .72rem; margin-top:.55rem; border:1px solid var(--border); border-radius:10px; }
.load-track { height:.65rem; margin-top:.45rem; border-radius:999px; overflow:hidden; background:color-mix(in srgb,CanvasText 8%,transparent); }
.load-fill { display:block; height:100%; min-width:0; border-radius:inherit; background:var(--green); transition:width .25s ease; }
.load-fill.yellow { background:var(--yellow); }
.load-fill.red { background:var(--red); }
.calibration-warnings { margin:.65rem 0 0; padding:.55rem .75rem .55rem 1.8rem; border-radius:9px; background:color-mix(in srgb,var(--yellow) 10%,transparent); }
.calibration-warnings li { margin:.18rem 0; }
.device-comparison-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:.65rem; }
.device-comparison-card { padding:.72rem; border:1px solid var(--border); border-radius:10px; background:var(--panel); }
.device-comparison-card strong,.device-comparison-card span { display:block; }
.device-comparison-card .comparison-value { font-size:1.35rem; font-weight:800; margin:.3rem 0; }
.calibration-manager-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:.65rem; }
.calibration-profile-card { padding:.7rem; border:1px solid var(--border); border-radius:10px; }
.calibration-profile-card dl { margin:.45rem 0 0; display:grid; gap:.3rem; }
.calibration-profile-card dl div { display:flex; justify-content:space-between; gap:.5rem; }
.calibration-wizard { display:grid; grid-template-columns:repeat(7,auto); align-items:center; justify-content:start; gap:.4rem; margin-top:.75rem; overflow-x:auto; }
.calibration-wizard .step { display:grid; place-items:center; min-width:9rem; min-height:4.6rem; padding:.55rem; border:1px solid var(--border); border-radius:10px; text-align:center; }
.data-mode-switch { display:flex; flex-wrap:wrap; gap:.35rem; }
.data-mode-switch a { padding:.35rem .55rem; border:1px solid var(--border); border-radius:999px; font-size:.78rem; }
.data-mode-switch a.active { background:var(--blue); color:white; border-color:var(--blue); }
@media(max-width:700px){.detector-tube-grid,.detector-tube-card dl{grid-template-columns:1fr}.measurement-quality-card{align-items:flex-start}.calibration-wizard{grid-template-columns:1fr}.calibration-wizard .arrow{display:none}}

"""

DASHBOARD_CSS += r"""
.history-corrected-line{fill:none;stroke:#7c3aed;stroke-width:1.25;stroke-dasharray:2.5 1.5}
.history-key.corrected{background:#7c3aed}
.device-comparison-section,.calibration-management{margin-top:1.1rem}
.device-comparison-card,.calibration-manager-card,.report-data-mode-card{background:var(--card-bg,#fff);border:1px solid var(--border,#d9e2ec);border-radius:14px;padding:1rem;box-shadow:0 6px 20px rgba(15,23,42,.04)}
.device-comparison-row,.device-comparison-summary,.calibration-profile-row,.calibration-history-row{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.65rem 0;border-bottom:1px solid var(--border,#e5e7eb)}
.device-comparison-row:last-child,.calibration-profile-row:last-child,.calibration-history-row:last-child{border-bottom:0}
.device-comparison-row div,.calibration-profile-row div,.calibration-history-row div{display:flex;flex-direction:column;min-width:0}
.device-comparison-row small,.calibration-profile-row small,.calibration-history-row small{color:var(--muted,#64748b)}
.device-comparison-summary{font-size:1.05rem;border-top:2px solid var(--border,#d9e2ec);border-bottom:0;margin-top:.25rem}
.comparison-status{border-radius:999px;padding:.35rem .7rem;font-weight:700}.comparison-status.ok{background:#dcfce7;color:#166534}.comparison-status.warning{background:#fef3c7;color:#92400e}
.calibration-manager-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1rem 0}
.calibration-manager-card h3{margin-top:0}.profile-state{font-weight:800;color:#15803d}.calibration-profile-row.custom .profile-state{color:#ca8a04}
.calibration-wizard-steps{display:flex;align-items:center;justify-content:space-between;gap:.6rem;flex-wrap:wrap;margin-bottom:1rem}.calibration-wizard-steps span{display:flex;align-items:center;gap:.4rem}.calibration-wizard-steps b{display:grid;place-items:center;width:1.7rem;height:1.7rem;border-radius:50%;background:#e0f2fe;color:#075985}.calibration-wizard-steps i{font-style:normal;color:#94a3b8}
.calibration-profile-form{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem}.calibration-profile-form label{display:flex;flex-direction:column;gap:.3rem}.calibration-profile-form .wide{grid-column:1/-1}.calibration-profile-form button{justify-self:start}
.calibration-history-list{display:flex;flex-direction:column}
.report-data-mode-card{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin:1rem 0}.report-data-mode-card>div:first-child{display:flex;flex-direction:column}.data-mode-switch{display:flex;gap:.45rem;flex-wrap:wrap}
@media(max-width:820px){.calibration-manager-grid{grid-template-columns:1fr}.calibration-profile-form{grid-template-columns:1fr 1fr}.report-data-mode-card{align-items:flex-start;flex-direction:column}}
@media(max-width:560px){.calibration-profile-form{grid-template-columns:1fr}.device-comparison-row,.device-comparison-summary,.calibration-profile-row,.calibration-history-row{align-items:flex-start;flex-direction:column;gap:.25rem}.calibration-wizard-steps i{display:none}.calibration-wizard-steps{align-items:flex-start;flex-direction:column}}
"""
