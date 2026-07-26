from __future__ import annotations

CATALOG: dict[str, str] = {'1 h counting uncertainty': '1 h counting uncertainty',
 '1 h coverage': 'Dekking 1 uur',
 '1 h mean': '1-uursgemiddelde',
 '1 h mean / 7 d mean × 100': '1-uursgemiddelde / 7-daags gemiddelde × 100',
 '1 h mean dose rate': 'Gemiddeld dosistempo over 1 uur',
 '1 h mean minus 7 d baseline': '1-uursgemiddelde min 7-daagse basislijn',
 '24 h Fano factor': 'Fano-factor over 24 uur',
 '24 h P95': 'P95 over 24 uur',
 '24 h P99': 'P99 over 24 uur',
 '24 h Z-score': 'Z-score over 24 uur',
 '24 h counting uncertainty': '24 h counting uncertainty',
 '24 h distribution, percentiles and latest-value deviation': '24-uursverdeling, percentielen en afwijking van de '
                                                              'laatste waarde',
 '24 h maximum': 'Maximum over 24 uur',
 '24 h mean': '24-uursgemiddelde',
 '24 h mean dose rate': 'Gemiddeld dosistempo over 24 uur',
 '24 h median': 'Mediaan over 24 uur',
 '24 h minimum': 'Minimum over 24 uur',
 '24 h standard deviation': 'Standaardafwijking over 24 uur',
 '50th percentile': '50e percentiel',
 '7 d baseline': '7-daagse referentie',
 '7 d baseline dose rate': 'Dosistempo van de 7-daagse basislijn',
 '7 d baseline drift': 'Verschuiving van de 7-daagse basislijn',
 '7 d counting uncertainty': '7 d counting uncertainty',
 '7-day smoothed daily median': 'Dagmediaan, afgevlakt over 7 dagen',
 '95th percentile': '95e percentiel',
 '99th percentile': '99e percentiel',
 'A device function is temporarily unavailable.': 'Een apparaatfunctie is tijdelijk niet beschikbaar.',
 'A fresh backup is recommended before deletion.': 'A fresh backup is recommended before deletion.',
 'A recent position change can affect comparability': 'Een recente positiewijziging kan de vergelijkbaarheid '
                                                      'beïnvloeden',
 'Above the typical time profile': 'Boven het typische tijdprofiel',
 'Above the usual local range': 'Boven het gebruikelijke lokale bereik',
 'Absolute radiation assessment': 'Absolute stralingsbeoordeling',
 'Absolute thresholds and local anomaly detection answer different questions.': 'Absolute drempels en lokale '
                                                                                'anomaliedetectie beantwoorden '
                                                                                'verschillende vragen.',
 'Acceleration magnitude': 'Versnellingsgrootte',
 'Acceleration raw values': 'Ruwe versnellingswaarden',
 'Accepted device values are stored separately after live CPM plausibility confirmation': 'Accepted device values are '
                                                                                          'stored separately after '
                                                                                          'live CPM plausibility '
                                                                                          'confirmation',
 'Active threshold profile': 'Actief drempelprofiel',
 'Adaptive background profile': 'Adaptief achtergrondprofiel',
 'Advanced': 'Geavanceerd',
 'Advanced diagnostics': 'Geavanceerde diagnose',
 'Advanced visuals': 'Geavanceerde visualisaties',
 'Affected GMC devices': 'Affected GMC devices',
 'Agreement': 'Overeenkomst',
 'Air-pressure source': 'Luchtdrukbron',
 'Air-pressure trend': 'Luchtdruktrend',
 'All GMC history was deleted': 'All GMC history was deleted',
 'All baselines and comparisons use the same robust quality-filtered measurements.': 'Alle baselines en vergelijkingen '
                                                                                     'gebruiken dezelfde robuuste '
                                                                                     'kwaliteitsgefilterde metingen.',
 'All connected GMC devices': 'Alle verbonden GMC-apparaten',
 'All devices': 'Alle apparaten',
 'All downloads below automatically use the GMC device currently shown in Analysis. Select another connected device above to change the report source.': 'All '
                                                                                                                                                         'downloads '
                                                                                                                                                         'below '
                                                                                                                                                         'automatically '
                                                                                                                                                         'use '
                                                                                                                                                         'the '
                                                                                                                                                         'GMC '
                                                                                                                                                         'device '
                                                                                                                                                         'currently '
                                                                                                                                                         'shown '
                                                                                                                                                         'in '
                                                                                                                                                         'Analysis. '
                                                                                                                                                         'Select '
                                                                                                                                                         'another '
                                                                                                                                                         'connected '
                                                                                                                                                         'device '
                                                                                                                                                         'above '
                                                                                                                                                         'to '
                                                                                                                                                         'change '
                                                                                                                                                         'the '
                                                                                                                                                         'report '
                                                                                                                                                         'source.',
 'All known GMC devices with stored history': 'All known GMC devices with stored history',
 'All statistical values, confidence intervals and diagnostics': 'Alle statistische waarden, '
                                                                 'betrouwbaarheidsintervallen en diagnostiek',
 'All {count} known GMC devices are connected': 'All {count} known GMC devices are connected',
 'Allow restore': 'Herstel toestaan',
 'Already assigned to {name}': 'Already assigned to {name}',
 'Analysis': 'Analyse',
 'Analysis JSON': 'Analyse-JSON',
 'Analysis PDF': 'Analyse-pdf',
 'Analysis depth': 'Analyseniveau',
 'Analysis for': 'Analyse voor',
 'Analysis is still being prepared': 'Analysis is still being prepared',
 'Analysis shown': 'Analyse wordt getoond',
 'Analysis, the traffic light and downloads will become meaningful after the first stored samples arrive.': 'Analyse, '
                                                                                                            'verkeerslicht '
                                                                                                            'en '
                                                                                                            'downloads '
                                                                                                            'worden '
                                                                                                            'zinvol '
                                                                                                            'zodra de '
                                                                                                            'eerste '
                                                                                                            'metingen '
                                                                                                            'zijn '
                                                                                                            'opgeslagen.',
 'Analyze this device': 'Dit apparaat analyseren',
 'Another report is already being generated': 'Er wordt al een ander rapport gegenereerd',
 'Another report or maintenance job is running': 'Another report or maintenance job is running',
 'Another report or restore job is running': 'Er wordt al een ander rapport of herstel uitgevoerd',
 'Another report, maintenance export, or restore job is running': 'Er wordt al een ander rapport, onderhoudsexport of '
                                                                  'herstelproces uitgevoerd.',
 'App Started At': 'App gestart om',
 'Apply': 'Apply',
 'Assessment': 'Beoordeling',
 'Assigned': 'Assigned',
 'At least 24 h reference and 6 h persistence are required': 'At least 24 h reference and 6 h persistence are required',
 'At least two daily background values are required.': 'Er zijn minimaal twee dagelijkse achtergrondwaarden nodig.',
 'At least {count} valid hourly values are required': 'Minstens {count} geldige uurwaarden zijn vereist',
 'At least {count} valid pairs are required': 'Minstens {count} geldige paren zijn vereist',
 'At least {days} days of learning data are required': 'Minstens {days} dagen leergegevens zijn vereist',
 'At least {span:g} hPa pressure variation is required': 'Minstens {span:g} hPa drukvariatie is vereist',
 'At the same time, the value is clearly above the usual local background. Review the trend and measurement conditions.': 'Tegelijkertijd '
                                                                                                                          'ligt '
                                                                                                                          'de '
                                                                                                                          'waarde '
                                                                                                                          'duidelijk '
                                                                                                                          'boven '
                                                                                                                          'de '
                                                                                                                          'gebruikelijke '
                                                                                                                          'lokale '
                                                                                                                          'achtergrond. '
                                                                                                                          'Controleer '
                                                                                                                          'de '
                                                                                                                          'trend '
                                                                                                                          'en '
                                                                                                                          'meetomstandigheden.',
 'Automatic device detection is running': 'Automatic device detection is running',
 'Automatic refresh is temporarily unavailable': 'Automatic refresh is temporarily unavailable',
 'Availability': 'Beschikbaarheid',
 'Available': 'Available',
 'Back to analysis': 'Back to analysis',
 'Background index': 'Achtergrondindex',
 'Background index compares the rolling 1 h mean with the available 7 d baseline.': 'Achtergrondindex = '
                                                                                    'voortschrijdend 1-uursgemiddelde '
                                                                                    'ten opzichte van de beschikbare '
                                                                                    '7-daagse basislijn.',
 'Background index formula explanation': 'Achtergrondindex = voortschrijdend 1-uursgemiddelde ten opzichte van de '
                                         'beschikbare 7-daagse basislijn.',
 'Background trend over days and months': 'Ontwikkeling van de achtergrond over dagen en maanden',
 'Backup is compatible and ready to restore.': 'Backup is compatible and ready to restore.',
 'Backup preview failed': 'Backup preview failed',
 'Baseline available': 'Referentie beschikbaar',
 'Baseline currently stable': 'Referentie momenteel stabiel',
 'Baseline deviation': 'Afwijking van referentie',
 'Baseline deviation, drift and sustained relative events': 'Referentieafwijking, drift en aanhoudende relatieve '
                                                            'gebeurtenissen',
 'Baseline deviation: {cpm} CPM ({percent}%)': 'Afwijking van basislijn: {cpm} CPM ({percent}%)',
 'Baseline drift: {value}%': 'Basislijndrift: {value}%',
 'Baseline learning in progress': 'Basislijn wordt nog geleerd',
 'Baseline readiness': 'Gereedheid van de basislijn',
 'Baseline: {value} CPM': 'Basislijn: {value} CPM',
 'Battery voltage': 'Batterijspanning',
 'Baud rate': 'Baudsnelheid',
 'Below the typical time profile': 'Onder het typische tijdprofiel',
 'Below warning threshold': 'Onder de waarschuwingsdrempel',
 'BfS and ICRP reference profiles convert annual dose values into continuous-rate equivalents for context. They are not official instantaneous alarm limits and cannot replace professional dose assessment.': 'BfS- '
                                                                                                                                                                                                               'en '
                                                                                                                                                                                                               'ICRP-referentieprofielen '
                                                                                                                                                                                                               'zetten '
                                                                                                                                                                                                               'jaardoses '
                                                                                                                                                                                                               'ter '
                                                                                                                                                                                                               'context '
                                                                                                                                                                                                               'om '
                                                                                                                                                                                                               'in '
                                                                                                                                                                                                               'equivalente '
                                                                                                                                                                                                               'continue '
                                                                                                                                                                                                               'dosistempi. '
                                                                                                                                                                                                               'Het '
                                                                                                                                                                                                               'zijn '
                                                                                                                                                                                                               'geen '
                                                                                                                                                                                                               'officiële '
                                                                                                                                                                                                               'directe '
                                                                                                                                                                                                               'alarmgrenzen '
                                                                                                                                                                                                               'en '
                                                                                                                                                                                                               'ze '
                                                                                                                                                                                                               'vervangen '
                                                                                                                                                                                                               'geen '
                                                                                                                                                                                                               'professionele '
                                                                                                                                                                                                               'dosisbeoordeling.',
 'BfS reference projection': 'BfS-referentieprojectie',
 'Both connected counters show a quality-filtered simultaneous rise': 'Beide aangesloten tellers tonen gelijktijdig '
                                                                      'een kwaliteitsgefilterde stijging',
 'Both connected counters show a simultaneous rise': 'Beide aangesloten tellers tonen een gelijktijdige stijging',
 'Broadly compatible with Poisson-like spread': 'Grotendeels passend bij een Poisson-achtige spreiding',
 'CPM': 'CPM',
 'CPM and derived dose rate': 'CPM en afgeleid dosistempo',
 'CPM distribution and Poisson comparison': 'CPM-verdeling en Poisson-vergelijking',
 'CPM distribution — {title}': 'CPM-verdeling — {title}',
 'CPM is the primary measurement.': 'CPM is de primaire meting.',
 'CPM per µSv/h': 'CPM per µSv/h',
 'CPM quality': 'CPM-kwaliteit',
 'CPM statistics  min {minimum:.0f} | max {maximum:.0f} | mean {mean:.2f} | median {median:.2f} | SD {sd:.2f} | P95 {p95:.2f} | missing {missing}': 'CPM-statistiek  '
                                                                                                                                                    'min '
                                                                                                                                                    '{minimum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'max '
                                                                                                                                                    '{maximum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'gemiddelde '
                                                                                                                                                    '{mean:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'mediaan '
                                                                                                                                                    '{median:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'SD '
                                                                                                                                                    '{sd:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'P95 '
                                                                                                                                                    '{p95:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'ontbrekend '
                                                                                                                                                    '{missing}',
 'CPM statistics: no accepted measurements in selected period': 'CPM-statistiek: geen geaccepteerde metingen in de '
                                                                'geselecteerde periode',
 'CPM–pressure correlation': 'CPM–luchtdrukcorrelatie',
 'CPM–temperature correlation': 'Correlatie CPM–temperatuur',
 'CPM–voltage correlation': 'Correlatie CPM–spanning',
 'CSV files preserve every accepted measurement without interpolation. PNG reports include CPM, temperature, voltage, optional raw signed gyro diagnostics, summary statistics, sample completeness, device identity, timezone, period and generation time. ZIP bundles additionally contain analysis JSON, daily summaries, events, histogram, heatmap and a multi-page PDF report.': 'CSV-bestanden '
                                                                                                                                                                                                                                                                                                                                                                                       'bewaren '
                                                                                                                                                                                                                                                                                                                                                                                       'elke '
                                                                                                                                                                                                                                                                                                                                                                                       'geaccepteerde '
                                                                                                                                                                                                                                                                                                                                                                                       'meting '
                                                                                                                                                                                                                                                                                                                                                                                       'zonder '
                                                                                                                                                                                                                                                                                                                                                                                       'interpolatie. '
                                                                                                                                                                                                                                                                                                                                                                                       'PNG-rapporten '
                                                                                                                                                                                                                                                                                                                                                                                       'bevatten '
                                                                                                                                                                                                                                                                                                                                                                                       'CPM, '
                                                                                                                                                                                                                                                                                                                                                                                       'temperatuur, '
                                                                                                                                                                                                                                                                                                                                                                                       'spanning, '
                                                                                                                                                                                                                                                                                                                                                                                       'optionele '
                                                                                                                                                                                                                                                                                                                                                                                       'onbewerkte '
                                                                                                                                                                                                                                                                                                                                                                                       'gyrodiagnostiek '
                                                                                                                                                                                                                                                                                                                                                                                       'met '
                                                                                                                                                                                                                                                                                                                                                                                       'teken, '
                                                                                                                                                                                                                                                                                                                                                                                       'samenvattende '
                                                                                                                                                                                                                                                                                                                                                                                       'statistieken, '
                                                                                                                                                                                                                                                                                                                                                                                       'volledigheid, '
                                                                                                                                                                                                                                                                                                                                                                                       'apparaatidentiteit, '
                                                                                                                                                                                                                                                                                                                                                                                       'tijdzone, '
                                                                                                                                                                                                                                                                                                                                                                                       'periode '
                                                                                                                                                                                                                                                                                                                                                                                       'en '
                                                                                                                                                                                                                                                                                                                                                                                       'aanmaaktijd. '
                                                                                                                                                                                                                                                                                                                                                                                       'ZIP-pakketten '
                                                                                                                                                                                                                                                                                                                                                                                       'bevatten '
                                                                                                                                                                                                                                                                                                                                                                                       'daarnaast '
                                                                                                                                                                                                                                                                                                                                                                                       'analyse-JSON, '
                                                                                                                                                                                                                                                                                                                                                                                       'dagsamenvattingen, '
                                                                                                                                                                                                                                                                                                                                                                                       'gebeurtenissen, '
                                                                                                                                                                                                                                                                                                                                                                                       'histogram, '
                                                                                                                                                                                                                                                                                                                                                                                       'heatmap '
                                                                                                                                                                                                                                                                                                                                                                                       'en '
                                                                                                                                                                                                                                                                                                                                                                                       'een '
                                                                                                                                                                                                                                                                                                                                                                                       'PDF-rapport '
                                                                                                                                                                                                                                                                                                                                                                                       'met '
                                                                                                                                                                                                                                                                                                                                                                                       'meerdere '
                                                                                                                                                                                                                                                                                                                                                                                       'pagina’s.',
 'Calibrated acceleration': 'Gekalibreerde versnelling',
 'Calibration profile': 'Kalibratieprofiel',
 'Capabilities': 'Mogelijkheden',
 'Check location, orientation and environmental conditions when a persistent jump appears.': 'Controleer locatie, '
                                                                                             'oriëntatie en '
                                                                                             'omgevingsomstandigheden '
                                                                                             'wanneer een blijvende '
                                                                                             'sprong verschijnt.',
 'Check manually': 'Handmatig controleren',
 'Check the Home Assistant general settings and restart the add-on.': 'Controleer de algemene Home '
                                                                      'Assistant-instellingen en start de add-on '
                                                                      'opnieuw.',
 'Check the USB cable and power supply if this continues for more than 15 minutes.': 'Controleer de USB-kabel en '
                                                                                     'voeding als dit langer dan 15 '
                                                                                     'minuten aanhoudt.',
 'Check the measurement conditions, observe the trend and verify the reading with an appropriate instrument if it persists.': 'Controleer '
                                                                                                                              'de '
                                                                                                                              'meetomstandigheden, '
                                                                                                                              'volg '
                                                                                                                              'de '
                                                                                                                              'trend '
                                                                                                                              'en '
                                                                                                                              'verifieer '
                                                                                                                              'de '
                                                                                                                              'meting '
                                                                                                                              'met '
                                                                                                                              'een '
                                                                                                                              'geschikt '
                                                                                                                              'instrument '
                                                                                                                              'als '
                                                                                                                              'deze '
                                                                                                                              'aanhoudt.',
 'Check the measurement location': 'Controleer de meetlocatie',
 'Choose counters by detected device name. The technical Linux path remains visible only for identification.': 'Choose '
                                                                                                               'counters '
                                                                                                               'by '
                                                                                                               'detected '
                                                                                                               'device '
                                                                                                               'name. '
                                                                                                               'The '
                                                                                                               'technical '
                                                                                                               'Linux '
                                                                                                               'path '
                                                                                                               'remains '
                                                                                                               'visible '
                                                                                                               'only '
                                                                                                               'for '
                                                                                                               'identification.',
 'Choose how much detail the analysis cards show. The selection is stored in this browser.': 'Kies hoeveel detail de '
                                                                                             'analysekaarten tonen. De '
                                                                                             'keuze wordt in deze '
                                                                                             'browser opgeslagen.',
 'Choose whether reports include all devices or one selected device.': 'Kies of rapporten alle apparaten of één '
                                                                       'geselecteerd apparaat bevatten.',
 'Clear': 'Clear',
 'Clearly above the usual local range': 'Duidelijk boven het gebruikelijke lokale bereik',
 'Clearly elevated': 'Duidelijk verhoogd',
 'Clearly elevated: clearly above the usual local range': 'Duidelijk verhoogd: duidelijk boven het gebruikelijke '
                                                          'lokale bereik',
 'Clock offset exceeds warning threshold': 'Klokafwijking overschrijdt waarschuwingsdrempel',
 'Clock synchronized': 'Klok gesynchroniseerd',
 'Close to Poisson expectation': 'Dicht bij de Poisson-verwachting',
 'Co-location and equal geometry must be ensured by the user': 'Co-location and equal geometry must be ensured by the '
                                                               'user',
 'Collapse all': 'Collapse all',
 'Combines recent trend, robust statistics, device agreement and learned background. It is a statistical aid, not a safety classification.': 'Combines '
                                                                                                                                             'recent '
                                                                                                                                             'trend, '
                                                                                                                                             'robust '
                                                                                                                                             'statistics, '
                                                                                                                                             'device '
                                                                                                                                             'agreement '
                                                                                                                                             'and '
                                                                                                                                             'learned '
                                                                                                                                             'background. '
                                                                                                                                             'It '
                                                                                                                                             'is '
                                                                                                                                             'a '
                                                                                                                                             'statistical '
                                                                                                                                             'aid, '
                                                                                                                                             'not '
                                                                                                                                             'a '
                                                                                                                                             'safety '
                                                                                                                                             'classification.',
 'Compared with local baseline': 'Vergeleken met de lokale basislijn',
 'Compares connected counters, device stability, shared events and the long-term relative response.': 'Compares '
                                                                                                      'connected '
                                                                                                      'counters, '
                                                                                                      'device '
                                                                                                      'stability, '
                                                                                                      'shared events '
                                                                                                      'and the '
                                                                                                      'long-term '
                                                                                                      'relative '
                                                                                                      'response.',
 'Compares pressure changes with quality-filtered counts. The result is only a statistical hint and never changes warning thresholds.': 'Compares '
                                                                                                                                        'pressure '
                                                                                                                                        'changes '
                                                                                                                                        'with '
                                                                                                                                        'quality-filtered '
                                                                                                                                        'counts. '
                                                                                                                                        'The '
                                                                                                                                        'result '
                                                                                                                                        'is '
                                                                                                                                        'only '
                                                                                                                                        'a '
                                                                                                                                        'statistical '
                                                                                                                                        'hint '
                                                                                                                                        'and '
                                                                                                                                        'never '
                                                                                                                                        'changes '
                                                                                                                                        'warning '
                                                                                                                                        'thresholds.',
 'Compares the current value with the usual background at this location.': 'Vergelijkt de huidige waarde met de '
                                                                           'gebruikelijke achtergrond op deze locatie.',
 'Comparison confidence': 'Betrouwbaarheid van de vergelijking',
 'Complete ZIP bundle': 'Volledig ZIP-pakket',
 'Complete history deletion failed': 'Complete history deletion failed',
 'Complete history deletion is disabled in the app configuration.': 'Het volledig verwijderen van de geschiedenis is '
                                                                    'uitgeschakeld in de appconfiguratie.',
 'Completeness: {value:.2f}%': 'Volledigheid: {value:.2f}%',
 'Confidence': 'Betrouwbaarheid',
 'Configured CPM conversion factor': 'Geconfigureerde CPM-omrekenfactor',
 'Configured baud rate': 'Geconfigureerde baudsnelheid',
 'Configured device name': 'Geconfigureerde apparaatnaam',
 'Configured location': 'Geconfigureerde locatie',
 'Configured measurement interval': 'Geconfigureerd meetinterval',
 'Confirmed original samples in 24 h · {accepted} stored': 'Confirmed original samples in 24 h · {accepted} stored',
 'Connect two devices to enable comparison.': 'Sluit twee apparaten aan om vergelijking te activeren.',
 'Connect two devices to learn a relative response factor.': 'Connect two devices to learn a relative response factor.',
 'Connected GMC devices': 'Verbonden GMC-apparaten',
 'Connected counters without an active stability warning': 'Verbonden tellers zonder actieve stabiliteitswaarschuwing',
 'Connected devices': 'Verbonden apparaten',
 'Connection active': 'Connection active',
 'Consecutive upload errors': 'Opeenvolgende uploadfouten',
 'Continue observing': 'Blijf observeren',
 'Coordinates': 'Coördinaten',
 'Correlation': 'Correlatie',
 'Correlation does not imply causation. Strong values should be investigated over longer periods before drawing conclusions.': 'Correlatie '
                                                                                                                               'betekent '
                                                                                                                               'geen '
                                                                                                                               'causaliteit. '
                                                                                                                               'Sterke '
                                                                                                                               'waarden '
                                                                                                                               'moeten '
                                                                                                                               'over '
                                                                                                                               'langere '
                                                                                                                               'perioden '
                                                                                                                               'worden '
                                                                                                                               'onderzocht '
                                                                                                                               'voordat '
                                                                                                                               'conclusies '
                                                                                                                               'worden '
                                                                                                                               'getrokken.',
 'Cosmic influence is possible': 'Kosmische invloed mogelijk',
 'Cosmic influence – statistical indication': 'Kosmische invloed – statistische aanwijzing',
 'Counter ID': 'Teller-ID',
 'Counting statistics': 'Telstatistiek',
 'Counting uncertainty (68%): −{minus:.2f}/+{plus:.2f} CPM · {impulses} impulses in {duration}': 'Counting uncertainty '
                                                                                                 '(68%): '
                                                                                                 '−{minus:.2f}/+{plus:.2f} '
                                                                                                 'CPM · {impulses} '
                                                                                                 'impulses in '
                                                                                                 '{duration}',
 'Counting uncertainty not available': 'Counting uncertainty not available',
 'Country': 'Land',
 'Coverage percent': 'Dekkingspercentage',
 'Coverage, gaps, runtime counters and derived dose-rate values': 'Dekking, hiaten, looptijdtellers en afgeleide '
                                                                  'dosistempo’s',
 'Critical': 'Kritiek',
 'Critical: danger threshold exceeded': 'Kritiek: gevarendrempel overschreden',
 'Current': 'Actueel',
 'Current air pressure': 'Huidige luchtdruk',
 'Current database size': 'Current database size',
 'Current difference': 'Huidig verschil',
 'Current value': 'Huidige waarde',
 'Current value is {z:+.2f} robust standard deviations from the 24 h median': 'De huidige waarde ligt {z:+.2f} '
                                                                              'robuuste standaardafwijkingen van de '
                                                                              '24-uursmediaan',
 'Current value is {z:+.2f} standard deviations from the 24 h mean': 'De huidige waarde ligt {z:+.2f} '
                                                                     'standaardafwijkingen van het 24-uursgemiddelde',
 'Current week bundle': 'Pakket huidige week',
 'Currently selected': 'Momenteel geselecteerd',
 'Custom period': 'Aangepaste periode',
 'Custom thresholds': 'Aangepaste drempels',
 'Daily and weekly profile is still being formed': 'Het dag- en weekprofiel wordt nog gevormd',
 'Daily quality-filtered medians are smoothed over seven days. The period cards compare the recent part of each period with the preceding part; detected jumps are statistical changes and do not determine their cause.': 'Dagelijkse, '
                                                                                                                                                                                                                           'op '
                                                                                                                                                                                                                           'kwaliteit '
                                                                                                                                                                                                                           'gefilterde '
                                                                                                                                                                                                                           'medianen '
                                                                                                                                                                                                                           'worden '
                                                                                                                                                                                                                           'over '
                                                                                                                                                                                                                           'zeven '
                                                                                                                                                                                                                           'dagen '
                                                                                                                                                                                                                           'afgevlakt. '
                                                                                                                                                                                                                           'De '
                                                                                                                                                                                                                           'periodekaarten '
                                                                                                                                                                                                                           'vergelijken '
                                                                                                                                                                                                                           'het '
                                                                                                                                                                                                                           'recente '
                                                                                                                                                                                                                           'deel '
                                                                                                                                                                                                                           'van '
                                                                                                                                                                                                                           'elke '
                                                                                                                                                                                                                           'periode '
                                                                                                                                                                                                                           'met '
                                                                                                                                                                                                                           'het '
                                                                                                                                                                                                                           'voorafgaande '
                                                                                                                                                                                                                           'deel; '
                                                                                                                                                                                                                           'gedetecteerde '
                                                                                                                                                                                                                           'sprongen '
                                                                                                                                                                                                                           'zijn '
                                                                                                                                                                                                                           'statistische '
                                                                                                                                                                                                                           'veranderingen '
                                                                                                                                                                                                                           'en '
                                                                                                                                                                                                                           'bepalen '
                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                           'oorzaak '
                                                                                                                                                                                                                           'niet.',
 'Daily summary CSV': 'Dagoverzicht CSV',
 'Danger threshold exceeded': 'Gevarendrempel overschreden',
 'Danger thresholds': 'Gevarendrempels',
 'Danger zone': 'Danger zone',
 'Dashboard navigation': 'Dashboard navigation',
 'Data exports': 'Data-export',
 'Data period': 'Data period',
 'Data quality': 'Datakwaliteit',
 'Data quality is too low for a reliable assessment': 'De gegevenskwaliteit is te laag voor een betrouwbare '
                                                      'beoordeling',
 'Data quality status unavailable': 'Datakwaliteitsstatus niet beschikbaar',
 'Data quality: {value}': 'Gegevenskwaliteit: {value}',
 'Database': 'Database',
 'Database health': 'Databasestatus',
 'Database size': 'Databasegrootte',
 'Date': 'Datum',
 'Delete all GMC history': 'Delete all GMC history',
 'Delete history': 'Delete history',
 'Deletion confirmation text must be exactly DELETE ALL GMC HISTORY': 'Deletion confirmation text must be exactly '
                                                                      'DELETE ALL GMC HISTORY',
 'Deletion is disabled by default.': 'Deletion is disabled by default.',
 'Derived dose rate': 'Afgeleid dosistempo',
 'Derived from 1 h mean CPM': 'Afgeleid van het 1-uursgemiddelde CPM',
 'Derived from 24 h mean CPM': 'Afgeleid van het 24-uursgemiddelde CPM',
 'Derived from 7 d mean CPM': 'Afgeleid van het 7-daags gemiddelde CPM',
 'Derived from latest CPM': 'Afgeleid van de laatste CPM',
 'Detailed interpretation and the most useful supporting values': 'Gedetailleerde interpretatie en de nuttigste '
                                                                  'ondersteunende waarden',
 'Detect, identify and assign GMC counters': 'Detect, identify and assign GMC counters',
 'Detected': 'Gedetecteerd',
 'Detected Capabilities': 'Gedetecteerde mogelijkheden',
 'Detected GMC device': 'Detected GMC device',
 'Detected baseline jumps': 'Gedetecteerde sprongen in de basislijn',
 'Detected relative anomaly events: {count}': 'Gedetecteerde relatieve anomaliegebeurtenissen: {count}',
 'Deviation': 'Afwijking',
 'Device': 'Apparaat',
 'Device Profile': 'Apparaatprofiel',
 'Device Time Errors Since Start': 'Fouten apparaatklok sinds start',
 'Device assignments saved': 'Device assignments saved',
 'Device assignments were saved.': 'Device assignments were saved.',
 'Device baseline': 'Apparaatbaseline',
 'Device capabilities': 'Apparaatmogelijkheden',
 'Device clock': 'Apparaatklok',
 'Device clock offset': 'Afwijking apparaatklok',
 'Device clock status': 'Status apparaatklok',
 'Device clock unavailable': 'Apparaatklok niet beschikbaar',
 'Device clock warning': 'Device clock warning',
 'Device comparison': 'Apparaatvergelijking',
 'Device details, live values and analysis selection are shown below.': 'Apparaatgegevens, actuele waarden en de '
                                                                        'analyseselectie staan hieronder.',
 'Device health warning': 'Device health warning',
 'Device position': 'Apparaatpositie',
 'Device status updated': 'Device status updated',
 'Device temperature is unavailable.': 'De apparaattemperatuur is niet beschikbaar.',
 'Device time': 'Apparaattijd',
 'Device-specific details are listed above.': 'Apparaatspecifieke details staan in het gedeelte hierboven.',
 'Device: {value}': 'Apparaat: {value}',
 'Devices': 'Devices',
 'Diagnostics JSON': 'Diagnostiek-JSON',
 'Disabled': 'Uitgeschakeld',
 'Discarded CPM peaks': 'Discarded CPM peaks',
 'Discarded unconfirmed CPM peaks': 'Discarded unconfirmed CPM peaks',
 'Display down': 'Plat, display omlaag',
 'Display up': 'Plat, display omhoog',
 'Dose rate = CPM / configured conversion factor ({factor:g} CPM per µSv/h).': 'Dosistempo = CPM / ingestelde '
                                                                               'conversiefactor ({factor:g} CPM per '
                                                                               'µSv/h).',
 'Dose rate formula explanation': 'Dosistempo = CPM / ingestelde conversiefactor ({factor:g} CPM per µSv/h).',
 'Dose-rate values are derived from CPM using the configured conversion factor.': 'Dosistempowaarden worden uit CPM '
                                                                                  'afgeleid met de ingestelde '
                                                                                  'conversiefactor.',
 'Dose-rate values, traffic-light states and events are derived indicators. CPM remains the primary measurement.': 'Dosistempowaarden, '
                                                                                                                   'verkeerslichtstatussen '
                                                                                                                   'en '
                                                                                                                   'gebeurtenissen '
                                                                                                                   'zijn '
                                                                                                                   'afgeleide '
                                                                                                                   'indicatoren. '
                                                                                                                   'CPM '
                                                                                                                   'blijft '
                                                                                                                   'de '
                                                                                                                   'primaire '
                                                                                                                   'meting.',
 'Download': 'Downloaden',
 'Downloads': 'Downloads',
 'Dual-tube measurement': 'Meting met twee buizen',
 'Duration [s]': 'Duur [s]',
 'During the learning phase, leave the counters in a stable location and allow additional measurements to accumulate.': 'Laat '
                                                                                                                        'de '
                                                                                                                        'tellers '
                                                                                                                        'tijdens '
                                                                                                                        'de '
                                                                                                                        'leerfase '
                                                                                                                        'op '
                                                                                                                        'een '
                                                                                                                        'stabiele '
                                                                                                                        'locatie '
                                                                                                                        'staan '
                                                                                                                        'en '
                                                                                                                        'verzamel '
                                                                                                                        'meer '
                                                                                                                        'metingen.',
 'Each device has its own MQTT identity and history. The cards show the latest accepted measurement.': 'Elk apparaat '
                                                                                                       'heeft een '
                                                                                                       'eigen '
                                                                                                       'MQTT-identiteit '
                                                                                                       'en '
                                                                                                       'geschiedenis. '
                                                                                                       'De kaarten '
                                                                                                       'tonen de '
                                                                                                       'laatst '
                                                                                                       'geaccepteerde '
                                                                                                       'meting.',
 'Each physical serial device can only be assigned once': 'Each physical serial device can only be assigned once',
 'Elevated': 'Verhoogd',
 'Elevated relative background': 'Verhoogde relatieve achtergrond',
 'Elevated: within warning range': 'Verhoogd: binnen het waarschuwingsbereik',
 'Elevation': 'Hoogte',
 'Enable complete history deletion in the app configuration and restart only when deletion is planned.': 'Enable '
                                                                                                         'complete '
                                                                                                         'history '
                                                                                                         'deletion in '
                                                                                                         'the app '
                                                                                                         'configuration '
                                                                                                         'and restart '
                                                                                                         'only when '
                                                                                                         'deletion is '
                                                                                                         'planned.',
 'Enable enable_restore in the app configuration and restart only when a restore is planned.': 'Schakel enable_restore '
                                                                                               'in de app-configuratie '
                                                                                               'in en herstart alleen '
                                                                                               'wanneer een herstel '
                                                                                               'gepland is.',
 'Enable “{setting}” in the app configuration and restart only when a restore is planned.': 'Schakel ‘{setting}’ in de '
                                                                                            'app-configuratie in en '
                                                                                            'start de app alleen '
                                                                                            'opnieuw wanneer een '
                                                                                            'herstel is gepland.',
 'End time UTC': 'Eindtijd UTC',
 'End time local': 'Lokale eindtijd',
 'Entities': 'Entiteiten',
 'Environment': 'Omgeving',
 'Error time': 'Tijdstip van fout',
 'Estimated pressure influence': 'Geschatte drukinvloed',
 'Evaluated by': 'Beoordeeld op basis van',
 'Evaluates the current value using the configured thresholds.': 'Beoordeelt de actuele waarde aan de hand van de '
                                                                 'ingestelde drempels.',
 'Events CSV': 'Gebeurtenissen-CSV',
 'Events and diagnostics': 'Events and diagnostics',
 'Events last 24 h': 'Gebeurtenissen van de afgelopen 24 uur',
 'Excellent': 'Uitstekend',
 'Excluded measurements': 'Uitgesloten metingen',
 'Excluded pairs': 'Uitgesloten paren',
 'Expand all': 'Expand all',
 'Expected samples': 'Verwachte metingen',
 'Expert view': 'Expertweergave',
 'Explanation of the two assessments': 'Uitleg van de twee beoordelingen',
 'Export details': 'Exportdetails',
 'Extremely elevated': 'Extreem verhoogd',
 'Extremely elevated: far above the usual local range': 'Extreem verhoogd: ver boven het gebruikelijke lokale bereik',
 'Falling': 'Dalend',
 'Falling air pressure can slightly increase the share of cosmically generated secondary radiation at ground level, while rising air pressure tends to reduce it; the model detects only such statistical relationships and cannot clearly distinguish them from other natural influences.': 'Een '
                                                                                                                                                                                                                                                                                             'dalende '
                                                                                                                                                                                                                                                                                             'luchtdruk '
                                                                                                                                                                                                                                                                                             'kan '
                                                                                                                                                                                                                                                                                             'het '
                                                                                                                                                                                                                                                                                             'aandeel '
                                                                                                                                                                                                                                                                                             'kosmisch '
                                                                                                                                                                                                                                                                                             'opgewekte '
                                                                                                                                                                                                                                                                                             'secundaire '
                                                                                                                                                                                                                                                                                             'straling '
                                                                                                                                                                                                                                                                                             'op '
                                                                                                                                                                                                                                                                                             'grondniveau '
                                                                                                                                                                                                                                                                                             'licht '
                                                                                                                                                                                                                                                                                             'verhogen, '
                                                                                                                                                                                                                                                                                             'terwijl '
                                                                                                                                                                                                                                                                                             'een '
                                                                                                                                                                                                                                                                                             'stijgende '
                                                                                                                                                                                                                                                                                             'luchtdruk '
                                                                                                                                                                                                                                                                                             'dit '
                                                                                                                                                                                                                                                                                             'eerder '
                                                                                                                                                                                                                                                                                             'verlaagt; '
                                                                                                                                                                                                                                                                                             'het '
                                                                                                                                                                                                                                                                                             'model '
                                                                                                                                                                                                                                                                                             'herkent '
                                                                                                                                                                                                                                                                                             'alleen '
                                                                                                                                                                                                                                                                                             'zulke '
                                                                                                                                                                                                                                                                                             'statistische '
                                                                                                                                                                                                                                                                                             'verbanden '
                                                                                                                                                                                                                                                                                             'en '
                                                                                                                                                                                                                                                                                             'kan '
                                                                                                                                                                                                                                                                                             'deze '
                                                                                                                                                                                                                                                                                             'niet '
                                                                                                                                                                                                                                                                                             'duidelijk '
                                                                                                                                                                                                                                                                                             'onderscheiden '
                                                                                                                                                                                                                                                                                             'van '
                                                                                                                                                                                                                                                                                             'andere '
                                                                                                                                                                                                                                                                                             'natuurlijke '
                                                                                                                                                                                                                                                                                             'invloeden.',
 'Falling air pressure is often associated with a slightly higher intensity of cosmically generated secondary radiation at ground level, while rising air pressure is associated with a slightly lower intensity. The strength of this relationship depends on detector, location and atmosphere; the cause cannot be determined unambiguously from total counts.': 'Een '
                                                                                                                                                                                                                                                                                                                                                                    'dalende '
                                                                                                                                                                                                                                                                                                                                                                    'luchtdruk '
                                                                                                                                                                                                                                                                                                                                                                    'hangt '
                                                                                                                                                                                                                                                                                                                                                                    'vaak '
                                                                                                                                                                                                                                                                                                                                                                    'samen '
                                                                                                                                                                                                                                                                                                                                                                    'met '
                                                                                                                                                                                                                                                                                                                                                                    'een '
                                                                                                                                                                                                                                                                                                                                                                    'iets '
                                                                                                                                                                                                                                                                                                                                                                    'hogere '
                                                                                                                                                                                                                                                                                                                                                                    'intensiteit '
                                                                                                                                                                                                                                                                                                                                                                    'van '
                                                                                                                                                                                                                                                                                                                                                                    'kosmisch '
                                                                                                                                                                                                                                                                                                                                                                    'opgewekte '
                                                                                                                                                                                                                                                                                                                                                                    'secundaire '
                                                                                                                                                                                                                                                                                                                                                                    'straling '
                                                                                                                                                                                                                                                                                                                                                                    'op '
                                                                                                                                                                                                                                                                                                                                                                    'grondniveau, '
                                                                                                                                                                                                                                                                                                                                                                    'terwijl '
                                                                                                                                                                                                                                                                                                                                                                    'een '
                                                                                                                                                                                                                                                                                                                                                                    'stijgende '
                                                                                                                                                                                                                                                                                                                                                                    'luchtdruk '
                                                                                                                                                                                                                                                                                                                                                                    'samenhangt '
                                                                                                                                                                                                                                                                                                                                                                    'met '
                                                                                                                                                                                                                                                                                                                                                                    'een '
                                                                                                                                                                                                                                                                                                                                                                    'iets '
                                                                                                                                                                                                                                                                                                                                                                    'lagere '
                                                                                                                                                                                                                                                                                                                                                                    'intensiteit. '
                                                                                                                                                                                                                                                                                                                                                                    'De '
                                                                                                                                                                                                                                                                                                                                                                    'sterkte '
                                                                                                                                                                                                                                                                                                                                                                    'van '
                                                                                                                                                                                                                                                                                                                                                                    'dit '
                                                                                                                                                                                                                                                                                                                                                                    'verband '
                                                                                                                                                                                                                                                                                                                                                                    'hangt '
                                                                                                                                                                                                                                                                                                                                                                    'af '
                                                                                                                                                                                                                                                                                                                                                                    'van '
                                                                                                                                                                                                                                                                                                                                                                    'detector, '
                                                                                                                                                                                                                                                                                                                                                                    'locatie '
                                                                                                                                                                                                                                                                                                                                                                    'en '
                                                                                                                                                                                                                                                                                                                                                                    'atmosfeer; '
                                                                                                                                                                                                                                                                                                                                                                    'uit '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'totale '
                                                                                                                                                                                                                                                                                                                                                                    'tellingen '
                                                                                                                                                                                                                                                                                                                                                                    'kan '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'oorzaak '
                                                                                                                                                                                                                                                                                                                                                                    'niet '
                                                                                                                                                                                                                                                                                                                                                                    'eenduidig '
                                                                                                                                                                                                                                                                                                                                                                    'worden '
                                                                                                                                                                                                                                                                                                                                                                    'bepaald.',
 'Fano factor': 'Fano-factor',
 'Fano factor = variance / mean; a value near 1 is consistent with Poisson-like counting statistics.': 'Fano-factor = '
                                                                                                       'variantie / '
                                                                                                       'gemiddelde; '
                                                                                                       'een waarde '
                                                                                                       'rond 1 past '
                                                                                                       'bij '
                                                                                                       'Poisson-achtige '
                                                                                                       'telstatistiek.',
 'Fano factor formula explanation': 'Fano-factor = variantie / gemiddelde; een waarde rond 1 past bij Poisson-achtige '
                                    'telstatistiek.',
 'Fano factor: {value}': 'Fano-factor: {value}',
 'Far above the usual local range': 'Ver boven het gebruikelijke lokale bereik',
 'File size': 'File size',
 'Firmware version': 'Firmwareversie',
 'Flat': 'Flat',
 'Fleet intelligence': 'Analyse van de apparaatgroep',
 'Format': 'Formaat',
 'Fri': 'Vr',
 'Friday': 'Vrijdag',
 'Full history ZIP': 'Volledige geschiedenis-ZIP',
 'GMC Radiation Monitor': 'GMC-stralingsmonitor',
 'GMC Radiation Monitoring': 'GMC-stralingsbewaking',
 'GMC Reports': 'GMC-rapporten',
 'GMC analysis report {period}': 'GMC-analyserapport {period}',
 'GMC detected': 'GMC detected',
 'GMC devices are being detected automatically': 'GMC devices are being detected automatically',
 'GMC radiation analysis report': 'GMC-stralingsanalyserapport',
 'GMC radiation monitoring report {period}': 'GMC-stralingsmonitoringsrapport {period}',
 'GMC-300/320 family': 'GMC-300/320-familie',
 'GMC-320 and GMC-500+ combined': 'GMC-320 and GMC-500+ combined',
 'GMC-500 family': 'GMC-500-familie',
 'GMC-600 family': 'GMC-600-familie',
 'GMCMap consecutive upload errors': 'Opeenvolgende GMCMap-uploadfouten',
 'GMCMap counter ID': 'GMCMap-teller-ID',
 'GMCMap is enabled, but this device has no counter ID mapping.': 'GMCMap is ingeschakeld, maar aan dit apparaat is '
                                                                  'geen teller-ID toegewezen.',
 'GMCMap last HTTP status': 'Laatste GMCMap-HTTP-status',
 'GMCMap last error time': 'Tijdstip van laatste GMCMap-fout',
 'GMCMap last server response': 'Laatste GMCMap-serverreactie',
 'GMCMap last successful upload': 'Laatste geslaagde GMCMap-upload',
 'GMCMap last upload attempt': 'Laatste GMCMap-uploadpoging',
 'GMCMap last upload error': 'Laatste GMCMap-uploadfout',
 'GMCMap last uploaded CPM': 'Laatst naar GMCMap geüploade CPM',
 'GMCMap next upload': 'Volgende GMCMap-upload',
 'GMCMap successful uploads since start': 'Geslaagde GMCMap-uploads sinds start',
 'GMCMap upload errors since start': 'GMCMap-uploadfouten sinds start',
 'GMCMap upload status': 'GMCMap-uploadstatus',
 'GQ manufacturer recommendation': 'GQ-fabrikantadvies',
 'Gaps are excluded from effective counting time': 'Gaps are excluded from effective counting time',
 'Generated export exceeds the {limit_mib} MiB safety limit': 'De gegenereerde export overschrijdt de '
                                                              'veiligheidslimiet van {limit_mib} MiB.',
 'Generated maintenance export exceeds the 128 MiB safety limit': 'De gegenereerde onderhoudsexport overschrijdt de '
                                                                  'veiligheidslimiet van 128 MiB.',
 'Generated report exceeds the 64 MiB safety limit': 'Het gegenereerde rapport overschrijdt de veiligheidslimiet van '
                                                     '64 MiB',
 'Generic GQ GMC / RFC1201-compatible device': 'Generiek GQ GMC-apparaat dat compatibel is met RFC1201',
 'Generic RFC1201-compatible device': 'Generiek RFC1201-compatibel apparaat',
 'Global report settings': 'Algemene rapport- en exportinstellingen',
 'Good': 'Goed',
 'Green': 'Groen',
 'Gyro Calibrated {axis}': 'Gyro Calibrated {axis}',
 'Gyro Errors Since Start': 'Gyrofouten sinds start',
 'Gyro Raw {axis}': 'Ruwe gyrowaarde {axis}',
 'Gyro X': 'Gyro X',
 'Gyro Y': 'Gyro Y',
 'Gyro Z': 'Gyro Z',
 'Gyro data will be included when available.': 'Gyrogegevens worden opgenomen wanneer ze beschikbaar zijn.',
 'Gyro errors': 'Gyroscoopfouten',
 'Gyro recording is disabled.': 'Gyroregistratie is uitgeschakeld.',
 'Gyroscope': 'Gyroscoop',
 'Hardware model': 'Hardwaremodel',
 'Heartbeat Errors Since Start': 'Heartbeatfouten sinds start',
 'Heartbeat mode': 'Heartbeatmodus',
 'Heartbeat rolling 60 s CPM': 'Heartbeat voortschrijdende 60 s CPM',
 'Heatmap PNG': 'Heatmap-PNG',
 'Heuristic statistical assessment; not a radiation-protection classification.': 'Heuristische statistische '
                                                                                 'beoordeling; geen '
                                                                                 'stralingsbeschermingsclassificatie.',
 'High': 'Hoog',
 'High relative increase': 'Sterke relatieve stijging',
 'High-dose Tube CPM': 'Hogedosisbuis CPM',
 'High-dose tube': 'Hogedosisbuis',
 'Highest stored 24 h value': 'Hoogste opgeslagen waarde in 24 uur',
 'Histogram PNG': 'Histogram-PNG',
 'Historical chart is still being formed': 'De historische grafiek wordt nog opgebouwd',
 'Historical development': 'Historische ontwikkeling',
 'History': 'History',
 'History Write Errors Since Start': 'Schrijffouten in historie sinds start',
 'History deleted': 'History deleted',
 'History maintenance': 'Geschiedenisbeheer',
 'History restore failed': 'Herstel van historie mislukt',
 'History restore is disabled. Enable enable_restore in the app configuration and restart.': 'Herstel van historie is '
                                                                                             'uitgeschakeld. Schakel '
                                                                                             'enable_restore in de '
                                                                                             'app-configuratie in en '
                                                                                             'herstart.',
 'History restore is disabled. Enable “{setting}” in the app configuration and restart.': 'Geschiedenisherstel is '
                                                                                          'uitgeschakeld. Schakel '
                                                                                          '‘{setting}’ in de '
                                                                                          'app-configuratie in en '
                                                                                          'start opnieuw.',
 'History storage warning': 'History storage warning',
 'Home Assistant API client is not configured': 'Home Assistant API client is not configured',
 'Home Assistant Recorder entity patterns': 'Home Assistant Recorder entity patterns',
 'Home Assistant Recorder history cleared': 'Home Assistant Recorder history cleared',
 'Home Assistant host UART': 'Home Assistant host UART',
 'Home Assistant location': 'Home Assistant-locatie',
 'How are connected counters compared?': 'Hoe worden aangesloten tellers vergeleken?',
 'How closely the observed spread resembles Poisson-like counting': 'Hoe sterk de waargenomen spreiding lijkt op '
                                                                    'Poisson-achtige tellingen',
 'How is data quality evaluated?': 'Hoe wordt de gegevenskwaliteit beoordeeld?',
 'How is the background profile calculated?': 'Hoe wordt het achtergrondprofiel berekend?',
 'How is the pressure relationship assessed?': 'Hoe wordt de relatie met luchtdruk beoordeeld?',
 'However, the value is noticeably above the usual local background. Observe the trend.': 'De waarde ligt echter '
                                                                                          'opvallend boven de '
                                                                                          'gebruikelijke lokale '
                                                                                          'achtergrond. Volg de trend.',
 'ICRP reference projection': 'ICRP-referentieprojectie',
 'Inclination': 'Helling',
 'Ingest diagnostics cleared': 'Ingest diagnostics cleared',
 'Inspecting backup…': 'Inspecting backup…',
 'Insufficient': 'Onvoldoende',
 'Insufficient history for level-shift detection': 'Insufficient history for level-shift detection',
 'Insufficient paired daily values': 'Onvoldoende vergelijkbare dagwaarden',
 'Integrity': 'Integriteit',
 'Intelligence': 'Intelligence',
 'Intelligent radiation analysis': 'Intelligente stralingsanalyse',
 'Internal database cleared': 'Internal database cleared',
 'Internal serial port': 'Internal serial port',
 'Interpret statistics with coverage in mind': 'Interpreteer statistieken met de dekking in gedachten',
 'Interpret these values together with coverage, device stability and the historical background.': 'Interpreteer deze '
                                                                                                   'waarden samen met '
                                                                                                   'dekking, '
                                                                                                   'apparaatstabiliteit '
                                                                                                   'en de historische '
                                                                                                   'achtergrond.',
 'Interpretation': 'Interpretatie',
 'Interval diagnostics': 'Intervaldiagnose',
 'Invalid deletion confirmation': 'Invalid deletion confirmation',
 'Invalid device clock response': 'Ongeldig antwoord van apparaatklok',
 'Invalid request parameters': 'Ongeldige aanvraagparameters.',
 'Invalid serial configuration request': 'Invalid serial configuration request',
 'Keep both counters close together and similarly oriented when using the comparison as a reference.': 'Houd beide '
                                                                                                       'tellers dicht '
                                                                                                       'bij elkaar en '
                                                                                                       'op dezelfde '
                                                                                                       'manier '
                                                                                                       'georiënteerd '
                                                                                                       'wanneer je de '
                                                                                                       'vergelijking '
                                                                                                       'als referentie '
                                                                                                       'gebruikt.',
 'Known radio or Zigbee adapter': 'Known radio or Zigbee adapter',
 'Language': 'Taal',
 'Last HTTP status': 'Laatste HTTP-status',
 'Last Successful Measurement': 'Laatste geslaagde meting',
 'Last attempt': 'Laatste poging',
 'Last backup requested in this browser': 'Last backup requested in this browser',
 'Last sample age': 'Leeftijd van laatste meting',
 'Last server response': 'Laatste serverreactie',
 'Last successful storage': 'Last successful storage',
 'Last update': 'Laatste update',
 'Last upload': 'Laatste upload',
 'Last upload error': 'Laatste uploadfout',
 'Latest CPM': 'Actuele CPM',
 'Latest CPM uncertainty': 'Latest CPM uncertainty',
 'Latest CPM vs 24 h distribution': 'Laatste CPM vergeleken met de 24-uursverdeling',
 'Latest accepted value': 'Latest accepted value',
 'Latest dose rate': 'Actueel dosistempo',
 'Latest measurement': 'Laatste meting',
 'Learned Radiation Baseline': 'Aangeleerde stralingsbasislijn',
 'Learned from local history': 'Geleerd uit lokale historie',
 'Learned pressure coefficient': 'Geleerde drukcoëfficiënt',
 'Learning baseline': 'Referentieniveau leren',
 'Learning basis': 'Leerbasis',
 'Learning progress': 'Leervoortgang',
 'Learning: not enough local history yet': 'Leren: nog onvoldoende lokale historie',
 'Learning: {pairs}/{minimum} pairs · {days:.1f}/{minimum_days:g} days': 'Learning: {pairs}/{minimum} pairs · '
                                                                         '{days:.1f}/{minimum_days:g} days',
 'Learns typical values for the current hour, weekday and temperature range and shows long-term drift.': 'Learns '
                                                                                                         'typical '
                                                                                                         'values for '
                                                                                                         'the current '
                                                                                                         'hour, '
                                                                                                         'weekday and '
                                                                                                         'temperature '
                                                                                                         'range and '
                                                                                                         'shows '
                                                                                                         'long-term '
                                                                                                         'drift.',
 'Less variable than Poisson expectation': 'Minder variabel dan de Poisson-verwachting',
 'Likely device-specific deviation': 'Waarschijnlijk apparaatspecifieke afwijking',
 'Limited': 'Beperkt',
 'Live radiation CPS': 'Live straling CPS',
 'Live system status': 'Live system status',
 'Local background analysis': 'Lokale achtergrondanalyse',
 'Local background is still being learned': 'De lokale achtergrond wordt nog aangeleerd',
 'Local background model is available': 'Het lokale achtergrondmodel is beschikbaar',
 'Local baseline': 'Lokale basislijn',
 'Local hour': 'Lokale uur',
 'Local time [{timezone}]': 'Lokale tijd [{timezone}]',
 'Local timestamp': 'Lokale tijdstempel',
 'Location data comes from the Home Assistant general settings and is not sent to an external geocoding service.': 'De '
                                                                                                                   'locatiegegevens '
                                                                                                                   'komen '
                                                                                                                   'uit '
                                                                                                                   'de '
                                                                                                                   'algemene '
                                                                                                                   'Home '
                                                                                                                   'Assistant-instellingen '
                                                                                                                   'en '
                                                                                                                   'worden '
                                                                                                                   'niet '
                                                                                                                   'naar '
                                                                                                                   'een '
                                                                                                                   'externe '
                                                                                                                   'geocoderingsdienst '
                                                                                                                   'verzonden.',
 'Location unavailable': 'Locatie niet beschikbaar',
 'Long-term context': 'Langetermijncontext',
 'Long-term drift': 'Langetermijndrift',
 'Long-term relative factor available': 'Long-term relative factor available',
 'Long-term relative response': 'Long-term relative response',
 'Longest gap': 'Langste meetonderbreking',
 'Longest gap [s]': 'Langste onderbreking [s]',
 'Longest gap: {seconds} s': 'Langste onderbreking: {seconds} s',
 'Low': 'Laag',
 'Low-dose Tube CPM': 'Lagedosisbuis CPM',
 'Low-dose tube': 'Lagedosisbuis',
 'Lowest stored 24 h value': 'Laagste opgeslagen waarde in 24 uur',
 'Machine-readable statistics and event data': 'Machineleesbare statistieken en gebeurtenisgegevens',
 'Maximum': 'Maximum',
 'Maximum CPM': 'Maximale CPM',
 'Maximum background index [%]': 'Maximale achtergrondindex [%]',
 'Mean': 'Gemiddelde',
 'Mean CPM': 'Gemiddelde CPM',
 'Mean CPM by weekday and hour — {title}': 'Gemiddelde CPM per weekdag en uur — {title}',
 'Mean absolute difference': 'Gemiddeld absoluut verschil',
 'Mean: {value} CPM': 'Gemiddelde: {value} CPM',
 'Measurement interval': 'Meetinterval',
 'Measurement-site baseline': 'Gecombineerde baseline van de meetlocatie',
 'Measurements': 'Measurements',
 'Measurements are sent to the public GMCMap service.': 'Metingen worden naar de openbare GMCMap-dienst verzonden.',
 'Measurements to delete': 'Measurements to delete',
 'Median': 'Mediaan',
 'Median CPM': 'Mediane CPM',
 'Median: {value} CPM': 'Mediaan: {value} CPM',
 'Medium': 'Gemiddeld',
 'Merge a compatible SQLite backup into the current history. Existing rows are preserved or updated by device serial and UTC timestamp.': 'Voeg '
                                                                                                                                          'een '
                                                                                                                                          'compatibele '
                                                                                                                                          'SQLite-back-up '
                                                                                                                                          'samen '
                                                                                                                                          'met '
                                                                                                                                          'de '
                                                                                                                                          'huidige '
                                                                                                                                          'geschiedenis. '
                                                                                                                                          'Bestaande '
                                                                                                                                          'regels '
                                                                                                                                          'blijven '
                                                                                                                                          'behouden '
                                                                                                                                          'of '
                                                                                                                                          'worden '
                                                                                                                                          'bijgewerkt '
                                                                                                                                          'op '
                                                                                                                                          'serienummer '
                                                                                                                                          'en '
                                                                                                                                          'UTC-tijdstempel.',
 'Merged {rows} measurement rows from schema {schema}.': '{rows} meetrijen uit schema {schema} zijn samengevoegd.',
 'Minimum / maximum: {minimum} / {maximum} CPM': 'Minimum / maximum: {minimum} / {maximum} CPM',
 'Minimum CPM': 'Minimale CPM',
 'Mixed device profiles': 'Gemengde apparaatprofielen',
 'Moderate linear relationship': 'Matige lineaire relatie',
 'Mon': 'Ma',
 'Monday': 'Maandag',
 'More history is needed before the relative background indicator is classified.': 'Meer geschiedenis is nodig voordat '
                                                                                   'de relatieve achtergrondindicator '
                                                                                   'wordt geclassificeerd.',
 'More history is needed; approximately {count} additional measurements are required.': 'More history is needed; '
                                                                                        'approximately {count} '
                                                                                        'additional measurements are '
                                                                                        'required.',
 'More measurements are needed for this weekday and hour.': 'Voor deze weekdag en dit uur zijn meer metingen nodig.',
 'More variable than Poisson expectation': 'Variabeler dan de Poisson-verwachting',
 'Move away from the suspected source if safe to do so, avoid unnecessary exposure and seek qualified radiation-protection advice.': 'Ga '
                                                                                                                                     'indien '
                                                                                                                                     'veilig '
                                                                                                                                     'mogelijk '
                                                                                                                                     'weg '
                                                                                                                                     'van '
                                                                                                                                     'de '
                                                                                                                                     'vermoedelijke '
                                                                                                                                     'bron, '
                                                                                                                                     'vermijd '
                                                                                                                                     'onnodige '
                                                                                                                                     'blootstelling '
                                                                                                                                     'en '
                                                                                                                                     'vraag '
                                                                                                                                     'deskundig '
                                                                                                                                     'stralingsbeschermingsadvies.',
 'Never': 'Nooit',
 'Newest sample': 'Nieuwste meting',
 'Next upload': 'Volgende upload',
 'No GMC device detected': 'No GMC device detected',
 'No action is required while the result remains normal. Investigate persistent changes by checking the measurement location and comparing both devices.': 'Er '
                                                                                                                                                           'is '
                                                                                                                                                           'geen '
                                                                                                                                                           'actie '
                                                                                                                                                           'nodig '
                                                                                                                                                           'zolang '
                                                                                                                                                           'het '
                                                                                                                                                           'resultaat '
                                                                                                                                                           'normaal '
                                                                                                                                                           'blijft. '
                                                                                                                                                           'Onderzoek '
                                                                                                                                                           'blijvende '
                                                                                                                                                           'veranderingen '
                                                                                                                                                           'door '
                                                                                                                                                           'de '
                                                                                                                                                           'meetlocatie '
                                                                                                                                                           'te '
                                                                                                                                                           'controleren '
                                                                                                                                                           'en '
                                                                                                                                                           'beide '
                                                                                                                                                           'apparaten '
                                                                                                                                                           'te '
                                                                                                                                                           'vergelijken.',
 'No action is required. Continue normal monitoring.': 'Er is geen actie nodig. Ga door met normale bewaking.',
 'No action is required. The assessment becomes more reliable as additional measurements are collected.': 'Er is geen '
                                                                                                          'actie '
                                                                                                          'nodig. De '
                                                                                                          'beoordeling '
                                                                                                          'wordt '
                                                                                                          'betrouwbaarder '
                                                                                                          'naarmate '
                                                                                                          'meer '
                                                                                                          'metingen '
                                                                                                          'worden '
                                                                                                          'verzameld.',
 'No action required': 'Geen actie nodig',
 'No active device warnings': 'No active device warnings',
 'No connected GMC device': 'No connected GMC device',
 'No connected counter is available yet. The next serial scan runs automatically.': 'No connected counter is available '
                                                                                    'yet. The next serial scan runs '
                                                                                    'automatically.',
 'No connected devices.': 'Geen apparaten verbonden.',
 'No current pressure source is available': 'Geen actuele luchtdrukbron beschikbaar',
 'No data': 'Geen gegevens',
 'No known GMC devices': 'No known GMC devices',
 'No matching Home Assistant entities': 'No matching Home Assistant entities',
 'No measurement yet': 'Nog geen meting',
 'No measurements in selected period': 'Geen metingen in de geselecteerde periode',
 'No measurements yet.': 'Nog geen metingen.',
 'No persistent level shift detected': 'No persistent level shift detected',
 'No position changes recorded.': 'Geen positiewijzigingen geregistreerd.',
 'No pressure variation': 'Onvoldoende drukvariatie',
 'No pressure-typical signature': 'Geen druktypische signatuur',
 'No pronounced baseline jumps detected.': 'Geen uitgesproken sprongen in de basislijn gedetecteerd.',
 'No reports have been requested in this browser yet.': 'No reports have been requested in this browser yet.',
 'No shared rise detected.': 'Geen gezamenlijke stijging gedetecteerd.',
 'No stored measurements': 'No stored measurements',
 'No suitable serial device was found.': 'No suitable serial device was found.',
 'No sustained relative anomaly events detected': 'Geen aanhoudende relatieve anomaliegebeurtenissen gedetecteerd',
 'No valid CPM baseline': 'Geen geldige CPM-baseline',
 'Normal': 'Normaal',
 'Normal for this time': 'Normaal voor dit tijdstip',
 'Normal: within the usual local range': 'Normaal: binnen het gebruikelijke lokale bereik',
 'Not available yet — at least two CPM samples are required': 'Nog niet beschikbaar — minstens twee CPM-metingen zijn '
                                                              'vereist',
 'Not available yet — more baseline history is required': 'Nog niet beschikbaar — meer basislijngeschiedenis is '
                                                          'vereist',
 'Not available yet — more paired samples are required': 'Nog niet beschikbaar — meer gekoppelde metingen zijn vereist',
 'Not available yet — no temperature samples were stored in the current 24 h window.': 'Nog niet beschikbaar — in het '
                                                                                       'huidige 24-uursvenster zijn '
                                                                                       'geen temperatuurmetingen '
                                                                                       'opgeslagen.',
 'Not available yet — the 24 h CPM series needs variation and at least two samples': 'Nog niet beschikbaar — de '
                                                                                     '24-uurs-CPM-reeks moet variëren '
                                                                                     'en minstens twee metingen '
                                                                                     'bevatten',
 'Not available yet — the 24 h mean and spread are still insufficient': 'Nog niet beschikbaar — het 24-uursgemiddelde '
                                                                        'en de spreiding zijn nog onvoldoende',
 'Not available — CPM did not vary during this period': 'Niet beschikbaar — CPM varieerde niet in deze periode',
 'Not available — the sensor value did not vary during this period': 'Niet beschikbaar — de sensorwaarde varieerde '
                                                                     'niet in deze periode',
 'Not configured': 'Niet geconfigureerd',
 'Not connected': 'Not connected',
 'Not detected yet': 'Nog niet gedetecteerd',
 'Not enough local history yet': 'Nog onvoldoende lokale historie',
 'Not found': 'Niet gevonden',
 'Not recorded in this browser': 'Not recorded in this browser',
 'Not suitable as a GMC device': 'Not suitable as a GMC device',
 'Not suitable for GMC': 'Not suitable for GMC',
 'Not yet checked as a GMC device': 'Not yet checked as a GMC device',
 'Noticeable': 'Opvallend',
 'Noticeable baseline drift': 'Merkbare referentiedrift',
 'Noticeable difference from Poisson-like spread': 'Merkbaar verschil met Poisson-achtige spreiding',
 'Noticeable statistical deviation': 'Merkbare statistische afwijking',
 'Noticeable: above the usual local range': 'Opvallend: boven het gebruikelijke lokale bereik',
 'Number of samples': 'Aantal metingen',
 'Observed': 'Waargenomen',
 'Observed SD / √mean': 'Waargenomen SD / √gemiddelde',
 'Official reference values': 'Officiële referentiewaarden',
 'Offline': 'Offline',
 'Oldest sample': 'Oudste meting',
 'One current weather entity is available': 'Eén actuele weerentiteit is beschikbaar',
 'One-hour mean is {deviation:+.1f}% relative to the learned baseline': 'Het uurgemiddelde ligt {deviation:+.1f}% ten '
                                                                        'opzichte van de aangeleerde basislijn',
 'One-hour means': 'Uurgemiddelden',
 'One-hour robust level is {deviation:+.1f}% relative to the device baseline': 'Het robuuste uurniveau is '
                                                                               '{deviation:+.1f}% ten opzichte van de '
                                                                               'apparaatbaseline',
 'Online': 'Online',
 'Only quality-filtered, one-to-one time-matched measurements are compared. Agreement, correlation, relative bias and stability are evaluated separately so one faulty counter does not automatically define the site result.': 'Alleen '
                                                                                                                                                                                                                                'op '
                                                                                                                                                                                                                                'kwaliteit '
                                                                                                                                                                                                                                'gefilterde, '
                                                                                                                                                                                                                                'één-op-één '
                                                                                                                                                                                                                                'in '
                                                                                                                                                                                                                                'tijd '
                                                                                                                                                                                                                                'gekoppelde '
                                                                                                                                                                                                                                'metingen '
                                                                                                                                                                                                                                'worden '
                                                                                                                                                                                                                                'vergeleken. '
                                                                                                                                                                                                                                'Overeenstemming, '
                                                                                                                                                                                                                                'correlatie, '
                                                                                                                                                                                                                                'relatieve '
                                                                                                                                                                                                                                'afwijking '
                                                                                                                                                                                                                                'en '
                                                                                                                                                                                                                                'stabiliteit '
                                                                                                                                                                                                                                'worden '
                                                                                                                                                                                                                                'afzonderlijk '
                                                                                                                                                                                                                                'beoordeeld, '
                                                                                                                                                                                                                                'zodat '
                                                                                                                                                                                                                                'één '
                                                                                                                                                                                                                                'defecte '
                                                                                                                                                                                                                                'teller '
                                                                                                                                                                                                                                'niet '
                                                                                                                                                                                                                                'automatisch '
                                                                                                                                                                                                                                'het '
                                                                                                                                                                                                                                'locatieresultaat '
                                                                                                                                                                                                                                'bepaalt.',
 'Only the most important conclusions at a glance': 'Alleen de belangrijkste conclusies in één oogopslag',
 'Open': 'Open',
 'Open serial device connections': 'Open serial device connections',
 'Operational events cleared': 'Operational events cleared',
 'Orientation cannot be verified automatically': 'Orientation cannot be verified automatically',
 'Orientation changes detected': 'Orientation changes detected',
 'Orientation data is temporarily unavailable.': 'Oriëntatiegegevens zijn tijdelijk niet beschikbaar.',
 'Orientation qualification': 'Orientation qualification',
 'Orientation stable': 'Orientation stable',
 'Original raw-data CSV': 'Original raw-data CSV',
 'Outliers and invalid measurements': 'Uitschieters en ongeldige metingen',
 'Overview': 'Overzicht',
 'P95 CPM': 'P95-CPM',
 'P95: {value} CPM': 'P95: {value} CPM',
 'P99 CPM': 'P99-CPM',
 'P99: {value} CPM': 'P99: {value} CPM',
 'PDF report': 'PDF-rapport',
 'Pair-level disagreement': 'Afwijking op paarniveau',
 'Pearson r · n={count} paired samples': 'Pearson-r · n={count} gekoppelde metingen',
 'Period: {period} ({timezone})': 'Periode: {period} ({timezone})',
 'Permanently delete all GMC history from this app and Home Assistant Recorder. This includes CPM, temperature, voltage, gyro and tube measurements for every known GMC and all time periods.': 'Permanently '
                                                                                                                                                                                                'delete '
                                                                                                                                                                                                'all '
                                                                                                                                                                                                'GMC '
                                                                                                                                                                                                'history '
                                                                                                                                                                                                'from '
                                                                                                                                                                                                'this '
                                                                                                                                                                                                'app '
                                                                                                                                                                                                'and '
                                                                                                                                                                                                'Home '
                                                                                                                                                                                                'Assistant '
                                                                                                                                                                                                'Recorder. '
                                                                                                                                                                                                'This '
                                                                                                                                                                                                'includes '
                                                                                                                                                                                                'CPM, '
                                                                                                                                                                                                'temperature, '
                                                                                                                                                                                                'voltage, '
                                                                                                                                                                                                'gyro '
                                                                                                                                                                                                'and '
                                                                                                                                                                                                'tube '
                                                                                                                                                                                                'measurements '
                                                                                                                                                                                                'for '
                                                                                                                                                                                                'every '
                                                                                                                                                                                                'known '
                                                                                                                                                                                                'GMC '
                                                                                                                                                                                                'and '
                                                                                                                                                                                                'all '
                                                                                                                                                                                                'time '
                                                                                                                                                                                                'periods.',
 'Persistent level shift detected': 'Persistent level shift detected',
 'Pin card': 'Pin card',
 'Pitch angle': 'Kantelhoek',
 'Plausibilised from two weather entities': 'Gepubliceerd uit twee weerentiteiten',
 'Poisson SD ratio': 'Poisson-SD-verhouding',
 'Poisson SD ratio = observed standard deviation / √mean; a value near 1 indicates Poisson-like spread.': 'Poisson-SD-verhouding '
                                                                                                          '= '
                                                                                                          'waargenomen '
                                                                                                          'standaardafwijking '
                                                                                                          '/ '
                                                                                                          '√gemiddelde; '
                                                                                                          'een waarde '
                                                                                                          'rond 1 '
                                                                                                          'wijst op '
                                                                                                          'Poisson-achtige '
                                                                                                          'spreiding.',
 'Poisson SD ratio formula explanation': 'Poisson-SD-verhouding = waargenomen standaardafwijking / √gemiddelde; een '
                                         'waarde rond 1 wijst op Poisson-achtige spreiding.',
 'Poisson SD ratio: {value}': 'Poisson-SD-verhouding: {value}',
 'Poisson counting interval from the observed impulse count': 'Poisson counting interval from the observed impulse '
                                                              'count',
 'Poisson expectation (λ={mean:.2f})': 'Poisson-verwachting (λ={mean:.2f})',
 'Poor': 'Slecht',
 'Position change log': 'Logboek positiewijzigingen',
 'Possible GMC connection cable': 'Possible GMC connection cable',
 'Possible persistent level shift': 'Possible persistent level shift',
 'Pressure model is still being formed': 'Het drukmodel wordt nog gevormd',
 'Pressure model unavailable': 'Drukmodel niet beschikbaar',
 'Pressure-typical signature is pronounced': 'Duidelijke druktypische signatuur',
 'Preview backup': 'Preview backup',
 'Previous day': 'Vorige dag',
 'Previous week': 'Vorige week',
 'Probable real change': 'Waarschijnlijke echte verandering',
 'Probable shared measurement-site change': 'Waarschijnlijke gezamenlijke verandering op de meetlocatie',
 'Profile': 'Apparaatprofiel',
 'Profile is still being formed': 'Het profiel wordt nog gevormd',
 'Provider': 'Aanbieder',
 'Public GMCMap upload': 'Openbare GMCMap-upload',
 'Quality weight': 'Kwaliteitsgewicht',
 'Quality-filtered correlation': 'Kwaliteitsgefilterde correlatie',
 'Quality-filtered measurement CSV': 'Quality-filtered measurement CSV',
 'Quick downloads': 'Snelle downloads',
 'Radiation 1 h Mean': 'Straling 1-uursgemiddelde',
 'Radiation 1 h Median': 'Straling 1-uursmediaan',
 'Radiation 1 h Standard Deviation': 'Straling 1-uursstandaardafwijking',
 'Radiation Baseline Deviation': 'Afwijking stralingsbasislijn',
 'Radiation CPM': 'Straling CPM',
 'Radiation Rapid Change': 'Snelle stralingsverandering',
 'Radiation count rate [CPM]': 'Stralingstelsnelheid [CPM]',
 'Radiation counts fluctuate naturally. The Fano factor and Poisson spread ratio compare the observed variation with a simple counting-statistics model; they describe distribution shape but not a physical cause or calibration state.': 'Stralingstellingen '
                                                                                                                                                                                                                                           'fluctueren '
                                                                                                                                                                                                                                           'van '
                                                                                                                                                                                                                                           'nature. '
                                                                                                                                                                                                                                           'De '
                                                                                                                                                                                                                                           'Fano-factor '
                                                                                                                                                                                                                                           'en '
                                                                                                                                                                                                                                           'Poisson-spreidingsverhouding '
                                                                                                                                                                                                                                           'vergelijken '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'waargenomen '
                                                                                                                                                                                                                                           'variatie '
                                                                                                                                                                                                                                           'met '
                                                                                                                                                                                                                                           'een '
                                                                                                                                                                                                                                           'eenvoudig '
                                                                                                                                                                                                                                           'telstatistisch '
                                                                                                                                                                                                                                           'model; '
                                                                                                                                                                                                                                           'ze '
                                                                                                                                                                                                                                           'beschrijven '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'vorm '
                                                                                                                                                                                                                                           'van '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'verdeling, '
                                                                                                                                                                                                                                           'maar '
                                                                                                                                                                                                                                           'geen '
                                                                                                                                                                                                                                           'fysieke '
                                                                                                                                                                                                                                           'oorzaak '
                                                                                                                                                                                                                                           'of '
                                                                                                                                                                                                                                           'kalibratiestatus.',
 'Radiation measurement continues unless the device status says otherwise.': 'De stralingsmeting gaat door, tenzij de '
                                                                             'apparaatstatus anders aangeeft.',
 'Radiation measurement continues. An external Home Assistant temperature may be used when configured.': 'De '
                                                                                                         'stralingsmeting '
                                                                                                         'gaat door. '
                                                                                                         'Een externe '
                                                                                                         'Home '
                                                                                                         'Assistant-temperatuur '
                                                                                                         'kan worden '
                                                                                                         'gebruikt '
                                                                                                         'wanneer die '
                                                                                                         'is '
                                                                                                         'geconfigureerd.',
 'Radiation measurement continues; only the optional orientation value is affected.': 'De stralingsmeting gaat door; '
                                                                                      'alleen de optionele '
                                                                                      'oriëntatiewaarde is getroffen.',
 'Radiation monitoring analysis': 'Analyse van stralingsmonitoring',
 'Radiation traffic light': 'Stralingsverkeerslicht',
 'Radiation traffic light hysteresis explanation': 'Het stralingsverkeerslicht gebruikt hysterese: geel vanaf '
                                                   '{yellow_enter:g}% en terug onder {yellow_clear:g}%; rood vanaf '
                                                   '{red_enter:g}% en terug onder {red_clear:g}%.',
 'Radiation traffic light uses hysteresis: it enters yellow at {yellow_enter:g}% and clears below {yellow_clear:g}%; it enters red at {red_enter:g}% and clears below {red_clear:g}%.': 'Het '
                                                                                                                                                                                        'stralingsverkeerslicht '
                                                                                                                                                                                        'gebruikt '
                                                                                                                                                                                        'hysterese: '
                                                                                                                                                                                        'geel '
                                                                                                                                                                                        'vanaf '
                                                                                                                                                                                        '{yellow_enter:g}% '
                                                                                                                                                                                        'en '
                                                                                                                                                                                        'terug '
                                                                                                                                                                                        'onder '
                                                                                                                                                                                        '{yellow_clear:g}%; '
                                                                                                                                                                                        'rood '
                                                                                                                                                                                        'vanaf '
                                                                                                                                                                                        '{red_enter:g}% '
                                                                                                                                                                                        'en '
                                                                                                                                                                                        'terug '
                                                                                                                                                                                        'onder '
                                                                                                                                                                                        '{red_clear:g}%.',
 'Raw CSV': 'Ruwe CSV',
 'Raw device values are stored separately before quality filtering': 'Raw device values are stored separately before '
                                                                     'quality filtering',
 'Raw gyro [signed int16]': 'Ruwe gyro [int16 met teken]',
 'Raw-data archive': 'Raw-data archive',
 'Read-only mode': 'Read-only mode',
 'Ready for new measurements': 'Ready for new measurements',
 'Recent 30 days compared with the preceding 30 days': 'Laatste 30 dagen vergeleken met de voorgaande 30 dagen',
 'Recent data quality is high': 'De kwaliteit van de recente gegevens is hoog',
 'Recent period compared with the preceding period': 'Recente periode vergeleken met de voorgaande periode',
 'Recent quality-filtered data quality is high': 'De kwaliteit van de recente gefilterde gegevens is hoog',
 'Recent reports': 'Recent reports',
 'Recommendation': 'Aanbeveling',
 'Recommended': 'Recommended',
 'Reconnects': 'Herverbindingen',
 'Red': 'Rood',
 'Reduced': 'Verminderd',
 'Refreshing device status…': 'Refreshing device status…',
 'Relative anomaly indicator only; not a safety classification.': 'Alleen een relatieve anomalie-indicator; geen '
                                                                  'veiligheidsclassificatie.',
 'Relative correction factor': 'Relative correction factor',
 'Relative spread': 'Relative spread',
 'Relative to 7 d baseline': 'Ten opzichte van de 7-daagse basislijn',
 'Relative-factor confidence': 'Relative-factor confidence',
 'Remaining deviation': 'Resterende afwijking',
 'Remove': 'Remove',
 'Report': 'Report',
 'Report generation failed': 'Genereren van rapport mislukt',
 'Report target': 'Rapport voor',
 'Reports': 'Reports',
 'Reports for the displayed analysis': 'Reports for the displayed analysis',
 'Rescan devices': 'Rescan devices',
 'Resolve persistent connection gaps before relying on long-term comparisons.': 'Los blijvende '
                                                                                'verbindingsonderbrekingen op voordat '
                                                                                'je op langetermijnvergelijkingen '
                                                                                'vertrouwt.',
 'Restore backup': 'Back-up herstellen',
 'Restore complete': 'Herstel voltooid',
 'Restore confirmation text must be exactly RESTORE': 'De bevestigingstekst moet exact RESTORE zijn',
 'Restore history': 'Geschiedenis herstellen',
 'Restore is disabled by default.': 'Herstel is standaard uitgeschakeld.',
 'Restore upload must be between 1 byte and 128 MiB': 'Het herstelbestand moet tussen 1 byte en 128 MiB groot zijn',
 'Return to GMC Radiation Monitoring': 'Terug naar GMC-stralingsbewaking',
 'Return to GMC Reports': 'Terug naar GMC-rapporten',
 'Review the event export for timing and severity': 'Bekijk de gebeurtenisexport voor tijdstip en ernst',
 'Review the recent trend and event timing. Check both counters and the measurement location if the change persists.': 'Bekijk '
                                                                                                                       'de '
                                                                                                                       'recente '
                                                                                                                       'trend '
                                                                                                                       'en '
                                                                                                                       'het '
                                                                                                                       'tijdstip '
                                                                                                                       'van '
                                                                                                                       'gebeurtenissen. '
                                                                                                                       'Controleer '
                                                                                                                       'beide '
                                                                                                                       'tellers '
                                                                                                                       'en '
                                                                                                                       'de '
                                                                                                                       'meetlocatie '
                                                                                                                       'als '
                                                                                                                       'de '
                                                                                                                       'verandering '
                                                                                                                       'aanhoudt.',
 'Rising': 'Stijgend',
 'Robust medians are used; rejected measurements and isolated spikes do not immediately change the profile.': 'Er '
                                                                                                              'worden '
                                                                                                              'robuuste '
                                                                                                              'medianen '
                                                                                                              'gebruikt; '
                                                                                                              'afgewezen '
                                                                                                              'metingen '
                                                                                                              'en '
                                                                                                              'losse '
                                                                                                              'pieken '
                                                                                                              'veranderen '
                                                                                                              'het '
                                                                                                              'profiel '
                                                                                                              'niet '
                                                                                                              'direct.',
 'Robust one-hour values': 'Robuuste waarden over één uur',
 'Roll angle': 'Rolhoek',
 'Rolling windows end at the latest stored measurement. Dose-rate values are derived from CPM using the configured factor and are not independently measured. CPM remains the primary measurement. The traffic light is a relative background-anomaly indicator, not an emergency, health, or radiation-safety classification.': 'Voortschrijdende '
                                                                                                                                                                                                                                                                                                                                 'vensters '
                                                                                                                                                                                                                                                                                                                                 'eindigen '
                                                                                                                                                                                                                                                                                                                                 'bij '
                                                                                                                                                                                                                                                                                                                                 'de '
                                                                                                                                                                                                                                                                                                                                 'laatst '
                                                                                                                                                                                                                                                                                                                                 'opgeslagen '
                                                                                                                                                                                                                                                                                                                                 'meting. '
                                                                                                                                                                                                                                                                                                                                 'Dosistempo’s '
                                                                                                                                                                                                                                                                                                                                 'worden '
                                                                                                                                                                                                                                                                                                                                 'met '
                                                                                                                                                                                                                                                                                                                                 'de '
                                                                                                                                                                                                                                                                                                                                 'ingestelde '
                                                                                                                                                                                                                                                                                                                                 'factor '
                                                                                                                                                                                                                                                                                                                                 'uit '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'afgeleid '
                                                                                                                                                                                                                                                                                                                                 'en '
                                                                                                                                                                                                                                                                                                                                 'niet '
                                                                                                                                                                                                                                                                                                                                 'onafhankelijk '
                                                                                                                                                                                                                                                                                                                                 'gemeten. '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'blijft '
                                                                                                                                                                                                                                                                                                                                 'de '
                                                                                                                                                                                                                                                                                                                                 'primaire '
                                                                                                                                                                                                                                                                                                                                 'meting. '
                                                                                                                                                                                                                                                                                                                                 'Het '
                                                                                                                                                                                                                                                                                                                                 'verkeerslicht '
                                                                                                                                                                                                                                                                                                                                 'is '
                                                                                                                                                                                                                                                                                                                                 'een '
                                                                                                                                                                                                                                                                                                                                 'relatieve '
                                                                                                                                                                                                                                                                                                                                 'achtergrondanomalie-indicator, '
                                                                                                                                                                                                                                                                                                                                 'geen '
                                                                                                                                                                                                                                                                                                                                 'nood-, '
                                                                                                                                                                                                                                                                                                                                 'gezondheids- '
                                                                                                                                                                                                                                                                                                                                 'of '
                                                                                                                                                                                                                                                                                                                                 'stralingsveiligheidsclassificatie.',
 'SD: {value} CPM': 'SD: {value} CPM',
 'SQLite backup': 'SQLite-back-up',
 'SQLite backup file': 'SQLite backup file',
 'SQLite database vacuum completed': 'SQLite database vacuum completed',
 'Sample standard deviation': 'Steekproefstandaardafwijking',
 'Samples': 'Metingen',
 'Samples: {samples} / {expected}': 'Metingen: {samples} / {expected}',
 'Sampling interval: {interval} s | Samples: {samples}/{expected} | Completeness: {completeness:.2f}% | Generated: {generated} | App {version}': 'Meetinterval: '
                                                                                                                                                 '{interval} '
                                                                                                                                                 's '
                                                                                                                                                 '| '
                                                                                                                                                 'Metingen: '
                                                                                                                                                 '{samples}/{expected} '
                                                                                                                                                 '| '
                                                                                                                                                 'Volledigheid: '
                                                                                                                                                 '{completeness:.2f}% '
                                                                                                                                                 '| '
                                                                                                                                                 'Gegenereerd: '
                                                                                                                                                 '{generated} '
                                                                                                                                                 '| '
                                                                                                                                                 'App '
                                                                                                                                                 '{version}',
 'Sampling interval: {seconds} s': 'Meetinterval: {seconds} s',
 'Sat': 'Za',
 'Saturday': 'Zaterdag',
 'Save a custom report below to reuse it with one tap.': 'Save a custom report below to reuse it with one tap.',
 'Save assignments and restart': 'Save assignments and restart',
 'Save preset': 'Save preset',
 'Saved report presets': 'Saved report presets',
 'Saving changes restarts the add-on so the new serial assignments become active.': 'Saving changes restarts the '
                                                                                    'add-on so the new serial '
                                                                                    'assignments become active.',
 'Scanning and testing suitable unassigned USB ports…': 'Scanning and testing suitable unassigned USB ports…',
 'Schema': 'Schema',
 'Scoped only to known GMC sensor entities': 'Scoped only to known GMC sensor entities',
 'Second half vs first half of available 7 d window': 'Tweede helft vergeleken met de eerste helft van het beschikbare '
                                                      '7-daagse venster',
 'Select a SQLite backup file first.': 'Select a SQLite backup file first.',
 'Select a backup to preview its schema, devices, data period and row counts before restoring.': 'Select a backup to '
                                                                                                 'preview its schema, '
                                                                                                 'devices, data period '
                                                                                                 'and row counts '
                                                                                                 'before restoring.',
 'Select exactly one serial device for every configured GMC': 'Select exactly one serial device for every configured '
                                                              'GMC',
 'Select the GMC-320, the GMC-500+, or a combined report containing both devices.': 'Select the GMC-320, the GMC-500+, '
                                                                                    'or a combined report containing '
                                                                                    'both devices.',
 'Select the physical counter for this configured GMC device.': 'Select the physical counter for this configured GMC '
                                                                'device.',
 'Selected serial device is no longer available': 'Selected serial device is no longer available',
 'Separate original samples in 24 h · {accepted} accepted · {pending} pending': 'Separate original samples in 24 h · '
                                                                                '{accepted} accepted · {pending} '
                                                                                'pending',
 'Serial': 'Serienummer',
 'Serial Errors Since Start': 'Seriële fouten sinds start',
 'Serial Reconnects Since Start': 'Seriële herverbindingen sinds start',
 'Serial USB device': 'Serial USB device',
 'Serial connection recovered': 'Serial connection recovered',
 'Serial device connections': 'Serial device connections',
 'Serial errors / reconnects': 'Seriële fouten / herverbindingen',
 'Serial port': 'Seriële poort',
 'Serial: {serial} | Period: {period} | Timezone: {timezone}': 'Serienummer: {serial} | Periode: {period} | Tijdzone: '
                                                               '{timezone}',
 'Serial: {value}': 'Serienummer: {value}',
 'Severity': 'Ernst',
 'Shared CPM rise': 'Gezamenlijke CPM-stijging',
 'Shared event detector': 'Detector voor gezamenlijke gebeurtenissen',
 'Show analysis': 'Analyse tonen',
 'Show help': 'Show help',
 'Show other serial devices': 'Show other serial devices',
 'Shows live connection state, the latest accepted measurement and warnings for each automatically detected GMC counter.': 'Shows '
                                                                                                                           'live '
                                                                                                                           'connection '
                                                                                                                           'state, '
                                                                                                                           'the '
                                                                                                                           'latest '
                                                                                                                           'accepted '
                                                                                                                           'measurement '
                                                                                                                           'and '
                                                                                                                           'warnings '
                                                                                                                           'for '
                                                                                                                           'each '
                                                                                                                           'automatically '
                                                                                                                           'detected '
                                                                                                                           'GMC '
                                                                                                                           'counter.',
 'Simple': 'Eenvoudig',
 'Since app start': 'Sinds het starten van de app',
 'Slightly noticeable': 'Licht opvallend',
 'Slightly tilted': 'Slightly tilted',
 'Small baseline drift': 'Kleine referentiedrift',
 'Smart Alert State': 'Status slimme waarschuwing',
 'Smoothed historical background trend': 'Afgevlakte historische achtergrondtrend',
 'Source validation': 'Broncontrole',
 'Specific ISO week': 'Specifieke ISO-week',
 'Specific date': 'Specifieke datum',
 'Spread above the Poisson expectation can be caused by environmental changes, device instability or changing interference; the metric does not identify which cause applies.': 'Spread '
                                                                                                                                                                                'above '
                                                                                                                                                                                'the '
                                                                                                                                                                                'Poisson '
                                                                                                                                                                                'expectation '
                                                                                                                                                                                'can '
                                                                                                                                                                                'be '
                                                                                                                                                                                'caused '
                                                                                                                                                                                'by '
                                                                                                                                                                                'environmental '
                                                                                                                                                                                'changes, '
                                                                                                                                                                                'device '
                                                                                                                                                                                'instability '
                                                                                                                                                                                'or '
                                                                                                                                                                                'changing '
                                                                                                                                                                                'interference; '
                                                                                                                                                                                'the '
                                                                                                                                                                                'metric '
                                                                                                                                                                                'does '
                                                                                                                                                                                'not '
                                                                                                                                                                                'identify '
                                                                                                                                                                                'which '
                                                                                                                                                                                'cause '
                                                                                                                                                                                'applies.',
 'Stability and device health': 'Stabiliteit en apparaatstatus',
 'Stable': 'Stabiel',
 'Stable device path': 'Stable device path',
 'Stable devices': 'Stabiele apparaten',
 'Standard deviation CPM': 'Standaardafwijking CPM',
 'Start time UTC': 'Starttijd UTC',
 'Start time local': 'Lokale starttijd',
 'Start with a readable PDF or a complete ZIP bundle. Raw and specialist formats remain available below without crowding the main view.': 'Begin '
                                                                                                                                          'met '
                                                                                                                                          'een '
                                                                                                                                          'leesbare '
                                                                                                                                          'PDF '
                                                                                                                                          'of '
                                                                                                                                          'een '
                                                                                                                                          'compleet '
                                                                                                                                          'ZIP-pakket. '
                                                                                                                                          'Ruwe '
                                                                                                                                          'en '
                                                                                                                                          'specialistische '
                                                                                                                                          'formaten '
                                                                                                                                          'blijven '
                                                                                                                                          'hieronder '
                                                                                                                                          'beschikbaar '
                                                                                                                                          'zonder '
                                                                                                                                          'de '
                                                                                                                                          'hoofdweergave '
                                                                                                                                          'te '
                                                                                                                                          'overladen.',
 'Statistical indication only': 'Alleen statistische aanwijzing',
 'Statistical level shift': 'Statistical level shift',
 'Statistically noticeable': 'Statistisch opvallend',
 'Statistics': 'Statistiek',
 'Stored samples': 'Opgeslagen metingen',
 'Stored samples across all devices': 'Opgeslagen metingen van alle apparaten',
 'Stored samples for this device': 'Opgeslagen metingen voor dit apparaat',
 'Strong common signal': 'Sterk gezamenlijk signaal',
 'Strong linear relationship': 'Sterke lineaire relatie',
 'Strong statistical deviation': 'Sterke statistische afwijking',
 'Successful uploads': 'Geslaagde uploads',
 'Successful uploads since start': 'Geslaagde uploads sinds start',
 'Suitable for most trend analysis': 'Geschikt voor de meeste trendanalyses',
 'Summary': 'Samenvatting',
 'Sun': 'Zo',
 'Sunday': 'Zondag',
 'Supervisor API access is unavailable': 'Supervisor API access is unavailable',
 'Supply voltage [V]': 'Voedingsspanning [V]',
 'Suspicious CPM value is being verified': 'Suspicious CPM value is being verified',
 'Sustained Radiation Alert': 'Aanhoudende stralingswaarschuwing',
 'Sustained relative anomaly events': 'Aanhoudende relatieve anomaliegebeurtenissen',
 'Sustained yellow/red relative anomaly events': 'Aanhoudende gele/rode relatieve anomaliegebeurtenissen',
 'Temperature': 'Temperatuur',
 'Temperature / voltage errors': 'Temperatuur- / spanningsfouten',
 'Temperature Errors Since Start': 'Temperatuurfouten sinds start',
 'Temperature [°C]': 'Temperatuur [°C]',
 'Temperature and voltage relationships': 'Relaties met temperatuur en spanning',
 'Temperature bins (24 h)': 'Temperatuurklassen (24 u)',
 'Temperature correlation': 'Temperatuurcorrelatie',
 'Temperature profile is still being formed': 'Het temperatuurprofiel wordt nog gevormd',
 'Temperature trend': 'Temperatuurtrend',
 'Temperature-specific background': 'Temperatuurspecifieke achtergrond',
 'The Supervisor options could not be loaded: {error}': 'The Supervisor options could not be loaded: {error}',
 'The absolute assessment starts after the first measurement.': 'De absolute beoordeling start na de eerste meting.',
 'The absolute level is below the configured warning threshold, but the value is far above the learned local background.': 'Het '
                                                                                                                           'absolute '
                                                                                                                           'niveau '
                                                                                                                           'ligt '
                                                                                                                           'onder '
                                                                                                                           'de '
                                                                                                                           'ingestelde '
                                                                                                                           'waarschuwingsdrempel, '
                                                                                                                           'maar '
                                                                                                                           'de '
                                                                                                                           'waarde '
                                                                                                                           'ligt '
                                                                                                                           'ver '
                                                                                                                           'boven '
                                                                                                                           'de '
                                                                                                                           'aangeleerde '
                                                                                                                           'lokale '
                                                                                                                           'achtergrond.',
 'The absolute level is currently uncritical, but the local comparison or short-term trend deserves continued observation.': 'Het '
                                                                                                                             'absolute '
                                                                                                                             'niveau '
                                                                                                                             'is '
                                                                                                                             'momenteel '
                                                                                                                             'niet '
                                                                                                                             'kritisch, '
                                                                                                                             'maar '
                                                                                                                             'de '
                                                                                                                             'lokale '
                                                                                                                             'vergelijking '
                                                                                                                             'of '
                                                                                                                             'kortetermijntrend '
                                                                                                                             'verdient '
                                                                                                                             'verdere '
                                                                                                                             'observatie.',
 'The absolute level is currently uncritical. More local history is required before anomaly detection becomes reliable.': 'Het '
                                                                                                                          'absolute '
                                                                                                                          'niveau '
                                                                                                                          'is '
                                                                                                                          'momenteel '
                                                                                                                          'niet '
                                                                                                                          'kritisch. '
                                                                                                                          'Er '
                                                                                                                          'is '
                                                                                                                          'meer '
                                                                                                                          'lokale '
                                                                                                                          'historie '
                                                                                                                          'nodig '
                                                                                                                          'voordat '
                                                                                                                          'anomaliedetectie '
                                                                                                                          'betrouwbaar '
                                                                                                                          'wordt.',
 'The add-on is restarting so the new serial assignments become active.': 'The add-on is restarting so the new serial '
                                                                          'assignments become active.',
 'The app combines the recent trend, robust statistics, agreement between connected counters and the learned local background. The result is a statistical aid and does not identify a physical cause.': 'De '
                                                                                                                                                                                                         'app '
                                                                                                                                                                                                         'combineert '
                                                                                                                                                                                                         'de '
                                                                                                                                                                                                         'recente '
                                                                                                                                                                                                         'trend, '
                                                                                                                                                                                                         'robuuste '
                                                                                                                                                                                                         'statistiek, '
                                                                                                                                                                                                         'overeenstemming '
                                                                                                                                                                                                         'tussen '
                                                                                                                                                                                                         'aangesloten '
                                                                                                                                                                                                         'tellers '
                                                                                                                                                                                                         'en '
                                                                                                                                                                                                         'de '
                                                                                                                                                                                                         'aangeleerde '
                                                                                                                                                                                                         'lokale '
                                                                                                                                                                                                         'achtergrond. '
                                                                                                                                                                                                         'Het '
                                                                                                                                                                                                         'resultaat '
                                                                                                                                                                                                         'is '
                                                                                                                                                                                                         'een '
                                                                                                                                                                                                         'statistisch '
                                                                                                                                                                                                         'hulpmiddel '
                                                                                                                                                                                                         'en '
                                                                                                                                                                                                         'bepaalt '
                                                                                                                                                                                                         'geen '
                                                                                                                                                                                                         'fysieke '
                                                                                                                                                                                                         'oorzaak.',
 'The app compares quality-filtered measurements from the same weekday and hour. Robust medians reduce the influence of isolated spikes and regular daily patterns are kept separate from unusual changes.': 'De '
                                                                                                                                                                                                             'app '
                                                                                                                                                                                                             'vergelijkt '
                                                                                                                                                                                                             'op '
                                                                                                                                                                                                             'kwaliteit '
                                                                                                                                                                                                             'gefilterde '
                                                                                                                                                                                                             'metingen '
                                                                                                                                                                                                             'van '
                                                                                                                                                                                                             'dezelfde '
                                                                                                                                                                                                             'weekdag '
                                                                                                                                                                                                             'en '
                                                                                                                                                                                                             'hetzelfde '
                                                                                                                                                                                                             'uur. '
                                                                                                                                                                                                             'Robuuste '
                                                                                                                                                                                                             'medianen '
                                                                                                                                                                                                             'verminderen '
                                                                                                                                                                                                             'de '
                                                                                                                                                                                                             'invloed '
                                                                                                                                                                                                             'van '
                                                                                                                                                                                                             'losse '
                                                                                                                                                                                                             'pieken '
                                                                                                                                                                                                             'en '
                                                                                                                                                                                                             'normale '
                                                                                                                                                                                                             'dagelijkse '
                                                                                                                                                                                                             'patronen '
                                                                                                                                                                                                             'blijven '
                                                                                                                                                                                                             'gescheiden '
                                                                                                                                                                                                             'van '
                                                                                                                                                                                                             'ongebruikelijke '
                                                                                                                                                                                                             'veranderingen.',
 'The app compares quality-filtered radiation measurements with available air-pressure data. A statistical relationship can support interpretation, but correlation alone does not prove a cosmic or environmental cause.': 'De '
                                                                                                                                                                                                                            'app '
                                                                                                                                                                                                                            'vergelijkt '
                                                                                                                                                                                                                            'op '
                                                                                                                                                                                                                            'kwaliteit '
                                                                                                                                                                                                                            'gefilterde '
                                                                                                                                                                                                                            'stralingsmetingen '
                                                                                                                                                                                                                            'met '
                                                                                                                                                                                                                            'beschikbare '
                                                                                                                                                                                                                            'luchtdrukgegevens. '
                                                                                                                                                                                                                            'Een '
                                                                                                                                                                                                                            'statistische '
                                                                                                                                                                                                                            'relatie '
                                                                                                                                                                                                                            'kan '
                                                                                                                                                                                                                            'de '
                                                                                                                                                                                                                            'interpretatie '
                                                                                                                                                                                                                            'ondersteunen, '
                                                                                                                                                                                                                            'maar '
                                                                                                                                                                                                                            'correlatie '
                                                                                                                                                                                                                            'alleen '
                                                                                                                                                                                                                            'bewijst '
                                                                                                                                                                                                                            'geen '
                                                                                                                                                                                                                            'kosmische '
                                                                                                                                                                                                                            'of '
                                                                                                                                                                                                                            'omgevingsgerelateerde '
                                                                                                                                                                                                                            'oorzaak.',
 'The comparison uses only quality-filtered, one-to-one paired measurements.': 'De vergelijking gebruikt uitsluitend '
                                                                               'kwaliteitsgefilterde, één-op-één '
                                                                               'gekoppelde metingen.',
 'The configured danger threshold is exceeded.': 'De ingestelde gevarendrempel is overschreden.',
 'The connected counters currently agree well': 'De aangesloten tellers komen momenteel goed overeen',
 'The counters disagree, so a device-specific effect is more likely': 'De tellers wijken af; een apparaatspecifiek '
                                                                      'effect is daarom waarschijnlijker',
 'The current radiation level is uncritical according to the selected thresholds.': 'Het huidige stralingsniveau is '
                                                                                    'volgens de gekozen drempels niet '
                                                                                    'kritisch.',
 'The current value is below the configured warning threshold and within the usual local range.': 'De huidige waarde '
                                                                                                  'ligt onder de '
                                                                                                  'ingestelde '
                                                                                                  'waarschuwingsdrempel '
                                                                                                  'en binnen het '
                                                                                                  'gebruikelijke '
                                                                                                  'lokale bereik.',
 'The current value is within the configured warning range.': 'De huidige waarde ligt binnen het ingestelde '
                                                              'waarschuwingsbereik.',
 'The deviation is device-specific; the measurement-site profile remains normal': 'De afwijking is apparaatspecifiek; '
                                                                                  'het meetlocatieprofiel blijft '
                                                                                  'normaal',
 'The device baseline is available, but there are not enough recent measurements for a current comparison.': 'De '
                                                                                                             'apparaatreferentie '
                                                                                                             'is '
                                                                                                             'beschikbaar, '
                                                                                                             'maar er '
                                                                                                             'zijn nog '
                                                                                                             'niet '
                                                                                                             'genoeg '
                                                                                                             'recente '
                                                                                                             'metingen '
                                                                                                             'voor een '
                                                                                                             'actuele '
                                                                                                             'vergelijking.',
 'The device clock differs from Home Assistant time.': 'The device clock differs from Home Assistant time.',
 'The filtered counters disagree, so a device-specific effect is more likely': 'De gefilterde tellers wijken af; een '
                                                                               'apparaatspecifiek effect is '
                                                                               'waarschijnlijker',
 'The learned baseline remains available. More current samples are required before the local comparison can be updated.': 'De '
                                                                                                                          'geleerde '
                                                                                                                          'referentie '
                                                                                                                          'blijft '
                                                                                                                          'beschikbaar. '
                                                                                                                          'Er '
                                                                                                                          'zijn '
                                                                                                                          'meer '
                                                                                                                          'actuele '
                                                                                                                          'metingen '
                                                                                                                          'nodig '
                                                                                                                          'om '
                                                                                                                          'de '
                                                                                                                          'lokale '
                                                                                                                          'vergelijking '
                                                                                                                          'bij '
                                                                                                                          'te '
                                                                                                                          'werken.',
 'The level-shift detector looks for persistent statistical changes and does not alter radiation warnings.': 'The '
                                                                                                             'level-shift '
                                                                                                             'detector '
                                                                                                             'looks '
                                                                                                             'for '
                                                                                                             'persistent '
                                                                                                             'statistical '
                                                                                                             'changes '
                                                                                                             'and does '
                                                                                                             'not '
                                                                                                             'alter '
                                                                                                             'radiation '
                                                                                                             'warnings.',
 'The local background is still being learned, so no anomaly assessment is available yet.': 'De lokale achtergrond '
                                                                                            'wordt nog geleerd; er is '
                                                                                            'daarom nog geen '
                                                                                            'anomaliebeoordeling '
                                                                                            'beschikbaar.',
 'The measurement-site baseline is {deviation:+.1f}% above its typical value': 'De baseline van de meetlocatie ligt '
                                                                               '{deviation:+.1f}% boven de typische '
                                                                               'waarde',
 'The measurement-site profile combines both devices with quality weighting': 'Het meetlocatieprofiel combineert beide '
                                                                              'apparaten met kwaliteitsweging',
 'The measurement-site profile currently relies on one device': 'Het meetlocatieprofiel is momenteel gebaseerd op één '
                                                                'apparaat',
 'The pressure model cannot prove cosmic radiation and never suppresses radiation warnings.': 'Het drukmodel kan '
                                                                                              'kosmische straling niet '
                                                                                              'bewijzen en onderdrukt '
                                                                                              'nooit '
                                                                                              'stralingswaarschuwingen.',
 'The quality-filtered counter comparison currently agrees well': 'De kwaliteitsgefilterde tellervergelijking komt '
                                                                  'momenteel goed overeen',
 'The recent 30-minute robust trend is rising': 'De robuuste trend van de afgelopen 30 minuten stijgt',
 'The recent 30-minute trend is rising': 'De recente trend van 30 minuten stijgt',
 'The request could not be processed. Check the selected options.': 'De aanvraag kon niet worden verwerkt. Controleer '
                                                                    'de geselecteerde opties.',
 'The score combines time-window coverage, missing or irregular intervals, duplicate timestamps and optional-sensor coverage. It indicates how strongly the analysis can rely on the stored series.': 'De '
                                                                                                                                                                                                      'score '
                                                                                                                                                                                                      'combineert '
                                                                                                                                                                                                      'dekking '
                                                                                                                                                                                                      'van '
                                                                                                                                                                                                      'het '
                                                                                                                                                                                                      'tijdvenster, '
                                                                                                                                                                                                      'ontbrekende '
                                                                                                                                                                                                      'of '
                                                                                                                                                                                                      'onregelmatige '
                                                                                                                                                                                                      'intervallen, '
                                                                                                                                                                                                      'dubbele '
                                                                                                                                                                                                      'tijdstempels '
                                                                                                                                                                                                      'en '
                                                                                                                                                                                                      'dekking '
                                                                                                                                                                                                      'van '
                                                                                                                                                                                                      'optionele '
                                                                                                                                                                                                      'sensoren. '
                                                                                                                                                                                                      'Hij '
                                                                                                                                                                                                      'geeft '
                                                                                                                                                                                                      'aan '
                                                                                                                                                                                                      'hoe '
                                                                                                                                                                                                      'sterk '
                                                                                                                                                                                                      'de '
                                                                                                                                                                                                      'analyse '
                                                                                                                                                                                                      'op '
                                                                                                                                                                                                      'de '
                                                                                                                                                                                                      'opgeslagen '
                                                                                                                                                                                                      'reeks '
                                                                                                                                                                                                      'kan '
                                                                                                                                                                                                      'vertrouwen.',
 'The serial connection is unstable.': 'De seriële verbinding is instabiel.',
 'The traffic light and events are relative anomaly indicators, not safety classifications.': 'Het verkeerslicht en de '
                                                                                              'gebeurtenissen zijn '
                                                                                              'relatieve '
                                                                                              'anomalie-indicatoren, '
                                                                                              'geen '
                                                                                              'veiligheidsclassificaties.',
 'The value is also within the usual range for this location.': 'De waarde ligt ook binnen het gebruikelijke bereik '
                                                                'voor deze locatie.',
 'The values most users need first': 'De waarden die de meeste gebruikers het eerst nodig hebben',
 'These are statistical changes. They can indicate a location, geometry or environmental change, but do not identify the cause.': 'Dit '
                                                                                                                                  'zijn '
                                                                                                                                  'statistische '
                                                                                                                                  'veranderingen. '
                                                                                                                                  'Ze '
                                                                                                                                  'kunnen '
                                                                                                                                  'wijzen '
                                                                                                                                  'op '
                                                                                                                                  'een '
                                                                                                                                  'verandering '
                                                                                                                                  'van '
                                                                                                                                  'locatie, '
                                                                                                                                  'geometrie '
                                                                                                                                  'of '
                                                                                                                                  'omgeving, '
                                                                                                                                  'maar '
                                                                                                                                  'bepalen '
                                                                                                                                  'de '
                                                                                                                                  'oorzaak '
                                                                                                                                  'niet.',
 'These values describe the shape of the count distribution. They do not by themselves prove a physical cause or a calibration state.': 'Deze '
                                                                                                                                        'waarden '
                                                                                                                                        'beschrijven '
                                                                                                                                        'de '
                                                                                                                                        'vorm '
                                                                                                                                        'van '
                                                                                                                                        'de '
                                                                                                                                        'telverdeling. '
                                                                                                                                        'Op '
                                                                                                                                        'zichzelf '
                                                                                                                                        'bewijzen '
                                                                                                                                        'ze '
                                                                                                                                        'geen '
                                                                                                                                        'fysieke '
                                                                                                                                        'oorzaak '
                                                                                                                                        'of '
                                                                                                                                        'kalibratiestatus.',
 'This analysis detects unusual changes compared with the normal background at this location. It is not a danger classification; an unusual value can still be below the absolute warning threshold.': 'Deze '
                                                                                                                                                                                                       'analyse '
                                                                                                                                                                                                       'detecteert '
                                                                                                                                                                                                       'ongebruikelijke '
                                                                                                                                                                                                       'veranderingen '
                                                                                                                                                                                                       'ten '
                                                                                                                                                                                                       'opzichte '
                                                                                                                                                                                                       'van '
                                                                                                                                                                                                       'de '
                                                                                                                                                                                                       'normale '
                                                                                                                                                                                                       'achtergrond '
                                                                                                                                                                                                       'op '
                                                                                                                                                                                                       'deze '
                                                                                                                                                                                                       'locatie. '
                                                                                                                                                                                                       'Het '
                                                                                                                                                                                                       'is '
                                                                                                                                                                                                       'geen '
                                                                                                                                                                                                       'gevarenclassificatie; '
                                                                                                                                                                                                       'een '
                                                                                                                                                                                                       'opvallende '
                                                                                                                                                                                                       'waarde '
                                                                                                                                                                                                       'kan '
                                                                                                                                                                                                       'nog '
                                                                                                                                                                                                       'steeds '
                                                                                                                                                                                                       'onder '
                                                                                                                                                                                                       'de '
                                                                                                                                                                                                       'absolute '
                                                                                                                                                                                                       'waarschuwingsdrempel '
                                                                                                                                                                                                       'liggen.',
 'This cannot be undone. Delete all GMC history?': 'This cannot be undone. Delete all GMC history?',
 'This classification only compares the current measurement with the selected thresholds. It does not compare the value with the usual background at this location.': 'Deze '
                                                                                                                                                                      'classificatie '
                                                                                                                                                                      'vergelijkt '
                                                                                                                                                                      'alleen '
                                                                                                                                                                      'de '
                                                                                                                                                                      'huidige '
                                                                                                                                                                      'meting '
                                                                                                                                                                      'met '
                                                                                                                                                                      'de '
                                                                                                                                                                      'gekozen '
                                                                                                                                                                      'drempels. '
                                                                                                                                                                      'Zij '
                                                                                                                                                                      'vergelijkt '
                                                                                                                                                                      'de '
                                                                                                                                                                      'waarde '
                                                                                                                                                                      'niet '
                                                                                                                                                                      'met '
                                                                                                                                                                      'de '
                                                                                                                                                                      'gebruikelijke '
                                                                                                                                                                      'achtergrond '
                                                                                                                                                                      'op '
                                                                                                                                                                      'deze '
                                                                                                                                                                      'locatie.',
 'This factor is only a relative device comparison and is not an absolute radiation calibration.': 'This factor is '
                                                                                                   'only a relative '
                                                                                                   'device comparison '
                                                                                                   'and is not an '
                                                                                                   'absolute radiation '
                                                                                                   'calibration.',
 'This report is descriptive and is not a radiation-safety classification.': 'Dit rapport is beschrijvend en vormt '
                                                                             'geen stralingsveiligheidsclassificatie.',
 'Thresholds can be changed in the add-on configuration.': 'Drempels kunnen in de add-onconfiguratie worden aangepast.',
 'Thu': 'Do',
 'Thursday': 'Donderdag',
 'Tilted': 'Tilted',
 'Time series': 'Tijdreeks',
 'Time series, Poisson comparison and weekday/hour heatmap': 'Tijdreeks, Poisson-vergelijking en weekdag/uur-heatmap',
 'Time-series PNG': 'Tijdreeks-PNG',
 'Timestamp diagnostics': 'Tijdstempeldiagnose',
 'Timezone': 'Tijdzone',
 'Today so far bundle': 'Pakket van vandaag tot nu toe',
 'Too few pressure/CPM pairs': 'Te weinig druk/CPM-paren',
 'Too few valid paired measurements for a reliable device comparison': 'Te weinig geldige meetparen voor een '
                                                                       'betrouwbare vergelijking',
 'Too little or too fragmented for strong conclusions': 'Te weinig of te versnipperde gegevens voor sterke conclusies',
 'Trend (30 min)': 'Trend (30 min)',
 'Tue': 'Di',
 'Tuesday': 'Dinsdag',
 'Type DELETE ALL GMC HISTORY to confirm': 'Type DELETE ALL GMC HISTORY to confirm',
 'Type RESTORE to confirm': 'Typ RESTORE ter bevestiging',
 'Typical for {weekday} at {hour}:00': 'Typisch voor {weekday} om {hour}:00',
 'USB down': 'Rechtop, USB onder',
 'USB left': 'Rechtop, USB links',
 'USB right': 'Rechtop, USB rechts',
 'USB up': 'Rechtop, USB boven',
 'UTC timestamp': 'UTC-tijdstempel',
 'Unavailable': 'Niet beschikbaar',
 'Unconfirmed values since bridge start': 'Unconfirmed values since bridge start',
 'Uncritical': 'Niet kritisch',
 'Uncritical: below warning threshold': 'Niet kritisch: onder de waarschuwingsdrempel',
 'Unknown': 'Onbekend',
 'Unknown GMC': 'Onbekend GMC-apparaat',
 'Unknown report device': 'Onbekend rapportapparaat',
 'Unknown serial device': 'Unknown serial device',
 'Unstable': 'Instabiel',
 'Unsupported report format': 'Niet-ondersteund rapportformaat',
 'Upload errors': 'Uploadfouten',
 'Upload errors since start': 'Uploadfouten sinds start',
 'Upload failed': 'Upload mislukt',
 'Upload successful': 'Upload geslaagd',
 'Uploading': 'Bezig met uploaden',
 'Upright': 'Upright',
 'Use this as context only and review longer periods before drawing conclusions.': 'Gebruik dit alleen als context en '
                                                                                   'bekijk langere perioden voordat je '
                                                                                   'conclusies trekt.',
 'Valid measurements': 'Geldige metingen',
 'Variance / mean': 'Variantie / gemiddelde',
 'Very close to Poisson-like spread': 'Zeer dicht bij Poisson-achtige spreiding',
 'Very complete 24 h data window': 'Zeer volledig 24-uurs gegevensvenster',
 'Very strong linear relationship': 'Zeer sterke lineaire relatie',
 'Very weak linear relationship': 'Zeer zwakke lineaire relatie',
 'Voltage': 'Spanning',
 'Voltage Errors Since Start': 'Spanningsfouten sinds start',
 'Voltage [V]': 'Spanning [V]',
 'Voltage correlation': 'Spanningscorrelatie',
 'Waiting for enough recent measurements': 'Wachten op voldoende recente metingen',
 'Waiting for first upload': 'Wachten op eerste upload',
 'Waiting for recent measurements': 'Wachten op recente metingen',
 'Waiting for the first accepted measurement': 'Waiting for the first accepted measurement',
 'Warning': 'Waarschuwing',
 'Warning from {warning} s; critical from {critical} s': 'Waarschuwing vanaf {warning} s; kritiek vanaf {critical} s',
 'Warning threshold exceeded': 'Waarschuwingsdrempel overschreden',
 'Warning thresholds': 'Waarschuwingsdrempels',
 'Weak linear relationship': 'Zwakke lineaire relatie',
 'Weather pressure sources disagree': 'De luchtdrukbronnen spreken elkaar tegen',
 'Wed': 'Wo',
 'Wednesday': 'Woensdag',
 'Weekday': 'Weekdag',
 'Weekday/hour heatmap': 'Heatmap weekdag/uur',
 'What does the historical trend mean?': 'Wat betekent de historische trend?',
 'What each report preserves and how periods are defined': 'Wat elk rapport bewaart en hoe perioden zijn gedefinieerd',
 'What should I do?': 'Wat moet ik doen?',
 'What this assessment means': 'Betekenis van deze beoordeling',
 'Why are Poisson values shown?': 'Waarom worden Poisson-waarden getoond?',
 'Why is this assessment shown?': 'Waarom wordt deze beoordeling getoond?',
 'Within local background range': 'Binnen lokaal achtergrondniveau',
 'Within normal statistical variation': 'Binnen normale statistische variatie',
 'Within the usual local range': 'Binnen het gebruikelijke lokale bereik',
 'Within warning range': 'Binnen het waarschuwingsbereik',
 'Yellow': 'Geel',
 'Z-score = (latest CPM − 24 h mean) / 24 h standard deviation.': 'Z-score = (laatste CPM − 24-uursgemiddelde) / '
                                                                  '24-uursstandaardafwijking.',
 'Z-score formula explanation': 'Z-score = (laatste CPM − 24-uursgemiddelde) / 24-uursstandaardafwijking.',
 'complete and regularly spaced data': 'volledige en regelmatig verdeelde gegevens',
 'confirmations': 'confirmations',
 'counting uncertainty {value:.2f}%': 'counting uncertainty {value:.2f}%',
 'coverage': 'dekking',
 'daily values': 'dagwaarden',
 'days': 'dagen',
 'duplicates / clock regressions': 'duplicaten / klokterugloop',
 'entity patterns': 'entity patterns',
 'errors': 'errors',
 'estimated signal probability': 'geschatte signaalkans',
 'excluded measurements': 'uitgesloten metingen',
 'longest gap {value} s': 'langste onderbreking {value} s',
 'measurements': 'measurements',
 'minimum sample coverage': 'minimale meetdekking',
 'n={count} paired samples': 'n={count} gekoppelde metingen',
 'n={count} · {coverage:.1f}% coverage': 'n={count} · dekking {coverage:.1f}%',
 'paired samples': 'meetparen',
 'reconnects': 'reconnects',
 'relative to baseline': 'ten opzichte van de basislijn',
 'score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s': 'score {score:.1f}/100 · dekking '
                                                                           '{coverage:.1f}% · langste onderbreking '
                                                                           '{gap} s',
 'short / long intervals': 'korte / lange intervallen',
 'since the current bridge start': 'since the current bridge start',
 'temperature coverage {value}%': 'temperatuurdekking {value}%',
 'unknown': 'onbekend',
 'valid hourly values': 'geldige uurwaarden',
 'valid paired samples': 'geldige meetparen',
 'voltage coverage {value}%': 'spanningsdekking {value}%',
 'write errors since app start': 'write errors since app start',
 '{before:.2f} → {after:.2f} CPM · {sigma:.1f}σ · {hours} h persistent': '{before:.2f} → {after:.2f} CPM · '
                                                                         '{sigma:.1f}σ · {hours} h persistent',
 '{check_type} result cached for {seconds} s · schema v{schema}': 'Resultaat van {check_type} {seconds} s in cache · '
                                                                  'schema v{schema}',
 '{connected} connected · {disconnected} disconnected': '{connected} connected · {disconnected} disconnected',
 '{count} implausible measurements were excluded from the assessment': '{count} onwaarschijnlijke metingen zijn '
                                                                       'uitgesloten van de beoordeling',
 '{count} measurements': '{count} metingen',
 '{count} measurements and {events} events were removed.': '{count} measurements and {events} events were removed.',
 '{events} events · {diagnostics} diagnostics': '{events} events · {diagnostics} diagnostics',
 '{gyro_note} History retention: {days} days. Daily periods are local calendar days; weekly periods are ISO weeks from Monday through Sunday.': '{gyro_note} '
                                                                                                                                                'Bewaartermijn '
                                                                                                                                                'historie: '
                                                                                                                                                '{days} '
                                                                                                                                                'dagen. '
                                                                                                                                                'Dagperioden '
                                                                                                                                                'zijn '
                                                                                                                                                'lokale '
                                                                                                                                                'kalenderdagen; '
                                                                                                                                                'weekperioden '
                                                                                                                                                'zijn '
                                                                                                                                                'ISO-weken '
                                                                                                                                                'van '
                                                                                                                                                'maandag '
                                                                                                                                                'tot '
                                                                                                                                                'en '
                                                                                                                                                'met '
                                                                                                                                                'zondag.',
 '{model} — Radiation monitoring report': '{model} — Stralingsmonitoringsrapport',
 '{seconds} seconds ago': '{seconds} seconds ago',
 '{value:g} h': '{value:g} h',
 '{value:g} min': '{value:g} min',
 '{value} clock regressions observed': '{value} klokteruglopen waargenomen',
 '{value} duplicate timestamps observed': '{value} dubbele tijdstempels waargenomen',
 '{value} long intervals': '{value} lange intervallen',
 '{value} unusually short intervals': '{value} ongewoon korte intervallen',
 '{value} vs local baseline': '{value} ten opzichte van lokale basislijn',
 '{value}% time-window coverage': '{value}% tijdvensterdekking'}

