from __future__ import annotations

CATALOG: dict[str, str] = {'1 h counting uncertainty': '1 h counting uncertainty',
 '1 h coverage': 'Copertura 1 h',
 '1 h mean': 'Media 1 h',
 '1 h mean / 7 d mean × 100': 'Media 1 h / media 7 g × 100',
 '1 h mean dose rate': 'Tasso di dose medio su 1 h',
 '1 h mean minus 7 d baseline': 'Media 1 h meno baseline 7 g',
 '24 h Fano factor': 'Fattore di Fano su 24 h',
 '24 h P95': 'P95 su 24 h',
 '24 h P99': 'P99 su 24 h',
 '24 h Z-score': 'Punteggio Z su 24 h',
 '24 h counting uncertainty': '24 h counting uncertainty',
 '24 h distribution, percentiles and latest-value deviation': 'Distribuzione 24 h, percentili e deviazione dell’ultimo '
                                                              'valore',
 '24 h maximum': 'Massimo su 24 h',
 '24 h mean': 'Media su 24 h',
 '24 h mean dose rate': 'Tasso di dose medio su 24 h',
 '24 h median': 'Mediana su 24 h',
 '24 h minimum': 'Minimo su 24 h',
 '24 h standard deviation': 'Deviazione standard su 24 h',
 '50th percentile': '50° percentile',
 '7 d baseline': 'Baseline 7 g',
 '7 d baseline dose rate': 'Tasso di dose della baseline su 7 giorni',
 '7 d baseline drift': 'Deriva della baseline su 7 giorni',
 '7 d counting uncertainty': '7 d counting uncertainty',
 '7-day smoothed daily median': 'Mediana giornaliera smussata su 7 giorni',
 '95th percentile': '95° percentile',
 '99th percentile': '99° percentile',
 'A device function is temporarily unavailable.': 'Una funzione del dispositivo è temporaneamente non disponibile.',
 'A fresh backup is recommended before deletion.': 'A fresh backup is recommended before deletion.',
 'A recent position change can affect comparability': 'Un recente cambio di posizione può influire sulla '
                                                      'confrontabilità',
 'Above the typical time profile': 'Sopra il profilo temporale tipico',
 'Above the usual local range': 'Sopra l’intervallo locale abituale',
 'Absolute radiation assessment': 'Valutazione assoluta della radiazione',
 'Absolute thresholds and local anomaly detection answer different questions.': 'Le soglie assolute e il rilevamento '
                                                                                'locale delle anomalie rispondono a '
                                                                                'domande diverse.',
 'Acceleration magnitude': 'Modulo accelerazione',
 'Acceleration raw values': 'Valori grezzi accelerazione',
 'Accepted device values are stored separately after live CPM plausibility confirmation': 'Accepted device values are '
                                                                                          'stored separately after '
                                                                                          'live CPM plausibility '
                                                                                          'confirmation',
 'Active threshold profile': 'Profilo soglie attivo',
 'Adaptive background profile': 'Profilo di fondo adattivo',
 'Advanced': 'Avanzato',
 'Advanced diagnostics': 'Diagnostica avanzata',
 'Advanced visuals': 'Visualizzazioni avanzate',
 'Affected GMC devices': 'Affected GMC devices',
 'Agreement': 'Concordanza',
 'Air-pressure source': 'Fonte della pressione atmosferica',
 'Air-pressure trend': 'Andamento della pressione atmosferica',
 'All GMC history was deleted': 'All GMC history was deleted',
 'All baselines and comparisons use the same robust quality-filtered measurements.': 'Tutte le baseline e i confronti '
                                                                                     'usano le stesse misure robuste '
                                                                                     'filtrate per qualità.',
 'All connected GMC devices': 'Tutti i dispositivi GMC collegati',
 'All devices': 'Tutti i dispositivi',
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
 'All statistical values, confidence intervals and diagnostics': 'Tutti i valori statistici, gli intervalli di '
                                                                 'confidenza e la diagnostica',
 'All {count} known GMC devices are connected': 'All {count} known GMC devices are connected',
 'Allow restore': 'Consenti ripristino',
 'Already assigned to {name}': 'Already assigned to {name}',
 'Analysis': 'Analisi',
 'Analysis JSON': 'JSON analisi',
 'Analysis PDF': 'PDF di analisi',
 'Analysis depth': 'Livello di analisi',
 'Analysis for': 'Analisi di',
 'Analysis is still being prepared': 'Analysis is still being prepared',
 'Analysis shown': 'Analisi visualizzata',
 'Analysis, the traffic light and downloads will become meaningful after the first stored samples arrive.': 'L’analisi, '
                                                                                                            'il '
                                                                                                            'semaforo '
                                                                                                            'e i '
                                                                                                            'download '
                                                                                                            'diventeranno '
                                                                                                            'significativi '
                                                                                                            'dopo la '
                                                                                                            'memorizzazione '
                                                                                                            'delle '
                                                                                                            'prime '
                                                                                                            'misure.',
 'Analyze this device': 'Analizza questo dispositivo',
 'Another report is already being generated': 'È già in corso la generazione di un altro rapporto',
 'Another report or maintenance job is running': 'Another report or maintenance job is running',
 'Another report or restore job is running': 'È già in corso un altro rapporto o ripristino',
 'Another report, maintenance export, or restore job is running': 'È già in esecuzione un altro rapporto, '
                                                                  'un’esportazione di manutenzione o un ripristino.',
 'App Started At': 'App avviata alle',
 'Apply': 'Apply',
 'Assessment': 'Valutazione',
 'Assigned': 'Assigned',
 'At least 24 h reference and 6 h persistence are required': 'At least 24 h reference and 6 h persistence are required',
 'At least two daily background values are required.': 'Sono necessari almeno due valori giornalieri del fondo.',
 'At least {count} valid hourly values are required': 'Sono necessari almeno {count} valori orari validi',
 'At least {count} valid pairs are required': 'Sono necessarie almeno {count} coppie valide',
 'At least {days} days of learning data are required': 'Sono necessari almeno {days} giorni di dati di apprendimento',
 'At least {span:g} hPa pressure variation is required': 'È necessaria una variazione di pressione di almeno {span:g} '
                                                         'hPa',
 'At the same time, the value is clearly above the usual local background. Review the trend and measurement conditions.': 'Allo '
                                                                                                                          'stesso '
                                                                                                                          'tempo '
                                                                                                                          'il '
                                                                                                                          'valore '
                                                                                                                          'è '
                                                                                                                          'chiaramente '
                                                                                                                          'sopra '
                                                                                                                          'il '
                                                                                                                          'fondo '
                                                                                                                          'locale '
                                                                                                                          'abituale. '
                                                                                                                          'Verifica '
                                                                                                                          'la '
                                                                                                                          'tendenza '
                                                                                                                          'e '
                                                                                                                          'le '
                                                                                                                          'condizioni '
                                                                                                                          'di '
                                                                                                                          'misura.',
 'Automatic device detection is running': 'Automatic device detection is running',
 'Automatic refresh is temporarily unavailable': 'Automatic refresh is temporarily unavailable',
 'Availability': 'Disponibilità',
 'Available': 'Available',
 'Back to analysis': 'Back to analysis',
 'Background index': 'Indice di fondo',
 'Background index compares the rolling 1 h mean with the available 7 d baseline.': 'Indice di fondo = media mobile di '
                                                                                    '1 h rapportata alla baseline '
                                                                                    'disponibile di 7 giorni.',
 'Background index formula explanation': 'Indice di fondo = media mobile di 1 h rapportata alla baseline disponibile '
                                         'di 7 giorni.',
 'Background trend over days and months': 'Andamento del fondo nel corso di giorni e mesi',
 'Backup is compatible and ready to restore.': 'Backup is compatible and ready to restore.',
 'Backup preview failed': 'Backup preview failed',
 'Baseline available': 'Baseline disponibile',
 'Baseline currently stable': 'Baseline attualmente stabile',
 'Baseline deviation': 'Deviazione dalla baseline',
 'Baseline deviation, drift and sustained relative events': 'Deviazione e deriva della baseline ed eventi relativi '
                                                            'persistenti',
 'Baseline deviation: {cpm} CPM ({percent}%)': 'Deviazione dalla baseline: {cpm} CPM ({percent}%)',
 'Baseline drift: {value}%': 'Deriva della baseline: {value}%',
 'Baseline learning in progress': 'Apprendimento della baseline in corso',
 'Baseline readiness': 'Disponibilità della baseline',
 'Baseline: {value} CPM': 'Baseline: {value} CPM',
 'Battery voltage': 'Tensione della batteria',
 'Baud rate': 'Velocità in baud',
 'Below the typical time profile': 'Sotto il profilo temporale tipico',
 'Below warning threshold': 'Sotto la soglia di avviso',
 'BfS and ICRP reference profiles convert annual dose values into continuous-rate equivalents for context. They are not official instantaneous alarm limits and cannot replace professional dose assessment.': 'I '
                                                                                                                                                                                                               'profili '
                                                                                                                                                                                                               'di '
                                                                                                                                                                                                               'riferimento '
                                                                                                                                                                                                               'BfS '
                                                                                                                                                                                                               'e '
                                                                                                                                                                                                               'ICRP '
                                                                                                                                                                                                               'convertono '
                                                                                                                                                                                                               'le '
                                                                                                                                                                                                               'dosi '
                                                                                                                                                                                                               'annuali '
                                                                                                                                                                                                               'in '
                                                                                                                                                                                                               'equivalenti '
                                                                                                                                                                                                               'di '
                                                                                                                                                                                                               'tasso '
                                                                                                                                                                                                               'continuo '
                                                                                                                                                                                                               'a '
                                                                                                                                                                                                               'scopo '
                                                                                                                                                                                                               'contestuale. '
                                                                                                                                                                                                               'Non '
                                                                                                                                                                                                               'sono '
                                                                                                                                                                                                               'limiti '
                                                                                                                                                                                                               'ufficiali '
                                                                                                                                                                                                               'di '
                                                                                                                                                                                                               'allarme '
                                                                                                                                                                                                               'istantaneo '
                                                                                                                                                                                                               'e '
                                                                                                                                                                                                               'non '
                                                                                                                                                                                                               'sostituiscono '
                                                                                                                                                                                                               'una '
                                                                                                                                                                                                               'valutazione '
                                                                                                                                                                                                               'dosimetrica '
                                                                                                                                                                                                               'professionale.',
 'BfS reference projection': 'Proiezione di riferimento BfS',
 'Both connected counters show a quality-filtered simultaneous rise': 'Entrambi i contatori collegati mostrano un '
                                                                      'aumento simultaneo filtrato per qualità',
 'Both connected counters show a simultaneous rise': 'Entrambi i contatori connessi mostrano un aumento simultaneo',
 'Broadly compatible with Poisson-like spread': 'In generale compatibile con una dispersione tipo Poisson',
 'CPM': 'CPM',
 'CPM and derived dose rate': 'CPM e tasso di dose derivato',
 'CPM distribution and Poisson comparison': 'Distribuzione CPM e confronto di Poisson',
 'CPM distribution — {title}': 'Distribuzione CPM — {title}',
 'CPM is the primary measurement.': 'Il CPM è la misura principale.',
 'CPM per µSv/h': 'CPM per µSv/h',
 'CPM quality': 'Qualità CPM',
 'CPM statistics  min {minimum:.0f} | max {maximum:.0f} | mean {mean:.2f} | median {median:.2f} | SD {sd:.2f} | P95 {p95:.2f} | missing {missing}': 'Statistiche '
                                                                                                                                                    'CPM  '
                                                                                                                                                    'min '
                                                                                                                                                    '{minimum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'max '
                                                                                                                                                    '{maximum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'media '
                                                                                                                                                    '{mean:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'mediana '
                                                                                                                                                    '{median:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'DS '
                                                                                                                                                    '{sd:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'P95 '
                                                                                                                                                    '{p95:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'mancanti '
                                                                                                                                                    '{missing}',
 'CPM statistics: no accepted measurements in selected period': 'Statistiche CPM: nessuna misura accettata nel periodo '
                                                                'selezionato',
 'CPM–pressure correlation': 'Correlazione CPM–pressione',
 'CPM–temperature correlation': 'Correlazione CPM–temperatura',
 'CPM–voltage correlation': 'Correlazione CPM–tensione',
 'CSV files preserve every accepted measurement without interpolation. PNG reports include CPM, temperature, voltage, optional raw signed gyro diagnostics, summary statistics, sample completeness, device identity, timezone, period and generation time. ZIP bundles additionally contain analysis JSON, daily summaries, events, histogram, heatmap and a multi-page PDF report.': 'I '
                                                                                                                                                                                                                                                                                                                                                                                       'file '
                                                                                                                                                                                                                                                                                                                                                                                       'CSV '
                                                                                                                                                                                                                                                                                                                                                                                       'conservano '
                                                                                                                                                                                                                                                                                                                                                                                       'ogni '
                                                                                                                                                                                                                                                                                                                                                                                       'misura '
                                                                                                                                                                                                                                                                                                                                                                                       'accettata '
                                                                                                                                                                                                                                                                                                                                                                                       'senza '
                                                                                                                                                                                                                                                                                                                                                                                       'interpolazione. '
                                                                                                                                                                                                                                                                                                                                                                                       'I '
                                                                                                                                                                                                                                                                                                                                                                                       'rapporti '
                                                                                                                                                                                                                                                                                                                                                                                       'PNG '
                                                                                                                                                                                                                                                                                                                                                                                       'includono '
                                                                                                                                                                                                                                                                                                                                                                                       'CPM, '
                                                                                                                                                                                                                                                                                                                                                                                       'temperatura, '
                                                                                                                                                                                                                                                                                                                                                                                       'tensione, '
                                                                                                                                                                                                                                                                                                                                                                                       'diagnostica '
                                                                                                                                                                                                                                                                                                                                                                                       'giroscopica '
                                                                                                                                                                                                                                                                                                                                                                                       'grezza '
                                                                                                                                                                                                                                                                                                                                                                                       'con '
                                                                                                                                                                                                                                                                                                                                                                                       'segno '
                                                                                                                                                                                                                                                                                                                                                                                       'opzionale, '
                                                                                                                                                                                                                                                                                                                                                                                       'statistiche '
                                                                                                                                                                                                                                                                                                                                                                                       'riepilogative, '
                                                                                                                                                                                                                                                                                                                                                                                       'completezza, '
                                                                                                                                                                                                                                                                                                                                                                                       'identità '
                                                                                                                                                                                                                                                                                                                                                                                       'del '
                                                                                                                                                                                                                                                                                                                                                                                       'dispositivo, '
                                                                                                                                                                                                                                                                                                                                                                                       'fuso '
                                                                                                                                                                                                                                                                                                                                                                                       'orario, '
                                                                                                                                                                                                                                                                                                                                                                                       'periodo '
                                                                                                                                                                                                                                                                                                                                                                                       'e '
                                                                                                                                                                                                                                                                                                                                                                                       'ora '
                                                                                                                                                                                                                                                                                                                                                                                       'di '
                                                                                                                                                                                                                                                                                                                                                                                       'generazione. '
                                                                                                                                                                                                                                                                                                                                                                                       'I '
                                                                                                                                                                                                                                                                                                                                                                                       'pacchetti '
                                                                                                                                                                                                                                                                                                                                                                                       'ZIP '
                                                                                                                                                                                                                                                                                                                                                                                       'contengono '
                                                                                                                                                                                                                                                                                                                                                                                       'inoltre '
                                                                                                                                                                                                                                                                                                                                                                                       'JSON '
                                                                                                                                                                                                                                                                                                                                                                                       'di '
                                                                                                                                                                                                                                                                                                                                                                                       'analisi, '
                                                                                                                                                                                                                                                                                                                                                                                       'riepiloghi '
                                                                                                                                                                                                                                                                                                                                                                                       'giornalieri, '
                                                                                                                                                                                                                                                                                                                                                                                       'eventi, '
                                                                                                                                                                                                                                                                                                                                                                                       'istogramma, '
                                                                                                                                                                                                                                                                                                                                                                                       'mappa '
                                                                                                                                                                                                                                                                                                                                                                                       'di '
                                                                                                                                                                                                                                                                                                                                                                                       'calore '
                                                                                                                                                                                                                                                                                                                                                                                       'e '
                                                                                                                                                                                                                                                                                                                                                                                       'un '
                                                                                                                                                                                                                                                                                                                                                                                       'rapporto '
                                                                                                                                                                                                                                                                                                                                                                                       'PDF '
                                                                                                                                                                                                                                                                                                                                                                                       'multipagina.',
 'Calibrated acceleration': 'Accelerazione calibrata',
 'Calibration profile': 'Profilo di calibrazione',
 'Capabilities': 'Capacità',
 'Check location, orientation and environmental conditions when a persistent jump appears.': 'Controlla posizione, '
                                                                                             'orientamento e '
                                                                                             'condizioni ambientali '
                                                                                             'quando compare un salto '
                                                                                             'persistente.',
 'Check manually': 'Controllare manualmente',
 'Check the Home Assistant general settings and restart the add-on.': 'Controllare le impostazioni generali di Home '
                                                                      'Assistant e riavviare il componente aggiuntivo.',
 'Check the USB cable and power supply if this continues for more than 15 minutes.': 'Controlla il cavo USB e '
                                                                                     'l’alimentazione se il problema '
                                                                                     'continua per più di 15 minuti.',
 'Check the measurement conditions, observe the trend and verify the reading with an appropriate instrument if it persists.': 'Controllare '
                                                                                                                              'le '
                                                                                                                              'condizioni '
                                                                                                                              'di '
                                                                                                                              'misura, '
                                                                                                                              'osservare '
                                                                                                                              'l’andamento '
                                                                                                                              'e '
                                                                                                                              'verificare '
                                                                                                                              'la '
                                                                                                                              'lettura '
                                                                                                                              'con '
                                                                                                                              'uno '
                                                                                                                              'strumento '
                                                                                                                              'appropriato '
                                                                                                                              'se '
                                                                                                                              'persiste.',
 'Check the measurement location': 'Controllare il luogo di misura',
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
 'Choose how much detail the analysis cards show. The selection is stored in this browser.': 'Scegliere quanti '
                                                                                             'dettagli mostrare nelle '
                                                                                             'schede di analisi. La '
                                                                                             'selezione viene salvata '
                                                                                             'in questo browser.',
 'Choose whether reports include all devices or one selected device.': 'Scegli se i rapporti includono tutti i '
                                                                       'dispositivi o un solo dispositivo selezionato.',
 'Clear': 'Clear',
 'Clearly above the usual local range': 'Chiaramente sopra l’intervallo locale abituale',
 'Clearly elevated': 'Chiaramente elevato',
 'Clearly elevated: clearly above the usual local range': 'Chiaramente elevato: chiaramente sopra l’intervallo locale '
                                                          'abituale',
 'Clock offset exceeds warning threshold': 'Lo scostamento dell’orologio supera la soglia di avviso',
 'Clock synchronized': 'Orologio sincronizzato',
 'Close to Poisson expectation': 'Vicino all’attesa di Poisson',
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
 'Compared with local baseline': 'Confrontato con la baseline locale',
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
 'Compares the current value with the usual background at this location.': 'Confronta il valore attuale con il fondo '
                                                                           'abituale del luogo.',
 'Comparison confidence': 'Affidabilità del confronto',
 'Complete ZIP bundle': 'Pacchetto ZIP completo',
 'Complete history deletion failed': 'Complete history deletion failed',
 'Complete history deletion is disabled in the app configuration.': 'L’eliminazione completa della cronologia è '
                                                                    'disattivata nella configurazione '
                                                                    'dell’applicazione.',
 'Completeness: {value:.2f}%': 'Completezza: {value:.2f}%',
 'Confidence': 'Affidabilità',
 'Configured CPM conversion factor': 'Fattore di conversione CPM configurato',
 'Configured baud rate': 'Velocità in baud configurata',
 'Configured device name': 'Nome dispositivo configurato',
 'Configured location': 'Posizione configurata',
 'Configured measurement interval': 'Intervallo di misura configurato',
 'Confirmed original samples in 24 h · {accepted} stored': 'Confirmed original samples in 24 h · {accepted} stored',
 'Connect two devices to enable comparison.': 'Collegare due dispositivi per attivare il confronto.',
 'Connect two devices to learn a relative response factor.': 'Connect two devices to learn a relative response factor.',
 'Connected GMC devices': 'Dispositivi GMC collegati',
 'Connected counters without an active stability warning': 'Contatori collegati senza avvisi attivi di stabilità',
 'Connected devices': 'Dispositivi collegati',
 'Connection active': 'Connection active',
 'Consecutive upload errors': 'Errori di invio consecutivi',
 'Continue observing': 'Continuare a osservare',
 'Coordinates': 'Coordinate',
 'Correlation': 'Correlazione',
 'Correlation does not imply causation. Strong values should be investigated over longer periods before drawing conclusions.': 'La '
                                                                                                                               'correlazione '
                                                                                                                               'non '
                                                                                                                               'implica '
                                                                                                                               'causalità. '
                                                                                                                               'I '
                                                                                                                               'valori '
                                                                                                                               'elevati '
                                                                                                                               'vanno '
                                                                                                                               'esaminati '
                                                                                                                               'su '
                                                                                                                               'periodi '
                                                                                                                               'più '
                                                                                                                               'lunghi '
                                                                                                                               'prima '
                                                                                                                               'di '
                                                                                                                               'trarre '
                                                                                                                               'conclusioni.',
 'Cosmic influence is possible': 'Possibile influenza cosmica',
 'Cosmic influence – statistical indication': 'Influenza cosmica – indicazione statistica',
 'Counter ID': 'ID contatore',
 'Counting statistics': 'Statistiche di conteggio',
 'Counting uncertainty (68%): −{minus:.2f}/+{plus:.2f} CPM · {impulses} impulses in {duration}': 'Counting uncertainty '
                                                                                                 '(68%): '
                                                                                                 '−{minus:.2f}/+{plus:.2f} '
                                                                                                 'CPM · {impulses} '
                                                                                                 'impulses in '
                                                                                                 '{duration}',
 'Counting uncertainty not available': 'Counting uncertainty not available',
 'Country': 'Paese',
 'Coverage percent': 'Copertura percentuale',
 'Coverage, gaps, runtime counters and derived dose-rate values': 'Copertura, lacune, contatori di esecuzione e ratei '
                                                                  'di dose derivati',
 'Critical': 'Critico',
 'Critical: danger threshold exceeded': 'Critico: soglia di pericolo superata',
 'Current': 'Attuale',
 'Current air pressure': 'Pressione atmosferica attuale',
 'Current database size': 'Current database size',
 'Current difference': 'Differenza attuale',
 'Current value': 'Valore attuale',
 'Current value is {z:+.2f} robust standard deviations from the 24 h median': 'Il valore attuale è a {z:+.2f} '
                                                                              'deviazioni standard robuste dalla '
                                                                              'mediana delle 24 h',
 'Current value is {z:+.2f} standard deviations from the 24 h mean': 'Il valore attuale dista {z:+.2f} deviazioni '
                                                                     'standard dalla media di 24 ore',
 'Current week bundle': 'Pacchetto settimana corrente',
 'Currently selected': 'Attualmente selezionato',
 'Custom period': 'Periodo personalizzato',
 'Custom thresholds': 'Soglie personalizzate',
 'Daily and weekly profile is still being formed': 'Il profilo giornaliero e settimanale è ancora in formazione',
 'Daily quality-filtered medians are smoothed over seven days. The period cards compare the recent part of each period with the preceding part; detected jumps are statistical changes and do not determine their cause.': 'Le '
                                                                                                                                                                                                                           'mediane '
                                                                                                                                                                                                                           'giornaliere '
                                                                                                                                                                                                                           'filtrate '
                                                                                                                                                                                                                           'per '
                                                                                                                                                                                                                           'qualità '
                                                                                                                                                                                                                           'vengono '
                                                                                                                                                                                                                           'smussate '
                                                                                                                                                                                                                           'su '
                                                                                                                                                                                                                           'sette '
                                                                                                                                                                                                                           'giorni. '
                                                                                                                                                                                                                           'Le '
                                                                                                                                                                                                                           'schede '
                                                                                                                                                                                                                           'dei '
                                                                                                                                                                                                                           'periodi '
                                                                                                                                                                                                                           'confrontano '
                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                           'parte '
                                                                                                                                                                                                                           'recente '
                                                                                                                                                                                                                           'di '
                                                                                                                                                                                                                           'ciascun '
                                                                                                                                                                                                                           'periodo '
                                                                                                                                                                                                                           'con '
                                                                                                                                                                                                                           'quella '
                                                                                                                                                                                                                           'precedente; '
                                                                                                                                                                                                                           'i '
                                                                                                                                                                                                                           'salti '
                                                                                                                                                                                                                           'rilevati '
                                                                                                                                                                                                                           'sono '
                                                                                                                                                                                                                           'cambiamenti '
                                                                                                                                                                                                                           'statistici '
                                                                                                                                                                                                                           'e '
                                                                                                                                                                                                                           'non '
                                                                                                                                                                                                                           'ne '
                                                                                                                                                                                                                           'determinano '
                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                           'causa.',
 'Daily summary CSV': 'CSV riepilogo giornaliero',
 'Danger threshold exceeded': 'Soglia di pericolo superata',
 'Danger thresholds': 'Soglie di pericolo',
 'Danger zone': 'Danger zone',
 'Dashboard navigation': 'Dashboard navigation',
 'Data exports': 'Esportazioni dati',
 'Data period': 'Data period',
 'Data quality': 'Qualità dei dati',
 'Data quality is too low for a reliable assessment': 'La qualità dei dati è troppo bassa per una valutazione '
                                                      'affidabile',
 'Data quality status unavailable': 'Stato qualità dati non disponibile',
 'Data quality: {value}': 'Qualità dati: {value}',
 'Database': 'Database',
 'Database health': 'Stato database',
 'Database size': 'Dimensione database',
 'Date': 'Data',
 'Delete all GMC history': 'Delete all GMC history',
 'Delete history': 'Delete history',
 'Deletion confirmation text must be exactly DELETE ALL GMC HISTORY': 'Deletion confirmation text must be exactly '
                                                                      'DELETE ALL GMC HISTORY',
 'Deletion is disabled by default.': 'Deletion is disabled by default.',
 'Derived dose rate': 'Tasso di dose derivato',
 'Derived from 1 h mean CPM': 'Derivato dalla media CPM di 1 h',
 'Derived from 24 h mean CPM': 'Derivato dalla media CPM di 24 h',
 'Derived from 7 d mean CPM': 'Derivato dalla media CPM di 7 g',
 'Derived from latest CPM': 'Derivato dall’ultimo CPM',
 'Detailed interpretation and the most useful supporting values': 'Interpretazione dettagliata e valori di supporto '
                                                                  'più utili',
 'Detect, identify and assign GMC counters': 'Detect, identify and assign GMC counters',
 'Detected': 'Rilevato',
 'Detected Capabilities': 'Funzionalità rilevate',
 'Detected GMC device': 'Detected GMC device',
 'Detected baseline jumps': 'Salti della baseline rilevati',
 'Detected relative anomaly events: {count}': 'Eventi di anomalia relativa rilevati: {count}',
 'Deviation': 'Scostamento',
 'Device': 'Dispositivo',
 'Device Profile': 'Profilo dispositivo',
 'Device Time Errors Since Start': 'Errori dell’ora del dispositivo dall’avvio',
 'Device assignments saved': 'Device assignments saved',
 'Device assignments were saved.': 'Device assignments were saved.',
 'Device baseline': 'Baseline del dispositivo',
 'Device capabilities': 'Funzioni del dispositivo',
 'Device clock': 'Orologio del dispositivo',
 'Device clock offset': 'Scostamento dell’orologio del dispositivo',
 'Device clock status': 'Stato dell’orologio del dispositivo',
 'Device clock unavailable': 'Orologio del dispositivo non disponibile',
 'Device clock warning': 'Device clock warning',
 'Device comparison': 'Confronto dispositivi',
 'Device details, live values and analysis selection are shown below.': 'Di seguito sono mostrati i dettagli, i valori '
                                                                        'attuali e la selezione di analisi di ciascun '
                                                                        'dispositivo.',
 'Device health warning': 'Device health warning',
 'Device position': 'Posizione dispositivo',
 'Device status updated': 'Device status updated',
 'Device temperature is unavailable.': 'La temperatura del dispositivo non è disponibile.',
 'Device time': 'Ora del dispositivo',
 'Device-specific details are listed above.': 'I dettagli specifici dei dispositivi sono elencati nella sezione '
                                              'superiore.',
 'Device: {value}': 'Dispositivo: {value}',
 'Devices': 'Devices',
 'Diagnostics JSON': 'JSON diagnostica',
 'Disabled': 'Disattivato',
 'Discarded CPM peaks': 'Discarded CPM peaks',
 'Discarded unconfirmed CPM peaks': 'Discarded unconfirmed CPM peaks',
 'Display down': 'Piatto, display in basso',
 'Display up': 'Piatto, display in alto',
 'Dose rate = CPM / configured conversion factor ({factor:g} CPM per µSv/h).': 'Rateo di dose = CPM / fattore di '
                                                                               'conversione configurato ({factor:g} '
                                                                               'CPM per µSv/h).',
 'Dose rate formula explanation': 'Rateo di dose = CPM / fattore di conversione configurato ({factor:g} CPM per '
                                  'µSv/h).',
 'Dose-rate values are derived from CPM using the configured conversion factor.': 'I valori di dose rate sono derivati '
                                                                                  'dal CPM usando il fattore di '
                                                                                  'conversione configurato.',
 'Dose-rate values, traffic-light states and events are derived indicators. CPM remains the primary measurement.': 'Dose '
                                                                                                                   'rate, '
                                                                                                                   'stati '
                                                                                                                   'del '
                                                                                                                   'semaforo '
                                                                                                                   'ed '
                                                                                                                   'eventi '
                                                                                                                   'sono '
                                                                                                                   'indicatori '
                                                                                                                   'derivati. '
                                                                                                                   'Il '
                                                                                                                   'CPM '
                                                                                                                   'resta '
                                                                                                                   'la '
                                                                                                                   'misura '
                                                                                                                   'principale.',
 'Download': 'Scarica',
 'Downloads': 'Download',
 'Dual-tube measurement': 'Misurazione a doppio tubo',
 'Duration [s]': 'Durata [s]',
 'During the learning phase, leave the counters in a stable location and allow additional measurements to accumulate.': 'Durante '
                                                                                                                        'la '
                                                                                                                        'fase '
                                                                                                                        'di '
                                                                                                                        'apprendimento, '
                                                                                                                        'lascia '
                                                                                                                        'i '
                                                                                                                        'contatori '
                                                                                                                        'in '
                                                                                                                        'una '
                                                                                                                        'posizione '
                                                                                                                        'stabile '
                                                                                                                        'e '
                                                                                                                        'consenti '
                                                                                                                        'l’accumulo '
                                                                                                                        'di '
                                                                                                                        'ulteriori '
                                                                                                                        'misure.',
 'Each device has its own MQTT identity and history. The cards show the latest accepted measurement.': 'Ogni '
                                                                                                       'dispositivo '
                                                                                                       'dispone di una '
                                                                                                       'propria '
                                                                                                       'identità MQTT '
                                                                                                       'e cronologia. '
                                                                                                       'Le schede '
                                                                                                       'mostrano '
                                                                                                       'l’ultima '
                                                                                                       'misurazione '
                                                                                                       'accettata.',
 'Each physical serial device can only be assigned once': 'Each physical serial device can only be assigned once',
 'Elevated': 'Elevato',
 'Elevated relative background': 'Fondo relativo elevato',
 'Elevated: within warning range': 'Elevato: nell’intervallo di avviso',
 'Elevation': 'Altitudine',
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
 'Enable enable_restore in the app configuration and restart only when a restore is planned.': 'Abilitare '
                                                                                               'enable_restore nella '
                                                                                               'configurazione '
                                                                                               'dell’app e riavviare '
                                                                                               'solo quando è previsto '
                                                                                               'un ripristino.',
 'Enable “{setting}” in the app configuration and restart only when a restore is planned.': 'Attiva “{setting}” nella '
                                                                                            'configurazione dell’app e '
                                                                                            'riavvia solo quando è '
                                                                                            'previsto un ripristino.',
 'End time UTC': 'Ora fine UTC',
 'End time local': 'Ora fine locale',
 'Entities': 'Entità',
 'Environment': 'Ambiente',
 'Error time': 'Ora dell’errore',
 'Estimated pressure influence': 'Influenza stimata della pressione',
 'Evaluated by': 'Valutato in base a',
 'Evaluates the current value using the configured thresholds.': 'Valuta il valore attuale usando le soglie '
                                                                 'configurate.',
 'Events CSV': 'CSV eventi',
 'Events and diagnostics': 'Events and diagnostics',
 'Events last 24 h': 'Eventi delle ultime 24 h',
 'Excellent': 'Eccellente',
 'Excluded measurements': 'Misure escluse',
 'Excluded pairs': 'Coppie escluse',
 'Expand all': 'Expand all',
 'Expected samples': 'Campioni attesi',
 'Expert view': 'Vista esperto',
 'Explanation of the two assessments': 'Spiegazione delle due valutazioni',
 'Export details': 'Dettagli esportazione',
 'Extremely elevated': 'Estremamente elevato',
 'Extremely elevated: far above the usual local range': 'Estremamente elevato: molto sopra l’intervallo locale '
                                                        'abituale',
 'Falling': 'In diminuzione',
 'Falling air pressure can slightly increase the share of cosmically generated secondary radiation at ground level, while rising air pressure tends to reduce it; the model detects only such statistical relationships and cannot clearly distinguish them from other natural influences.': 'Una '
                                                                                                                                                                                                                                                                                             'diminuzione '
                                                                                                                                                                                                                                                                                             'della '
                                                                                                                                                                                                                                                                                             'pressione '
                                                                                                                                                                                                                                                                                             'atmosferica '
                                                                                                                                                                                                                                                                                             'può '
                                                                                                                                                                                                                                                                                             'aumentare '
                                                                                                                                                                                                                                                                                             'leggermente '
                                                                                                                                                                                                                                                                                             'la '
                                                                                                                                                                                                                                                                                             'quota '
                                                                                                                                                                                                                                                                                             'di '
                                                                                                                                                                                                                                                                                             'radiazione '
                                                                                                                                                                                                                                                                                             'secondaria '
                                                                                                                                                                                                                                                                                             'di '
                                                                                                                                                                                                                                                                                             'origine '
                                                                                                                                                                                                                                                                                             'cosmica '
                                                                                                                                                                                                                                                                                             'al '
                                                                                                                                                                                                                                                                                             'suolo, '
                                                                                                                                                                                                                                                                                             'mentre '
                                                                                                                                                                                                                                                                                             'un '
                                                                                                                                                                                                                                                                                             'aumento '
                                                                                                                                                                                                                                                                                             'tende '
                                                                                                                                                                                                                                                                                             'a '
                                                                                                                                                                                                                                                                                             'ridurla; '
                                                                                                                                                                                                                                                                                             'il '
                                                                                                                                                                                                                                                                                             'modello '
                                                                                                                                                                                                                                                                                             'rileva '
                                                                                                                                                                                                                                                                                             'soltanto '
                                                                                                                                                                                                                                                                                             'tali '
                                                                                                                                                                                                                                                                                             'relazioni '
                                                                                                                                                                                                                                                                                             'statistiche '
                                                                                                                                                                                                                                                                                             'e '
                                                                                                                                                                                                                                                                                             'non '
                                                                                                                                                                                                                                                                                             'può '
                                                                                                                                                                                                                                                                                             'distinguerle '
                                                                                                                                                                                                                                                                                             'chiaramente '
                                                                                                                                                                                                                                                                                             'da '
                                                                                                                                                                                                                                                                                             'altri '
                                                                                                                                                                                                                                                                                             'influssi '
                                                                                                                                                                                                                                                                                             'naturali.',
 'Falling air pressure is often associated with a slightly higher intensity of cosmically generated secondary radiation at ground level, while rising air pressure is associated with a slightly lower intensity. The strength of this relationship depends on detector, location and atmosphere; the cause cannot be determined unambiguously from total counts.': 'Una '
                                                                                                                                                                                                                                                                                                                                                                    'pressione '
                                                                                                                                                                                                                                                                                                                                                                    'atmosferica '
                                                                                                                                                                                                                                                                                                                                                                    'in '
                                                                                                                                                                                                                                                                                                                                                                    'calo '
                                                                                                                                                                                                                                                                                                                                                                    'è '
                                                                                                                                                                                                                                                                                                                                                                    'spesso '
                                                                                                                                                                                                                                                                                                                                                                    'associata '
                                                                                                                                                                                                                                                                                                                                                                    'a '
                                                                                                                                                                                                                                                                                                                                                                    'un’intensità '
                                                                                                                                                                                                                                                                                                                                                                    'leggermente '
                                                                                                                                                                                                                                                                                                                                                                    'maggiore '
                                                                                                                                                                                                                                                                                                                                                                    'della '
                                                                                                                                                                                                                                                                                                                                                                    'radiazione '
                                                                                                                                                                                                                                                                                                                                                                    'secondaria '
                                                                                                                                                                                                                                                                                                                                                                    'di '
                                                                                                                                                                                                                                                                                                                                                                    'origine '
                                                                                                                                                                                                                                                                                                                                                                    'cosmica '
                                                                                                                                                                                                                                                                                                                                                                    'al '
                                                                                                                                                                                                                                                                                                                                                                    'suolo, '
                                                                                                                                                                                                                                                                                                                                                                    'mentre '
                                                                                                                                                                                                                                                                                                                                                                    'una '
                                                                                                                                                                                                                                                                                                                                                                    'pressione '
                                                                                                                                                                                                                                                                                                                                                                    'in '
                                                                                                                                                                                                                                                                                                                                                                    'aumento '
                                                                                                                                                                                                                                                                                                                                                                    'è '
                                                                                                                                                                                                                                                                                                                                                                    'associata '
                                                                                                                                                                                                                                                                                                                                                                    'a '
                                                                                                                                                                                                                                                                                                                                                                    'un’intensità '
                                                                                                                                                                                                                                                                                                                                                                    'leggermente '
                                                                                                                                                                                                                                                                                                                                                                    'minore. '
                                                                                                                                                                                                                                                                                                                                                                    'L’intensità '
                                                                                                                                                                                                                                                                                                                                                                    'di '
                                                                                                                                                                                                                                                                                                                                                                    'questa '
                                                                                                                                                                                                                                                                                                                                                                    'relazione '
                                                                                                                                                                                                                                                                                                                                                                    'dipende '
                                                                                                                                                                                                                                                                                                                                                                    'dal '
                                                                                                                                                                                                                                                                                                                                                                    'rivelatore, '
                                                                                                                                                                                                                                                                                                                                                                    'dal '
                                                                                                                                                                                                                                                                                                                                                                    'luogo '
                                                                                                                                                                                                                                                                                                                                                                    'e '
                                                                                                                                                                                                                                                                                                                                                                    'dall’atmosfera; '
                                                                                                                                                                                                                                                                                                                                                                    'la '
                                                                                                                                                                                                                                                                                                                                                                    'causa '
                                                                                                                                                                                                                                                                                                                                                                    'non '
                                                                                                                                                                                                                                                                                                                                                                    'può '
                                                                                                                                                                                                                                                                                                                                                                    'essere '
                                                                                                                                                                                                                                                                                                                                                                    'determinata '
                                                                                                                                                                                                                                                                                                                                                                    'in '
                                                                                                                                                                                                                                                                                                                                                                    'modo '
                                                                                                                                                                                                                                                                                                                                                                    'univoco '
                                                                                                                                                                                                                                                                                                                                                                    'dai '
                                                                                                                                                                                                                                                                                                                                                                    'conteggi '
                                                                                                                                                                                                                                                                                                                                                                    'totali.',
 'Fano factor': 'Fattore di Fano',
 'Fano factor = variance / mean; a value near 1 is consistent with Poisson-like counting statistics.': 'Fattore di '
                                                                                                       'Fano = '
                                                                                                       'varianza / '
                                                                                                       'media; un '
                                                                                                       'valore vicino '
                                                                                                       'a 1 è '
                                                                                                       'compatibile '
                                                                                                       'con un '
                                                                                                       'conteggio di '
                                                                                                       'tipo Poisson.',
 'Fano factor formula explanation': 'Fattore di Fano = varianza / media; un valore vicino a 1 è compatibile con un '
                                    'conteggio di tipo Poisson.',
 'Fano factor: {value}': 'Fattore di Fano: {value}',
 'Far above the usual local range': 'Molto sopra l’intervallo locale abituale',
 'File size': 'File size',
 'Firmware version': 'Versione firmware',
 'Flat': 'Flat',
 'Fleet intelligence': 'Analisi del gruppo di dispositivi',
 'Format': 'Formato',
 'Fri': 'Ven',
 'Friday': 'Venerdì',
 'Full history ZIP': 'ZIP cronologia completa',
 'GMC Radiation Monitor': 'Monitor radiazioni GMC',
 'GMC Radiation Monitoring': 'Monitoraggio delle radiazioni GMC',
 'GMC Reports': 'Rapport GMC',
 'GMC analysis report {period}': 'Rapporto di analisi GMC {period}',
 'GMC detected': 'GMC detected',
 'GMC devices are being detected automatically': 'GMC devices are being detected automatically',
 'GMC radiation analysis report': 'Rapporto di analisi delle radiazioni GMC',
 'GMC radiation monitoring report {period}': 'Rapporto di monitoraggio radiazioni GMC {period}',
 'GMC-300/320 family': 'Famiglia GMC-300/320',
 'GMC-320 and GMC-500+ combined': 'GMC-320 and GMC-500+ combined',
 'GMC-500 family': 'Famiglia GMC-500',
 'GMC-600 family': 'Famiglia GMC-600',
 'GMCMap consecutive upload errors': 'Errori consecutivi di invio GMCMap',
 'GMCMap counter ID': 'ID contatore GMCMap',
 'GMCMap is enabled, but this device has no counter ID mapping.': 'GMCMap è attivo, ma a questo dispositivo non è '
                                                                  'associato alcun ID contatore.',
 'GMCMap last HTTP status': 'Ultimo stato HTTP GMCMap',
 'GMCMap last error time': 'Ora dell’ultimo errore GMCMap',
 'GMCMap last server response': 'Ultima risposta del server GMCMap',
 'GMCMap last successful upload': 'Ultimo invio GMCMap riuscito',
 'GMCMap last upload attempt': 'Ultimo tentativo di invio GMCMap',
 'GMCMap last upload error': 'Ultimo errore di invio GMCMap',
 'GMCMap last uploaded CPM': 'Ultimo CPM inviato a GMCMap',
 'GMCMap next upload': 'Prossimo invio GMCMap',
 'GMCMap successful uploads since start': 'Invii GMCMap riusciti dall’avvio',
 'GMCMap upload errors since start': 'Errori di invio GMCMap dall’avvio',
 'GMCMap upload status': 'Stato invio GMCMap',
 'GQ manufacturer recommendation': 'Raccomandazione del produttore GQ',
 'Gaps are excluded from effective counting time': 'Gaps are excluded from effective counting time',
 'Generated export exceeds the {limit_mib} MiB safety limit': 'L’esportazione generata supera il limite di sicurezza '
                                                              'di {limit_mib} MiB.',
 'Generated maintenance export exceeds the 128 MiB safety limit': 'L’esportazione di manutenzione generata supera il '
                                                                  'limite di sicurezza di 128 MiB.',
 'Generated report exceeds the 64 MiB safety limit': 'Il rapporto generato supera il limite di sicurezza di 64 MiB',
 'Generic GQ GMC / RFC1201-compatible device': 'Dispositivo GQ GMC generico compatibile RFC1201',
 'Generic RFC1201-compatible device': 'Dispositivo generico compatibile RFC1201',
 'Global report settings': 'Impostazioni globali di rapporti ed esportazioni',
 'Good': 'Buona',
 'Green': 'Verde',
 'Gyro Calibrated {axis}': 'Gyro Calibrated {axis}',
 'Gyro Errors Since Start': 'Errori giroscopio dall’avvio',
 'Gyro Raw {axis}': 'Valore gyro grezzo {axis}',
 'Gyro X': 'Gyro X',
 'Gyro Y': 'Gyro Y',
 'Gyro Z': 'Gyro Z',
 'Gyro data will be included when available.': 'I dati del giroscopio saranno inclusi quando disponibili.',
 'Gyro errors': 'Errori del giroscopio',
 'Gyro recording is disabled.': 'La registrazione del giroscopio è disattivata.',
 'Gyroscope': 'Giroscopio',
 'Hardware model': 'Modello hardware',
 'Heartbeat Errors Since Start': 'Errori heartbeat dall’avvio',
 'Heartbeat mode': 'Modalità heartbeat',
 'Heartbeat rolling 60 s CPM': 'CPM mobili su 60 s dell’heartbeat',
 'Heatmap PNG': 'Mappa di calore PNG',
 'Heuristic statistical assessment; not a radiation-protection classification.': 'Valutazione statistica euristica; '
                                                                                 'non è una classificazione di '
                                                                                 'radioprotezione.',
 'High': 'Alta',
 'High relative increase': 'Forte aumento relativo',
 'High-dose Tube CPM': 'Tubo alta dose CPM',
 'High-dose tube': 'Tubo ad alta dose',
 'Highest stored 24 h value': 'Valore massimo memorizzato nelle 24 h',
 'Histogram PNG': 'Istogramma PNG',
 'Historical chart is still being formed': 'Il grafico storico è ancora in formazione',
 'Historical development': 'Andamento storico',
 'History': 'History',
 'History Write Errors Since Start': 'Errori di scrittura cronologia dall’avvio',
 'History deleted': 'History deleted',
 'History maintenance': 'Gestione cronologia',
 'History restore failed': 'Ripristino cronologia non riuscito',
 'History restore is disabled. Enable enable_restore in the app configuration and restart.': 'Il ripristino della '
                                                                                             'cronologia è '
                                                                                             'disattivato. Abilitare '
                                                                                             'enable_restore nella '
                                                                                             'configurazione e '
                                                                                             'riavviare.',
 'History restore is disabled. Enable “{setting}” in the app configuration and restart.': 'Il ripristino della '
                                                                                          'cronologia è disattivato. '
                                                                                          'Attiva “{setting}” nella '
                                                                                          'configurazione dell’app e '
                                                                                          'riavvia.',
 'History storage warning': 'History storage warning',
 'Home Assistant API client is not configured': 'Home Assistant API client is not configured',
 'Home Assistant Recorder entity patterns': 'Home Assistant Recorder entity patterns',
 'Home Assistant Recorder history cleared': 'Home Assistant Recorder history cleared',
 'Home Assistant host UART': 'Home Assistant host UART',
 'Home Assistant location': 'Posizione Home Assistant',
 'How are connected counters compared?': 'Come vengono confrontati i contatori collegati?',
 'How closely the observed spread resembles Poisson-like counting': 'Quanto la dispersione osservata assomiglia a un '
                                                                    'conteggio tipo Poisson',
 'How is data quality evaluated?': 'Come viene valutata la qualità dei dati?',
 'How is the background profile calculated?': 'Come viene calcolato il profilo di fondo?',
 'How is the pressure relationship assessed?': 'Come viene valutata la relazione con la pressione?',
 'However, the value is noticeably above the usual local background. Observe the trend.': 'Tuttavia il valore è '
                                                                                          'sensibilmente sopra il '
                                                                                          'fondo locale abituale. '
                                                                                          'Osserva la tendenza.',
 'ICRP reference projection': 'Proiezione di riferimento ICRP',
 'Inclination': 'Inclinazione',
 'Ingest diagnostics cleared': 'Ingest diagnostics cleared',
 'Inspecting backup…': 'Inspecting backup…',
 'Insufficient': 'Insufficiente',
 'Insufficient history for level-shift detection': 'Insufficient history for level-shift detection',
 'Insufficient paired daily values': 'Valori giornalieri confrontabili insufficienti',
 'Integrity': 'Integrità',
 'Intelligence': 'Intelligence',
 'Intelligent radiation analysis': 'Analisi intelligente delle radiazioni',
 'Internal database cleared': 'Internal database cleared',
 'Internal serial port': 'Internal serial port',
 'Interpret statistics with coverage in mind': 'Interpretare le statistiche tenendo conto della copertura',
 'Interpret these values together with coverage, device stability and the historical background.': 'Interpreta questi '
                                                                                                   'valori insieme '
                                                                                                   'alla copertura, '
                                                                                                   'alla stabilità del '
                                                                                                   'dispositivo e al '
                                                                                                   'fondo storico.',
 'Interpretation': 'Interpretazione',
 'Interval diagnostics': 'Diagnostica degli intervalli',
 'Invalid deletion confirmation': 'Invalid deletion confirmation',
 'Invalid device clock response': 'Risposta non valida dell’orologio del dispositivo',
 'Invalid request parameters': 'Parametri della richiesta non validi.',
 'Invalid serial configuration request': 'Invalid serial configuration request',
 'Keep both counters close together and similarly oriented when using the comparison as a reference.': 'Mantieni '
                                                                                                       'entrambi i '
                                                                                                       'contatori '
                                                                                                       'vicini e '
                                                                                                       'orientati in '
                                                                                                       'modo simile '
                                                                                                       'quando usi il '
                                                                                                       'confronto come '
                                                                                                       'riferimento.',
 'Known radio or Zigbee adapter': 'Known radio or Zigbee adapter',
 'Language': 'Lingua',
 'Last HTTP status': 'Ultimo stato HTTP',
 'Last Successful Measurement': 'Ultima misura riuscita',
 'Last attempt': 'Ultimo tentativo',
 'Last backup requested in this browser': 'Last backup requested in this browser',
 'Last sample age': 'Età dell’ultima misura',
 'Last server response': 'Ultima risposta del server',
 'Last successful storage': 'Last successful storage',
 'Last update': 'Ultimo aggiornamento',
 'Last upload': 'Ultimo invio',
 'Last upload error': 'Ultimo errore di invio',
 'Latest CPM': 'CPM attuali',
 'Latest CPM uncertainty': 'Latest CPM uncertainty',
 'Latest CPM vs 24 h distribution': 'Ultimo CPM rispetto alla distribuzione di 24 h',
 'Latest accepted value': 'Latest accepted value',
 'Latest dose rate': 'Tasso di dose attuale',
 'Latest measurement': 'Ultima misurazione',
 'Learned Radiation Baseline': 'Baseline radiazioni appresa',
 'Learned from local history': 'Appresa dallo storico locale',
 'Learned pressure coefficient': 'Coefficiente di pressione appreso',
 'Learning baseline': 'Apprendimento della baseline',
 'Learning basis': 'Base di apprendimento',
 'Learning progress': 'Avanzamento apprendimento',
 'Learning: not enough local history yet': 'Apprendimento: storico locale ancora insufficiente',
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
 'Less variable than Poisson expectation': 'Meno variabile dell’attesa di Poisson',
 'Likely device-specific deviation': 'Deviazione probabilmente specifica del dispositivo',
 'Limited': 'Limitata',
 'Live radiation CPS': 'CPS di radiazione in tempo reale',
 'Live system status': 'Live system status',
 'Local background analysis': 'Analisi del fondo locale',
 'Local background is still being learned': 'Il fondo locale è ancora in fase di apprendimento',
 'Local background model is available': 'Il modello del fondo locale è disponibile',
 'Local baseline': 'Baseline locale',
 'Local hour': 'Ora locale',
 'Local time [{timezone}]': 'Ora locale [{timezone}]',
 'Local timestamp': 'Timestamp locale',
 'Location data comes from the Home Assistant general settings and is not sent to an external geocoding service.': 'I '
                                                                                                                   'dati '
                                                                                                                   'sulla '
                                                                                                                   'posizione '
                                                                                                                   'provengono '
                                                                                                                   'dalle '
                                                                                                                   'impostazioni '
                                                                                                                   'generali '
                                                                                                                   'di '
                                                                                                                   'Home '
                                                                                                                   'Assistant '
                                                                                                                   'e '
                                                                                                                   'non '
                                                                                                                   'vengono '
                                                                                                                   'inviati '
                                                                                                                   'a '
                                                                                                                   'servizi '
                                                                                                                   'esterni '
                                                                                                                   'di '
                                                                                                                   'geocodifica.',
 'Location unavailable': 'Posizione non disponibile',
 'Long-term context': 'Contesto a lungo termine',
 'Long-term drift': 'Deriva a lungo termine',
 'Long-term relative factor available': 'Long-term relative factor available',
 'Long-term relative response': 'Long-term relative response',
 'Longest gap': 'Interruzione più lunga',
 'Longest gap [s]': 'Intervallo più lungo [s]',
 'Longest gap: {seconds} s': 'Intervallo più lungo: {seconds} s',
 'Low': 'Bassa',
 'Low-dose Tube CPM': 'Tubo bassa dose CPM',
 'Low-dose tube': 'Tubo a bassa dose',
 'Lowest stored 24 h value': 'Valore minimo memorizzato nelle 24 h',
 'Machine-readable statistics and event data': 'Statistiche e dati degli eventi leggibili da macchina',
 'Maximum': 'Massimo',
 'Maximum CPM': 'CPM massimo',
 'Maximum background index [%]': 'Indice di fondo massimo [%]',
 'Mean': 'Media',
 'Mean CPM': 'CPM medio',
 'Mean CPM by weekday and hour — {title}': 'CPM medio per giorno e ora — {title}',
 'Mean absolute difference': 'Differenza assoluta media',
 'Mean: {value} CPM': 'Media: {value} CPM',
 'Measurement interval': 'Intervallo di misura',
 'Measurement-site baseline': 'Baseline combinata del sito di misura',
 'Measurements': 'Measurements',
 'Measurements are sent to the public GMCMap service.': 'Le misurazioni vengono inviate al servizio pubblico GMCMap.',
 'Measurements to delete': 'Measurements to delete',
 'Median': 'Mediana',
 'Median CPM': 'CPM mediano',
 'Median: {value} CPM': 'Mediana: {value} CPM',
 'Medium': 'Media',
 'Merge a compatible SQLite backup into the current history. Existing rows are preserved or updated by device serial and UTC timestamp.': 'Unisce '
                                                                                                                                          'un '
                                                                                                                                          'backup '
                                                                                                                                          'SQLite '
                                                                                                                                          'compatibile '
                                                                                                                                          'alla '
                                                                                                                                          'cronologia '
                                                                                                                                          'corrente. '
                                                                                                                                          'Le '
                                                                                                                                          'righe '
                                                                                                                                          'esistenti '
                                                                                                                                          'vengono '
                                                                                                                                          'conservate '
                                                                                                                                          'o '
                                                                                                                                          'aggiornate '
                                                                                                                                          'per '
                                                                                                                                          'seriale '
                                                                                                                                          'del '
                                                                                                                                          'dispositivo '
                                                                                                                                          'e '
                                                                                                                                          'timestamp '
                                                                                                                                          'UTC.',
 'Merged {rows} measurement rows from schema {schema}.': 'Sono state unite {rows} righe di misura dallo schema '
                                                         '{schema}.',
 'Minimum / maximum: {minimum} / {maximum} CPM': 'Minimo / massimo: {minimum} / {maximum} CPM',
 'Minimum CPM': 'CPM minimo',
 'Mixed device profiles': 'Profili dispositivo misti',
 'Moderate linear relationship': 'Relazione lineare moderata',
 'Mon': 'Lun',
 'Monday': 'Lunedì',
 'More history is needed before the relative background indicator is classified.': 'Serve più cronologia prima di '
                                                                                   'classificare l’indicatore di fondo '
                                                                                   'relativo.',
 'More history is needed; approximately {count} additional measurements are required.': 'More history is needed; '
                                                                                        'approximately {count} '
                                                                                        'additional measurements are '
                                                                                        'required.',
 'More measurements are needed for this weekday and hour.': 'Sono necessarie più misure per questo giorno e questa '
                                                            'ora.',
 'More variable than Poisson expectation': 'Più variabile dell’attesa di Poisson',
 'Move away from the suspected source if safe to do so, avoid unnecessary exposure and seek qualified radiation-protection advice.': 'Allontanarsi '
                                                                                                                                     'dalla '
                                                                                                                                     'sorgente '
                                                                                                                                     'sospetta '
                                                                                                                                     'se '
                                                                                                                                     'è '
                                                                                                                                     'possibile '
                                                                                                                                     'farlo '
                                                                                                                                     'in '
                                                                                                                                     'sicurezza, '
                                                                                                                                     'evitare '
                                                                                                                                     'esposizioni '
                                                                                                                                     'non '
                                                                                                                                     'necessarie '
                                                                                                                                     'e '
                                                                                                                                     'richiedere '
                                                                                                                                     'una '
                                                                                                                                     'consulenza '
                                                                                                                                     'qualificata '
                                                                                                                                     'di '
                                                                                                                                     'radioprotezione.',
 'Never': 'Mai',
 'Newest sample': 'Campione più recente',
 'Next upload': 'Prossimo invio',
 'No GMC device detected': 'No GMC device detected',
 'No action is required while the result remains normal. Investigate persistent changes by checking the measurement location and comparing both devices.': 'Non '
                                                                                                                                                           'è '
                                                                                                                                                           'richiesta '
                                                                                                                                                           'alcuna '
                                                                                                                                                           'azione '
                                                                                                                                                           'finché '
                                                                                                                                                           'il '
                                                                                                                                                           'risultato '
                                                                                                                                                           'rimane '
                                                                                                                                                           'normale. '
                                                                                                                                                           'Esamina '
                                                                                                                                                           'i '
                                                                                                                                                           'cambiamenti '
                                                                                                                                                           'persistenti '
                                                                                                                                                           'controllando '
                                                                                                                                                           'il '
                                                                                                                                                           'luogo '
                                                                                                                                                           'di '
                                                                                                                                                           'misura '
                                                                                                                                                           'e '
                                                                                                                                                           'confrontando '
                                                                                                                                                           'entrambi '
                                                                                                                                                           'i '
                                                                                                                                                           'dispositivi.',
 'No action is required. Continue normal monitoring.': 'Non è richiesta alcuna azione. Continua il normale '
                                                       'monitoraggio.',
 'No action is required. The assessment becomes more reliable as additional measurements are collected.': 'Non è '
                                                                                                          'richiesta '
                                                                                                          'alcuna '
                                                                                                          'azione. La '
                                                                                                          'valutazione '
                                                                                                          'diventa più '
                                                                                                          'affidabile '
                                                                                                          'con la '
                                                                                                          'raccolta di '
                                                                                                          'ulteriori '
                                                                                                          'misure.',
 'No action required': 'Nessuna azione necessaria',
 'No active device warnings': 'No active device warnings',
 'No connected GMC device': 'No connected GMC device',
 'No connected counter is available yet. The next serial scan runs automatically.': 'No connected counter is available '
                                                                                    'yet. The next serial scan runs '
                                                                                    'automatically.',
 'No connected devices.': 'Nessun dispositivo collegato.',
 'No current pressure source is available': 'Nessuna fonte di pressione attuale disponibile',
 'No data': 'Nessun dato',
 'No known GMC devices': 'No known GMC devices',
 'No matching Home Assistant entities': 'No matching Home Assistant entities',
 'No measurement yet': 'Nessuna misurazione disponibile',
 'No measurements in selected period': 'Nessuna misura nel periodo selezionato',
 'No measurements yet.': 'Nessuna misurazione disponibile.',
 'No persistent level shift detected': 'No persistent level shift detected',
 'No position changes recorded.': 'Nessun cambio di posizione registrato.',
 'No pressure variation': 'Variazione di pressione insufficiente',
 'No pressure-typical signature': 'Nessuna firma tipica della pressione',
 'No pronounced baseline jumps detected.': 'Nessun salto pronunciato della baseline rilevato.',
 'No reports have been requested in this browser yet.': 'No reports have been requested in this browser yet.',
 'No shared rise detected.': 'Nessun aumento comune rilevato.',
 'No stored measurements': 'No stored measurements',
 'No suitable serial device was found.': 'No suitable serial device was found.',
 'No sustained relative anomaly events detected': 'Nessun evento persistente di anomalia relativa rilevato',
 'No valid CPM baseline': 'Nessuna baseline CPM valida',
 'Normal': 'Normale',
 'Normal for this time': 'Normale per questo orario',
 'Normal: within the usual local range': 'Normale: nell’intervallo locale abituale',
 'Not available yet — at least two CPM samples are required': 'Non ancora disponibile — sono necessarie almeno due '
                                                              'misure CPM',
 'Not available yet — more baseline history is required': 'Non ancora disponibile — serve più storico della baseline',
 'Not available yet — more paired samples are required': 'Non ancora disponibile — servono più coppie di misure',
 'Not available yet — no temperature samples were stored in the current 24 h window.': 'Non ancora disponibile — nella '
                                                                                       'finestra corrente di 24 h non '
                                                                                       'sono state memorizzate misure '
                                                                                       'di temperatura.',
 'Not available yet — the 24 h CPM series needs variation and at least two samples': 'Non ancora disponibile — la '
                                                                                     'serie CPM di 24 h deve variare e '
                                                                                     'contenere almeno due misure',
 'Not available yet — the 24 h mean and spread are still insufficient': 'Non ancora disponibile — media e dispersione '
                                                                        'di 24 h sono ancora insufficienti',
 'Not available — CPM did not vary during this period': 'Non disponibile — i CPM non sono variati durante questo '
                                                        'periodo',
 'Not available — the sensor value did not vary during this period': 'Non disponibile — il valore del sensore non è '
                                                                     'variato durante questo periodo',
 'Not configured': 'Non configurato',
 'Not connected': 'Not connected',
 'Not detected yet': 'Non ancora rilevato',
 'Not enough local history yet': 'Storico locale ancora insufficiente',
 'Not found': 'Non trovato',
 'Not recorded in this browser': 'Not recorded in this browser',
 'Not suitable as a GMC device': 'Not suitable as a GMC device',
 'Not suitable for GMC': 'Not suitable for GMC',
 'Not yet checked as a GMC device': 'Not yet checked as a GMC device',
 'Noticeable': 'Anomalo',
 'Noticeable baseline drift': 'Deriva della baseline evidente',
 'Noticeable difference from Poisson-like spread': 'Differenza evidente rispetto a una dispersione tipo Poisson',
 'Noticeable statistical deviation': 'Deviazione statistica evidente',
 'Noticeable: above the usual local range': 'Anomalo: sopra l’intervallo locale abituale',
 'Number of samples': 'Numero di campioni',
 'Observed': 'Osservato',
 'Observed SD / √mean': 'DS osservata / √media',
 'Official reference values': 'Valori di riferimento ufficiali',
 'Offline': 'Non in linea',
 'Oldest sample': 'Campione più vecchio',
 'One current weather entity is available': 'È disponibile un’entità meteo attuale',
 'One-hour mean is {deviation:+.1f}% relative to the learned baseline': 'La media di un’ora è {deviation:+.1f}% '
                                                                        'rispetto alla baseline appresa',
 'One-hour means': 'Medie di un’ora',
 'One-hour robust level is {deviation:+.1f}% relative to the device baseline': 'Il livello robusto di un’ora è '
                                                                               '{deviation:+.1f}% rispetto alla '
                                                                               'baseline del dispositivo',
 'Online': 'In linea',
 'Only quality-filtered, one-to-one time-matched measurements are compared. Agreement, correlation, relative bias and stability are evaluated separately so one faulty counter does not automatically define the site result.': 'Vengono '
                                                                                                                                                                                                                                'confrontate '
                                                                                                                                                                                                                                'solo '
                                                                                                                                                                                                                                'misure '
                                                                                                                                                                                                                                'filtrate '
                                                                                                                                                                                                                                'per '
                                                                                                                                                                                                                                'qualità '
                                                                                                                                                                                                                                'e '
                                                                                                                                                                                                                                'abbinate '
                                                                                                                                                                                                                                'una '
                                                                                                                                                                                                                                'a '
                                                                                                                                                                                                                                'una '
                                                                                                                                                                                                                                'nel '
                                                                                                                                                                                                                                'tempo. '
                                                                                                                                                                                                                                'Concordanza, '
                                                                                                                                                                                                                                'correlazione, '
                                                                                                                                                                                                                                'scostamento '
                                                                                                                                                                                                                                'relativo '
                                                                                                                                                                                                                                'e '
                                                                                                                                                                                                                                'stabilità '
                                                                                                                                                                                                                                'vengono '
                                                                                                                                                                                                                                'valutati '
                                                                                                                                                                                                                                'separatamente, '
                                                                                                                                                                                                                                'così '
                                                                                                                                                                                                                                'un '
                                                                                                                                                                                                                                'contatore '
                                                                                                                                                                                                                                'difettoso '
                                                                                                                                                                                                                                'non '
                                                                                                                                                                                                                                'determina '
                                                                                                                                                                                                                                'automaticamente '
                                                                                                                                                                                                                                'il '
                                                                                                                                                                                                                                'risultato '
                                                                                                                                                                                                                                'del '
                                                                                                                                                                                                                                'sito.',
 'Only the most important conclusions at a glance': 'Solo le conclusioni più importanti a colpo d’occhio',
 'Open': 'Open',
 'Open serial device connections': 'Open serial device connections',
 'Operational events cleared': 'Operational events cleared',
 'Orientation cannot be verified automatically': 'Orientation cannot be verified automatically',
 'Orientation changes detected': 'Orientation changes detected',
 'Orientation data is temporarily unavailable.': 'I dati di orientamento sono temporaneamente non disponibili.',
 'Orientation qualification': 'Orientation qualification',
 'Orientation stable': 'Orientation stable',
 'Original raw-data CSV': 'Original raw-data CSV',
 'Outliers and invalid measurements': 'Valori anomali e misure non valide',
 'Overview': 'Panoramica',
 'P95 CPM': 'CPM P95',
 'P95: {value} CPM': 'P95: {value} CPM',
 'P99 CPM': 'CPM P99',
 'P99: {value} CPM': 'P99: {value} CPM',
 'PDF report': 'Rapporto PDF',
 'Pair-level disagreement': 'Disaccordo a livello di coppia',
 'Pearson r · n={count} paired samples': 'r di Pearson · n={count} coppie di misure',
 'Period: {period} ({timezone})': 'Periodo: {period} ({timezone})',
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
 'Pitch angle': 'Angolo di beccheggio',
 'Plausibilised from two weather entities': 'Plausibilizzato da due entità meteo',
 'Poisson SD ratio': 'Rapporto DS di Poisson',
 'Poisson SD ratio = observed standard deviation / √mean; a value near 1 indicates Poisson-like spread.': 'Rapporto DS '
                                                                                                          'di Poisson '
                                                                                                          '= '
                                                                                                          'deviazione '
                                                                                                          'standard '
                                                                                                          'osservata / '
                                                                                                          '√media; un '
                                                                                                          'valore '
                                                                                                          'vicino a 1 '
                                                                                                          'indica una '
                                                                                                          'dispersione '
                                                                                                          'di tipo '
                                                                                                          'Poisson.',
 'Poisson SD ratio formula explanation': 'Rapporto DS di Poisson = deviazione standard osservata / √media; un valore '
                                         'vicino a 1 indica una dispersione di tipo Poisson.',
 'Poisson SD ratio: {value}': 'Rapporto DS di Poisson: {value}',
 'Poisson counting interval from the observed impulse count': 'Poisson counting interval from the observed impulse '
                                                              'count',
 'Poisson expectation (λ={mean:.2f})': 'Attesa di Poisson (λ={mean:.2f})',
 'Poor': 'Scarsa',
 'Position change log': 'Registro dei cambi di posizione',
 'Possible GMC connection cable': 'Possible GMC connection cable',
 'Possible persistent level shift': 'Possible persistent level shift',
 'Pressure model is still being formed': 'Il modello di pressione è ancora in formazione',
 'Pressure model unavailable': 'Modello di pressione non disponibile',
 'Pressure-typical signature is pronounced': 'Firma tipica della pressione marcata',
 'Preview backup': 'Preview backup',
 'Previous day': 'Giorno precedente',
 'Previous week': 'Settimana precedente',
 'Probable real change': 'Probabile cambiamento reale',
 'Probable shared measurement-site change': 'Probabile variazione comune del sito di misura',
 'Profile': 'Profilo dispositivo',
 'Profile is still being formed': 'Il profilo è ancora in formazione',
 'Provider': 'Fornitore',
 'Public GMCMap upload': 'Invio pubblico a GMCMap',
 'Quality weight': 'Peso di qualità',
 'Quality-filtered correlation': 'Correlazione filtrata per qualità',
 'Quality-filtered measurement CSV': 'Quality-filtered measurement CSV',
 'Quick downloads': 'Download rapidi',
 'Radiation 1 h Mean': 'Media radiazioni 1 h',
 'Radiation 1 h Median': 'Mediana radiazioni 1 h',
 'Radiation 1 h Standard Deviation': 'Deviazione standard radiazioni 1 h',
 'Radiation Baseline Deviation': 'Deviazione baseline radiazioni',
 'Radiation CPM': 'Radiazioni CPM',
 'Radiation Rapid Change': 'Variazione rapida radiazioni',
 'Radiation count rate [CPM]': 'Tasso di conteggio radiazioni [CPM]',
 'Radiation counts fluctuate naturally. The Fano factor and Poisson spread ratio compare the observed variation with a simple counting-statistics model; they describe distribution shape but not a physical cause or calibration state.': 'I '
                                                                                                                                                                                                                                           'conteggi '
                                                                                                                                                                                                                                           'di '
                                                                                                                                                                                                                                           'radiazione '
                                                                                                                                                                                                                                           'variano '
                                                                                                                                                                                                                                           'naturalmente. '
                                                                                                                                                                                                                                           'Il '
                                                                                                                                                                                                                                           'fattore '
                                                                                                                                                                                                                                           'di '
                                                                                                                                                                                                                                           'Fano '
                                                                                                                                                                                                                                           'e '
                                                                                                                                                                                                                                           'il '
                                                                                                                                                                                                                                           'rapporto '
                                                                                                                                                                                                                                           'di '
                                                                                                                                                                                                                                           'dispersione '
                                                                                                                                                                                                                                           'di '
                                                                                                                                                                                                                                           'Poisson '
                                                                                                                                                                                                                                           'confrontano '
                                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                                           'variazione '
                                                                                                                                                                                                                                           'osservata '
                                                                                                                                                                                                                                           'con '
                                                                                                                                                                                                                                           'un '
                                                                                                                                                                                                                                           'semplice '
                                                                                                                                                                                                                                           'modello '
                                                                                                                                                                                                                                           'statistico '
                                                                                                                                                                                                                                           'di '
                                                                                                                                                                                                                                           'conteggio; '
                                                                                                                                                                                                                                           'descrivono '
                                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                                           'forma '
                                                                                                                                                                                                                                           'della '
                                                                                                                                                                                                                                           'distribuzione, '
                                                                                                                                                                                                                                           'ma '
                                                                                                                                                                                                                                           'non '
                                                                                                                                                                                                                                           'una '
                                                                                                                                                                                                                                           'causa '
                                                                                                                                                                                                                                           'fisica '
                                                                                                                                                                                                                                           'né '
                                                                                                                                                                                                                                           'lo '
                                                                                                                                                                                                                                           'stato '
                                                                                                                                                                                                                                           'di '
                                                                                                                                                                                                                                           'calibrazione.',
 'Radiation measurement continues unless the device status says otherwise.': 'La misurazione della radiazione '
                                                                             'continua, salvo diversa indicazione '
                                                                             'dello stato del dispositivo.',
 'Radiation measurement continues. An external Home Assistant temperature may be used when configured.': 'La '
                                                                                                         'misurazione '
                                                                                                         'della '
                                                                                                         'radiazione '
                                                                                                         'continua. Se '
                                                                                                         'configurata, '
                                                                                                         'può essere '
                                                                                                         'usata una '
                                                                                                         'temperatura '
                                                                                                         'esterna di '
                                                                                                         'Home '
                                                                                                         'Assistant.',
 'Radiation measurement continues; only the optional orientation value is affected.': 'La misurazione della radiazione '
                                                                                      'continua; è interessato solo il '
                                                                                      'valore di orientamento '
                                                                                      'opzionale.',
 'Radiation monitoring analysis': 'Analisi del monitoraggio radiazioni',
 'Radiation traffic light': 'Semaforo radiazioni',
 'Radiation traffic light hysteresis explanation': 'Il semaforo usa l’isteresi: entra in giallo al {yellow_enter:g}% e '
                                                   'rientra sotto il {yellow_clear:g}%; entra in rosso al '
                                                   '{red_enter:g}% e rientra sotto il {red_clear:g}%.',
 'Radiation traffic light uses hysteresis: it enters yellow at {yellow_enter:g}% and clears below {yellow_clear:g}%; it enters red at {red_enter:g}% and clears below {red_clear:g}%.': 'Il '
                                                                                                                                                                                        'semaforo '
                                                                                                                                                                                        'usa '
                                                                                                                                                                                        'l’isteresi: '
                                                                                                                                                                                        'entra '
                                                                                                                                                                                        'in '
                                                                                                                                                                                        'giallo '
                                                                                                                                                                                        'al '
                                                                                                                                                                                        '{yellow_enter:g}% '
                                                                                                                                                                                        'e '
                                                                                                                                                                                        'rientra '
                                                                                                                                                                                        'sotto '
                                                                                                                                                                                        'il '
                                                                                                                                                                                        '{yellow_clear:g}%; '
                                                                                                                                                                                        'entra '
                                                                                                                                                                                        'in '
                                                                                                                                                                                        'rosso '
                                                                                                                                                                                        'al '
                                                                                                                                                                                        '{red_enter:g}% '
                                                                                                                                                                                        'e '
                                                                                                                                                                                        'rientra '
                                                                                                                                                                                        'sotto '
                                                                                                                                                                                        'il '
                                                                                                                                                                                        '{red_clear:g}%.',
 'Raw CSV': 'CSV grezzo',
 'Raw device values are stored separately before quality filtering': 'Raw device values are stored separately before '
                                                                     'quality filtering',
 'Raw gyro [signed int16]': 'Gyro grezzo [int16 con segno]',
 'Raw-data archive': 'Raw-data archive',
 'Read-only mode': 'Read-only mode',
 'Ready for new measurements': 'Ready for new measurements',
 'Recent 30 days compared with the preceding 30 days': 'Ultimi 30 giorni confrontati con i 30 precedenti',
 'Recent data quality is high': 'La qualità dei dati recenti è elevata',
 'Recent period compared with the preceding period': 'Periodo recente confrontato con quello precedente',
 'Recent quality-filtered data quality is high': 'La qualità recente dei dati filtrati è elevata',
 'Recent reports': 'Recent reports',
 'Recommendation': 'Raccomandazione',
 'Recommended': 'Recommended',
 'Reconnects': 'Riconnessioni',
 'Red': 'Rosso',
 'Reduced': 'Ridotta',
 'Refreshing device status…': 'Refreshing device status…',
 'Relative anomaly indicator only; not a safety classification.': 'Solo indicatore di anomalia relativa; non è una '
                                                                  'classificazione di sicurezza.',
 'Relative correction factor': 'Relative correction factor',
 'Relative spread': 'Relative spread',
 'Relative to 7 d baseline': 'Rispetto alla baseline di 7 g',
 'Relative-factor confidence': 'Relative-factor confidence',
 'Remaining deviation': 'Deviazione residua',
 'Remove': 'Remove',
 'Report': 'Report',
 'Report generation failed': 'Generazione rapporto non riuscita',
 'Report target': 'Dispositivi del rapporto',
 'Reports': 'Reports',
 'Reports for the displayed analysis': 'Reports for the displayed analysis',
 'Rescan devices': 'Rescan devices',
 'Resolve persistent connection gaps before relying on long-term comparisons.': 'Risolvi le interruzioni persistenti '
                                                                                'della connessione prima di fare '
                                                                                'affidamento sui confronti a lungo '
                                                                                'termine.',
 'Restore backup': 'Ripristina backup',
 'Restore complete': 'Ripristino completato',
 'Restore confirmation text must be exactly RESTORE': 'Il testo di conferma deve essere esattamente RESTORE',
 'Restore history': 'Ripristina cronologia',
 'Restore is disabled by default.': 'Il ripristino è disattivato per impostazione predefinita.',
 'Restore upload must be between 1 byte and 128 MiB': 'Il file di ripristino deve essere compreso tra 1 byte e 128 MiB',
 'Return to GMC Radiation Monitoring': 'Torna al monitoraggio delle radiazioni GMC',
 'Return to GMC Reports': 'Torna ai rapporti GMC',
 'Review the event export for timing and severity': 'Controllare l’esportazione degli eventi per orario e gravità',
 'Review the recent trend and event timing. Check both counters and the measurement location if the change persists.': 'Esamina '
                                                                                                                       'la '
                                                                                                                       'tendenza '
                                                                                                                       'recente '
                                                                                                                       'e '
                                                                                                                       'l’orario '
                                                                                                                       'degli '
                                                                                                                       'eventi. '
                                                                                                                       'Controlla '
                                                                                                                       'entrambi '
                                                                                                                       'i '
                                                                                                                       'contatori '
                                                                                                                       'e '
                                                                                                                       'il '
                                                                                                                       'luogo '
                                                                                                                       'di '
                                                                                                                       'misura '
                                                                                                                       'se '
                                                                                                                       'il '
                                                                                                                       'cambiamento '
                                                                                                                       'persiste.',
 'Rising': 'In aumento',
 'Robust medians are used; rejected measurements and isolated spikes do not immediately change the profile.': 'Vengono '
                                                                                                              'usate '
                                                                                                              'mediane '
                                                                                                              'robuste; '
                                                                                                              'le '
                                                                                                              'misure '
                                                                                                              'rifiutate '
                                                                                                              'e i '
                                                                                                              'picchi '
                                                                                                              'isolati '
                                                                                                              'non '
                                                                                                              'modificano '
                                                                                                              'subito '
                                                                                                              'il '
                                                                                                              'profilo.',
 'Robust one-hour values': 'Valori robusti di un’ora',
 'Roll angle': 'Angolo di rollio',
 'Rolling windows end at the latest stored measurement. Dose-rate values are derived from CPM using the configured factor and are not independently measured. CPM remains the primary measurement. The traffic light is a relative background-anomaly indicator, not an emergency, health, or radiation-safety classification.': 'Le '
                                                                                                                                                                                                                                                                                                                                 'finestre '
                                                                                                                                                                                                                                                                                                                                 'mobili '
                                                                                                                                                                                                                                                                                                                                 'terminano '
                                                                                                                                                                                                                                                                                                                                 'all’ultima '
                                                                                                                                                                                                                                                                                                                                 'misura '
                                                                                                                                                                                                                                                                                                                                 'memorizzata. '
                                                                                                                                                                                                                                                                                                                                 'I '
                                                                                                                                                                                                                                                                                                                                 'ratei '
                                                                                                                                                                                                                                                                                                                                 'di '
                                                                                                                                                                                                                                                                                                                                 'dose '
                                                                                                                                                                                                                                                                                                                                 'sono '
                                                                                                                                                                                                                                                                                                                                 'derivati '
                                                                                                                                                                                                                                                                                                                                 'dai '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'con '
                                                                                                                                                                                                                                                                                                                                 'il '
                                                                                                                                                                                                                                                                                                                                 'fattore '
                                                                                                                                                                                                                                                                                                                                 'configurato '
                                                                                                                                                                                                                                                                                                                                 'e '
                                                                                                                                                                                                                                                                                                                                 'non '
                                                                                                                                                                                                                                                                                                                                 'sono '
                                                                                                                                                                                                                                                                                                                                 'misurati '
                                                                                                                                                                                                                                                                                                                                 'indipendentemente. '
                                                                                                                                                                                                                                                                                                                                 'I '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'restano '
                                                                                                                                                                                                                                                                                                                                 'la '
                                                                                                                                                                                                                                                                                                                                 'misura '
                                                                                                                                                                                                                                                                                                                                 'primaria. '
                                                                                                                                                                                                                                                                                                                                 'Il '
                                                                                                                                                                                                                                                                                                                                 'semaforo '
                                                                                                                                                                                                                                                                                                                                 'indica '
                                                                                                                                                                                                                                                                                                                                 'un’anomalia '
                                                                                                                                                                                                                                                                                                                                 'relativa '
                                                                                                                                                                                                                                                                                                                                 'del '
                                                                                                                                                                                                                                                                                                                                 'fondo, '
                                                                                                                                                                                                                                                                                                                                 'non '
                                                                                                                                                                                                                                                                                                                                 'una '
                                                                                                                                                                                                                                                                                                                                 'classificazione '
                                                                                                                                                                                                                                                                                                                                 'di '
                                                                                                                                                                                                                                                                                                                                 'emergenza, '
                                                                                                                                                                                                                                                                                                                                 'sanitaria '
                                                                                                                                                                                                                                                                                                                                 'o '
                                                                                                                                                                                                                                                                                                                                 'di '
                                                                                                                                                                                                                                                                                                                                 'radioprotezione.',
 'SD: {value} CPM': 'DS: {value} CPM',
 'SQLite backup': 'Backup SQLite',
 'SQLite backup file': 'SQLite backup file',
 'SQLite database vacuum completed': 'SQLite database vacuum completed',
 'Sample standard deviation': 'Deviazione standard campionaria',
 'Samples': 'Campioni',
 'Samples: {samples} / {expected}': 'Campioni: {samples} / {expected}',
 'Sampling interval: {interval} s | Samples: {samples}/{expected} | Completeness: {completeness:.2f}% | Generated: {generated} | App {version}': 'Intervallo: '
                                                                                                                                                 '{interval} '
                                                                                                                                                 's '
                                                                                                                                                 '| '
                                                                                                                                                 'Campioni: '
                                                                                                                                                 '{samples}/{expected} '
                                                                                                                                                 '| '
                                                                                                                                                 'Completezza: '
                                                                                                                                                 '{completeness:.2f}% '
                                                                                                                                                 '| '
                                                                                                                                                 'Generato: '
                                                                                                                                                 '{generated} '
                                                                                                                                                 '| '
                                                                                                                                                 'App '
                                                                                                                                                 '{version}',
 'Sampling interval: {seconds} s': 'Intervallo di campionamento: {seconds} s',
 'Sat': 'Sab',
 'Saturday': 'Sabato',
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
 'Second half vs first half of available 7 d window': 'Seconda metà rispetto alla prima metà della finestra '
                                                      'disponibile di 7 g',
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
 'Serial': 'Numero di serie',
 'Serial Errors Since Start': 'Errori seriali dall’avvio',
 'Serial Reconnects Since Start': 'Riconnessioni seriali dall’avvio',
 'Serial USB device': 'Serial USB device',
 'Serial connection recovered': 'Serial connection recovered',
 'Serial device connections': 'Serial device connections',
 'Serial errors / reconnects': 'Errori seriali / riconnessioni',
 'Serial port': 'Porta seriale',
 'Serial: {serial} | Period: {period} | Timezone: {timezone}': 'Seriale: {serial} | Periodo: {period} | Fuso orario: '
                                                               '{timezone}',
 'Serial: {value}': 'Seriale: {value}',
 'Severity': 'Gravità',
 'Shared CPM rise': 'Aumento comune dei CPM',
 'Shared event detector': 'Rilevatore di eventi comuni',
 'Show analysis': 'Mostra analisi',
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
 'Simple': 'Semplice',
 'Since app start': 'Dall’avvio dell’applicazione',
 'Slightly noticeable': 'Leggermente anomalo',
 'Slightly tilted': 'Slightly tilted',
 'Small baseline drift': 'Piccola deriva della baseline',
 'Smart Alert State': 'Stato allarme intelligente',
 'Smoothed historical background trend': 'Andamento storico smussato del fondo',
 'Source validation': 'Convalida delle fonti',
 'Specific ISO week': 'Settimana ISO specifica',
 'Specific date': 'Data specifica',
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
 'Stability and device health': 'Stabilità e stato del dispositivo',
 'Stable': 'Stabile',
 'Stable device path': 'Stable device path',
 'Stable devices': 'Dispositivi stabili',
 'Standard deviation CPM': 'Deviazione standard CPM',
 'Start time UTC': 'Ora inizio UTC',
 'Start time local': 'Ora inizio locale',
 'Start with a readable PDF or a complete ZIP bundle. Raw and specialist formats remain available below without crowding the main view.': 'Inizia '
                                                                                                                                          'con '
                                                                                                                                          'un '
                                                                                                                                          'PDF '
                                                                                                                                          'leggibile '
                                                                                                                                          'o '
                                                                                                                                          'un '
                                                                                                                                          'pacchetto '
                                                                                                                                          'ZIP '
                                                                                                                                          'completo. '
                                                                                                                                          'I '
                                                                                                                                          'formati '
                                                                                                                                          'grezzi '
                                                                                                                                          'e '
                                                                                                                                          'specialistici '
                                                                                                                                          'restano '
                                                                                                                                          'disponibili '
                                                                                                                                          'più '
                                                                                                                                          'sotto '
                                                                                                                                          'senza '
                                                                                                                                          'affollare '
                                                                                                                                          'la '
                                                                                                                                          'vista '
                                                                                                                                          'principale.',
 'Statistical indication only': 'Solo indicazione statistica',
 'Statistical level shift': 'Statistical level shift',
 'Statistically noticeable': 'Statisticamente rilevante',
 'Statistics': 'Statistiche',
 'Stored samples': 'Campioni memorizzati',
 'Stored samples across all devices': 'Misurazioni memorizzate di tutti i dispositivi',
 'Stored samples for this device': 'Misurazioni memorizzate per questo dispositivo',
 'Strong common signal': 'Forte segnale comune',
 'Strong linear relationship': 'Relazione lineare forte',
 'Strong statistical deviation': 'Forte deviazione statistica',
 'Successful uploads': 'Invii riusciti',
 'Successful uploads since start': 'Invii riusciti dall’avvio',
 'Suitable for most trend analysis': 'Adatto alla maggior parte delle analisi di tendenza',
 'Summary': 'Riepilogo',
 'Sun': 'Dom',
 'Sunday': 'Domenica',
 'Supervisor API access is unavailable': 'Supervisor API access is unavailable',
 'Supply voltage [V]': 'Tensione di alimentazione [V]',
 'Suspicious CPM value is being verified': 'Suspicious CPM value is being verified',
 'Sustained Radiation Alert': 'Allarme radiazioni persistente',
 'Sustained relative anomaly events': 'Eventi persistenti di anomalia relativa',
 'Sustained yellow/red relative anomaly events': 'Eventi persistenti di anomalia relativa gialla/rossa',
 'Temperature': 'Temperatura',
 'Temperature / voltage errors': 'Errori di temperatura / tensione',
 'Temperature Errors Since Start': 'Errori temperatura dall’avvio',
 'Temperature [°C]': 'Temperatura [°C]',
 'Temperature and voltage relationships': 'Relazioni con temperatura e tensione',
 'Temperature bins (24 h)': 'Classi di temperatura (24 h)',
 'Temperature correlation': 'Correlazione temperatura',
 'Temperature profile is still being formed': 'Il profilo di temperatura è ancora in formazione',
 'Temperature trend': 'Andamento della temperatura',
 'Temperature-specific background': 'Fondo specifico per temperatura',
 'The Supervisor options could not be loaded: {error}': 'The Supervisor options could not be loaded: {error}',
 'The absolute assessment starts after the first measurement.': 'La valutazione assoluta inizia dopo la prima '
                                                                'misurazione.',
 'The absolute level is below the configured warning threshold, but the value is far above the learned local background.': 'Il '
                                                                                                                           'livello '
                                                                                                                           'assoluto '
                                                                                                                           'è '
                                                                                                                           'inferiore '
                                                                                                                           'alla '
                                                                                                                           'soglia '
                                                                                                                           'di '
                                                                                                                           'avviso '
                                                                                                                           'configurata, '
                                                                                                                           'ma '
                                                                                                                           'il '
                                                                                                                           'valore '
                                                                                                                           'è '
                                                                                                                           'molto '
                                                                                                                           'superiore '
                                                                                                                           'al '
                                                                                                                           'fondo '
                                                                                                                           'locale '
                                                                                                                           'appreso.',
 'The absolute level is currently uncritical, but the local comparison or short-term trend deserves continued observation.': 'Il '
                                                                                                                             'livello '
                                                                                                                             'assoluto '
                                                                                                                             'non '
                                                                                                                             'è '
                                                                                                                             'attualmente '
                                                                                                                             'critico, '
                                                                                                                             'ma '
                                                                                                                             'il '
                                                                                                                             'confronto '
                                                                                                                             'locale '
                                                                                                                             'o '
                                                                                                                             'la '
                                                                                                                             'tendenza '
                                                                                                                             'a '
                                                                                                                             'breve '
                                                                                                                             'termine '
                                                                                                                             'richiede '
                                                                                                                             'ulteriore '
                                                                                                                             'osservazione.',
 'The absolute level is currently uncritical. More local history is required before anomaly detection becomes reliable.': 'Il '
                                                                                                                          'livello '
                                                                                                                          'assoluto '
                                                                                                                          'non '
                                                                                                                          'è '
                                                                                                                          'attualmente '
                                                                                                                          'critico. '
                                                                                                                          'È '
                                                                                                                          'necessario '
                                                                                                                          'più '
                                                                                                                          'storico '
                                                                                                                          'locale '
                                                                                                                          'prima '
                                                                                                                          'che '
                                                                                                                          'il '
                                                                                                                          'rilevamento '
                                                                                                                          'delle '
                                                                                                                          'anomalie '
                                                                                                                          'sia '
                                                                                                                          'affidabile.',
 'The add-on is restarting so the new serial assignments become active.': 'The add-on is restarting so the new serial '
                                                                          'assignments become active.',
 'The app combines the recent trend, robust statistics, agreement between connected counters and the learned local background. The result is a statistical aid and does not identify a physical cause.': 'L’app '
                                                                                                                                                                                                         'combina '
                                                                                                                                                                                                         'la '
                                                                                                                                                                                                         'tendenza '
                                                                                                                                                                                                         'recente, '
                                                                                                                                                                                                         'statistiche '
                                                                                                                                                                                                         'robuste, '
                                                                                                                                                                                                         'la '
                                                                                                                                                                                                         'concordanza '
                                                                                                                                                                                                         'tra '
                                                                                                                                                                                                         'i '
                                                                                                                                                                                                         'contatori '
                                                                                                                                                                                                         'collegati '
                                                                                                                                                                                                         'e '
                                                                                                                                                                                                         'il '
                                                                                                                                                                                                         'fondo '
                                                                                                                                                                                                         'locale '
                                                                                                                                                                                                         'appreso. '
                                                                                                                                                                                                         'Il '
                                                                                                                                                                                                         'risultato '
                                                                                                                                                                                                         'è '
                                                                                                                                                                                                         'un '
                                                                                                                                                                                                         'supporto '
                                                                                                                                                                                                         'statistico '
                                                                                                                                                                                                         'e '
                                                                                                                                                                                                         'non '
                                                                                                                                                                                                         'identifica '
                                                                                                                                                                                                         'una '
                                                                                                                                                                                                         'causa '
                                                                                                                                                                                                         'fisica.',
 'The app compares quality-filtered measurements from the same weekday and hour. Robust medians reduce the influence of isolated spikes and regular daily patterns are kept separate from unusual changes.': 'L’app '
                                                                                                                                                                                                             'confronta '
                                                                                                                                                                                                             'misure '
                                                                                                                                                                                                             'filtrate '
                                                                                                                                                                                                             'per '
                                                                                                                                                                                                             'qualità '
                                                                                                                                                                                                             'dello '
                                                                                                                                                                                                             'stesso '
                                                                                                                                                                                                             'giorno '
                                                                                                                                                                                                             'della '
                                                                                                                                                                                                             'settimana '
                                                                                                                                                                                                             'e '
                                                                                                                                                                                                             'della '
                                                                                                                                                                                                             'stessa '
                                                                                                                                                                                                             'ora. '
                                                                                                                                                                                                             'Le '
                                                                                                                                                                                                             'mediane '
                                                                                                                                                                                                             'robuste '
                                                                                                                                                                                                             'riducono '
                                                                                                                                                                                                             'l’influenza '
                                                                                                                                                                                                             'dei '
                                                                                                                                                                                                             'picchi '
                                                                                                                                                                                                             'isolati '
                                                                                                                                                                                                             'e '
                                                                                                                                                                                                             'i '
                                                                                                                                                                                                             'normali '
                                                                                                                                                                                                             'andamenti '
                                                                                                                                                                                                             'giornalieri '
                                                                                                                                                                                                             'vengono '
                                                                                                                                                                                                             'separati '
                                                                                                                                                                                                             'dai '
                                                                                                                                                                                                             'cambiamenti '
                                                                                                                                                                                                             'insoliti.',
 'The app compares quality-filtered radiation measurements with available air-pressure data. A statistical relationship can support interpretation, but correlation alone does not prove a cosmic or environmental cause.': 'L’app '
                                                                                                                                                                                                                            'confronta '
                                                                                                                                                                                                                            'le '
                                                                                                                                                                                                                            'misure '
                                                                                                                                                                                                                            'di '
                                                                                                                                                                                                                            'radiazione '
                                                                                                                                                                                                                            'filtrate '
                                                                                                                                                                                                                            'per '
                                                                                                                                                                                                                            'qualità '
                                                                                                                                                                                                                            'con '
                                                                                                                                                                                                                            'i '
                                                                                                                                                                                                                            'dati '
                                                                                                                                                                                                                            'disponibili '
                                                                                                                                                                                                                            'sulla '
                                                                                                                                                                                                                            'pressione '
                                                                                                                                                                                                                            'atmosferica. '
                                                                                                                                                                                                                            'Una '
                                                                                                                                                                                                                            'relazione '
                                                                                                                                                                                                                            'statistica '
                                                                                                                                                                                                                            'può '
                                                                                                                                                                                                                            'aiutare '
                                                                                                                                                                                                                            'l’interpretazione, '
                                                                                                                                                                                                                            'ma '
                                                                                                                                                                                                                            'la '
                                                                                                                                                                                                                            'sola '
                                                                                                                                                                                                                            'correlazione '
                                                                                                                                                                                                                            'non '
                                                                                                                                                                                                                            'dimostra '
                                                                                                                                                                                                                            'una '
                                                                                                                                                                                                                            'causa '
                                                                                                                                                                                                                            'cosmica '
                                                                                                                                                                                                                            'o '
                                                                                                                                                                                                                            'ambientale.',
 'The comparison uses only quality-filtered, one-to-one paired measurements.': 'Il confronto usa solo misure filtrate '
                                                                               'per qualità e abbinate uno a uno.',
 'The configured danger threshold is exceeded.': 'La soglia di pericolo configurata è superata.',
 'The connected counters currently agree well': 'I contatori connessi concordano attualmente bene',
 'The counters disagree, so a device-specific effect is more likely': 'I contatori non concordano; è quindi più '
                                                                      'probabile un effetto specifico del dispositivo',
 'The current radiation level is uncritical according to the selected thresholds.': 'Il livello attuale di radiazione '
                                                                                    'non è critico secondo le soglie '
                                                                                    'selezionate.',
 'The current value is below the configured warning threshold and within the usual local range.': 'Il valore attuale è '
                                                                                                  'inferiore alla '
                                                                                                  'soglia di avviso '
                                                                                                  'configurata e '
                                                                                                  'rientra '
                                                                                                  'nell’intervallo '
                                                                                                  'locale abituale.',
 'The current value is within the configured warning range.': 'Il valore attuale è nell’intervallo di avviso '
                                                              'configurato.',
 'The deviation is device-specific; the measurement-site profile remains normal': 'La deviazione è specifica del '
                                                                                  'dispositivo; il profilo del sito '
                                                                                  'rimane normale',
 'The device baseline is available, but there are not enough recent measurements for a current comparison.': 'La '
                                                                                                             'baseline '
                                                                                                             'del '
                                                                                                             'dispositivo '
                                                                                                             'è '
                                                                                                             'disponibile, '
                                                                                                             'ma non '
                                                                                                             'ci sono '
                                                                                                             'ancora '
                                                                                                             'abbastanza '
                                                                                                             'misure '
                                                                                                             'recenti '
                                                                                                             'per un '
                                                                                                             'confronto '
                                                                                                             'attuale.',
 'The device clock differs from Home Assistant time.': 'The device clock differs from Home Assistant time.',
 'The filtered counters disagree, so a device-specific effect is more likely': 'I contatori filtrati non concordano; è '
                                                                               'più probabile un effetto specifico del '
                                                                               'dispositivo',
 'The learned baseline remains available. More current samples are required before the local comparison can be updated.': 'La '
                                                                                                                          'baseline '
                                                                                                                          'appresa '
                                                                                                                          'rimane '
                                                                                                                          'disponibile. '
                                                                                                                          'Servono '
                                                                                                                          'ulteriori '
                                                                                                                          'campioni '
                                                                                                                          'recenti '
                                                                                                                          'per '
                                                                                                                          'aggiornare '
                                                                                                                          'il '
                                                                                                                          'confronto '
                                                                                                                          'locale.',
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
 'The local background is still being learned, so no anomaly assessment is available yet.': 'Il fondo locale è ancora '
                                                                                            'in fase di apprendimento, '
                                                                                            'quindi non è ancora '
                                                                                            'disponibile una '
                                                                                            'valutazione delle '
                                                                                            'anomalie.',
 'The measurement-site baseline is {deviation:+.1f}% above its typical value': 'La baseline del sito di misura è '
                                                                               '{deviation:+.1f}% sopra il valore '
                                                                               'tipico',
 'The measurement-site profile combines both devices with quality weighting': 'Il profilo del sito combina entrambi i '
                                                                              'dispositivi con ponderazione della '
                                                                              'qualità',
 'The measurement-site profile currently relies on one device': 'Il profilo del sito di misura si basa attualmente su '
                                                                'un solo dispositivo',
 'The pressure model cannot prove cosmic radiation and never suppresses radiation warnings.': 'Il modello di pressione '
                                                                                              'non può dimostrare la '
                                                                                              'radiazione cosmica e '
                                                                                              'non sopprime mai gli '
                                                                                              'avvisi di radiazione.',
 'The quality-filtered counter comparison currently agrees well': 'Il confronto filtrato per qualità dei contatori '
                                                                  'concorda bene',
 'The recent 30-minute robust trend is rising': 'La tendenza robusta degli ultimi 30 minuti è in aumento',
 'The recent 30-minute trend is rising': 'La tendenza recente di 30 minuti è in aumento',
 'The request could not be processed. Check the selected options.': 'Impossibile elaborare la richiesta. Controlla le '
                                                                    'opzioni selezionate.',
 'The score combines time-window coverage, missing or irregular intervals, duplicate timestamps and optional-sensor coverage. It indicates how strongly the analysis can rely on the stored series.': 'Il '
                                                                                                                                                                                                      'punteggio '
                                                                                                                                                                                                      'combina '
                                                                                                                                                                                                      'copertura '
                                                                                                                                                                                                      'della '
                                                                                                                                                                                                      'finestra '
                                                                                                                                                                                                      'temporale, '
                                                                                                                                                                                                      'intervalli '
                                                                                                                                                                                                      'mancanti '
                                                                                                                                                                                                      'o '
                                                                                                                                                                                                      'irregolari, '
                                                                                                                                                                                                      'timestamp '
                                                                                                                                                                                                      'duplicati '
                                                                                                                                                                                                      'e '
                                                                                                                                                                                                      'copertura '
                                                                                                                                                                                                      'dei '
                                                                                                                                                                                                      'sensori '
                                                                                                                                                                                                      'opzionali. '
                                                                                                                                                                                                      'Indica '
                                                                                                                                                                                                      'quanto '
                                                                                                                                                                                                      'l’analisi '
                                                                                                                                                                                                      'può '
                                                                                                                                                                                                      'fare '
                                                                                                                                                                                                      'affidamento '
                                                                                                                                                                                                      'sulla '
                                                                                                                                                                                                      'serie '
                                                                                                                                                                                                      'memorizzata.',
 'The serial connection is unstable.': 'La connessione seriale è instabile.',
 'The traffic light and events are relative anomaly indicators, not safety classifications.': 'Il semaforo e gli '
                                                                                              'eventi sono indicatori '
                                                                                              'di anomalia relativa, '
                                                                                              'non classificazioni di '
                                                                                              'sicurezza.',
 'The value is also within the usual range for this location.': 'Il valore è anche nell’intervallo abituale di questo '
                                                                'luogo.',
 'The values most users need first': 'I valori che servono prima alla maggior parte degli utenti',
 'These are statistical changes. They can indicate a location, geometry or environmental change, but do not identify the cause.': 'Sono '
                                                                                                                                  'variazioni '
                                                                                                                                  'statistiche. '
                                                                                                                                  'Possono '
                                                                                                                                  'indicare '
                                                                                                                                  'un '
                                                                                                                                  'cambiamento '
                                                                                                                                  'di '
                                                                                                                                  'posizione, '
                                                                                                                                  'geometria '
                                                                                                                                  'o '
                                                                                                                                  'ambiente, '
                                                                                                                                  'ma '
                                                                                                                                  'non '
                                                                                                                                  'ne '
                                                                                                                                  'identificano '
                                                                                                                                  'la '
                                                                                                                                  'causa.',
 'These values describe the shape of the count distribution. They do not by themselves prove a physical cause or a calibration state.': 'Questi '
                                                                                                                                        'valori '
                                                                                                                                        'descrivono '
                                                                                                                                        'la '
                                                                                                                                        'forma '
                                                                                                                                        'della '
                                                                                                                                        'distribuzione '
                                                                                                                                        'dei '
                                                                                                                                        'conteggi. '
                                                                                                                                        'Da '
                                                                                                                                        'soli '
                                                                                                                                        'non '
                                                                                                                                        'dimostrano '
                                                                                                                                        'una '
                                                                                                                                        'causa '
                                                                                                                                        'fisica '
                                                                                                                                        'né '
                                                                                                                                        'lo '
                                                                                                                                        'stato '
                                                                                                                                        'di '
                                                                                                                                        'calibrazione.',
 'This analysis detects unusual changes compared with the normal background at this location. It is not a danger classification; an unusual value can still be below the absolute warning threshold.': 'Questa '
                                                                                                                                                                                                       'analisi '
                                                                                                                                                                                                       'rileva '
                                                                                                                                                                                                       'variazioni '
                                                                                                                                                                                                       'insolite '
                                                                                                                                                                                                       'rispetto '
                                                                                                                                                                                                       'al '
                                                                                                                                                                                                       'fondo '
                                                                                                                                                                                                       'normale '
                                                                                                                                                                                                       'del '
                                                                                                                                                                                                       'luogo. '
                                                                                                                                                                                                       'Non '
                                                                                                                                                                                                       'è '
                                                                                                                                                                                                       'una '
                                                                                                                                                                                                       'classificazione '
                                                                                                                                                                                                       'di '
                                                                                                                                                                                                       'pericolo; '
                                                                                                                                                                                                       'un '
                                                                                                                                                                                                       'valore '
                                                                                                                                                                                                       'insolito '
                                                                                                                                                                                                       'può '
                                                                                                                                                                                                       'comunque '
                                                                                                                                                                                                       'restare '
                                                                                                                                                                                                       'sotto '
                                                                                                                                                                                                       'la '
                                                                                                                                                                                                       'soglia '
                                                                                                                                                                                                       'assoluta '
                                                                                                                                                                                                       'di '
                                                                                                                                                                                                       'avviso.',
 'This cannot be undone. Delete all GMC history?': 'This cannot be undone. Delete all GMC history?',
 'This classification only compares the current measurement with the selected thresholds. It does not compare the value with the usual background at this location.': 'Questa '
                                                                                                                                                                      'classificazione '
                                                                                                                                                                      'confronta '
                                                                                                                                                                      'solo '
                                                                                                                                                                      'la '
                                                                                                                                                                      'misurazione '
                                                                                                                                                                      'attuale '
                                                                                                                                                                      'con '
                                                                                                                                                                      'le '
                                                                                                                                                                      'soglie '
                                                                                                                                                                      'selezionate. '
                                                                                                                                                                      'Non '
                                                                                                                                                                      'la '
                                                                                                                                                                      'confronta '
                                                                                                                                                                      'con '
                                                                                                                                                                      'il '
                                                                                                                                                                      'fondo '
                                                                                                                                                                      'abituale '
                                                                                                                                                                      'del '
                                                                                                                                                                      'luogo.',
 'This factor is only a relative device comparison and is not an absolute radiation calibration.': 'This factor is '
                                                                                                   'only a relative '
                                                                                                   'device comparison '
                                                                                                   'and is not an '
                                                                                                   'absolute radiation '
                                                                                                   'calibration.',
 'This report is descriptive and is not a radiation-safety classification.': 'Questo rapporto è descrittivo e non '
                                                                             'costituisce una classificazione di '
                                                                             'radioprotezione.',
 'Thresholds can be changed in the add-on configuration.': 'Le soglie possono essere modificate nella configurazione '
                                                           'dell’add-on.',
 'Thu': 'Gio',
 'Thursday': 'Giovedì',
 'Tilted': 'Tilted',
 'Time series': 'Serie temporale',
 'Time series, Poisson comparison and weekday/hour heatmap': 'Serie temporale, confronto Poisson e mappa di calore '
                                                             'giorno/ora',
 'Time-series PNG': 'Serie temporale PNG',
 'Timestamp diagnostics': 'Diagnostica dei timestamp',
 'Timezone': 'Fuso orario',
 'Today so far bundle': 'Pacchetto giornata corrente',
 'Too few pressure/CPM pairs': 'Troppe poche coppie pressione/CPM',
 'Too few valid paired measurements for a reliable device comparison': 'Troppo poche misure abbinate valide per un '
                                                                       'confronto affidabile',
 'Too little or too fragmented for strong conclusions': 'Dati troppo pochi o frammentati per conclusioni solide',
 'Trend (30 min)': 'Tendenza (30 min)',
 'Tue': 'Mar',
 'Tuesday': 'Martedì',
 'Type DELETE ALL GMC HISTORY to confirm': 'Type DELETE ALL GMC HISTORY to confirm',
 'Type RESTORE to confirm': 'Digitare RESTORE per confermare',
 'Typical for {weekday} at {hour}:00': 'Tipico per {weekday} alle {hour}:00',
 'USB down': 'Verticale, USB in basso',
 'USB left': 'Verticale, USB a sinistra',
 'USB right': 'Verticale, USB a destra',
 'USB up': 'Verticale, USB in alto',
 'UTC timestamp': 'Timestamp UTC',
 'Unavailable': 'Non disponibile',
 'Unconfirmed values since bridge start': 'Unconfirmed values since bridge start',
 'Uncritical': 'Non critico',
 'Uncritical: below warning threshold': 'Non critico: sotto la soglia di avviso',
 'Unknown': 'Sconosciuto',
 'Unknown GMC': 'Dispositivo GMC sconosciuto',
 'Unknown report device': 'Dispositivo rapporto sconosciuto',
 'Unknown serial device': 'Unknown serial device',
 'Unstable': 'Instabile',
 'Unsupported report format': 'Formato rapporto non supportato',
 'Upload errors': 'Errori di invio',
 'Upload errors since start': 'Errori di invio dall’avvio',
 'Upload failed': 'Invio non riuscito',
 'Upload successful': 'Invio riuscito',
 'Uploading': 'Invio in corso',
 'Upright': 'Upright',
 'Use this as context only and review longer periods before drawing conclusions.': 'Usa questa informazione solo come '
                                                                                   'contesto e valuta periodi più '
                                                                                   'lunghi prima di trarre '
                                                                                   'conclusioni.',
 'Valid measurements': 'Misure valide',
 'Variance / mean': 'Varianza / media',
 'Very close to Poisson-like spread': 'Molto vicino a una dispersione tipo Poisson',
 'Very complete 24 h data window': 'Finestra dati 24 h molto completa',
 'Very strong linear relationship': 'Relazione lineare molto forte',
 'Very weak linear relationship': 'Relazione lineare molto debole',
 'Voltage': 'Tensione',
 'Voltage Errors Since Start': 'Errori tensione dall’avvio',
 'Voltage [V]': 'Tensione [V]',
 'Voltage correlation': 'Correlazione tensione',
 'Waiting for enough recent measurements': 'In attesa di misure recenti sufficienti',
 'Waiting for first upload': 'In attesa del primo invio',
 'Waiting for recent measurements': 'In attesa di misure recenti',
 'Waiting for the first accepted measurement': 'Waiting for the first accepted measurement',
 'Warning': 'Avviso',
 'Warning from {warning} s; critical from {critical} s': 'Avviso da {warning} s; critico da {critical} s',
 'Warning threshold exceeded': 'Soglia di avviso superata',
 'Warning thresholds': 'Soglie di avviso',
 'Weak linear relationship': 'Relazione lineare debole',
 'Weather pressure sources disagree': 'Le fonti della pressione meteo non concordano',
 'Wed': 'Mer',
 'Wednesday': 'Mercoledì',
 'Weekday': 'Giorno della settimana',
 'Weekday/hour heatmap': 'Mappa di calore giorno/ora',
 'What does the historical trend mean?': 'Che cosa significa la tendenza storica?',
 'What each report preserves and how periods are defined': 'Cosa conserva ogni rapporto e come sono definiti i periodi',
 'What should I do?': 'Che cosa devo fare?',
 'What this assessment means': 'Significato di questa valutazione',
 'Why are Poisson values shown?': 'Perché vengono mostrati i valori di Poisson?',
 'Why is this assessment shown?': 'Perché viene mostrata questa valutazione?',
 'Within local background range': 'Nel fondo locale',
 'Within normal statistical variation': 'Entro la normale variazione statistica',
 'Within the usual local range': 'Nell’intervallo locale abituale',
 'Within warning range': 'Nell’intervallo di avviso',
 'Yellow': 'Giallo',
 'Z-score = (latest CPM − 24 h mean) / 24 h standard deviation.': 'Punteggio Z = (ultimo CPM − media 24 h) / '
                                                                  'deviazione standard 24 h.',
 'Z-score formula explanation': 'Punteggio Z = (ultimo CPM − media 24 h) / deviazione standard 24 h.',
 'complete and regularly spaced data': 'dati completi e regolarmente distanziati',
 'confirmations': 'confirmations',
 'counting uncertainty {value:.2f}%': 'counting uncertainty {value:.2f}%',
 'coverage': 'copertura',
 'daily values': 'valori giornalieri',
 'days': 'giorni',
 'duplicates / clock regressions': 'duplicati / regressioni dell’orologio',
 'entity patterns': 'entity patterns',
 'errors': 'errors',
 'estimated signal probability': 'probabilità stimata del segnale',
 'excluded measurements': 'misure escluse',
 'longest gap {value} s': 'intervallo massimo {value} s',
 'measurements': 'measurements',
 'minimum sample coverage': 'copertura minima dei campioni',
 'n={count} paired samples': 'n={count} coppie di misure',
 'n={count} · {coverage:.1f}% coverage': 'n={count} · copertura {coverage:.1f}%',
 'paired samples': 'coppie di misure',
 'reconnects': 'reconnects',
 'relative to baseline': 'rispetto alla baseline',
 'score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s': 'punteggio {score:.1f}/100 · copertura '
                                                                           '{coverage:.1f}% · intervallo massimo {gap} '
                                                                           's',
 'short / long intervals': 'intervalli brevi / lunghi',
 'since the current bridge start': 'since the current bridge start',
 'temperature coverage {value}%': 'copertura temperatura {value}%',
 'unknown': 'sconosciuto',
 'valid hourly values': 'valori orari validi',
 'valid paired samples': 'coppie di misure valide',
 'voltage coverage {value}%': 'copertura tensione {value}%',
 'write errors since app start': 'write errors since app start',
 '{before:.2f} → {after:.2f} CPM · {sigma:.1f}σ · {hours} h persistent': '{before:.2f} → {after:.2f} CPM · '
                                                                         '{sigma:.1f}σ · {hours} h persistent',
 '{check_type} result cached for {seconds} s · schema v{schema}': 'Risultato {check_type} memorizzato per {seconds} s '
                                                                  '· schema v{schema}',
 '{connected} connected · {disconnected} disconnected': '{connected} connected · {disconnected} disconnected',
 '{count} implausible measurements were excluded from the assessment': '{count} misure non plausibili sono state '
                                                                       'escluse dalla valutazione',
 '{count} measurements': '{count} misure',
 '{count} measurements and {events} events were removed.': '{count} measurements and {events} events were removed.',
 '{events} events · {diagnostics} diagnostics': '{events} events · {diagnostics} diagnostics',
 '{gyro_note} History retention: {days} days. Daily periods are local calendar days; weekly periods are ISO weeks from Monday through Sunday.': '{gyro_note} '
                                                                                                                                                'Conservazione '
                                                                                                                                                'cronologia: '
                                                                                                                                                '{days} '
                                                                                                                                                'giorni. '
                                                                                                                                                'I '
                                                                                                                                                'periodi '
                                                                                                                                                'giornalieri '
                                                                                                                                                'sono '
                                                                                                                                                'giorni '
                                                                                                                                                'di '
                                                                                                                                                'calendario '
                                                                                                                                                'locali; '
                                                                                                                                                'quelli '
                                                                                                                                                'settimanali '
                                                                                                                                                'sono '
                                                                                                                                                'settimane '
                                                                                                                                                'ISO '
                                                                                                                                                'da '
                                                                                                                                                'lunedì '
                                                                                                                                                'a '
                                                                                                                                                'domenica.',
 '{model} — Radiation monitoring report': '{model} — Rapporto di monitoraggio radiazioni',
 '{seconds} seconds ago': '{seconds} seconds ago',
 '{value:g} h': '{value:g} h',
 '{value:g} min': '{value:g} min',
 '{value} clock regressions observed': '{value} regressioni dell’orologio osservate',
 '{value} duplicate timestamps observed': '{value} timestamp duplicati osservati',
 '{value} long intervals': '{value} intervalli lunghi',
 '{value} unusually short intervals': '{value} intervalli insolitamente brevi',
 '{value} vs local baseline': '{value} rispetto alla baseline locale',
 '{value}% time-window coverage': 'copertura temporale {value}%'}

