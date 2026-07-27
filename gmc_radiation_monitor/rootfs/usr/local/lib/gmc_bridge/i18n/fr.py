from __future__ import annotations

CATALOG: dict[str, str] = {'1 h counting uncertainty': '1 h counting uncertainty',
 '1 h coverage': 'Couverture sur 1 h',
 '1 h mean': 'Moyenne sur 1 h',
 '1 h mean / 7 d mean × 100': 'Moyenne 1 h / moyenne 7 j × 100',
 '1 h mean dose rate': 'Débit de dose moyen sur 1 h',
 '1 h mean minus 7 d baseline': 'Moyenne 1 h moins référence 7 j',
 '24 h Fano factor': 'Facteur de Fano sur 24 h',
 '24 h P95': 'P95 sur 24 h',
 '24 h P99': 'P99 sur 24 h',
 '24 h Z-score': 'Score Z sur 24 h',
 '24 h counting uncertainty': '24 h counting uncertainty',
 '24 h distribution, percentiles and latest-value deviation': 'Distribution sur 24 h, percentiles et écart de la '
                                                              'dernière valeur',
 '24 h maximum': 'Maximum sur 24 h',
 '24 h mean': 'Moyenne sur 24 h',
 '24 h mean dose rate': 'Débit de dose moyen sur 24 h',
 '24 h median': 'Médiane sur 24 h',
 '24 h minimum': 'Minimum sur 24 h',
 '24 h standard deviation': 'Écart-type sur 24 h',
 '50th percentile': '50e percentile',
 '7 d baseline': 'Référence sur 7 j',
 '7 d baseline dose rate': 'Débit de dose de référence sur 7 jours',
 '7 d baseline drift': 'Dérive de la référence sur 7 jours',
 '7 d counting uncertainty': '7 d counting uncertainty',
 '7-day smoothed daily median': 'Médiane quotidienne lissée sur 7 jours',
 '95th percentile': '95e percentile',
 '99th percentile': '99e percentile',
 'A device function is temporarily unavailable.': 'Une fonction de l’appareil est temporairement indisponible.',
 'A fresh backup is recommended before deletion.': 'A fresh backup is recommended before deletion.',
 'A recent position change can affect comparability': 'Un changement récent de position peut affecter la comparabilité',
 'Above the typical time profile': 'Au-dessus du profil temporel typique',
 'Above the usual local range': 'Au-dessus de la plage locale habituelle',
 'Absolute radiation assessment': 'Évaluation absolue du rayonnement',
 'Absolute thresholds and local anomaly detection answer different questions.': 'Les seuils absolus et la détection '
                                                                                'locale des anomalies répondent à des '
                                                                                'questions différentes.',
 'Acceleration magnitude': 'Norme de l’accélération',
 'Acceleration raw values': 'Valeurs brutes d’accélération',
 'Accepted device values are stored separately after live CPM plausibility confirmation': 'Accepted device values are '
                                                                                          'stored separately after '
                                                                                          'live CPM plausibility '
                                                                                          'confirmation',
 'Active threshold profile': 'Profil de seuil actif',
 'Adaptive background profile': 'Profil de fond adaptatif',
 'Advanced': 'Avancé',
 'Advanced diagnostics': 'Diagnostics avancés',
 'Advanced visuals': 'Visualisations avancées',
 'Affected GMC devices': 'Affected GMC devices',
 'Agreement': 'Concordance',
 'Air-pressure source': 'Source de pression atmosphérique',
 'Air-pressure trend': 'Tendance de pression atmosphérique',
 'All GMC history was deleted': 'All GMC history was deleted',
 'All baselines and comparisons use the same robust quality-filtered measurements.': 'Toutes les références et '
                                                                                     'comparaisons utilisent les mêmes '
                                                                                     'mesures robustes filtrées par '
                                                                                     'qualité.',
 'All connected GMC devices': 'Tous les appareils GMC connectés',
 'All devices': 'Tous les appareils',
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
 'All statistical values, confidence intervals and diagnostics': 'Toutes les valeurs statistiques, intervalles de '
                                                                 'confiance et diagnostics',
 'All {count} known GMC devices are connected': 'All {count} known GMC devices are connected',
 'Allow restore': 'Autoriser la restauration',
 'Already assigned to {name}': 'Already assigned to {name}',
 'Analysis': 'Analyse',
 'Analysis JSON': 'JSON d’analyse',
 'Analysis PDF': 'PDF d’analyse',
 'Analysis depth': 'Niveau d’analyse',
 'Analysis for': 'Analyse de',
 'Analysis is still being prepared': 'Analysis is still being prepared',
 'Analysis shown': 'Analyse affichée',
 'Analysis, the traffic light and downloads will become meaningful after the first stored samples arrive.': 'L’analyse, '
                                                                                                            'le feu '
                                                                                                            'tricolore '
                                                                                                            'et les '
                                                                                                            'téléchargements '
                                                                                                            'deviendront '
                                                                                                            'pertinents '
                                                                                                            'dès '
                                                                                                            'l’enregistrement '
                                                                                                            'des '
                                                                                                            'premières '
                                                                                                            'mesures.',
 'Analyze this device': 'Analyser cet appareil',
 'Another report is already being generated': 'Un autre rapport est déjà en cours de génération',
 'Another report or maintenance job is running': 'Another report or maintenance job is running',
 'Another report or restore job is running': 'Un autre rapport ou une restauration est déjà en cours',
 'Another report, maintenance export, or restore job is running': 'Un autre rapport, export de maintenance ou travail '
                                                                  'de restauration est déjà en cours.',
 'App Started At': 'Application démarrée à',
 'Apply': 'Apply',
 'Assessment': 'Évaluation',
 'Assigned': 'Assigned',
 'At least 24 h reference and 6 h persistence are required': 'At least 24 h reference and 6 h persistence are required',
 'At least two daily background values are required.': 'Au moins deux valeurs quotidiennes du fond sont nécessaires.',
 'At least {count} valid hourly values are required': 'Au moins {count} valeurs horaires valides sont nécessaires',
 'At least {count} valid pairs are required': 'Au moins {count} paires valides sont requises',
 'At least {days} days of learning data are required': 'Au moins {days} jours de données d’apprentissage sont '
                                                       'nécessaires',
 'At least {span:g} hPa pressure variation is required': 'Une variation de pression d’au moins {span:g} hPa est '
                                                         'nécessaire',
 'At the same time, the value is clearly above the usual local background. Review the trend and measurement conditions.': 'En '
                                                                                                                          'même '
                                                                                                                          'temps, '
                                                                                                                          'la '
                                                                                                                          'valeur '
                                                                                                                          'est '
                                                                                                                          'nettement '
                                                                                                                          'supérieure '
                                                                                                                          'au '
                                                                                                                          'fond '
                                                                                                                          'local '
                                                                                                                          'habituel. '
                                                                                                                          'Vérifiez '
                                                                                                                          'la '
                                                                                                                          'tendance '
                                                                                                                          'et '
                                                                                                                          'les '
                                                                                                                          'conditions '
                                                                                                                          'de '
                                                                                                                          'mesure.',
 'Automatic device detection is running': 'Automatic device detection is running',
 'Automatic refresh is temporarily unavailable': 'Automatic refresh is temporarily unavailable',
 'Availability': 'Disponibilité',
 'Available': 'Available',
 'Back to analysis': 'Back to analysis',
 'Background index': 'Indice de fond',
 'Background index compares the rolling 1 h mean with the available 7 d baseline.': 'Indice de fond = moyenne '
                                                                                    'glissante sur 1 h rapportée à la '
                                                                                    'référence disponible sur 7 jours.',
 'Background index formula explanation': 'Indice de fond = moyenne glissante sur 1 h rapportée à la référence '
                                         'disponible sur 7 jours.',
 'Background trend over days and months': 'Évolution du fond sur plusieurs jours et mois',
 'Backup is compatible and ready to restore.': 'Backup is compatible and ready to restore.',
 'Backup preview failed': 'Backup preview failed',
 'Baseline available': 'Référence disponible',
 'Baseline currently stable': 'Référence actuellement stable',
 'Baseline deviation': 'Écart au niveau de référence',
 'Baseline deviation, drift and sustained relative events': 'Écart à la référence, dérive et événements relatifs '
                                                            'persistants',
 'Baseline deviation: {cpm} CPM ({percent}%)': 'Écart à la référence : {cpm} CPM ({percent} %)',
 'Baseline drift: {value}%': 'Dérive de la référence : {value} %',
 'Baseline learning in progress': 'Apprentissage du niveau de référence en cours',
 'Baseline readiness': 'Disponibilité du niveau de référence',
 'Baseline: {value} CPM': 'Référence : {value} CPM',
 'Battery voltage': 'Tension de la batterie',
 'Baud rate': 'Débit en bauds',
 'Below the typical time profile': 'En dessous du profil temporel typique',
 'Below warning threshold': 'Sous le seuil d’avertissement',
 'BfS and ICRP reference profiles convert annual dose values into continuous-rate equivalents for context. They are not official instantaneous alarm limits and cannot replace professional dose assessment.': 'Les '
                                                                                                                                                                                                               'profils '
                                                                                                                                                                                                               'de '
                                                                                                                                                                                                               'référence '
                                                                                                                                                                                                               'BfS '
                                                                                                                                                                                                               'et '
                                                                                                                                                                                                               'CIPR '
                                                                                                                                                                                                               'convertissent '
                                                                                                                                                                                                               'les '
                                                                                                                                                                                                               'doses '
                                                                                                                                                                                                               'annuelles '
                                                                                                                                                                                                               'en '
                                                                                                                                                                                                               'équivalents '
                                                                                                                                                                                                               'de '
                                                                                                                                                                                                               'débit '
                                                                                                                                                                                                               'continu '
                                                                                                                                                                                                               'à '
                                                                                                                                                                                                               'titre '
                                                                                                                                                                                                               'de '
                                                                                                                                                                                                               'contexte. '
                                                                                                                                                                                                               'Ce '
                                                                                                                                                                                                               'ne '
                                                                                                                                                                                                               'sont '
                                                                                                                                                                                                               'pas '
                                                                                                                                                                                                               'des '
                                                                                                                                                                                                               'seuils '
                                                                                                                                                                                                               'officiels '
                                                                                                                                                                                                               'd’alarme '
                                                                                                                                                                                                               'instantanée '
                                                                                                                                                                                                               'et '
                                                                                                                                                                                                               'ils '
                                                                                                                                                                                                               'ne '
                                                                                                                                                                                                               'remplacent '
                                                                                                                                                                                                               'pas '
                                                                                                                                                                                                               'une '
                                                                                                                                                                                                               'évaluation '
                                                                                                                                                                                                               'dosimétrique '
                                                                                                                                                                                                               'professionnelle.',
 'BfS reference projection': 'Projection de référence BfS',
 'Both connected counters show a quality-filtered simultaneous rise': 'Les deux compteurs connectés montrent une '
                                                                      'hausse simultanée filtrée par qualité',
 'Both connected counters show a simultaneous rise': 'Les deux compteurs connectés montrent une hausse simultanée',
 'Broadly compatible with Poisson-like spread': 'Globalement compatible avec une dispersion de type Poisson',
 'CPM': 'CPM',
 'CPM and derived dose rate': 'CPM et débit de dose dérivé',
 'CPM distribution and Poisson comparison': 'Distribution des CPM et comparaison de Poisson',
 'CPM distribution — {title}': 'Distribution des CPM — {title}',
 'CPM is the primary measurement.': 'Le CPM est la mesure principale.',
 'CPM per µSv/h': 'CPM par µSv/h',
 'CPM quality': 'Qualité CPM',
 'CPM statistics  min {minimum:.0f} | max {maximum:.0f} | mean {mean:.2f} | median {median:.2f} | SD {sd:.2f} | P95 {p95:.2f} | missing {missing}': 'Statistiques '
                                                                                                                                                    'CPM  '
                                                                                                                                                    'min '
                                                                                                                                                    '{minimum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'max '
                                                                                                                                                    '{maximum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'moyenne '
                                                                                                                                                    '{mean:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'médiane '
                                                                                                                                                    '{median:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'ET '
                                                                                                                                                    '{sd:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'P95 '
                                                                                                                                                    '{p95:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'manquants '
                                                                                                                                                    '{missing}',
 'CPM statistics: no accepted measurements in selected period': 'Statistiques CPM : aucune mesure acceptée pendant la '
                                                                'période sélectionnée',
 'CPM–pressure correlation': 'Corrélation CPM–pression',
 'CPM–temperature correlation': 'Corrélation CPM–température',
 'CPM–voltage correlation': 'Corrélation CPM–tension',
 'CSV files preserve every accepted measurement without interpolation. PNG reports include CPM, temperature, voltage, optional raw signed gyro diagnostics, summary statistics, sample completeness, device identity, timezone, period and generation time. ZIP bundles additionally contain analysis JSON, daily summaries, events, histogram, heatmap and a multi-page PDF report.': 'Les '
                                                                                                                                                                                                                                                                                                                                                                                       'fichiers '
                                                                                                                                                                                                                                                                                                                                                                                       'CSV '
                                                                                                                                                                                                                                                                                                                                                                                       'conservent '
                                                                                                                                                                                                                                                                                                                                                                                       'chaque '
                                                                                                                                                                                                                                                                                                                                                                                       'mesure '
                                                                                                                                                                                                                                                                                                                                                                                       'acceptée '
                                                                                                                                                                                                                                                                                                                                                                                       'sans '
                                                                                                                                                                                                                                                                                                                                                                                       'interpolation. '
                                                                                                                                                                                                                                                                                                                                                                                       'Les '
                                                                                                                                                                                                                                                                                                                                                                                       'rapports '
                                                                                                                                                                                                                                                                                                                                                                                       'PNG '
                                                                                                                                                                                                                                                                                                                                                                                       'incluent '
                                                                                                                                                                                                                                                                                                                                                                                       'les '
                                                                                                                                                                                                                                                                                                                                                                                       'CPM, '
                                                                                                                                                                                                                                                                                                                                                                                       'la '
                                                                                                                                                                                                                                                                                                                                                                                       'température, '
                                                                                                                                                                                                                                                                                                                                                                                       'la '
                                                                                                                                                                                                                                                                                                                                                                                       'tension, '
                                                                                                                                                                                                                                                                                                                                                                                       'les '
                                                                                                                                                                                                                                                                                                                                                                                       'diagnostics '
                                                                                                                                                                                                                                                                                                                                                                                       'gyroscopiques '
                                                                                                                                                                                                                                                                                                                                                                                       'bruts '
                                                                                                                                                                                                                                                                                                                                                                                       'signés '
                                                                                                                                                                                                                                                                                                                                                                                       'facultatifs, '
                                                                                                                                                                                                                                                                                                                                                                                       'les '
                                                                                                                                                                                                                                                                                                                                                                                       'statistiques '
                                                                                                                                                                                                                                                                                                                                                                                       'récapitulatives, '
                                                                                                                                                                                                                                                                                                                                                                                       'la '
                                                                                                                                                                                                                                                                                                                                                                                       'complétude, '
                                                                                                                                                                                                                                                                                                                                                                                       'l’identité '
                                                                                                                                                                                                                                                                                                                                                                                       'de '
                                                                                                                                                                                                                                                                                                                                                                                       'l’appareil, '
                                                                                                                                                                                                                                                                                                                                                                                       'le '
                                                                                                                                                                                                                                                                                                                                                                                       'fuseau '
                                                                                                                                                                                                                                                                                                                                                                                       'horaire, '
                                                                                                                                                                                                                                                                                                                                                                                       'la '
                                                                                                                                                                                                                                                                                                                                                                                       'période '
                                                                                                                                                                                                                                                                                                                                                                                       'et '
                                                                                                                                                                                                                                                                                                                                                                                       'l’heure '
                                                                                                                                                                                                                                                                                                                                                                                       'de '
                                                                                                                                                                                                                                                                                                                                                                                       'génération. '
                                                                                                                                                                                                                                                                                                                                                                                       'Les '
                                                                                                                                                                                                                                                                                                                                                                                       'archives '
                                                                                                                                                                                                                                                                                                                                                                                       'ZIP '
                                                                                                                                                                                                                                                                                                                                                                                       'contiennent '
                                                                                                                                                                                                                                                                                                                                                                                       'en '
                                                                                                                                                                                                                                                                                                                                                                                       'plus '
                                                                                                                                                                                                                                                                                                                                                                                       'le '
                                                                                                                                                                                                                                                                                                                                                                                       'JSON '
                                                                                                                                                                                                                                                                                                                                                                                       'd’analyse, '
                                                                                                                                                                                                                                                                                                                                                                                       'les '
                                                                                                                                                                                                                                                                                                                                                                                       'résumés '
                                                                                                                                                                                                                                                                                                                                                                                       'quotidiens, '
                                                                                                                                                                                                                                                                                                                                                                                       'les '
                                                                                                                                                                                                                                                                                                                                                                                       'événements, '
                                                                                                                                                                                                                                                                                                                                                                                       'l’histogramme, '
                                                                                                                                                                                                                                                                                                                                                                                       'la '
                                                                                                                                                                                                                                                                                                                                                                                       'carte '
                                                                                                                                                                                                                                                                                                                                                                                       'thermique '
                                                                                                                                                                                                                                                                                                                                                                                       'et '
                                                                                                                                                                                                                                                                                                                                                                                       'un '
                                                                                                                                                                                                                                                                                                                                                                                       'rapport '
                                                                                                                                                                                                                                                                                                                                                                                       'PDF '
                                                                                                                                                                                                                                                                                                                                                                                       'multipage.',
 'Calibrated acceleration': 'Accélération étalonnée',
 'Calibration profile': 'Profil d’étalonnage',
 'Capabilities': 'Capacités',
 'Check location, orientation and environmental conditions when a persistent jump appears.': 'Vérifiez l’emplacement, '
                                                                                             'l’orientation et les '
                                                                                             'conditions '
                                                                                             'environnementales '
                                                                                             'lorsqu’un changement '
                                                                                             'persistant apparaît.',
 'Check manually': 'Vérifier manuellement',
 'Check the Home Assistant general settings and restart the add-on.': 'Vérifiez les paramètres généraux de Home '
                                                                      'Assistant, puis redémarrez le module '
                                                                      'complémentaire.',
 'Check the USB cable and power supply if this continues for more than 15 minutes.': 'Vérifiez le câble USB et '
                                                                                     'l’alimentation si cela dure plus '
                                                                                     'de 15 minutes.',
 'Check the measurement conditions, observe the trend and verify the reading with an appropriate instrument if it persists.': 'Vérifiez '
                                                                                                                              'les '
                                                                                                                              'conditions '
                                                                                                                              'de '
                                                                                                                              'mesure, '
                                                                                                                              'observez '
                                                                                                                              'la '
                                                                                                                              'tendance '
                                                                                                                              'et '
                                                                                                                              'confirmez '
                                                                                                                              'la '
                                                                                                                              'valeur '
                                                                                                                              'avec '
                                                                                                                              'un '
                                                                                                                              'instrument '
                                                                                                                              'approprié '
                                                                                                                              'si '
                                                                                                                              'elle '
                                                                                                                              'persiste.',
 'Check the measurement location': 'Vérifier le lieu de mesure',
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
 'Choose how much detail the analysis cards show. The selection is stored in this browser.': 'Choisissez le niveau de '
                                                                                             'détail des cartes '
                                                                                             'd’analyse. Le choix est '
                                                                                             'enregistré dans ce '
                                                                                             'navigateur.',
 'Choose whether reports include all devices or one selected device.': 'Choisissez si les rapports incluent tous les '
                                                                       'appareils ou un seul appareil sélectionné.',
 'Clear': 'Clear',
 'Clearly above the usual local range': 'Nettement au-dessus de la plage locale habituelle',
 'Clearly elevated': 'Nettement élevé',
 'Clearly elevated: clearly above the usual local range': 'Nettement élevé : nettement au-dessus de la plage locale '
                                                          'habituelle',
 'Clock offset exceeds warning threshold': 'Le décalage de l’horloge dépasse le seuil d’avertissement',
 'Clock synchronized': 'Horloge synchronisée',
 'Close to Poisson expectation': 'Proche de l’attente de Poisson',
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
 'Compared with local baseline': 'Comparé à la référence locale',
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
 'Compares the current value with the usual background at this location.': 'Compare la valeur actuelle au fond '
                                                                           'habituel de cet emplacement.',
 'Comparison confidence': 'Confiance de la comparaison',
 'Complete ZIP bundle': 'Archive ZIP complète',
 'Complete history deletion failed': 'Complete history deletion failed',
 'Complete history deletion is disabled in the app configuration.': 'La suppression complète de l’historique est '
                                                                    'désactivée dans la configuration de '
                                                                    'l’application.',
 'Completeness: {value:.2f}%': 'Complétude : {value:.2f} %',
 'Confidence': 'Niveau de confiance',
 'Configured CPM conversion factor': 'Facteur de conversion CPM configuré',
 'Configured baud rate': 'Débit en bauds configuré',
 'Configured device name': 'Nom d’appareil configuré',
 'Configured location': 'Emplacement configuré',
 'Configured measurement interval': 'Intervalle de mesure configuré',
 'Confirmed original samples in 24 h · {accepted} stored': 'Confirmed original samples in 24 h · {accepted} stored',
 'Connect two devices to enable comparison.': 'Connectez deux appareils pour activer la comparaison.',
 'Connect two devices to learn a relative response factor.': 'Connect two devices to learn a relative response factor.',
 'Connected GMC devices': 'Appareils GMC connectés',
 'Connected counters without an active stability warning': 'Compteurs connectés sans avertissement actif de stabilité',
 'Connected devices': 'Appareils connectés',
 'Connection active': 'Connection active',
 'Consecutive upload errors': 'Erreurs d’envoi consécutives',
 'Continue observing': 'Poursuivre la surveillance',
 'Coordinates': 'Coordonnées',
 'Correlation': 'Corrélation',
 'Correlation does not imply causation. Strong values should be investigated over longer periods before drawing conclusions.': 'Une '
                                                                                                                               'corrélation '
                                                                                                                               'n’implique '
                                                                                                                               'pas '
                                                                                                                               'une '
                                                                                                                               'causalité. '
                                                                                                                               'Les '
                                                                                                                               'valeurs '
                                                                                                                               'fortes '
                                                                                                                               'doivent '
                                                                                                                               'être '
                                                                                                                               'étudiées '
                                                                                                                               'sur '
                                                                                                                               'des '
                                                                                                                               'périodes '
                                                                                                                               'plus '
                                                                                                                               'longues '
                                                                                                                               'avant '
                                                                                                                               'toute '
                                                                                                                               'conclusion.',
 'Cosmic influence is possible': 'Une influence cosmique est possible',
 'Cosmic influence – statistical indication': 'Influence cosmique – indication statistique',
 'Counter ID': 'Identifiant du compteur',
 'Counting statistics': 'Statistiques de comptage',
 'Counting uncertainty (68%): −{minus:.2f}/+{plus:.2f} CPM · {impulses} impulses in {duration}': 'Counting uncertainty '
                                                                                                 '(68%): '
                                                                                                 '−{minus:.2f}/+{plus:.2f} '
                                                                                                 'CPM · {impulses} '
                                                                                                 'impulses in '
                                                                                                 '{duration}',
 'Counting uncertainty not available': 'Counting uncertainty not available',
 'Country': 'Pays',
 'Coverage percent': 'Couverture en pourcentage',
 'Coverage, gaps, runtime counters and derived dose-rate values': 'Couverture, lacunes, compteurs d’exécution et '
                                                                  'débits de dose dérivés',
 'Critical': 'Critique',
 'Critical: danger threshold exceeded': 'Critique : seuil de danger dépassé',
 'Current': 'Actuel',
 'Current air pressure': 'Pression atmosphérique actuelle',
 'Current database size': 'Current database size',
 'Current difference': 'Écart actuel',
 'Current value': 'Valeur actuelle',
 'Current value is {z:+.2f} robust standard deviations from the 24 h median': 'La valeur actuelle se situe à {z:+.2f} '
                                                                              'écarts-types robustes de la médiane sur '
                                                                              '24 h',
 'Current value is {z:+.2f} standard deviations from the 24 h mean': 'La valeur actuelle se situe à {z:+.2f} '
                                                                     'écarts-types de la moyenne sur 24 h',
 'Current week bundle': 'Archive de la semaine en cours',
 'Currently selected': 'Actuellement sélectionné',
 'Custom period': 'Période personnalisée',
 'Custom thresholds': 'Seuils personnalisés',
 'Daily and weekly profile is still being formed': 'Le profil quotidien et hebdomadaire est encore en cours de '
                                                   'formation',
 'Daily quality-filtered medians are smoothed over seven days. The period cards compare the recent part of each period with the preceding part; detected jumps are statistical changes and do not determine their cause.': 'Les '
                                                                                                                                                                                                                           'médianes '
                                                                                                                                                                                                                           'quotidiennes '
                                                                                                                                                                                                                           'filtrées '
                                                                                                                                                                                                                           'selon '
                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                           'qualité '
                                                                                                                                                                                                                           'sont '
                                                                                                                                                                                                                           'lissées '
                                                                                                                                                                                                                           'sur '
                                                                                                                                                                                                                           'sept '
                                                                                                                                                                                                                           'jours. '
                                                                                                                                                                                                                           'Les '
                                                                                                                                                                                                                           'cartes '
                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                           'période '
                                                                                                                                                                                                                           'comparent '
                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                           'partie '
                                                                                                                                                                                                                           'récente '
                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                           'chaque '
                                                                                                                                                                                                                           'période '
                                                                                                                                                                                                                           'à '
                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                           'partie '
                                                                                                                                                                                                                           'précédente '
                                                                                                                                                                                                                           '; '
                                                                                                                                                                                                                           'les '
                                                                                                                                                                                                                           'ruptures '
                                                                                                                                                                                                                           'détectées '
                                                                                                                                                                                                                           'sont '
                                                                                                                                                                                                                           'des '
                                                                                                                                                                                                                           'changements '
                                                                                                                                                                                                                           'statistiques '
                                                                                                                                                                                                                           'et '
                                                                                                                                                                                                                           'n’en '
                                                                                                                                                                                                                           'déterminent '
                                                                                                                                                                                                                           'pas '
                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                           'cause.',
 'Daily summary CSV': 'CSV de résumé quotidien',
 'Danger threshold exceeded': 'Seuil de danger dépassé',
 'Danger thresholds': 'Seuils de danger',
 'Danger zone': 'Danger zone',
 'Dashboard navigation': 'Dashboard navigation',
 'Data exports': 'Exports de données',
 'Data period': 'Data period',
 'Data quality': 'Qualité des données',
 'Data quality is too low for a reliable assessment': 'La qualité des données est trop faible pour une évaluation '
                                                      'fiable',
 'Data quality status unavailable': 'État de qualité des données indisponible',
 'Data quality: {value}': 'Qualité des données : {value}',
 'Database': 'Database',
 'Database health': 'État de la base de données',
 'Database size': 'Taille de la base',
 'Date': 'Date',
 'Delete all GMC history': 'Delete all GMC history',
 'Delete history': 'Delete history',
 'Deletion confirmation text must be exactly DELETE ALL GMC HISTORY': 'Deletion confirmation text must be exactly '
                                                                      'DELETE ALL GMC HISTORY',
 'Deletion is disabled by default.': 'Deletion is disabled by default.',
 'Derived dose rate': 'Débit de dose dérivé',
 'Derived from 1 h mean CPM': 'Dérivé de la moyenne CPM sur 1 h',
 'Derived from 24 h mean CPM': 'Dérivé de la moyenne CPM sur 24 h',
 'Derived from 7 d mean CPM': 'Dérivé de la moyenne CPM sur 7 jours',
 'Derived from latest CPM': 'Dérivé du dernier CPM',
 'Detailed interpretation and the most useful supporting values': 'Interprétation détaillée et valeurs justificatives '
                                                                  'les plus utiles',
 'Detect, identify and assign GMC counters': 'Detect, identify and assign GMC counters',
 'Detected': 'Détectée',
 'Detected Capabilities': 'Fonctions détectées',
 'Detected GMC device': 'Detected GMC device',
 'Detected baseline jumps': 'Sauts de référence détectés',
 'Detected relative anomaly events: {count}': 'Événements d’anomalie relative détectés : {count}',
 'Deviation': 'Écart',
 'Device': 'Appareil',
 'Device Profile': 'Profil de l’appareil',
 'Device Time Errors Since Start': 'Erreurs d’heure de l’appareil depuis le démarrage',
 'Device assignments saved': 'Device assignments saved',
 'Device assignments were saved.': 'Device assignments were saved.',
 'Device baseline': 'Référence de l’appareil',
 'Device capabilities': 'Fonctions de l’appareil',
 'Device clock': 'Horloge de l’appareil',
 'Device clock offset': 'Décalage de l’horloge de l’appareil',
 'Device clock status': 'État de l’horloge de l’appareil',
 'Device clock unavailable': 'Horloge de l’appareil indisponible',
 'Device clock warning': 'Device clock warning',
 'Device comparison': 'Comparaison des appareils',
 'Device details, live values and analysis selection are shown below.': 'Les détails, les valeurs actuelles et la '
                                                                        'sélection d’analyse de chaque appareil sont '
                                                                        'affichés ci-dessous.',
 'Device health warning': 'Device health warning',
 'Device position': 'Position de l’appareil',
 'Device status updated': 'Device status updated',
 'Device temperature is unavailable.': 'La température de l’appareil n’est pas disponible.',
 'Device time': 'Heure de l’appareil',
 'Device-specific details are listed above.': 'Les détails propres à chaque appareil figurent dans la section '
                                              'ci-dessus.',
 'Device: {value}': 'Appareil : {value}',
 'Devices': 'Devices',
 'Diagnostics JSON': 'JSON de diagnostic',
 'Disabled': 'Désactivé',
 'Discarded CPM peaks': 'Discarded CPM peaks',
 'Discarded unconfirmed CPM peaks': 'Discarded unconfirmed CPM peaks',
 'Display down': 'À plat, écran vers le bas',
 'Display up': 'À plat, écran vers le haut',
 'Dose rate = CPM / configured conversion factor ({factor:g} CPM per µSv/h).': 'Débit de dose = CPM / facteur de '
                                                                               'conversion configuré ({factor:g} CPM '
                                                                               'par µSv/h).',
 'Dose rate formula explanation': 'Débit de dose = CPM / facteur de conversion configuré ({factor:g} CPM par µSv/h).',
 'Dose-rate values are derived from CPM using the configured conversion factor.': 'Les débits de dose sont dérivés des '
                                                                                  'CPM avec le facteur de conversion '
                                                                                  'configuré.',
 'Dose-rate values, traffic-light states and events are derived indicators. CPM remains the primary measurement.': 'Les '
                                                                                                                   'débits '
                                                                                                                   'de '
                                                                                                                   'dose, '
                                                                                                                   'les '
                                                                                                                   'états '
                                                                                                                   'du '
                                                                                                                   'feu '
                                                                                                                   'et '
                                                                                                                   'les '
                                                                                                                   'événements '
                                                                                                                   'sont '
                                                                                                                   'des '
                                                                                                                   'indicateurs '
                                                                                                                   'dérivés. '
                                                                                                                   'Le '
                                                                                                                   'CPM '
                                                                                                                   'reste '
                                                                                                                   'la '
                                                                                                                   'mesure '
                                                                                                                   'principale.',
 'Download': 'Télécharger',
 'Downloads': 'Téléchargements',
 'Dual-tube measurement': 'Mesure à deux tubes',
 'Duration [s]': 'Durée [s]',
 'During the learning phase, leave the counters in a stable location and allow additional measurements to accumulate.': 'Pendant '
                                                                                                                        'la '
                                                                                                                        'phase '
                                                                                                                        'd’apprentissage, '
                                                                                                                        'laissez '
                                                                                                                        'les '
                                                                                                                        'compteurs '
                                                                                                                        'dans '
                                                                                                                        'un '
                                                                                                                        'emplacement '
                                                                                                                        'stable '
                                                                                                                        'et '
                                                                                                                        'laissez '
                                                                                                                        's’accumuler '
                                                                                                                        'davantage '
                                                                                                                        'de '
                                                                                                                        'mesures.',
 'Each device has its own MQTT identity and history. The cards show the latest accepted measurement.': 'Chaque '
                                                                                                       'appareil '
                                                                                                       'possède sa '
                                                                                                       'propre '
                                                                                                       'identité MQTT '
                                                                                                       'et son propre '
                                                                                                       'historique. '
                                                                                                       'Les cartes '
                                                                                                       'affichent la '
                                                                                                       'dernière '
                                                                                                       'mesure '
                                                                                                       'acceptée.',
 'Each physical serial device can only be assigned once': 'Each physical serial device can only be assigned once',
 'Elevated': 'Élevé',
 'Elevated relative background': 'Fond relatif élevé',
 'Elevated: within warning range': 'Élevé : dans la plage d’avertissement',
 'Elevation': 'Altitude',
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
 'Enable enable_restore in the app configuration and restart only when a restore is planned.': 'Activez enable_restore '
                                                                                               'dans la configuration '
                                                                                               'de l’application et '
                                                                                               'redémarrez uniquement '
                                                                                               'lorsqu’une '
                                                                                               'restauration est '
                                                                                               'prévue.',
 'Enable “{setting}” in the app configuration and restart only when a restore is planned.': 'Activez « {setting} » '
                                                                                            'dans la configuration de '
                                                                                            'l’application et '
                                                                                            'redémarrez uniquement '
                                                                                            'lorsqu’une restauration '
                                                                                            'est prévue.',
 'End time UTC': 'Heure de fin UTC',
 'End time local': 'Heure de fin locale',
 'Entities': 'Entités',
 'Environment': 'Environnement',
 'Error time': 'Heure de l’erreur',
 'Estimated pressure influence': 'Influence estimée de la pression',
 'Evaluated by': 'Évalué selon',
 'Evaluates the current value using the configured thresholds.': 'Évalue la valeur actuelle selon les seuils '
                                                                 'configurés.',
 'Events CSV': 'CSV des événements',
 'Events and diagnostics': 'Events and diagnostics',
 'Events last 24 h': 'Événements des dernières 24 h',
 'Excellent': 'Excellente',
 'Excluded measurements': 'Mesures exclues',
 'Excluded pairs': 'Paires exclues',
 'Expand all': 'Expand all',
 'Expected samples': 'Mesures attendues',
 'Expert view': 'Vue experte',
 'Explanation of the two assessments': 'Explication des deux évaluations',
 'Export details': 'Détails des exports',
 'Extremely elevated': 'Extrêmement élevé',
 'Extremely elevated: far above the usual local range': 'Extrêmement élevé : très au-dessus de la plage locale '
                                                        'habituelle',
 'Falling': 'En baisse',
 'Falling air pressure can slightly increase the share of cosmically generated secondary radiation at ground level, while rising air pressure tends to reduce it; the model detects only such statistical relationships and cannot clearly distinguish them from other natural influences.': 'Une '
                                                                                                                                                                                                                                                                                             'baisse '
                                                                                                                                                                                                                                                                                             'de '
                                                                                                                                                                                                                                                                                             'la '
                                                                                                                                                                                                                                                                                             'pression '
                                                                                                                                                                                                                                                                                             'atmosphérique '
                                                                                                                                                                                                                                                                                             'peut '
                                                                                                                                                                                                                                                                                             'légèrement '
                                                                                                                                                                                                                                                                                             'augmenter '
                                                                                                                                                                                                                                                                                             'la '
                                                                                                                                                                                                                                                                                             'part '
                                                                                                                                                                                                                                                                                             'du '
                                                                                                                                                                                                                                                                                             'rayonnement '
                                                                                                                                                                                                                                                                                             'secondaire '
                                                                                                                                                                                                                                                                                             'd’origine '
                                                                                                                                                                                                                                                                                             'cosmique '
                                                                                                                                                                                                                                                                                             'au '
                                                                                                                                                                                                                                                                                             'niveau '
                                                                                                                                                                                                                                                                                             'du '
                                                                                                                                                                                                                                                                                             'sol, '
                                                                                                                                                                                                                                                                                             'tandis '
                                                                                                                                                                                                                                                                                             'qu’une '
                                                                                                                                                                                                                                                                                             'hausse '
                                                                                                                                                                                                                                                                                             'tend '
                                                                                                                                                                                                                                                                                             'à '
                                                                                                                                                                                                                                                                                             'la '
                                                                                                                                                                                                                                                                                             'réduire '
                                                                                                                                                                                                                                                                                             '; '
                                                                                                                                                                                                                                                                                             'le '
                                                                                                                                                                                                                                                                                             'modèle '
                                                                                                                                                                                                                                                                                             'ne '
                                                                                                                                                                                                                                                                                             'détecte '
                                                                                                                                                                                                                                                                                             'que '
                                                                                                                                                                                                                                                                                             'de '
                                                                                                                                                                                                                                                                                             'telles '
                                                                                                                                                                                                                                                                                             'relations '
                                                                                                                                                                                                                                                                                             'statistiques '
                                                                                                                                                                                                                                                                                             'et '
                                                                                                                                                                                                                                                                                             'ne '
                                                                                                                                                                                                                                                                                             'peut '
                                                                                                                                                                                                                                                                                             'pas '
                                                                                                                                                                                                                                                                                             'les '
                                                                                                                                                                                                                                                                                             'distinguer '
                                                                                                                                                                                                                                                                                             'clairement '
                                                                                                                                                                                                                                                                                             'd’autres '
                                                                                                                                                                                                                                                                                             'influences '
                                                                                                                                                                                                                                                                                             'naturelles.',
 'Falling air pressure is often associated with a slightly higher intensity of cosmically generated secondary radiation at ground level, while rising air pressure is associated with a slightly lower intensity. The strength of this relationship depends on detector, location and atmosphere; the cause cannot be determined unambiguously from total counts.': 'Une '
                                                                                                                                                                                                                                                                                                                                                                    'baisse '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'la '
                                                                                                                                                                                                                                                                                                                                                                    'pression '
                                                                                                                                                                                                                                                                                                                                                                    'atmosphérique '
                                                                                                                                                                                                                                                                                                                                                                    'est '
                                                                                                                                                                                                                                                                                                                                                                    'souvent '
                                                                                                                                                                                                                                                                                                                                                                    'associée '
                                                                                                                                                                                                                                                                                                                                                                    'à '
                                                                                                                                                                                                                                                                                                                                                                    'une '
                                                                                                                                                                                                                                                                                                                                                                    'intensité '
                                                                                                                                                                                                                                                                                                                                                                    'légèrement '
                                                                                                                                                                                                                                                                                                                                                                    'plus '
                                                                                                                                                                                                                                                                                                                                                                    'élevée '
                                                                                                                                                                                                                                                                                                                                                                    'du '
                                                                                                                                                                                                                                                                                                                                                                    'rayonnement '
                                                                                                                                                                                                                                                                                                                                                                    'secondaire '
                                                                                                                                                                                                                                                                                                                                                                    'd’origine '
                                                                                                                                                                                                                                                                                                                                                                    'cosmique '
                                                                                                                                                                                                                                                                                                                                                                    'au '
                                                                                                                                                                                                                                                                                                                                                                    'sol, '
                                                                                                                                                                                                                                                                                                                                                                    'tandis '
                                                                                                                                                                                                                                                                                                                                                                    'qu’une '
                                                                                                                                                                                                                                                                                                                                                                    'hausse '
                                                                                                                                                                                                                                                                                                                                                                    'est '
                                                                                                                                                                                                                                                                                                                                                                    'associée '
                                                                                                                                                                                                                                                                                                                                                                    'à '
                                                                                                                                                                                                                                                                                                                                                                    'une '
                                                                                                                                                                                                                                                                                                                                                                    'intensité '
                                                                                                                                                                                                                                                                                                                                                                    'légèrement '
                                                                                                                                                                                                                                                                                                                                                                    'plus '
                                                                                                                                                                                                                                                                                                                                                                    'faible. '
                                                                                                                                                                                                                                                                                                                                                                    'La '
                                                                                                                                                                                                                                                                                                                                                                    'force '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'cette '
                                                                                                                                                                                                                                                                                                                                                                    'relation '
                                                                                                                                                                                                                                                                                                                                                                    'dépend '
                                                                                                                                                                                                                                                                                                                                                                    'du '
                                                                                                                                                                                                                                                                                                                                                                    'détecteur, '
                                                                                                                                                                                                                                                                                                                                                                    'du '
                                                                                                                                                                                                                                                                                                                                                                    'lieu '
                                                                                                                                                                                                                                                                                                                                                                    'et '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'l’atmosphère '
                                                                                                                                                                                                                                                                                                                                                                    '; '
                                                                                                                                                                                                                                                                                                                                                                    'les '
                                                                                                                                                                                                                                                                                                                                                                    'comptages '
                                                                                                                                                                                                                                                                                                                                                                    'totaux '
                                                                                                                                                                                                                                                                                                                                                                    'ne '
                                                                                                                                                                                                                                                                                                                                                                    'permettent '
                                                                                                                                                                                                                                                                                                                                                                    'pas '
                                                                                                                                                                                                                                                                                                                                                                    'd’en '
                                                                                                                                                                                                                                                                                                                                                                    'déterminer '
                                                                                                                                                                                                                                                                                                                                                                    'la '
                                                                                                                                                                                                                                                                                                                                                                    'cause '
                                                                                                                                                                                                                                                                                                                                                                    'sans '
                                                                                                                                                                                                                                                                                                                                                                    'ambiguïté.',
 'Fano factor': 'Facteur de Fano',
 'Fano factor = variance / mean; a value near 1 is consistent with Poisson-like counting statistics.': 'Facteur de '
                                                                                                       'Fano = '
                                                                                                       'variance / '
                                                                                                       'moyenne ; une '
                                                                                                       'valeur proche '
                                                                                                       'de 1 est '
                                                                                                       'compatible '
                                                                                                       'avec un '
                                                                                                       'comptage de '
                                                                                                       'type Poisson.',
 'Fano factor formula explanation': 'Facteur de Fano = variance / moyenne ; une valeur proche de 1 est compatible avec '
                                    'un comptage de type Poisson.',
 'Fano factor: {value}': 'Facteur de Fano : {value}',
 'Far above the usual local range': 'Très au-dessus de la plage locale habituelle',
 'File size': 'File size',
 'Firmware version': 'Version du micrologiciel',
 'Flat': 'Flat',
 'Fleet intelligence': 'Analyse du parc d’appareils',
 'Format': 'Format',
 'Fri': 'Ven',
 'Friday': 'Vendredi',
 'Full history ZIP': 'ZIP de l’historique complet',
 'GMC Radiation Monitor': 'Moniteur de rayonnement GMC',
 'GMC Radiation Monitoring': 'Surveillance du rayonnement GMC',
 'GMC Reports': 'Rapports GMC',
 'GMC analysis report {period}': 'Rapport d’analyse GMC {period}',
 'GMC detected': 'GMC detected',
 'GMC devices are being detected automatically': 'GMC devices are being detected automatically',
 'GMC radiation analysis report': 'Rapport d’analyse du rayonnement GMC',
 'GMC radiation monitoring report {period}': 'Rapport de surveillance du rayonnement GMC {period}',
 'GMC-300/320 family': 'Famille GMC-300/320',
 'GMC-320 and GMC-500+ combined': 'GMC-320 and GMC-500+ combined',
 'GMC-500 family': 'Famille GMC-500',
 'GMC-600 family': 'Famille GMC-600',
 'GMCMap consecutive upload errors': 'Erreurs d’envoi GMCMap consécutives',
 'GMCMap counter ID': 'Identifiant de compteur GMCMap',
 'GMCMap is enabled, but this device has no counter ID mapping.': 'GMCMap est activé, mais aucun identifiant de '
                                                                  'compteur n’est associé à cet appareil.',
 'GMCMap last HTTP status': 'Dernier état HTTP GMCMap',
 'GMCMap last error time': 'Heure de la dernière erreur GMCMap',
 'GMCMap last server response': 'Dernière réponse du serveur GMCMap',
 'GMCMap last successful upload': 'Dernier envoi GMCMap réussi',
 'GMCMap last upload attempt': 'Dernière tentative d’envoi GMCMap',
 'GMCMap last upload error': 'Dernière erreur d’envoi GMCMap',
 'GMCMap last uploaded CPM': 'Dernier CPM envoyé à GMCMap',
 'GMCMap next upload': 'Prochain envoi GMCMap',
 'GMCMap successful uploads since start': 'Envois GMCMap réussis depuis le démarrage',
 'GMCMap upload errors since start': 'Erreurs d’envoi GMCMap depuis le démarrage',
 'GMCMap upload status': 'État de l’envoi GMCMap',
 'GQ manufacturer recommendation': 'Recommandation du fabricant GQ',
 'Gaps are excluded from effective counting time': 'Gaps are excluded from effective counting time',
 'Generated export exceeds the {limit_mib} MiB safety limit': 'L’export généré dépasse la limite de sécurité de '
                                                              '{limit_mib} Mio.',
 'Generated maintenance export exceeds the 128 MiB safety limit': 'L’export de maintenance généré dépasse la limite de '
                                                                  'sécurité de 128 Mio.',
 'Generated report exceeds the 64 MiB safety limit': 'Le rapport généré dépasse la limite de sécurité de 64 Mio',
 'Generic GQ GMC / RFC1201-compatible device': 'Appareil GQ GMC générique compatible RFC1201',
 'Generic RFC1201-compatible device': 'Appareil générique compatible RFC1201',
 'Global report settings': 'Paramètres globaux des rapports et des exports',
 'Good': 'Bonne',
 'Green': 'Vert',
 'Gyro Calibrated {axis}': 'Gyro Calibrated {axis}',
 'Gyro Errors Since Start': 'Erreurs gyroscopiques depuis le démarrage',
 'Gyro Raw {axis}': 'Valeur gyro brute {axis}',
 'Gyro X': 'Gyro X',
 'Gyro Y': 'Gyro Y',
 'Gyro Z': 'Gyro Z',
 'Gyro data will be included when available.': 'Les données gyroscopiques seront incluses lorsqu’elles sont '
                                               'disponibles.',
 'Gyro errors': 'Erreurs du gyroscope',
 'Gyro recording is disabled.': 'L’enregistrement gyroscopique est désactivé.',
 'Gyroscope': 'Gyroscope',
 'Hardware model': 'Modèle matériel',
 'Heartbeat Errors Since Start': 'Erreurs de heartbeat depuis le démarrage',
 'Heartbeat mode': 'Mode heartbeat',
 'Heartbeat rolling 60 s CPM': 'CPM glissantes sur 60 s du heartbeat',
 'Heatmap PNG': 'Carte thermique PNG',
 'Heuristic statistical assessment; not a radiation-protection classification.': 'Évaluation statistique heuristique ; '
                                                                                 'ce n’est pas une classification de '
                                                                                 'radioprotection.',
 'High': 'Élevé',
 'High relative increase': 'Forte hausse relative',
 'High-dose Tube CPM': 'Tube haute dose CPM',
 'High-dose tube': 'Tube haute dose',
 'Highest stored 24 h value': 'Valeur maximale enregistrée sur 24 h',
 'Histogram PNG': 'Histogramme PNG',
 'Historical chart is still being formed': 'Le graphique historique est encore en cours de constitution',
 'Historical development': 'Évolution historique',
 'History': 'History',
 'History Write Errors Since Start': 'Erreurs d’écriture de l’historique depuis le démarrage',
 'History deleted': 'History deleted',
 'History maintenance': 'Gestion de l’historique',
 'History restore failed': 'Échec de la restauration de l’historique',
 'History restore is disabled. Enable enable_restore in the app configuration and restart.': 'La restauration de '
                                                                                             'l’historique est '
                                                                                             'désactivée. Activez '
                                                                                             'enable_restore dans la '
                                                                                             'configuration de '
                                                                                             'l’application et '
                                                                                             'redémarrez.',
 'History restore is disabled. Enable “{setting}” in the app configuration and restart.': 'La restauration de '
                                                                                          'l’historique est '
                                                                                          'désactivée. Activez « '
                                                                                          '{setting} » dans la '
                                                                                          'configuration de '
                                                                                          'l’application et '
                                                                                          'redémarrez.',
 'History storage warning': 'History storage warning',
 'Home Assistant API client is not configured': 'Home Assistant API client is not configured',
 'Home Assistant Recorder entity patterns': 'Home Assistant Recorder entity patterns',
 'Home Assistant Recorder history cleared': 'Home Assistant Recorder history cleared',
 'Home Assistant host UART': 'Home Assistant host UART',
 'Home Assistant location': 'Emplacement Home Assistant',
 'How are connected counters compared?': 'Comment les compteurs connectés sont-ils comparés ?',
 'How closely the observed spread resembles Poisson-like counting': 'À quel point la dispersion observée ressemble à '
                                                                    'un comptage de type Poisson',
 'How is data quality evaluated?': 'Comment la qualité des données est-elle évaluée ?',
 'How is the background profile calculated?': 'Comment le profil de fond est-il calculé ?',
 'How is the pressure relationship assessed?': 'Comment la relation avec la pression est-elle évaluée ?',
 'However, the value is noticeably above the usual local background. Observe the trend.': 'La valeur est toutefois '
                                                                                          'sensiblement supérieure au '
                                                                                          'fond local habituel. '
                                                                                          'Surveillez la tendance.',
 'ICRP reference projection': 'Projection de référence CIPR',
 'Inclination': 'Inclinaison',
 'Ingest diagnostics cleared': 'Ingest diagnostics cleared',
 'Inspecting backup…': 'Inspecting backup…',
 'Insufficient': 'Insuffisant',
 'Insufficient history for level-shift detection': 'Insufficient history for level-shift detection',
 'Insufficient paired daily values': 'Valeurs quotidiennes comparables insuffisantes',
 'Integrity': 'Intégrité',
 'Intelligence': 'Intelligence',
 'Intelligent radiation analysis': 'Analyse intelligente du rayonnement',
 'Internal database cleared': 'Internal database cleared',
 'Internal serial port': 'Internal serial port',
 'Interpret statistics with coverage in mind': 'Interpréter les statistiques en tenant compte de la couverture',
 'Interpret these values together with coverage, device stability and the historical background.': 'Interprétez ces '
                                                                                                   'valeurs avec la '
                                                                                                   'couverture, la '
                                                                                                   'stabilité de '
                                                                                                   'l’appareil et le '
                                                                                                   'fond historique.',
 'Interpretation': 'Interprétation',
 'Interval diagnostics': 'Diagnostic des intervalles',
 'Invalid deletion confirmation': 'Invalid deletion confirmation',
 'Invalid device clock response': 'Réponse d’horloge de l’appareil invalide',
 'Invalid request parameters': 'Paramètres de requête non valides.',
 'Invalid serial configuration request': 'Invalid serial configuration request',
 'Keep both counters close together and similarly oriented when using the comparison as a reference.': 'Gardez les '
                                                                                                       'deux compteurs '
                                                                                                       'proches et '
                                                                                                       'orientés de '
                                                                                                       'manière '
                                                                                                       'similaire '
                                                                                                       'lorsque vous '
                                                                                                       'utilisez la '
                                                                                                       'comparaison '
                                                                                                       'comme '
                                                                                                       'référence.',
 'Known radio or Zigbee adapter': 'Known radio or Zigbee adapter',
 'Language': 'Langue',
 'Last HTTP status': 'Dernier état HTTP',
 'Last Successful Measurement': 'Dernière mesure réussie',
 'Last attempt': 'Dernière tentative',
 'Last backup requested in this browser': 'Last backup requested in this browser',
 'Last sample age': 'Âge de la dernière mesure',
 'Last server response': 'Dernière réponse du serveur',
 'Last successful storage': 'Last successful storage',
 'Last update': 'Dernière mise à jour',
 'Last upload': 'Dernier envoi',
 'Last upload error': 'Dernière erreur d’envoi',
 'Latest CPM': 'CPM actuels',
 'Latest CPM uncertainty': 'Latest CPM uncertainty',
 'Latest CPM vs 24 h distribution': 'Dernier CPM comparé à la distribution sur 24 h',
 'Latest accepted value': 'Latest accepted value',
 'Latest dose rate': 'Débit de dose actuel',
 'Latest measurement': 'Dernière mesure',
 'Learned Radiation Baseline': 'Niveau de référence du rayonnement appris',
 'Learned from local history': 'Apprise à partir de l’historique local',
 'Learned pressure coefficient': 'Coefficient de pression appris',
 'Learning baseline': 'Apprentissage du niveau de référence',
 'Learning basis': 'Base d’apprentissage',
 'Learning progress': 'Progression de l’apprentissage',
 'Learning: not enough local history yet': 'Apprentissage : historique local encore insuffisant',
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
 'Less variable than Poisson expectation': 'Moins variable que l’attente de Poisson',
 'Likely device-specific deviation': 'Écart probablement propre à l’appareil',
 'Limited': 'Limitée',
 'Live radiation CPS': 'CPS de rayonnement en direct',
 'Live system status': 'Live system status',
 'Local background analysis': 'Analyse du fond local',
 'Local background is still being learned': 'Le fond local est encore en cours d’apprentissage',
 'Local background model is available': 'Le modèle du fond local est disponible',
 'Local baseline': 'Référence locale',
 'Local hour': 'Heure locale',
 'Local time [{timezone}]': 'Heure locale [{timezone}]',
 'Local timestamp': 'Horodatage local',
 'Location data comes from the Home Assistant general settings and is not sent to an external geocoding service.': 'Les '
                                                                                                                   'données '
                                                                                                                   'de '
                                                                                                                   'localisation '
                                                                                                                   'proviennent '
                                                                                                                   'des '
                                                                                                                   'paramètres '
                                                                                                                   'généraux '
                                                                                                                   'de '
                                                                                                                   'Home '
                                                                                                                   'Assistant '
                                                                                                                   'et '
                                                                                                                   'ne '
                                                                                                                   'sont '
                                                                                                                   'envoyées '
                                                                                                                   'à '
                                                                                                                   'aucun '
                                                                                                                   'service '
                                                                                                                   'externe '
                                                                                                                   'de '
                                                                                                                   'géocodage.',
 'Location unavailable': 'Emplacement indisponible',
 'Long-term context': 'Contexte à long terme',
 'Long-term drift': 'Dérive à long terme',
 'Long-term relative factor available': 'Long-term relative factor available',
 'Long-term relative response': 'Long-term relative response',
 'Longest gap': 'Plus longue interruption',
 'Longest gap [s]': 'Plus longue lacune [s]',
 'Longest gap: {seconds} s': 'Plus longue lacune : {seconds} s',
 'Low': 'Faible',
 'Low-dose Tube CPM': 'Tube basse dose CPM',
 'Low-dose tube': 'Tube faible dose',
 'Lowest stored 24 h value': 'Valeur minimale enregistrée sur 24 h',
 'Machine-readable statistics and event data': 'Statistiques et données d’événements lisibles par machine',
 'Maximum': 'Maximum',
 'Maximum CPM': 'CPM maximal',
 'Maximum background index [%]': 'Indice de fond maximal [%]',
 'Mean': 'Moyenne',
 'Mean CPM': 'CPM moyen',
 'Mean CPM by weekday and hour — {title}': 'CPM moyen par jour et par heure — {title}',
 'Mean absolute difference': 'Écart absolu moyen',
 'Mean: {value} CPM': 'Moyenne : {value} CPM',
 'Measurement interval': 'Intervalle de mesure',
 'Measurement-site baseline': 'Référence fusionnée du lieu de mesure',
 'Measurements': 'Measurements',
 'Measurements are sent to the public GMCMap service.': 'Les mesures sont envoyées au service public GMCMap.',
 'Measurements to delete': 'Measurements to delete',
 'Median': 'Médiane',
 'Median CPM': 'CPM médian',
 'Median: {value} CPM': 'Médiane : {value} CPM',
 'Medium': 'Moyen',
 'Merge a compatible SQLite backup into the current history. Existing rows are preserved or updated by device serial and UTC timestamp.': 'Fusionner '
                                                                                                                                          'une '
                                                                                                                                          'sauvegarde '
                                                                                                                                          'SQLite '
                                                                                                                                          'compatible '
                                                                                                                                          'avec '
                                                                                                                                          'l’historique '
                                                                                                                                          'actuel. '
                                                                                                                                          'Les '
                                                                                                                                          'lignes '
                                                                                                                                          'existantes '
                                                                                                                                          'sont '
                                                                                                                                          'conservées '
                                                                                                                                          'ou '
                                                                                                                                          'mises '
                                                                                                                                          'à '
                                                                                                                                          'jour '
                                                                                                                                          'selon '
                                                                                                                                          'le '
                                                                                                                                          'numéro '
                                                                                                                                          'de '
                                                                                                                                          'série '
                                                                                                                                          'et '
                                                                                                                                          'l’horodatage '
                                                                                                                                          'UTC.',
 'Merged {rows} measurement rows from schema {schema}.': '{rows} lignes de mesures du schéma {schema} ont été '
                                                         'fusionnées.',
 'Minimum / maximum: {minimum} / {maximum} CPM': 'Minimum / maximum : {minimum} / {maximum} CPM',
 'Minimum CPM': 'CPM minimal',
 'Mixed device profiles': 'Profils d’appareils mixtes',
 'Moderate linear relationship': 'Relation linéaire modérée',
 'Mon': 'Lun',
 'Monday': 'Lundi',
 'More history is needed before the relative background indicator is classified.': 'Davantage d’historique est '
                                                                                   'nécessaire avant de classer '
                                                                                   'l’indicateur de fond relatif.',
 'More history is needed; approximately {count} additional measurements are required.': 'More history is needed; '
                                                                                        'approximately {count} '
                                                                                        'additional measurements are '
                                                                                        'required.',
 'More measurements are needed for this weekday and hour.': 'Davantage de mesures sont nécessaires pour ce jour et '
                                                            'cette heure.',
 'More variable than Poisson expectation': 'Plus variable que l’attente de Poisson',
 'Move away from the suspected source if safe to do so, avoid unnecessary exposure and seek qualified radiation-protection advice.': 'Éloignez-vous '
                                                                                                                                     'de '
                                                                                                                                     'la '
                                                                                                                                     'source '
                                                                                                                                     'suspectée '
                                                                                                                                     'si '
                                                                                                                                     'cela '
                                                                                                                                     'peut '
                                                                                                                                     'être '
                                                                                                                                     'fait '
                                                                                                                                     'sans '
                                                                                                                                     'danger, '
                                                                                                                                     'évitez '
                                                                                                                                     'toute '
                                                                                                                                     'exposition '
                                                                                                                                     'inutile '
                                                                                                                                     'et '
                                                                                                                                     'demandez '
                                                                                                                                     'conseil '
                                                                                                                                     'à '
                                                                                                                                     'un '
                                                                                                                                     'spécialiste '
                                                                                                                                     'de '
                                                                                                                                     'la '
                                                                                                                                     'radioprotection.',
 'Never': 'Jamais',
 'Newest sample': 'Mesure la plus récente',
 'Next upload': 'Prochain envoi',
 'No GMC device detected': 'No GMC device detected',
 'No action is required while the result remains normal. Investigate persistent changes by checking the measurement location and comparing both devices.': 'Aucune '
                                                                                                                                                           'action '
                                                                                                                                                           'n’est '
                                                                                                                                                           'requise '
                                                                                                                                                           'tant '
                                                                                                                                                           'que '
                                                                                                                                                           'le '
                                                                                                                                                           'résultat '
                                                                                                                                                           'reste '
                                                                                                                                                           'normal. '
                                                                                                                                                           'Examinez '
                                                                                                                                                           'les '
                                                                                                                                                           'changements '
                                                                                                                                                           'persistants '
                                                                                                                                                           'en '
                                                                                                                                                           'vérifiant '
                                                                                                                                                           'le '
                                                                                                                                                           'lieu '
                                                                                                                                                           'de '
                                                                                                                                                           'mesure '
                                                                                                                                                           'et '
                                                                                                                                                           'en '
                                                                                                                                                           'comparant '
                                                                                                                                                           'les '
                                                                                                                                                           'deux '
                                                                                                                                                           'appareils.',
 'No action is required. Continue normal monitoring.': 'Aucune action n’est requise. Poursuivez la surveillance '
                                                       'normale.',
 'No action is required. The assessment becomes more reliable as additional measurements are collected.': 'Aucune '
                                                                                                          'action '
                                                                                                          'n’est '
                                                                                                          'requise. '
                                                                                                          'L’évaluation '
                                                                                                          'devient '
                                                                                                          'plus fiable '
                                                                                                          'à mesure '
                                                                                                          'que des '
                                                                                                          'mesures '
                                                                                                          'supplémentaires '
                                                                                                          'sont '
                                                                                                          'collectées.',
 'No action required': 'Aucune action requise',
 'No active device warnings': 'No active device warnings',
 'No connected GMC device': 'No connected GMC device',
 'No connected counter is available yet. The next serial scan runs automatically.': 'No connected counter is available '
                                                                                    'yet. The next serial scan runs '
                                                                                    'automatically.',
 'No connected devices.': 'Aucun appareil connecté.',
 'No current pressure source is available': 'Aucune source de pression actuelle disponible',
 'No data': 'Aucune donnée',
 'No known GMC devices': 'No known GMC devices',
 'No matching Home Assistant entities': 'No matching Home Assistant entities',
 'No measurement yet': 'Aucune mesure pour le moment',
 'No measurements in selected period': 'Aucune mesure pendant la période sélectionnée',
 'No measurements yet.': 'Aucune mesure pour le moment.',
 'No persistent level shift detected': 'No persistent level shift detected',
 'No position changes recorded.': 'Aucun changement de position enregistré.',
 'No pressure variation': 'Aucune variation de pression suffisante',
 'No pressure-typical signature': 'Aucune signature typique de la pression',
 'No pronounced baseline jumps detected.': 'Aucun saut prononcé du niveau de référence détecté.',
 'No reports have been requested in this browser yet.': 'No reports have been requested in this browser yet.',
 'No shared rise detected.': 'Aucune hausse commune détectée.',
 'No stored measurements': 'No stored measurements',
 'No suitable serial device was found.': 'No suitable serial device was found.',
 'No sustained relative anomaly events detected': 'Aucun événement d’anomalie relative persistante détecté',
 'No valid CPM baseline': 'Aucune référence CPM valide',
 'Normal': 'Normal',
 'Normal for this time': 'Normal pour cette heure',
 'Normal: within the usual local range': 'Normal : dans la plage locale habituelle',
 'Not available yet — at least two CPM samples are required': 'Pas encore disponible — au moins deux mesures CPM sont '
                                                              'nécessaires',
 'Not available yet — more baseline history is required': 'Pas encore disponible — davantage d’historique de référence '
                                                          'est nécessaire',
 'Not available yet — more paired samples are required': 'Pas encore disponible — davantage de paires de mesures sont '
                                                         'nécessaires',
 'Not available yet — no temperature samples were stored in the current 24 h window.': 'Pas encore disponible — aucune '
                                                                                       'mesure de température n’a été '
                                                                                       'enregistrée dans la fenêtre '
                                                                                       'actuelle de 24 h.',
 'Not available yet — the 24 h CPM series needs variation and at least two samples': 'Pas encore disponible — la série '
                                                                                     'CPM sur 24 h doit varier et '
                                                                                     'comporter au moins deux mesures',
 'Not available yet — the 24 h mean and spread are still insufficient': 'Pas encore disponible — la moyenne et la '
                                                                        'dispersion sur 24 h sont encore insuffisantes',
 'Not available — CPM did not vary during this period': 'Indisponible — le CPM n’a pas varié pendant cette période',
 'Not available — the sensor value did not vary during this period': 'Indisponible — la valeur du capteur n’a pas '
                                                                     'varié pendant cette période',
 'Not configured': 'Non configuré',
 'Not connected': 'Not connected',
 'Not detected yet': 'Pas encore détecté',
 'Not enough local history yet': 'Historique local encore insuffisant',
 'Not found': 'Introuvable',
 'Not recorded in this browser': 'Not recorded in this browser',
 'Not suitable as a GMC device': 'Not suitable as a GMC device',
 'Not suitable for GMC': 'Not suitable for GMC',
 'Not yet checked as a GMC device': 'Not yet checked as a GMC device',
 'Noticeable': 'Remarquable',
 'Noticeable baseline drift': 'Dérive notable de la référence',
 'Noticeable difference from Poisson-like spread': 'Écart notable par rapport à une dispersion de type Poisson',
 'Noticeable statistical deviation': 'Écart statistique notable',
 'Noticeable: above the usual local range': 'Remarquable : au-dessus de la plage locale habituelle',
 'Number of samples': 'Nombre de mesures',
 'Observed': 'Observé',
 'Observed SD / √mean': 'Écart-type observé / √moyenne',
 'Official reference values': 'Valeurs de référence officielles',
 'Offline': 'Hors ligne',
 'Oldest sample': 'Mesure la plus ancienne',
 'One current weather entity is available': 'Une entité météo actuelle est disponible',
 'One-hour mean is {deviation:+.1f}% relative to the learned baseline': 'La moyenne sur une heure est de '
                                                                        '{deviation:+.1f}% par rapport à la référence '
                                                                        'apprise',
 'One-hour means': 'Moyennes sur une heure',
 'One-hour robust level is {deviation:+.1f}% relative to the device baseline': 'Le niveau robuste sur une heure est de '
                                                                               '{deviation:+.1f}% par rapport à la '
                                                                               'référence de l’appareil',
 'Online': 'En ligne',
 'Only quality-filtered, one-to-one time-matched measurements are compared. Agreement, correlation, relative bias and stability are evaluated separately so one faulty counter does not automatically define the site result.': 'Seules '
                                                                                                                                                                                                                                'les '
                                                                                                                                                                                                                                'mesures '
                                                                                                                                                                                                                                'filtrées '
                                                                                                                                                                                                                                'selon '
                                                                                                                                                                                                                                'la '
                                                                                                                                                                                                                                'qualité '
                                                                                                                                                                                                                                'et '
                                                                                                                                                                                                                                'appariées '
                                                                                                                                                                                                                                'une '
                                                                                                                                                                                                                                'à '
                                                                                                                                                                                                                                'une '
                                                                                                                                                                                                                                'dans '
                                                                                                                                                                                                                                'le '
                                                                                                                                                                                                                                'temps '
                                                                                                                                                                                                                                'sont '
                                                                                                                                                                                                                                'comparées. '
                                                                                                                                                                                                                                'L’accord, '
                                                                                                                                                                                                                                'la '
                                                                                                                                                                                                                                'corrélation, '
                                                                                                                                                                                                                                'le '
                                                                                                                                                                                                                                'biais '
                                                                                                                                                                                                                                'relatif '
                                                                                                                                                                                                                                'et '
                                                                                                                                                                                                                                'la '
                                                                                                                                                                                                                                'stabilité '
                                                                                                                                                                                                                                'sont '
                                                                                                                                                                                                                                'évalués '
                                                                                                                                                                                                                                'séparément '
                                                                                                                                                                                                                                'afin '
                                                                                                                                                                                                                                'qu’un '
                                                                                                                                                                                                                                'compteur '
                                                                                                                                                                                                                                'défectueux '
                                                                                                                                                                                                                                'ne '
                                                                                                                                                                                                                                'détermine '
                                                                                                                                                                                                                                'pas '
                                                                                                                                                                                                                                'automatiquement '
                                                                                                                                                                                                                                'le '
                                                                                                                                                                                                                                'résultat '
                                                                                                                                                                                                                                'du '
                                                                                                                                                                                                                                'site.',
 'Only the most important conclusions at a glance': 'Uniquement les conclusions essentielles en un coup d’œil',
 'Open': 'Open',
 'Open serial device connections': 'Open serial device connections',
 'Operational events cleared': 'Operational events cleared',
 'Orientation cannot be verified automatically': 'Orientation cannot be verified automatically',
 'Orientation changes detected': 'Orientation changes detected',
 'Orientation data is temporarily unavailable.': 'Les données d’orientation sont temporairement indisponibles.',
 'Orientation qualification': 'Orientation qualification',
 'Orientation stable': 'Orientation stable',
 'Original raw-data CSV': 'Original raw-data CSV',
 'Outliers and invalid measurements': 'Valeurs aberrantes et mesures invalides',
 'Overview': 'Vue d’ensemble',
 'P95 CPM': 'CPM P95',
 'P95: {value} CPM': 'P95 : {value} CPM',
 'P99 CPM': 'CPM P99',
 'P99: {value} CPM': 'P99 : {value} CPM',
 'PDF report': 'Rapport PDF',
 'Pair-level disagreement': 'Désaccord au niveau des paires',
 'Pearson r · n={count} paired samples': 'r de Pearson · n={count} paires de mesures',
 'Period: {period} ({timezone})': 'Période : {period} ({timezone})',
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
 'Pitch angle': 'Angle de tangage',
 'Plausibilised from two weather entities': 'Plausibilisé à partir de deux entités météo',
 'Poisson SD ratio': 'Rapport ET de Poisson',
 'Poisson SD ratio = observed standard deviation / √mean; a value near 1 indicates Poisson-like spread.': 'Rapport ET '
                                                                                                          'de Poisson '
                                                                                                          '= '
                                                                                                          'écart-type '
                                                                                                          'observé / '
                                                                                                          '√moyenne ; '
                                                                                                          'une valeur '
                                                                                                          'proche de 1 '
                                                                                                          'indique une '
                                                                                                          'dispersion '
                                                                                                          'de type '
                                                                                                          'Poisson.',
 'Poisson SD ratio formula explanation': 'Rapport ET de Poisson = écart-type observé / √moyenne ; une valeur proche de '
                                         '1 indique une dispersion de type Poisson.',
 'Poisson SD ratio: {value}': 'Rapport ET de Poisson : {value}',
 'Poisson counting interval from the observed impulse count': 'Poisson counting interval from the observed impulse '
                                                              'count',
 'Poisson expectation (λ={mean:.2f})': 'Attente de Poisson (λ={mean:.2f})',
 'Poor': 'Mauvaise',
 'Position change log': 'Journal des changements de position',
 'Possible GMC connection cable': 'Possible GMC connection cable',
 'Possible persistent level shift': 'Possible persistent level shift',
 'Pressure model is still being formed': 'Le modèle de pression est encore en cours de formation',
 'Pressure model unavailable': 'Modèle de pression indisponible',
 'Pressure-typical signature is pronounced': 'Signature typique de la pression marquée',
 'Preview backup': 'Preview backup',
 'Previous day': 'Jour précédent',
 'Previous week': 'Semaine précédente',
 'Probable real change': 'Changement réel probable',
 'Probable shared measurement-site change': 'Modification commune probable du lieu de mesure',
 'Profile': 'Profil de l’appareil',
 'Profile is still being formed': 'Le profil est encore en cours de formation',
 'Provider': 'Fournisseur',
 'Public GMCMap upload': 'Envoi public vers GMCMap',
 'Quality weight': 'Poids de qualité',
 'Quality-filtered correlation': 'Corrélation filtrée par qualité',
 'Quality-filtered measurement CSV': 'Quality-filtered measurement CSV',
 'Quick downloads': 'Téléchargements rapides',
 'Radiation 1 h Mean': 'Moyenne du rayonnement sur 1 h',
 'Radiation 1 h Median': 'Médiane du rayonnement sur 1 h',
 'Radiation 1 h Standard Deviation': 'Écart-type du rayonnement sur 1 h',
 'Radiation Baseline Deviation': 'Écart au niveau de référence du rayonnement',
 'Radiation CPM': 'Rayonnement CPM',
 'Radiation Rapid Change': 'Variation rapide du rayonnement',
 'Radiation count rate [CPM]': 'Taux de comptage du rayonnement [CPM]',
 'Radiation counts fluctuate naturally. The Fano factor and Poisson spread ratio compare the observed variation with a simple counting-statistics model; they describe distribution shape but not a physical cause or calibration state.': 'Les '
                                                                                                                                                                                                                                           'comptages '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'rayonnement '
                                                                                                                                                                                                                                           'fluctuent '
                                                                                                                                                                                                                                           'naturellement. '
                                                                                                                                                                                                                                           'Le '
                                                                                                                                                                                                                                           'facteur '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'Fano '
                                                                                                                                                                                                                                           'et '
                                                                                                                                                                                                                                           'le '
                                                                                                                                                                                                                                           'rapport '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'dispersion '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'Poisson '
                                                                                                                                                                                                                                           'comparent '
                                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                                           'variation '
                                                                                                                                                                                                                                           'observée '
                                                                                                                                                                                                                                           'à '
                                                                                                                                                                                                                                           'un '
                                                                                                                                                                                                                                           'modèle '
                                                                                                                                                                                                                                           'simple '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'statistique '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'comptage '
                                                                                                                                                                                                                                           '; '
                                                                                                                                                                                                                                           'ils '
                                                                                                                                                                                                                                           'décrivent '
                                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                                           'forme '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                                           'distribution, '
                                                                                                                                                                                                                                           'mais '
                                                                                                                                                                                                                                           'pas '
                                                                                                                                                                                                                                           'une '
                                                                                                                                                                                                                                           'cause '
                                                                                                                                                                                                                                           'physique '
                                                                                                                                                                                                                                           'ni '
                                                                                                                                                                                                                                           'l’état '
                                                                                                                                                                                                                                           'd’étalonnage.',
 'Radiation measurement continues unless the device status says otherwise.': 'La mesure du rayonnement continue sauf '
                                                                             'indication contraire de l’état de '
                                                                             'l’appareil.',
 'Radiation measurement continues. An external Home Assistant temperature may be used when configured.': 'La mesure du '
                                                                                                         'rayonnement '
                                                                                                         'continue. '
                                                                                                         'Une '
                                                                                                         'température '
                                                                                                         'externe de '
                                                                                                         'Home '
                                                                                                         'Assistant '
                                                                                                         'peut être '
                                                                                                         'utilisée '
                                                                                                         'lorsqu’elle '
                                                                                                         'est '
                                                                                                         'configurée.',
 'Radiation measurement continues; only the optional orientation value is affected.': 'La mesure du rayonnement '
                                                                                      'continue ; seule la valeur '
                                                                                      'd’orientation facultative est '
                                                                                      'affectée.',
 'Radiation monitoring analysis': 'Analyse de surveillance du rayonnement',
 'Radiation traffic light': 'Feu tricolore de rayonnement',
 'Radiation traffic light hysteresis explanation': 'Le feu tricolore utilise une hystérésis : jaune à '
                                                   '{yellow_enter:g}% et retour sous {yellow_clear:g}% ; rouge à '
                                                   '{red_enter:g}% et retour sous {red_clear:g}%.',
 'Radiation traffic light uses hysteresis: it enters yellow at {yellow_enter:g}% and clears below {yellow_clear:g}%; it enters red at {red_enter:g}% and clears below {red_clear:g}%.': 'Le '
                                                                                                                                                                                        'feu '
                                                                                                                                                                                        'tricolore '
                                                                                                                                                                                        'utilise '
                                                                                                                                                                                        'une '
                                                                                                                                                                                        'hystérésis '
                                                                                                                                                                                        ': '
                                                                                                                                                                                        'jaune '
                                                                                                                                                                                        'à '
                                                                                                                                                                                        '{yellow_enter:g}% '
                                                                                                                                                                                        'et '
                                                                                                                                                                                        'retour '
                                                                                                                                                                                        'sous '
                                                                                                                                                                                        '{yellow_clear:g}% '
                                                                                                                                                                                        '; '
                                                                                                                                                                                        'rouge '
                                                                                                                                                                                        'à '
                                                                                                                                                                                        '{red_enter:g}% '
                                                                                                                                                                                        'et '
                                                                                                                                                                                        'retour '
                                                                                                                                                                                        'sous '
                                                                                                                                                                                        '{red_clear:g}%.',
 'Raw CSV': 'CSV brut',
 'Raw device values are stored separately before quality filtering': 'Raw device values are stored separately before '
                                                                     'quality filtering',
 'Raw gyro [signed int16]': 'Gyro brut [int16 signé]',
 'Raw-data archive': 'Raw-data archive',
 'Read-only mode': 'Read-only mode',
 'Ready for new measurements': 'Ready for new measurements',
 'Recent 30 days compared with the preceding 30 days': '30 derniers jours comparés aux 30 jours précédents',
 'Recent data quality is high': 'La qualité des données récentes est élevée',
 'Recent period compared with the preceding period': 'Période récente comparée à la période précédente',
 'Recent quality-filtered data quality is high': 'La qualité récente des données filtrées est élevée',
 'Recent reports': 'Recent reports',
 'Recommendation': 'Recommandation',
 'Recommended': 'Recommended',
 'Reconnects': 'Reconnexions',
 'Red': 'Rouge',
 'Reduced': 'Réduite',
 'Refreshing device status…': 'Refreshing device status…',
 'Relative anomaly indicator only; not a safety classification.': 'Indicateur d’anomalie relative uniquement ; il ne '
                                                                  's’agit pas d’une classification de sécurité.',
 'Relative correction factor': 'Relative correction factor',
 'Relative spread': 'Relative spread',
 'Relative to 7 d baseline': 'Par rapport à la référence 7 j',
 'Relative-factor confidence': 'Relative-factor confidence',
 'Remaining deviation': 'Écart restant',
 'Remove': 'Remove',
 'Report': 'Report',
 'Report generation failed': 'Échec de la génération du rapport',
 'Report target': 'Cible du rapport',
 'Reports': 'Reports',
 'Reports for the displayed analysis': 'Reports for the displayed analysis',
 'Rescan devices': 'Rescan devices',
 'Resolve persistent connection gaps before relying on long-term comparisons.': 'Corrigez les interruptions de '
                                                                                'connexion persistantes avant de vous '
                                                                                'fier aux comparaisons à long terme.',
 'Restore backup': 'Restaurer la sauvegarde',
 'Restore complete': 'Restauration terminée',
 'Restore confirmation text must be exactly RESTORE': 'Le texte de confirmation doit être exactement RESTORE',
 'Restore history': 'Restaurer l’historique',
 'Restore is disabled by default.': 'La restauration est désactivée par défaut.',
 'Restore upload must be between 1 byte and 128 MiB': 'Le fichier de restauration doit faire entre 1 octet et 128 Mio',
 'Return to GMC Radiation Monitoring': 'Retour à la surveillance du rayonnement GMC',
 'Return to GMC Reports': 'Retour aux rapports GMC',
 'Review the event export for timing and severity': 'Consultez l’export des événements pour l’heure et la gravité',
 'Review the recent trend and event timing. Check both counters and the measurement location if the change persists.': 'Examinez '
                                                                                                                       'la '
                                                                                                                       'tendance '
                                                                                                                       'récente '
                                                                                                                       'et '
                                                                                                                       'l’heure '
                                                                                                                       'des '
                                                                                                                       'événements. '
                                                                                                                       'Vérifiez '
                                                                                                                       'les '
                                                                                                                       'deux '
                                                                                                                       'compteurs '
                                                                                                                       'et '
                                                                                                                       'le '
                                                                                                                       'lieu '
                                                                                                                       'de '
                                                                                                                       'mesure '
                                                                                                                       'si '
                                                                                                                       'le '
                                                                                                                       'changement '
                                                                                                                       'persiste.',
 'Rising': 'En hausse',
 'Robust medians are used; rejected measurements and isolated spikes do not immediately change the profile.': 'Des '
                                                                                                              'médianes '
                                                                                                              'robustes '
                                                                                                              'sont '
                                                                                                              'utilisées '
                                                                                                              '; les '
                                                                                                              'mesures '
                                                                                                              'rejetées '
                                                                                                              'et les '
                                                                                                              'pics '
                                                                                                              'isolés '
                                                                                                              'ne '
                                                                                                              'modifient '
                                                                                                              'pas '
                                                                                                              'immédiatement '
                                                                                                              'le '
                                                                                                              'profil.',
 'Robust one-hour values': 'Valeurs robustes sur une heure',
 'Roll angle': 'Angle de roulis',
 'Rolling windows end at the latest stored measurement. Dose-rate values are derived from CPM using the configured factor and are not independently measured. CPM remains the primary measurement. The traffic light is a relative background-anomaly indicator, not an emergency, health, or radiation-safety classification.': 'Les '
                                                                                                                                                                                                                                                                                                                                 'fenêtres '
                                                                                                                                                                                                                                                                                                                                 'glissantes '
                                                                                                                                                                                                                                                                                                                                 'se '
                                                                                                                                                                                                                                                                                                                                 'terminent '
                                                                                                                                                                                                                                                                                                                                 'à '
                                                                                                                                                                                                                                                                                                                                 'la '
                                                                                                                                                                                                                                                                                                                                 'dernière '
                                                                                                                                                                                                                                                                                                                                 'mesure '
                                                                                                                                                                                                                                                                                                                                 'enregistrée. '
                                                                                                                                                                                                                                                                                                                                 'Les '
                                                                                                                                                                                                                                                                                                                                 'débits '
                                                                                                                                                                                                                                                                                                                                 'de '
                                                                                                                                                                                                                                                                                                                                 'dose '
                                                                                                                                                                                                                                                                                                                                 'sont '
                                                                                                                                                                                                                                                                                                                                 'dérivés '
                                                                                                                                                                                                                                                                                                                                 'du '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'avec '
                                                                                                                                                                                                                                                                                                                                 'le '
                                                                                                                                                                                                                                                                                                                                 'facteur '
                                                                                                                                                                                                                                                                                                                                 'configuré '
                                                                                                                                                                                                                                                                                                                                 'et '
                                                                                                                                                                                                                                                                                                                                 'ne '
                                                                                                                                                                                                                                                                                                                                 'sont '
                                                                                                                                                                                                                                                                                                                                 'pas '
                                                                                                                                                                                                                                                                                                                                 'mesurés '
                                                                                                                                                                                                                                                                                                                                 'indépendamment. '
                                                                                                                                                                                                                                                                                                                                 'Le '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'reste '
                                                                                                                                                                                                                                                                                                                                 'la '
                                                                                                                                                                                                                                                                                                                                 'mesure '
                                                                                                                                                                                                                                                                                                                                 'principale. '
                                                                                                                                                                                                                                                                                                                                 'Le '
                                                                                                                                                                                                                                                                                                                                 'feu '
                                                                                                                                                                                                                                                                                                                                 'tricolore '
                                                                                                                                                                                                                                                                                                                                 'indique '
                                                                                                                                                                                                                                                                                                                                 'une '
                                                                                                                                                                                                                                                                                                                                 'anomalie '
                                                                                                                                                                                                                                                                                                                                 'relative '
                                                                                                                                                                                                                                                                                                                                 'du '
                                                                                                                                                                                                                                                                                                                                 'fond, '
                                                                                                                                                                                                                                                                                                                                 'et '
                                                                                                                                                                                                                                                                                                                                 'non '
                                                                                                                                                                                                                                                                                                                                 'une '
                                                                                                                                                                                                                                                                                                                                 'classification '
                                                                                                                                                                                                                                                                                                                                 'd’urgence, '
                                                                                                                                                                                                                                                                                                                                 'de '
                                                                                                                                                                                                                                                                                                                                 'santé '
                                                                                                                                                                                                                                                                                                                                 'ou '
                                                                                                                                                                                                                                                                                                                                 'de '
                                                                                                                                                                                                                                                                                                                                 'radioprotection.',
 'SD: {value} CPM': 'ET : {value} CPM',
 'SQLite backup': 'Sauvegarde SQLite',
 'SQLite backup file': 'SQLite backup file',
 'SQLite database vacuum completed': 'SQLite database vacuum completed',
 'Sample standard deviation': 'Écart-type d’échantillon',
 'Samples': 'Échantillons',
 'Samples: {samples} / {expected}': 'Mesures : {samples} / {expected}',
 'Sampling interval: {interval} s | Samples: {samples}/{expected} | Completeness: {completeness:.2f}% | Generated: {generated} | App {version}': 'Intervalle '
                                                                                                                                                 ': '
                                                                                                                                                 '{interval} '
                                                                                                                                                 's '
                                                                                                                                                 '| '
                                                                                                                                                 'Mesures '
                                                                                                                                                 ': '
                                                                                                                                                 '{samples}/{expected} '
                                                                                                                                                 '| '
                                                                                                                                                 'Complétude '
                                                                                                                                                 ': '
                                                                                                                                                 '{completeness:.2f} '
                                                                                                                                                 '% '
                                                                                                                                                 '| '
                                                                                                                                                 'Généré '
                                                                                                                                                 ': '
                                                                                                                                                 '{generated} '
                                                                                                                                                 '| '
                                                                                                                                                 'App '
                                                                                                                                                 '{version}',
 'Sampling interval: {seconds} s': 'Intervalle d’échantillonnage : {seconds} s',
 'Sat': 'Sam',
 'Saturday': 'Samedi',
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
 'Second half vs first half of available 7 d window': 'Seconde moitié comparée à la première moitié de la fenêtre '
                                                      'disponible sur 7 jours',
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
 'Serial': 'Numéro de série',
 'Serial Errors Since Start': 'Erreurs série depuis le démarrage',
 'Serial Reconnects Since Start': 'Reconnexions série depuis le démarrage',
 'Serial USB device': 'Serial USB device',
 'Serial connection recovered': 'Serial connection recovered',
 'Serial device connections': 'Serial device connections',
 'Serial errors / reconnects': 'Erreurs série / reconnexions',
 'Serial port': 'Port série',
 'Serial: {serial} | Period: {period} | Timezone: {timezone}': 'Numéro de série : {serial} | Période : {period} | '
                                                               'Fuseau horaire : {timezone}',
 'Serial: {value}': 'Numéro de série : {value}',
 'Severity': 'Gravité',
 'Shared CPM rise': 'Hausse commune des CPM',
 'Shared event detector': 'Détecteur d’événement commun',
 'Show analysis': 'Afficher l’analyse',
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
 'Simple': 'Simple',
 'Since app start': 'Depuis le démarrage de l’application',
 'Slightly noticeable': 'Légèrement notable',
 'Slightly tilted': 'Slightly tilted',
 'Small baseline drift': 'Faible dérive de la référence',
 'Smart Alert State': 'État de l’alerte intelligente',
 'Smoothed historical background trend': 'Tendance historique lissée du fond',
 'Source validation': 'Validation des sources',
 'Specific ISO week': 'Semaine ISO précise',
 'Specific date': 'Date précise',
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
 'Stability and device health': 'Stabilité et état des appareils',
 'Stable': 'Stable',
 'Stable device path': 'Stable device path',
 'Stable devices': 'Appareils stables',
 'Standard deviation CPM': 'Écart-type CPM',
 'Start time UTC': 'Heure de début UTC',
 'Start time local': 'Heure de début locale',
 'Start with a readable PDF or a complete ZIP bundle. Raw and specialist formats remain available below without crowding the main view.': 'Commencez '
                                                                                                                                          'par '
                                                                                                                                          'un '
                                                                                                                                          'PDF '
                                                                                                                                          'lisible '
                                                                                                                                          'ou '
                                                                                                                                          'une '
                                                                                                                                          'archive '
                                                                                                                                          'ZIP '
                                                                                                                                          'complète. '
                                                                                                                                          'Les '
                                                                                                                                          'formats '
                                                                                                                                          'bruts '
                                                                                                                                          'et '
                                                                                                                                          'spécialisés '
                                                                                                                                          'restent '
                                                                                                                                          'disponibles '
                                                                                                                                          'plus '
                                                                                                                                          'bas '
                                                                                                                                          'sans '
                                                                                                                                          'surcharger '
                                                                                                                                          'la '
                                                                                                                                          'vue '
                                                                                                                                          'principale.',
 'Statistical indication only': 'Indication statistique uniquement',
 'Statistical level shift': 'Statistical level shift',
 'Statistically noticeable': 'Statistiquement notable',
 'Statistics': 'Statistiques',
 'Stored samples': 'Mesures stockées',
 'Stored samples across all devices': 'Mesures enregistrées pour tous les appareils',
 'Stored samples for this device': 'Mesures enregistrées pour cet appareil',
 'Strong common signal': 'Signal commun fort',
 'Strong linear relationship': 'Forte relation linéaire',
 'Strong statistical deviation': 'Fort écart statistique',
 'Successful uploads': 'Envois réussis',
 'Successful uploads since start': 'Envois réussis depuis le démarrage',
 'Suitable for most trend analysis': 'Adapté à la plupart des analyses de tendance',
 'Summary': 'Résumé',
 'Sun': 'Dim',
 'Sunday': 'Dimanche',
 'Supervisor API access is unavailable': 'Supervisor API access is unavailable',
 'Supply voltage [V]': 'Tension d’alimentation [V]',
 'Suspicious CPM value is being verified': 'Suspicious CPM value is being verified',
 'Sustained Radiation Alert': 'Alerte de rayonnement persistante',
 'Sustained relative anomaly events': 'Événements persistants d’anomalie relative',
 'Sustained yellow/red relative anomaly events': 'Événements persistants d’anomalie relative jaune/rouge',
 'Temperature': 'Température',
 'Temperature / voltage errors': 'Erreurs de température / tension',
 'Temperature Errors Since Start': 'Erreurs de température depuis le démarrage',
 'Temperature [°C]': 'Température [°C]',
 'Temperature and voltage relationships': 'Relations avec la température et la tension',
 'Temperature bins (24 h)': 'Classes de température (24 h)',
 'Temperature correlation': 'Corrélation avec la température',
 'Temperature profile is still being formed': 'Le profil de température est encore en cours de formation',
 'Temperature trend': 'Tendance de température',
 'Temperature-specific background': 'Fond spécifique à la température',
 'The Supervisor options could not be loaded: {error}': 'The Supervisor options could not be loaded: {error}',
 'The absolute assessment starts after the first measurement.': 'L’évaluation absolue commence après la première '
                                                                'mesure.',
 'The absolute level is below the configured warning threshold, but the value is far above the learned local background.': 'Le '
                                                                                                                           'niveau '
                                                                                                                           'absolu '
                                                                                                                           'reste '
                                                                                                                           'inférieur '
                                                                                                                           'au '
                                                                                                                           'seuil '
                                                                                                                           'd’avertissement '
                                                                                                                           'configuré, '
                                                                                                                           'mais '
                                                                                                                           'la '
                                                                                                                           'valeur '
                                                                                                                           'est '
                                                                                                                           'très '
                                                                                                                           'supérieure '
                                                                                                                           'au '
                                                                                                                           'fond '
                                                                                                                           'local '
                                                                                                                           'appris.',
 'The absolute level is currently uncritical, but the local comparison or short-term trend deserves continued observation.': 'Le '
                                                                                                                             'niveau '
                                                                                                                             'absolu '
                                                                                                                             'est '
                                                                                                                             'actuellement '
                                                                                                                             'non '
                                                                                                                             'critique, '
                                                                                                                             'mais '
                                                                                                                             'la '
                                                                                                                             'comparaison '
                                                                                                                             'locale '
                                                                                                                             'ou '
                                                                                                                             'la '
                                                                                                                             'tendance '
                                                                                                                             'à '
                                                                                                                             'court '
                                                                                                                             'terme '
                                                                                                                             'mérite '
                                                                                                                             'une '
                                                                                                                             'surveillance '
                                                                                                                             'continue.',
 'The absolute level is currently uncritical. More local history is required before anomaly detection becomes reliable.': 'Le '
                                                                                                                          'niveau '
                                                                                                                          'absolu '
                                                                                                                          'est '
                                                                                                                          'actuellement '
                                                                                                                          'non '
                                                                                                                          'critique. '
                                                                                                                          'Davantage '
                                                                                                                          'd’historique '
                                                                                                                          'local '
                                                                                                                          'est '
                                                                                                                          'nécessaire '
                                                                                                                          'pour '
                                                                                                                          'rendre '
                                                                                                                          'la '
                                                                                                                          'détection '
                                                                                                                          'd’anomalies '
                                                                                                                          'fiable.',
 'The add-on is restarting so the new serial assignments become active.': 'The add-on is restarting so the new serial '
                                                                          'assignments become active.',
 'The app combines the recent trend, robust statistics, agreement between connected counters and the learned local background. The result is a statistical aid and does not identify a physical cause.': 'L’application '
                                                                                                                                                                                                         'combine '
                                                                                                                                                                                                         'la '
                                                                                                                                                                                                         'tendance '
                                                                                                                                                                                                         'récente, '
                                                                                                                                                                                                         'des '
                                                                                                                                                                                                         'statistiques '
                                                                                                                                                                                                         'robustes, '
                                                                                                                                                                                                         'l’accord '
                                                                                                                                                                                                         'entre '
                                                                                                                                                                                                         'les '
                                                                                                                                                                                                         'compteurs '
                                                                                                                                                                                                         'connectés '
                                                                                                                                                                                                         'et '
                                                                                                                                                                                                         'le '
                                                                                                                                                                                                         'fond '
                                                                                                                                                                                                         'local '
                                                                                                                                                                                                         'appris. '
                                                                                                                                                                                                         'Le '
                                                                                                                                                                                                         'résultat '
                                                                                                                                                                                                         'est '
                                                                                                                                                                                                         'une '
                                                                                                                                                                                                         'aide '
                                                                                                                                                                                                         'statistique '
                                                                                                                                                                                                         'et '
                                                                                                                                                                                                         'n’identifie '
                                                                                                                                                                                                         'pas '
                                                                                                                                                                                                         'une '
                                                                                                                                                                                                         'cause '
                                                                                                                                                                                                         'physique.',
 'The app compares quality-filtered measurements from the same weekday and hour. Robust medians reduce the influence of isolated spikes and regular daily patterns are kept separate from unusual changes.': 'L’application '
                                                                                                                                                                                                             'compare '
                                                                                                                                                                                                             'les '
                                                                                                                                                                                                             'mesures '
                                                                                                                                                                                                             'filtrées '
                                                                                                                                                                                                             'selon '
                                                                                                                                                                                                             'la '
                                                                                                                                                                                                             'qualité '
                                                                                                                                                                                                             'du '
                                                                                                                                                                                                             'même '
                                                                                                                                                                                                             'jour '
                                                                                                                                                                                                             'de '
                                                                                                                                                                                                             'la '
                                                                                                                                                                                                             'semaine '
                                                                                                                                                                                                             'et '
                                                                                                                                                                                                             'de '
                                                                                                                                                                                                             'la '
                                                                                                                                                                                                             'même '
                                                                                                                                                                                                             'heure. '
                                                                                                                                                                                                             'Des '
                                                                                                                                                                                                             'médianes '
                                                                                                                                                                                                             'robustes '
                                                                                                                                                                                                             'réduisent '
                                                                                                                                                                                                             'l’influence '
                                                                                                                                                                                                             'des '
                                                                                                                                                                                                             'pics '
                                                                                                                                                                                                             'isolés '
                                                                                                                                                                                                             'et '
                                                                                                                                                                                                             'les '
                                                                                                                                                                                                             'rythmes '
                                                                                                                                                                                                             'quotidiens '
                                                                                                                                                                                                             'réguliers '
                                                                                                                                                                                                             'sont '
                                                                                                                                                                                                             'séparés '
                                                                                                                                                                                                             'des '
                                                                                                                                                                                                             'changements '
                                                                                                                                                                                                             'inhabituels.',
 'The app compares quality-filtered radiation measurements with available air-pressure data. A statistical relationship can support interpretation, but correlation alone does not prove a cosmic or environmental cause.': 'L’application '
                                                                                                                                                                                                                            'compare '
                                                                                                                                                                                                                            'les '
                                                                                                                                                                                                                            'mesures '
                                                                                                                                                                                                                            'de '
                                                                                                                                                                                                                            'rayonnement '
                                                                                                                                                                                                                            'filtrées '
                                                                                                                                                                                                                            'selon '
                                                                                                                                                                                                                            'la '
                                                                                                                                                                                                                            'qualité '
                                                                                                                                                                                                                            'aux '
                                                                                                                                                                                                                            'données '
                                                                                                                                                                                                                            'de '
                                                                                                                                                                                                                            'pression '
                                                                                                                                                                                                                            'atmosphérique '
                                                                                                                                                                                                                            'disponibles. '
                                                                                                                                                                                                                            'Une '
                                                                                                                                                                                                                            'relation '
                                                                                                                                                                                                                            'statistique '
                                                                                                                                                                                                                            'peut '
                                                                                                                                                                                                                            'aider '
                                                                                                                                                                                                                            'l’interprétation, '
                                                                                                                                                                                                                            'mais '
                                                                                                                                                                                                                            'la '
                                                                                                                                                                                                                            'corrélation '
                                                                                                                                                                                                                            'seule '
                                                                                                                                                                                                                            'ne '
                                                                                                                                                                                                                            'prouve '
                                                                                                                                                                                                                            'pas '
                                                                                                                                                                                                                            'une '
                                                                                                                                                                                                                            'cause '
                                                                                                                                                                                                                            'cosmique '
                                                                                                                                                                                                                            'ou '
                                                                                                                                                                                                                            'environnementale.',
 'The comparison uses only quality-filtered, one-to-one paired measurements.': 'La comparaison utilise uniquement des '
                                                                               'mesures filtrées par qualité et '
                                                                               'appariées une à une.',
 'The configured danger threshold is exceeded.': 'Le seuil de danger configuré est dépassé.',
 'The connected counters currently agree well': 'Les compteurs connectés concordent actuellement bien',
 'The counters disagree, so a device-specific effect is more likely': 'Les compteurs divergent; un effet propre à un '
                                                                      'appareil est donc plus probable',
 'The current radiation level is uncritical according to the selected thresholds.': 'Le niveau actuel de rayonnement '
                                                                                    'est non critique selon les seuils '
                                                                                    'sélectionnés.',
 'The current value is below the configured warning threshold and within the usual local range.': 'La valeur actuelle '
                                                                                                  'est inférieure au '
                                                                                                  'seuil '
                                                                                                  'd’avertissement '
                                                                                                  'configuré et se '
                                                                                                  'situe dans la plage '
                                                                                                  'locale habituelle.',
 'The current value is within the configured warning range.': 'La valeur actuelle se trouve dans la plage '
                                                              'd’avertissement configurée.',
 'The deviation is device-specific; the measurement-site profile remains normal': 'L’écart est propre à l’appareil ; '
                                                                                  'le profil du lieu de mesure reste '
                                                                                  'normal',
 'The device baseline is available, but there are not enough recent measurements for a current comparison.': 'La '
                                                                                                             'référence '
                                                                                                             'de '
                                                                                                             'l’appareil '
                                                                                                             'est '
                                                                                                             'disponible, '
                                                                                                             'mais il '
                                                                                                             'n’y a '
                                                                                                             'pas '
                                                                                                             'encore '
                                                                                                             'assez de '
                                                                                                             'mesures '
                                                                                                             'récentes '
                                                                                                             'pour une '
                                                                                                             'comparaison '
                                                                                                             'actuelle.',
 'The device clock differs from Home Assistant time.': 'The device clock differs from Home Assistant time.',
 'The filtered counters disagree, so a device-specific effect is more likely': 'Les compteurs filtrés divergent ; un '
                                                                               'effet propre à l’appareil est plus '
                                                                               'probable',
 'The learned baseline remains available. More current samples are required before the local comparison can be updated.': 'La '
                                                                                                                          'référence '
                                                                                                                          'apprise '
                                                                                                                          'reste '
                                                                                                                          'disponible. '
                                                                                                                          'Davantage '
                                                                                                                          'de '
                                                                                                                          'mesures '
                                                                                                                          'actuelles '
                                                                                                                          'sont '
                                                                                                                          'nécessaires '
                                                                                                                          'pour '
                                                                                                                          'actualiser '
                                                                                                                          'la '
                                                                                                                          'comparaison '
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
 'The local background is still being learned, so no anomaly assessment is available yet.': 'Le fond local est encore '
                                                                                            'en cours d’apprentissage '
                                                                                            '; aucune évaluation '
                                                                                            'd’anomalie n’est encore '
                                                                                            'disponible.',
 'The measurement-site baseline is {deviation:+.1f}% above its typical value': 'La référence du lieu de mesure est de '
                                                                               '{deviation:+.1f}% au-dessus de sa '
                                                                               'valeur typique',
 'The measurement-site profile combines both devices with quality weighting': 'Le profil du lieu de mesure combine les '
                                                                              'deux appareils avec une pondération par '
                                                                              'qualité',
 'The measurement-site profile currently relies on one device': 'Le profil du lieu de mesure repose actuellement sur '
                                                                'un seul appareil',
 'The pressure model cannot prove cosmic radiation and never suppresses radiation warnings.': 'Le modèle de pression '
                                                                                              'ne peut pas prouver un '
                                                                                              'rayonnement cosmique et '
                                                                                              'ne supprime jamais les '
                                                                                              'alertes de rayonnement.',
 'The quality-filtered counter comparison currently agrees well': 'La comparaison filtrée par qualité des compteurs '
                                                                  'concorde actuellement bien',
 'The recent 30-minute robust trend is rising': 'La tendance robuste des 30 dernières minutes est à la hausse',
 'The recent 30-minute trend is rising': 'La tendance récente sur 30 minutes est à la hausse',
 'The request could not be processed. Check the selected options.': 'La requête n’a pas pu être traitée. Vérifiez les '
                                                                    'options sélectionnées.',
 'The score combines time-window coverage, missing or irregular intervals, duplicate timestamps and optional-sensor coverage. It indicates how strongly the analysis can rely on the stored series.': 'Le '
                                                                                                                                                                                                      'score '
                                                                                                                                                                                                      'combine '
                                                                                                                                                                                                      'la '
                                                                                                                                                                                                      'couverture '
                                                                                                                                                                                                      'de '
                                                                                                                                                                                                      'la '
                                                                                                                                                                                                      'fenêtre '
                                                                                                                                                                                                      'temporelle, '
                                                                                                                                                                                                      'les '
                                                                                                                                                                                                      'intervalles '
                                                                                                                                                                                                      'manquants '
                                                                                                                                                                                                      'ou '
                                                                                                                                                                                                      'irréguliers, '
                                                                                                                                                                                                      'les '
                                                                                                                                                                                                      'horodatages '
                                                                                                                                                                                                      'en '
                                                                                                                                                                                                      'double '
                                                                                                                                                                                                      'et '
                                                                                                                                                                                                      'la '
                                                                                                                                                                                                      'couverture '
                                                                                                                                                                                                      'des '
                                                                                                                                                                                                      'capteurs '
                                                                                                                                                                                                      'facultatifs. '
                                                                                                                                                                                                      'Il '
                                                                                                                                                                                                      'indique '
                                                                                                                                                                                                      'dans '
                                                                                                                                                                                                      'quelle '
                                                                                                                                                                                                      'mesure '
                                                                                                                                                                                                      'l’analyse '
                                                                                                                                                                                                      'peut '
                                                                                                                                                                                                      's’appuyer '
                                                                                                                                                                                                      'sur '
                                                                                                                                                                                                      'la '
                                                                                                                                                                                                      'série '
                                                                                                                                                                                                      'enregistrée.',
 'The serial connection is unstable.': 'La connexion série est instable.',
 'The traffic light and events are relative anomaly indicators, not safety classifications.': 'Le feu et les '
                                                                                              'événements sont des '
                                                                                              'indicateurs d’anomalie '
                                                                                              'relative, pas des '
                                                                                              'classifications de '
                                                                                              'sécurité.',
 'The value is also within the usual range for this location.': 'La valeur se situe également dans la plage habituelle '
                                                                'de cet emplacement.',
 'The values most users need first': 'Les valeurs dont la plupart des utilisateurs ont besoin en premier',
 'These are statistical changes. They can indicate a location, geometry or environmental change, but do not identify the cause.': 'Il '
                                                                                                                                  's’agit '
                                                                                                                                  'de '
                                                                                                                                  'changements '
                                                                                                                                  'statistiques. '
                                                                                                                                  'Ils '
                                                                                                                                  'peuvent '
                                                                                                                                  'indiquer '
                                                                                                                                  'un '
                                                                                                                                  'changement '
                                                                                                                                  'de '
                                                                                                                                  'lieu, '
                                                                                                                                  'de '
                                                                                                                                  'géométrie '
                                                                                                                                  'ou '
                                                                                                                                  'd’environnement, '
                                                                                                                                  'sans '
                                                                                                                                  'en '
                                                                                                                                  'identifier '
                                                                                                                                  'la '
                                                                                                                                  'cause.',
 'These values describe the shape of the count distribution. They do not by themselves prove a physical cause or a calibration state.': 'Ces '
                                                                                                                                        'valeurs '
                                                                                                                                        'décrivent '
                                                                                                                                        'la '
                                                                                                                                        'forme '
                                                                                                                                        'de '
                                                                                                                                        'la '
                                                                                                                                        'distribution '
                                                                                                                                        'des '
                                                                                                                                        'comptages. '
                                                                                                                                        'À '
                                                                                                                                        'elles '
                                                                                                                                        'seules, '
                                                                                                                                        'elles '
                                                                                                                                        'ne '
                                                                                                                                        'prouvent '
                                                                                                                                        'ni '
                                                                                                                                        'une '
                                                                                                                                        'cause '
                                                                                                                                        'physique '
                                                                                                                                        'ni '
                                                                                                                                        'un '
                                                                                                                                        'état '
                                                                                                                                        'd’étalonnage.',
 'This analysis detects unusual changes compared with the normal background at this location. It is not a danger classification; an unusual value can still be below the absolute warning threshold.': 'Cette '
                                                                                                                                                                                                       'analyse '
                                                                                                                                                                                                       'détecte '
                                                                                                                                                                                                       'les '
                                                                                                                                                                                                       'variations '
                                                                                                                                                                                                       'inhabituelles '
                                                                                                                                                                                                       'par '
                                                                                                                                                                                                       'rapport '
                                                                                                                                                                                                       'au '
                                                                                                                                                                                                       'fond '
                                                                                                                                                                                                       'normal '
                                                                                                                                                                                                       'de '
                                                                                                                                                                                                       'cet '
                                                                                                                                                                                                       'emplacement. '
                                                                                                                                                                                                       'Ce '
                                                                                                                                                                                                       'n’est '
                                                                                                                                                                                                       'pas '
                                                                                                                                                                                                       'une '
                                                                                                                                                                                                       'classification '
                                                                                                                                                                                                       'du '
                                                                                                                                                                                                       'danger '
                                                                                                                                                                                                       '; '
                                                                                                                                                                                                       'une '
                                                                                                                                                                                                       'valeur '
                                                                                                                                                                                                       'inhabituelle '
                                                                                                                                                                                                       'peut '
                                                                                                                                                                                                       'rester '
                                                                                                                                                                                                       'sous '
                                                                                                                                                                                                       'le '
                                                                                                                                                                                                       'seuil '
                                                                                                                                                                                                       'absolu '
                                                                                                                                                                                                       'd’avertissement.',
 'This cannot be undone. Delete all GMC history?': 'This cannot be undone. Delete all GMC history?',
 'This classification only compares the current measurement with the selected thresholds. It does not compare the value with the usual background at this location.': 'Cette '
                                                                                                                                                                      'classification '
                                                                                                                                                                      'compare '
                                                                                                                                                                      'uniquement '
                                                                                                                                                                      'la '
                                                                                                                                                                      'mesure '
                                                                                                                                                                      'actuelle '
                                                                                                                                                                      'aux '
                                                                                                                                                                      'seuils '
                                                                                                                                                                      'sélectionnés. '
                                                                                                                                                                      'Elle '
                                                                                                                                                                      'ne '
                                                                                                                                                                      'la '
                                                                                                                                                                      'compare '
                                                                                                                                                                      'pas '
                                                                                                                                                                      'au '
                                                                                                                                                                      'fond '
                                                                                                                                                                      'habituel '
                                                                                                                                                                      'de '
                                                                                                                                                                      'cet '
                                                                                                                                                                      'emplacement.',
 'This factor is only a relative device comparison and is not an absolute radiation calibration.': 'This factor is '
                                                                                                   'only a relative '
                                                                                                   'device comparison '
                                                                                                   'and is not an '
                                                                                                   'absolute radiation '
                                                                                                   'calibration.',
 'This report is descriptive and is not a radiation-safety classification.': 'Ce rapport est descriptif et ne '
                                                                             'constitue pas une classification de '
                                                                             'radioprotection.',
 'Thresholds can be changed in the add-on configuration.': 'Les seuils peuvent être modifiés dans la configuration de '
                                                           'l’add-on.',
 'Thu': 'Jeu',
 'Thursday': 'Jeudi',
 'Tilted': 'Tilted',
 'Time series': 'Série temporelle',
 'Time series, Poisson comparison and weekday/hour heatmap': 'Série temporelle, comparaison de Poisson et carte '
                                                             'thermique jour/heure',
 'Time-series PNG': 'Série temporelle PNG',
 'Timestamp diagnostics': 'Diagnostic des horodatages',
 'Timezone': 'Fuseau horaire',
 'Today so far bundle': 'Archive de la journée en cours',
 'Too few pressure/CPM pairs': 'Trop peu de paires pression/CPM',
 'Too few valid paired measurements for a reliable device comparison': 'Trop peu de mesures appariées valides pour une '
                                                                       'comparaison fiable',
 'Too little or too fragmented for strong conclusions': 'Trop peu de données ou données trop fragmentées pour des '
                                                        'conclusions solides',
 'Trend (30 min)': 'Tendance (30 min)',
 'Tue': 'Mar',
 'Tuesday': 'Mardi',
 'Type DELETE ALL GMC HISTORY to confirm': 'Type DELETE ALL GMC HISTORY to confirm',
 'Type RESTORE to confirm': 'Saisissez RESTORE pour confirmer',
 'Typical for {weekday} at {hour}:00': 'Typique pour {weekday} à {hour}:00',
 'USB down': 'Vertical, USB en bas',
 'USB left': 'Vertical, USB à gauche',
 'USB right': 'Vertical, USB à droite',
 'USB up': 'Vertical, USB en haut',
 'UTC timestamp': 'Horodatage UTC',
 'Unavailable': 'Indisponible',
 'Unconfirmed values since bridge start': 'Unconfirmed values since bridge start',
 'Uncritical': 'Sans danger immédiat',
 'Uncritical: below warning threshold': 'Non critique : sous le seuil d’avertissement',
 'Unknown': 'Inconnu',
 'Unknown GMC': 'Appareil GMC inconnu',
 'Unknown report device': 'Appareil de rapport inconnu',
 'Unknown serial device': 'Unknown serial device',
 'Unstable': 'Instable',
 'Unsupported report format': 'Format de rapport non pris en charge',
 'Upload errors': 'Erreurs d’envoi',
 'Upload errors since start': 'Erreurs d’envoi depuis le démarrage',
 'Upload failed': 'Échec de l’envoi',
 'Upload successful': 'Envoi réussi',
 'Uploading': 'Envoi en cours',
 'Upright': 'Upright',
 'Use this as context only and review longer periods before drawing conclusions.': 'Utilisez ceci uniquement comme '
                                                                                   'contexte et examinez des périodes '
                                                                                   'plus longues avant de tirer des '
                                                                                   'conclusions.',
 'Valid measurements': 'Mesures valides',
 'Variance / mean': 'Variance / moyenne',
 'Very close to Poisson-like spread': 'Très proche d’une dispersion de type Poisson',
 'Very complete 24 h data window': 'Fenêtre de données sur 24 h très complète',
 'Very strong linear relationship': 'Très forte relation linéaire',
 'Very weak linear relationship': 'Très faible relation linéaire',
 'Voltage': 'Tension',
 'Voltage Errors Since Start': 'Erreurs de tension depuis le démarrage',
 'Voltage [V]': 'Tension [V]',
 'Voltage correlation': 'Corrélation avec la tension',
 'Waiting for enough recent measurements': 'En attente de mesures récentes suffisantes',
 'Waiting for first upload': 'En attente du premier envoi',
 'Waiting for recent measurements': 'En attente de mesures récentes',
 'Waiting for the first accepted measurement': 'Waiting for the first accepted measurement',
 'Warning': 'Avertissement',
 'Warning from {warning} s; critical from {critical} s': 'Avertissement à partir de {warning} s ; critique à partir de '
                                                         '{critical} s',
 'Warning threshold exceeded': 'Seuil d’avertissement dépassé',
 'Warning thresholds': 'Seuils d’avertissement',
 'Weak linear relationship': 'Faible relation linéaire',
 'Weather pressure sources disagree': 'Les sources de pression météo divergent',
 'Wed': 'Mer',
 'Wednesday': 'Mercredi',
 'Weekday': 'Jour de la semaine',
 'Weekday/hour heatmap': 'Carte thermique jour/heure',
 'What does the historical trend mean?': 'Que signifie la tendance historique ?',
 'What each report preserves and how periods are defined': 'Contenu de chaque rapport et définition des périodes',
 'What should I do?': 'Que dois-je faire ?',
 'What this assessment means': 'Signification de cette évaluation',
 'Why are Poisson values shown?': 'Pourquoi les valeurs de Poisson sont-elles affichées ?',
 'Why is this assessment shown?': 'Pourquoi cette évaluation est-elle affichée ?',
 'Within local background range': 'Dans la plage du fond local',
 'Within normal statistical variation': 'Dans la variation statistique normale',
 'Within the usual local range': 'Dans la plage locale habituelle',
 'Within warning range': 'Dans la plage d’avertissement',
 'Yellow': 'Jaune',
 'Z-score = (latest CPM − 24 h mean) / 24 h standard deviation.': 'Score Z = (dernier CPM − moyenne 24 h) / écart-type '
                                                                  '24 h.',
 'Z-score formula explanation': 'Score Z = (dernier CPM − moyenne 24 h) / écart-type 24 h.',
 'complete and regularly spaced data': 'données complètes et régulièrement espacées',
 'confirmations': 'confirmations',
 'counting uncertainty {value:.2f}%': 'counting uncertainty {value:.2f}%',
 'coverage': 'couverture',
 'daily values': 'valeurs quotidiennes',
 'days': 'jours',
 'duplicates / clock regressions': 'doublons / retours d’horloge',
 'entity patterns': 'entity patterns',
 'errors': 'errors',
 'estimated signal probability': 'probabilité estimée du signal',
 'excluded measurements': 'mesures exclues',
 'longest gap {value} s': 'plus longue lacune {value} s',
 'measurements': 'measurements',
 'minimum sample coverage': 'couverture minimale des mesures',
 'n={count} paired samples': 'n={count} paires de mesures',
 'n={count} · {coverage:.1f}% coverage': 'n={count} · couverture {coverage:.1f}%',
 'paired samples': 'paires de mesures',
 'reconnects': 'reconnects',
 'relative to baseline': 'par rapport à la référence',
 'score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s': 'score {score:.1f}/100 · couverture '
                                                                           '{coverage:.1f}% · plus longue lacune {gap} '
                                                                           's',
 'short / long intervals': 'intervalles courts / longs',
 'since the current bridge start': 'since the current bridge start',
 'temperature coverage {value}%': 'couverture de température {value}%',
 'unknown': 'inconnu',
 'valid hourly values': 'valeurs horaires valides',
 'valid paired samples': 'paires de mesures valides',
 'voltage coverage {value}%': 'couverture de tension {value}%',
 'write errors since app start': 'write errors since app start',
 '{before:.2f} → {after:.2f} CPM · {sigma:.1f}σ · {hours} h persistent': '{before:.2f} → {after:.2f} CPM · '
                                                                         '{sigma:.1f}σ · {hours} h persistent',
 '{check_type} result cached for {seconds} s · schema v{schema}': 'Résultat {check_type} mis en cache pendant '
                                                                  '{seconds} s · schéma v{schema}',
 '{connected} connected · {disconnected} disconnected': '{connected} connected · {disconnected} disconnected',
 '{count} implausible measurements were excluded from the assessment': '{count} mesures non plausibles ont été exclues '
                                                                       'de l’évaluation',
 '{count} measurements': '{count} mesures',
 '{count} measurements and {events} events were removed.': '{count} measurements and {events} events were removed.',
 '{events} events · {diagnostics} diagnostics': '{events} events · {diagnostics} diagnostics',
 '{gyro_note} History retention: {days} days. Daily periods are local calendar days; weekly periods are ISO weeks from Monday through Sunday.': '{gyro_note} '
                                                                                                                                                'Conservation '
                                                                                                                                                'de '
                                                                                                                                                'l’historique '
                                                                                                                                                ': '
                                                                                                                                                '{days} '
                                                                                                                                                'jours. '
                                                                                                                                                'Les '
                                                                                                                                                'périodes '
                                                                                                                                                'quotidiennes '
                                                                                                                                                'sont '
                                                                                                                                                'des '
                                                                                                                                                'jours '
                                                                                                                                                'calendaires '
                                                                                                                                                'locaux '
                                                                                                                                                '; '
                                                                                                                                                'les '
                                                                                                                                                'périodes '
                                                                                                                                                'hebdomadaires '
                                                                                                                                                'sont '
                                                                                                                                                'des '
                                                                                                                                                'semaines '
                                                                                                                                                'ISO '
                                                                                                                                                'du '
                                                                                                                                                'lundi '
                                                                                                                                                'au '
                                                                                                                                                'dimanche.',
 '{model} — Radiation monitoring report': '{model} — Rapport de surveillance du rayonnement',
 '{seconds} seconds ago': '{seconds} seconds ago',
 '{value:g} h': '{value:g} h',
 '{value:g} min': '{value:g} min',
 '{value} clock regressions observed': '{value} retours d’horloge observés',
 '{value} duplicate timestamps observed': '{value} horodatages en double observés',
 '{value} long intervals': '{value} intervalles longs',
 '{value} unusually short intervals': '{value} intervalles anormalement courts',
 '{value} vs local baseline': '{value} par rapport à la référence locale',
 '{value}% time-window coverage': 'couverture de la fenêtre {value}%'}