# Runtime presentation templates added in 7.1.4.
CATALOG.update({
    'Comparison confidence: {confidence}': 'Betrouwbaarheid van vergelijking: {confidence}',
    'Confidence: {confidence}': 'Betrouwbaarheid: {confidence}',
    'Status': 'Status',
    'Typical background': 'Typische achtergrond',
    'Valid paired samples': 'Geldige meetparen',
    'Warning from {warning:g} s; critical from {critical:g} s': 'Waarschuwing vanaf {warning:g} s; kritiek vanaf {critical:g} s',
    'valid hourly values · {days:.1f} days · {span:.1f} hPa': 'geldige uurwaarden · {days:.1f} dagen · {span:.1f} hPa',
    '{a:+.1f}% / {b:+.1f}%': '{a:+.1f}% / {b:+.1f}%',
    '{b} × factor → {a}': '{b} × factor → {a}',
    '{content}': '{content}',
    '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)': '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)',
    '{days} days': '{days} dagen',
    '{dose:.3f} µSv/h': '{dose:.3f} µSv/h',
    '{first} {second}': '{first} {second}',
    '{from_value} → {to_value}': '{from_value} → {to_value}',
    '{note} · n={samples}': '{note} · n={samples}',
    '{pairs} valid paired samples': '{pairs} geldige meetparen',
    '{pairs} valid paired samples · counting uncertainty {value:.2f}%': '{pairs} geldige meetparen · telonzekerheid {value:.2f}%',
    '{probability:.0f}% estimated signal probability': '{probability:.0f} % geschatte signaalkans',
    '{span:.0f} {days_label} · {count} {daily_label}': '{span:.0f} {days_label} · {count} {daily_label}',
    '{start}–{end} °C · {samples} Samples': '{start}–{end} °C · {samples} metingen',
    '{trend:+.1f} CPM': '{trend:+.1f} CPM',
    '{value:g} µSv/h': '{value:g} µSv/h',
    'Last uploaded CPM': 'Laatst verzonden CPM',
    'Last uploaded ACPM': 'Laatst verzonden ACPM',
    'GMCMap last uploaded ACPM': 'Laatst naar GMCMap verzonden ACPM',
    'GMCMap ACPM accepted samples': 'Geaccepteerde metingen voor GMCMap-ACPM',
    'ACPM is the average of all accepted CPM readings since the current app measurement session began.': 'ACPM is het gemiddelde van alle geaccepteerde CPM-metingen sinds het begin van de huidige meetsessie van de app.',
    'User manual': 'Gebruikershandleiding',
    'Open user manual PDF': 'Gebruikershandleiding als PDF openen',
    'User manual is not available': 'De gebruikershandleiding is niet beschikbaar',
})

