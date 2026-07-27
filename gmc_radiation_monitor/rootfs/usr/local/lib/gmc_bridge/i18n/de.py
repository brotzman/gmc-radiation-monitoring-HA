from __future__ import annotations

CATALOG: dict[str, str] = {'1 h counting uncertainty': '1-h-Zählunsicherheit',
 '1 h coverage': '1-h-Abdeckung',
 '1 h mean': '1-h-Mittel',
 '1 h mean / 7 d mean × 100': '1-h-Mittel / 7-Tage-Mittel × 100',
 '1 h mean dose rate': '1-h-Mitteldosisleistung',
 '1 h mean minus 7 d baseline': '1-h-Mittel minus 7-Tage-Baseline',
 '24 h Fano factor': '24-h-Fano-Faktor',
 '24 h P95': '24-h-P95',
 '24 h P99': '24-h-P99',
 '24 h Z-score': '24-h-Z-Score',
 '24 h counting uncertainty': '24-h-Zählunsicherheit',
 '24 h distribution, percentiles and latest-value deviation': '24-h-Verteilung, Perzentile und Abweichung des '
                                                              'letzten Werts',
 '24 h maximum': '24-h-Maximum',
 '24 h mean': '24-h-Mittel',
 '24 h mean dose rate': '24-h-Mitteldosisleistung',
 '24 h median': '24-h-Median',
 '24 h minimum': '24-h-Minimum',
 '24 h standard deviation': '24-h-Standardabweichung',
 '50th percentile': '50. Perzentil',
 '7 d baseline': '7-Tage-Baseline',
 '7 d baseline dose rate': '7-Tage-Baseline-Dosisleistung',
 '7 d baseline drift': '7-Tage-Baseline-Drift',
 '7 d counting uncertainty': '7-Tage-Zählunsicherheit',
 '7-day smoothed daily median': 'Tagesmedian, über 7 Tage geglättet',
 '95th percentile': '95. Perzentil',
 '99th percentile': '99. Perzentil',
 'A device function is temporarily unavailable.': 'Eine Gerätefunktion ist vorübergehend nicht verfügbar.',
 'A fresh backup is recommended before deletion.': 'Vor dem Löschen wird eine aktuelle Sicherung empfohlen.',
 'A recent position change can affect comparability': 'Eine kürzliche Lageänderung kann die Vergleichbarkeit '
                                                      'beeinflussen',
 'Above the typical time profile': 'Über dem typischen Zeitprofil',
 'Above the usual local range': 'Über dem üblichen lokalen Bereich',
 'Absolute radiation assessment': 'Absolute Strahlungsbewertung',
 'Absolute thresholds and local anomaly detection answer different questions.': 'Absolute Grenzwerte und lokale '
                                                                                'Anomalieerkennung beantworten '
                                                                                'unterschiedliche Fragen.',
 'Acceleration magnitude': 'Beschleunigungsbetrag',
 'Acceleration raw values': 'Beschleunigungs-Rohwerte',
 'Accepted device values are stored separately after live CPM plausibility confirmation': 'Übernommene Gerätewerte '
                                                                                          'werden nach der laufenden '
                                                                                          'CPM-Plausibilitätsbestätigung '
                                                                                          'separat gespeichert',
 'Active threshold profile': 'Aktives Grenzwertprofil',
 'Adaptive background profile': 'Adaptives Hintergrundprofil',
 'Advanced': 'Erweitert',
 'Advanced diagnostics': 'Erweiterte Diagnose',
 'Advanced visuals': 'Erweiterte Visualisierungen',
 'Affected GMC devices': 'Betroffene GMC-Geräte',
 'Agreement': 'Übereinstimmung',
 'Air-pressure source': 'Luftdruckquelle',
 'Air-pressure trend': 'Luftdrucktrend',
 'All GMC history was deleted': 'Der gesamte GMC-Verlauf wurde gelöscht',
 'All baselines and comparisons use the same robust quality-filtered measurements.': 'Alle Baselines und Vergleiche '
                                                                                     'verwenden dieselben robust '
                                                                                     'qualitätsgefilterten '
                                                                                     'Messwerte.',
 'All connected GMC devices': 'Alle verbundenen GMC-Geräte',
 'All devices': 'Alle Geräte',
 'All downloads below automatically use the GMC device currently shown in Analysis. Select another connected device above to change the report source.': 'Alle '
                                                                                                                                                         'Downloads '
                                                                                                                                                         'verwenden '
                                                                                                                                                         'automatisch '
                                                                                                                                                         'das '
                                                                                                                                                         'GMC-Gerät, '
                                                                                                                                                         'das '
                                                                                                                                                         'aktuell '
                                                                                                                                                         'in '
                                                                                                                                                         'der '
                                                                                                                                                         'Analyse '
                                                                                                                                                         'angezeigt '
                                                                                                                                                         'wird. '
                                                                                                                                                         'Wähle '
                                                                                                                                                         'oben '
                                                                                                                                                         'ein '
                                                                                                                                                         'anderes '
                                                                                                                                                         'verbundenes '
                                                                                                                                                         'Gerät '
                                                                                                                                                         'aus, '
                                                                                                                                                         'um '
                                                                                                                                                         'die '
                                                                                                                                                         'Berichtsquelle '
                                                                                                                                                         'zu '
                                                                                                                                                         'wechseln.',
 'All known GMC devices with stored history': 'Alle bekannten GMC-Geräte mit gespeichertem Verlauf',
 'All statistical values, confidence intervals and diagnostics': 'Alle statistischen Kennzahlen, '
                                                                 'Vertrauensintervalle und Diagnosedaten',
 'All {count} known GMC devices are connected': 'Alle {count} bekannten GMC-Geräte sind verbunden',
 'Allow restore': 'Wiederherstellung erlauben',
 'Already assigned to {name}': 'Bereits {name} zugewiesen',
 'Analysis': 'Analyse',
 'Analysis JSON': 'Analyse-JSON',
 'Analysis PDF': 'Analyse-PDF',
 'Analysis depth': 'Analysetiefe',
 'Analysis for': 'Analyse für',
 'Analysis is still being prepared': 'Die Analyse wird noch vorbereitet',
 'Analysis shown': 'Analyse wird angezeigt',
 'Analysis, the traffic light and downloads will become meaningful after the first stored samples arrive.': 'Analyse, '
                                                                                                            'Ampel '
                                                                                                            'und '
                                                                                                            'Downloads '
                                                                                                            'werden '
                                                                                                            'aussagekräftig, '
                                                                                                            'sobald '
                                                                                                            'die '
                                                                                                            'ersten '
                                                                                                            'Messwerte '
                                                                                                            'gespeichert '
                                                                                                            'wurden.',
 'Analyze this device': 'Dieses Gerät analysieren',
 'Another report is already being generated': 'Ein anderer Bericht wird bereits erstellt',
 'Another report or maintenance job is running': 'Ein anderer Bericht- oder Wartungsvorgang läuft bereits',
 'Another report or restore job is running': 'Ein anderer Bericht oder Wiederherstellungsvorgang läuft bereits',
 'Another report, maintenance export, or restore job is running': 'Ein anderer Bericht, Wartungsexport oder '
                                                                  'Wiederherstellungsvorgang läuft bereits.',
 'App Started At': 'App gestartet am',
 'Apply': 'Übernehmen',
 'Assessment': 'Bewertung',
 'Assigned': 'Zugewiesen',
 'At least 24 h reference and 6 h persistence are required': 'Mindestens 24 h Referenz und 6 h anhaltende Änderung '
                                                             'sind erforderlich',
 'At least two daily background values are required.': 'Mindestens zwei tägliche Hintergrundwerte sind erforderlich.',
 'At least {count} valid hourly values are required': 'Mindestens {count} gültige Stundenwerte sind erforderlich',
 'At least {count} valid pairs are required': 'Mindestens {count} gültige Paare sind erforderlich',
 'At least {days} days of learning data are required': 'Mindestens {days} Tage Lerndaten sind erforderlich',
 'At least {span:g} hPa pressure variation is required': 'Mindestens {span:g} hPa beobachtete Druckspanne sind '
                                                         'erforderlich',
 'At the same time, the value is clearly above the usual local background. Review the trend and measurement conditions.': 'Gleichzeitig '
                                                                                                                          'liegt '
                                                                                                                          'der '
                                                                                                                          'Wert '
                                                                                                                          'deutlich '
                                                                                                                          'über '
                                                                                                                          'dem '
                                                                                                                          'üblichen '
                                                                                                                          'lokalen '
                                                                                                                          'Hintergrund. '
                                                                                                                          'Prüfe '
                                                                                                                          'den '
                                                                                                                          'Verlauf '
                                                                                                                          'und '
                                                                                                                          'die '
                                                                                                                          'Messbedingungen.',
 'Automatic device detection is running': 'Die automatische Geräteerkennung läuft',
 'Automatic refresh is temporarily unavailable': 'Die automatische Aktualisierung ist vorübergehend nicht verfügbar',
 'Availability': 'Verfügbarkeit',
 'Available': 'Verfügbar',
 'Back to analysis': 'Zurück zur Analyse',
 'Background index': 'Hintergrundindex',
 'Background index compares the rolling 1 h mean with the available 7 d baseline.': 'Hintergrundindex = gleitendes '
                                                                                    '1-h-Mittel im Verhältnis zur '
                                                                                    'verfügbaren 7-Tage-Baseline.',
 'Background index formula explanation': 'Hintergrundindex = gleitendes 1-h-Mittel im Verhältnis zur verfügbaren '
                                         '7-Tage-Baseline.',
 'Background trend over days and months': 'Entwicklung des Hintergrunds über Tage und Monate',
 'Backup is compatible and ready to restore.': 'Die Sicherung ist kompatibel und kann wiederhergestellt werden.',
 'Backup preview failed': 'Die Sicherungsvorschau ist fehlgeschlagen',
 'Baseline available': 'Baseline verfügbar',
 'Baseline currently stable': 'Baseline derzeit stabil',
 'Baseline deviation': 'Baseline-Abweichung',
 'Baseline deviation, drift and sustained relative events': 'Baseline-Abweichung, Drift und anhaltende relative '
                                                            'Ereignisse',
 'Baseline deviation: {cpm} CPM ({percent}%)': 'Baseline-Abweichung: {cpm} CPM ({percent} %)',
 'Baseline drift: {value}%': 'Baseline-Drift: {value} %',
 'Baseline learning in progress': 'Baseline wird noch gebildet',
 'Baseline readiness': 'Baseline-Bereitschaft',
 'Baseline: {value} CPM': 'Baseline: {value} CPM',
 'Battery voltage': 'Batteriespannung',
 'Baud rate': 'Baudrate',
 'Below the typical time profile': 'Unter dem typischen Zeitprofil',
 'Below warning threshold': 'Unterhalb der Warnschwelle',
 'BfS and ICRP reference profiles convert annual dose values into continuous-rate equivalents for context. They are not official instantaneous alarm limits and cannot replace professional dose assessment.': 'Die '
                                                                                                                                                                                                               'BfS- '
                                                                                                                                                                                                               'und '
                                                                                                                                                                                                               'ICRP-Referenzprofile '
                                                                                                                                                                                                               'rechnen '
                                                                                                                                                                                                               'Jahresdosen '
                                                                                                                                                                                                               'zur '
                                                                                                                                                                                                               'Einordnung '
                                                                                                                                                                                                               'in '
                                                                                                                                                                                                               'kontinuierliche '
                                                                                                                                                                                                               'Dosisleistungsäquivalente '
                                                                                                                                                                                                               'um. '
                                                                                                                                                                                                               'Sie '
                                                                                                                                                                                                               'sind '
                                                                                                                                                                                                               'keine '
                                                                                                                                                                                                               'amtlichen '
                                                                                                                                                                                                               'Sofort-Alarmgrenzen '
                                                                                                                                                                                                               'und '
                                                                                                                                                                                                               'ersetzen '
                                                                                                                                                                                                               'keine '
                                                                                                                                                                                                               'fachliche '
                                                                                                                                                                                                               'Dosisbewertung.',
 'BfS reference projection': 'BfS-Referenzprojektion',
 'Both connected counters show a quality-filtered simultaneous rise': 'Beide verbundenen Zähler zeigen gleichzeitig '
                                                                      'einen qualitätsgefilterten Anstieg',
 'Both connected counters show a simultaneous rise': 'Beide verbundenen Zähler zeigen gleichzeitig einen Anstieg',
 'Broadly compatible with Poisson-like spread': 'Weitgehend mit Poisson-ähnlicher Streuung vereinbar',
 'CPM': 'CPM',
 'CPM and derived dose rate': 'CPM und abgeleitete Dosisleistung',
 'CPM distribution and Poisson comparison': 'CPM-Verteilung und Poisson-Vergleich',
 'CPM distribution — {title}': 'CPM-Verteilung — {title}',
 'CPM is the primary measurement.': 'CPM ist der primäre Messwert.',
 'CPM per µSv/h': 'CPM je µSv/h',
 'CPM quality': 'CPM-Qualität',
 'CPM statistics  min {minimum:.0f} | max {maximum:.0f} | mean {mean:.2f} | median {median:.2f} | SD {sd:.2f} | P95 {p95:.2f} | missing {missing}': 'CPM-Statistik  '
                                                                                                                                                    'Min. '
                                                                                                                                                    '{minimum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'Max. '
                                                                                                                                                    '{maximum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'Mittel '
                                                                                                                                                    '{mean:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'Median '
                                                                                                                                                    '{median:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'SD '
                                                                                                                                                    '{sd:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'P95 '
                                                                                                                                                    '{p95:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'fehlend '
                                                                                                                                                    '{missing}',
 'CPM statistics: no accepted measurements in selected period': 'CPM-Statistik: Im gewählten Zeitraum liegen keine '
                                                                'akzeptierten Messwerte vor',
 'CPM–pressure correlation': 'CPM–Luftdruck-Korrelation',
 'CPM–temperature correlation': 'CPM–Temperatur-Korrelation',
 'CPM–voltage correlation': 'CPM–Spannungs-Korrelation',
 'CSV files preserve every accepted measurement without interpolation. PNG reports include CPM, temperature, voltage, optional raw signed gyro diagnostics, summary statistics, sample completeness, device identity, timezone, period and generation time. ZIP bundles additionally contain analysis JSON, daily summaries, events, histogram, heatmap and a multi-page PDF report.': 'CSV-Dateien '
                                                                                                                                                                                                                                                                                                                                                                                       'enthalten '
                                                                                                                                                                                                                                                                                                                                                                                       'jeden '
                                                                                                                                                                                                                                                                                                                                                                                       'akzeptierten '
                                                                                                                                                                                                                                                                                                                                                                                       'Messwert '
                                                                                                                                                                                                                                                                                                                                                                                       'ohne '
                                                                                                                                                                                                                                                                                                                                                                                       'Interpolation. '
                                                                                                                                                                                                                                                                                                                                                                                       'PNG-Berichte '
                                                                                                                                                                                                                                                                                                                                                                                       'enthalten '
                                                                                                                                                                                                                                                                                                                                                                                       'CPM, '
                                                                                                                                                                                                                                                                                                                                                                                       'Temperatur, '
                                                                                                                                                                                                                                                                                                                                                                                       'Spannung, '
                                                                                                                                                                                                                                                                                                                                                                                       'optional '
                                                                                                                                                                                                                                                                                                                                                                                       'signierte '
                                                                                                                                                                                                                                                                                                                                                                                       'Gyro-Rohdiagnosen, '
                                                                                                                                                                                                                                                                                                                                                                                       'Zusammenfassungsstatistiken, '
                                                                                                                                                                                                                                                                                                                                                                                       'Datenabdeckung, '
                                                                                                                                                                                                                                                                                                                                                                                       'Geräteidentität, '
                                                                                                                                                                                                                                                                                                                                                                                       'Zeitzone, '
                                                                                                                                                                                                                                                                                                                                                                                       'Zeitraum '
                                                                                                                                                                                                                                                                                                                                                                                       'und '
                                                                                                                                                                                                                                                                                                                                                                                       'Erstellungszeit. '
                                                                                                                                                                                                                                                                                                                                                                                       'ZIP-Pakete '
                                                                                                                                                                                                                                                                                                                                                                                       'enthalten '
                                                                                                                                                                                                                                                                                                                                                                                       'zusätzlich '
                                                                                                                                                                                                                                                                                                                                                                                       'Analyse-JSON, '
                                                                                                                                                                                                                                                                                                                                                                                       'Tageszusammenfassungen, '
                                                                                                                                                                                                                                                                                                                                                                                       'Ereignisse, '
                                                                                                                                                                                                                                                                                                                                                                                       'Histogramm, '
                                                                                                                                                                                                                                                                                                                                                                                       'Heatmap '
                                                                                                                                                                                                                                                                                                                                                                                       'und '
                                                                                                                                                                                                                                                                                                                                                                                       'einen '
                                                                                                                                                                                                                                                                                                                                                                                       'mehrseitigen '
                                                                                                                                                                                                                                                                                                                                                                                       'PDF-Bericht.',
 'Calibrated acceleration': 'Kalibrierte Beschleunigung',
 'Calibration profile': 'Kalibrierprofil',
 'Capabilities': 'Fähigkeiten',
 'Check location, orientation and environmental conditions when a persistent jump appears.': 'Prüfe bei einem '
                                                                                             'anhaltenden Sprung '
                                                                                             'Standort, Ausrichtung '
                                                                                             'und '
                                                                                             'Umgebungsbedingungen.',
 'Check manually': 'Manuell prüfen',
 'Check the Home Assistant general settings and restart the add-on.': 'Prüfe die allgemeinen '
                                                                      'Home-Assistant-Einstellungen und starte das '
                                                                      'Add-on neu.',
 'Check the USB cable and power supply if this continues for more than 15 minutes.': 'Prüfe USB-Kabel und '
                                                                                     'Stromversorgung, wenn dies '
                                                                                     'länger als 15 Minuten anhält.',
 'Check the measurement conditions, observe the trend and verify the reading with an appropriate instrument if it persists.': 'Prüfe '
                                                                                                                              'die '
                                                                                                                              'Messbedingungen, '
                                                                                                                              'beobachte '
                                                                                                                              'den '
                                                                                                                              'Verlauf '
                                                                                                                              'und '
                                                                                                                              'bestätige '
                                                                                                                              'den '
                                                                                                                              'Wert '
                                                                                                                              'bei '
                                                                                                                              'anhaltender '
                                                                                                                              'Erhöhung '
                                                                                                                              'mit '
                                                                                                                              'einem '
                                                                                                                              'geeigneten '
                                                                                                                              'Messgerät.',
 'Check the measurement location': 'Messort prüfen',
 'Choose counters by detected device name. The technical Linux path remains visible only for identification.': 'Wähle '
                                                                                                               'die '
                                                                                                               'Zähler '
                                                                                                               'anhand '
                                                                                                               'des '
                                                                                                               'erkannten '
                                                                                                               'Gerätenamens. '
                                                                                                               'Der '
                                                                                                               'technische '
                                                                                                               'Linux-Pfad '
                                                                                                               'bleibt '
                                                                                                               'nur '
                                                                                                               'zur '
                                                                                                               'eindeutigen '
                                                                                                               'Identifikation '
                                                                                                               'sichtbar.',
 'Choose how much detail the analysis cards show. The selection is stored in this browser.': 'Lege fest, wie viele '
                                                                                             'Details die '
                                                                                             'Analysekarten zeigen. '
                                                                                             'Die Auswahl wird in '
                                                                                             'diesem Browser '
                                                                                             'gespeichert.',
 'Choose whether reports include all devices or one selected device.': 'Lege fest, ob Berichte alle Geräte oder nur '
                                                                       'ein ausgewähltes Gerät enthalten.',
 'Clear': 'Leeren',
 'Clearly above the usual local range': 'Deutlich über dem üblichen lokalen Bereich',
 'Clearly elevated': 'Deutlich erhöht',
 'Clearly elevated: clearly above the usual local range': 'Deutlich erhöht: deutlich über dem üblichen lokalen '
                                                          'Bereich',
 'Clock offset exceeds warning threshold': 'Zeitabweichung überschreitet Warnschwelle',
 'Clock synchronized': 'Uhr synchron',
 'Close to Poisson expectation': 'Nahe an der Poisson-Erwartung',
 'Co-location and equal geometry must be ensured by the user': 'Gleicher Standort und gleiche Messgeometrie müssen '
                                                               'durch den Benutzer sichergestellt werden',
 'Collapse all': 'Alle einklappen',
 'Combines recent trend, robust statistics, device agreement and learned background. It is a statistical aid, not a safety classification.': 'Kombiniert '
                                                                                                                                             'den '
                                                                                                                                             'jüngsten '
                                                                                                                                             'Trend, '
                                                                                                                                             'robuste '
                                                                                                                                             'Statistik, '
                                                                                                                                             'Geräteübereinstimmung '
                                                                                                                                             'und '
                                                                                                                                             'den '
                                                                                                                                             'gelernten '
                                                                                                                                             'Hintergrund. '
                                                                                                                                             'Dies '
                                                                                                                                             'ist '
                                                                                                                                             'eine '
                                                                                                                                             'statistische '
                                                                                                                                             'Hilfe '
                                                                                                                                             'und '
                                                                                                                                             'keine '
                                                                                                                                             'Sicherheitsklassifikation.',
 'Compared with local baseline': 'Verglichen mit der lokalen Baseline',
 'Compares connected counters, device stability, shared events and the long-term relative response.': 'Vergleicht '
                                                                                                      'verbundene '
                                                                                                      'Zähler, '
                                                                                                      'Gerätestabilität, '
                                                                                                      'gemeinsame '
                                                                                                      'Ereignisse '
                                                                                                      'und das '
                                                                                                      'langfristige '
                                                                                                      'relative '
                                                                                                      'Ansprechverhältnis.',
 'Compares pressure changes with quality-filtered counts. The result is only a statistical hint and never changes warning thresholds.': 'Vergleicht '
                                                                                                                                        'Luftdruckänderungen '
                                                                                                                                        'mit '
                                                                                                                                        'qualitätsgefilterten '
                                                                                                                                        'Zählwerten. '
                                                                                                                                        'Das '
                                                                                                                                        'Ergebnis '
                                                                                                                                        'ist '
                                                                                                                                        'nur '
                                                                                                                                        'ein '
                                                                                                                                        'statistischer '
                                                                                                                                        'Hinweis '
                                                                                                                                        'und '
                                                                                                                                        'verändert '
                                                                                                                                        'niemals '
                                                                                                                                        'Warnschwellen.',
 'Compares the current value with the usual background at this location.': 'Vergleicht den aktuellen Wert mit dem '
                                                                           'üblichen Hintergrund an diesem Standort.',
 'Comparison confidence': 'Vertrauensniveau des Vergleichs',
 'Complete ZIP bundle': 'Vollständiges ZIP-Paket',
 'Complete history deletion failed': 'Vollständiges Löschen des Verlaufs fehlgeschlagen',
 'Complete history deletion is disabled in the app configuration.': 'Das vollständige Löschen des Verlaufs ist in '
                                                                    'der Add-on-Konfiguration deaktiviert.',
 'Completeness: {value:.2f}%': 'Vollständigkeit: {value:.2f} %',
 'Confidence': 'Vertrauen',
 'Configured CPM conversion factor': 'Konfigurierter CPM-Umrechnungsfaktor',
 'Configured baud rate': 'Konfigurierte Baudrate',
 'Configured device name': 'Konfigurierter Gerätename',
 'Configured location': 'Konfigurierter Standort',
 'Configured measurement interval': 'Konfiguriertes Messintervall',
 'Confirmed original samples in 24 h · {accepted} stored': 'Bestätigte Originalmessungen in 24 h · {accepted} '
                                                           'gespeichert',
 'Connect two devices to enable comparison.': 'Für den Vergleich müssen zwei Geräte verbunden sein.',
 'Connect two devices to learn a relative response factor.': 'Zwei Geräte verbinden, um einen relativen '
                                                             'Ansprechfaktor zu lernen.',
 'Connected GMC devices': 'Verbundene GMC-Geräte',
 'Connected counters without an active stability warning': 'Verbundene Zähler ohne aktive Stabilitätswarnung',
 'Connected devices': 'Verbundene Geräte',
 'Connection active': 'Verbindung aktiv',
 'Consecutive upload errors': 'Aufeinanderfolgende Uploadfehler',
 'Continue observing': 'Weiter beobachten',
 'Coordinates': 'Koordinaten',
 'Correlation': 'Korrelation',
 'Correlation does not imply causation. Strong values should be investigated over longer periods before drawing conclusions.': 'Korrelation '
                                                                                                                               'bedeutet '
                                                                                                                               'nicht '
                                                                                                                               'Ursache. '
                                                                                                                               'Starke '
                                                                                                                               'Zusammenhänge '
                                                                                                                               'sollten '
                                                                                                                               'über '
                                                                                                                               'längere '
                                                                                                                               'Zeiträume '
                                                                                                                               'geprüft '
                                                                                                                               'werden, '
                                                                                                                               'bevor '
                                                                                                                               'Schlussfolgerungen '
                                                                                                                               'gezogen '
                                                                                                                               'werden.',
 'Cosmic influence is possible': 'Kosmischer Einfluss möglich',
 'Cosmic influence – statistical indication': 'Kosmischer Einfluss – statistischer Hinweis',
 'Counter ID': 'Zähler-ID',
 'Counting statistics': 'Zählstatistik',
 'Counting uncertainty (68%): −{minus:.2f}/+{plus:.2f} CPM · {impulses} impulses in {duration}': 'Zählunsicherheit '
                                                                                                 '(68 %): '
                                                                                                 '−{minus:.2f}/+{plus:.2f} '
                                                                                                 'CPM · {impulses} '
                                                                                                 'Impulse in '
                                                                                                 '{duration}',
 'Counting uncertainty not available': 'Zählunsicherheit nicht verfügbar',
 'Country': 'Land',
 'Coverage percent': 'Abdeckung in Prozent',
 'Coverage, gaps, runtime counters and derived dose-rate values': 'Abdeckung, Lücken, Laufzeitzähler und abgeleitete '
                                                                  'Dosisleistung',
 'Critical': 'Kritisch',
 'Critical: danger threshold exceeded': 'Kritisch: Gefahrenschwelle überschritten',
 'Current': 'Aktuell',
 'Current air pressure': 'Aktueller Luftdruck',
 'Current database size': 'Aktuelle Datenbankgröße',
 'Current difference': 'Aktuelle Differenz',
 'Current value': 'Aktueller Wert',
 'Current value is {z:+.2f} robust standard deviations from the 24 h median': 'Der aktuelle Wert liegt {z:+.2f} '
                                                                              'robuste Standardabweichungen vom '
                                                                              '24-h-Median entfernt',
 'Current value is {z:+.2f} standard deviations from the 24 h mean': 'Der aktuelle Wert liegt {z:+.2f} '
                                                                     'Standardabweichungen vom 24-h-Mittel entfernt',
 'Current week bundle': 'Paket der laufenden Woche',
 'Currently selected': 'Aktuell ausgewählt',
 'Custom period': 'Eigener Zeitraum',
 'Custom thresholds': 'Benutzerdefinierte Grenzwerte',
 'Daily and weekly profile is still being formed': 'Tages- und Wochenprofil wird noch gebildet',
 'Daily quality-filtered medians are smoothed over seven days. The period cards compare the recent part of each period with the preceding part; detected jumps are statistical changes and do not determine their cause.': 'Tägliche '
                                                                                                                                                                                                                           'qualitätsgefilterte '
                                                                                                                                                                                                                           'Mediane '
                                                                                                                                                                                                                           'werden '
                                                                                                                                                                                                                           'über '
                                                                                                                                                                                                                           'sieben '
                                                                                                                                                                                                                           'Tage '
                                                                                                                                                                                                                           'geglättet. '
                                                                                                                                                                                                                           'Die '
                                                                                                                                                                                                                           'Zeitraumkarten '
                                                                                                                                                                                                                           'vergleichen '
                                                                                                                                                                                                                           'den '
                                                                                                                                                                                                                           'jüngsten '
                                                                                                                                                                                                                           'Teil '
                                                                                                                                                                                                                           'eines '
                                                                                                                                                                                                                           'Zeitraums '
                                                                                                                                                                                                                           'mit '
                                                                                                                                                                                                                           'dem '
                                                                                                                                                                                                                           'vorherigen; '
                                                                                                                                                                                                                           'erkannte '
                                                                                                                                                                                                                           'Sprünge '
                                                                                                                                                                                                                           'sind '
                                                                                                                                                                                                                           'statistische '
                                                                                                                                                                                                                           'Änderungen '
                                                                                                                                                                                                                           'und '
                                                                                                                                                                                                                           'bestimmen '
                                                                                                                                                                                                                           'nicht '
                                                                                                                                                                                                                           'deren '
                                                                                                                                                                                                                           'Ursache.',
 'Daily summary CSV': 'Tageszusammenfassungs-CSV',
 'Danger threshold exceeded': 'Gefahrenschwelle überschritten',
 'Danger thresholds': 'Gefahrenschwellen',
 'Danger zone': 'Gefahrenbereich',
 'Dashboard navigation': 'Dashboard-Navigation',
 'Data exports': 'Datenexporte',
 'Data period': 'Datenzeitraum',
 'Data quality': 'Datenqualität',
 'Data quality is too low for a reliable assessment': 'Die Datenqualität ist für eine belastbare Bewertung noch zu '
                                                      'gering',
 'Data quality status unavailable': 'Datenqualitätsstatus nicht verfügbar',
 'Data quality: {value}': 'Datenqualität: {value}',
 'Database': 'Datenbank',
 'Database health': 'Datenbankzustand',
 'Database size': 'Datenbankgröße',
 'Date': 'Datum',
 'Delete all GMC history': 'Gesamten GMC-Verlauf löschen',
 'Delete history': 'Historie löschen',
 'Deletion confirmation text must be exactly DELETE ALL GMC HISTORY': 'Der Bestätigungstext muss exakt DELETE ALL '
                                                                      'GMC HISTORY lauten',
 'Deletion is disabled by default.': 'Das Löschen ist standardmäßig deaktiviert.',
 'Derived dose rate': 'Abgeleitete Dosisleistung',
 'Derived from 1 h mean CPM': 'Aus dem 1-h-CPM-Mittel abgeleitet',
 'Derived from 24 h mean CPM': 'Aus dem 24-h-CPM-Mittel abgeleitet',
 'Derived from 7 d mean CPM': 'Aus dem 7-Tage-CPM-Mittel abgeleitet',
 'Derived from latest CPM': 'Aus dem letzten CPM-Wert abgeleitet',
 'Detailed interpretation and the most useful supporting values': 'Ausführliche Einordnung und die wichtigsten '
                                                                  'unterstützenden Werte',
 'Detect, identify and assign GMC counters': 'GMC-Zähler erkennen, identifizieren und zuordnen',
 'Detected': 'Erkannt',
 'Detected Capabilities': 'Erkannte Fähigkeiten',
 'Detected GMC device': 'Erkanntes GMC-Gerät',
 'Detected baseline jumps': 'Erkannte Baseline-Sprünge',
 'Detected relative anomaly events: {count}': 'Erkannte relative Anomalieereignisse: {count}',
 'Deviation': 'Abweichung',
 'Device': 'Gerät',
 'Device Profile': 'Geräteprofil',
 'Device Time Errors Since Start': 'Fehler der Gerätezeit seit Start',
 'Device assignments saved': 'Gerätezuordnungen gespeichert',
 'Device assignments were saved.': 'Die Gerätezuordnungen wurden gespeichert.',
 'Device baseline': 'Geräte-Baseline',
 'Device capabilities': 'Gerätefähigkeiten',
 'Device clock': 'Geräteuhr',
 'Device clock offset': 'Abweichung der Geräteuhr',
 'Device clock status': 'Status der Geräteuhr',
 'Device clock unavailable': 'Geräteuhr nicht verfügbar',
 'Device clock warning': 'Warnung zur Geräteuhr',
 'Device comparison': 'Gerätevergleich',
 'Device details, live values and analysis selection are shown below.': 'Gerätedetails, aktuelle Messwerte und die '
                                                                        'Auswahl für die Analyse werden hier '
                                                                        'angezeigt.',
 'Device health warning': 'Warnung zum Gerätezustand',
 'Device position': 'Gerätelage',
 'Device status updated': 'Gerätestatus aktualisiert',
 'Device temperature is unavailable.': 'Die Gerätetemperatur ist nicht verfügbar.',
 'Device time': 'Gerätezeit',
 'Device-specific details are listed above.': 'Gerätespezifische Details stehen im Gerätebereich oben.',
 'Device: {value}': 'Gerät: {value}',
 'Devices': 'Geräte',
 'Diagnostics JSON': 'Diagnose-JSON',
 'Disabled': 'Deaktiviert',
 'Discarded CPM peaks': 'Verworfene CPM-Spitzen',
 'Discarded unconfirmed CPM peaks': 'Verworfene unbestätigte CPM-Spitzen',
 'Display down': 'Flach, Display unten',
 'Display up': 'Flach, Display oben',
 'Dose rate = CPM / configured conversion factor ({factor:g} CPM per µSv/h).': 'Dosisleistung = CPM / konfigurierter '
                                                                               'Umrechnungsfaktor ({factor:g} CPM je '
                                                                               'µSv/h).',
 'Dose rate formula explanation': 'Dosisleistung = CPM / konfigurierter Umrechnungsfaktor ({factor:g} CPM je µSv/h).',
 'Dose-rate values are derived from CPM using the configured conversion factor.': 'Dosisleistungswerte werden mit '
                                                                                  'dem konfigurierten '
                                                                                  'Umrechnungsfaktor aus CPM '
                                                                                  'abgeleitet.',
 'Dose-rate values, traffic-light states and events are derived indicators. CPM remains the primary measurement.': 'Dosisleistungswerte, '
                                                                                                                   'Ampelzustände '
                                                                                                                   'und '
                                                                                                                   'Ereignisse '
                                                                                                                   'sind '
                                                                                                                   'abgeleitete '
                                                                                                                   'Indikatoren. '
                                                                                                                   'CPM '
                                                                                                                   'bleibt '
                                                                                                                   'der '
                                                                                                                   'primäre '
                                                                                                                   'Messwert.',
 'Download': 'Herunterladen',
 'Downloads': 'Downloads',
 'Dual-tube measurement': 'Dual-Tube-Messung',
 'Duration [s]': 'Dauer [s]',
 'During the learning phase, leave the counters in a stable location and allow additional measurements to accumulate.': 'Lasse '
                                                                                                                        'die '
                                                                                                                        'Zähler '
                                                                                                                        'während '
                                                                                                                        'der '
                                                                                                                        'Lernphase '
                                                                                                                        'an '
                                                                                                                        'einem '
                                                                                                                        'stabilen '
                                                                                                                        'Ort '
                                                                                                                        'und '
                                                                                                                        'sammle '
                                                                                                                        'weitere '
                                                                                                                        'Messungen.',
 'Each device has its own MQTT identity and history. The cards show the latest accepted measurement.': 'Jedes Gerät '
                                                                                                       'besitzt eine '
                                                                                                       'eigene '
                                                                                                       'MQTT-Identität '
                                                                                                       'und '
                                                                                                       'Historie. '
                                                                                                       'Die Karten '
                                                                                                       'zeigen den '
                                                                                                       'letzten '
                                                                                                       'akzeptierten '
                                                                                                       'Messwert.',
 'Each physical serial device can only be assigned once': 'Jedes physische serielle Gerät kann nur einmal zugewiesen '
                                                          'werden',
 'Elevated': 'Erhöht',
 'Elevated relative background': 'Erhöhter relativer Hintergrund',
 'Elevated: within warning range': 'Erhöht: im Warnbereich',
 'Elevation': 'Höhe',
 'Enable complete history deletion in the app configuration and restart only when deletion is planned.': 'Aktiviere '
                                                                                                         '„Vollständiges '
                                                                                                         'Löschen '
                                                                                                         'erlauben“ '
                                                                                                         'in der '
                                                                                                         'App-Konfiguration '
                                                                                                         'und starte '
                                                                                                         'die App '
                                                                                                         'nur dann '
                                                                                                         'neu, wenn '
                                                                                                         'eine '
                                                                                                         'Löschung '
                                                                                                         'geplant '
                                                                                                         'ist.',
 'Enable enable_restore in the app configuration and restart only when a restore is planned.': 'Aktiviere '
                                                                                               'enable_restore in '
                                                                                               'der '
                                                                                               'App-Konfiguration '
                                                                                               'und starte die App '
                                                                                               'nur dann neu, wenn '
                                                                                               'eine '
                                                                                               'Wiederherstellung '
                                                                                               'geplant ist.',
 'Enable “{setting}” in the app configuration and restart only when a restore is planned.': 'Aktiviere „{setting}“ '
                                                                                            'in der '
                                                                                            'App-Konfiguration und '
                                                                                            'starte die App nur dann '
                                                                                            'neu, wenn eine '
                                                                                            'Wiederherstellung '
                                                                                            'geplant ist.',
 'End time UTC': 'Endzeit UTC',
 'End time local': 'Endzeit lokal',
 'Entities': 'Entitäten',
 'Environment': 'Umgebung',
 'Error time': 'Fehlerzeitpunkt',
 'Estimated pressure influence': 'Geschätzter Druckeinfluss',
 'Evaluated by': 'Bewertet nach',
 'Evaluates the current value using the configured thresholds.': 'Bewertet den aktuellen Messwert anhand der '
                                                                 'konfigurierten Grenzwerte.',
 'Events CSV': 'Ereignis-CSV',
 'Events and diagnostics': 'Ereignisse und Diagnosedaten',
 'Events last 24 h': 'Ereignisse der letzten 24 h',
 'Excellent': 'Ausgezeichnet',
 'Excluded measurements': 'Ausgeschlossene Messwerte',
 'Excluded pairs': 'Ausgeschlossene Paare',
 'Expand all': 'Alle ausklappen',
 'Expected samples': 'Erwartete Messwerte',
 'Expert view': 'Expertenansicht',
 'Explanation of the two assessments': 'Erklärung der beiden Bewertungen',
 'Export details': 'Exportdetails',
 'Extremely elevated': 'Extrem erhöht',
 'Extremely elevated: far above the usual local range': 'Extrem erhöht: weit über dem üblichen lokalen Bereich',
 'Falling': 'Fallend',
 'Falling air pressure can slightly increase the share of cosmically generated secondary radiation at ground level, while rising air pressure tends to reduce it; the model detects only such statistical relationships and cannot clearly distinguish them from other natural influences.': 'Sinkender '
                                                                                                                                                                                                                                                                                             'Luftdruck '
                                                                                                                                                                                                                                                                                             'kann '
                                                                                                                                                                                                                                                                                             'den '
                                                                                                                                                                                                                                                                                             'Anteil '
                                                                                                                                                                                                                                                                                             'kosmisch '
                                                                                                                                                                                                                                                                                             'erzeugter '
                                                                                                                                                                                                                                                                                             'Sekundärstrahlung '
                                                                                                                                                                                                                                                                                             'am '
                                                                                                                                                                                                                                                                                             'Boden '
                                                                                                                                                                                                                                                                                             'leicht '
                                                                                                                                                                                                                                                                                             'erhöhen, '
                                                                                                                                                                                                                                                                                             'während '
                                                                                                                                                                                                                                                                                             'steigender '
                                                                                                                                                                                                                                                                                             'Luftdruck '
                                                                                                                                                                                                                                                                                             'ihn '
                                                                                                                                                                                                                                                                                             'eher '
                                                                                                                                                                                                                                                                                             'verringert; '
                                                                                                                                                                                                                                                                                             'das '
                                                                                                                                                                                                                                                                                             'Modell '
                                                                                                                                                                                                                                                                                             'erkennt '
                                                                                                                                                                                                                                                                                             'nur '
                                                                                                                                                                                                                                                                                             'solche '
                                                                                                                                                                                                                                                                                             'statistischen '
                                                                                                                                                                                                                                                                                             'Zusammenhänge '
                                                                                                                                                                                                                                                                                             'und '
                                                                                                                                                                                                                                                                                             'kann '
                                                                                                                                                                                                                                                                                             'andere '
                                                                                                                                                                                                                                                                                             'natürliche '
                                                                                                                                                                                                                                                                                             'Einflüsse '
                                                                                                                                                                                                                                                                                             'nicht '
                                                                                                                                                                                                                                                                                             'eindeutig '
                                                                                                                                                                                                                                                                                             'davon '
                                                                                                                                                                                                                                                                                             'trennen.',
 'Falling air pressure is often associated with a slightly higher intensity of cosmically generated secondary radiation at ground level, while rising air pressure is associated with a slightly lower intensity. The strength of this relationship depends on detector, location and atmosphere; the cause cannot be determined unambiguously from total counts.': 'Sinkender '
                                                                                                                                                                                                                                                                                                                                                                    'Luftdruck '
                                                                                                                                                                                                                                                                                                                                                                    'ist '
                                                                                                                                                                                                                                                                                                                                                                    'häufig '
                                                                                                                                                                                                                                                                                                                                                                    'mit '
                                                                                                                                                                                                                                                                                                                                                                    'einer '
                                                                                                                                                                                                                                                                                                                                                                    'leicht '
                                                                                                                                                                                                                                                                                                                                                                    'höheren '
                                                                                                                                                                                                                                                                                                                                                                    'Intensität '
                                                                                                                                                                                                                                                                                                                                                                    'kosmisch '
                                                                                                                                                                                                                                                                                                                                                                    'erzeugter '
                                                                                                                                                                                                                                                                                                                                                                    'Sekundärstrahlung '
                                                                                                                                                                                                                                                                                                                                                                    'am '
                                                                                                                                                                                                                                                                                                                                                                    'Boden '
                                                                                                                                                                                                                                                                                                                                                                    'verbunden, '
                                                                                                                                                                                                                                                                                                                                                                    'steigender '
                                                                                                                                                                                                                                                                                                                                                                    'Luftdruck '
                                                                                                                                                                                                                                                                                                                                                                    'mit '
                                                                                                                                                                                                                                                                                                                                                                    'einer '
                                                                                                                                                                                                                                                                                                                                                                    'leicht '
                                                                                                                                                                                                                                                                                                                                                                    'niedrigeren. '
                                                                                                                                                                                                                                                                                                                                                                    'Die '
                                                                                                                                                                                                                                                                                                                                                                    'Stärke '
                                                                                                                                                                                                                                                                                                                                                                    'dieses '
                                                                                                                                                                                                                                                                                                                                                                    'Zusammenhangs '
                                                                                                                                                                                                                                                                                                                                                                    'hängt '
                                                                                                                                                                                                                                                                                                                                                                    'von '
                                                                                                                                                                                                                                                                                                                                                                    'Detektor, '
                                                                                                                                                                                                                                                                                                                                                                    'Standort '
                                                                                                                                                                                                                                                                                                                                                                    'und '
                                                                                                                                                                                                                                                                                                                                                                    'Atmosphäre '
                                                                                                                                                                                                                                                                                                                                                                    'ab; '
                                                                                                                                                                                                                                                                                                                                                                    'aus '
                                                                                                                                                                                                                                                                                                                                                                    'den '
                                                                                                                                                                                                                                                                                                                                                                    'Gesamtmesswerten '
                                                                                                                                                                                                                                                                                                                                                                    'lässt '
                                                                                                                                                                                                                                                                                                                                                                    'sich '
                                                                                                                                                                                                                                                                                                                                                                    'die '
                                                                                                                                                                                                                                                                                                                                                                    'Ursache '
                                                                                                                                                                                                                                                                                                                                                                    'nicht '
                                                                                                                                                                                                                                                                                                                                                                    'eindeutig '
                                                                                                                                                                                                                                                                                                                                                                    'bestimmen.',
 'Fano factor': 'Fano-Faktor',
 'Fano factor = variance / mean; a value near 1 is consistent with Poisson-like counting statistics.': 'Fano-Faktor '
                                                                                                       '= Varianz / '
                                                                                                       'Mittelwert; '
                                                                                                       'ein Wert '
                                                                                                       'nahe 1 ist '
                                                                                                       'mit '
                                                                                                       'Poisson-ähnlicher '
                                                                                                       'Zählstatistik '
                                                                                                       'vereinbar.',
 'Fano factor formula explanation': 'Fano-Faktor = Varianz / Mittelwert; ein Wert nahe 1 ist mit Poisson-ähnlicher '
                                    'Zählstatistik vereinbar.',
 'Fano factor: {value}': 'Fano-Faktor: {value}',
 'Far above the usual local range': 'Weit über dem üblichen lokalen Bereich',
 'File size': 'Dateigröße',
 'Firmware version': 'Firmwareversion',
 'Flat': 'Flach',
 'Fleet intelligence': 'Geräteverbund-Auswertung',
 'Format': 'Format',
 'Fri': 'Fr',
 'Friday': 'Freitag',
 'Full history ZIP': 'Vollständiges Historien-ZIP',
 'GMC Radiation Monitor': 'GMC-Strahlungsmonitor',
 'GMC Radiation Monitoring': 'GMC-Strahlungsüberwachung',
 'GMC Reports': 'GMC-Berichte',
 'GMC analysis report {period}': 'GMC-Analysebericht {period}',
 'GMC detected': 'GMC erkannt',
 'GMC devices are being detected automatically': 'GMC-Geräte werden automatisch erkannt',
 'GMC radiation analysis report': 'GMC-Strahlungsanalysebericht',
 'GMC radiation monitoring report {period}': 'GMC-Strahlungsüberwachungsbericht {period}',
 'GMC-300/320 family': 'GMC-300/320-Familie',
 'GMC-320 and GMC-500+ combined': 'GMC-320 und GMC-500+ kombiniert',
 'GMC-500 family': 'GMC-500-Familie',
 'GMC-600 family': 'GMC-600-Familie',
 'GMCMap consecutive upload errors': 'Aufeinanderfolgende GMCMap-Uploadfehler',
 'GMCMap counter ID': 'GMCMap-Zähler-ID',
 'GMCMap is enabled, but this device has no counter ID mapping.': 'GMCMap ist aktiviert, aber diesem Gerät ist keine '
                                                                  'Zähler-ID zugeordnet.',
 'GMCMap last HTTP status': 'Letzter GMCMap-HTTP-Status',
 'GMCMap last error time': 'Zeitpunkt des letzten GMCMap-Fehlers',
 'GMCMap last server response': 'Letzte GMCMap-Serverantwort',
 'GMCMap last successful upload': 'Letzter erfolgreicher GMCMap-Upload',
 'GMCMap last upload attempt': 'Letzter GMCMap-Uploadversuch',
 'GMCMap last upload error': 'Letzter GMCMap-Uploadfehler',
 'GMCMap last uploaded CPM': 'Zuletzt an GMCMap übertragene CPM',
 'GMCMap next upload': 'Nächster GMCMap-Upload',
 'GMCMap successful uploads since start': 'Erfolgreiche GMCMap-Uploads seit Start',
 'GMCMap upload errors since start': 'GMCMap-Uploadfehler seit Start',
 'GMCMap upload status': 'GMCMap-Uploadstatus',
 'GQ manufacturer recommendation': 'GQ-Empfehlung',
 'Gaps are excluded from effective counting time': 'Messlücken zählen nicht zur effektiven Messdauer',
 'Generated export exceeds the {limit_mib} MiB safety limit': 'Der erzeugte Export überschreitet die '
                                                              'Sicherheitsgrenze von {limit_mib} MiB.',
 'Generated maintenance export exceeds the 128 MiB safety limit': 'Der erzeugte Wartungsexport überschreitet die '
                                                                  'Sicherheitsgrenze von 128 MiB.',
 'Generated report exceeds the 64 MiB safety limit': 'Der erzeugte Bericht überschreitet die Sicherheitsgrenze von '
                                                     '64 MiB',
 'Generic GQ GMC / RFC1201-compatible device': 'Generisches GQ-GMC-/RFC1201-kompatibles Gerät',
 'Generic RFC1201-compatible device': 'Generisches RFC1201-kompatibles Gerät',
 'Global report settings': 'Globale Berichts- und Exporteinstellungen',
 'Good': 'Gut',
 'Green': 'Grün',
 'Gyro Calibrated {axis}': 'Gyro kalibriert {axis}',
 'Gyro Errors Since Start': 'Gyro-Fehler seit Start',
 'Gyro Raw {axis}': 'Gyro-Rohwert {axis}',
 'Gyro X': 'Gyro X',
 'Gyro Y': 'Gyro Y',
 'Gyro Z': 'Gyro Z',
 'Gyro data will be included when available.': 'Gyrodaten werden einbezogen, sofern sie verfügbar sind.',
 'Gyro errors': 'Gyro-Fehler',
 'Gyro recording is disabled.': 'Die Gyro-Aufzeichnung ist deaktiviert.',
 'Gyroscope': 'Gyroskop',
 'Hardware model': 'Hardwaremodell',
 'Heartbeat Errors Since Start': 'Heartbeat-Fehler seit Start',
 'Heartbeat mode': 'Heartbeat-Modus',
 'Heartbeat rolling 60 s CPM': 'Heartbeat-CPM über 60 s',
 'Heatmap PNG': 'Heatmap-PNG',
 'Heuristic statistical assessment; not a radiation-protection classification.': 'Heuristische statistische '
                                                                                 'Bewertung; keine '
                                                                                 'strahlenschutzfachliche '
                                                                                 'Einstufung.',
 'High': 'Hoch',
 'High relative increase': 'Starke relative Erhöhung',
 'High-dose Tube CPM': 'Hochdosis-Röhre CPM',
 'High-dose tube': 'Hochdosis-Röhre',
 'Highest stored 24 h value': 'Höchster gespeicherter Wert der letzten 24 h',
 'Histogram PNG': 'Histogramm-PNG',
 'Historical chart is still being formed': 'Historisches Diagramm wird noch aufgebaut',
 'Historical development': 'Historische Entwicklung',
 'History': 'Verlauf',
 'History Write Errors Since Start': 'Fehler beim Schreiben der Historie seit Start',
 'History deleted': 'Verlauf gelöscht',
 'History maintenance': 'Historienverwaltung',
 'History restore failed': 'Wiederherstellung der Historie fehlgeschlagen',
 'History restore is disabled. Enable enable_restore in the app configuration and restart.': 'Die Wiederherstellung '
                                                                                             'der Historie ist '
                                                                                             'deaktiviert. Aktiviere '
                                                                                             'enable_restore in der '
                                                                                             'App-Konfiguration und '
                                                                                             'starte neu.',
 'History restore is disabled. Enable “{setting}” in the app configuration and restart.': 'Die Wiederherstellung der '
                                                                                          'Historie ist deaktiviert. '
                                                                                          'Aktiviere „{setting}“ in '
                                                                                          'der App-Konfiguration und '
                                                                                          'starte neu.',
 'History storage warning': 'Warnung zur Verlaufsspeicherung',
 'Home Assistant API client is not configured': 'Der Home-Assistant-API-Client ist nicht konfiguriert',
 'Home Assistant Recorder entity patterns': 'Entitätsmuster des Home-Assistant-Recorders',
 'Home Assistant Recorder history cleared': 'Home-Assistant-Recorder-Verlauf gelöscht',
 'Home Assistant host UART': 'UART des Home-Assistant-Hosts',
 'Home Assistant location': 'Home-Assistant-Standort',
 'How are connected counters compared?': 'Wie werden verbundene Zähler verglichen?',
 'How closely the observed spread resembles Poisson-like counting': 'Wie ähnlich die beobachtete Streuung einer '
                                                                    'Poisson-Verteilung ist',
 'How is data quality evaluated?': 'Wie wird die Datenqualität bewertet?',
 'How is the background profile calculated?': 'Wie wird das Hintergrundprofil berechnet?',
 'How is the pressure relationship assessed?': 'Wie wird der Zusammenhang mit dem Luftdruck bewertet?',
 'However, the value is noticeably above the usual local background. Observe the trend.': 'Der Wert liegt jedoch '
                                                                                          'auffällig über dem '
                                                                                          'üblichen lokalen '
                                                                                          'Hintergrund. Beobachte '
                                                                                          'den Verlauf.',
 'ICRP reference projection': 'ICRP-Referenzprojektion',
 'Inclination': 'Neigung',
 'Ingest diagnostics cleared': 'Import-Diagnosedaten gelöscht',
 'Inspecting backup…': 'Sicherung wird geprüft …',
 'Insufficient': 'Unzureichend',
 'Insufficient history for level-shift detection': 'Noch nicht genügend Verlauf für die Niveauwechsel-Erkennung',
 'Insufficient paired daily values': 'Nicht genügend vergleichbare Tageswerte',
 'Integrity': 'Integrität',
 'Intelligence': 'Intelligente Auswertung',
 'Intelligent radiation analysis': 'Intelligente Strahlungsanalyse',
 'Internal database cleared': 'Interne Datenbank geleert',
 'Internal serial port': 'Interner serieller Anschluss',
 'Interpret statistics with coverage in mind': 'Statistiken unter Berücksichtigung der Abdeckung interpretieren',
 'Interpret these values together with coverage, device stability and the historical background.': 'Interpretiere '
                                                                                                   'diese Werte '
                                                                                                   'gemeinsam mit '
                                                                                                   'Datenabdeckung, '
                                                                                                   'Gerätestabilität '
                                                                                                   'und historischem '
                                                                                                   'Hintergrund.',
 'Interpretation': 'Interpretation',
 'Interval diagnostics': 'Intervall-Diagnose',
 'Invalid deletion confirmation': 'Ungültige Löschbestätigung',
 'Invalid device clock response': 'Ungültige Antwort der Geräteuhr',
 'Invalid request parameters': 'Ungültige Anfrageparameter.',
 'Invalid serial configuration request': 'Ungültige Anfrage zur seriellen Konfiguration',
 'Keep both counters close together and similarly oriented when using the comparison as a reference.': 'Platziere '
                                                                                                       'beide Zähler '
                                                                                                       'nah '
                                                                                                       'beieinander '
                                                                                                       'und ähnlich '
                                                                                                       'ausgerichtet, '
                                                                                                       'wenn der '
                                                                                                       'Vergleich '
                                                                                                       'als Referenz '
                                                                                                       'dienen soll.',
 'Known radio or Zigbee adapter': 'Bekannter Funk- oder Zigbee-Adapter',
 'Language': 'Sprache',
 'Last HTTP status': 'Letzter HTTP-Status',
 'Last Successful Measurement': 'Letzte erfolgreiche Messung',
 'Last attempt': 'Letzter Versuch',
 'Last backup requested in this browser': 'Letzte in diesem Browser angeforderte Sicherung',
 'Last sample age': 'Alter des letzten Messwerts',
 'Last server response': 'Letzte Serverantwort',
 'Last successful storage': 'Letzte erfolgreiche Speicherung',
 'Last update': 'Letzte Aktualisierung',
 'Last upload': 'Letzter Upload',
 'Last upload error': 'Letzter Uploadfehler',
 'Latest CPM': 'Aktuelle CPM',
 'Latest CPM uncertainty': 'Unsicherheit des letzten CPM-Werts',
 'Latest CPM vs 24 h distribution': 'Letzter CPM-Wert im Vergleich zur 24-h-Verteilung',
 'Latest accepted value': 'Letzter akzeptierter Wert',
 'Latest dose rate': 'Aktuelle Dosisleistung',
 'Latest measurement': 'Letzter Messwert',
 'Learned Radiation Baseline': 'Erlernte Strahlungs-Baseline',
 'Learned from local history': 'Aus dem lokalen Verlauf gelernt',
 'Learned pressure coefficient': 'Gelernter Druckkoeffizient',
 'Learning baseline': 'Baseline wird gebildet',
 'Learning basis': 'Lerngrundlage',
 'Learning progress': 'Lernfortschritt',
 'Learning: not enough local history yet': 'Lernt noch: noch nicht genügend lokale Verlaufsdaten',
 'Learning: {pairs}/{minimum} pairs · {days:.1f}/{minimum_days:g} days': 'Lernen: {pairs}/{minimum} Paare · '
                                                                         '{days:.1f}/{minimum_days:g} Tage',
 'Learns typical values for the current hour, weekday and temperature range and shows long-term drift.': 'Lernt '
                                                                                                         'typische '
                                                                                                         'Werte für '
                                                                                                         'die '
                                                                                                         'aktuelle '
                                                                                                         'Stunde, '
                                                                                                         'den '
                                                                                                         'Wochentag '
                                                                                                         'und den '
                                                                                                         'Temperaturbereich '
                                                                                                         'und zeigt '
                                                                                                         'langfristige '
                                                                                                         'Drift.',
 'Less variable than Poisson expectation': 'Weniger variabel als die Poisson-Erwartung',
 'Likely device-specific deviation': 'Wahrscheinlich gerätespezifische Abweichung',
 'Limited': 'Eingeschränkt',
 'Live radiation CPS': 'Live-Strahlung CPS',
 'Live system status': 'Live-Systemstatus',
 'Local background analysis': 'Lokale Hintergrundanalyse',
 'Local background is still being learned': 'Der lokale Hintergrund wird noch ermittelt',
 'Local background model is available': 'Das lokale Hintergrundmodell ist verfügbar',
 'Local baseline': 'Lokale Baseline',
 'Local hour': 'Lokale Stunde',
 'Local time [{timezone}]': 'Lokale Zeit [{timezone}]',
 'Local timestamp': 'Lokaler Zeitstempel',
 'Location data comes from the Home Assistant general settings and is not sent to an external geocoding service.': 'Die '
                                                                                                                   'Standortdaten '
                                                                                                                   'stammen '
                                                                                                                   'aus '
                                                                                                                   'den '
                                                                                                                   'allgemeinen '
                                                                                                                   'Home-Assistant-Einstellungen '
                                                                                                                   'und '
                                                                                                                   'werden '
                                                                                                                   'nicht '
                                                                                                                   'an '
                                                                                                                   'einen '
                                                                                                                   'externen '
                                                                                                                   'Geokodierungsdienst '
                                                                                                                   'gesendet.',
 'Location unavailable': 'Standort nicht verfügbar',
 'Long-term context': 'Langzeitkontext',
 'Long-term drift': 'Langzeitdrift',
 'Long-term relative factor available': 'Langfristiger relativer Faktor verfügbar',
 'Long-term relative response': 'Langfristiges relatives Ansprechverhältnis',
 'Longest gap': 'Längste Messlücke',
 'Longest gap [s]': 'Längste Lücke [s]',
 'Longest gap: {seconds} s': 'Längste Lücke: {seconds} s',
 'Low': 'Niedrig',
 'Low-dose Tube CPM': 'Niedrigdosis-Röhre CPM',
 'Low-dose tube': 'Niedrigdosis-Röhre',
 'Lowest stored 24 h value': 'Niedrigster gespeicherter Wert der letzten 24 h',
 'Machine-readable statistics and event data': 'Maschinenlesbare Statistiken und Ereignisdaten',
 'Maximum': 'Maximum',
 'Maximum CPM': 'Maximale CPM',
 'Maximum background index [%]': 'Maximaler Hintergrundindex [%]',
 'Mean': 'Mittelwert',
 'Mean CPM': 'Mittlere CPM',
 'Mean CPM by weekday and hour — {title}': 'Mittlere CPM nach Wochentag und Stunde — {title}',
 'Mean absolute difference': 'Mittlere absolute Abweichung',
 'Mean: {value} CPM': 'Mittelwert: {value} CPM',
 'Measurement interval': 'Messintervall',
 'Measurement-site baseline': 'Verbund-Baseline des Messorts',
 'Measurements': 'Messwerte',
 'Measurements are sent to the public GMCMap service.': 'Messwerte werden an den öffentlichen GMCMap-Dienst '
                                                        'gesendet.',
 'Measurements to delete': 'Zu löschende Messwerte',
 'Median': 'Median',
 'Median CPM': 'Median-CPM',
 'Median: {value} CPM': 'Median: {value} CPM',
 'Medium': 'Mittel',
 'Merge a compatible SQLite backup into the current history. Existing rows are preserved or updated by device serial and UTC timestamp.': 'Eine '
                                                                                                                                          'kompatible '
                                                                                                                                          'SQLite-Sicherung '
                                                                                                                                          'in '
                                                                                                                                          'die '
                                                                                                                                          'aktuelle '
                                                                                                                                          'Historie '
                                                                                                                                          'zusammenführen. '
                                                                                                                                          'Bestehende '
                                                                                                                                          'Zeilen '
                                                                                                                                          'bleiben '
                                                                                                                                          'erhalten '
                                                                                                                                          'oder '
                                                                                                                                          'werden '
                                                                                                                                          'nach '
                                                                                                                                          'Geräteseriennummer '
                                                                                                                                          'und '
                                                                                                                                          'UTC-Zeitstempel '
                                                                                                                                          'aktualisiert.',
 'Merged {rows} measurement rows from schema {schema}.': '{rows} Messwertzeilen aus Schema {schema} wurden '
                                                         'zusammengeführt.',
 'Minimum / maximum: {minimum} / {maximum} CPM': 'Minimum / Maximum: {minimum} / {maximum} CPM',
 'Minimum CPM': 'Minimale CPM',
 'Mixed device profiles': 'Gemischte Geräteprofile',
 'Moderate linear relationship': 'Mittlerer linearer Zusammenhang',
 'Mon': 'Mo',
 'Monday': 'Montag',
 'More history is needed before the relative background indicator is classified.': 'Es werden mehr Verlaufsdaten '
                                                                                   'benötigt, bevor der relative '
                                                                                   'Hintergrundindikator eingestuft '
                                                                                   'wird.',
 'More history is needed; approximately {count} additional measurements are required.': 'Es wird mehr Verlauf '
                                                                                        'benötigt; ungefähr {count} '
                                                                                        'weitere Messwerte sind '
                                                                                        'erforderlich.',
 'More measurements are needed for this weekday and hour.': 'Für diesen Wochentag und diese Stunde werden noch mehr '
                                                            'Messwerte benötigt.',
 'More variable than Poisson expectation': 'Variabler als die Poisson-Erwartung',
 'Move away from the suspected source if safe to do so, avoid unnecessary exposure and seek qualified radiation-protection advice.': 'Entferne '
                                                                                                                                     'dich, '
                                                                                                                                     'sofern '
                                                                                                                                     'gefahrlos '
                                                                                                                                     'möglich, '
                                                                                                                                     'von '
                                                                                                                                     'der '
                                                                                                                                     'vermuteten '
                                                                                                                                     'Quelle, '
                                                                                                                                     'vermeide '
                                                                                                                                     'unnötige '
                                                                                                                                     'Exposition '
                                                                                                                                     'und '
                                                                                                                                     'hole '
                                                                                                                                     'fachkundigen '
                                                                                                                                     'Strahlenschutzrat '
                                                                                                                                     'ein.',
 'Never': 'Nie',
 'Newest sample': 'Neuester Messwert',
 'Next upload': 'Nächster Upload',
 'No GMC device detected': 'Kein GMC-Gerät erkannt',
 'No action is required while the result remains normal. Investigate persistent changes by checking the measurement location and comparing both devices.': 'Solange '
                                                                                                                                                           'das '
                                                                                                                                                           'Ergebnis '
                                                                                                                                                           'normal '
                                                                                                                                                           'bleibt, '
                                                                                                                                                           'ist '
                                                                                                                                                           'keine '
                                                                                                                                                           'Maßnahme '
                                                                                                                                                           'erforderlich. '
                                                                                                                                                           'Prüfe '
                                                                                                                                                           'bei '
                                                                                                                                                           'anhaltenden '
                                                                                                                                                           'Änderungen '
                                                                                                                                                           'den '
                                                                                                                                                           'Messort '
                                                                                                                                                           'und '
                                                                                                                                                           'vergleiche '
                                                                                                                                                           'beide '
                                                                                                                                                           'Geräte.',
 'No action is required. Continue normal monitoring.': 'Keine Maßnahme erforderlich. Setze die normale Überwachung '
                                                       'fort.',
 'No action is required. The assessment becomes more reliable as additional measurements are collected.': 'Keine '
                                                                                                          'Maßnahme '
                                                                                                          'erforderlich. '
                                                                                                          'Mit '
                                                                                                          'weiteren '
                                                                                                          'Messungen '
                                                                                                          'wird die '
                                                                                                          'Bewertung '
                                                                                                          'belastbarer.',
 'No action required': 'Keine Maßnahmen erforderlich',
 'No active device warnings': 'Keine aktiven Gerätewarnungen',
 'No connected GMC device': 'Kein verbundenes GMC-Gerät',
 'No connected counter is available yet. The next serial scan runs automatically.': 'Noch ist kein verbundener '
                                                                                    'Zähler verfügbar. Der nächste '
                                                                                    'serielle Suchlauf startet '
                                                                                    'automatisch.',
 'No connected devices.': 'Keine verbundenen Geräte.',
 'No current pressure source is available': 'Keine aktuelle Luftdruckquelle verfügbar',
 'No data': 'Keine Daten',
 'No known GMC devices': 'Keine bekannten GMC-Geräte',
 'No matching Home Assistant entities': 'Keine passenden Home-Assistant-Entitäten',
 'No measurement yet': 'Noch kein Messwert',
 'No measurements in selected period': 'Keine Messwerte im gewählten Zeitraum',
 'No measurements yet.': 'Noch keine Messwerte.',
 'No persistent level shift detected': 'Kein anhaltender Niveauwechsel erkannt',
 'No position changes recorded.': 'Keine Lageänderungen aufgezeichnet.',
 'No pressure variation': 'Keine ausreichende Luftdruckschwankung',
 'No pressure-typical signature': 'Keine drucktypische Signatur',
 'No pronounced baseline jumps detected.': 'Keine ausgeprägten Baseline-Sprünge erkannt.',
 'No reports have been requested in this browser yet.': 'In diesem Browser wurden noch keine Berichte angefordert.',
 'No shared rise detected.': 'Kein gemeinsamer CPM-Anstieg erkannt.',
 'No stored measurements': 'Keine gespeicherten Messwerte',
 'No suitable serial device was found.': 'Kein geeignetes serielles Gerät gefunden.',
 'No sustained relative anomaly events detected': 'Keine anhaltenden relativen Anomalieereignisse erkannt',
 'No valid CPM baseline': 'Keine gültige CPM-Baseline',
 'Normal': 'Unauffällig',
 'Normal for this time': 'Normal für diese Zeit',
 'Normal: within the usual local range': 'Normal: im üblichen lokalen Bereich',
 'Not available yet — at least two CPM samples are required': 'Noch nicht verfügbar – mindestens zwei CPM-Messwerte '
                                                              'sind erforderlich',
 'Not available yet — more baseline history is required': 'Noch nicht verfügbar – mehr Baseline-Verlauf ist '
                                                          'erforderlich',
 'Not available yet — more paired samples are required': 'Noch nicht verfügbar – weitere Messwertpaare sind '
                                                         'erforderlich',
 'Not available yet — no temperature samples were stored in the current 24 h window.': 'Noch nicht verfügbar – im '
                                                                                       'aktuellen 24-h-Zeitraum '
                                                                                       'wurden keine Temperaturwerte '
                                                                                       'gespeichert.',
 'Not available yet — the 24 h CPM series needs variation and at least two samples': 'Noch nicht verfügbar – die '
                                                                                     '24-h-CPM-Reihe benötigt '
                                                                                     'Streuung und mindestens zwei '
                                                                                     'Messwerte',
 'Not available yet — the 24 h mean and spread are still insufficient': 'Noch nicht verfügbar – 24-h-Mittelwert und '
                                                                        'Streuung reichen noch nicht aus',
 'Not available — CPM did not vary during this period': 'Nicht verfügbar – CPM hat sich in diesem Zeitraum nicht '
                                                        'verändert',
 'Not available — the sensor value did not vary during this period': 'Nicht verfügbar – der Sensorwert hat sich in '
                                                                     'diesem Zeitraum nicht verändert',
 'Not configured': 'Nicht konfiguriert',
 'Not connected': 'Nicht verbunden',
 'Not detected yet': 'Noch nicht erkannt',
 'Not enough local history yet': 'Noch nicht genügend lokale Verlaufsdaten',
 'Not found': 'Nicht gefunden',
 'Not recorded in this browser': 'In diesem Browser nicht erfasst',
 'Not suitable as a GMC device': 'Nicht als GMC-Gerät geeignet',
 'Not suitable for GMC': 'Nicht für GMC geeignet',
 'Not yet checked as a GMC device': 'Noch nicht als GMC-Gerät geprüft',
 'Noticeable': 'Auffällig',
 'Noticeable baseline drift': 'Auffällige Baseline-Drift',
 'Noticeable difference from Poisson-like spread': 'Auffälliger Unterschied zur Poisson-ähnlichen Streuung',
 'Noticeable statistical deviation': 'Auffällige statistische Abweichung',
 'Noticeable: above the usual local range': 'Auffällig: über dem üblichen lokalen Bereich',
 'Number of samples': 'Anzahl der Messwerte',
 'Observed': 'Beobachtet',
 'Observed SD / √mean': 'Beobachtete Standardabweichung / √Mittelwert',
 'Official reference values': 'Offizielle Referenzwerte',
 'Offline': 'Offline',
 'Oldest sample': 'Ältester Messwert',
 'One current weather entity is available': 'Eine aktuelle Wetterentität ist verfügbar',
 'One-hour mean is {deviation:+.1f}% relative to the learned baseline': 'Das 1-Stunden-Mittel liegt '
                                                                        '{deviation:+.1f}% relativ zur erlernten '
                                                                        'Basislinie',
 'One-hour means': '1-Stunden-Mittelwerte',
 'One-hour robust level is {deviation:+.1f}% relative to the device baseline': 'Das robuste 1-Stunden-Niveau liegt '
                                                                               '{deviation:+.1f}% relativ zur '
                                                                               'Geräte-Baseline',
 'Online': 'Online',
 'Only quality-filtered, one-to-one time-matched measurements are compared. Agreement, correlation, relative bias and stability are evaluated separately so one faulty counter does not automatically define the site result.': 'Verglichen '
                                                                                                                                                                                                                                'werden '
                                                                                                                                                                                                                                'nur '
                                                                                                                                                                                                                                'qualitätsgefilterte, '
                                                                                                                                                                                                                                'zeitlich '
                                                                                                                                                                                                                                'eindeutig '
                                                                                                                                                                                                                                'zugeordnete '
                                                                                                                                                                                                                                'Messwerte. '
                                                                                                                                                                                                                                'Übereinstimmung, '
                                                                                                                                                                                                                                'Korrelation, '
                                                                                                                                                                                                                                'relative '
                                                                                                                                                                                                                                'Abweichung '
                                                                                                                                                                                                                                'und '
                                                                                                                                                                                                                                'Stabilität '
                                                                                                                                                                                                                                'werden '
                                                                                                                                                                                                                                'getrennt '
                                                                                                                                                                                                                                'bewertet, '
                                                                                                                                                                                                                                'damit '
                                                                                                                                                                                                                                'ein '
                                                                                                                                                                                                                                'fehlerhafter '
                                                                                                                                                                                                                                'Zähler '
                                                                                                                                                                                                                                'nicht '
                                                                                                                                                                                                                                'automatisch '
                                                                                                                                                                                                                                'das '
                                                                                                                                                                                                                                'Standortergebnis '
                                                                                                                                                                                                                                'bestimmt.',
 'Only the most important conclusions at a glance': 'Nur die wichtigsten Aussagen auf einen Blick',
 'Open': 'Öffnen',
 'Open serial device connections': 'Geräteanschlüsse öffnen',
 'Operational events cleared': 'Betriebsereignisse gelöscht',
 'Orientation cannot be verified automatically': 'Orientierung kann nicht automatisch geprüft werden',
 'Orientation changes detected': 'Orientierungsänderungen erkannt',
 'Orientation data is temporarily unavailable.': 'Lageinformationen sind vorübergehend nicht verfügbar.',
 'Orientation qualification': 'Orientierungsprüfung',
 'Orientation stable': 'Orientierung stabil',
 'Original raw-data CSV': 'Unveränderte Rohdaten-CSV',
 'Outliers and invalid measurements': 'Ausreißer und ungültige Messwerte',
 'Overview': 'Übersicht',
 'P95 CPM': 'P95-CPM',
 'P95: {value} CPM': 'P95: {value} CPM',
 'P99 CPM': 'P99-CPM',
 'P99: {value} CPM': 'P99: {value} CPM',
 'PDF report': 'PDF-Bericht',
 'Pair-level disagreement': 'Abweichung auf Paarebene',
 'Pearson r · n={count} paired samples': 'Pearson-r · n={count} Messwertpaare',
 'Period: {period} ({timezone})': 'Zeitraum: {period} ({timezone})',
 'Permanently delete all GMC history from this app and Home Assistant Recorder. This includes CPM, temperature, voltage, gyro and tube measurements for every known GMC and all time periods.': 'Löscht '
                                                                                                                                                                                                'dauerhaft '
                                                                                                                                                                                                'den '
                                                                                                                                                                                                'gesamten '
                                                                                                                                                                                                'GMC-Verlauf '
                                                                                                                                                                                                'aus '
                                                                                                                                                                                                'dieser '
                                                                                                                                                                                                'App '
                                                                                                                                                                                                'und '
                                                                                                                                                                                                'dem '
                                                                                                                                                                                                'Home-Assistant-Recorder. '
                                                                                                                                                                                                'Dies '
                                                                                                                                                                                                'umfasst '
                                                                                                                                                                                                'CPM, '
                                                                                                                                                                                                'Temperatur, '
                                                                                                                                                                                                'Spannung, '
                                                                                                                                                                                                'Gyro- '
                                                                                                                                                                                                'und '
                                                                                                                                                                                                'Röhrenmesswerte '
                                                                                                                                                                                                'aller '
                                                                                                                                                                                                'bekannten '
                                                                                                                                                                                                'GMCs '
                                                                                                                                                                                                'über '
                                                                                                                                                                                                'alle '
                                                                                                                                                                                                'Zeiträume.',
 'Persistent level shift detected': 'Anhaltender Niveauwechsel erkannt',
 'Pin card': 'Karte anheften',
 'Pitch angle': 'Nickwinkel',
 'Plausibilised from two weather entities': 'Aus zwei Wetterentitäten plausibilisiert',
 'Poisson SD ratio': 'Poisson-SD-Verhältnis',
 'Poisson SD ratio = observed standard deviation / √mean; a value near 1 indicates Poisson-like spread.': 'Poisson-SD-Verhältnis '
                                                                                                          '= '
                                                                                                          'beobachtete '
                                                                                                          'Standardabweichung '
                                                                                                          '/ '
                                                                                                          '√Mittelwert; '
                                                                                                          'ein Wert '
                                                                                                          'nahe 1 '
                                                                                                          'weist auf '
                                                                                                          'Poisson-ähnliche '
                                                                                                          'Streuung '
                                                                                                          'hin.',
 'Poisson SD ratio formula explanation': 'Poisson-SD-Verhältnis = beobachtete Standardabweichung / √Mittelwert; ein '
                                         'Wert nahe 1 weist auf Poisson-ähnliche Streuung hin.',
 'Poisson SD ratio: {value}': 'Poisson-SD-Verhältnis: {value}',
 'Poisson counting interval from the observed impulse count': 'Poisson-Zählintervall aus der beobachteten Impulszahl',
 'Poisson expectation (λ={mean:.2f})': 'Poisson-Erwartung (λ={mean:.2f})',
 'Poor': 'Schlecht',
 'Position change log': 'Lageänderungsprotokoll',
 'Possible GMC connection cable': 'Mögliches GMC-Verbindungskabel',
 'Possible persistent level shift': 'Anhaltender Niveauwechsel möglich',
 'Pressure model is still being formed': 'Luftdruckmodell wird noch gebildet',
 'Pressure model unavailable': 'Luftdruckmodell nicht verfügbar',
 'Pressure-typical signature is pronounced': 'Drucktypische Signatur deutlich',
 'Preview backup': 'Sicherung prüfen',
 'Previous day': 'Vorheriger Tag',
 'Previous week': 'Vorherige Woche',
 'Probable real change': 'Wahrscheinliche reale Änderung',
 'Probable shared measurement-site change': 'Wahrscheinliche gemeinsame Änderung am Messort',
 'Profile': 'Geräteprofil',
 'Profile is still being formed': 'Profil wird noch gebildet',
 'Provider': 'Anbieter',
 'Public GMCMap upload': 'Öffentlicher GMCMap-Upload',
 'Quality weight': 'Qualitätsgewicht',
 'Quality-filtered correlation': 'Qualitätsgefilterte Korrelation',
 'Quality-filtered measurement CSV': 'Qualitätsgefilterte Messwert-CSV',
 'Quick downloads': 'Schnelldownloads',
 'Radiation 1 h Mean': 'Strahlung 1-h-Mittel',
 'Radiation 1 h Median': 'Strahlung 1-h-Median',
 'Radiation 1 h Standard Deviation': 'Strahlung 1-h-Standardabweichung',
 'Radiation Baseline Deviation': 'Strahlungs-Baseline-Abweichung',
 'Radiation CPM': 'Strahlung CPM',
 'Radiation Rapid Change': 'Schnelle Strahlungsänderung',
 'Radiation count rate [CPM]': 'Strahlungszählrate [CPM]',
 'Radiation counts fluctuate naturally. The Fano factor and Poisson spread ratio compare the observed variation with a simple counting-statistics model; they describe distribution shape but not a physical cause or calibration state.': 'Strahlungszählungen '
                                                                                                                                                                                                                                           'schwanken '
                                                                                                                                                                                                                                           'von '
                                                                                                                                                                                                                                           'Natur '
                                                                                                                                                                                                                                           'aus. '
                                                                                                                                                                                                                                           'Fano-Faktor '
                                                                                                                                                                                                                                           'und '
                                                                                                                                                                                                                                           'Poisson-Streuungsverhältnis '
                                                                                                                                                                                                                                           'vergleichen '
                                                                                                                                                                                                                                           'die '
                                                                                                                                                                                                                                           'beobachtete '
                                                                                                                                                                                                                                           'Schwankung '
                                                                                                                                                                                                                                           'mit '
                                                                                                                                                                                                                                           'einem '
                                                                                                                                                                                                                                           'einfachen '
                                                                                                                                                                                                                                           'Zählstatistikmodell; '
                                                                                                                                                                                                                                           'sie '
                                                                                                                                                                                                                                           'beschreiben '
                                                                                                                                                                                                                                           'die '
                                                                                                                                                                                                                                           'Verteilungsform, '
                                                                                                                                                                                                                                           'aber '
                                                                                                                                                                                                                                           'weder '
                                                                                                                                                                                                                                           'eine '
                                                                                                                                                                                                                                           'physikalische '
                                                                                                                                                                                                                                           'Ursache '
                                                                                                                                                                                                                                           'noch '
                                                                                                                                                                                                                                           'den '
                                                                                                                                                                                                                                           'Kalibrierzustand.',
 'Radiation measurement continues unless the device status says otherwise.': 'Die Strahlungsmessung läuft weiter, '
                                                                             'sofern der Gerätestatus nichts anderes '
                                                                             'anzeigt.',
 'Radiation measurement continues. An external Home Assistant temperature may be used when configured.': 'Die '
                                                                                                         'Strahlungsmessung '
                                                                                                         'läuft '
                                                                                                         'weiter. '
                                                                                                         'Bei '
                                                                                                         'entsprechender '
                                                                                                         'Konfiguration '
                                                                                                         'kann eine '
                                                                                                         'externe '
                                                                                                         'Home-Assistant-Temperatur '
                                                                                                         'verwendet '
                                                                                                         'werden.',
 'Radiation measurement continues; only the optional orientation value is affected.': 'Die Strahlungsmessung läuft '
                                                                                      'weiter; betroffen ist nur der '
                                                                                      'optionale Lagewert.',
 'Radiation monitoring analysis': 'Analyse der Strahlungsüberwachung',
 'Radiation traffic light': 'Strahlungsampel',
 'Radiation traffic light hysteresis explanation': 'Die Strahlungsampel arbeitet mit Hysterese: Gelb ab '
                                                   '{yellow_enter:g}% und Rückkehr unter {yellow_clear:g}%; Rot ab '
                                                   '{red_enter:g}% und Rückkehr unter {red_clear:g}%.',
 'Radiation traffic light uses hysteresis: it enters yellow at {yellow_enter:g}% and clears below {yellow_clear:g}%; it enters red at {red_enter:g}% and clears below {red_clear:g}%.': 'Die '
                                                                                                                                                                                        'Strahlungsampel '
                                                                                                                                                                                        'arbeitet '
                                                                                                                                                                                        'mit '
                                                                                                                                                                                        'Hysterese: '
                                                                                                                                                                                        'Gelb '
                                                                                                                                                                                        'ab '
                                                                                                                                                                                        '{yellow_enter:g}% '
                                                                                                                                                                                        'und '
                                                                                                                                                                                        'Rückkehr '
                                                                                                                                                                                        'unter '
                                                                                                                                                                                        '{yellow_clear:g}%; '
                                                                                                                                                                                        'Rot '
                                                                                                                                                                                        'ab '
                                                                                                                                                                                        '{red_enter:g}% '
                                                                                                                                                                                        'und '
                                                                                                                                                                                        'Rückkehr '
                                                                                                                                                                                        'unter '
                                                                                                                                                                                        '{red_clear:g}%.',
 'Raw CSV': 'Rohdaten-CSV',
 'Raw device values are stored separately before quality filtering': 'Unveränderte Gerätewerte werden vor der '
                                                                     'Qualitätsfilterung separat gespeichert',
 'Raw gyro [signed int16]': 'Gyro-Rohwerte [vorzeichenbehaftetes int16]',
 'Raw-data archive': 'Rohdatenarchiv',
 'Read-only mode': 'Nur-Lese-Modus',
 'Ready for new measurements': 'Bereit für neue Messungen',
 'Recent 30 days compared with the preceding 30 days': 'Letzte 30 Tage im Vergleich zu den vorherigen 30 Tagen',
 'Recent data quality is high': 'Die Qualität der aktuellen Daten ist hoch',
 'Recent period compared with the preceding period': 'Aktueller Zeitraum im Vergleich zum vorherigen Zeitraum',
 'Recent quality-filtered data quality is high': 'Die Qualität der jüngsten gefilterten Daten ist hoch',
 'Recent reports': 'Letzte Berichte',
 'Recommendation': 'Empfehlung',
 'Recommended': 'Empfohlen',
 'Reconnects': 'Wiederverbindungen',
 'Red': 'Rot',
 'Reduced': 'Reduziert',
 'Refreshing device status…': 'Gerätestatus wird aktualisiert …',
 'Relative anomaly indicator only; not a safety classification.': 'Nur relativer Anomalieindikator; keine '
                                                                  'Sicherheitsklassifikation.',
 'Relative correction factor': 'Relativer Korrekturfaktor',
 'Relative spread': 'Relative Streuung',
 'Relative to 7 d baseline': 'Relativ zur 7-Tage-Baseline',
 'Relative-factor confidence': 'Vertrauen des relativen Faktors',
 'Remaining deviation': 'Verbleibende Abweichung',
 'Remove': 'Entfernen',
 'Report': 'Bericht',
 'Report generation failed': 'Berichtserstellung fehlgeschlagen',
 'Report target': 'Bericht für',
 'Reports': 'Berichte',
 'Reports for the displayed analysis': 'Berichte für die angezeigte Analyse',
 'Rescan devices': 'Geräte neu suchen',
 'Resolve persistent connection gaps before relying on long-term comparisons.': 'Behebe anhaltende '
                                                                                'Verbindungslücken, bevor du dich '
                                                                                'auf Langzeitvergleiche verlässt.',
 'Restore backup': 'Sicherung wiederherstellen',
 'Restore complete': 'Wiederherstellung abgeschlossen',
 'Restore confirmation text must be exactly RESTORE': 'Der Bestätigungstext muss genau RESTORE lauten',
 'Restore history': 'Historie wiederherstellen',
 'Restore is disabled by default.': 'Die Wiederherstellung ist standardmäßig deaktiviert.',
 'Restore upload must be between 1 byte and 128 MiB': 'Der Wiederherstellungs-Upload muss zwischen 1 Byte und 128 '
                                                      'MiB groß sein',
 'Return to GMC Radiation Monitoring': 'Zurück zur GMC-Strahlungsüberwachung',
 'Return to GMC Reports': 'Zurück zu den GMC-Berichten',
 'Review the event export for timing and severity': 'Ereignisexport auf Zeitpunkt und Schweregrad prüfen',
 'Review the recent trend and event timing. Check both counters and the measurement location if the change persists.': 'Prüfe '
                                                                                                                       'den '
                                                                                                                       'jüngsten '
                                                                                                                       'Verlauf '
                                                                                                                       'und '
                                                                                                                       'den '
                                                                                                                       'Zeitpunkt '
                                                                                                                       'der '
                                                                                                                       'Ereignisse. '
                                                                                                                       'Kontrolliere '
                                                                                                                       'bei '
                                                                                                                       'anhaltender '
                                                                                                                       'Änderung '
                                                                                                                       'beide '
                                                                                                                       'Zähler '
                                                                                                                       'und '
                                                                                                                       'den '
                                                                                                                       'Messort.',
 'Rising': 'Steigend',
 'Robust medians are used; rejected measurements and isolated spikes do not immediately change the profile.': 'Es '
                                                                                                              'werden '
                                                                                                              'robuste '
                                                                                                              'Medianwerte '
                                                                                                              'verwendet; '
                                                                                                              'verworfene '
                                                                                                              'Messungen '
                                                                                                              'und '
                                                                                                              'einzelne '
                                                                                                              'Spitzen '
                                                                                                              'verändern '
                                                                                                              'das '
                                                                                                              'Profil '
                                                                                                              'nicht '
                                                                                                              'unmittelbar.',
 'Robust one-hour values': 'Robuste 1-Stunden-Werte',
 'Roll angle': 'Rollwinkel',
 'Rolling windows end at the latest stored measurement. Dose-rate values are derived from CPM using the configured factor and are not independently measured. CPM remains the primary measurement. The traffic light is a relative background-anomaly indicator, not an emergency, health, or radiation-safety classification.': 'Gleitende '
                                                                                                                                                                                                                                                                                                                                 'Zeitfenster '
                                                                                                                                                                                                                                                                                                                                 'enden '
                                                                                                                                                                                                                                                                                                                                 'beim '
                                                                                                                                                                                                                                                                                                                                 'zuletzt '
                                                                                                                                                                                                                                                                                                                                 'gespeicherten '
                                                                                                                                                                                                                                                                                                                                 'Messwert. '
                                                                                                                                                                                                                                                                                                                                 'Dosisleistungen '
                                                                                                                                                                                                                                                                                                                                 'werden '
                                                                                                                                                                                                                                                                                                                                 'mit '
                                                                                                                                                                                                                                                                                                                                 'dem '
                                                                                                                                                                                                                                                                                                                                 'konfigurierten '
                                                                                                                                                                                                                                                                                                                                 'Faktor '
                                                                                                                                                                                                                                                                                                                                 'aus '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'abgeleitet '
                                                                                                                                                                                                                                                                                                                                 'und '
                                                                                                                                                                                                                                                                                                                                 'nicht '
                                                                                                                                                                                                                                                                                                                                 'unabhängig '
                                                                                                                                                                                                                                                                                                                                 'gemessen. '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'bleibt '
                                                                                                                                                                                                                                                                                                                                 'der '
                                                                                                                                                                                                                                                                                                                                 'primäre '
                                                                                                                                                                                                                                                                                                                                 'Messwert. '
                                                                                                                                                                                                                                                                                                                                 'Die '
                                                                                                                                                                                                                                                                                                                                 'Ampel '
                                                                                                                                                                                                                                                                                                                                 'zeigt '
                                                                                                                                                                                                                                                                                                                                 'relative '
                                                                                                                                                                                                                                                                                                                                 'Hintergrundanomalien '
                                                                                                                                                                                                                                                                                                                                 'und '
                                                                                                                                                                                                                                                                                                                                 'ist '
                                                                                                                                                                                                                                                                                                                                 'keine '
                                                                                                                                                                                                                                                                                                                                 'Notfall-, '
                                                                                                                                                                                                                                                                                                                                 'Gesundheits- '
                                                                                                                                                                                                                                                                                                                                 'oder '
                                                                                                                                                                                                                                                                                                                                 'Strahlenschutzklassifikation.',
 'SD: {value} CPM': 'SD: {value} CPM',
 'SQLite backup': 'SQLite-Sicherung',
 'SQLite backup file': 'SQLite-Sicherungsdatei',
 'SQLite database vacuum completed': 'SQLite-Datenbank komprimiert',
 'Sample standard deviation': 'Stichproben-Standardabweichung',
 'Samples': 'Messwerte',
 'Samples: {samples} / {expected}': 'Messwerte: {samples} / {expected}',
 'Sampling interval: {interval} s | Samples: {samples}/{expected} | Completeness: {completeness:.2f}% | Generated: {generated} | App {version}': 'Messintervall: '
                                                                                                                                                 '{interval} '
                                                                                                                                                 's '
                                                                                                                                                 '| '
                                                                                                                                                 'Messwerte: '
                                                                                                                                                 '{samples}/{expected} '
                                                                                                                                                 '| '
                                                                                                                                                 'Vollständigkeit: '
                                                                                                                                                 '{completeness:.2f} '
                                                                                                                                                 '% '
                                                                                                                                                 '| '
                                                                                                                                                 'Erstellt: '
                                                                                                                                                 '{generated} '
                                                                                                                                                 '| '
                                                                                                                                                 'App '
                                                                                                                                                 '{version}',
 'Sampling interval: {seconds} s': 'Messintervall: {seconds} s',
 'Sat': 'Sa',
 'Saturday': 'Samstag',
 'Save a custom report below to reuse it with one tap.': 'Speichere unten einen eigenen Bericht, um ihn später mit '
                                                         'einem Klick erneut zu verwenden.',
 'Save assignments and restart': 'Zuordnungen speichern und neu starten',
 'Save preset': 'Vorgabe speichern',
 'Saved report presets': 'Gespeicherte Berichtsvorgaben',
 'Saving changes restarts the add-on so the new serial assignments become active.': 'Beim Speichern wird das Add-on '
                                                                                    'neu gestartet, damit die neuen '
                                                                                    'Gerätezuordnungen aktiv werden.',
 'Scanning and testing suitable unassigned USB ports…': 'Geeignete freie USB-Anschlüsse werden gesucht und geprüft …',
 'Schema': 'Schema',
 'Scoped only to known GMC sensor entities': 'Nur auf bekannte GMC-Sensorentitäten beschränkt',
 'Second half vs first half of available 7 d window': 'Zweite Hälfte im Vergleich zur ersten Hälfte des verfügbaren '
                                                      '7-Tage-Zeitraums',
 'Select a SQLite backup file first.': 'Wähle zuerst eine SQLite-Sicherungsdatei aus.',
 'Select a backup to preview its schema, devices, data period and row counts before restoring.': 'Wähle eine '
                                                                                                 'Sicherung aus, um '
                                                                                                 'vor der '
                                                                                                 'Wiederherstellung '
                                                                                                 'Schema, Geräte, '
                                                                                                 'Datenzeitraum und '
                                                                                                 'Zeilenanzahlen zu '
                                                                                                 'prüfen.',
 'Select exactly one serial device for every configured GMC': 'Wähle für jedes konfigurierte GMC genau ein serielles '
                                                              'Gerät aus',
 'Select the GMC-320, the GMC-500+, or a combined report containing both devices.': 'Wähle den GMC-320, den GMC-500+ '
                                                                                    'oder einen kombinierten Bericht '
                                                                                    'mit beiden Geräten.',
 'Select the physical counter for this configured GMC device.': 'Wähle den physischen Zähler für dieses '
                                                                'konfigurierte GMC-Gerät.',
 'Selected serial device is no longer available': 'Das ausgewählte serielle Gerät ist nicht mehr verfügbar',
 'Separate original samples in 24 h · {accepted} accepted · {pending} pending': 'Separate Originalmessungen in 24 h '
                                                                                '· {accepted} übernommen · {pending} '
                                                                                'noch nicht bestätigt',
 'Serial': 'Seriennummer',
 'Serial Errors Since Start': 'Serielle Fehler seit Start',
 'Serial Reconnects Since Start': 'Serielle Neuverbindungen seit Start',
 'Serial USB device': 'Serielles USB-Gerät',
 'Serial connection recovered': 'Serielle Verbindung wiederhergestellt',
 'Serial device connections': 'Geräteanschlüsse',
 'Serial errors / reconnects': 'Serielle Fehler / Reconnects',
 'Serial port': 'Serieller Port',
 'Serial: {serial} | Period: {period} | Timezone: {timezone}': 'Seriennummer: {serial} | Zeitraum: {period} | '
                                                               'Zeitzone: {timezone}',
 'Serial: {value}': 'Seriennummer: {value}',
 'Severity': 'Schweregrad',
 'Shared CPM rise': 'Gemeinsamer CPM-Anstieg',
 'Shared event detector': 'Gemeinsamer Ereignisdetektor',
 'Show analysis': 'Analyse anzeigen',
 'Show help': 'Hilfe anzeigen',
 'Show other serial devices': 'Andere serielle Geräte anzeigen',
 'Shows live connection state, the latest accepted measurement and warnings for each automatically detected GMC counter.': 'Zeigt '
                                                                                                                           'den '
                                                                                                                           'Live-Verbindungszustand, '
                                                                                                                           'den '
                                                                                                                           'letzten '
                                                                                                                           'akzeptierten '
                                                                                                                           'Messwert '
                                                                                                                           'und '
                                                                                                                           'Warnungen '
                                                                                                                           'für '
                                                                                                                           'jeden '
                                                                                                                           'automatisch '
                                                                                                                           'erkannten '
                                                                                                                           'GMC-Zähler.',
 'Simple': 'Einfach',
 'Since app start': 'Seit App-Start',
 'Slightly noticeable': 'Leicht auffällig',
 'Slightly tilted': 'Leicht geneigt',
 'Small baseline drift': 'Geringe Baseline-Drift',
 'Smart Alert State': 'Intelligenter Alarmstatus',
 'Smoothed historical background trend': 'Geglättete historische Hintergrundentwicklung',
 'Source validation': 'Quellenprüfung',
 'Specific ISO week': 'Bestimmte ISO-Woche',
 'Specific date': 'Bestimmtes Datum',
 'Spread above the Poisson expectation can be caused by environmental changes, device instability or changing interference; the metric does not identify which cause applies.': 'Eine '
                                                                                                                                                                                'Streuung '
                                                                                                                                                                                'oberhalb '
                                                                                                                                                                                'der '
                                                                                                                                                                                'Poisson-Erwartung '
                                                                                                                                                                                'kann '
                                                                                                                                                                                'durch '
                                                                                                                                                                                'Umweltänderungen, '
                                                                                                                                                                                'Geräteinstabilität '
                                                                                                                                                                                'oder '
                                                                                                                                                                                'wechselnde '
                                                                                                                                                                                'Störquellen '
                                                                                                                                                                                'entstehen; '
                                                                                                                                                                                'die '
                                                                                                                                                                                'Kennzahl '
                                                                                                                                                                                'bestimmt '
                                                                                                                                                                                'nicht, '
                                                                                                                                                                                'welche '
                                                                                                                                                                                'Ursache '
                                                                                                                                                                                'vorliegt.',
 'Stability and device health': 'Stabilität und Gerätezustand',
 'Stable': 'Stabil',
 'Stable device path': 'Stabiler Gerätepfad',
 'Stable devices': 'Stabile Geräte',
 'Standard deviation CPM': 'CPM-Standardabweichung',
 'Start time UTC': 'Startzeit UTC',
 'Start time local': 'Startzeit lokal',
 'Start with a readable PDF or a complete ZIP bundle. Raw and specialist formats remain available below without crowding the main view.': 'Beginne '
                                                                                                                                          'mit '
                                                                                                                                          'einem '
                                                                                                                                          'gut '
                                                                                                                                          'lesbaren '
                                                                                                                                          'PDF '
                                                                                                                                          'oder '
                                                                                                                                          'einem '
                                                                                                                                          'vollständigen '
                                                                                                                                          'ZIP-Paket. '
                                                                                                                                          'Rohdaten- '
                                                                                                                                          'und '
                                                                                                                                          'Spezialformate '
                                                                                                                                          'bleiben '
                                                                                                                                          'weiter '
                                                                                                                                          'unten '
                                                                                                                                          'verfügbar, '
                                                                                                                                          'ohne '
                                                                                                                                          'die '
                                                                                                                                          'Hauptansicht '
                                                                                                                                          'zu '
                                                                                                                                          'überladen.',
 'Statistical indication only': 'Nur statistischer Hinweis',
 'Statistical level shift': 'Statistischer Niveauwechsel',
 'Statistically noticeable': 'Statistisch auffällig',
 'Statistics': 'Statistik',
 'Stored samples': 'Gespeicherte Messwerte',
 'Stored samples across all devices': 'Messwerte aller Geräte',
 'Stored samples for this device': 'Messwerte dieses Geräts',
 'Strong common signal': 'Starkes gemeinsames Signal',
 'Strong linear relationship': 'Starker linearer Zusammenhang',
 'Strong statistical deviation': 'Starke statistische Abweichung',
 'Successful uploads': 'Erfolgreiche Uploads',
 'Successful uploads since start': 'Erfolgreiche Uploads seit Start',
 'Suitable for most trend analysis': 'Für die meisten Trendanalysen geeignet',
 'Summary': 'Zusammenfassung',
 'Sun': 'So',
 'Sunday': 'Sonntag',
 'Supervisor API access is unavailable': 'Der Zugriff auf die Supervisor-API ist nicht verfügbar',
 'Supply voltage [V]': 'Versorgungsspannung [V]',
 'Suspicious CPM value is being verified': 'Verdächtiger CPM-Wert wird überprüft',
 'Sustained Radiation Alert': 'Anhaltender Strahlungsalarm',
 'Sustained relative anomaly events': 'Anhaltende relative Anomalieereignisse',
 'Sustained yellow/red relative anomaly events': 'Anhaltende gelbe/rote relative Anomalieereignisse',
 'Temperature': 'Temperatur',
 'Temperature / voltage errors': 'Temperatur- / Spannungsfehler',
 'Temperature Errors Since Start': 'Temperaturfehler seit Start',
 'Temperature [°C]': 'Temperatur [°C]',
 'Temperature and voltage relationships': 'Zusammenhänge mit Temperatur und Spannung',
 'Temperature bins (24 h)': 'Temperaturklassen (24 h)',
 'Temperature correlation': 'Temperaturkorrelation',
 'Temperature profile is still being formed': 'Temperaturprofil wird noch gebildet',
 'Temperature trend': 'Temperaturtrend',
 'Temperature-specific background': 'Temperaturspezifischer Hintergrund',
 'The Supervisor options could not be loaded: {error}': 'Die Supervisor-Optionen konnten nicht geladen werden: '
                                                        '{error}',
 'The absolute assessment starts after the first measurement.': 'Die absolute Bewertung beginnt nach dem ersten '
                                                                'Messwert.',
 'The absolute level is below the configured warning threshold, but the value is far above the learned local background.': 'Die '
                                                                                                                           'absolute '
                                                                                                                           'Bewertung '
                                                                                                                           'liegt '
                                                                                                                           'unter '
                                                                                                                           'der '
                                                                                                                           'konfigurierten '
                                                                                                                           'Warnschwelle, '
                                                                                                                           'der '
                                                                                                                           'Wert '
                                                                                                                           'liegt '
                                                                                                                           'jedoch '
                                                                                                                           'weit '
                                                                                                                           'über '
                                                                                                                           'dem '
                                                                                                                           'erlernten '
                                                                                                                           'lokalen '
                                                                                                                           'Hintergrund.',
 'The absolute level is currently uncritical, but the local comparison or short-term trend deserves continued observation.': 'Die '
                                                                                                                             'absolute '
                                                                                                                             'Bewertung '
                                                                                                                             'ist '
                                                                                                                             'derzeit '
                                                                                                                             'unkritisch, '
                                                                                                                             'aber '
                                                                                                                             'der '
                                                                                                                             'lokale '
                                                                                                                             'Vergleich '
                                                                                                                             'oder '
                                                                                                                             'der '
                                                                                                                             'Kurzzeittrend '
                                                                                                                             'sollte '
                                                                                                                             'weiter '
                                                                                                                             'beobachtet '
                                                                                                                             'werden.',
 'The absolute level is currently uncritical. More local history is required before anomaly detection becomes reliable.': 'Die '
                                                                                                                          'absolute '
                                                                                                                          'Bewertung '
                                                                                                                          'ist '
                                                                                                                          'derzeit '
                                                                                                                          'unkritisch. '
                                                                                                                          'Für '
                                                                                                                          'eine '
                                                                                                                          'zuverlässige '
                                                                                                                          'Anomalieerkennung '
                                                                                                                          'werden '
                                                                                                                          'mehr '
                                                                                                                          'lokale '
                                                                                                                          'Verlaufsdaten '
                                                                                                                          'benötigt.',
 'The add-on is restarting so the new serial assignments become active.': 'Das Add-on wird neu gestartet, damit die '
                                                                          'neuen seriellen Zuordnungen aktiv werden.',
 'The app combines the recent trend, robust statistics, agreement between connected counters and the learned local background. The result is a statistical aid and does not identify a physical cause.': 'Die '
                                                                                                                                                                                                         'App '
                                                                                                                                                                                                         'kombiniert '
                                                                                                                                                                                                         'den '
                                                                                                                                                                                                         'jüngsten '
                                                                                                                                                                                                         'Verlauf, '
                                                                                                                                                                                                         'robuste '
                                                                                                                                                                                                         'Statistiken, '
                                                                                                                                                                                                         'die '
                                                                                                                                                                                                         'Übereinstimmung '
                                                                                                                                                                                                         'verbundener '
                                                                                                                                                                                                         'Zähler '
                                                                                                                                                                                                         'und '
                                                                                                                                                                                                         'den '
                                                                                                                                                                                                         'erlernten '
                                                                                                                                                                                                         'lokalen '
                                                                                                                                                                                                         'Hintergrund. '
                                                                                                                                                                                                         'Das '
                                                                                                                                                                                                         'Ergebnis '
                                                                                                                                                                                                         'ist '
                                                                                                                                                                                                         'eine '
                                                                                                                                                                                                         'statistische '
                                                                                                                                                                                                         'Hilfe '
                                                                                                                                                                                                         'und '
                                                                                                                                                                                                         'bestimmt '
                                                                                                                                                                                                         'keine '
                                                                                                                                                                                                         'physikalische '
                                                                                                                                                                                                         'Ursache.',
 'The app compares quality-filtered measurements from the same weekday and hour. Robust medians reduce the influence of isolated spikes and regular daily patterns are kept separate from unusual changes.': 'Die '
                                                                                                                                                                                                             'App '
                                                                                                                                                                                                             'vergleicht '
                                                                                                                                                                                                             'qualitätsgefilterte '
                                                                                                                                                                                                             'Messungen '
                                                                                                                                                                                                             'desselben '
                                                                                                                                                                                                             'Wochentags '
                                                                                                                                                                                                             'und '
                                                                                                                                                                                                             'derselben '
                                                                                                                                                                                                             'Stunde. '
                                                                                                                                                                                                             'Robuste '
                                                                                                                                                                                                             'Mediane '
                                                                                                                                                                                                             'verringern '
                                                                                                                                                                                                             'den '
                                                                                                                                                                                                             'Einfluss '
                                                                                                                                                                                                             'einzelner '
                                                                                                                                                                                                             'Spitzen '
                                                                                                                                                                                                             'und '
                                                                                                                                                                                                             'trennen '
                                                                                                                                                                                                             'regelmäßige '
                                                                                                                                                                                                             'Tagesmuster '
                                                                                                                                                                                                             'von '
                                                                                                                                                                                                             'ungewöhnlichen '
                                                                                                                                                                                                             'Änderungen.',
 'The app compares quality-filtered radiation measurements with available air-pressure data. A statistical relationship can support interpretation, but correlation alone does not prove a cosmic or environmental cause.': 'Die '
                                                                                                                                                                                                                            'App '
                                                                                                                                                                                                                            'vergleicht '
                                                                                                                                                                                                                            'qualitätsgefilterte '
                                                                                                                                                                                                                            'Strahlungsmessungen '
                                                                                                                                                                                                                            'mit '
                                                                                                                                                                                                                            'verfügbaren '
                                                                                                                                                                                                                            'Luftdruckdaten. '
                                                                                                                                                                                                                            'Ein '
                                                                                                                                                                                                                            'statistischer '
                                                                                                                                                                                                                            'Zusammenhang '
                                                                                                                                                                                                                            'kann '
                                                                                                                                                                                                                            'die '
                                                                                                                                                                                                                            'Einordnung '
                                                                                                                                                                                                                            'unterstützen, '
                                                                                                                                                                                                                            'aber '
                                                                                                                                                                                                                            'eine '
                                                                                                                                                                                                                            'Korrelation '
                                                                                                                                                                                                                            'allein '
                                                                                                                                                                                                                            'beweist '
                                                                                                                                                                                                                            'keine '
                                                                                                                                                                                                                            'kosmische '
                                                                                                                                                                                                                            'oder '
                                                                                                                                                                                                                            'umweltbedingte '
                                                                                                                                                                                                                            'Ursache.',
 'The comparison uses only quality-filtered, one-to-one paired measurements.': 'Der Vergleich verwendet '
                                                                               'ausschließlich qualitätsgefilterte, '
                                                                               'eindeutig gepaarte Messwerte.',
 'The configured danger threshold is exceeded.': 'Die konfigurierte Gefahrenschwelle ist überschritten.',
 'The connected counters currently agree well': 'Die verbundenen Zähler stimmen derzeit gut überein',
 'The counters disagree, so a device-specific effect is more likely': 'Die Zähler weichen voneinander ab; ein '
                                                                      'gerätespezifischer Effekt ist daher '
                                                                      'wahrscheinlicher',
 'The current radiation level is uncritical according to the selected thresholds.': 'Die aktuelle Strahlungsleistung '
                                                                                    'ist nach den gewählten '
                                                                                    'Grenzwerten unkritisch.',
 'The current value is below the configured warning threshold and within the usual local range.': 'Der aktuelle Wert '
                                                                                                  'liegt unter der '
                                                                                                  'konfigurierten '
                                                                                                  'Warnschwelle und '
                                                                                                  'im üblichen '
                                                                                                  'lokalen Bereich.',
 'The current value is within the configured warning range.': 'Der aktuelle Wert liegt im konfigurierten '
                                                              'Warnbereich.',
 'The deviation is device-specific; the measurement-site profile remains normal': 'Die Abweichung ist '
                                                                                  'gerätespezifisch; das '
                                                                                  'Messortprofil bleibt normal',
 'The device baseline is available, but there are not enough recent measurements for a current comparison.': 'Die '
                                                                                                             'Geräte-Baseline '
                                                                                                             'ist '
                                                                                                             'verfügbar, '
                                                                                                             'aber '
                                                                                                             'für '
                                                                                                             'einen '
                                                                                                             'aktuellen '
                                                                                                             'Vergleich '
                                                                                                             'liegen '
                                                                                                             'noch '
                                                                                                             'nicht '
                                                                                                             'genügend '
                                                                                                             'neue '
                                                                                                             'Messwerte '
                                                                                                             'vor.',
 'The device clock differs from Home Assistant time.': 'Die Geräteuhr weicht von der Home-Assistant-Zeit ab.',
 'The filtered counters disagree, so a device-specific effect is more likely': 'Die gefilterten Zähler weichen '
                                                                               'voneinander ab; ein '
                                                                               'gerätespezifischer Effekt ist '
                                                                               'wahrscheinlicher',
 'The learned baseline remains available. More current samples are required before the local comparison can be updated.': 'Die '
                                                                                                                          'gelernte '
                                                                                                                          'Baseline '
                                                                                                                          'bleibt '
                                                                                                                          'verfügbar. '
                                                                                                                          'Für '
                                                                                                                          'die '
                                                                                                                          'Aktualisierung '
                                                                                                                          'des '
                                                                                                                          'lokalen '
                                                                                                                          'Vergleichs '
                                                                                                                          'werden '
                                                                                                                          'weitere '
                                                                                                                          'aktuelle '
                                                                                                                          'Messwerte '
                                                                                                                          'benötigt.',
 'The level-shift detector looks for persistent statistical changes and does not alter radiation warnings.': 'Die '
                                                                                                             'Niveauwechsel-Erkennung '
                                                                                                             'sucht '
                                                                                                             'nach '
                                                                                                             'anhaltenden '
                                                                                                             'statistischen '
                                                                                                             'Änderungen '
                                                                                                             'und '
                                                                                                             'verändert '
                                                                                                             'keine '
                                                                                                             'Strahlungswarnungen.',
 'The local background is still being learned, so no anomaly assessment is available yet.': 'Der lokale Hintergrund '
                                                                                            'wird noch gebildet; '
                                                                                            'daher ist noch keine '
                                                                                            'Anomaliebewertung '
                                                                                            'verfügbar.',
 'The measurement-site baseline is {deviation:+.1f}% above its typical value': 'Die Verbund-Baseline des Messorts '
                                                                               'liegt {deviation:+.1f}% über ihrem '
                                                                               'typischen Wert',
 'The measurement-site profile combines both devices with quality weighting': 'Das Messortprofil kombiniert beide '
                                                                              'Geräte qualitätsgewichtet',
 'The measurement-site profile currently relies on one device': 'Das Messortprofil basiert derzeit nur auf einem '
                                                                'Gerät',
 'The pressure model cannot prove cosmic radiation and never suppresses radiation warnings.': 'Das Luftdruckmodell '
                                                                                              'kann kosmische '
                                                                                              'Strahlung nicht '
                                                                                              'nachweisen und '
                                                                                              'unterdrückt niemals '
                                                                                              'Strahlungswarnungen.',
 'The quality-filtered counter comparison currently agrees well': 'Der qualitätsgefilterte Zählervergleich stimmt '
                                                                  'derzeit gut überein',
 'The recent 30-minute robust trend is rising': 'Der robuste 30-Minuten-Trend steigt',
 'The recent 30-minute trend is rising': 'Der aktuelle 30-Minuten-Trend steigt',
 'The request could not be processed. Check the selected options.': 'Die Anfrage konnte nicht verarbeitet werden. '
                                                                    'Prüfe die ausgewählten Optionen.',
 'The score combines time-window coverage, missing or irregular intervals, duplicate timestamps and optional-sensor coverage. It indicates how strongly the analysis can rely on the stored series.': 'Die '
                                                                                                                                                                                                      'Bewertung '
                                                                                                                                                                                                      'kombiniert '
                                                                                                                                                                                                      'Zeitfensterabdeckung, '
                                                                                                                                                                                                      'fehlende '
                                                                                                                                                                                                      'oder '
                                                                                                                                                                                                      'unregelmäßige '
                                                                                                                                                                                                      'Intervalle, '
                                                                                                                                                                                                      'doppelte '
                                                                                                                                                                                                      'Zeitstempel '
                                                                                                                                                                                                      'und '
                                                                                                                                                                                                      'die '
                                                                                                                                                                                                      'Abdeckung '
                                                                                                                                                                                                      'optionaler '
                                                                                                                                                                                                      'Sensoren. '
                                                                                                                                                                                                      'Sie '
                                                                                                                                                                                                      'zeigt, '
                                                                                                                                                                                                      'wie '
                                                                                                                                                                                                      'belastbar '
                                                                                                                                                                                                      'die '
                                                                                                                                                                                                      'Analyse '
                                                                                                                                                                                                      'auf '
                                                                                                                                                                                                      'der '
                                                                                                                                                                                                      'gespeicherten '
                                                                                                                                                                                                      'Reihe '
                                                                                                                                                                                                      'aufbauen '
                                                                                                                                                                                                      'kann.',
 'The serial connection is unstable.': 'Die serielle Verbindung ist instabil.',
 'The traffic light and events are relative anomaly indicators, not safety classifications.': 'Ampel und Ereignisse '
                                                                                              'sind relative '
                                                                                              'Anomalieindikatoren '
                                                                                              'und keine '
                                                                                              'Sicherheitsklassifikationen.',
 'The value is also within the usual range for this location.': 'Der Wert liegt außerdem im üblichen Bereich für '
                                                                'diesen Standort.',
 'The values most users need first': 'Die wichtigsten Werte auf einen Blick',
 'These are statistical changes. They can indicate a location, geometry or environmental change, but do not identify the cause.': 'Dies '
                                                                                                                                  'sind '
                                                                                                                                  'statistische '
                                                                                                                                  'Änderungen. '
                                                                                                                                  'Sie '
                                                                                                                                  'können '
                                                                                                                                  'auf '
                                                                                                                                  'einen '
                                                                                                                                  'Orts-, '
                                                                                                                                  'Geometrie- '
                                                                                                                                  'oder '
                                                                                                                                  'Umwelteinfluss '
                                                                                                                                  'hindeuten, '
                                                                                                                                  'bestimmen '
                                                                                                                                  'die '
                                                                                                                                  'Ursache '
                                                                                                                                  'aber '
                                                                                                                                  'nicht.',
 'These values describe the shape of the count distribution. They do not by themselves prove a physical cause or a calibration state.': 'Diese '
                                                                                                                                        'Werte '
                                                                                                                                        'beschreiben '
                                                                                                                                        'die '
                                                                                                                                        'Form '
                                                                                                                                        'der '
                                                                                                                                        'Zählwertverteilung. '
                                                                                                                                        'Für '
                                                                                                                                        'sich '
                                                                                                                                        'allein '
                                                                                                                                        'belegen '
                                                                                                                                        'sie '
                                                                                                                                        'weder '
                                                                                                                                        'eine '
                                                                                                                                        'physikalische '
                                                                                                                                        'Ursache '
                                                                                                                                        'noch '
                                                                                                                                        'den '
                                                                                                                                        'Kalibrierzustand.',
 'This analysis detects unusual changes compared with the normal background at this location. It is not a danger classification; an unusual value can still be below the absolute warning threshold.': 'Diese '
                                                                                                                                                                                                       'Analyse '
                                                                                                                                                                                                       'erkennt '
                                                                                                                                                                                                       'ungewöhnliche '
                                                                                                                                                                                                       'Veränderungen '
                                                                                                                                                                                                       'gegenüber '
                                                                                                                                                                                                       'dem '
                                                                                                                                                                                                       'normalen '
                                                                                                                                                                                                       'Hintergrund '
                                                                                                                                                                                                       'an '
                                                                                                                                                                                                       'diesem '
                                                                                                                                                                                                       'Standort. '
                                                                                                                                                                                                       'Sie '
                                                                                                                                                                                                       'ist '
                                                                                                                                                                                                       'keine '
                                                                                                                                                                                                       'Gefahrenklassifikation; '
                                                                                                                                                                                                       'ein '
                                                                                                                                                                                                       'auffälliger '
                                                                                                                                                                                                       'Wert '
                                                                                                                                                                                                       'kann '
                                                                                                                                                                                                       'weiterhin '
                                                                                                                                                                                                       'unter '
                                                                                                                                                                                                       'der '
                                                                                                                                                                                                       'absoluten '
                                                                                                                                                                                                       'Warnschwelle '
                                                                                                                                                                                                       'liegen.',
 'This cannot be undone. Delete all GMC history?': 'Dies kann nicht rückgängig gemacht werden. Gesamten GMC-Verlauf '
                                                   'löschen?',
 'This classification only compares the current measurement with the selected thresholds. It does not compare the value with the usual background at this location.': 'Diese '
                                                                                                                                                                      'Einstufung '
                                                                                                                                                                      'vergleicht '
                                                                                                                                                                      'den '
                                                                                                                                                                      'aktuellen '
                                                                                                                                                                      'Messwert '
                                                                                                                                                                      'ausschließlich '
                                                                                                                                                                      'mit '
                                                                                                                                                                      'den '
                                                                                                                                                                      'gewählten '
                                                                                                                                                                      'Grenzwerten. '
                                                                                                                                                                      'Sie '
                                                                                                                                                                      'vergleicht '
                                                                                                                                                                      'ihn '
                                                                                                                                                                      'nicht '
                                                                                                                                                                      'mit '
                                                                                                                                                                      'dem '
                                                                                                                                                                      'üblichen '
                                                                                                                                                                      'Hintergrund '
                                                                                                                                                                      'an '
                                                                                                                                                                      'diesem '
                                                                                                                                                                      'Standort.',
 'This factor is only a relative device comparison and is not an absolute radiation calibration.': 'Dieser Faktor '
                                                                                                   'ist nur ein '
                                                                                                   'relativer '
                                                                                                   'Gerätevergleich '
                                                                                                   'und keine '
                                                                                                   'absolute '
                                                                                                   'Strahlungskalibrierung.',
 'This report is descriptive and is not a radiation-safety classification.': 'Dieser Bericht ist beschreibend und '
                                                                             'keine strahlenschutzfachliche '
                                                                             'Einstufung.',
 'Thresholds can be changed in the add-on configuration.': 'Die Grenzwerte können in der Add-on-Konfiguration '
                                                           'geändert werden.',
 'Thu': 'Do',
 'Thursday': 'Donnerstag',
 'Tilted': 'Schräg',
 'Time series': 'Zeitreihe',
 'Time series, Poisson comparison and weekday/hour heatmap': 'Zeitreihe, Poisson-Vergleich und '
                                                             'Wochentag/Stunde-Heatmap',
 'Time-series PNG': 'Zeitreihen-PNG',
 'Timestamp diagnostics': 'Zeitstempel-Diagnose',
 'Timezone': 'Zeitzone',
 'Today so far bundle': 'Heutiges Paket bis jetzt',
 'Too few pressure/CPM pairs': 'Zu wenige Luftdruck-/CPM-Paare',
 'Too few valid paired measurements for a reliable device comparison': 'Zu wenige gültige Messwertpaare für einen '
                                                                       'belastbaren Gerätevergleich',
 'Too little or too fragmented for strong conclusions': 'Zu wenig oder zu fragmentiert für belastbare '
                                                        'Schlussfolgerungen',
 'Trend (30 min)': 'Trend (30 Min.)',
 'Tue': 'Di',
 'Tuesday': 'Dienstag',
 'Type DELETE ALL GMC HISTORY to confirm': 'Zur Bestätigung DELETE ALL GMC HISTORY eingeben',
 'Type RESTORE to confirm': 'Zur Bestätigung RESTORE eingeben',
 'Typical for {weekday} at {hour}:00': 'Typisch für {weekday} um {hour}:00 Uhr',
 'USB down': 'Hochkant, USB unten',
 'USB left': 'Hochkant, USB links',
 'USB right': 'Hochkant, USB rechts',
 'USB up': 'Hochkant, USB oben',
 'UTC timestamp': 'UTC-Zeitstempel',
 'Unavailable': 'Nicht verfügbar',
 'Unconfirmed values since bridge start': 'Unbestätigte Werte seit dem Bridge-Start',
 'Uncritical': 'Unkritisch',
 'Uncritical: below warning threshold': 'Unkritisch: unterhalb der Warnschwelle',
 'Unknown': 'Unbekannt',
 'Unknown GMC': 'Unbekanntes GMC-Gerät',
 'Unknown report device': 'Unbekanntes Berichtsgerät',
 'Unknown serial device': 'Unbekanntes serielles Gerät',
 'Unstable': 'Instabil',
 'Unsupported report format': 'Nicht unterstütztes Berichtsformat',
 'Upload errors': 'Uploadfehler',
 'Upload errors since start': 'Uploadfehler seit Start',
 'Upload failed': 'Upload fehlgeschlagen',
 'Upload successful': 'Upload erfolgreich',
 'Uploading': 'Wird hochgeladen',
 'Upright': 'Hochkant',
 'Use this as context only and review longer periods before drawing conclusions.': 'Nutze dies nur als Kontext und '
                                                                                   'prüfe längere Zeiträume, bevor '
                                                                                   'du Schlussfolgerungen ziehst.',
 'Valid measurements': 'Gültige Messwerte',
 'Variance / mean': 'Varianz / Mittelwert',
 'Very close to Poisson-like spread': 'Sehr nahe an Poisson-ähnlicher Streuung',
 'Very complete 24 h data window': 'Sehr vollständiges 24-h-Datenfenster',
 'Very strong linear relationship': 'Sehr starker linearer Zusammenhang',
 'Very weak linear relationship': 'Sehr schwacher linearer Zusammenhang',
 'Voltage': 'Spannung',
 'Voltage Errors Since Start': 'Spannungsfehler seit Start',
 'Voltage [V]': 'Spannung [V]',
 'Voltage correlation': 'Spannungskorrelation',
 'Waiting for enough recent measurements': 'Wartet auf genügend aktuelle Messwerte',
 'Waiting for first upload': 'Wartet auf ersten Upload',
 'Waiting for recent measurements': 'Wartet auf aktuelle Messwerte',
 'Waiting for the first accepted measurement': 'Warten auf den ersten akzeptierten Messwert',
 'Warning': 'Warnung',
 'Warning from {warning} s; critical from {critical} s': 'Warnung ab {warning} s; kritisch ab {critical} s',
 'Warning threshold exceeded': 'Warnschwelle überschritten',
 'Warning thresholds': 'Warnschwellen',
 'Weak linear relationship': 'Schwacher linearer Zusammenhang',
 'Weather pressure sources disagree': 'Die Luftdruckquellen widersprechen sich',
 'Wed': 'Mi',
 'Wednesday': 'Mittwoch',
 'Weekday': 'Wochentag',
 'Weekday/hour heatmap': 'Wochentag-/Stunden-Heatmap',
 'What does the historical trend mean?': 'Was bedeutet die historische Entwicklung?',
 'What each report preserves and how periods are defined': 'Welche Inhalte die Berichte enthalten und wie Zeiträume '
                                                           'definiert sind',
 'What should I do?': 'Was sollte ich tun?',
 'What this assessment means': 'Bedeutung dieser Bewertung',
 'Why are Poisson values shown?': 'Warum werden Poisson-Werte angezeigt?',
 'Why is this assessment shown?': 'Warum wird das so bewertet?',
 'Within local background range': 'Im lokalen Hintergrundbereich',
 'Within normal statistical variation': 'Innerhalb normaler statistischer Schwankung',
 'Within the usual local range': 'Im üblichen lokalen Bereich',
 'Within warning range': 'Im Warnbereich',
 'Yellow': 'Gelb',
 'Z-score = (latest CPM − 24 h mean) / 24 h standard deviation.': 'Z-Score = (letzter CPM-Wert − 24-h-Mittelwert) / '
                                                                  '24-h-Standardabweichung.',
 'Z-score formula explanation': 'Z-Score = (letzter CPM-Wert − 24-h-Mittelwert) / 24-h-Standardabweichung.',
 'complete and regularly spaced data': 'Vollständige und regelmäßig verteilte Daten',
 'confirmations': 'Bestätigungen',
 'counting uncertainty {value:.2f}%': 'Zählunsicherheit {value:.2f}%',
 'coverage': 'Abdeckung',
 'daily values': 'Tageswerte',
 'days': 'Tage',
 'duplicates / clock regressions': 'Duplikate / Zeitrücksprünge',
 'entity patterns': 'Entitätsmuster',
 'errors': 'Fehler',
 'estimated signal probability': 'geschätzte Signalwahrscheinlichkeit',
 'excluded measurements': 'ausgeschlossene Messwerte',
 'longest gap {value} s': 'längste Lücke {value} s',
 'measurements': 'Messwerte',
 'minimum sample coverage': 'Mindest-Messabdeckung',
 'n={count} paired samples': 'n={count} Messwertpaare',
 'n={count} · {coverage:.1f}% coverage': 'n={count} · {coverage:.1f}% Abdeckung',
 'paired samples': 'Messwertpaare',
 'reconnects': 'Wiederverbindungen',
 'relative to baseline': 'gegenüber der Baseline',
 'score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s': 'Wertung {score:.1f}/100 · Abdeckung '
                                                                           '{coverage:.1f}% · längste Lücke {gap} s',
 'short / long intervals': 'kurze / lange Intervalle',
 'since the current bridge start': 'seit dem aktuellen Bridge-Start',
 'temperature coverage {value}%': 'Temperaturabdeckung {value}%',
 'unknown': 'unbekannt',
 'valid hourly values': 'gültige Stundenwerte',
 'valid paired samples': 'gültige Messwertpaare',
 'voltage coverage {value}%': 'Spannungsabdeckung {value}%',
 'write errors since app start': 'Schreibfehler seit App-Start',
 '{before:.2f} → {after:.2f} CPM · {sigma:.1f}σ · {hours} h persistent': '{before:.2f} → {after:.2f} CPM · '
                                                                         '{sigma:.1f}σ · seit {hours} h anhaltend',
 '{check_type} result cached for {seconds} s · schema v{schema}': '{check_type}-Ergebnis für {seconds} s '
                                                                  'zwischengespeichert · Schema v{schema}',
 '{connected} connected · {disconnected} disconnected': '{connected} verbunden · {disconnected} getrennt',
 '{count} implausible measurements were excluded from the assessment': '{count} unplausible Messwerte wurden aus der '
                                                                       'Bewertung ausgeschlossen',
 '{count} measurements': '{count} Messwerte',
 '{count} measurements and {events} events were removed.': '{count} Messwerte und {events} Ereignisse wurden '
                                                           'entfernt.',
 '{events} events · {diagnostics} diagnostics': '{events} Ereignisse · {diagnostics} Diagnosedatensätze',
 '{gyro_note} History retention: {days} days. Daily periods are local calendar days; weekly periods are ISO weeks from Monday through Sunday.': '{gyro_note} '
                                                                                                                                                'Aufbewahrungsdauer '
                                                                                                                                                'der '
                                                                                                                                                'Historie: '
                                                                                                                                                '{days} '
                                                                                                                                                'Tage. '
                                                                                                                                                'Tageszeiträume '
                                                                                                                                                'entsprechen '
                                                                                                                                                'lokalen '
                                                                                                                                                'Kalendertagen; '
                                                                                                                                                'Wochenzeiträume '
                                                                                                                                                'sind '
                                                                                                                                                'ISO-Wochen '
                                                                                                                                                'von '
                                                                                                                                                'Montag '
                                                                                                                                                'bis '
                                                                                                                                                'Sonntag.',
 '{model} — Radiation monitoring report': '{model} — Strahlungsüberwachungsbericht',
 '{seconds} seconds ago': 'vor {seconds} Sekunden',
 '{value:g} h': '{value:g} h',
 '{value:g} min': '{value:g} min',
 '{value} clock regressions observed': '{value} Zeitrücksprünge erkannt',
 '{value} duplicate timestamps observed': '{value} doppelte Zeitstempel erkannt',
 '{value} long intervals': '{value} lange Intervalle',
 '{value} unusually short intervals': '{value} ungewöhnlich kurze Intervalle',
 '{value} vs local baseline': '{value} gegenüber lokaler Baseline',
 '{value}% time-window coverage': '{value}% Zeitfenster-Abdeckung'}