# Runtime presentation templates added in 7.1.4.
CATALOG.update({
    'Comparison confidence: {confidence}': 'Affidabilità del confronto: {confidence}',
    'Confidence: {confidence}': 'Affidabilità: {confidence}',
    'Status': 'Stato',
    'Typical background': 'Fondo tipico',
    'Valid paired samples': 'Coppie di misure valide',
    'Warning from {warning:g} s; critical from {critical:g} s': 'Avviso da {warning:g} s; critico da {critical:g} s',
    'valid hourly values · {days:.1f} days · {span:.1f} hPa': 'valori orari validi · {days:.1f} giorni · {span:.1f} hPa',
    '{a:+.1f}% / {b:+.1f}%': '{a:+.1f}% / {b:+.1f}%',
    '{b} × factor → {a}': '{b} × fattore → {a}',
    '{content}': '{content}',
    '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)': '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)',
    '{days} days': '{days} giorni',
    '{dose:.3f} µSv/h': '{dose:.3f} µSv/h',
    '{first} {second}': '{first} {second}',
    '{from_value} → {to_value}': '{from_value} → {to_value}',
    '{note} · n={samples}': '{note} · n={samples}',
    '{pairs} valid paired samples': '{pairs} coppie di misure valide',
    '{pairs} valid paired samples · counting uncertainty {value:.2f}%': '{pairs} coppie di misure valide · incertezza di conteggio {value:.2f}%',
    '{probability:.0f}% estimated signal probability': '{probability:.0f} % di probabilità stimata del segnale',
    '{span:.0f} {days_label} · {count} {daily_label}': '{span:.0f} {days_label} · {count} {daily_label}',
    '{start}–{end} °C · {samples} Samples': '{start}–{end} °C · {samples} misure',
    '{trend:+.1f} CPM': '{trend:+.1f} CPM',
    '{value:g} µSv/h': '{value:g} µSv/h',
    'Last uploaded CPM': 'Ultimo CPM inviato',
    'Last uploaded ACPM': 'Ultimo ACPM inviato',
    'GMCMap last uploaded ACPM': 'Ultimo ACPM inviato a GMCMap',
    'GMCMap ACPM accepted samples': 'Campioni accettati per l’ACPM GMCMap',
    'ACPM is the average of all accepted CPM readings since the current app measurement session began.': 'L’ACPM è la media di tutte le letture CPM accettate dall’inizio della sessione di misurazione corrente dell’app.',
    'User manual': 'Manuale utente',
    'Open user manual PDF': 'Apri il manuale utente in PDF',
    'User manual is not available': 'Il manuale utente non è disponibile',
})