# Runtime presentation templates added in 7.1.4.
CATALOG.update({
    'Comparison confidence: {confidence}': 'Niveau de confiance de la comparaison : {confidence}',
    'Confidence: {confidence}': 'Niveau de confiance : {confidence}',
    'Status': 'État',
    'Typical background': 'Fond typique',
    'Valid paired samples': 'Paires de mesures valides',
    'Warning from {warning:g} s; critical from {critical:g} s': 'Avertissement à partir de {warning:g} s ; critique à partir de {critical:g} s',
    'valid hourly values · {days:.1f} days · {span:.1f} hPa': 'valeurs horaires valides · {days:.1f} jours · {span:.1f} hPa',
    '{a:+.1f}% / {b:+.1f}%': '{a:+.1f}% / {b:+.1f}%',
    '{b} × factor → {a}': '{b} × facteur → {a}',
    '{content}': '{content}',
    '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)': '{date} : {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)',
    '{days} days': '{days} jours',
    '{dose:.3f} µSv/h': '{dose:.3f} µSv/h',
    '{first} {second}': '{first} {second}',
    '{from_value} → {to_value}': '{from_value} → {to_value}',
    '{note} · n={samples}': '{note} · n={samples}',
    '{pairs} valid paired samples': '{pairs} paires de mesures valides',
    '{pairs} valid paired samples · counting uncertainty {value:.2f}%': '{pairs} paires de mesures valides · incertitude de comptage {value:.2f}%',
    '{probability:.0f}% estimated signal probability': '{probability:.0f} % de probabilité estimée du signal',
    '{span:.0f} {days_label} · {count} {daily_label}': '{span:.0f} {days_label} · {count} {daily_label}',
    '{start}–{end} °C · {samples} Samples': '{start}–{end} °C · {samples} mesures',
    '{trend:+.1f} CPM': '{trend:+.1f} CPM',
    '{value:g} µSv/h': '{value:g} µSv/h',
    'Last uploaded CPM': 'Dernier CPM transmis',
    'Last uploaded ACPM': 'Dernier ACPM transmis',
    'GMCMap last uploaded ACPM': 'Dernier ACPM transmis à GMCMap',
    'GMCMap ACPM accepted samples': 'Mesures acceptées pour l’ACPM GMCMap',
    'ACPM is the average of all accepted CPM readings since the current app measurement session began.': 'L’ACPM est la moyenne de toutes les mesures CPM acceptées depuis le début de la session de mesure actuelle de l’application.',
    'User manual': 'Manuel d’utilisation',
    'Open user manual PDF': 'Ouvrir le manuel d’utilisation en PDF',
    'User manual is not available': 'Le manuel d’utilisation n’est pas disponible',
})