# Version 8.2.1 report and history labels.
CATALOG.update({
    'Accepted measurements [count]': 'Geaccepteerde metingen [aantal]',
    'Local hour [h]': 'Lokaal uur [u]',
    'Mean count rate [CPM]': 'Gemiddelde telsnelheid [CPM]',
    'Radiation Monitoring': 'Stralingsmonitoring',
    'Rejected raw value': 'Verworpen ruwe waarde',
})


# Version 8.2.1 complete runtime localization.
CATALOG.update({
    'The recent level differs from counting noise with {probability:.2f}% statistical confidence': 'Het recente niveau wijkt met {probability:.2f} % statistische zekerheid af van de telruis',
    'A comparable or more extreme hourly level occurred about once in {rarity:.1f} historical hours': 'Een vergelijkbaar of extremer uurniveau kwam historisch ongeveer eens per {rarity:.1f} uur voor',
})

# Long-term analysis 9.1.0
CATALOG.update({'24 hours': '24 uur', '30 days': '30 dagen', '365 days': '365 dagen', '7 days': '7 dagen', '7-day rolling median': 'Voortschrijdende mediaan over 7 dagen', '90 days': '90 dagen', '95% block-bootstrap interval for mean': '95%-blokbootstrapinterval voor het gemiddelde', '95% block-bootstrap interval for median': '95%-blokbootstrapinterval voor de mediaan', 'Air-pressure association': 'Samenhang met luchtdruk', 'Annual projection from the last 30 days: {value} µSv': 'Jaarprojectie op basis van de laatste 30 dagen: {value} µSv', 'Annual projection is not shown until a sufficiently complete 30-day period exists.': 'De jaarprojectie wordt pas getoond na een voldoende volledige periode van 30 dagen.', 'Based on {hours} covered hours': 'Gebaseerd op {hours} gedekte uren', 'Bootstrap uncertainty, distribution dispersion, EWMA and CUSUM': 'Bootstrap-onzekerheid, spreiding, EWMA en CUSUM', 'Calendar heat map': 'Kalender-heatmap', 'Calendar heat map of daily median CPM': 'Kalender-heatmap van dagelijkse CPM-medianen', 'Connected periods above the robust local long-term threshold': 'Aaneengesloten perioden boven de robuuste lokale langetermijndrempel', 'Contextual Fano-like ratio; rolling CPM values are not independent Poisson counts': 'Contextuele Fano-achtige verhouding; voortschrijdende CPM-waarden zijn geen onafhankelijke Poisson-tellingen', 'Correlation does not prove causation.': 'Correlatie bewijst geen causaliteit.', 'Coverage {coverage}% · at least {required}% required': 'Dekking {coverage}% · minimaal {required}% vereist', 'Covered hours': 'Gedekte uren', 'Cumulative derived dose': 'Cumulatieve afgeleide dosis', 'Daily and monthly development': 'Dagelijkse en maandelijkse ontwikkeling', 'Daily median': 'Dagmediaan', 'Daily median and 7-day rolling median': 'Dagmediaan en voortschrijdende mediaan over 7 dagen', 'Daily medians, rolling median and calendar view': 'Dagmedianen, voortschrijdende mediaan en kalenderweergave', 'Derived cumulative dose: {dose} µSv': 'Afgeleide cumulatieve dosis: {dose} µSv', 'Derived dose (µSv)': 'Afgeleide dosis (µSv)', 'Derived from the robust local background; not an official alarm threshold': 'Afgeleid van de robuuste lokale achtergrond; geen officiële alarmdrempel', 'Duration (h)': 'Duur (h)', 'EWMA, CUSUM, trend tests and relative event detection provide statistical context only. They do not identify a radiation source and do not replace calibrated radiation-protection measurements.': 'EWMA, CUSUM, trendtoetsen en relatieve gebeurtenisdetectie geven alleen statistische context. Ze identificeren geen stralingsbron en vervangen geen gekalibreerde stralingsbeschermingsmetingen.', 'Effective sample size': 'Effectieve steekproefgrootte', 'Environmental correlations are exploratory. They may reflect common time patterns, ventilation, weather or other confounding factors and do not prove causation.': 'Omgevingscorrelaties zijn verkennend. Ze kunnen gemeenschappelijke tijdpatronen, ventilatie, weer of andere verstorende factoren weerspiegelen en bewijzen geen causaliteit.', 'Excess area (CPM·h)': 'Overschrijdingsoppervlak (CPM·h)', 'Exploratory Spearman correlations at 0, 3, 6, 12 and 24 hour lags': 'Verkennende Spearman-correlaties met vertragingen van 0, 3, 6, 12 en 24 uur', 'Higher': 'Hoger', 'Hourly dispersion ratio': 'Uurlijkse spreidingsverhouding', 'Lagged environmental associations': 'Vertraagde omgevingssamenhangen', 'Long-term analysis': 'Langetermijnanalyse', 'Long-term analysis for {device}': 'Langetermijnanalyse voor {device}', 'Long-term background, cumulative dose, trend, recurring patterns and statistical process diagnostics': 'Langetermijnachtergrond, cumulatieve dosis, trend, terugkerende patronen en statistische procesdiagnostiek', 'Long-term overview': 'Langetermijnoverzicht', 'Long-term statistical diagnostics': 'Statistische langetermijndiagnostiek', 'Long-term trend': 'Langetermijntrend', 'Lower': 'Lager', 'Mann-Kendall test with Sen slope on sufficiently covered daily medians': 'Mann-Kendall-toets met Sen-helling op voldoende gedekte dagmedianen', 'Maximum CPM': 'Maximale CPM', 'Mean CPM': 'Gemiddelde CPM', 'Median CPM': 'Mediane CPM', 'Median {median} CPM · coverage {coverage}%': 'Mediaan {median} CPM · dekking {coverage}%', 'Month': 'Maand', 'Monthly aggregates': 'Maandaggregaten', 'Moving blocks preserve short-range time dependence': 'Bewegende blokken behouden kortetermijnafhankelijkheid', 'No calendar data available': 'Geen kalendergegevens beschikbaar', 'No long-term analysis available yet': 'Nog geen langetermijnanalyse beschikbaar', 'No monthly aggregates available': 'Geen maandaggregaten beschikbaar', 'No persistent CUSUM signal detected': 'Geen aanhoudend CUSUM-signaal gedetecteerd', 'No persistent EWMA signal detected': 'Geen aanhoudend EWMA-signaal gedetecteerd', 'No persistent relative elevation episodes detected': 'Geen aanhoudende relatieve verhogingsperioden gedetecteerd', 'No supported dose conversion for this period': 'Geen ondersteunde dosisconversie voor deze periode', 'No value is calculated until enough hourly pairs are available.': 'Er wordt pas een waarde berekend wanneer voldoende uurparen beschikbaar zijn.', 'Not enough daily values for a long-term chart': 'Onvoldoende dagwaarden voor een langetermijngrafiek', 'Not enough paired data': 'Onvoldoende gekoppelde gegevens', 'Not yet meaningful': 'Nog niet zinvol', 'Only {covered} of {required} days covered': 'Slechts {covered} van {required} dagen gedekt', 'Persistent elevation episodes': 'Aanhoudende verhogingsperioden', 'Persistent episodes': 'Aanhoudende perioden', 'Preliminary': 'Voorlopig', 'Ready': 'Beoordeelbaar', 'Real time windows with duration and coverage checks': 'Echte tijdvensters met controle van duur en dekking', 'Recent 7-day median relative to the robust long-term background': 'Recente 7-daagse mediaan ten opzichte van de robuuste langetermijnachtergrond', 'Recent background deviation': 'Recente achtergrondafwijking', 'Relative event threshold': 'Relatieve gebeurtenisdrempel', 'Robust local background': 'Robuuste lokale achtergrond', 'Scientific interpretation': 'Wetenschappelijke interpretatie', 'Start': 'Start', 'Statistical signal detected': 'Statistisch signaal gedetecteerd', 'Stored measurements are required before long-term statistics can be calculated.': 'Opgeslagen metingen zijn nodig voordat langetermijnstatistieken kunnen worden berekend.', 'Strongest at {lag} h lag · {pairs} pairs · {strength} association': 'Sterkste samenhang bij {lag} uur vertraging · {pairs} paren · {strength} samenhang', 'Temperature association': 'Samenhang met temperatuur', 'The detector uses the robust long-term local background and does not replace radiation-safety alarms.': 'De detectie gebruikt de robuuste lokale langetermijnachtergrond en vervangt geen stralingsveiligheidsalarmen.', 'Time at or above configured danger threshold': 'Tijd op of boven de ingestelde gevarendrempel', 'Time in configured warning range': 'Tijd in het ingestelde waarschuwingsbereik', 'Typical range P05–P95: {low}–{high} CPM': 'Typisch bereik P05-P95: {low}-{high} CPM', 'moderate': 'matige', 'strong': 'sterke', 'weak': 'zwakke', '{date}: median {median} CPM, coverage {coverage}%': '{date}: mediaan {median} CPM, dekking {coverage}%', '{direction} · {slope} CPM/day · p={p}': '{direction} · {slope} CPM/dag · p={p}', '{hours} covered hours': '{hours} gedekte uren', '{hours} total elevated hours · longest {longest} h': '{hours} verhoogde uren totaal · langste {longest} uur', '{observed} daily observations · correlation duration {duration} days': '{observed} dagelijkse waarnemingen · correlatieduur {duration} dagen', '{replicates} replicates · block length {block} days': '{replicates} herhalingen · bloklengte {block} dagen', 'Long-term': 'Lange termijn', 'stable': 'stabiel', 'increasing': 'stijgend', 'decreasing': 'dalend'})