# Version 8.2.1 report and history labels.
CATALOG.update({
    'Accepted measurements [count]': 'Misure accettate [numero]',
    'Local hour [h]': 'Ora locale [h]',
    'Mean count rate [CPM]': 'Frequenza di conteggio media [CPM]',
    'Radiation Monitoring': 'Monitoraggio delle radiazioni',
    'Rejected raw value': 'Valore grezzo scartato',
})


# Version 8.2.1 complete runtime localization.
CATALOG.update({
    'The recent level differs from counting noise with {probability:.2f}% statistical confidence': 'Il livello recente differisce dal rumore di conteggio con una confidenza statistica del {probability:.2f} %',
    'A comparable or more extreme hourly level occurred about once in {rarity:.1f} historical hours': 'Un livello orario comparabile o più estremo si è verificato circa una volta ogni {rarity:.1f} ore storiche',
})

# Long-term analysis 9.1.1
CATALOG.update({'24 hours': '24 ore', '30 days': '30 giorni', '365 days': '365 giorni', '7 days': '7 giorni', '7-day rolling median': 'Mediana mobile a 7 giorni', '90 days': '90 giorni', '95% block-bootstrap interval for mean': 'Intervallo bootstrap a blocchi al 95% per la media', '95% block-bootstrap interval for median': 'Intervallo bootstrap a blocchi al 95% per la mediana', 'Air-pressure association': 'Associazione con la pressione atmosferica', 'Annual projection from the last 30 days: {value} µSv': 'Proiezione annuale dagli ultimi 30 giorni: {value} µSv', 'Annual projection is not shown until a sufficiently complete 30-day period exists.': 'La proiezione annuale viene mostrata solo dopo un periodo di 30 giorni sufficientemente completo.', 'Based on {hours} covered hours': 'Basato su {hours} ore coperte', 'Bootstrap uncertainty, distribution dispersion, EWMA and CUSUM': 'Incertezza bootstrap, dispersione, EWMA e CUSUM', 'Calendar heat map': 'Mappa termica del calendario', 'Calendar heat map of daily median CPM': 'Mappa termica delle mediane CPM giornaliere', 'Connected periods above the robust local long-term threshold': 'Periodi continui sopra la soglia locale robusta a lungo termine', 'Contextual Fano-like ratio; rolling CPM values are not independent Poisson counts': 'Rapporto contestuale simile a Fano; i CPM mobili non sono conteggi di Poisson indipendenti', 'Correlation does not prove causation.': 'La correlazione non dimostra causalità.', 'Coverage {coverage}% · at least {required}% required': 'Copertura {coverage}% · richiesto almeno {required}%', 'Covered hours': 'Ore coperte', 'Cumulative derived dose': 'Dose cumulativa derivata', 'Daily and monthly development': 'Andamento giornaliero e mensile', 'Daily median': 'Mediana giornaliera', 'Daily median and 7-day rolling median': 'Mediana giornaliera e mediana mobile a 7 giorni', 'Daily medians, rolling median and calendar view': 'Mediane giornaliere, mediana mobile e vista calendario', 'Derived cumulative dose: {dose} µSv': 'Dose cumulativa derivata: {dose} µSv', 'Derived dose (µSv)': 'Dose derivata (µSv)', 'Derived from the robust local background; not an official alarm threshold': 'Derivato dal fondo locale robusto; non è una soglia di allarme ufficiale', 'Duration (h)': 'Durata (h)', 'EWMA, CUSUM, trend tests and relative event detection provide statistical context only. They do not identify a radiation source and do not replace calibrated radiation-protection measurements.': 'EWMA, CUSUM, i test di tendenza e il rilevamento relativo forniscono solo un contesto statistico. Non identificano una sorgente e non sostituiscono misure calibrate di radioprotezione.', 'Effective sample size': 'Dimensione effettiva del campione', 'Environmental correlations are exploratory. They may reflect common time patterns, ventilation, weather or other confounding factors and do not prove causation.': 'Le correlazioni ambientali sono esplorative. Possono riflettere schemi temporali comuni, ventilazione, meteo o altri fattori e non dimostrano causalità.', 'Excess area (CPM·h)': 'Area di eccesso (CPM·h)', 'Exploratory Spearman correlations at 0, 3, 6, 12 and 24 hour lags': 'Correlazioni di Spearman esplorative con ritardi di 0, 3, 6, 12 e 24 ore', 'Higher': 'Più alto', 'Hourly dispersion ratio': 'Rapporto di dispersione oraria', 'Lagged environmental associations': 'Associazioni ambientali ritardate', 'Long-term analysis': 'Analisi a lungo termine', 'Long-term analysis for {device}': 'Analisi a lungo termine per {device}', 'Long-term background, cumulative dose, trend, recurring patterns and statistical process diagnostics': 'Fondo a lungo termine, dose cumulativa, tendenza, schemi ricorrenti e diagnostica statistica del processo', 'Long-term overview': 'Panoramica a lungo termine', 'Long-term statistical diagnostics': 'Diagnostica statistica a lungo termine', 'Long-term trend': 'Tendenza a lungo termine', 'Lower': 'Più basso', 'Mann-Kendall test with Sen slope on sufficiently covered daily medians': 'Test di Mann-Kendall con pendenza di Sen sulle mediane giornaliere con copertura sufficiente', 'Maximum CPM': 'CPM massimo', 'Mean CPM': 'CPM medio', 'Median CPM': 'CPM mediano', 'Median {median} CPM · coverage {coverage}%': 'Mediana {median} CPM · copertura {coverage}%', 'Month': 'Mese', 'Monthly aggregates': 'Aggregati mensili', 'Moving blocks preserve short-range time dependence': 'I blocchi mobili preservano la dipendenza temporale a breve raggio', 'No calendar data available': 'Nessun dato di calendario disponibile', 'No long-term analysis available yet': 'Analisi a lungo termine non ancora disponibile', 'No monthly aggregates available': 'Nessun aggregato mensile disponibile', 'No persistent CUSUM signal detected': 'Nessun segnale CUSUM persistente rilevato', 'No persistent EWMA signal detected': 'Nessun segnale EWMA persistente rilevato', 'No persistent relative elevation episodes detected': 'Nessun episodio relativo persistente rilevato', 'No supported dose conversion for this period': 'Nessuna conversione di dose supportata per questo periodo', 'No value is calculated until enough hourly pairs are available.': 'Nessun valore viene calcolato finché non sono disponibili sufficienti coppie orarie.', 'Not enough daily values for a long-term chart': 'Valori giornalieri insufficienti per un grafico a lungo termine', 'Not enough paired data': 'Dati accoppiati insufficienti', 'Not yet meaningful': 'Non ancora significativo', 'Only {covered} of {required} days covered': 'Coperti solo {covered} giorni su {required}', 'Persistent elevation episodes': 'Episodi di aumento persistente', 'Persistent episodes': 'Episodi persistenti', 'Preliminary': 'Preliminare', 'Ready': 'Valutabile', 'Real time windows with duration and coverage checks': 'Finestre temporali reali con controllo di durata e copertura', 'Recent 7-day median relative to the robust long-term background': 'Mediana recente a 7 giorni rispetto al fondo robusto a lungo termine', 'Recent background deviation': 'Deviazione recente dal fondo', 'Relative event threshold': 'Soglia relativa degli eventi', 'Robust local background': 'Fondo locale robusto', 'Scientific interpretation': 'Interpretazione scientifica', 'Start': 'Inizio', 'Statistical signal detected': 'Segnale statistico rilevato', 'Stored measurements are required before long-term statistics can be calculated.': 'Sono necessarie misure memorizzate prima di calcolare le statistiche a lungo termine.', 'Strongest at {lag} h lag · {pairs} pairs · {strength} association': 'Associazione più forte con ritardo di {lag} h · {pairs} coppie · associazione {strength}', 'Temperature association': 'Associazione con la temperatura', 'The detector uses the robust long-term local background and does not replace radiation-safety alarms.': 'Il rilevamento utilizza il fondo locale robusto a lungo termine e non sostituisce gli allarmi di radioprotezione.', 'Time at or above configured danger threshold': 'Tempo alla o sopra la soglia di pericolo configurata', 'Time in configured warning range': 'Tempo nell’intervallo di avviso configurato', 'Typical range P05–P95: {low}–{high} CPM': 'Intervallo tipico P05-P95: {low}-{high} CPM', 'moderate': 'moderata', 'strong': 'forte', 'weak': 'debole', '{date}: median {median} CPM, coverage {coverage}%': '{date}: mediana {median} CPM, copertura {coverage}%', '{direction} · {slope} CPM/day · p={p}': '{direction} · {slope} CPM/giorno · p={p}', '{hours} covered hours': '{hours} ore coperte', '{hours} total elevated hours · longest {longest} h': '{hours} ore elevate totali · più lunga {longest} h', '{observed} daily observations · correlation duration {duration} days': '{observed} osservazioni giornaliere · durata della correlazione {duration} giorni', '{replicates} replicates · block length {block} days': '{replicates} repliche · lunghezza blocco {block} giorni', 'Long-term': 'Lungo termine', 'stable': 'stabile', 'increasing': 'crescente', 'decreasing': 'decrescente'})