# Version 8.2.1 report and history labels.
CATALOG.update({
    'Accepted measurements [count]': 'Mesures acceptées [nombre]',
    'Local hour [h]': 'Heure locale [h]',
    'Mean count rate [CPM]': 'Taux de comptage moyen [CPM]',
    'Radiation Monitoring': 'Surveillance des rayonnements',
    'Rejected raw value': 'Valeur brute rejetée',
})


# Version 8.2.1 complete runtime localization.
CATALOG.update({
    'The recent level differs from counting noise with {probability:.2f}% statistical confidence': 'Le niveau récent se distingue du bruit de comptage avec un niveau de confiance statistique de {probability:.2f} %',
    'A comparable or more extreme hourly level occurred about once in {rarity:.1f} historical hours': "Un niveau horaire comparable ou plus extrême s'est produit environ une fois toutes les {rarity:.1f} heures historiques",
})

# Long-term analysis 9.1.1
CATALOG.update({'24 hours': '24 heures', '30 days': '30 jours', '365 days': '365 jours', '7 days': '7 jours', '7-day rolling median': 'Médiane glissante sur 7 jours', '90 days': '90 jours', '95% block-bootstrap interval for mean': 'Intervalle bootstrap par blocs à 95 % pour la moyenne', '95% block-bootstrap interval for median': 'Intervalle bootstrap par blocs à 95 % pour la médiane', 'Air-pressure association': 'Association avec la pression atmosphérique', 'Annual projection from the last 30 days: {value} µSv': 'Projection annuelle à partir des 30 derniers jours : {value} µSv', 'Annual projection is not shown until a sufficiently complete 30-day period exists.': 'La projection annuelle n’est affichée qu’après une période de 30 jours suffisamment complète.', 'Based on {hours} covered hours': 'Basé sur {hours} heures couvertes', 'Bootstrap uncertainty, distribution dispersion, EWMA and CUSUM': 'Incertitude bootstrap, dispersion, EWMA et CUSUM', 'Calendar heat map': 'Carte thermique du calendrier', 'Calendar heat map of daily median CPM': 'Carte thermique des médianes CPM quotidiennes', 'Connected periods above the robust local long-term threshold': 'Périodes continues au-dessus du seuil local robuste à long terme', 'Contextual Fano-like ratio; rolling CPM values are not independent Poisson counts': 'Rapport contextuel de type Fano ; les CPM glissants ne sont pas des comptages de Poisson indépendants', 'Correlation does not prove causation.': 'La corrélation ne prouve pas la causalité.', 'Coverage {coverage}% · at least {required}% required': 'Couverture {coverage} % · au moins {required} % requis', 'Covered hours': 'Heures couvertes', 'Cumulative derived dose': 'Dose cumulée dérivée', 'Daily and monthly development': 'Évolution quotidienne et mensuelle', 'Daily median': 'Médiane quotidienne', 'Daily median and 7-day rolling median': 'Médiane quotidienne et médiane glissante sur 7 jours', 'Daily medians, rolling median and calendar view': 'Médianes quotidiennes, médiane glissante et vue calendrier', 'Derived cumulative dose: {dose} µSv': 'Dose cumulée dérivée : {dose} µSv', 'Derived dose (µSv)': 'Dose dérivée (µSv)', 'Derived from the robust local background; not an official alarm threshold': 'Dérivé du fond local robuste ; ce n’est pas un seuil d’alarme officiel', 'Duration (h)': 'Durée (h)', 'EWMA, CUSUM, trend tests and relative event detection provide statistical context only. They do not identify a radiation source and do not replace calibrated radiation-protection measurements.': 'EWMA, CUSUM, les tests de tendance et la détection relative fournissent uniquement un contexte statistique. Ils n’identifient pas une source et ne remplacent pas des mesures étalonnées de radioprotection.', 'Effective sample size': 'Taille effective de l’échantillon', 'Environmental correlations are exploratory. They may reflect common time patterns, ventilation, weather or other confounding factors and do not prove causation.': 'Les corrélations environnementales sont exploratoires. Elles peuvent refléter des rythmes communs, la ventilation, la météo ou d’autres facteurs et ne prouvent pas la causalité.', 'Excess area (CPM·h)': 'Aire d’excès (CPM·h)', 'Exploratory Spearman correlations at 0, 3, 6, 12 and 24 hour lags': 'Corrélations de Spearman exploratoires avec décalages de 0, 3, 6, 12 et 24 heures', 'Higher': 'Plus élevé', 'Hourly dispersion ratio': 'Rapport de dispersion horaire', 'Lagged environmental associations': 'Associations environnementales décalées', 'Long-term analysis': 'Analyse à long terme', 'Long-term analysis for {device}': 'Analyse à long terme pour {device}', 'Long-term background, cumulative dose, trend, recurring patterns and statistical process diagnostics': 'Fond à long terme, dose cumulée, tendance, motifs récurrents et diagnostic statistique du processus', 'Long-term overview': 'Vue d’ensemble à long terme', 'Long-term statistical diagnostics': 'Diagnostics statistiques à long terme', 'Long-term trend': 'Tendance à long terme', 'Lower': 'Plus faible', 'Mann-Kendall test with Sen slope on sufficiently covered daily medians': 'Test de Mann-Kendall avec pente de Sen sur les médianes quotidiennes suffisamment couvertes', 'Maximum CPM': 'CPM maximal', 'Mean CPM': 'CPM moyen', 'Median CPM': 'CPM médian', 'Median {median} CPM · coverage {coverage}%': 'Médiane {median} CPM · couverture {coverage} %', 'Month': 'Mois', 'Monthly aggregates': 'Agrégats mensuels', 'Moving blocks preserve short-range time dependence': 'Les blocs mobiles préservent la dépendance temporelle à court terme', 'No calendar data available': 'Aucune donnée de calendrier disponible', 'No long-term analysis available yet': 'Aucune analyse à long terme disponible pour le moment', 'No monthly aggregates available': 'Aucun agrégat mensuel disponible', 'No persistent CUSUM signal detected': 'Aucun signal CUSUM persistant détecté', 'No persistent EWMA signal detected': 'Aucun signal EWMA persistant détecté', 'No persistent relative elevation episodes detected': 'Aucun épisode relatif persistant détecté', 'No supported dose conversion for this period': 'Aucune conversion de dose prise en charge pour cette période', 'No value is calculated until enough hourly pairs are available.': 'Aucune valeur n’est calculée avant de disposer de suffisamment de paires horaires.', 'Not enough daily values for a long-term chart': 'Pas assez de valeurs quotidiennes pour un graphique à long terme', 'Not enough paired data': 'Pas assez de données appariées', 'Not yet meaningful': 'Pas encore interprétable', 'Only {covered} of {required} days covered': 'Seulement {covered} jours sur {required} couverts', 'Persistent elevation episodes': 'Épisodes d’élévation persistante', 'Persistent episodes': 'Épisodes persistants', 'Preliminary': 'Préliminaire', 'Ready': 'Exploitable', 'Real time windows with duration and coverage checks': 'Fenêtres temporelles réelles avec contrôle de durée et de couverture', 'Recent 7-day median relative to the robust long-term background': 'Médiane récente sur 7 jours par rapport au fond robuste à long terme', 'Recent background deviation': 'Écart récent au fond', 'Relative event threshold': 'Seuil d’événement relatif', 'Robust local background': 'Fond local robuste', 'Scientific interpretation': 'Interprétation scientifique', 'Start': 'Début', 'Statistical signal detected': 'Signal statistique détecté', 'Stored measurements are required before long-term statistics can be calculated.': 'Des mesures enregistrées sont nécessaires pour calculer les statistiques à long terme.', 'Strongest at {lag} h lag · {pairs} pairs · {strength} association': 'Association la plus forte avec un décalage de {lag} h · {pairs} paires · association {strength}', 'Temperature association': 'Association avec la température', 'The detector uses the robust long-term local background and does not replace radiation-safety alarms.': 'La détection utilise le fond local robuste à long terme et ne remplace pas les alarmes de radioprotection.', 'Time at or above configured danger threshold': 'Temps au niveau ou au-dessus du seuil de danger configuré', 'Time in configured warning range': 'Temps dans la plage d’avertissement configurée', 'Typical range P05–P95: {low}–{high} CPM': 'Plage typique P05-P95 : {low}-{high} CPM', 'moderate': 'modérée', 'strong': 'forte', 'weak': 'faible', '{date}: median {median} CPM, coverage {coverage}%': '{date} : médiane {median} CPM, couverture {coverage} %', '{direction} · {slope} CPM/day · p={p}': '{direction} · {slope} CPM/jour · p={p}', '{hours} covered hours': '{hours} heures couvertes', '{hours} total elevated hours · longest {longest} h': '{hours} heures élevées au total · plus longue {longest} h', '{observed} daily observations · correlation duration {duration} days': '{observed} observations quotidiennes · durée de corrélation {duration} jours', '{replicates} replicates · block length {block} days': '{replicates} répétitions · longueur de bloc {block} jours', 'Long-term': 'Long terme', 'stable': 'stable', 'increasing': 'croissante', 'decreasing': 'décroissante'})