# Recent baseline wording 9.1.0
CATALOG.update({'Recent baseline context': 'Recente referentiecontext', 'Seven-day baseline deviation, drift and sustained relative events': 'Afwijking van de 7-daagse referentie, drift en aanhoudende relatieve gebeurtenissen'})


# Extended agreement and seasonal analysis 9.1.0
CATALOG.update({'Bland-Altman bias': 'Bland-Altman-bias', '95% limits of agreement': '95%-overeenstemmingsgrenzen', 'Mean signed difference A minus B': 'Gemiddeld verschil met teken A min B', 'Exploratory paired-device agreement; correlation alone does not establish agreement.': 'Verkennende overeenstemming tussen gekoppelde apparaten; correlatie alleen toont geen overeenstemming aan.', 'Seasonal month-of-year profile': 'Seizoensprofiel per kalendermaand', 'Median CPM by calendar month across available years': 'Mediaan CPM per kalendermaand over de beschikbare jaren', 'Calendar month': 'Kalendermaand', 'Days represented': 'Vertegenwoordigde dagen', 'Not enough months for a seasonal profile': 'Onvoldoende maanden voor een seizoensprofiel', 'At least six represented calendar months are required.': 'Minstens zes vertegenwoordigde kalendermaanden zijn vereist.', 'Exploratory seasonal summary; it does not separate weather, location, detector or calibration changes.': 'Verkennende seizoenssamenvatting; veranderingen in weer, locatie, detector of kalibratie worden niet afzonderlijk bepaald.'})