# Runtime presentation templates added in 7.1.4.
CATALOG.update({
    'Comparison confidence: {confidence}': 'Vertrauen des Vergleichs: {confidence}',
    'Confidence: {confidence}': 'Vertrauen: {confidence}',
    'Status': 'Status',
    'Typical background': 'Typischer Hintergrund',
    'Valid paired samples': 'Gültige Messwertpaare',
    'Warning from {warning:g} s; critical from {critical:g} s': 'Warnung ab {warning:g} s; kritisch ab {critical:g} s',
    'valid hourly values · {days:.1f} days · {span:.1f} hPa': 'gültige Stundenwerte · {days:.1f} Tage · {span:.1f} hPa',
    '{a:+.1f}% / {b:+.1f}%': '{a:+.1f}% / {b:+.1f}%',
    '{b} × factor → {a}': '{b} × Faktor → {a}',
    '{content}': '{content}',
    '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)': '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)',
    '{days} days': '{days} Tage',
    '{dose:.3f} µSv/h': '{dose:.3f} µSv/h',
    '{first} {second}': '{first} {second}',
    '{from_value} → {to_value}': '{from_value} → {to_value}',
    '{note} · n={samples}': '{note} · n={samples}',
    '{pairs} valid paired samples': '{pairs} gültige Messwertpaare',
    '{pairs} valid paired samples · counting uncertainty {value:.2f}%': '{pairs} gültige Messwertpaare · Zählunsicherheit {value:.2f}%',
    '{probability:.0f}% estimated signal probability': '{probability:.0f} % geschätzte Signalwahrscheinlichkeit',
    '{span:.0f} {days_label} · {count} {daily_label}': '{span:.0f} {days_label} · {count} {daily_label}',
    '{start}–{end} °C · {samples} Samples': '{start}–{end} °C · {samples} Messwerte',
    '{trend:+.1f} CPM': '{trend:+.1f} CPM',
    '{value:g} µSv/h': '{value:g} µSv/h',
    'Last uploaded CPM': 'Zuletzt übermitteltes CPM',
    'Last uploaded ACPM': 'Zuletzt übermitteltes ACPM',
    'GMCMap last uploaded ACPM': 'Zuletzt an GMCMap übermitteltes ACPM',
    'GMCMap ACPM accepted samples': 'Akzeptierte Messwerte für GMCMap-ACPM',
    'ACPM is the average of all accepted CPM readings since the current app measurement session began.': 'ACPM ist der Durchschnitt aller akzeptierten CPM-Messwerte seit Beginn der aktuellen Messsitzung der App.',
    'User manual': 'Benutzerhandbuch',
    'Open user manual PDF': 'Benutzerhandbuch als PDF öffnen',
    'User manual is not available': 'Das Benutzerhandbuch ist nicht verfügbar',
})

