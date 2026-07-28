
(() => {
  const analysisDevice = window.GMC_BOOTSTRAP.analysisDevice || "";
  const uiStorageKey = 'gmc-dashboard-usability-v1';
  const uiText = window.GMC_BOOTSTRAP.uiText || {};
  const uiLanguage = (document.documentElement.lang || 'en').toLowerCase();
  const uiLocale = uiLanguage === 'de' ? 'de-DE' : uiLanguage === 'en' ? 'en-US' : uiLanguage;
  function formatUiNumber(value, options = {}) {
    const number = Number(value || 0);
    return new Intl.NumberFormat(uiLocale, options).format(Number.isFinite(number) ? number : 0);
  }

  function resolveDashboardUrl(value) {
    try { return new URL(value, window.location.href); }
    catch (_error) { return new URL(value, 'http://localhost/'); }
  }

  const languageSelect = document.getElementById('language-select');
  languageSelect?.addEventListener('change', () => {
    const form = document.getElementById('language-select-form');
    if (form instanceof HTMLFormElement) form.requestSubmit();
  });
  document.getElementById('reload-dashboard')?.addEventListener('click', () => {
    window.location.reload();
  });

  function readJson(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key) || '') || fallback; }
    catch (_error) { return fallback; }
  }
  function writeJson(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (_error) {}
  }
  const preferences = readJson(uiStorageKey, { cards: {}, groups: {}, pinned: [], reportForms: {}, lastSection: '', analysisLevel: '' });
  const analysisLevelSelect = document.getElementById('analysis-level-select');
  const allowedAnalysisLevels = new Set(['summary', 'analysis', 'expert']);
  function setAnalysisLevel(requestedLevel, persist = true) {
    const fallback = analysisLevelSelect?.dataset.defaultLevel || 'analysis';
    const level = allowedAnalysisLevels.has(requestedLevel) ? requestedLevel : fallback;
    document.body.dataset.analysisLevel = level;
    let selectedDescription = '';
    if (analysisLevelSelect instanceof HTMLSelectElement) {
      analysisLevelSelect.value = level;
      const selectedOption = analysisLevelSelect.selectedOptions[0];
      selectedDescription = selectedOption?.dataset.description || '';
      analysisLevelSelect.title = selectedDescription || analysisLevelSelect.getAttribute('aria-label') || '';
    }
    const description = document.getElementById('analysis-level-description');
    if (description && selectedDescription) description.textContent = selectedDescription;
    if (persist) { preferences.analysisLevel = level; writeJson(uiStorageKey, preferences); }
  }
  analysisLevelSelect?.addEventListener('change', () => {
    setAnalysisLevel(analysisLevelSelect.value || 'analysis');
  });
  setAnalysisLevel(preferences.analysisLevel || analysisLevelSelect?.dataset.defaultLevel || 'analysis', false);

  const toggleAllButtons = [...document.querySelectorAll('#toggle-all-cards')];
  const allDetailsSelector = 'details.collapsible-card, details.analysis-group, details.download-group';
  function updateToggleAllButton() {
    if (!toggleAllButtons.length) return;
    const details = [...document.querySelectorAll(allDetailsSelector)];
    const allOpen = details.length > 0 && details.every((item) => item.open);
    toggleAllButtons.forEach((button) => {
      button.textContent = allOpen ? uiText.collapseAll : uiText.expandAll;
      button.setAttribute('aria-expanded', String(allOpen));
    });
  }
  function setAllCards(open) {
    const details = [...document.querySelectorAll(allDetailsSelector)];
    preferences.cards = preferences.cards || {};
    preferences.groups = preferences.groups || {};
    details.forEach((item) => {
      item.open = open;
      if (!item.id) return;
      if (item.classList.contains('collapsible-card')) preferences.cards[item.id] = open;
      else preferences.groups[item.id] = open;
    });
    writeJson(uiStorageKey, preferences);
    updateToggleAllButton();
  }
  const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches === true;
  function jumpToSection(selector) {
    if (!selector || selector.charAt(0) !== '#') return false;
    const target = document.getElementById(selector.slice(1));
    if (!target) return false;
    if (target.classList.contains('advanced-only') && document.body.dataset.analysisLevel === 'summary') {
      setAnalysisLevel('analysis');
    }
    let parent = target.parentElement;
    while (parent) {
      if (parent instanceof HTMLDetailsElement) parent.open = true;
      parent = parent.parentElement;
    }
    const scroller = document.getElementById('page-scroll');
    if (scroller) {
      const targetTop = target.getBoundingClientRect().top - scroller.getBoundingClientRect().top + scroller.scrollTop - 12;
      scroller.scrollTo({ top: Math.max(0, targetTop), behavior: reduceMotion ? 'auto' : 'smooth' });
    } else {
      target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    }
    preferences.lastSection = selector;
    writeJson(uiStorageKey, preferences);
    try {
      const nextUrl = new URL(window.location.href);
      nextUrl.hash = selector;
      history.replaceState(null, '', nextUrl.pathname + nextUrl.search + nextUrl.hash);
    } catch (_error) {}
    return true;
  }
  document.addEventListener('click', (event) => {
    const toggleAll = event.target.closest('#toggle-all-cards');
    if (!toggleAll) return;
    event.preventDefault();
    const details = [...document.querySelectorAll(allDetailsSelector)];
    setAllCards(!(details.length > 0 && details.every((item) => item.open)));
  });
  const sectionSelect = document.getElementById('section-select');
  const sectionNavigationSlot = document.getElementById('section-navigation-slot');
  const sectionFloatingNavigation = document.getElementById('section-floating-navigation');
  const navigationScrollContainer = document.getElementById('page-scroll');
  sectionSelect?.addEventListener('change', () => {
    const sectionId = sectionSelect.value || 'devices';
    jumpToSection(`#${sectionId}`);
  });
  function updateFloatingSectionNavigation() {
    if (!sectionNavigationSlot || !sectionFloatingNavigation) return;
    const slotBox = sectionNavigationSlot.getBoundingClientRect();
    const scrollBox = navigationScrollContainer?.getBoundingClientRect();
    const safeTop = Math.max(12, (scrollBox?.top || 0) + 12);
    const shouldFloat = slotBox.top < safeTop;
    if (!shouldFloat) {
      sectionFloatingNavigation.classList.remove('is-floating');
      sectionFloatingNavigation.style.removeProperty('--section-floating-left');
      sectionFloatingNavigation.style.removeProperty('--section-floating-width');
      return;
    }
    const viewportPadding = 12;
    const width = Math.min(slotBox.width, window.innerWidth - viewportPadding * 2);
    const left = Math.min(
      Math.max(viewportPadding, slotBox.left),
      Math.max(viewportPadding, window.innerWidth - width - viewportPadding),
    );
    sectionFloatingNavigation.style.setProperty('--section-floating-left', `${Math.round(left)}px`);
    sectionFloatingNavigation.style.setProperty('--section-floating-width', `${Math.round(width)}px`);
    sectionFloatingNavigation.classList.add('is-floating');
  }
  let sectionFloatingFrame = 0;
  function scheduleFloatingSectionNavigationUpdate() {
    if (sectionFloatingFrame) return;
    sectionFloatingFrame = window.requestAnimationFrame(() => {
      sectionFloatingFrame = 0;
      updateFloatingSectionNavigation();
    });
  }
  navigationScrollContainer?.addEventListener('scroll', scheduleFloatingSectionNavigationUpdate, {passive:true});
  window.addEventListener('resize', scheduleFloatingSectionNavigationUpdate, {passive:true});
  scheduleFloatingSectionNavigationUpdate();

  document.querySelectorAll('a[href*="action=download"]').forEach((link) => {
    const url = resolveDashboardUrl(link.getAttribute('href') || '');
    url.searchParams.set('device', analysisDevice);
    url.searchParams.set('lang', "__LANGUAGE__");
    link.setAttribute('href', url.pathname + url.search);
  });
  document.querySelectorAll('form').forEach((form) => {
    const actionInput = form.querySelector('input[name="action"][value="download"]');
    if (!actionInput || form.querySelector('input[name="device"]')) return;
    const input = document.createElement('input');
    input.type = 'hidden'; input.name = 'device'; input.value = analysisDevice; form.appendChild(input);
    if (!form.querySelector('input[name="lang"]')) {
      const langInput = document.createElement('input');
      langInput.type = 'hidden'; langInput.name = 'lang'; langInput.value = "__LANGUAGE__"; form.appendChild(langInput);
    }
  });

  const currentUrl = new URL(window.location.href);
  const savedDevice = preferences.device || '';
  const cssEscape = window.CSS && typeof window.CSS.escape === 'function'
    ? window.CSS.escape
    : (value) => String(value).replace(/[^a-zA-Z0-9_-]/g, (char) => `\\${char}`);
  if (!currentUrl.searchParams.has('device') && savedDevice && savedDevice !== analysisDevice && document.querySelector(`[data-device-serial="${cssEscape(savedDevice)}"]`)) {
    currentUrl.searchParams.set('device', savedDevice);
    window.location.replace(currentUrl.toString());
    return;
  }
  if (analysisDevice) { preferences.device = analysisDevice; writeJson(uiStorageKey, preferences); }
  document.addEventListener('click', (event) => {
    const deviceLink = event.target.closest('a.device-select');
    if (deviceLink) {
      const card = deviceLink.closest('[data-device-serial]');
      if (card) { preferences.device = card.dataset.deviceSerial || ''; writeJson(uiStorageKey, preferences); }
    }
  });

  const primaryDashboard = document.getElementById('primary-dashboard');
  function applyCardPreferences() {
    const cards = [...document.querySelectorAll('details.collapsible-card')];
    cards.forEach((card, index) => {
      if (!card.dataset.defaultOrder) card.dataset.defaultOrder = String(index);
      if (Object.prototype.hasOwnProperty.call(preferences.cards || {}, card.id)) card.open = Boolean(preferences.cards[card.id]);
      const pinned = (preferences.pinned || []).includes(card.id);
      card.classList.toggle('pinned-card', pinned);
      const pin = card.querySelector('.card-pin');
      if (pin) { pin.setAttribute('aria-pressed', String(pinned)); pin.textContent = pinned ? '★' : '☆'; }
      if (card.parentElement === primaryDashboard) {
        const pinIndex = (preferences.pinned || []).indexOf(card.id);
        card.style.order = pinned ? String(-100 + pinIndex) : card.dataset.defaultOrder;
      }
    });
  }
  function applyGroupPreferences() {
    document.querySelectorAll('details.analysis-group, details.download-group').forEach((group) => {
      if (group.id && Object.prototype.hasOwnProperty.call(preferences.groups || {}, group.id)) {
        group.open = Boolean(preferences.groups[group.id]);
      }
    });
  }
  applyCardPreferences();
  applyGroupPreferences();
  updateToggleAllButton();

  document.addEventListener('toggle', (event) => {
    const item = event.target;
    if (!(item instanceof HTMLDetailsElement)) return;
    if (item.classList.contains('collapsible-card')) {
      preferences.cards = preferences.cards || {};
      preferences.cards[item.id] = item.open;
    } else if (item.classList.contains('analysis-group') || item.classList.contains('download-group')) {
      preferences.groups = preferences.groups || {};
      if (item.id) preferences.groups[item.id] = item.open;
    } else {
      return;
    }
    writeJson(uiStorageKey, preferences);
    updateToggleAllButton();
  }, true);

  let helpPopover = null;
  let helpTrigger = null;
  function closeHelp({ restoreFocus = false } = {}) {
    if (helpTrigger) { helpTrigger.removeAttribute('aria-describedby'); helpTrigger.setAttribute('aria-expanded', 'false'); }
    if (helpPopover) helpPopover.remove();
    helpPopover = null;
    if (restoreFocus && helpTrigger) helpTrigger.focus();
    helpTrigger = null;
  }
  document.addEventListener('click', (event) => {
    const pin = event.target.closest('.card-pin');
    if (pin) {
      event.preventDefault(); event.stopPropagation();
      const card = pin.closest('details.collapsible-card');
      if (!card) return;
      preferences.pinned = preferences.pinned || [];
      const index = preferences.pinned.indexOf(card.id);
      if (index >= 0) preferences.pinned.splice(index, 1); else preferences.pinned.push(card.id);
      writeJson(uiStorageKey, preferences); applyCardPreferences(); return;
    }
    const help = event.target.closest('.card-help');
    if (help) {
      event.preventDefault(); event.stopPropagation(); closeHelp();
      const text = help.dataset.help || '';
      if (!text) return;
      const popover = document.createElement('div'); popover.className = 'card-help-popover'; popover.textContent = text; popover.setAttribute('role','tooltip'); popover.id = `help-${Date.now()}`; help.setAttribute('aria-describedby', popover.id); help.setAttribute('aria-expanded','true'); helpTrigger = help;
      document.body.appendChild(popover); helpPopover = popover;
      const rect = help.getBoundingClientRect();
      const left = Math.min(window.innerWidth - popover.offsetWidth - 12, Math.max(12, rect.right - popover.offsetWidth));
      const top = Math.min(window.innerHeight - popover.offsetHeight - 12, rect.bottom + 8);
      popover.style.left = `${left}px`; popover.style.top = `${top}px`; return;
    }
    if (helpPopover && !event.target.closest('.card-help-popover')) closeHelp();
  });
  window.addEventListener('resize', () => closeHelp());
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && helpPopover) { event.preventDefault(); closeHelp({restoreFocus:true}); } });
  document.getElementById('page-scroll')?.addEventListener('scroll', () => closeHelp(), {passive:true});
  function setActiveSection(id) {
    if (!(sectionSelect instanceof HTMLSelectElement)) return;
    const option = [...sectionSelect.options].find((item) => item.value === id);
    if (!option) return;
    sectionSelect.value = id;
    sectionSelect.title = option.textContent.trim();
  }
  if (!window.location.hash && preferences.lastSection) {
    requestAnimationFrame(() => jumpToSection(preferences.lastSection));
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      setActiveSection(visible.target.id);
    }, { root: document.getElementById('page-scroll'), rootMargin: '-20% 0px -65% 0px', threshold: [0.05, 0.25] });
    ['devices','radiation-intelligence','analysis','long-term-analysis','history','workflow','calibration-management','reports'].forEach((id) => { const node = document.getElementById(id); if (node) observer.observe(node); });
  }

  document.querySelectorAll('form.report-preset-source').forEach((form) => {
    const kind = form.dataset.presetKind || 'custom';
    const saved = (preferences.reportForms || {})[kind] || {};
    for (const [name, value] of Object.entries(saved)) { const field = form.elements.namedItem(name); if (field && typeof value === 'string') field.value = value; }
    form.addEventListener('change', () => {
      preferences.reportForms = preferences.reportForms || {};
      preferences.reportForms[kind] = Object.fromEntries([...new FormData(form).entries()].filter(([key]) => !['device','lang','action'].includes(key)).map(([key,value]) => [key,String(value)]));
      writeJson(uiStorageKey, preferences);
    });
  });


  const customReportForm = document.getElementById('custom-report-form');
  const customReportPeriod = document.getElementById('custom-report-period');
  const reportPreviewPeriod = document.getElementById('report-preview-period');
  const reportPreviewCoverage = document.getElementById('report-preview-coverage');
  const reportPreviewSamples = document.getElementById('report-preview-samples');
  const reportPreviewGap = document.getElementById('report-preview-gap');
  const reportPreviewWarning = document.getElementById('report-preview-warning');
  const reportFormStatus = document.getElementById('report-form-status');
  const reportSubmit = document.getElementById('custom-report-submit');
  let reportPreviewTimer = null;
  let reportPreviewController = null;

  function formatDuration(seconds) {
    const value = Math.max(0, Number(seconds || 0));
    if (value < 3600) return `${Math.round(value / 60)} min`;
    if (value < 86400) return `${formatUiNumber(value / 3600, { minimumFractionDigits:1, maximumFractionDigits:1 })} h`;
    return `${formatUiNumber(value / 86400, { minimumFractionDigits:1, maximumFractionDigits:1 })} d`;
  }
  function setReportStatus(message = '', tone = '') {
    if (!reportFormStatus) return;
    reportFormStatus.textContent = message;
    reportFormStatus.dataset.tone = tone;
    reportFormStatus.hidden = !message;
  }
  function reportField(name) { return customReportForm?.elements.namedItem(name) || null; }
  function updateReportPeriodFields() {
    if (!customReportForm || !customReportPeriod) return;
    const period = customReportPeriod.value || 'daily';
    const visibility = {
      date: period === 'daily',
      week: period === 'weekly',
      month: period === 'monthly',
      start: period === 'custom',
      end: period === 'custom',
    };
    Object.entries(visibility).forEach(([name, visible]) => {
      const wrapper = customReportForm.querySelector(`[data-report-${name}-field]`);
      const input = reportField(name);
      if (wrapper) wrapper.hidden = !visible;
      if (input) input.required = visible;
    });
  }
  function validateReportForm() {
    if (!customReportForm) return false;
    updateReportPeriodFields();
    const period = customReportPeriod?.value || 'daily';
    const startInput = reportField('start');
    const endInput = reportField('end');
    if (period === 'custom' && startInput?.value && endInput?.value && endInput.value < startInput.value) {
      const message = uiText.reportEndBeforeStart || 'The end date must not be before the start date.';
      endInput.setCustomValidity(message);
      setReportStatus(message, 'error');
      return false;
    }
    if (endInput) endInput.setCustomValidity('');
    const valid = customReportForm.checkValidity();
    if (!valid) setReportStatus(uiText.completeRequiredFields || 'Complete the required period fields.', 'error');
    else setReportStatus('');
    return valid;
  }
  function applyReportPreset(preset) {
    if (!customReportForm || !customReportPeriod) return;
    const dateInput = reportField('date');
    const monthInput = reportField('month');
    const startInput = reportField('start');
    const endInput = reportField('end');
    const today = customReportForm.dataset.today || dateInput?.value || '';
    if (preset === 'today') {
      customReportPeriod.value = 'daily'; if (dateInput) dateInput.value = today;
    } else if (preset === 'yesterday') {
      customReportPeriod.value = 'daily'; if (dateInput) dateInput.value = customReportForm.dataset.yesterday || today;
    } else if (preset === 'rolling24') customReportPeriod.value = 'rolling24';
    else if (preset === 'rolling7') customReportPeriod.value = 'rolling7';
    else if (preset === 'month') {
      customReportPeriod.value = 'monthly'; if (monthInput) monthInput.value = customReportForm.dataset.currentMonth || '';
    } else if (preset === 'custom') {
      customReportPeriod.value = 'custom'; if (endInput && !endInput.value) endInput.value = today;
    }
    updateReportPeriodFields();
    customReportForm.dispatchEvent(new Event('change', {bubbles:true}));
    scheduleReportPreview();
  }
  document.querySelectorAll('[data-report-preset]').forEach((button) => {
    button.addEventListener('click', () => applyReportPreset(button.dataset.reportPreset || 'custom'));
  });

  async function refreshReportPreview() {
    if (!customReportForm || !validateReportForm()) return;
    reportPreviewController?.abort();
    reportPreviewController = new AbortController();
    const params = new URLSearchParams(new FormData(customReportForm));
    params.delete('action'); params.delete('selection'); params.delete('format');
    const currentUrl = new URL(window.location.href);
    const device = currentUrl.searchParams.get('device');
    const lang = currentUrl.searchParams.get('lang');
    if (device) params.set('device', device);
    if (lang) params.set('lang', lang);
    try {
      const response = await fetch(`./api/report-preview?${params.toString()}`, {
        cache:'no-store', credentials:'same-origin', headers:{'Accept':'application/json'}, signal:reportPreviewController.signal,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || `preview failed: ${response.status}`);
      if (reportPreviewPeriod) reportPreviewPeriod.textContent = data.period_label || '—';
      if (reportPreviewCoverage) reportPreviewCoverage.textContent = `${formatUiNumber(data.time_coverage_percent, { minimumFractionDigits:1, maximumFractionDigits:1 })} %`;
      if (reportPreviewSamples) reportPreviewSamples.textContent = formatUiNumber(data.samples, { maximumFractionDigits:0 });
      if (reportPreviewGap) reportPreviewGap.textContent = formatDuration(data.gap_seconds);
      if (reportPreviewWarning) { reportPreviewWarning.textContent = data.warning || ''; reportPreviewWarning.hidden = !data.warning; }
    } catch (error) {
      if (error?.name === 'AbortError') return;
      const message = `${uiText.reportPreviewFailed || 'The report preview could not be created.'} (${uiText.errorCode || 'Error code'}: REPORT-PREVIEW-01)`;
      if (reportPreviewWarning) { reportPreviewWarning.textContent = message; reportPreviewWarning.hidden = false; }
      setReportStatus(message, 'error');
      console.debug('GMC report preview failed', error);
    }
  }
  function scheduleReportPreview() {
    window.clearTimeout(reportPreviewTimer);
    reportPreviewTimer = window.setTimeout(refreshReportPreview, 220);
  }
  if (customReportForm) {
    updateReportPeriodFields();
    customReportForm.addEventListener('input', scheduleReportPreview);
    customReportForm.addEventListener('change', scheduleReportPreview);
    customReportForm.addEventListener('submit', (event) => {
      if (!validateReportForm()) {
        event.preventDefault();
        customReportForm.reportValidity();
        if (reportSubmit) reportSubmit.disabled = false;
        return;
      }
      if (reportSubmit) {
        reportSubmit.disabled = true;
        reportSubmit.dataset.originalText = reportSubmit.textContent || '';
        reportSubmit.textContent = uiText.preparingDownload || 'Preparing…';
      }
      setReportStatus(uiText.reportInputsPreserved || 'The selected settings are saved in this browser.', 'info');
    });
    scheduleReportPreview();
  }


  const restoreForm = document.getElementById('restore-form');
  document.getElementById('preview-restore')?.addEventListener('click', async () => {
    if (!restoreForm) return;
    const file = restoreForm.querySelector('input[name="backup"]')?.files?.[0];
    const output = document.getElementById('restore-preview');
    if (!file) { if (output) output.textContent = uiText.noFile; return; }
    if (output) output.textContent = uiText.previewing;
    const body = new FormData(); body.append('backup', file); body.append('preview_csrf_token', restoreForm.querySelector('input[name="preview_csrf_token"]')?.value || '');
    try {
      const response = await fetch('?action=restore-preview', { method:'POST', body, credentials:'same-origin', headers:{'Accept':'application/json'} });
      const data = await response.json(); const previewToken = restoreForm.querySelector('input[name="preview_csrf_token"]'); if (previewToken && data.next_csrf_token) previewToken.value = data.next_csrf_token; if (!response.ok) throw new Error(data.error || uiText.previewFailed);
      const formatTime = (value) => value ? new Date(value * 1000).toLocaleString(uiLocale) : uiText.noData;
      const formatSize = (value) => `${formatUiNumber(Number(value || 0) / 1024 / 1024, { minimumFractionDigits:2, maximumFractionDigits:2 })} MiB`;
      if (output) {
        output.replaceChildren();
        const headline = document.createElement('strong'); headline.textContent = uiText.backupReady; output.appendChild(headline);
        const grid = document.createElement('div'); grid.className = 'restore-preview-grid';
        const values = [
          [uiText.integrity, data.integrity], [uiText.schema, `${data.schema_version} / ${data.supported_schema_version}`],
          [uiText.measurements, formatUiNumber(data.measurements, { maximumFractionDigits:0 })], [uiText.rawMeasurements, formatUiNumber(data.raw_measurements, { maximumFractionDigits:0 })],
          [uiText.annotations, formatUiNumber(data.annotations, { maximumFractionDigits:0 })], [uiText.devices, formatUiNumber((data.device_serials || []).length, { maximumFractionDigits:0 })], [uiText.fileSize, formatSize(data.size_bytes)],
          [uiText.dataPeriod, `${formatTime(data.first_timestamp_utc)} – ${formatTime(data.last_timestamp_utc)}`],
        ];
        values.forEach(([label,value]) => { const cell=document.createElement('div'); const title=document.createElement('strong'); title.textContent=label; const content=document.createElement('span'); content.textContent=String(value); cell.append(title,content); grid.appendChild(cell); });
        output.appendChild(grid);
      }
    } catch (error) { if (output) output.textContent = `${uiText.previewFailed}: ${error.message}`; }
  });

  document.getElementById('copy-support-diagnostics')?.addEventListener('click', async () => {
    const status = document.getElementById('support-diagnostics-status');
    try {
      const response = await fetch('./api/support-diagnostics', {cache:'no-store', credentials:'same-origin'});
      if (!response.ok) throw new Error(`support diagnostics failed: ${response.status}`);
      const text = await response.text();
      await navigator.clipboard.writeText(text);
      if (status) status.textContent = uiText.diagnosticsCopied || 'Support diagnostics copied.';
    } catch (error) {
      if (status) status.textContent = `${uiText.copyFailed || 'Copy failed'} (DIAGNOSTICS-COPY-01)`;
      console.debug('GMC support diagnostics copy failed', error);
    }
  });

  document.addEventListener('click', (event) => {
    const reset = event.target.closest('[data-chart-reset]');
    if (reset) {
      const chart = reset.closest('.workflow-history-chart');
      chart?.scrollTo({left:0, behavior:reduceMotion ? 'auto' : 'smooth'});
      return;
    }
    const download = event.target.closest('[data-chart-download]');
    if (download) {
      const chart = download.closest('.workflow-history-chart');
      const svg = chart?.querySelector('svg');
      if (!svg) return;
      const source = new XMLSerializer().serializeToString(svg);
      const blob = new Blob([source], {type:'image/svg+xml;charset=utf-8'});
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'gmc-history-chart.svg';
      document.body.appendChild(link); link.click(); link.remove();
      window.setTimeout(() => URL.revokeObjectURL(link.href), 1000);
    }
  });

  const pageScroll = document.getElementById('page-scroll');
  const liveStatus = document.getElementById('live-refresh-status');
  let liveRefreshRunning = false;
  let liveRefreshDelayMs = 10000;
  let liveRefreshTimer = null;
  function scheduleLiveRefresh(delay = liveRefreshDelayMs) {
    window.clearTimeout(liveRefreshTimer);
    liveRefreshTimer = window.setTimeout(refreshLiveDevices, delay);
  }
  function setLiveStatus(text, state = '') {
    if (!liveStatus) return;
    liveStatus.textContent = text || '';
    liveStatus.dataset.state = state;
    liveStatus.hidden = !text;
  }
  function updateLiveCard(device) {
    const card = [...document.querySelectorAll('#devices .device-card')].find((item) => item.dataset.deviceSerial === String(device.serial || ''));
    if (!card) return false;
    const update = (name, value) => { const node = card.querySelector(`[data-live="${name}"]`); if (node && value !== undefined && value !== null) node.textContent = String(value); };
    const status = card.querySelector('[data-live="status"]');
    if (status) { status.textContent = device.status_label; status.className = `device-status ${device.status_class}`; }
    update('freshness', device.freshness_display);
    const freshness = card.querySelector('[data-live="freshness"]');
    if (freshness) {
      freshness.dataset.freshnessState = device.freshness_state || '';
      freshness.className = `device-freshness freshness-${device.freshness_severity || 'online'}`;
    }
    update('dose-number', device.dose_number);
    update('dose-unit', device.dose_unit);
    update('quality-stars', device.quality_stars);
    update('cpm', device.latest_value);
    update('health', device.health_summary);
    card.dataset.liveUpdatedUtc = String(device.timestamp_utc || 0);
    return true;
  }
  async function refreshLiveDevices() {
    if (liveRefreshRunning || document.hidden) { scheduleLiveRefresh(); return; }
    liveRefreshRunning = true;
    try {
      const currentUrl = new URL(window.location.href);
      const refreshUrl = resolveDashboardUrl('./api/live-devices');
      for (const key of ['lang', 'device']) { const value = currentUrl.searchParams.get(key); if (value !== null) refreshUrl.searchParams.set(key, value); }
      const response = await fetch(refreshUrl, { cache:'no-store', credentials:'same-origin', headers:{'Accept':'application/json'} });
      if (!response.ok) throw new Error(`live refresh failed: ${response.status}`);
      const data = await response.json();
      const cards = [...document.querySelectorAll('#devices .device-card')];
      if (Number(data.connected_count) !== cards.length || String(data.selected_serial || '') !== String(document.getElementById('devices')?.dataset.selectedSerial || '')) {
        window.location.reload(); return;
      }
      (data.devices || []).forEach(updateLiveCard);
      liveRefreshDelayMs = 10000;
      setLiveStatus('', 'ok');
    } catch (error) {
      liveRefreshDelayMs = Math.min(120000, Math.max(15000, liveRefreshDelayMs * 2));
      setLiveStatus(window.GMC_BOOTSTRAP.liveRefreshInterrupted || 'Live update interrupted', 'warning');
      console.debug('GMC live device refresh paused', error);
    } finally {
      liveRefreshRunning = false;
      scheduleLiveRefresh();
    }
  }
  scheduleLiveRefresh(10000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) scheduleLiveRefresh(100); });
  window.addEventListener('online', () => scheduleLiveRefresh(100));
})();