# Recent baseline wording 9.1.1
CATALOG.update({'Recent baseline context': 'Contesto recente della linea di base', 'Seven-day baseline deviation, drift and sustained relative events': 'Scostamento dalla linea di base a 7 giorni, deriva ed eventi relativi persistenti'})


# Extended agreement and seasonal analysis 9.1.1
CATALOG.update({'Bland-Altman bias': 'Bias di Bland-Altman', '95% limits of agreement': 'Limiti di concordanza al 95%', 'Mean signed difference A minus B': 'Differenza media con segno A meno B', 'Exploratory paired-device agreement; correlation alone does not establish agreement.': 'Concordanza esplorativa tra dispositivi appaiati; la sola correlazione non dimostra la concordanza.', 'Seasonal month-of-year profile': 'Profilo stagionale per mese dell’anno', 'Median CPM by calendar month across available years': 'Mediana CPM per mese di calendario negli anni disponibili', 'Calendar month': 'Mese di calendario', 'Days represented': 'Giorni rappresentati', 'Not enough months for a seasonal profile': 'Mesi insufficienti per un profilo stagionale', 'At least six represented calendar months are required.': 'Sono necessari almeno sei mesi di calendario rappresentati.', 'Exploratory seasonal summary; it does not separate weather, location, detector or calibration changes.': 'Riepilogo stagionale esplorativo; non separa variazioni di meteo, posizione, rivelatore o calibrazione.'})