# Version 8.2.1 report and history labels.
CATALOG.update({
    'Accepted measurements [count]': 'Akzeptierte Messwerte [Anzahl]',
    'Local hour [h]': 'Lokale Stunde [h]',
    'Mean count rate [CPM]': 'Mittlere Zählrate [CPM]',
    'Radiation Monitoring': 'Strahlungsüberwachung',
    'Rejected raw value': 'Verworfener Rohwert',
})


# Version 8.2.1 complete runtime localization.
CATALOG.update({
    'The recent level differs from counting noise with {probability:.2f}% statistical confidence': 'Das aktuelle Niveau unterscheidet sich mit einer statistischen Sicherheit von {probability:.2f} % vom erwarteten Zählrauschen',
    'A comparable or more extreme hourly level occurred about once in {rarity:.1f} historical hours': 'Ein vergleichbares oder extremeres Stundenniveau trat historisch etwa einmal in {rarity:.1f} Stunden auf',
})

# Long-term analysis 9.1.1
CATALOG.update({'24 hours': '24 Stunden', '30 days': '30 Tage', '365 days': '365 Tage', '7 days': '7 Tage', '7-day rolling median': 'Gleitender 7-Tage-Median', '90 days': '90 Tage', '95% block-bootstrap interval for mean': '95-%-Block-Bootstrap-Intervall für den Mittelwert', '95% block-bootstrap interval for median': '95-%-Block-Bootstrap-Intervall für den Median', 'Air-pressure association': 'Zusammenhang mit dem Luftdruck', 'Annual projection from the last 30 days: {value} µSv': 'Jahreshochrechnung aus den letzten 30 Tagen: {value} µSv', 'Annual projection is not shown until a sufficiently complete 30-day period exists.': 'Eine Jahreshochrechnung wird erst bei einem ausreichend vollständigen 30-Tage-Zeitraum angezeigt.', 'Based on {hours} covered hours': 'Basierend auf {hours} abgedeckten Stunden', 'Bootstrap uncertainty, distribution dispersion, EWMA and CUSUM': 'Bootstrap-Unsicherheit, Verteilungsstreuung, EWMA und CUSUM', 'Calendar heat map': 'Kalender-Heatmap', 'Calendar heat map of daily median CPM': 'Kalender-Heatmap der täglichen CPM-Mediane', 'Connected periods above the robust local long-term threshold': 'Zusammenhängende Zeiträume über der robusten lokalen Langzeitschwelle', 'Contextual Fano-like ratio; rolling CPM values are not independent Poisson counts': 'Kontextbezogenes Fano-ähnliches Verhältnis; gleitende CPM-Werte sind keine unabhängigen Poisson-Zählungen', 'Correlation does not prove causation.': 'Korrelation beweist keine Kausalität.', 'Coverage {coverage}% · at least {required}% required': 'Abdeckung {coverage} % · mindestens {required} % erforderlich', 'Covered hours': 'Abgedeckte Stunden', 'Cumulative derived dose': 'Kumulierte abgeleitete Dosis', 'Daily and monthly development': 'Tägliche und monatliche Entwicklung', 'Daily median': 'Tagesmedian', 'Daily median and 7-day rolling median': 'Tagesmedian und gleitender 7-Tage-Median', 'Daily medians, rolling median and calendar view': 'Tagesmediane, gleitender Median und Kalenderansicht', 'Derived cumulative dose: {dose} µSv': 'Abgeleitete kumulierte Dosis: {dose} µSv', 'Derived dose (µSv)': 'Abgeleitete Dosis (µSv)', 'Derived from the robust local background; not an official alarm threshold': 'Aus dem robusten lokalen Hintergrund abgeleitet; kein offizieller Alarmgrenzwert', 'Duration (h)': 'Dauer (h)', 'EWMA, CUSUM, trend tests and relative event detection provide statistical context only. They do not identify a radiation source and do not replace calibrated radiation-protection measurements.': 'EWMA, CUSUM, Trendtests und relative Ereigniserkennung liefern nur statistischen Kontext. Sie identifizieren keine Strahlungsquelle und ersetzen keine kalibrierten Strahlenschutzmessungen.', 'Effective sample size': 'Effektive Stichprobengröße', 'Environmental correlations are exploratory. They may reflect common time patterns, ventilation, weather or other confounding factors and do not prove causation.': 'Umweltkorrelationen sind explorativ. Sie können gemeinsame Zeitmuster, Lüftung, Wetter oder andere Störgrößen widerspiegeln und beweisen keine Kausalität.', 'Excess area (CPM·h)': 'Überschreitungsfläche (CPM·h)', 'Exploratory Spearman correlations at 0, 3, 6, 12 and 24 hour lags': 'Explorative Spearman-Korrelationen mit 0, 3, 6, 12 und 24 Stunden Verzögerung', 'Higher': 'Höher', 'Hourly dispersion ratio': 'Stündliches Streuungsverhältnis', 'Lagged environmental associations': 'Zeitverzögerte Umweltzusammenhänge', 'Long-term analysis': 'Langzeitanalyse', 'Long-term analysis for {device}': 'Langzeitanalyse für {device}', 'Long-term background, cumulative dose, trend, recurring patterns and statistical process diagnostics': 'Langzeithintergrund, kumulierte Dosis, Trend, wiederkehrende Muster und statistische Prozessdiagnostik', 'Long-term overview': 'Langzeitübersicht', 'Long-term statistical diagnostics': 'Statistische Langzeitdiagnostik', 'Long-term trend': 'Langzeittrend', 'Lower': 'Niedriger', 'Mann-Kendall test with Sen slope on sufficiently covered daily medians': 'Mann-Kendall-Test mit Sen-Steigung auf ausreichend abgedeckten Tagesmedianen', 'Maximum CPM': 'Maximale CPM', 'Mean CPM': 'CPM-Mittelwert', 'Median CPM': 'CPM-Median', 'Median {median} CPM · coverage {coverage}%': 'Median {median} CPM · Abdeckung {coverage} %', 'Month': 'Monat', 'Monthly aggregates': 'Monatsaggregate', 'Moving blocks preserve short-range time dependence': 'Gleitende Blöcke erhalten kurzfristige zeitliche Abhängigkeiten', 'No calendar data available': 'Keine Kalenderdaten verfügbar', 'No long-term analysis available yet': 'Noch keine Langzeitanalyse verfügbar', 'No monthly aggregates available': 'Keine Monatsaggregate verfügbar', 'No persistent CUSUM signal detected': 'Kein anhaltendes CUSUM-Signal erkannt', 'No persistent EWMA signal detected': 'Kein anhaltendes EWMA-Signal erkannt', 'No persistent relative elevation episodes detected': 'Keine anhaltenden relativen Erhöhungsphasen erkannt', 'No supported dose conversion for this period': 'Für diesen Zeitraum ist keine unterstützte Dosisumrechnung verfügbar', 'No value is calculated until enough hourly pairs are available.': 'Es wird erst ein Wert berechnet, wenn genügend Stundenpaare verfügbar sind.', 'Not enough daily values for a long-term chart': 'Nicht genügend Tageswerte für ein Langzeitdiagramm', 'Not enough paired data': 'Nicht genügend gepaarte Daten', 'Not yet meaningful': 'Noch nicht sinnvoll berechenbar', 'Only {covered} of {required} days covered': 'Nur {covered} von {required} Tagen abgedeckt', 'Persistent elevation episodes': 'Anhaltende Erhöhungsphasen', 'Persistent episodes': 'Anhaltende Phasen', 'Preliminary': 'Vorläufig', 'Ready': 'Auswertbar', 'Real time windows with duration and coverage checks': 'Echte Zeitfenster mit Prüfung von Dauer und Abdeckung', 'Recent 7-day median relative to the robust long-term background': 'Aktueller 7-Tage-Median relativ zum robusten Langzeithintergrund', 'Recent background deviation': 'Aktuelle Hintergrundabweichung', 'Relative event threshold': 'Relative Ereignisschwelle', 'Robust local background': 'Robuster lokaler Hintergrund', 'Scientific interpretation': 'Wissenschaftliche Einordnung', 'Start': 'Beginn', 'Statistical signal detected': 'Statistisches Signal erkannt', 'Stored measurements are required before long-term statistics can be calculated.': 'Gespeicherte Messwerte sind erforderlich, bevor Langzeitstatistiken berechnet werden können.', 'Strongest at {lag} h lag · {pairs} pairs · {strength} association': 'Stärkster Zusammenhang bei {lag} h Verzögerung · {pairs} Paare · {strength}', 'Temperature association': 'Zusammenhang mit der Temperatur', 'The detector uses the robust long-term local background and does not replace radiation-safety alarms.': 'Die Erkennung verwendet den robusten lokalen Langzeithintergrund und ersetzt keine Strahlenschutzalarme.', 'Time at or above configured danger threshold': 'Zeit am oder über dem konfigurierten Gefahrengrenzwert', 'Time in configured warning range': 'Zeit im konfigurierten Warnbereich', 'Typical range P05–P95: {low}–{high} CPM': 'Typischer Bereich P05-P95: {low}-{high} CPM', 'moderate': 'mäßiger Zusammenhang', 'strong': 'starker Zusammenhang', 'weak': 'schwacher Zusammenhang', '{date}: median {median} CPM, coverage {coverage}%': '{date}: Median {median} CPM, Abdeckung {coverage} %', '{direction} · {slope} CPM/day · p={p}': '{direction} · {slope} CPM/Tag · p={p}', '{hours} covered hours': '{hours} abgedeckte Stunden', '{hours} total elevated hours · longest {longest} h': '{hours} erhöhte Stunden insgesamt · längste Phase {longest} h', '{observed} daily observations · correlation duration {duration} days': '{observed} Tagesbeobachtungen · Korrelationsdauer {duration} Tage', '{replicates} replicates · block length {block} days': '{replicates} Wiederholungen · Blocklänge {block} Tage', 'Long-term': 'Langzeit', 'stable': 'stabil', 'increasing': 'steigend', 'decreasing': 'fallend'})