# Recent baseline wording 9.1.1
CATALOG.update({'Recent baseline context': 'Contexte récent de la ligne de base', 'Seven-day baseline deviation, drift and sustained relative events': 'Écart à la ligne de base sur 7 jours, dérive et événements relatifs persistants'})


# Extended agreement and seasonal analysis 9.1.1
CATALOG.update({'Bland-Altman bias': 'Biais de Bland-Altman', '95% limits of agreement': 'Limites d’accord à 95 %', 'Mean signed difference A minus B': 'Différence moyenne signée A moins B', 'Exploratory paired-device agreement; correlation alone does not establish agreement.': 'Accord exploratoire entre appareils appariés ; la corrélation seule ne démontre pas l’accord.', 'Seasonal month-of-year profile': 'Profil saisonnier par mois de l’année', 'Median CPM by calendar month across available years': 'Médiane CPM par mois civil sur les années disponibles', 'Calendar month': 'Mois civil', 'Days represented': 'Jours représentés', 'Not enough months for a seasonal profile': 'Pas assez de mois pour un profil saisonnier', 'At least six represented calendar months are required.': 'Au moins six mois civils représentés sont requis.', 'Exploratory seasonal summary; it does not separate weather, location, detector or calibration changes.': 'Résumé saisonnier exploratoire ; il ne sépare pas les changements de météo, de lieu, de détecteur ou d’étalonnage.'})