# Evidence-based long-term presentation and field-test diagnostics 9.3.0
CATALOG.update({'{available} of {required} required hourly pairs are available.': '{available} of {required} required hourly pairs are available.', 'FDR-adjusted p={value}': 'FDR-adjusted p={value}', 'Practical magnitude not available': 'Practical magnitude not available', 'Moderate practical magnitude': 'Moderate practical magnitude', 'Estimated change {value}% per month · {magnitude}': 'Estimated change {value}% per month · {magnitude}', 'Runtime since service start': 'Runtime since service start', 'Cumulative counters reset when the service restarts.': 'Cumulative counters reset when the service restarts.', 'GMCMap transmission': 'GMCMap transmission', 'Export field-test protocol (JSON)': 'Esporta protocollo di test sul campo (JSON)', '{months} represented calendar months': '{months} represented calendar months', 'Statistical process diagnostics': 'Diagnostica statistica di processo', 'At least 30 sufficiently complete days and an adequate effective sample size are required.': 'At least 30 sufficiently complete days and an adequate effective sample size are required.', '{success} successful · {errors} failed uploads': '{success} successful · {errors} failed uploads', 'No statistically clear long-term trend is visible': 'No statistically clear long-term trend is visible', 'Longest data gap': 'Longest data gap', 'Stored samples: {count}': 'Stored samples: {count}', 'Field-test interpretation': 'Field-test interpretation', 'A falling long-term tendency is visible': 'A falling long-term tendency is visible', 'Large practical magnitude': 'Large practical magnitude', '{days} covered days · {observed} daily observations': '{days} covered days · {observed} daily observations', 'Data basis': 'Base dati', 'A rising long-term tendency is visible': 'A rising long-term tendency is visible', 'Small practical magnitude': 'Small practical magnitude', 'Current background context': 'Contesto di fondo attuale', 'Annual projection from the last 90 days: {value} µSv': 'Proiezione annuale dagli ultimi 90 giorni: {value} µSv', 'The main result first; method details remain available below.': 'The main result first; method details remain available below.', 'Annual projection is not shown until a sufficiently complete 90-day period exists.': 'La proiezione annuale richiede un periodo di 90 giorni sufficientemente completo.', 'Supported': 'Supportato', 'Well supported': 'Ben supportato', 'Extended statistical methods': 'Metodi statistici avanzati', 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.': 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.', 'USB / serial recovery': 'USB / serial recovery', 'Database write errors': 'Database write errors', 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.': 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.', 'Plain-language assessment': 'Sintesi comprensibile', '{errors} serial errors · {reconnects} reconnects': '{errors} serial errors · {reconnects} reconnects', 'Long-term reliability field test': 'Test di affidabilità a lungo termine', 'No reliable long-term trend can be assessed yet': 'No reliable long-term trend can be assessed yet', 'Operational counters for USB, database continuity and GMCMap transmission': 'Operational counters for USB, database continuity and GMCMap transmission', 'EWMA, CUSUM and dispersion diagnostics; statistical context only': 'EWMA, CUSUM and dispersion diagnostics; statistical context only', '{count} detected gaps above the expected interval': '{count} detected gaps above the expected interval', 'Trend method details': 'Trend method details', 'FDR-adjusted significance not available': 'FDR-adjusted significance not available', 'Exploratory Spearman correlations with false-discovery-rate correction': 'Exploratory Spearman correlations with false-discovery-rate correction', 'Seasonal assessment': 'Seasonal assessment', 'Not evaluable': 'Non valutabile', 'Integrated derived dose in the measured period': 'Integrated derived dose in the measured period', 'Exploratory': 'Esplorativo', 'Confidence intervals, effective sample size, test statistics and practical effect size': 'Confidence intervals, effective sample size, test statistics and practical effect size', 'Very small practical magnitude': 'Very small practical magnitude'})