# Recent baseline wording 9.1.1
CATALOG.update({'Recent baseline context': 'Aktueller Baseline-Kontext', 'Seven-day baseline deviation, drift and sustained relative events': 'Abweichung von der 7-Tage-Baseline, Drift und anhaltende relative Ereignisse'})


# Extended agreement and seasonal analysis 9.1.1
CATALOG.update({'Bland-Altman bias': 'Bland-Altman-Bias', '95% limits of agreement': '95-%-Übereinstimmungsgrenzen', 'Mean signed difference A minus B': 'Mittlere vorzeichenbehaftete Differenz A minus B', 'Exploratory paired-device agreement; correlation alone does not establish agreement.': 'Explorative Übereinstimmung gepaarter Geräte; Korrelation allein belegt keine Übereinstimmung.', 'Seasonal month-of-year profile': 'Saisonprofil nach Kalendermonat', 'Median CPM by calendar month across available years': 'CPM-Median je Kalendermonat über die verfügbaren Jahre', 'Calendar month': 'Kalendermonat', 'Days represented': 'Berücksichtigte Tage', 'Not enough months for a seasonal profile': 'Nicht genügend Monate für ein Saisonprofil', 'At least six represented calendar months are required.': 'Mindestens sechs abgedeckte Kalendermonate sind erforderlich.', 'Exploratory seasonal summary; it does not separate weather, location, detector or calibration changes.': 'Explorative saisonale Zusammenfassung; Wetter-, Standort-, Detektor- oder Kalibrieränderungen werden nicht getrennt.'})