# Evidence-based long-term presentation and field-test diagnostics 10.0.1
CATALOG.update({'{available} of {required} required hourly pairs are available.': '{available} of {required} required hourly pairs are available.', 'FDR-adjusted p={value}': 'FDR-adjusted p={value}', 'Practical magnitude not available': 'Practical magnitude not available', 'Moderate practical magnitude': 'Moderate practical magnitude', 'Estimated change {value}% per month · {magnitude}': 'Estimated change {value}% per month · {magnitude}', 'Runtime since service start': 'Runtime since service start', 'Cumulative counters reset when the service restarts.': 'Cumulative counters reset when the service restarts.', 'GMCMap transmission': 'GMCMap transmission', 'Export field-test protocol (JSON)': 'Exporter le protocole de test terrain (JSON)', '{months} represented calendar months': '{months} represented calendar months', 'Statistical process diagnostics': 'Diagnostic statistique du processus', 'At least 30 sufficiently complete days and an adequate effective sample size are required.': 'At least 30 sufficiently complete days and an adequate effective sample size are required.', '{success} successful · {errors} failed uploads': '{success} successful · {errors} failed uploads', 'No statistically clear long-term trend is visible': 'No statistically clear long-term trend is visible', 'Longest data gap': 'Longest data gap', 'Stored samples: {count}': 'Stored samples: {count}', 'Field-test interpretation': 'Field-test interpretation', 'A falling long-term tendency is visible': 'A falling long-term tendency is visible', 'Large practical magnitude': 'Large practical magnitude', '{days} covered days · {observed} daily observations': '{days} covered days · {observed} daily observations', 'Data basis': 'Base de données', 'A rising long-term tendency is visible': 'A rising long-term tendency is visible', 'Small practical magnitude': 'Small practical magnitude', 'Current background context': 'Contexte de fond actuel', 'Annual projection from the last 90 days: {value} µSv': 'Projection annuelle à partir des 90 derniers jours : {value} µSv', 'The main result first; method details remain available below.': 'The main result first; method details remain available below.', 'Annual projection is not shown until a sufficiently complete 90-day period exists.': 'La projection annuelle nécessite une période de 90 jours suffisamment complète.', 'Supported': 'Étayer', 'Well supported': 'Très bien étayé', 'Extended statistical methods': 'Méthodes statistiques avancées', 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.': 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.', 'USB / serial recovery': 'USB / serial recovery', 'Database write errors': 'Database write errors', 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.': 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.', 'Plain-language assessment': 'Synthèse compréhensible', '{errors} serial errors · {reconnects} reconnects': '{errors} serial errors · {reconnects} reconnects', 'Long-term reliability field test': 'Test de fiabilité à long terme', 'No reliable long-term trend can be assessed yet': 'No reliable long-term trend can be assessed yet', 'Operational counters for USB, database continuity and GMCMap transmission': 'Operational counters for USB, database continuity and GMCMap transmission', 'EWMA, CUSUM and dispersion diagnostics; statistical context only': 'EWMA, CUSUM and dispersion diagnostics; statistical context only', '{count} detected gaps above the expected interval': '{count} detected gaps above the expected interval', 'Trend method details': 'Trend method details', 'FDR-adjusted significance not available': 'FDR-adjusted significance not available', 'Exploratory Spearman correlations with false-discovery-rate correction': 'Exploratory Spearman correlations with false-discovery-rate correction', 'Seasonal assessment': 'Seasonal assessment', 'Not evaluable': 'Non évaluable', 'Integrated derived dose in the measured period': 'Integrated derived dose in the measured period', 'Exploratory': 'Exploratoire', 'Confidence intervals, effective sample size, test statistics and practical effect size': 'Confidence intervals, effective sample size, test statistics and practical effect size', 'Very small practical magnitude': 'Very small practical magnitude'})