# Complete localized overrides for 9.3.0
CATALOG.update({'Not evaluable': 'Non valutabile', 'Exploratory': 'Esplorativo', 'Supported': 'Supportato', 'Well supported': 'Ben supportato', 'Very small practical magnitude': 'Entità pratica molto piccola', 'Small practical magnitude': 'Entità pratica piccola', 'Moderate practical magnitude': 'Entità pratica moderata', 'Large practical magnitude': 'Entità pratica grande', 'Practical magnitude not available': 'Entità pratica non disponibile', 'No reliable long-term trend can be assessed yet': 'Non è ancora possibile valutare una tendenza affidabile a lungo termine', 'At least 30 sufficiently complete days and an adequate effective sample size are required.': 'Sono necessari almeno 30 giorni sufficientemente completi e una dimensione campionaria effettiva adeguata.', 'A rising long-term tendency is visible': 'È visibile una tendenza crescente a lungo termine', 'A falling long-term tendency is visible': 'È visibile una tendenza decrescente a lungo termine', 'No statistically clear long-term trend is visible': 'Non è visibile una tendenza a lungo termine statisticamente chiara', 'Estimated change {value}% per month · {magnitude}': 'Variazione stimata {value}% al mese · {magnitude}', 'Runtime since service start': 'Tempo di esecuzione dall’avvio del servizio', 'Cumulative counters reset when the service restarts.': 'I contatori cumulativi vengono azzerati al riavvio del servizio.', 'USB / serial recovery': 'Ripristino USB / seriale', '{errors} serial errors · {reconnects} reconnects': '{errors} errori seriali · {reconnects} riconnessioni', 'Longest data gap': 'Intervallo di dati più lungo', '{count} detected gaps above the expected interval': '{count} intervalli rilevati oltre l’intervallo previsto', 'Database write errors': 'Errori di scrittura del database', 'Stored samples: {count}': 'Campioni memorizzati: {count}', 'GMCMap transmission': 'Trasmissione GMCMap', '{success} successful · {errors} failed uploads': '{success} riusciti · {errors} non riusciti', 'Export field-test protocol (JSON)': 'Esporta protocollo di test sul campo (JSON)', 'Field-test interpretation': 'Interpretazione del test sul campo', 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.': 'Questi contatori operativi aiutano a valutare l’affidabilità a lungo termine. Non certificano la calibrazione del rilevatore né l’accuratezza della misura.', '{available} of {required} required hourly pairs are available.': 'Sono disponibili {available} delle {required} coppie orarie richieste.', 'FDR-adjusted p={value}': 'p corretto FDR={value}', 'FDR-adjusted significance not available': 'Significatività corretta FDR non disponibile', 'Plain-language assessment': 'Sintesi comprensibile', 'The main result first; method details remain available below.': 'Prima il risultato principale; i dettagli metodologici restano disponibili sotto.', 'Current background context': 'Contesto di fondo attuale', 'Data basis': 'Base dati', '{days} covered days · {observed} daily observations': '{days} giorni coperti · {observed} osservazioni giornaliere', 'Integrated derived dose in the measured period': 'Dose derivata integrata nel periodo misurato', 'Seasonal assessment': 'Valutazione stagionale', '{months} represented calendar months': '{months} mesi di calendario rappresentati', 'Extended statistical methods': 'Metodi statistici estesi', 'Confidence intervals, effective sample size, test statistics and practical effect size': 'Intervalli di confidenza, campione effettivo, statistiche di test ed effetto pratico', 'Trend method details': 'Dettagli del metodo di tendenza', 'Statistical process diagnostics': 'Diagnostica statistica di processo', 'EWMA, CUSUM and dispersion diagnostics; statistical context only': 'Diagnostica EWMA, CUSUM e dispersione; solo contesto statistico', 'Exploratory Spearman correlations with false-discovery-rate correction': 'Correlazioni esplorative di Spearman con correzione del tasso di falsi rilevamenti', 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.': 'Le correlazioni ambientali sono esplorative. La correzione di Benjamini-Hochberg riduce i falsi rilevamenti tra i ritardi testati, ma non giustifica conclusioni causali.', 'Long-term reliability field test': 'Test sul campo dell’affidabilità a lungo termine', 'Operational counters for USB, database continuity and GMCMap transmission': 'Contatori operativi per USB, continuità del database e trasmissione GMCMap', 'Annual projection from the last 90 days: {value} µSv': 'Proiezione annuale dagli ultimi 90 giorni: {value} µSv', 'Annual projection is not shown until a sufficiently complete 90-day period exists.': 'La proiezione annuale viene mostrata solo dopo un periodo di 90 giorni sufficientemente completo.'})


# Sidebar navigation and responsive application shell 9.3.0
CATALOG.update({'Main navigation': 'Navigazione principale', 'Monitoring': 'Monitoraggio', 'Evaluation': 'Valutazione', 'Documentation': 'Documentazione', 'Administration': 'Amministrazione', 'Close navigation': 'Chiudi navigazione', 'Skip to content': 'Vai al contenuto', 'Menu': 'Menu', 'Refresh': 'Aggiorna'})

# Global view control and long-term interpretation context 9.4.0
CATALOG.update({'Choose how many details and tools are shown across all sections. The selection is stored in this browser.': 'Determina quanti dettagli e strumenti vengono mostrati in tutte le sezioni. La selezione viene salvata in questo browser.', 'Long-term interpretation context': 'Contesto di interpretazione a lungo termine', 'Intelligent analysis, adaptive background and cosmic-influence context for the selected detector.': 'Analisi intelligente, fondo adattivo e contesto statistico dell’influenza cosmica per il rilevatore selezionato.'})