# Evidence-based long-term presentation and field-test diagnostics 10.0.1
CATALOG.update({'Not evaluable': 'Nicht auswertbar', 'Exploratory': 'Explorativ', 'Supported': 'Belastbar', 'Well supported': 'Sehr gut abgesichert', 'Very small practical magnitude': 'Praktische Größenordnung sehr gering', 'Small practical magnitude': 'Praktische Größenordnung gering', 'Moderate practical magnitude': 'Praktische Größenordnung mittel', 'Large practical magnitude': 'Praktische Größenordnung groß', 'Practical magnitude not available': 'Praktische Größenordnung nicht verfügbar', 'No reliable long-term trend can be assessed yet': 'Noch kein belastbarer Langzeittrend bewertbar', 'At least 30 sufficiently complete days and an adequate effective sample size are required.': 'Erforderlich sind mindestens 30 ausreichend vollständige Tage und eine angemessene effektive Stichprobengröße.', 'A rising long-term tendency is visible': 'Eine steigende Langzeittendenz ist erkennbar', 'A falling long-term tendency is visible': 'Eine fallende Langzeittendenz ist erkennbar', 'No statistically clear long-term trend is visible': 'Kein statistisch eindeutiger Langzeittrend erkennbar', 'Estimated change {value}% per month · {magnitude}': 'Geschätzte Änderung {value} % pro Monat · {magnitude}', 'Runtime since service start': 'Laufzeit seit Dienststart', 'Cumulative counters reset when the service restarts.': 'Kumulative Zähler werden beim Neustart des Dienstes zurückgesetzt.', 'USB / serial recovery': 'USB-/Seriell-Wiederherstellung', '{errors} serial errors · {reconnects} reconnects': '{errors} serielle Fehler · {reconnects} Wiederverbindungen', 'Longest data gap': 'Längste Datenlücke', '{count} detected gaps above the expected interval': '{count} erkannte Lücken über dem erwarteten Intervall', 'Database write errors': 'Datenbank-Schreibfehler', 'Stored samples: {count}': 'Gespeicherte Messwerte: {count}', 'GMCMap transmission': 'GMCMap-Übertragung', '{success} successful · {errors} failed uploads': '{success} erfolgreich · {errors} fehlgeschlagene Uploads', 'Export field-test protocol (JSON)': 'Feldtestprotokoll exportieren (JSON)', 'Field-test interpretation': 'Einordnung des Feldtests', 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.': 'Diese Betriebszähler helfen, die Langzeitzuverlässigkeit zu beurteilen. Sie bestätigen weder die Detektorkalibrierung noch die Messgenauigkeit.', '{available} of {required} required hourly pairs are available.': '{available} von {required} erforderlichen Stundenpaaren sind vorhanden.', 'FDR-adjusted p={value}': 'FDR-korrigiertes p={value}', 'FDR-adjusted significance not available': 'FDR-korrigierte Signifikanz nicht verfügbar', 'Plain-language assessment': 'Verständliche Zusammenfassung', 'The main result first; method details remain available below.': 'Zuerst das Hauptergebnis; Methodendetails bleiben darunter verfügbar.', 'Current background context': 'Aktueller Hintergrundkontext', 'Data basis': 'Datengrundlage', '{days} covered days · {observed} daily observations': '{days} abgedeckte Tage · {observed} Tagesbeobachtungen', 'Integrated derived dose in the measured period': 'Integrierte abgeleitete Dosis im Messzeitraum', 'Seasonal assessment': 'Saisonale Bewertung', '{months} represented calendar months': '{months} vertretene Kalendermonate', 'Extended statistical methods': 'Erweiterte statistische Methoden', 'Confidence intervals, effective sample size, test statistics and practical effect size': 'Konfidenzintervalle, effektive Stichprobengröße, Teststatistiken und praktische Effektgröße', 'Trend method details': 'Methodendetails zum Trend', 'Statistical process diagnostics': 'Statistische Prozessdiagnostik', 'EWMA, CUSUM and dispersion diagnostics; statistical context only': 'EWMA-, CUSUM- und Streuungsdiagnostik; nur statistischer Kontext', 'Exploratory Spearman correlations with false-discovery-rate correction': 'Explorative Spearman-Korrelationen mit Korrektur der Falschentdeckungsrate', 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.': 'Umweltkorrelationen sind explorativ. Die Benjamini-Hochberg-Korrektur reduziert Falschentdeckungen über die geprüften Verzögerungen, rechtfertigt aber keine Kausalaussage.', 'Long-term reliability field test': 'Feldtest zur Langzeitzuverlässigkeit', 'Operational counters for USB, database continuity and GMCMap transmission': 'Betriebszähler für USB, Datenbankkontinuität und GMCMap-Übertragung', 'Annual projection from the last 90 days: {value} µSv': 'Jahreshochrechnung aus den letzten 90 Tagen: {value} µSv', 'Annual projection is not shown until a sufficiently complete 90-day period exists.': 'Eine Jahreshochrechnung wird erst bei einem ausreichend vollständigen 90-Tage-Zeitraum angezeigt.'})