# Complete localized overrides for 10.0.1
CATALOG.update({'Not evaluable': 'Non évaluable', 'Exploratory': 'Exploratoire', 'Supported': 'Étayer', 'Well supported': 'Très bien étayé', 'Very small practical magnitude': 'Importance pratique très faible', 'Small practical magnitude': 'Faible importance pratique', 'Moderate practical magnitude': 'Importance pratique modérée', 'Large practical magnitude': 'Grande importance pratique', 'Practical magnitude not available': 'Importance pratique indisponible', 'No reliable long-term trend can be assessed yet': 'Aucune tendance fiable à long terme ne peut encore être évaluée', 'At least 30 sufficiently complete days and an adequate effective sample size are required.': 'Au moins 30 jours suffisamment complets et une taille d’échantillon effective adéquate sont nécessaires.', 'A rising long-term tendency is visible': 'Une tendance haussière à long terme est visible', 'A falling long-term tendency is visible': 'Une tendance baissière à long terme est visible', 'No statistically clear long-term trend is visible': 'Aucune tendance statistiquement nette à long terme n’est visible', 'Estimated change {value}% per month · {magnitude}': 'Variation estimée de {value} % par mois · {magnitude}', 'Runtime since service start': 'Durée de fonctionnement depuis le démarrage du service', 'Cumulative counters reset when the service restarts.': 'Les compteurs cumulés sont réinitialisés au redémarrage du service.', 'USB / serial recovery': 'Récupération USB / série', '{errors} serial errors · {reconnects} reconnects': '{errors} erreurs série · {reconnects} reconnexions', 'Longest data gap': 'Plus longue lacune de données', '{count} detected gaps above the expected interval': '{count} lacunes détectées au-delà de l’intervalle attendu', 'Database write errors': 'Erreurs d’écriture de la base de données', 'Stored samples: {count}': 'Mesures enregistrées : {count}', 'GMCMap transmission': 'Transmission GMCMap', '{success} successful · {errors} failed uploads': '{success} réussis · {errors} échecs', 'Export field-test protocol (JSON)': 'Exporter le protocole de test terrain (JSON)', 'Field-test interpretation': 'Interprétation du test terrain', 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.': 'Ces compteurs de fonctionnement aident à évaluer la fiabilité à long terme. Ils ne certifient ni l’étalonnage du détecteur ni la précision des mesures.', '{available} of {required} required hourly pairs are available.': '{available} des {required} paires horaires requises sont disponibles.', 'FDR-adjusted p={value}': 'p ajusté FDR={value}', 'FDR-adjusted significance not available': 'Significativité ajustée FDR indisponible', 'Plain-language assessment': 'Synthèse compréhensible', 'The main result first; method details remain available below.': 'Le résultat principal d’abord ; les détails méthodologiques restent disponibles ci-dessous.', 'Current background context': 'Contexte de fond actuel', 'Data basis': 'Base de données', '{days} covered days · {observed} daily observations': '{days} jours couverts · {observed} observations quotidiennes', 'Integrated derived dose in the measured period': 'Dose dérivée intégrée sur la période mesurée', 'Seasonal assessment': 'Évaluation saisonnière', '{months} represented calendar months': '{months} mois civils représentés', 'Extended statistical methods': 'Méthodes statistiques avancées', 'Confidence intervals, effective sample size, test statistics and practical effect size': 'Intervalles de confiance, taille effective, statistiques de test et importance pratique', 'Trend method details': 'Détails de la méthode de tendance', 'Statistical process diagnostics': 'Diagnostic statistique du processus', 'EWMA, CUSUM and dispersion diagnostics; statistical context only': 'Diagnostics EWMA, CUSUM et dispersion ; contexte statistique uniquement', 'Exploratory Spearman correlations with false-discovery-rate correction': 'Corrélations exploratoires de Spearman avec correction du taux de fausses découvertes', 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.': 'Les corrélations environnementales sont exploratoires. La correction de Benjamini-Hochberg réduit les fausses découvertes entre les décalages testés, mais ne justifie aucune conclusion causale.', 'Long-term reliability field test': 'Test terrain de fiabilité à long terme', 'Operational counters for USB, database continuity and GMCMap transmission': 'Compteurs de fonctionnement pour USB, continuité de la base de données et transmission GMCMap', 'Annual projection from the last 90 days: {value} µSv': 'Projection annuelle à partir des 90 derniers jours : {value} µSv', 'Annual projection is not shown until a sufficiently complete 90-day period exists.': 'La projection annuelle n’est affichée qu’après une période de 90 jours suffisamment complète.'})
