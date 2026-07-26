from __future__ import annotations

CATALOG: dict[str, str] = {'1 h counting uncertainty': '1 h counting uncertainty',
 '1 h coverage': 'Cobertura de 1 h',
 '1 h mean': 'Media de 1 h',
 '1 h mean / 7 d mean × 100': 'Media de 1 h / media de 7 d × 100',
 '1 h mean dose rate': 'Tasa de dosis media de 1 h',
 '1 h mean minus 7 d baseline': 'Media de 1 h menos línea base de 7 d',
 '24 h Fano factor': 'Factor de Fano de 24 h',
 '24 h P95': 'P95 de 24 h',
 '24 h P99': 'P99 de 24 h',
 '24 h Z-score': 'Puntuación Z de 24 h',
 '24 h counting uncertainty': '24 h counting uncertainty',
 '24 h distribution, percentiles and latest-value deviation': 'Distribución de 24 h, percentiles y desviación del '
                                                              'último valor',
 '24 h maximum': 'Máximo de 24 h',
 '24 h mean': 'Media de 24 h',
 '24 h mean dose rate': 'Tasa de dosis media de 24 h',
 '24 h median': 'Mediana de 24 h',
 '24 h minimum': 'Mínimo de 24 h',
 '24 h standard deviation': 'Desviación estándar de 24 h',
 '50th percentile': 'Percentil 50',
 '7 d baseline': 'Línea base de 7 d',
 '7 d baseline dose rate': 'Tasa de dosis de la línea base de 7 días',
 '7 d baseline drift': 'Deriva de la línea base de 7 días',
 '7 d counting uncertainty': '7 d counting uncertainty',
 '7-day smoothed daily median': 'Mediana diaria suavizada durante 7 días',
 '95th percentile': 'Percentil 95',
 '99th percentile': 'Percentil 99',
 'A device function is temporarily unavailable.': 'Una función del dispositivo no está disponible temporalmente.',
 'A fresh backup is recommended before deletion.': 'A fresh backup is recommended before deletion.',
 'A recent position change can affect comparability': 'Un cambio reciente de posición puede afectar la comparabilidad',
 'Above the typical time profile': 'Por encima del perfil temporal típico',
 'Above the usual local range': 'Por encima del rango local habitual',
 'Absolute radiation assessment': 'Evaluación absoluta de la radiación',
 'Absolute thresholds and local anomaly detection answer different questions.': 'Los umbrales absolutos y la detección '
                                                                                'local de anomalías responden a '
                                                                                'preguntas distintas.',
 'Acceleration magnitude': 'Magnitud de aceleración',
 'Acceleration raw values': 'Valores brutos de aceleración',
 'Accepted device values are stored separately after live CPM plausibility confirmation': 'Accepted device values are '
                                                                                          'stored separately after '
                                                                                          'live CPM plausibility '
                                                                                          'confirmation',
 'Active threshold profile': 'Perfil de umbrales activo',
 'Adaptive background profile': 'Perfil de fondo adaptativo',
 'Advanced': 'Avanzado',
 'Advanced diagnostics': 'Diagnóstico avanzado',
 'Advanced visuals': 'Visualizaciones avanzadas',
 'Affected GMC devices': 'Affected GMC devices',
 'Agreement': 'Concordancia',
 'Air-pressure source': 'Fuente de presión atmosférica',
 'Air-pressure trend': 'Tendencia de presión atmosférica',
 'All GMC history was deleted': 'All GMC history was deleted',
 'All baselines and comparisons use the same robust quality-filtered measurements.': 'Todas las líneas base y '
                                                                                     'comparaciones usan las mismas '
                                                                                     'mediciones robustas filtradas '
                                                                                     'por calidad.',
 'All connected GMC devices': 'Todos los dispositivos GMC conectados',
 'All devices': 'Todos los dispositivos',
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
 'All statistical values, confidence intervals and diagnostics': 'Todos los valores estadísticos, intervalos de '
                                                                 'confianza y diagnósticos',
 'All {count} known GMC devices are connected': 'All {count} known GMC devices are connected',
 'Allow restore': 'Permitir restauración',
 'Already assigned to {name}': 'Already assigned to {name}',
 'Analysis': 'Análisis',
 'Analysis JSON': 'JSON de análisis',
 'Analysis PDF': 'PDF de análisis',
 'Analysis depth': 'Nivel de análisis',
 'Analysis for': 'Análisis de',
 'Analysis is still being prepared': 'Analysis is still being prepared',
 'Analysis shown': 'Análisis mostrado',
 'Analysis, the traffic light and downloads will become meaningful after the first stored samples arrive.': 'El '
                                                                                                            'análisis, '
                                                                                                            'el '
                                                                                                            'semáforo '
                                                                                                            'y las '
                                                                                                            'descargas '
                                                                                                            'serán '
                                                                                                            'significativos '
                                                                                                            'cuando se '
                                                                                                            'almacenen '
                                                                                                            'las '
                                                                                                            'primeras '
                                                                                                            'mediciones.',
 'Analyze this device': 'Analizar este dispositivo',
 'Another report is already being generated': 'Ya se está generando otro informe',
 'Another report or maintenance job is running': 'Another report or maintenance job is running',
 'Another report or restore job is running': 'Ya hay otro informe o restauración en curso',
 'Another report, maintenance export, or restore job is running': 'Ya se está ejecutando otro informe, exportación de '
                                                                  'mantenimiento o proceso de restauración.',
 'App Started At': 'Aplicación iniciada a las',
 'Apply': 'Apply',
 'Assessment': 'Evaluación',
 'Assigned': 'Assigned',
 'At least 24 h reference and 6 h persistence are required': 'At least 24 h reference and 6 h persistence are required',
 'At least two daily background values are required.': 'Se requieren al menos dos valores diarios de fondo.',
 'At least {count} valid hourly values are required': 'Se requieren al menos {count} valores horarios válidos',
 'At least {count} valid pairs are required': 'Se requieren al menos {count} pares válidos',
 'At least {days} days of learning data are required': 'Se requieren al menos {days} días de datos de aprendizaje',
 'At least {span:g} hPa pressure variation is required': 'Se requiere una variación de presión de al menos {span:g} '
                                                         'hPa',
 'At the same time, the value is clearly above the usual local background. Review the trend and measurement conditions.': 'Al '
                                                                                                                          'mismo '
                                                                                                                          'tiempo, '
                                                                                                                          'el '
                                                                                                                          'valor '
                                                                                                                          'está '
                                                                                                                          'claramente '
                                                                                                                          'por '
                                                                                                                          'encima '
                                                                                                                          'del '
                                                                                                                          'fondo '
                                                                                                                          'local '
                                                                                                                          'habitual. '
                                                                                                                          'Revise '
                                                                                                                          'la '
                                                                                                                          'tendencia '
                                                                                                                          'y '
                                                                                                                          'las '
                                                                                                                          'condiciones '
                                                                                                                          'de '
                                                                                                                          'medición.',
 'Automatic device detection is running': 'Automatic device detection is running',
 'Automatic refresh is temporarily unavailable': 'Automatic refresh is temporarily unavailable',
 'Availability': 'Disponibilidad',
 'Available': 'Available',
 'Back to analysis': 'Back to analysis',
 'Background index': 'Índice de fondo',
 'Background index compares the rolling 1 h mean with the available 7 d baseline.': 'Índice de fondo = media móvil de '
                                                                                    '1 h respecto a la línea base '
                                                                                    'disponible de 7 días.',
 'Background index formula explanation': 'Índice de fondo = media móvil de 1 h respecto a la línea base disponible de '
                                         '7 días.',
 'Background trend over days and months': 'Evolución del fondo durante días y meses',
 'Backup is compatible and ready to restore.': 'Backup is compatible and ready to restore.',
 'Backup preview failed': 'Backup preview failed',
 'Baseline available': 'Línea base disponible',
 'Baseline currently stable': 'Línea base actualmente estable',
 'Baseline deviation': 'Desviación de la línea base',
 'Baseline deviation, drift and sustained relative events': 'Desviación y deriva de la línea base y eventos relativos '
                                                            'sostenidos',
 'Baseline deviation: {cpm} CPM ({percent}%)': 'Desviación de la línea base: {cpm} CPM ({percent} %)',
 'Baseline drift: {value}%': 'Deriva de la línea base: {value} %',
 'Baseline learning in progress': 'Aprendizaje de la línea base en curso',
 'Baseline readiness': 'Disponibilidad de la línea base',
 'Baseline: {value} CPM': 'Línea base: {value} CPM',
 'Battery voltage': 'Tensión de la batería',
 'Baud rate': 'Velocidad en baudios',
 'Below the typical time profile': 'Por debajo del perfil temporal típico',
 'Below warning threshold': 'Por debajo del umbral de advertencia',
 'BfS and ICRP reference profiles convert annual dose values into continuous-rate equivalents for context. They are not official instantaneous alarm limits and cannot replace professional dose assessment.': 'Los '
                                                                                                                                                                                                               'perfiles '
                                                                                                                                                                                                               'de '
                                                                                                                                                                                                               'referencia '
                                                                                                                                                                                                               'BfS '
                                                                                                                                                                                                               'e '
                                                                                                                                                                                                               'ICRP '
                                                                                                                                                                                                               'convierten '
                                                                                                                                                                                                               'dosis '
                                                                                                                                                                                                               'anuales '
                                                                                                                                                                                                               'en '
                                                                                                                                                                                                               'equivalentes '
                                                                                                                                                                                                               'de '
                                                                                                                                                                                                               'tasa '
                                                                                                                                                                                                               'continua '
                                                                                                                                                                                                               'como '
                                                                                                                                                                                                               'contexto. '
                                                                                                                                                                                                               'No '
                                                                                                                                                                                                               'son '
                                                                                                                                                                                                               'límites '
                                                                                                                                                                                                               'oficiales '
                                                                                                                                                                                                               'de '
                                                                                                                                                                                                               'alarma '
                                                                                                                                                                                                               'instantánea '
                                                                                                                                                                                                               'ni '
                                                                                                                                                                                                               'sustituyen '
                                                                                                                                                                                                               'una '
                                                                                                                                                                                                               'evaluación '
                                                                                                                                                                                                               'dosimétrica '
                                                                                                                                                                                                               'profesional.',
 'BfS reference projection': 'Proyección de referencia BfS',
 'Both connected counters show a quality-filtered simultaneous rise': 'Ambos contadores conectados muestran un aumento '
                                                                      'simultáneo filtrado por calidad',
 'Both connected counters show a simultaneous rise': 'Ambos contadores conectados muestran un aumento simultáneo',
 'Broadly compatible with Poisson-like spread': 'En general compatible con una dispersión tipo Poisson',
 'CPM': 'CPM',
 'CPM and derived dose rate': 'CPM y tasa de dosis derivada',
 'CPM distribution and Poisson comparison': 'Distribución de CPM y comparación de Poisson',
 'CPM distribution — {title}': 'Distribución de CPM — {title}',
 'CPM is the primary measurement.': 'CPM es la medición principal.',
 'CPM per µSv/h': 'CPM por µSv/h',
 'CPM quality': 'Calidad de CPM',
 'CPM statistics  min {minimum:.0f} | max {maximum:.0f} | mean {mean:.2f} | median {median:.2f} | SD {sd:.2f} | P95 {p95:.2f} | missing {missing}': 'Estadísticas '
                                                                                                                                                    'CPM  '
                                                                                                                                                    'mín. '
                                                                                                                                                    '{minimum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'máx. '
                                                                                                                                                    '{maximum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'media '
                                                                                                                                                    '{mean:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'mediana '
                                                                                                                                                    '{median:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'DE '
                                                                                                                                                    '{sd:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'P95 '
                                                                                                                                                    '{p95:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'faltantes '
                                                                                                                                                    '{missing}',
 'CPM statistics: no accepted measurements in selected period': 'Estadísticas CPM: no hay mediciones aceptadas en el '
                                                                'periodo seleccionado',
 'CPM–pressure correlation': 'Correlación CPM–presión',
 'CPM–temperature correlation': 'Correlación CPM–temperatura',
 'CPM–voltage correlation': 'Correlación CPM–tensión',
 'CSV files preserve every accepted measurement without interpolation. PNG reports include CPM, temperature, voltage, optional raw signed gyro diagnostics, summary statistics, sample completeness, device identity, timezone, period and generation time. ZIP bundles additionally contain analysis JSON, daily summaries, events, histogram, heatmap and a multi-page PDF report.': 'Los '
                                                                                                                                                                                                                                                                                                                                                                                       'archivos '
                                                                                                                                                                                                                                                                                                                                                                                       'CSV '
                                                                                                                                                                                                                                                                                                                                                                                       'conservan '
                                                                                                                                                                                                                                                                                                                                                                                       'cada '
                                                                                                                                                                                                                                                                                                                                                                                       'medición '
                                                                                                                                                                                                                                                                                                                                                                                       'aceptada '
                                                                                                                                                                                                                                                                                                                                                                                       'sin '
                                                                                                                                                                                                                                                                                                                                                                                       'interpolación. '
                                                                                                                                                                                                                                                                                                                                                                                       'Los '
                                                                                                                                                                                                                                                                                                                                                                                       'informes '
                                                                                                                                                                                                                                                                                                                                                                                       'PNG '
                                                                                                                                                                                                                                                                                                                                                                                       'incluyen '
                                                                                                                                                                                                                                                                                                                                                                                       'CPM, '
                                                                                                                                                                                                                                                                                                                                                                                       'temperatura, '
                                                                                                                                                                                                                                                                                                                                                                                       'tensión, '
                                                                                                                                                                                                                                                                                                                                                                                       'diagnósticos '
                                                                                                                                                                                                                                                                                                                                                                                       'giroscópicos '
                                                                                                                                                                                                                                                                                                                                                                                       'brutos '
                                                                                                                                                                                                                                                                                                                                                                                       'con '
                                                                                                                                                                                                                                                                                                                                                                                       'signo '
                                                                                                                                                                                                                                                                                                                                                                                       'opcionales, '
                                                                                                                                                                                                                                                                                                                                                                                       'estadísticas '
                                                                                                                                                                                                                                                                                                                                                                                       'resumidas, '
                                                                                                                                                                                                                                                                                                                                                                                       'cobertura, '
                                                                                                                                                                                                                                                                                                                                                                                       'identidad '
                                                                                                                                                                                                                                                                                                                                                                                       'del '
                                                                                                                                                                                                                                                                                                                                                                                       'dispositivo, '
                                                                                                                                                                                                                                                                                                                                                                                       'zona '
                                                                                                                                                                                                                                                                                                                                                                                       'horaria, '
                                                                                                                                                                                                                                                                                                                                                                                       'periodo '
                                                                                                                                                                                                                                                                                                                                                                                       'y '
                                                                                                                                                                                                                                                                                                                                                                                       'hora '
                                                                                                                                                                                                                                                                                                                                                                                       'de '
                                                                                                                                                                                                                                                                                                                                                                                       'generación. '
                                                                                                                                                                                                                                                                                                                                                                                       'Los '
                                                                                                                                                                                                                                                                                                                                                                                       'paquetes '
                                                                                                                                                                                                                                                                                                                                                                                       'ZIP '
                                                                                                                                                                                                                                                                                                                                                                                       'incluyen '
                                                                                                                                                                                                                                                                                                                                                                                       'además '
                                                                                                                                                                                                                                                                                                                                                                                       'JSON '
                                                                                                                                                                                                                                                                                                                                                                                       'de '
                                                                                                                                                                                                                                                                                                                                                                                       'análisis, '
                                                                                                                                                                                                                                                                                                                                                                                       'resúmenes '
                                                                                                                                                                                                                                                                                                                                                                                       'diarios, '
                                                                                                                                                                                                                                                                                                                                                                                       'eventos, '
                                                                                                                                                                                                                                                                                                                                                                                       'histograma, '
                                                                                                                                                                                                                                                                                                                                                                                       'mapa '
                                                                                                                                                                                                                                                                                                                                                                                       'de '
                                                                                                                                                                                                                                                                                                                                                                                       'calor '
                                                                                                                                                                                                                                                                                                                                                                                       'y '
                                                                                                                                                                                                                                                                                                                                                                                       'un '
                                                                                                                                                                                                                                                                                                                                                                                       'informe '
                                                                                                                                                                                                                                                                                                                                                                                       'PDF '
                                                                                                                                                                                                                                                                                                                                                                                       'de '
                                                                                                                                                                                                                                                                                                                                                                                       'varias '
                                                                                                                                                                                                                                                                                                                                                                                       'páginas.',
 'Calibrated acceleration': 'Aceleración calibrada',
 'Calibration profile': 'Perfil de calibración',
 'Capabilities': 'Capacidades',
 'Check location, orientation and environmental conditions when a persistent jump appears.': 'Comprueba la ubicación, '
                                                                                             'la orientación y las '
                                                                                             'condiciones ambientales '
                                                                                             'cuando aparezca un salto '
                                                                                             'persistente.',
 'Check manually': 'Comprobar manualmente',
 'Check the Home Assistant general settings and restart the add-on.': 'Compruebe los ajustes generales de Home '
                                                                      'Assistant y reinicie el complemento.',
 'Check the USB cable and power supply if this continues for more than 15 minutes.': 'Comprueba el cable USB y la '
                                                                                     'alimentación si esto continúa '
                                                                                     'durante más de 15 minutos.',
 'Check the measurement conditions, observe the trend and verify the reading with an appropriate instrument if it persists.': 'Compruebe '
                                                                                                                              'las '
                                                                                                                              'condiciones '
                                                                                                                              'de '
                                                                                                                              'medición, '
                                                                                                                              'observe '
                                                                                                                              'la '
                                                                                                                              'tendencia '
                                                                                                                              'y '
                                                                                                                              'verifique '
                                                                                                                              'la '
                                                                                                                              'lectura '
                                                                                                                              'con '
                                                                                                                              'un '
                                                                                                                              'instrumento '
                                                                                                                              'adecuado '
                                                                                                                              'si '
                                                                                                                              'persiste.',
 'Check the measurement location': 'Comprobar el lugar de medición',
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
 'Choose how much detail the analysis cards show. The selection is stored in this browser.': 'Elija cuánto detalle '
                                                                                             'muestran las tarjetas de '
                                                                                             'análisis. La selección '
                                                                                             'se guarda en este '
                                                                                             'navegador.',
 'Choose whether reports include all devices or one selected device.': 'Elige si los informes incluyen todos los '
                                                                       'dispositivos o solo uno seleccionado.',
 'Clear': 'Clear',
 'Clearly above the usual local range': 'Claramente por encima del rango local habitual',
 'Clearly elevated': 'Claramente elevado',
 'Clearly elevated: clearly above the usual local range': 'Claramente elevado: claramente por encima del rango local '
                                                          'habitual',
 'Clock offset exceeds warning threshold': 'La desviación del reloj supera el umbral de aviso',
 'Clock synchronized': 'Reloj sincronizado',
 'Close to Poisson expectation': 'Cerca de la expectativa de Poisson',
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
 'Compared with local baseline': 'Comparado con la línea base local',
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
 'Compares the current value with the usual background at this location.': 'Compara el valor actual con el fondo '
                                                                           'habitual de esta ubicación.',
 'Comparison confidence': 'Confianza de la comparación',
 'Complete ZIP bundle': 'Paquete ZIP completo',
 'Complete history deletion failed': 'Complete history deletion failed',
 'Complete history deletion is disabled in the app configuration.': 'La eliminación completa del historial está '
                                                                    'desactivada en la configuración de la aplicación.',
 'Completeness: {value:.2f}%': 'Integridad: {value:.2f} %',
 'Confidence': 'Confianza',
 'Configured CPM conversion factor': 'Factor de conversión CPM configurado',
 'Configured baud rate': 'Velocidad en baudios configurada',
 'Configured device name': 'Nombre de dispositivo configurado',
 'Configured location': 'Ubicación configurada',
 'Configured measurement interval': 'Intervalo de medición configurado',
 'Confirmed original samples in 24 h · {accepted} stored': 'Confirmed original samples in 24 h · {accepted} stored',
 'Connect two devices to enable comparison.': 'Conecte dos dispositivos para activar la comparación.',
 'Connect two devices to learn a relative response factor.': 'Connect two devices to learn a relative response factor.',
 'Connected GMC devices': 'Dispositivos GMC conectados',
 'Connected counters without an active stability warning': 'Contadores conectados sin advertencia activa de '
                                                           'estabilidad',
 'Connected devices': 'Dispositivos conectados',
 'Connection active': 'Connection active',
 'Consecutive upload errors': 'Errores de envío consecutivos',
 'Continue observing': 'Continuar observando',
 'Coordinates': 'Coordenadas',
 'Correlation': 'Correlación',
 'Correlation does not imply causation. Strong values should be investigated over longer periods before drawing conclusions.': 'La '
                                                                                                                               'correlación '
                                                                                                                               'no '
                                                                                                                               'implica '
                                                                                                                               'causalidad. '
                                                                                                                               'Los '
                                                                                                                               'valores '
                                                                                                                               'fuertes '
                                                                                                                               'deben '
                                                                                                                               'investigarse '
                                                                                                                               'durante '
                                                                                                                               'periodos '
                                                                                                                               'más '
                                                                                                                               'largos '
                                                                                                                               'antes '
                                                                                                                               'de '
                                                                                                                               'extraer '
                                                                                                                               'conclusiones.',
 'Cosmic influence is possible': 'Es posible una influencia cósmica',
 'Cosmic influence – statistical indication': 'Influencia cósmica – indicación estadística',
 'Counter ID': 'ID del contador',
 'Counting statistics': 'Estadísticas de conteo',
 'Counting uncertainty (68%): −{minus:.2f}/+{plus:.2f} CPM · {impulses} impulses in {duration}': 'Counting uncertainty '
                                                                                                 '(68%): '
                                                                                                 '−{minus:.2f}/+{plus:.2f} '
                                                                                                 'CPM · {impulses} '
                                                                                                 'impulses in '
                                                                                                 '{duration}',
 'Counting uncertainty not available': 'Counting uncertainty not available',
 'Country': 'País',
 'Coverage percent': 'Cobertura porcentual',
 'Coverage, gaps, runtime counters and derived dose-rate values': 'Cobertura, huecos, contadores de ejecución y tasas '
                                                                  'de dosis derivadas',
 'Critical': 'Crítico',
 'Critical: danger threshold exceeded': 'Crítico: umbral de peligro superado',
 'Current': 'Actual',
 'Current air pressure': 'Presión atmosférica actual',
 'Current database size': 'Current database size',
 'Current difference': 'Diferencia actual',
 'Current value': 'Valor actual',
 'Current value is {z:+.2f} robust standard deviations from the 24 h median': 'El valor actual está a {z:+.2f} '
                                                                              'desviaciones estándar robustas de la '
                                                                              'mediana de 24 h',
 'Current value is {z:+.2f} standard deviations from the 24 h mean': 'El valor actual está a {z:+.2f} desviaciones '
                                                                     'estándar de la media de 24 h',
 'Current week bundle': 'Paquete de la semana actual',
 'Currently selected': 'Seleccionado actualmente',
 'Custom period': 'Periodo personalizado',
 'Custom thresholds': 'Umbrales personalizados',
 'Daily and weekly profile is still being formed': 'El perfil diario y semanal aún se está formando',
 'Daily quality-filtered medians are smoothed over seven days. The period cards compare the recent part of each period with the preceding part; detected jumps are statistical changes and do not determine their cause.': 'Las '
                                                                                                                                                                                                                           'medianas '
                                                                                                                                                                                                                           'diarias '
                                                                                                                                                                                                                           'filtradas '
                                                                                                                                                                                                                           'por '
                                                                                                                                                                                                                           'calidad '
                                                                                                                                                                                                                           'se '
                                                                                                                                                                                                                           'suavizan '
                                                                                                                                                                                                                           'durante '
                                                                                                                                                                                                                           'siete '
                                                                                                                                                                                                                           'días. '
                                                                                                                                                                                                                           'Las '
                                                                                                                                                                                                                           'tarjetas '
                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                           'período '
                                                                                                                                                                                                                           'comparan '
                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                           'parte '
                                                                                                                                                                                                                           'reciente '
                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                           'cada '
                                                                                                                                                                                                                           'período '
                                                                                                                                                                                                                           'con '
                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                           'anterior; '
                                                                                                                                                                                                                           'los '
                                                                                                                                                                                                                           'saltos '
                                                                                                                                                                                                                           'detectados '
                                                                                                                                                                                                                           'son '
                                                                                                                                                                                                                           'cambios '
                                                                                                                                                                                                                           'estadísticos '
                                                                                                                                                                                                                           'y '
                                                                                                                                                                                                                           'no '
                                                                                                                                                                                                                           'determinan '
                                                                                                                                                                                                                           'su '
                                                                                                                                                                                                                           'causa.',
 'Daily summary CSV': 'CSV de resumen diario',
 'Danger threshold exceeded': 'Umbral de peligro superado',
 'Danger thresholds': 'Umbrales de peligro',
 'Danger zone': 'Danger zone',
 'Dashboard navigation': 'Dashboard navigation',
 'Data exports': 'Exportaciones de datos',
 'Data period': 'Data period',
 'Data quality': 'Calidad de datos',
 'Data quality is too low for a reliable assessment': 'La calidad de los datos es demasiado baja para una evaluación '
                                                      'fiable',
 'Data quality status unavailable': 'Estado de calidad de datos no disponible',
 'Data quality: {value}': 'Calidad de datos: {value}',
 'Database': 'Database',
 'Database health': 'Estado de la base de datos',
 'Database size': 'Tamaño de la base',
 'Date': 'Fecha',
 'Delete all GMC history': 'Delete all GMC history',
 'Delete history': 'Delete history',
 'Deletion confirmation text must be exactly DELETE ALL GMC HISTORY': 'Deletion confirmation text must be exactly '
                                                                      'DELETE ALL GMC HISTORY',
 'Deletion is disabled by default.': 'Deletion is disabled by default.',
 'Derived dose rate': 'Tasa de dosis derivada',
 'Derived from 1 h mean CPM': 'Derivado de la media CPM de 1 h',
 'Derived from 24 h mean CPM': 'Derivado de la media CPM de 24 h',
 'Derived from 7 d mean CPM': 'Derivado de la media CPM de 7 d',
 'Derived from latest CPM': 'Derivado del último CPM',
 'Detailed interpretation and the most useful supporting values': 'Interpretación detallada y los valores de apoyo más '
                                                                  'útiles',
 'Detect, identify and assign GMC counters': 'Detect, identify and assign GMC counters',
 'Detected': 'Detectado',
 'Detected Capabilities': 'Capacidades detectadas',
 'Detected GMC device': 'Detected GMC device',
 'Detected baseline jumps': 'Saltos de línea base detectados',
 'Detected relative anomaly events: {count}': 'Eventos de anomalía relativa detectados: {count}',
 'Deviation': 'Desviación',
 'Device': 'Dispositivo',
 'Device Profile': 'Perfil del dispositivo',
 'Device Time Errors Since Start': 'Errores de hora del dispositivo desde el inicio',
 'Device assignments saved': 'Device assignments saved',
 'Device assignments were saved.': 'Device assignments were saved.',
 'Device baseline': 'Línea base del dispositivo',
 'Device capabilities': 'Funciones del dispositivo',
 'Device clock': 'Reloj del dispositivo',
 'Device clock offset': 'Desviación del reloj del dispositivo',
 'Device clock status': 'Estado del reloj del dispositivo',
 'Device clock unavailable': 'Reloj del dispositivo no disponible',
 'Device clock warning': 'Device clock warning',
 'Device comparison': 'Comparación de dispositivos',
 'Device details, live values and analysis selection are shown below.': 'A continuación se muestran los detalles, los '
                                                                        'valores actuales y la selección de análisis '
                                                                        'de cada dispositivo.',
 'Device health warning': 'Device health warning',
 'Device position': 'Posición del dispositivo',
 'Device status updated': 'Device status updated',
 'Device temperature is unavailable.': 'La temperatura del dispositivo no está disponible.',
 'Device time': 'Hora del dispositivo',
 'Device-specific details are listed above.': 'Los detalles de cada dispositivo aparecen en la sección superior.',
 'Device: {value}': 'Dispositivo: {value}',
 'Devices': 'Devices',
 'Diagnostics JSON': 'JSON de diagnóstico',
 'Disabled': 'Desactivado',
 'Discarded CPM peaks': 'Discarded CPM peaks',
 'Discarded unconfirmed CPM peaks': 'Discarded unconfirmed CPM peaks',
 'Display down': 'Plano, pantalla hacia abajo',
 'Display up': 'Plano, pantalla hacia arriba',
 'Dose rate = CPM / configured conversion factor ({factor:g} CPM per µSv/h).': 'Tasa de dosis = CPM / factor de '
                                                                               'conversión configurado ({factor:g} CPM '
                                                                               'por µSv/h).',
 'Dose rate formula explanation': 'Tasa de dosis = CPM / factor de conversión configurado ({factor:g} CPM por µSv/h).',
 'Dose-rate values are derived from CPM using the configured conversion factor.': 'Las tasas de dosis se derivan de '
                                                                                  'CPM mediante el factor de '
                                                                                  'conversión configurado.',
 'Dose-rate values, traffic-light states and events are derived indicators. CPM remains the primary measurement.': 'Las '
                                                                                                                   'tasas '
                                                                                                                   'de '
                                                                                                                   'dosis, '
                                                                                                                   'los '
                                                                                                                   'estados '
                                                                                                                   'del '
                                                                                                                   'semáforo '
                                                                                                                   'y '
                                                                                                                   'los '
                                                                                                                   'eventos '
                                                                                                                   'son '
                                                                                                                   'indicadores '
                                                                                                                   'derivados. '
                                                                                                                   'CPM '
                                                                                                                   'sigue '
                                                                                                                   'siendo '
                                                                                                                   'la '
                                                                                                                   'medición '
                                                                                                                   'principal.',
 'Download': 'Descargar',
 'Downloads': 'Descargas',
 'Dual-tube measurement': 'Medición con dos tubos',
 'Duration [s]': 'Duración [s]',
 'During the learning phase, leave the counters in a stable location and allow additional measurements to accumulate.': 'Durante '
                                                                                                                        'la '
                                                                                                                        'fase '
                                                                                                                        'de '
                                                                                                                        'aprendizaje, '
                                                                                                                        'deja '
                                                                                                                        'los '
                                                                                                                        'contadores '
                                                                                                                        'en '
                                                                                                                        'una '
                                                                                                                        'ubicación '
                                                                                                                        'estable '
                                                                                                                        'y '
                                                                                                                        'permite '
                                                                                                                        'que '
                                                                                                                        'se '
                                                                                                                        'acumulen '
                                                                                                                        'más '
                                                                                                                        'mediciones.',
 'Each device has its own MQTT identity and history. The cards show the latest accepted measurement.': 'Cada '
                                                                                                       'dispositivo '
                                                                                                       'tiene su '
                                                                                                       'propia '
                                                                                                       'identidad MQTT '
                                                                                                       'y su propio '
                                                                                                       'historial. Las '
                                                                                                       'tarjetas '
                                                                                                       'muestran la '
                                                                                                       'última '
                                                                                                       'medición '
                                                                                                       'aceptada.',
 'Each physical serial device can only be assigned once': 'Each physical serial device can only be assigned once',
 'Elevated': 'Elevado',
 'Elevated relative background': 'Fondo relativo elevado',
 'Elevated: within warning range': 'Elevado: dentro del rango de advertencia',
 'Elevation': 'Altitud',
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
 'Enable enable_restore in the app configuration and restart only when a restore is planned.': 'Active enable_restore '
                                                                                               'en la configuración de '
                                                                                               'la aplicación y '
                                                                                               'reinicie solo cuando '
                                                                                               'vaya a realizar una '
                                                                                               'restauración.',
 'Enable “{setting}” in the app configuration and restart only when a restore is planned.': 'Active « {setting} » en '
                                                                                            'la configuración de la '
                                                                                            'aplicación y reinicie '
                                                                                            'solo cuando vaya a '
                                                                                            'realizar una '
                                                                                            'restauración.',
 'End time UTC': 'Hora final UTC',
 'End time local': 'Hora final local',
 'Entities': 'Entidades',
 'Environment': 'Entorno',
 'Error time': 'Hora del error',
 'Estimated pressure influence': 'Influencia estimada de la presión',
 'Evaluated by': 'Evaluado según',
 'Evaluates the current value using the configured thresholds.': 'Evalúa el valor actual con los umbrales '
                                                                 'configurados.',
 'Events CSV': 'CSV de eventos',
 'Events and diagnostics': 'Events and diagnostics',
 'Events last 24 h': 'Eventos de las últimas 24 h',
 'Excellent': 'Excelente',
 'Excluded measurements': 'Mediciones excluidas',
 'Excluded pairs': 'Pares excluidos',
 'Expand all': 'Expand all',
 'Expected samples': 'Muestras esperadas',
 'Expert view': 'Vista experta',
 'Explanation of the two assessments': 'Explicación de las dos evaluaciones',
 'Export details': 'Detalles de exportación',
 'Extremely elevated': 'Extremadamente elevado',
 'Extremely elevated: far above the usual local range': 'Extremadamente elevado: muy por encima del rango local '
                                                        'habitual',
 'Falling': 'Descendente',
 'Falling air pressure can slightly increase the share of cosmically generated secondary radiation at ground level, while rising air pressure tends to reduce it; the model detects only such statistical relationships and cannot clearly distinguish them from other natural influences.': 'La '
                                                                                                                                                                                                                                                                                             'disminución '
                                                                                                                                                                                                                                                                                             'de '
                                                                                                                                                                                                                                                                                             'la '
                                                                                                                                                                                                                                                                                             'presión '
                                                                                                                                                                                                                                                                                             'atmosférica '
                                                                                                                                                                                                                                                                                             'puede '
                                                                                                                                                                                                                                                                                             'aumentar '
                                                                                                                                                                                                                                                                                             'ligeramente '
                                                                                                                                                                                                                                                                                             'la '
                                                                                                                                                                                                                                                                                             'proporción '
                                                                                                                                                                                                                                                                                             'de '
                                                                                                                                                                                                                                                                                             'radiación '
                                                                                                                                                                                                                                                                                             'secundaria '
                                                                                                                                                                                                                                                                                             'de '
                                                                                                                                                                                                                                                                                             'origen '
                                                                                                                                                                                                                                                                                             'cósmico '
                                                                                                                                                                                                                                                                                             'a '
                                                                                                                                                                                                                                                                                             'nivel '
                                                                                                                                                                                                                                                                                             'del '
                                                                                                                                                                                                                                                                                             'suelo, '
                                                                                                                                                                                                                                                                                             'mientras '
                                                                                                                                                                                                                                                                                             'que '
                                                                                                                                                                                                                                                                                             'el '
                                                                                                                                                                                                                                                                                             'aumento '
                                                                                                                                                                                                                                                                                             'de '
                                                                                                                                                                                                                                                                                             'la '
                                                                                                                                                                                                                                                                                             'presión '
                                                                                                                                                                                                                                                                                             'tiende '
                                                                                                                                                                                                                                                                                             'a '
                                                                                                                                                                                                                                                                                             'reducirla; '
                                                                                                                                                                                                                                                                                             'el '
                                                                                                                                                                                                                                                                                             'modelo '
                                                                                                                                                                                                                                                                                             'solo '
                                                                                                                                                                                                                                                                                             'detecta '
                                                                                                                                                                                                                                                                                             'estas '
                                                                                                                                                                                                                                                                                             'relaciones '
                                                                                                                                                                                                                                                                                             'estadísticas '
                                                                                                                                                                                                                                                                                             'y '
                                                                                                                                                                                                                                                                                             'no '
                                                                                                                                                                                                                                                                                             'puede '
                                                                                                                                                                                                                                                                                             'distinguirlas '
                                                                                                                                                                                                                                                                                             'claramente '
                                                                                                                                                                                                                                                                                             'de '
                                                                                                                                                                                                                                                                                             'otras '
                                                                                                                                                                                                                                                                                             'influencias '
                                                                                                                                                                                                                                                                                             'naturales.',
 'Falling air pressure is often associated with a slightly higher intensity of cosmically generated secondary radiation at ground level, while rising air pressure is associated with a slightly lower intensity. The strength of this relationship depends on detector, location and atmosphere; the cause cannot be determined unambiguously from total counts.': 'Una '
                                                                                                                                                                                                                                                                                                                                                                    'presión '
                                                                                                                                                                                                                                                                                                                                                                    'atmosférica '
                                                                                                                                                                                                                                                                                                                                                                    'descendente '
                                                                                                                                                                                                                                                                                                                                                                    'suele '
                                                                                                                                                                                                                                                                                                                                                                    'asociarse '
                                                                                                                                                                                                                                                                                                                                                                    'con '
                                                                                                                                                                                                                                                                                                                                                                    'una '
                                                                                                                                                                                                                                                                                                                                                                    'intensidad '
                                                                                                                                                                                                                                                                                                                                                                    'ligeramente '
                                                                                                                                                                                                                                                                                                                                                                    'mayor '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'radiación '
                                                                                                                                                                                                                                                                                                                                                                    'secundaria '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'origen '
                                                                                                                                                                                                                                                                                                                                                                    'cósmico '
                                                                                                                                                                                                                                                                                                                                                                    'a '
                                                                                                                                                                                                                                                                                                                                                                    'nivel '
                                                                                                                                                                                                                                                                                                                                                                    'del '
                                                                                                                                                                                                                                                                                                                                                                    'suelo, '
                                                                                                                                                                                                                                                                                                                                                                    'mientras '
                                                                                                                                                                                                                                                                                                                                                                    'que '
                                                                                                                                                                                                                                                                                                                                                                    'una '
                                                                                                                                                                                                                                                                                                                                                                    'presión '
                                                                                                                                                                                                                                                                                                                                                                    'ascendente '
                                                                                                                                                                                                                                                                                                                                                                    'se '
                                                                                                                                                                                                                                                                                                                                                                    'asocia '
                                                                                                                                                                                                                                                                                                                                                                    'con '
                                                                                                                                                                                                                                                                                                                                                                    'una '
                                                                                                                                                                                                                                                                                                                                                                    'intensidad '
                                                                                                                                                                                                                                                                                                                                                                    'ligeramente '
                                                                                                                                                                                                                                                                                                                                                                    'menor. '
                                                                                                                                                                                                                                                                                                                                                                    'La '
                                                                                                                                                                                                                                                                                                                                                                    'intensidad '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'esta '
                                                                                                                                                                                                                                                                                                                                                                    'relación '
                                                                                                                                                                                                                                                                                                                                                                    'depende '
                                                                                                                                                                                                                                                                                                                                                                    'del '
                                                                                                                                                                                                                                                                                                                                                                    'detector, '
                                                                                                                                                                                                                                                                                                                                                                    'la '
                                                                                                                                                                                                                                                                                                                                                                    'ubicación '
                                                                                                                                                                                                                                                                                                                                                                    'y '
                                                                                                                                                                                                                                                                                                                                                                    'la '
                                                                                                                                                                                                                                                                                                                                                                    'atmósfera; '
                                                                                                                                                                                                                                                                                                                                                                    'la '
                                                                                                                                                                                                                                                                                                                                                                    'causa '
                                                                                                                                                                                                                                                                                                                                                                    'no '
                                                                                                                                                                                                                                                                                                                                                                    'puede '
                                                                                                                                                                                                                                                                                                                                                                    'determinarse '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'forma '
                                                                                                                                                                                                                                                                                                                                                                    'inequívoca '
                                                                                                                                                                                                                                                                                                                                                                    'a '
                                                                                                                                                                                                                                                                                                                                                                    'partir '
                                                                                                                                                                                                                                                                                                                                                                    'de '
                                                                                                                                                                                                                                                                                                                                                                    'los '
                                                                                                                                                                                                                                                                                                                                                                    'recuentos '
                                                                                                                                                                                                                                                                                                                                                                    'totales.',
 'Fano factor': 'Factor de Fano',
 'Fano factor = variance / mean; a value near 1 is consistent with Poisson-like counting statistics.': 'Factor de Fano '
                                                                                                       '= varianza / '
                                                                                                       'media; un '
                                                                                                       'valor cercano '
                                                                                                       'a 1 es '
                                                                                                       'compatible con '
                                                                                                       'un conteo tipo '
                                                                                                       'Poisson.',
 'Fano factor formula explanation': 'Factor de Fano = varianza / media; un valor cercano a 1 es compatible con un '
                                    'conteo tipo Poisson.',
 'Fano factor: {value}': 'Factor de Fano: {value}',
 'Far above the usual local range': 'Muy por encima del rango local habitual',
 'File size': 'File size',
 'Firmware version': 'Versión del firmware',
 'Flat': 'Flat',
 'Fleet intelligence': 'Análisis del conjunto de dispositivos',
 'Format': 'Formato',
 'Fri': 'Vie',
 'Friday': 'Viernes',
 'Full history ZIP': 'ZIP del historial completo',
 'GMC Radiation Monitor': 'Monitor de radiación GMC',
 'GMC Radiation Monitoring': 'Monitorización de radiación GMC',
 'GMC Reports': 'Informes GMC',
 'GMC analysis report {period}': 'Informe de análisis GMC {period}',
 'GMC detected': 'GMC detected',
 'GMC devices are being detected automatically': 'GMC devices are being detected automatically',
 'GMC radiation analysis report': 'Informe de análisis de radiación GMC',
 'GMC radiation monitoring report {period}': 'Informe de monitorización de radiación GMC {period}',
 'GMC-300/320 family': 'Familia GMC-300/320',
 'GMC-320 and GMC-500+ combined': 'GMC-320 and GMC-500+ combined',
 'GMC-500 family': 'Familia GMC-500',
 'GMC-600 family': 'Familia GMC-600',
 'GMCMap consecutive upload errors': 'Errores consecutivos de envío a GMCMap',
 'GMCMap counter ID': 'ID de contador de GMCMap',
 'GMCMap is enabled, but this device has no counter ID mapping.': 'GMCMap está activado, pero este dispositivo no '
                                                                  'tiene asignado un ID de contador.',
 'GMCMap last HTTP status': 'Último estado HTTP de GMCMap',
 'GMCMap last error time': 'Hora del último error de GMCMap',
 'GMCMap last server response': 'Última respuesta del servidor GMCMap',
 'GMCMap last successful upload': 'Último envío correcto a GMCMap',
 'GMCMap last upload attempt': 'Último intento de envío a GMCMap',
 'GMCMap last upload error': 'Último error de envío a GMCMap',
 'GMCMap last uploaded CPM': 'Último CPM enviado a GMCMap',
 'GMCMap next upload': 'Próximo envío a GMCMap',
 'GMCMap successful uploads since start': 'Envíos correctos a GMCMap desde el inicio',
 'GMCMap upload errors since start': 'Errores de envío a GMCMap desde el inicio',
 'GMCMap upload status': 'Estado de envío a GMCMap',
 'GQ manufacturer recommendation': 'Recomendación del fabricante GQ',
 'Gaps are excluded from effective counting time': 'Gaps are excluded from effective counting time',
 'Generated export exceeds the {limit_mib} MiB safety limit': 'La exportación generada supera el límite de seguridad '
                                                              'de {limit_mib} MiB.',
 'Generated maintenance export exceeds the 128 MiB safety limit': 'La exportación de mantenimiento generada supera el '
                                                                  'límite de seguridad de 128 MiB.',
 'Generated report exceeds the 64 MiB safety limit': 'El informe generado supera el límite de seguridad de 64 MiB',
 'Generic GQ GMC / RFC1201-compatible device': 'Dispositivo GQ GMC genérico compatible con RFC1201',
 'Generic RFC1201-compatible device': 'Dispositivo genérico compatible con RFC1201',
 'Global report settings': 'Ajustes globales de informes y exportaciones',
 'Good': 'Buena',
 'Green': 'Verde',
 'Gyro Calibrated {axis}': 'Gyro Calibrated {axis}',
 'Gyro Errors Since Start': 'Errores del giroscopio desde el inicio',
 'Gyro Raw {axis}': 'Valor bruto del giroscopio {axis}',
 'Gyro X': 'Giroscopio X',
 'Gyro Y': 'Giroscopio Y',
 'Gyro Z': 'Giroscopio Z',
 'Gyro data will be included when available.': 'Los datos del giroscopio se incluirán cuando estén disponibles.',
 'Gyro errors': 'Errores del giroscopio',
 'Gyro recording is disabled.': 'El registro del giroscopio está desactivado.',
 'Gyroscope': 'Giroscopio',
 'Hardware model': 'Modelo de hardware',
 'Heartbeat Errors Since Start': 'Errores de heartbeat desde el inicio',
 'Heartbeat mode': 'Modo heartbeat',
 'Heartbeat rolling 60 s CPM': 'CPM móviles de 60 s del heartbeat',
 'Heatmap PNG': 'Mapa de calor PNG',
 'Heuristic statistical assessment; not a radiation-protection classification.': 'Evaluación estadística heurística; '
                                                                                 'no es una clasificación de '
                                                                                 'protección radiológica.',
 'High': 'Alta',
 'High relative increase': 'Aumento relativo alto',
 'High-dose Tube CPM': 'Tubo de alta dosis CPM',
 'High-dose tube': 'Tubo de dosis alta',
 'Highest stored 24 h value': 'Valor máximo almacenado en 24 h',
 'Histogram PNG': 'Histograma PNG',
 'Historical chart is still being formed': 'El gráfico histórico todavía se está formando',
 'Historical development': 'Evolución histórica',
 'History': 'History',
 'History Write Errors Since Start': 'Errores de escritura del historial desde el inicio',
 'History deleted': 'History deleted',
 'History maintenance': 'Mantenimiento del historial',
 'History restore failed': 'Falló la restauración del historial',
 'History restore is disabled. Enable enable_restore in the app configuration and restart.': 'La restauración del '
                                                                                             'historial está '
                                                                                             'desactivada. Active '
                                                                                             'enable_restore en la '
                                                                                             'configuración y '
                                                                                             'reinicie.',
 'History restore is disabled. Enable “{setting}” in the app configuration and restart.': 'La restauración del '
                                                                                          'historial está desactivada. '
                                                                                          'Active « {setting} » en la '
                                                                                          'configuración de la '
                                                                                          'aplicación y reinicie.',
 'History storage warning': 'History storage warning',
 'Home Assistant API client is not configured': 'Home Assistant API client is not configured',
 'Home Assistant Recorder entity patterns': 'Home Assistant Recorder entity patterns',
 'Home Assistant Recorder history cleared': 'Home Assistant Recorder history cleared',
 'Home Assistant host UART': 'Home Assistant host UART',
 'Home Assistant location': 'Ubicación de Home Assistant',
 'How are connected counters compared?': '¿Cómo se comparan los contadores conectados?',
 'How closely the observed spread resembles Poisson-like counting': 'Qué tan cerca se parece la dispersión observada a '
                                                                    'un conteo tipo Poisson',
 'How is data quality evaluated?': '¿Cómo se evalúa la calidad de los datos?',
 'How is the background profile calculated?': '¿Cómo se calcula el perfil de fondo?',
 'How is the pressure relationship assessed?': '¿Cómo se evalúa la relación con la presión?',
 'However, the value is noticeably above the usual local background. Observe the trend.': 'Sin embargo, el valor está '
                                                                                          'notablemente por encima del '
                                                                                          'fondo local habitual. '
                                                                                          'Observe la tendencia.',
 'ICRP reference projection': 'Proyección de referencia ICRP',
 'Inclination': 'Inclinación',
 'Ingest diagnostics cleared': 'Ingest diagnostics cleared',
 'Inspecting backup…': 'Inspecting backup…',
 'Insufficient': 'Insuficiente',
 'Insufficient history for level-shift detection': 'Insufficient history for level-shift detection',
 'Insufficient paired daily values': 'No hay suficientes valores diarios comparables',
 'Integrity': 'Integridad',
 'Intelligence': 'Intelligence',
 'Intelligent radiation analysis': 'Análisis inteligente de radiación',
 'Internal database cleared': 'Internal database cleared',
 'Internal serial port': 'Internal serial port',
 'Interpret statistics with coverage in mind': 'Interpretar las estadísticas teniendo en cuenta la cobertura',
 'Interpret these values together with coverage, device stability and the historical background.': 'Interpreta estos '
                                                                                                   'valores junto con '
                                                                                                   'la cobertura, la '
                                                                                                   'estabilidad del '
                                                                                                   'dispositivo y el '
                                                                                                   'fondo histórico.',
 'Interpretation': 'Interpretación',
 'Interval diagnostics': 'Diagnóstico de intervalos',
 'Invalid deletion confirmation': 'Invalid deletion confirmation',
 'Invalid device clock response': 'Respuesta no válida del reloj del dispositivo',
 'Invalid request parameters': 'Parámetros de solicitud no válidos.',
 'Invalid serial configuration request': 'Invalid serial configuration request',
 'Keep both counters close together and similarly oriented when using the comparison as a reference.': 'Mantén ambos '
                                                                                                       'contadores '
                                                                                                       'cerca y con '
                                                                                                       'una '
                                                                                                       'orientación '
                                                                                                       'similar cuando '
                                                                                                       'uses la '
                                                                                                       'comparación '
                                                                                                       'como '
                                                                                                       'referencia.',
 'Known radio or Zigbee adapter': 'Known radio or Zigbee adapter',
 'Language': 'Idioma',
 'Last HTTP status': 'Último estado HTTP',
 'Last Successful Measurement': 'Última medición correcta',
 'Last attempt': 'Último intento',
 'Last backup requested in this browser': 'Last backup requested in this browser',
 'Last sample age': 'Antigüedad de la última medición',
 'Last server response': 'Última respuesta del servidor',
 'Last successful storage': 'Last successful storage',
 'Last update': 'Última actualización',
 'Last upload': 'Último envío',
 'Last upload error': 'Último error de envío',
 'Latest CPM': 'CPM actuales',
 'Latest CPM uncertainty': 'Latest CPM uncertainty',
 'Latest CPM vs 24 h distribution': 'Último CPM frente a la distribución de 24 h',
 'Latest accepted value': 'Latest accepted value',
 'Latest dose rate': 'Tasa de dosis actual',
 'Latest measurement': 'Última medición',
 'Learned Radiation Baseline': 'Línea base de radiación aprendida',
 'Learned from local history': 'Aprendida del historial local',
 'Learned pressure coefficient': 'Coeficiente de presión aprendido',
 'Learning baseline': 'Aprendiendo la línea base',
 'Learning basis': 'Base de aprendizaje',
 'Learning progress': 'Progreso de aprendizaje',
 'Learning: not enough local history yet': 'Aprendiendo: aún no hay suficiente historial local',
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
 'Less variable than Poisson expectation': 'Menos variable que la expectativa de Poisson',
 'Likely device-specific deviation': 'Desviación probablemente específica del dispositivo',
 'Limited': 'Limitada',
 'Live radiation CPS': 'CPS de radiación en directo',
 'Live system status': 'Live system status',
 'Local background analysis': 'Análisis del fondo local',
 'Local background is still being learned': 'El fondo local todavía se está aprendiendo',
 'Local background model is available': 'El modelo de fondo local está disponible',
 'Local baseline': 'Línea base local',
 'Local hour': 'Hora local',
 'Local time [{timezone}]': 'Hora local [{timezone}]',
 'Local timestamp': 'Marca de tiempo local',
 'Location data comes from the Home Assistant general settings and is not sent to an external geocoding service.': 'Los '
                                                                                                                   'datos '
                                                                                                                   'de '
                                                                                                                   'ubicación '
                                                                                                                   'proceden '
                                                                                                                   'de '
                                                                                                                   'los '
                                                                                                                   'ajustes '
                                                                                                                   'generales '
                                                                                                                   'de '
                                                                                                                   'Home '
                                                                                                                   'Assistant '
                                                                                                                   'y '
                                                                                                                   'no '
                                                                                                                   'se '
                                                                                                                   'envían '
                                                                                                                   'a '
                                                                                                                   'ningún '
                                                                                                                   'servicio '
                                                                                                                   'externo '
                                                                                                                   'de '
                                                                                                                   'geocodificación.',
 'Location unavailable': 'Ubicación no disponible',
 'Long-term context': 'Contexto a largo plazo',
 'Long-term drift': 'Deriva a largo plazo',
 'Long-term relative factor available': 'Long-term relative factor available',
 'Long-term relative response': 'Long-term relative response',
 'Longest gap': 'Interrupción más larga',
 'Longest gap [s]': 'Mayor intervalo [s]',
 'Longest gap: {seconds} s': 'Mayor intervalo: {seconds} s',
 'Low': 'Baja',
 'Low-dose Tube CPM': 'Tubo de baja dosis CPM',
 'Low-dose tube': 'Tubo de dosis baja',
 'Lowest stored 24 h value': 'Valor mínimo almacenado en 24 h',
 'Machine-readable statistics and event data': 'Estadísticas y datos de eventos legibles por máquina',
 'Maximum': 'Máximo',
 'Maximum CPM': 'CPM máximo',
 'Maximum background index [%]': 'Índice de fondo máximo [%]',
 'Mean': 'Media',
 'Mean CPM': 'CPM medio',
 'Mean CPM by weekday and hour — {title}': 'CPM medio por día y hora — {title}',
 'Mean absolute difference': 'Diferencia absoluta media',
 'Mean: {value} CPM': 'Media: {value} CPM',
 'Measurement interval': 'Intervalo de medición',
 'Measurement-site baseline': 'Línea base combinada del lugar de medición',
 'Measurements': 'Measurements',
 'Measurements are sent to the public GMCMap service.': 'Las mediciones se envían al servicio público GMCMap.',
 'Measurements to delete': 'Measurements to delete',
 'Median': 'Mediana',
 'Median CPM': 'CPM mediano',
 'Median: {value} CPM': 'Mediana: {value} CPM',
 'Medium': 'Medio',
 'Merge a compatible SQLite backup into the current history. Existing rows are preserved or updated by device serial and UTC timestamp.': 'Fusiona '
                                                                                                                                          'una '
                                                                                                                                          'copia '
                                                                                                                                          'SQLite '
                                                                                                                                          'compatible '
                                                                                                                                          'con '
                                                                                                                                          'el '
                                                                                                                                          'historial '
                                                                                                                                          'actual. '
                                                                                                                                          'Las '
                                                                                                                                          'filas '
                                                                                                                                          'existentes '
                                                                                                                                          'se '
                                                                                                                                          'conservan '
                                                                                                                                          'o '
                                                                                                                                          'actualizan '
                                                                                                                                          'por '
                                                                                                                                          'número '
                                                                                                                                          'de '
                                                                                                                                          'serie '
                                                                                                                                          'y '
                                                                                                                                          'marca '
                                                                                                                                          'de '
                                                                                                                                          'tiempo '
                                                                                                                                          'UTC.',
 'Merged {rows} measurement rows from schema {schema}.': 'Se han combinado {rows} filas de mediciones del esquema '
                                                         '{schema}.',
 'Minimum / maximum: {minimum} / {maximum} CPM': 'Mínimo / máximo: {minimum} / {maximum} CPM',
 'Minimum CPM': 'CPM mínimo',
 'Mixed device profiles': 'Perfiles de dispositivos mixtos',
 'Moderate linear relationship': 'Relación lineal moderada',
 'Mon': 'Lun',
 'Monday': 'Lunes',
 'More history is needed before the relative background indicator is classified.': 'Se necesita más historial antes de '
                                                                                   'clasificar el indicador de fondo '
                                                                                   'relativo.',
 'More history is needed; approximately {count} additional measurements are required.': 'More history is needed; '
                                                                                        'approximately {count} '
                                                                                        'additional measurements are '
                                                                                        'required.',
 'More measurements are needed for this weekday and hour.': 'Se necesitan más mediciones para este día y esta hora.',
 'More variable than Poisson expectation': 'Más variable que la expectativa de Poisson',
 'Move away from the suspected source if safe to do so, avoid unnecessary exposure and seek qualified radiation-protection advice.': 'Aléjese '
                                                                                                                                     'de '
                                                                                                                                     'la '
                                                                                                                                     'fuente '
                                                                                                                                     'sospechosa '
                                                                                                                                     'si '
                                                                                                                                     'puede '
                                                                                                                                     'hacerlo '
                                                                                                                                     'con '
                                                                                                                                     'seguridad, '
                                                                                                                                     'evite '
                                                                                                                                     'exposiciones '
                                                                                                                                     'innecesarias '
                                                                                                                                     'y '
                                                                                                                                     'solicite '
                                                                                                                                     'asesoramiento '
                                                                                                                                     'cualificado '
                                                                                                                                     'en '
                                                                                                                                     'protección '
                                                                                                                                     'radiológica.',
 'Never': 'Nunca',
 'Newest sample': 'Muestra más reciente',
 'Next upload': 'Próximo envío',
 'No GMC device detected': 'No GMC device detected',
 'No action is required while the result remains normal. Investigate persistent changes by checking the measurement location and comparing both devices.': 'No '
                                                                                                                                                           'se '
                                                                                                                                                           'requiere '
                                                                                                                                                           'ninguna '
                                                                                                                                                           'acción '
                                                                                                                                                           'mientras '
                                                                                                                                                           'el '
                                                                                                                                                           'resultado '
                                                                                                                                                           'siga '
                                                                                                                                                           'siendo '
                                                                                                                                                           'normal. '
                                                                                                                                                           'Investiga '
                                                                                                                                                           'los '
                                                                                                                                                           'cambios '
                                                                                                                                                           'persistentes '
                                                                                                                                                           'comprobando '
                                                                                                                                                           'el '
                                                                                                                                                           'lugar '
                                                                                                                                                           'de '
                                                                                                                                                           'medición '
                                                                                                                                                           'y '
                                                                                                                                                           'comparando '
                                                                                                                                                           'ambos '
                                                                                                                                                           'dispositivos.',
 'No action is required. Continue normal monitoring.': 'No se requiere ninguna acción. Continúa con la supervisión '
                                                       'normal.',
 'No action is required. The assessment becomes more reliable as additional measurements are collected.': 'No se '
                                                                                                          'requiere '
                                                                                                          'ninguna '
                                                                                                          'acción. La '
                                                                                                          'evaluación '
                                                                                                          'será más '
                                                                                                          'fiable a '
                                                                                                          'medida que '
                                                                                                          'se '
                                                                                                          'recopilen '
                                                                                                          'más '
                                                                                                          'mediciones.',
 'No action required': 'No se requiere ninguna acción',
 'No active device warnings': 'No active device warnings',
 'No connected GMC device': 'No connected GMC device',
 'No connected counter is available yet. The next serial scan runs automatically.': 'No connected counter is available '
                                                                                    'yet. The next serial scan runs '
                                                                                    'automatically.',
 'No connected devices.': 'No hay dispositivos conectados.',
 'No current pressure source is available': 'No hay una fuente de presión actual disponible',
 'No data': 'Sin datos',
 'No known GMC devices': 'No known GMC devices',
 'No matching Home Assistant entities': 'No matching Home Assistant entities',
 'No measurement yet': 'Aún no hay mediciones',
 'No measurements in selected period': 'No hay mediciones en el periodo seleccionado',
 'No measurements yet.': 'Aún no hay mediciones.',
 'No persistent level shift detected': 'No persistent level shift detected',
 'No position changes recorded.': 'No se registraron cambios de posición.',
 'No pressure variation': 'Variación de presión insuficiente',
 'No pressure-typical signature': 'Sin firma típica de presión',
 'No pronounced baseline jumps detected.': 'No se detectaron saltos pronunciados de la línea base.',
 'No reports have been requested in this browser yet.': 'No reports have been requested in this browser yet.',
 'No shared rise detected.': 'No se detectó un aumento compartido.',
 'No stored measurements': 'No stored measurements',
 'No suitable serial device was found.': 'No suitable serial device was found.',
 'No sustained relative anomaly events detected': 'No se detectaron eventos sostenidos de anomalía relativa',
 'No valid CPM baseline': 'No hay una referencia CPM válida',
 'Normal': 'Normal',
 'Normal for this time': 'Normal para esta hora',
 'Normal: within the usual local range': 'Normal: dentro del rango local habitual',
 'Not available yet — at least two CPM samples are required': 'Aún no disponible: se requieren al menos dos mediciones '
                                                              'CPM',
 'Not available yet — more baseline history is required': 'Aún no disponible: se necesita más historial de línea base',
 'Not available yet — more paired samples are required': 'Aún no disponible: se necesitan más pares de mediciones',
 'Not available yet — no temperature samples were stored in the current 24 h window.': 'Aún no disponible: no se '
                                                                                       'almacenaron mediciones de '
                                                                                       'temperatura en la ventana '
                                                                                       'actual de 24 h.',
 'Not available yet — the 24 h CPM series needs variation and at least two samples': 'Aún no disponible: la serie CPM '
                                                                                     'de 24 h necesita variación y al '
                                                                                     'menos dos mediciones',
 'Not available yet — the 24 h mean and spread are still insufficient': 'Aún no disponible: la media y la dispersión '
                                                                        'de 24 h siguen siendo insuficientes',
 'Not available — CPM did not vary during this period': 'No disponible: el CPM no varió durante este periodo',
 'Not available — the sensor value did not vary during this period': 'No disponible: el valor del sensor no varió '
                                                                     'durante este periodo',
 'Not configured': 'No configurado',
 'Not connected': 'Not connected',
 'Not detected yet': 'Aún no detectado',
 'Not enough local history yet': 'Aún no hay suficiente historial local',
 'Not found': 'No encontrado',
 'Not recorded in this browser': 'Not recorded in this browser',
 'Not suitable as a GMC device': 'Not suitable as a GMC device',
 'Not suitable for GMC': 'Not suitable for GMC',
 'Not yet checked as a GMC device': 'Not yet checked as a GMC device',
 'Noticeable': 'Llamativo',
 'Noticeable baseline drift': 'Deriva apreciable de la línea base',
 'Noticeable difference from Poisson-like spread': 'Diferencia apreciable respecto a una dispersión tipo Poisson',
 'Noticeable statistical deviation': 'Desviación estadística apreciable',
 'Noticeable: above the usual local range': 'Llamativo: por encima del rango local habitual',
 'Number of samples': 'Número de muestras',
 'Observed': 'Observado',
 'Observed SD / √mean': 'DE observada / √media',
 'Official reference values': 'Valores oficiales de referencia',
 'Offline': 'Sin conexión',
 'Oldest sample': 'Muestra más antigua',
 'One current weather entity is available': 'Hay una entidad meteorológica actual disponible',
 'One-hour mean is {deviation:+.1f}% relative to the learned baseline': 'La media de una hora es {deviation:+.1f}% '
                                                                        'respecto a la referencia aprendida',
 'One-hour means': 'Medias de una hora',
 'One-hour robust level is {deviation:+.1f}% relative to the device baseline': 'El nivel robusto de una hora es '
                                                                               '{deviation:+.1f}% respecto a la línea '
                                                                               'base del dispositivo',
 'Online': 'En línea',
 'Only quality-filtered, one-to-one time-matched measurements are compared. Agreement, correlation, relative bias and stability are evaluated separately so one faulty counter does not automatically define the site result.': 'Solo '
                                                                                                                                                                                                                                'se '
                                                                                                                                                                                                                                'comparan '
                                                                                                                                                                                                                                'mediciones '
                                                                                                                                                                                                                                'filtradas '
                                                                                                                                                                                                                                'por '
                                                                                                                                                                                                                                'calidad '
                                                                                                                                                                                                                                'y '
                                                                                                                                                                                                                                'emparejadas '
                                                                                                                                                                                                                                'una '
                                                                                                                                                                                                                                'a '
                                                                                                                                                                                                                                'una '
                                                                                                                                                                                                                                'en '
                                                                                                                                                                                                                                'el '
                                                                                                                                                                                                                                'tiempo. '
                                                                                                                                                                                                                                'La '
                                                                                                                                                                                                                                'concordancia, '
                                                                                                                                                                                                                                'la '
                                                                                                                                                                                                                                'correlación, '
                                                                                                                                                                                                                                'el '
                                                                                                                                                                                                                                'sesgo '
                                                                                                                                                                                                                                'relativo '
                                                                                                                                                                                                                                'y '
                                                                                                                                                                                                                                'la '
                                                                                                                                                                                                                                'estabilidad '
                                                                                                                                                                                                                                'se '
                                                                                                                                                                                                                                'evalúan '
                                                                                                                                                                                                                                'por '
                                                                                                                                                                                                                                'separado '
                                                                                                                                                                                                                                'para '
                                                                                                                                                                                                                                'que '
                                                                                                                                                                                                                                'un '
                                                                                                                                                                                                                                'contador '
                                                                                                                                                                                                                                'defectuoso '
                                                                                                                                                                                                                                'no '
                                                                                                                                                                                                                                'determine '
                                                                                                                                                                                                                                'automáticamente '
                                                                                                                                                                                                                                'el '
                                                                                                                                                                                                                                'resultado '
                                                                                                                                                                                                                                'del '
                                                                                                                                                                                                                                'lugar.',
 'Only the most important conclusions at a glance': 'Solo las conclusiones más importantes de un vistazo',
 'Open': 'Open',
 'Open serial device connections': 'Open serial device connections',
 'Operational events cleared': 'Operational events cleared',
 'Orientation cannot be verified automatically': 'Orientation cannot be verified automatically',
 'Orientation changes detected': 'Orientation changes detected',
 'Orientation data is temporarily unavailable.': 'Los datos de orientación no están disponibles temporalmente.',
 'Orientation qualification': 'Orientation qualification',
 'Orientation stable': 'Orientation stable',
 'Original raw-data CSV': 'Original raw-data CSV',
 'Outliers and invalid measurements': 'Valores atípicos y mediciones no válidas',
 'Overview': 'Resumen',
 'P95 CPM': 'CPM P95',
 'P95: {value} CPM': 'P95: {value} CPM',
 'P99 CPM': 'CPM P99',
 'P99: {value} CPM': 'P99: {value} CPM',
 'PDF report': 'Informe PDF',
 'Pair-level disagreement': 'Desacuerdo a nivel de pares',
 'Pearson r · n={count} paired samples': 'r de Pearson · n={count} pares de mediciones',
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
 'Pitch angle': 'Ángulo de cabeceo',
 'Plausibilised from two weather entities': 'Plausibilizado a partir de dos entidades meteorológicas',
 'Poisson SD ratio': 'Relación DE de Poisson',
 'Poisson SD ratio = observed standard deviation / √mean; a value near 1 indicates Poisson-like spread.': 'Relación DE '
                                                                                                          'de Poisson '
                                                                                                          '= '
                                                                                                          'desviación '
                                                                                                          'estándar '
                                                                                                          'observada / '
                                                                                                          '√media; un '
                                                                                                          'valor '
                                                                                                          'cercano a 1 '
                                                                                                          'indica '
                                                                                                          'dispersión '
                                                                                                          'tipo '
                                                                                                          'Poisson.',
 'Poisson SD ratio formula explanation': 'Relación DE de Poisson = desviación estándar observada / √media; un valor '
                                         'cercano a 1 indica dispersión tipo Poisson.',
 'Poisson SD ratio: {value}': 'Relación DE de Poisson: {value}',
 'Poisson counting interval from the observed impulse count': 'Poisson counting interval from the observed impulse '
                                                              'count',
 'Poisson expectation (λ={mean:.2f})': 'Esperanza de Poisson (λ={mean:.2f})',
 'Poor': 'Deficiente',
 'Position change log': 'Registro de cambios de posición',
 'Possible GMC connection cable': 'Possible GMC connection cable',
 'Possible persistent level shift': 'Possible persistent level shift',
 'Pressure model is still being formed': 'El modelo de presión aún se está formando',
 'Pressure model unavailable': 'Modelo de presión no disponible',
 'Pressure-typical signature is pronounced': 'Firma típica de presión marcada',
 'Preview backup': 'Preview backup',
 'Previous day': 'Día anterior',
 'Previous week': 'Semana anterior',
 'Probable real change': 'Cambio real probable',
 'Probable shared measurement-site change': 'Cambio compartido probable en el lugar de medición',
 'Profile': 'Perfil del dispositivo',
 'Profile is still being formed': 'El perfil aún se está formando',
 'Provider': 'Proveedor',
 'Public GMCMap upload': 'Envío público a GMCMap',
 'Quality weight': 'Peso de calidad',
 'Quality-filtered correlation': 'Correlación filtrada por calidad',
 'Quality-filtered measurement CSV': 'Quality-filtered measurement CSV',
 'Quick downloads': 'Descargas rápidas',
 'Radiation 1 h Mean': 'Media de radiación de 1 h',
 'Radiation 1 h Median': 'Mediana de radiación de 1 h',
 'Radiation 1 h Standard Deviation': 'Desviación estándar de radiación de 1 h',
 'Radiation Baseline Deviation': 'Desviación de la línea base de radiación',
 'Radiation CPM': 'Radiación CPM',
 'Radiation Rapid Change': 'Cambio rápido de radiación',
 'Radiation count rate [CPM]': 'Tasa de conteo de radiación [CPM]',
 'Radiation counts fluctuate naturally. The Fano factor and Poisson spread ratio compare the observed variation with a simple counting-statistics model; they describe distribution shape but not a physical cause or calibration state.': 'Los '
                                                                                                                                                                                                                                           'recuentos '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'radiación '
                                                                                                                                                                                                                                           'fluctúan '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'forma '
                                                                                                                                                                                                                                           'natural. '
                                                                                                                                                                                                                                           'El '
                                                                                                                                                                                                                                           'factor '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'Fano '
                                                                                                                                                                                                                                           'y '
                                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                                           'relación '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'dispersión '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'Poisson '
                                                                                                                                                                                                                                           'comparan '
                                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                                           'variación '
                                                                                                                                                                                                                                           'observada '
                                                                                                                                                                                                                                           'con '
                                                                                                                                                                                                                                           'un '
                                                                                                                                                                                                                                           'modelo '
                                                                                                                                                                                                                                           'simple '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'estadística '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'conteo; '
                                                                                                                                                                                                                                           'describen '
                                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                                           'forma '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'la '
                                                                                                                                                                                                                                           'distribución, '
                                                                                                                                                                                                                                           'pero '
                                                                                                                                                                                                                                           'no '
                                                                                                                                                                                                                                           'una '
                                                                                                                                                                                                                                           'causa '
                                                                                                                                                                                                                                           'física '
                                                                                                                                                                                                                                           'ni '
                                                                                                                                                                                                                                           'el '
                                                                                                                                                                                                                                           'estado '
                                                                                                                                                                                                                                           'de '
                                                                                                                                                                                                                                           'calibración.',
 'Radiation measurement continues unless the device status says otherwise.': 'La medición de radiación continúa salvo '
                                                                             'que el estado del dispositivo indique lo '
                                                                             'contrario.',
 'Radiation measurement continues. An external Home Assistant temperature may be used when configured.': 'La medición '
                                                                                                         'de radiación '
                                                                                                         'continúa. '
                                                                                                         'Puede '
                                                                                                         'utilizarse '
                                                                                                         'una '
                                                                                                         'temperatura '
                                                                                                         'externa de '
                                                                                                         'Home '
                                                                                                         'Assistant '
                                                                                                         'cuando esté '
                                                                                                         'configurada.',
 'Radiation measurement continues; only the optional orientation value is affected.': 'La medición de radiación '
                                                                                      'continúa; solo se ve afectado '
                                                                                      'el valor de orientación '
                                                                                      'opcional.',
 'Radiation monitoring analysis': 'Análisis de monitorización de radiación',
 'Radiation traffic light': 'Semáforo de radiación',
 'Radiation traffic light hysteresis explanation': 'El semáforo usa histéresis: entra en amarillo al {yellow_enter:g}% '
                                                   'y sale por debajo del {yellow_clear:g}%; entra en rojo al '
                                                   '{red_enter:g}% y sale por debajo del {red_clear:g}%.',
 'Radiation traffic light uses hysteresis: it enters yellow at {yellow_enter:g}% and clears below {yellow_clear:g}%; it enters red at {red_enter:g}% and clears below {red_clear:g}%.': 'El '
                                                                                                                                                                                        'semáforo '
                                                                                                                                                                                        'usa '
                                                                                                                                                                                        'histéresis: '
                                                                                                                                                                                        'entra '
                                                                                                                                                                                        'en '
                                                                                                                                                                                        'amarillo '
                                                                                                                                                                                        'al '
                                                                                                                                                                                        '{yellow_enter:g}% '
                                                                                                                                                                                        'y '
                                                                                                                                                                                        'sale '
                                                                                                                                                                                        'por '
                                                                                                                                                                                        'debajo '
                                                                                                                                                                                        'del '
                                                                                                                                                                                        '{yellow_clear:g}%; '
                                                                                                                                                                                        'entra '
                                                                                                                                                                                        'en '
                                                                                                                                                                                        'rojo '
                                                                                                                                                                                        'al '
                                                                                                                                                                                        '{red_enter:g}% '
                                                                                                                                                                                        'y '
                                                                                                                                                                                        'sale '
                                                                                                                                                                                        'por '
                                                                                                                                                                                        'debajo '
                                                                                                                                                                                        'del '
                                                                                                                                                                                        '{red_clear:g}%.',
 'Raw CSV': 'CSV bruto',
 'Raw device values are stored separately before quality filtering': 'Raw device values are stored separately before '
                                                                     'quality filtering',
 'Raw gyro [signed int16]': 'Giroscopio bruto [int16 con signo]',
 'Raw-data archive': 'Raw-data archive',
 'Read-only mode': 'Read-only mode',
 'Ready for new measurements': 'Ready for new measurements',
 'Recent 30 days compared with the preceding 30 days': 'Últimos 30 días comparados con los 30 días anteriores',
 'Recent data quality is high': 'La calidad de los datos recientes es alta',
 'Recent period compared with the preceding period': 'Periodo reciente comparado con el periodo anterior',
 'Recent quality-filtered data quality is high': 'La calidad reciente de los datos filtrados es alta',
 'Recent reports': 'Recent reports',
 'Recommendation': 'Recomendación',
 'Recommended': 'Recommended',
 'Reconnects': 'Reconexiones',
 'Red': 'Rojo',
 'Reduced': 'Reducida',
 'Refreshing device status…': 'Refreshing device status…',
 'Relative anomaly indicator only; not a safety classification.': 'Solo es un indicador de anomalía relativa; no es '
                                                                  'una clasificación de seguridad.',
 'Relative correction factor': 'Relative correction factor',
 'Relative spread': 'Relative spread',
 'Relative to 7 d baseline': 'Respecto a la línea base de 7 d',
 'Relative-factor confidence': 'Relative-factor confidence',
 'Remaining deviation': 'Desviación restante',
 'Remove': 'Remove',
 'Report': 'Report',
 'Report generation failed': 'Falló la generación del informe',
 'Report target': 'Dispositivos del informe',
 'Reports': 'Reports',
 'Reports for the displayed analysis': 'Reports for the displayed analysis',
 'Rescan devices': 'Rescan devices',
 'Resolve persistent connection gaps before relying on long-term comparisons.': 'Resuelve las interrupciones de '
                                                                                'conexión persistentes antes de '
                                                                                'confiar en comparaciones a largo '
                                                                                'plazo.',
 'Restore backup': 'Restaurar copia',
 'Restore complete': 'Restauración completada',
 'Restore confirmation text must be exactly RESTORE': 'El texto de confirmación debe ser exactamente RESTORE',
 'Restore history': 'Restaurar historial',
 'Restore is disabled by default.': 'La restauración está desactivada de forma predeterminada.',
 'Restore upload must be between 1 byte and 128 MiB': 'El archivo de restauración debe tener entre 1 byte y 128 MiB',
 'Return to GMC Radiation Monitoring': 'Volver a la monitorización de radiación GMC',
 'Return to GMC Reports': 'Volver a los informes GMC',
 'Review the event export for timing and severity': 'Revise la exportación de eventos para ver el momento y la '
                                                    'gravedad',
 'Review the recent trend and event timing. Check both counters and the measurement location if the change persists.': 'Revisa '
                                                                                                                       'la '
                                                                                                                       'tendencia '
                                                                                                                       'reciente '
                                                                                                                       'y '
                                                                                                                       'el '
                                                                                                                       'momento '
                                                                                                                       'de '
                                                                                                                       'los '
                                                                                                                       'eventos. '
                                                                                                                       'Comprueba '
                                                                                                                       'ambos '
                                                                                                                       'contadores '
                                                                                                                       'y '
                                                                                                                       'el '
                                                                                                                       'lugar '
                                                                                                                       'de '
                                                                                                                       'medición '
                                                                                                                       'si '
                                                                                                                       'el '
                                                                                                                       'cambio '
                                                                                                                       'persiste.',
 'Rising': 'Ascendente',
 'Robust medians are used; rejected measurements and isolated spikes do not immediately change the profile.': 'Se '
                                                                                                              'utilizan '
                                                                                                              'medianas '
                                                                                                              'robustas; '
                                                                                                              'las '
                                                                                                              'mediciones '
                                                                                                              'rechazadas '
                                                                                                              'y los '
                                                                                                              'picos '
                                                                                                              'aislados '
                                                                                                              'no '
                                                                                                              'cambian '
                                                                                                              'el '
                                                                                                              'perfil '
                                                                                                              'de '
                                                                                                              'inmediato.',
 'Robust one-hour values': 'Valores robustos de una hora',
 'Roll angle': 'Ángulo de alabeo',
 'Rolling windows end at the latest stored measurement. Dose-rate values are derived from CPM using the configured factor and are not independently measured. CPM remains the primary measurement. The traffic light is a relative background-anomaly indicator, not an emergency, health, or radiation-safety classification.': 'Las '
                                                                                                                                                                                                                                                                                                                                 'ventanas '
                                                                                                                                                                                                                                                                                                                                 'móviles '
                                                                                                                                                                                                                                                                                                                                 'terminan '
                                                                                                                                                                                                                                                                                                                                 'en '
                                                                                                                                                                                                                                                                                                                                 'la '
                                                                                                                                                                                                                                                                                                                                 'última '
                                                                                                                                                                                                                                                                                                                                 'medición '
                                                                                                                                                                                                                                                                                                                                 'almacenada. '
                                                                                                                                                                                                                                                                                                                                 'Las '
                                                                                                                                                                                                                                                                                                                                 'tasas '
                                                                                                                                                                                                                                                                                                                                 'de '
                                                                                                                                                                                                                                                                                                                                 'dosis '
                                                                                                                                                                                                                                                                                                                                 'se '
                                                                                                                                                                                                                                                                                                                                 'derivan '
                                                                                                                                                                                                                                                                                                                                 'del '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'con '
                                                                                                                                                                                                                                                                                                                                 'el '
                                                                                                                                                                                                                                                                                                                                 'factor '
                                                                                                                                                                                                                                                                                                                                 'configurado '
                                                                                                                                                                                                                                                                                                                                 'y '
                                                                                                                                                                                                                                                                                                                                 'no '
                                                                                                                                                                                                                                                                                                                                 'se '
                                                                                                                                                                                                                                                                                                                                 'miden '
                                                                                                                                                                                                                                                                                                                                 'de '
                                                                                                                                                                                                                                                                                                                                 'forma '
                                                                                                                                                                                                                                                                                                                                 'independiente. '
                                                                                                                                                                                                                                                                                                                                 'El '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'sigue '
                                                                                                                                                                                                                                                                                                                                 'siendo '
                                                                                                                                                                                                                                                                                                                                 'la '
                                                                                                                                                                                                                                                                                                                                 'medición '
                                                                                                                                                                                                                                                                                                                                 'principal. '
                                                                                                                                                                                                                                                                                                                                 'El '
                                                                                                                                                                                                                                                                                                                                 'semáforo '
                                                                                                                                                                                                                                                                                                                                 'indica '
                                                                                                                                                                                                                                                                                                                                 'una '
                                                                                                                                                                                                                                                                                                                                 'anomalía '
                                                                                                                                                                                                                                                                                                                                 'relativa '
                                                                                                                                                                                                                                                                                                                                 'del '
                                                                                                                                                                                                                                                                                                                                 'fondo, '
                                                                                                                                                                                                                                                                                                                                 'no '
                                                                                                                                                                                                                                                                                                                                 'una '
                                                                                                                                                                                                                                                                                                                                 'clasificación '
                                                                                                                                                                                                                                                                                                                                 'de '
                                                                                                                                                                                                                                                                                                                                 'emergencia, '
                                                                                                                                                                                                                                                                                                                                 'salud '
                                                                                                                                                                                                                                                                                                                                 'o '
                                                                                                                                                                                                                                                                                                                                 'seguridad '
                                                                                                                                                                                                                                                                                                                                 'radiológica.',
 'SD: {value} CPM': 'DE: {value} CPM',
 'SQLite backup': 'Copia SQLite',
 'SQLite backup file': 'SQLite backup file',
 'SQLite database vacuum completed': 'SQLite database vacuum completed',
 'Sample standard deviation': 'Desviación estándar muestral',
 'Samples': 'Muestras',
 'Samples: {samples} / {expected}': 'Muestras: {samples} / {expected}',
 'Sampling interval: {interval} s | Samples: {samples}/{expected} | Completeness: {completeness:.2f}% | Generated: {generated} | App {version}': 'Intervalo: '
                                                                                                                                                 '{interval} '
                                                                                                                                                 's '
                                                                                                                                                 '| '
                                                                                                                                                 'Muestras: '
                                                                                                                                                 '{samples}/{expected} '
                                                                                                                                                 '| '
                                                                                                                                                 'Integridad: '
                                                                                                                                                 '{completeness:.2f} '
                                                                                                                                                 '% '
                                                                                                                                                 '| '
                                                                                                                                                 'Generado: '
                                                                                                                                                 '{generated} '
                                                                                                                                                 '| '
                                                                                                                                                 'App '
                                                                                                                                                 '{version}',
 'Sampling interval: {seconds} s': 'Intervalo de muestreo: {seconds} s',
 'Sat': 'Sáb',
 'Saturday': 'Sábado',
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
 'Second half vs first half of available 7 d window': 'Segunda mitad frente a la primera mitad de la ventana '
                                                      'disponible de 7 d',
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
 'Serial': 'Número de serie',
 'Serial Errors Since Start': 'Errores serie desde el inicio',
 'Serial Reconnects Since Start': 'Reconexiones serie desde el inicio',
 'Serial USB device': 'Serial USB device',
 'Serial connection recovered': 'Serial connection recovered',
 'Serial device connections': 'Serial device connections',
 'Serial errors / reconnects': 'Errores serie / reconexiones',
 'Serial port': 'Puerto serie',
 'Serial: {serial} | Period: {period} | Timezone: {timezone}': 'Número de serie: {serial} | Periodo: {period} | Zona '
                                                               'horaria: {timezone}',
 'Serial: {value}': 'Número de serie: {value}',
 'Severity': 'Gravedad',
 'Shared CPM rise': 'Aumento compartido de CPM',
 'Shared event detector': 'Detector de eventos compartidos',
 'Show analysis': 'Mostrar análisis',
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
 'Since app start': 'Desde el inicio de la aplicación',
 'Slightly noticeable': 'Ligeramente llamativo',
 'Slightly tilted': 'Slightly tilted',
 'Small baseline drift': 'Pequeña deriva de la línea base',
 'Smart Alert State': 'Estado de alerta inteligente',
 'Smoothed historical background trend': 'Tendencia histórica suavizada del fondo',
 'Source validation': 'Validación de fuentes',
 'Specific ISO week': 'Semana ISO específica',
 'Specific date': 'Fecha específica',
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
 'Stability and device health': 'Estabilidad y estado del dispositivo',
 'Stable': 'Estable',
 'Stable device path': 'Stable device path',
 'Stable devices': 'Dispositivos estables',
 'Standard deviation CPM': 'Desviación estándar CPM',
 'Start time UTC': 'Hora de inicio UTC',
 'Start time local': 'Hora de inicio local',
 'Start with a readable PDF or a complete ZIP bundle. Raw and specialist formats remain available below without crowding the main view.': 'Empiece '
                                                                                                                                          'con '
                                                                                                                                          'un '
                                                                                                                                          'PDF '
                                                                                                                                          'legible '
                                                                                                                                          'o '
                                                                                                                                          'un '
                                                                                                                                          'paquete '
                                                                                                                                          'ZIP '
                                                                                                                                          'completo. '
                                                                                                                                          'Los '
                                                                                                                                          'formatos '
                                                                                                                                          'brutos '
                                                                                                                                          'y '
                                                                                                                                          'especializados '
                                                                                                                                          'siguen '
                                                                                                                                          'disponibles '
                                                                                                                                          'más '
                                                                                                                                          'abajo '
                                                                                                                                          'sin '
                                                                                                                                          'recargar '
                                                                                                                                          'la '
                                                                                                                                          'vista '
                                                                                                                                          'principal.',
 'Statistical indication only': 'Solo indicación estadística',
 'Statistical level shift': 'Statistical level shift',
 'Statistically noticeable': 'Estadísticamente llamativo',
 'Statistics': 'Estadísticas',
 'Stored samples': 'Muestras almacenadas',
 'Stored samples across all devices': 'Mediciones guardadas de todos los dispositivos',
 'Stored samples for this device': 'Mediciones guardadas de este dispositivo',
 'Strong common signal': 'Señal compartida fuerte',
 'Strong linear relationship': 'Relación lineal fuerte',
 'Strong statistical deviation': 'Desviación estadística fuerte',
 'Successful uploads': 'Envíos correctos',
 'Successful uploads since start': 'Envíos correctos desde el inicio',
 'Suitable for most trend analysis': 'Adecuado para la mayoría de análisis de tendencias',
 'Summary': 'Resumen',
 'Sun': 'Dom',
 'Sunday': 'Domingo',
 'Supervisor API access is unavailable': 'Supervisor API access is unavailable',
 'Supply voltage [V]': 'Tensión de alimentación [V]',
 'Suspicious CPM value is being verified': 'Suspicious CPM value is being verified',
 'Sustained Radiation Alert': 'Alerta de radiación sostenida',
 'Sustained relative anomaly events': 'Eventos sostenidos de anomalía relativa',
 'Sustained yellow/red relative anomaly events': 'Eventos sostenidos de anomalía relativa amarilla/roja',
 'Temperature': 'Temperatura',
 'Temperature / voltage errors': 'Errores de temperatura / tensión',
 'Temperature Errors Since Start': 'Errores de temperatura desde el inicio',
 'Temperature [°C]': 'Temperatura [°C]',
 'Temperature and voltage relationships': 'Relaciones con temperatura y tensión',
 'Temperature bins (24 h)': 'Intervalos de temperatura (24 h)',
 'Temperature correlation': 'Correlación con la temperatura',
 'Temperature profile is still being formed': 'El perfil de temperatura aún se está formando',
 'Temperature trend': 'Tendencia de temperatura',
 'Temperature-specific background': 'Fondo específico de temperatura',
 'The Supervisor options could not be loaded: {error}': 'The Supervisor options could not be loaded: {error}',
 'The absolute assessment starts after the first measurement.': 'La evaluación absoluta comienza tras la primera '
                                                                'medición.',
 'The absolute level is below the configured warning threshold, but the value is far above the learned local background.': 'El '
                                                                                                                           'nivel '
                                                                                                                           'absoluto '
                                                                                                                           'está '
                                                                                                                           'por '
                                                                                                                           'debajo '
                                                                                                                           'del '
                                                                                                                           'umbral '
                                                                                                                           'de '
                                                                                                                           'advertencia '
                                                                                                                           'configurado, '
                                                                                                                           'pero '
                                                                                                                           'el '
                                                                                                                           'valor '
                                                                                                                           'está '
                                                                                                                           'muy '
                                                                                                                           'por '
                                                                                                                           'encima '
                                                                                                                           'del '
                                                                                                                           'fondo '
                                                                                                                           'local '
                                                                                                                           'aprendido.',
 'The absolute level is currently uncritical, but the local comparison or short-term trend deserves continued observation.': 'El '
                                                                                                                             'nivel '
                                                                                                                             'absoluto '
                                                                                                                             'no '
                                                                                                                             'es '
                                                                                                                             'crítico '
                                                                                                                             'actualmente, '
                                                                                                                             'pero '
                                                                                                                             'la '
                                                                                                                             'comparación '
                                                                                                                             'local '
                                                                                                                             'o '
                                                                                                                             'la '
                                                                                                                             'tendencia '
                                                                                                                             'a '
                                                                                                                             'corto '
                                                                                                                             'plazo '
                                                                                                                             'requiere '
                                                                                                                             'seguir '
                                                                                                                             'observándose.',
 'The absolute level is currently uncritical. More local history is required before anomaly detection becomes reliable.': 'El '
                                                                                                                          'nivel '
                                                                                                                          'absoluto '
                                                                                                                          'no '
                                                                                                                          'es '
                                                                                                                          'crítico '
                                                                                                                          'actualmente. '
                                                                                                                          'Se '
                                                                                                                          'necesita '
                                                                                                                          'más '
                                                                                                                          'historial '
                                                                                                                          'local '
                                                                                                                          'para '
                                                                                                                          'que '
                                                                                                                          'la '
                                                                                                                          'detección '
                                                                                                                          'de '
                                                                                                                          'anomalías '
                                                                                                                          'sea '
                                                                                                                          'fiable.',
 'The add-on is restarting so the new serial assignments become active.': 'The add-on is restarting so the new serial '
                                                                          'assignments become active.',
 'The app combines the recent trend, robust statistics, agreement between connected counters and the learned local background. The result is a statistical aid and does not identify a physical cause.': 'La '
                                                                                                                                                                                                         'aplicación '
                                                                                                                                                                                                         'combina '
                                                                                                                                                                                                         'la '
                                                                                                                                                                                                         'tendencia '
                                                                                                                                                                                                         'reciente, '
                                                                                                                                                                                                         'estadísticas '
                                                                                                                                                                                                         'robustas, '
                                                                                                                                                                                                         'la '
                                                                                                                                                                                                         'concordancia '
                                                                                                                                                                                                         'entre '
                                                                                                                                                                                                         'los '
                                                                                                                                                                                                         'contadores '
                                                                                                                                                                                                         'conectados '
                                                                                                                                                                                                         'y '
                                                                                                                                                                                                         'el '
                                                                                                                                                                                                         'fondo '
                                                                                                                                                                                                         'local '
                                                                                                                                                                                                         'aprendido. '
                                                                                                                                                                                                         'El '
                                                                                                                                                                                                         'resultado '
                                                                                                                                                                                                         'es '
                                                                                                                                                                                                         'una '
                                                                                                                                                                                                         'ayuda '
                                                                                                                                                                                                         'estadística '
                                                                                                                                                                                                         'y '
                                                                                                                                                                                                         'no '
                                                                                                                                                                                                         'identifica '
                                                                                                                                                                                                         'una '
                                                                                                                                                                                                         'causa '
                                                                                                                                                                                                         'física.',
 'The app compares quality-filtered measurements from the same weekday and hour. Robust medians reduce the influence of isolated spikes and regular daily patterns are kept separate from unusual changes.': 'La '
                                                                                                                                                                                                             'aplicación '
                                                                                                                                                                                                             'compara '
                                                                                                                                                                                                             'mediciones '
                                                                                                                                                                                                             'filtradas '
                                                                                                                                                                                                             'por '
                                                                                                                                                                                                             'calidad '
                                                                                                                                                                                                             'del '
                                                                                                                                                                                                             'mismo '
                                                                                                                                                                                                             'día '
                                                                                                                                                                                                             'de '
                                                                                                                                                                                                             'la '
                                                                                                                                                                                                             'semana '
                                                                                                                                                                                                             'y '
                                                                                                                                                                                                             'la '
                                                                                                                                                                                                             'misma '
                                                                                                                                                                                                             'hora. '
                                                                                                                                                                                                             'Las '
                                                                                                                                                                                                             'medianas '
                                                                                                                                                                                                             'robustas '
                                                                                                                                                                                                             'reducen '
                                                                                                                                                                                                             'la '
                                                                                                                                                                                                             'influencia '
                                                                                                                                                                                                             'de '
                                                                                                                                                                                                             'picos '
                                                                                                                                                                                                             'aislados '
                                                                                                                                                                                                             'y '
                                                                                                                                                                                                             'los '
                                                                                                                                                                                                             'patrones '
                                                                                                                                                                                                             'diarios '
                                                                                                                                                                                                             'regulares '
                                                                                                                                                                                                             'se '
                                                                                                                                                                                                             'separan '
                                                                                                                                                                                                             'de '
                                                                                                                                                                                                             'los '
                                                                                                                                                                                                             'cambios '
                                                                                                                                                                                                             'inusuales.',
 'The app compares quality-filtered radiation measurements with available air-pressure data. A statistical relationship can support interpretation, but correlation alone does not prove a cosmic or environmental cause.': 'La '
                                                                                                                                                                                                                            'aplicación '
                                                                                                                                                                                                                            'compara '
                                                                                                                                                                                                                            'las '
                                                                                                                                                                                                                            'mediciones '
                                                                                                                                                                                                                            'de '
                                                                                                                                                                                                                            'radiación '
                                                                                                                                                                                                                            'filtradas '
                                                                                                                                                                                                                            'por '
                                                                                                                                                                                                                            'calidad '
                                                                                                                                                                                                                            'con '
                                                                                                                                                                                                                            'los '
                                                                                                                                                                                                                            'datos '
                                                                                                                                                                                                                            'disponibles '
                                                                                                                                                                                                                            'de '
                                                                                                                                                                                                                            'presión '
                                                                                                                                                                                                                            'atmosférica. '
                                                                                                                                                                                                                            'Una '
                                                                                                                                                                                                                            'relación '
                                                                                                                                                                                                                            'estadística '
                                                                                                                                                                                                                            'puede '
                                                                                                                                                                                                                            'ayudar '
                                                                                                                                                                                                                            'a '
                                                                                                                                                                                                                            'interpretar, '
                                                                                                                                                                                                                            'pero '
                                                                                                                                                                                                                            'la '
                                                                                                                                                                                                                            'correlación '
                                                                                                                                                                                                                            'por '
                                                                                                                                                                                                                            'sí '
                                                                                                                                                                                                                            'sola '
                                                                                                                                                                                                                            'no '
                                                                                                                                                                                                                            'demuestra '
                                                                                                                                                                                                                            'una '
                                                                                                                                                                                                                            'causa '
                                                                                                                                                                                                                            'cósmica '
                                                                                                                                                                                                                            'o '
                                                                                                                                                                                                                            'ambiental.',
 'The comparison uses only quality-filtered, one-to-one paired measurements.': 'La comparación usa solo mediciones '
                                                                               'filtradas por calidad y emparejadas '
                                                                               'una a una.',
 'The configured danger threshold is exceeded.': 'Se ha superado el umbral de peligro configurado.',
 'The connected counters currently agree well': 'Los contadores conectados coinciden bien actualmente',
 'The counters disagree, so a device-specific effect is more likely': 'Los contadores discrepan, por lo que es más '
                                                                      'probable un efecto específico de un dispositivo',
 'The current radiation level is uncritical according to the selected thresholds.': 'El nivel actual de radiación no '
                                                                                    'es crítico según los umbrales '
                                                                                    'seleccionados.',
 'The current value is below the configured warning threshold and within the usual local range.': 'El valor actual '
                                                                                                  'está por debajo del '
                                                                                                  'umbral de '
                                                                                                  'advertencia '
                                                                                                  'configurado y '
                                                                                                  'dentro del rango '
                                                                                                  'local habitual.',
 'The current value is within the configured warning range.': 'El valor actual está dentro del rango de advertencia '
                                                              'configurado.',
 'The deviation is device-specific; the measurement-site profile remains normal': 'La desviación es específica del '
                                                                                  'dispositivo; el perfil del lugar de '
                                                                                  'medición sigue normal',
 'The device baseline is available, but there are not enough recent measurements for a current comparison.': 'La línea '
                                                                                                             'base del '
                                                                                                             'dispositivo '
                                                                                                             'está '
                                                                                                             'disponible, '
                                                                                                             'pero aún '
                                                                                                             'no hay '
                                                                                                             'suficientes '
                                                                                                             'mediciones '
                                                                                                             'recientes '
                                                                                                             'para una '
                                                                                                             'comparación '
                                                                                                             'actual.',
 'The device clock differs from Home Assistant time.': 'The device clock differs from Home Assistant time.',
 'The filtered counters disagree, so a device-specific effect is more likely': 'Los contadores filtrados discrepan, '
                                                                               'por lo que es más probable un efecto '
                                                                               'específico del dispositivo',
 'The learned baseline remains available. More current samples are required before the local comparison can be updated.': 'La '
                                                                                                                          'línea '
                                                                                                                          'base '
                                                                                                                          'aprendida '
                                                                                                                          'sigue '
                                                                                                                          'disponible. '
                                                                                                                          'Se '
                                                                                                                          'necesitan '
                                                                                                                          'más '
                                                                                                                          'muestras '
                                                                                                                          'actuales '
                                                                                                                          'para '
                                                                                                                          'actualizar '
                                                                                                                          'la '
                                                                                                                          'comparación '
                                                                                                                          'local.',
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
 'The local background is still being learned, so no anomaly assessment is available yet.': 'El fondo local aún se '
                                                                                            'está aprendiendo, por lo '
                                                                                            'que todavía no hay una '
                                                                                            'evaluación de anomalías.',
 'The measurement-site baseline is {deviation:+.1f}% above its typical value': 'La línea base del lugar de medición '
                                                                               'está {deviation:+.1f}% por encima de '
                                                                               'su valor típico',
 'The measurement-site profile combines both devices with quality weighting': 'El perfil del lugar de medición combina '
                                                                              'ambos dispositivos con ponderación de '
                                                                              'calidad',
 'The measurement-site profile currently relies on one device': 'El perfil del lugar de medición depende actualmente '
                                                                'de un solo dispositivo',
 'The pressure model cannot prove cosmic radiation and never suppresses radiation warnings.': 'El modelo de presión no '
                                                                                              'puede demostrar '
                                                                                              'radiación cósmica y '
                                                                                              'nunca suprime las '
                                                                                              'alertas de radiación.',
 'The quality-filtered counter comparison currently agrees well': 'La comparación de contadores filtrada por calidad '
                                                                  'coincide bien actualmente',
 'The recent 30-minute robust trend is rising': 'La tendencia robusta de los últimos 30 minutos está subiendo',
 'The recent 30-minute trend is rising': 'La tendencia reciente de 30 minutos está aumentando',
 'The request could not be processed. Check the selected options.': 'No se pudo procesar la solicitud. Comprueba las '
                                                                    'opciones seleccionadas.',
 'The score combines time-window coverage, missing or irregular intervals, duplicate timestamps and optional-sensor coverage. It indicates how strongly the analysis can rely on the stored series.': 'La '
                                                                                                                                                                                                      'puntuación '
                                                                                                                                                                                                      'combina '
                                                                                                                                                                                                      'la '
                                                                                                                                                                                                      'cobertura '
                                                                                                                                                                                                      'de '
                                                                                                                                                                                                      'la '
                                                                                                                                                                                                      'ventana '
                                                                                                                                                                                                      'temporal, '
                                                                                                                                                                                                      'los '
                                                                                                                                                                                                      'intervalos '
                                                                                                                                                                                                      'ausentes '
                                                                                                                                                                                                      'o '
                                                                                                                                                                                                      'irregulares, '
                                                                                                                                                                                                      'las '
                                                                                                                                                                                                      'marcas '
                                                                                                                                                                                                      'de '
                                                                                                                                                                                                      'tiempo '
                                                                                                                                                                                                      'duplicadas '
                                                                                                                                                                                                      'y '
                                                                                                                                                                                                      'la '
                                                                                                                                                                                                      'cobertura '
                                                                                                                                                                                                      'de '
                                                                                                                                                                                                      'sensores '
                                                                                                                                                                                                      'opcionales. '
                                                                                                                                                                                                      'Indica '
                                                                                                                                                                                                      'en '
                                                                                                                                                                                                      'qué '
                                                                                                                                                                                                      'medida '
                                                                                                                                                                                                      'el '
                                                                                                                                                                                                      'análisis '
                                                                                                                                                                                                      'puede '
                                                                                                                                                                                                      'confiar '
                                                                                                                                                                                                      'en '
                                                                                                                                                                                                      'la '
                                                                                                                                                                                                      'serie '
                                                                                                                                                                                                      'almacenada.',
 'The serial connection is unstable.': 'La conexión serie es inestable.',
 'The traffic light and events are relative anomaly indicators, not safety classifications.': 'El semáforo y los '
                                                                                              'eventos son indicadores '
                                                                                              'de anomalía relativa, '
                                                                                              'no clasificaciones de '
                                                                                              'seguridad.',
 'The value is also within the usual range for this location.': 'El valor también está dentro del rango habitual de '
                                                                'esta ubicación.',
 'The values most users need first': 'Los valores que la mayoría de usuarios necesita primero',
 'These are statistical changes. They can indicate a location, geometry or environmental change, but do not identify the cause.': 'Son '
                                                                                                                                  'cambios '
                                                                                                                                  'estadísticos. '
                                                                                                                                  'Pueden '
                                                                                                                                  'indicar '
                                                                                                                                  'un '
                                                                                                                                  'cambio '
                                                                                                                                  'de '
                                                                                                                                  'ubicación, '
                                                                                                                                  'geometría '
                                                                                                                                  'o '
                                                                                                                                  'entorno, '
                                                                                                                                  'pero '
                                                                                                                                  'no '
                                                                                                                                  'identifican '
                                                                                                                                  'la '
                                                                                                                                  'causa.',
 'These values describe the shape of the count distribution. They do not by themselves prove a physical cause or a calibration state.': 'Estos '
                                                                                                                                        'valores '
                                                                                                                                        'describen '
                                                                                                                                        'la '
                                                                                                                                        'forma '
                                                                                                                                        'de '
                                                                                                                                        'la '
                                                                                                                                        'distribución '
                                                                                                                                        'de '
                                                                                                                                        'conteos. '
                                                                                                                                        'Por '
                                                                                                                                        'sí '
                                                                                                                                        'solos '
                                                                                                                                        'no '
                                                                                                                                        'demuestran '
                                                                                                                                        'una '
                                                                                                                                        'causa '
                                                                                                                                        'física '
                                                                                                                                        'ni '
                                                                                                                                        'un '
                                                                                                                                        'estado '
                                                                                                                                        'de '
                                                                                                                                        'calibración.',
 'This analysis detects unusual changes compared with the normal background at this location. It is not a danger classification; an unusual value can still be below the absolute warning threshold.': 'Este '
                                                                                                                                                                                                       'análisis '
                                                                                                                                                                                                       'detecta '
                                                                                                                                                                                                       'cambios '
                                                                                                                                                                                                       'inusuales '
                                                                                                                                                                                                       'respecto '
                                                                                                                                                                                                       'al '
                                                                                                                                                                                                       'fondo '
                                                                                                                                                                                                       'normal '
                                                                                                                                                                                                       'de '
                                                                                                                                                                                                       'esta '
                                                                                                                                                                                                       'ubicación. '
                                                                                                                                                                                                       'No '
                                                                                                                                                                                                       'es '
                                                                                                                                                                                                       'una '
                                                                                                                                                                                                       'clasificación '
                                                                                                                                                                                                       'de '
                                                                                                                                                                                                       'peligro; '
                                                                                                                                                                                                       'un '
                                                                                                                                                                                                       'valor '
                                                                                                                                                                                                       'inusual '
                                                                                                                                                                                                       'puede '
                                                                                                                                                                                                       'seguir '
                                                                                                                                                                                                       'por '
                                                                                                                                                                                                       'debajo '
                                                                                                                                                                                                       'del '
                                                                                                                                                                                                       'umbral '
                                                                                                                                                                                                       'absoluto '
                                                                                                                                                                                                       'de '
                                                                                                                                                                                                       'advertencia.',
 'This cannot be undone. Delete all GMC history?': 'This cannot be undone. Delete all GMC history?',
 'This classification only compares the current measurement with the selected thresholds. It does not compare the value with the usual background at this location.': 'Esta '
                                                                                                                                                                      'clasificación '
                                                                                                                                                                      'solo '
                                                                                                                                                                      'compara '
                                                                                                                                                                      'la '
                                                                                                                                                                      'medición '
                                                                                                                                                                      'actual '
                                                                                                                                                                      'con '
                                                                                                                                                                      'los '
                                                                                                                                                                      'umbrales '
                                                                                                                                                                      'seleccionados. '
                                                                                                                                                                      'No '
                                                                                                                                                                      'la '
                                                                                                                                                                      'compara '
                                                                                                                                                                      'con '
                                                                                                                                                                      'el '
                                                                                                                                                                      'fondo '
                                                                                                                                                                      'habitual '
                                                                                                                                                                      'de '
                                                                                                                                                                      'esta '
                                                                                                                                                                      'ubicación.',
 'This factor is only a relative device comparison and is not an absolute radiation calibration.': 'This factor is '
                                                                                                   'only a relative '
                                                                                                   'device comparison '
                                                                                                   'and is not an '
                                                                                                   'absolute radiation '
                                                                                                   'calibration.',
 'This report is descriptive and is not a radiation-safety classification.': 'Este informe es descriptivo y no '
                                                                             'constituye una clasificación de '
                                                                             'seguridad radiológica.',
 'Thresholds can be changed in the add-on configuration.': 'Los umbrales pueden modificarse en la configuración del '
                                                           'complemento.',
 'Thu': 'Jue',
 'Thursday': 'Jueves',
 'Tilted': 'Tilted',
 'Time series': 'Serie temporal',
 'Time series, Poisson comparison and weekday/hour heatmap': 'Serie temporal, comparación de Poisson y mapa de calor '
                                                             'día/hora',
 'Time-series PNG': 'Serie temporal PNG',
 'Timestamp diagnostics': 'Diagnóstico de marcas de tiempo',
 'Timezone': 'Zona horaria',
 'Today so far bundle': 'Paquete del día hasta ahora',
 'Too few pressure/CPM pairs': 'Muy pocos pares presión/CPM',
 'Too few valid paired measurements for a reliable device comparison': 'Hay muy pocos pares válidos para una '
                                                                       'comparación fiable',
 'Too little or too fragmented for strong conclusions': 'Datos demasiado escasos o fragmentados para conclusiones '
                                                        'sólidas',
 'Trend (30 min)': 'Tendencia (30 min)',
 'Tue': 'Mar',
 'Tuesday': 'Martes',
 'Type DELETE ALL GMC HISTORY to confirm': 'Type DELETE ALL GMC HISTORY to confirm',
 'Type RESTORE to confirm': 'Escriba RESTORE para confirmar',
 'Typical for {weekday} at {hour}:00': 'Típico para {weekday} a las {hour}:00',
 'USB down': 'Vertical, USB abajo',
 'USB left': 'Vertical, USB a la izquierda',
 'USB right': 'Vertical, USB a la derecha',
 'USB up': 'Vertical, USB arriba',
 'UTC timestamp': 'Marca de tiempo UTC',
 'Unavailable': 'No disponible',
 'Unconfirmed values since bridge start': 'Unconfirmed values since bridge start',
 'Uncritical': 'No crítico',
 'Uncritical: below warning threshold': 'No crítico: por debajo del umbral de advertencia',
 'Unknown': 'Desconocido',
 'Unknown GMC': 'Dispositivo GMC desconocido',
 'Unknown report device': 'Dispositivo de informe desconocido',
 'Unknown serial device': 'Unknown serial device',
 'Unstable': 'Inestable',
 'Unsupported report format': 'Formato de informe no compatible',
 'Upload errors': 'Errores de envío',
 'Upload errors since start': 'Errores de envío desde el inicio',
 'Upload failed': 'Error de envío',
 'Upload successful': 'Envío correcto',
 'Uploading': 'Enviando',
 'Upright': 'Upright',
 'Use this as context only and review longer periods before drawing conclusions.': 'Utiliza esto solo como contexto y '
                                                                                   'revisa períodos más largos antes '
                                                                                   'de sacar conclusiones.',
 'Valid measurements': 'Mediciones válidas',
 'Variance / mean': 'Varianza / media',
 'Very close to Poisson-like spread': 'Muy cerca de una dispersión tipo Poisson',
 'Very complete 24 h data window': 'Ventana de datos de 24 h muy completa',
 'Very strong linear relationship': 'Relación lineal muy fuerte',
 'Very weak linear relationship': 'Relación lineal muy débil',
 'Voltage': 'Tensión',
 'Voltage Errors Since Start': 'Errores de tensión desde el inicio',
 'Voltage [V]': 'Tensión [V]',
 'Voltage correlation': 'Correlación con la tensión',
 'Waiting for enough recent measurements': 'Esperando suficientes mediciones recientes',
 'Waiting for first upload': 'Esperando el primer envío',
 'Waiting for recent measurements': 'Esperando mediciones recientes',
 'Waiting for the first accepted measurement': 'Waiting for the first accepted measurement',
 'Warning': 'Advertencia',
 'Warning from {warning} s; critical from {critical} s': 'Advertencia desde {warning} s; crítico desde {critical} s',
 'Warning threshold exceeded': 'Umbral de advertencia superado',
 'Warning thresholds': 'Umbrales de advertencia',
 'Weak linear relationship': 'Relación lineal débil',
 'Weather pressure sources disagree': 'Las fuentes de presión meteorológica no coinciden',
 'Wed': 'Mié',
 'Wednesday': 'Miércoles',
 'Weekday': 'Día de la semana',
 'Weekday/hour heatmap': 'Mapa de calor día/hora',
 'What does the historical trend mean?': '¿Qué significa la tendencia histórica?',
 'What each report preserves and how periods are defined': 'Qué conserva cada informe y cómo se definen los periodos',
 'What should I do?': '¿Qué debo hacer?',
 'What this assessment means': 'Qué significa esta evaluación',
 'Why are Poisson values shown?': '¿Por qué se muestran los valores de Poisson?',
 'Why is this assessment shown?': '¿Por qué se muestra esta evaluación?',
 'Within local background range': 'Dentro del fondo local',
 'Within normal statistical variation': 'Dentro de la variación estadística normal',
 'Within the usual local range': 'Dentro del rango local habitual',
 'Within warning range': 'Dentro del rango de advertencia',
 'Yellow': 'Amarillo',
 'Z-score = (latest CPM − 24 h mean) / 24 h standard deviation.': 'Puntuación Z = (último CPM − media de 24 h) / '
                                                                  'desviación estándar de 24 h.',
 'Z-score formula explanation': 'Puntuación Z = (último CPM − media de 24 h) / desviación estándar de 24 h.',
 'complete and regularly spaced data': 'datos completos y espaciados regularmente',
 'confirmations': 'confirmations',
 'counting uncertainty {value:.2f}%': 'counting uncertainty {value:.2f}%',
 'coverage': 'cobertura',
 'daily values': 'valores diarios',
 'days': 'días',
 'duplicates / clock regressions': 'duplicados / retrocesos del reloj',
 'entity patterns': 'entity patterns',
 'errors': 'errors',
 'estimated signal probability': 'probabilidad estimada de señal',
 'excluded measurements': 'mediciones excluidas',
 'longest gap {value} s': 'intervalo máximo {value} s',
 'measurements': 'measurements',
 'minimum sample coverage': 'cobertura mínima de muestras',
 'n={count} paired samples': 'n={count} pares de mediciones',
 'n={count} · {coverage:.1f}% coverage': 'n={count} · cobertura {coverage:.1f}%',
 'paired samples': 'pares de mediciones',
 'reconnects': 'reconnects',
 'relative to baseline': 'respecto a la línea base',
 'score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s': 'puntuación {score:.1f}/100 · cobertura '
                                                                           '{coverage:.1f}% · intervalo máximo {gap} s',
 'short / long intervals': 'intervalos cortos / largos',
 'since the current bridge start': 'since the current bridge start',
 'temperature coverage {value}%': 'cobertura de temperatura {value}%',
 'unknown': 'desconocido',
 'valid hourly values': 'valores horarios válidos',
 'valid paired samples': 'pares de mediciones válidos',
 'voltage coverage {value}%': 'cobertura de tensión {value}%',
 'write errors since app start': 'write errors since app start',
 '{before:.2f} → {after:.2f} CPM · {sigma:.1f}σ · {hours} h persistent': '{before:.2f} → {after:.2f} CPM · '
                                                                         '{sigma:.1f}σ · {hours} h persistent',
 '{check_type} result cached for {seconds} s · schema v{schema}': 'Resultado de {check_type} almacenado durante '
                                                                  '{seconds} s · esquema v{schema}',
 '{connected} connected · {disconnected} disconnected': '{connected} connected · {disconnected} disconnected',
 '{count} implausible measurements were excluded from the assessment': 'Se excluyeron {count} mediciones no plausibles '
                                                                       'de la evaluación',
 '{count} measurements': '{count} mediciones',
 '{count} measurements and {events} events were removed.': '{count} measurements and {events} events were removed.',
 '{events} events · {diagnostics} diagnostics': '{events} events · {diagnostics} diagnostics',
 '{gyro_note} History retention: {days} days. Daily periods are local calendar days; weekly periods are ISO weeks from Monday through Sunday.': '{gyro_note} '
                                                                                                                                                'Conservación '
                                                                                                                                                'del '
                                                                                                                                                'historial: '
                                                                                                                                                '{days} '
                                                                                                                                                'días. '
                                                                                                                                                'Los '
                                                                                                                                                'periodos '
                                                                                                                                                'diarios '
                                                                                                                                                'son '
                                                                                                                                                'días '
                                                                                                                                                'naturales '
                                                                                                                                                'locales; '
                                                                                                                                                'los '
                                                                                                                                                'semanales '
                                                                                                                                                'son '
                                                                                                                                                'semanas '
                                                                                                                                                'ISO '
                                                                                                                                                'de '
                                                                                                                                                'lunes '
                                                                                                                                                'a '
                                                                                                                                                'domingo.',
 '{model} — Radiation monitoring report': '{model} — Informe de monitorización de radiación',
 '{seconds} seconds ago': '{seconds} seconds ago',
 '{value:g} h': '{value:g} h',
 '{value:g} min': '{value:g} min',
 '{value} clock regressions observed': '{value} retrocesos del reloj observados',
 '{value} duplicate timestamps observed': '{value} marcas de tiempo duplicadas observadas',
 '{value} long intervals': '{value} intervalos largos',
 '{value} unusually short intervals': '{value} intervalos inusualmente cortos',
 '{value} vs local baseline': '{value} respecto a la línea base local',
 '{value}% time-window coverage': 'cobertura temporal {value}%'}

# Runtime presentation templates added in 7.1.4.
CATALOG.update({
    'Comparison confidence: {confidence}': 'Confianza de la comparación: {confidence}',
    'Confidence: {confidence}': 'Confianza: {confidence}',
    'Status': 'Estado',
    'Typical background': 'Fondo típico',
    'Valid paired samples': 'Pares de mediciones válidos',
    'Warning from {warning:g} s; critical from {critical:g} s': 'Advertencia desde {warning:g} s; crítico desde {critical:g} s',
    'valid hourly values · {days:.1f} days · {span:.1f} hPa': 'valores horarios válidos · {days:.1f} días · {span:.1f} hPa',
    '{a:+.1f}% / {b:+.1f}%': '{a:+.1f}% / {b:+.1f}%',
    '{b} × factor → {a}': '{b} × factor → {a}',
    '{content}': '{content}',
    '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)': '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)',
    '{days} days': '{days} días',
    '{dose:.3f} µSv/h': '{dose:.3f} µSv/h',
    '{first} {second}': '{first} {second}',
    '{from_value} → {to_value}': '{from_value} → {to_value}',
    '{note} · n={samples}': '{note} · n={samples}',
    '{pairs} valid paired samples': '{pairs} pares de mediciones válidos',
    '{pairs} valid paired samples · counting uncertainty {value:.2f}%': '{pairs} pares de mediciones válidos · incertidumbre de conteo {value:.2f}%',
    '{probability:.0f}% estimated signal probability': '{probability:.0f} % de probabilidad estimada de señal',
    '{span:.0f} {days_label} · {count} {daily_label}': '{span:.0f} {days_label} · {count} {daily_label}',
    '{start}–{end} °C · {samples} Samples': '{start}–{end} °C · {samples} mediciones',
    '{trend:+.1f} CPM': '{trend:+.1f} CPM',
    '{value:g} µSv/h': '{value:g} µSv/h',
    'Last uploaded CPM': 'Último CPM enviado',
    'Last uploaded ACPM': 'Último ACPM enviado',
    'GMCMap last uploaded ACPM': 'Último ACPM enviado a GMCMap',
    'GMCMap ACPM accepted samples': 'Muestras aceptadas para el ACPM de GMCMap',
    'ACPM is the average of all accepted CPM readings since the current app measurement session began.': 'El ACPM es el promedio de todas las lecturas CPM aceptadas desde el inicio de la sesión de medición actual de la aplicación.',
    'User manual': 'Manual de usuario',
    'Open user manual PDF': 'Abrir el manual de usuario en PDF',
    'User manual is not available': 'El manual de usuario no está disponible',
})

# Version 8.2.1 report and history labels.
CATALOG.update({
    'Accepted measurements [count]': 'Mediciones aceptadas [cantidad]',
    'Local hour [h]': 'Hora local [h]',
    'Mean count rate [CPM]': 'Tasa de conteo media [CPM]',
    'Radiation Monitoring': 'Monitorización de radiación',
    'Rejected raw value': 'Valor bruto descartado',
})


# Version 8.2.1 complete runtime localization.
CATALOG.update({
    'The recent level differs from counting noise with {probability:.2f}% statistical confidence': 'El nivel reciente difiere del ruido de conteo con una confianza estadística del {probability:.2f} %',
    'A comparable or more extreme hourly level occurred about once in {rarity:.1f} historical hours': 'Un nivel horario comparable o más extremo se produjo aproximadamente una vez cada {rarity:.1f} horas históricas',
})

# Long-term analysis 9.1.1
CATALOG.update({'24 hours': '24 horas', '30 days': '30 días', '365 days': '365 días', '7 days': '7 días', '7-day rolling median': 'Mediana móvil de 7 días', '90 days': '90 días', '95% block-bootstrap interval for mean': 'Intervalo bootstrap por bloques del 95 % para la media', '95% block-bootstrap interval for median': 'Intervalo bootstrap por bloques del 95 % para la mediana', 'Air-pressure association': 'Asociación con la presión atmosférica', 'Annual projection from the last 30 days: {value} µSv': 'Proyección anual a partir de los últimos 30 días: {value} µSv', 'Annual projection is not shown until a sufficiently complete 30-day period exists.': 'La proyección anual no se muestra hasta disponer de un período de 30 días suficientemente completo.', 'Based on {hours} covered hours': 'Basado en {hours} horas cubiertas', 'Bootstrap uncertainty, distribution dispersion, EWMA and CUSUM': 'Incertidumbre bootstrap, dispersión, EWMA y CUSUM', 'Calendar heat map': 'Mapa de calor del calendario', 'Calendar heat map of daily median CPM': 'Mapa de calor de las medianas CPM diarias', 'Connected periods above the robust local long-term threshold': 'Períodos continuos por encima del umbral local robusto a largo plazo', 'Contextual Fano-like ratio; rolling CPM values are not independent Poisson counts': 'Relación contextual tipo Fano; los valores CPM móviles no son conteos de Poisson independientes', 'Correlation does not prove causation.': 'La correlación no demuestra causalidad.', 'Coverage {coverage}% · at least {required}% required': 'Cobertura {coverage} % · se requiere al menos {required} %', 'Covered hours': 'Horas cubiertas', 'Cumulative derived dose': 'Dosis acumulada derivada', 'Daily and monthly development': 'Evolución diaria y mensual', 'Daily median': 'Mediana diaria', 'Daily median and 7-day rolling median': 'Mediana diaria y mediana móvil de 7 días', 'Daily medians, rolling median and calendar view': 'Medianas diarias, mediana móvil y vista de calendario', 'Derived cumulative dose: {dose} µSv': 'Dosis acumulada derivada: {dose} µSv', 'Derived dose (µSv)': 'Dosis derivada (µSv)', 'Derived from the robust local background; not an official alarm threshold': 'Derivado del fondo local robusto; no es un umbral oficial de alarma', 'Duration (h)': 'Duración (h)', 'EWMA, CUSUM, trend tests and relative event detection provide statistical context only. They do not identify a radiation source and do not replace calibrated radiation-protection measurements.': 'EWMA, CUSUM, las pruebas de tendencia y la detección relativa solo aportan contexto estadístico. No identifican una fuente ni sustituyen mediciones calibradas de protección radiológica.', 'Effective sample size': 'Tamaño efectivo de la muestra', 'Environmental correlations are exploratory. They may reflect common time patterns, ventilation, weather or other confounding factors and do not prove causation.': 'Las correlaciones ambientales son exploratorias. Pueden reflejar patrones temporales comunes, ventilación, meteorología u otros factores y no demuestran causalidad.', 'Excess area (CPM·h)': 'Área de exceso (CPM·h)', 'Exploratory Spearman correlations at 0, 3, 6, 12 and 24 hour lags': 'Correlaciones de Spearman exploratorias con retardos de 0, 3, 6, 12 y 24 horas', 'Higher': 'Más alto', 'Hourly dispersion ratio': 'Relación de dispersión horaria', 'Lagged environmental associations': 'Asociaciones ambientales retardadas', 'Long-term analysis': 'Análisis a largo plazo', 'Long-term analysis for {device}': 'Análisis a largo plazo para {device}', 'Long-term background, cumulative dose, trend, recurring patterns and statistical process diagnostics': 'Fondo a largo plazo, dosis acumulada, tendencia, patrones recurrentes y diagnóstico estadístico del proceso', 'Long-term overview': 'Resumen a largo plazo', 'Long-term statistical diagnostics': 'Diagnóstico estadístico a largo plazo', 'Long-term trend': 'Tendencia a largo plazo', 'Lower': 'Más bajo', 'Mann-Kendall test with Sen slope on sufficiently covered daily medians': 'Prueba de Mann-Kendall con pendiente de Sen sobre medianas diarias con cobertura suficiente', 'Maximum CPM': 'CPM máximo', 'Mean CPM': 'CPM medio', 'Median CPM': 'CPM mediano', 'Median {median} CPM · coverage {coverage}%': 'Mediana {median} CPM · cobertura {coverage} %', 'Month': 'Mes', 'Monthly aggregates': 'Agregados mensuales', 'Moving blocks preserve short-range time dependence': 'Los bloques móviles conservan la dependencia temporal de corto alcance', 'No calendar data available': 'No hay datos de calendario', 'No long-term analysis available yet': 'Todavía no hay análisis a largo plazo', 'No monthly aggregates available': 'No hay agregados mensuales', 'No persistent CUSUM signal detected': 'No se detectó una señal CUSUM persistente', 'No persistent EWMA signal detected': 'No se detectó una señal EWMA persistente', 'No persistent relative elevation episodes detected': 'No se detectaron episodios relativos persistentes', 'No supported dose conversion for this period': 'No hay una conversión de dosis compatible para este período', 'No value is calculated until enough hourly pairs are available.': 'No se calcula ningún valor hasta disponer de suficientes pares horarios.', 'Not enough daily values for a long-term chart': 'No hay suficientes valores diarios para un gráfico a largo plazo', 'Not enough paired data': 'No hay suficientes datos emparejados', 'Not yet meaningful': 'Aún no es significativo', 'Only {covered} of {required} days covered': 'Solo {covered} de {required} días cubiertos', 'Persistent elevation episodes': 'Episodios de elevación persistente', 'Persistent episodes': 'Episodios persistentes', 'Preliminary': 'Preliminar', 'Ready': 'Evaluable', 'Real time windows with duration and coverage checks': 'Ventanas temporales reales con comprobación de duración y cobertura', 'Recent 7-day median relative to the robust long-term background': 'Mediana reciente de 7 días respecto al fondo robusto a largo plazo', 'Recent background deviation': 'Desviación reciente del fondo', 'Relative event threshold': 'Umbral relativo de evento', 'Robust local background': 'Fondo local robusto', 'Scientific interpretation': 'Interpretación científica', 'Start': 'Inicio', 'Statistical signal detected': 'Señal estadística detectada', 'Stored measurements are required before long-term statistics can be calculated.': 'Se requieren mediciones almacenadas antes de calcular estadísticas a largo plazo.', 'Strongest at {lag} h lag · {pairs} pairs · {strength} association': 'Asociación más fuerte con {lag} h de retardo · {pairs} pares · asociación {strength}', 'Temperature association': 'Asociación con la temperatura', 'The detector uses the robust long-term local background and does not replace radiation-safety alarms.': 'La detección utiliza el fondo local robusto a largo plazo y no sustituye las alarmas de protección radiológica.', 'Time at or above configured danger threshold': 'Tiempo en o por encima del umbral de peligro configurado', 'Time in configured warning range': 'Tiempo en el rango de advertencia configurado', 'Typical range P05–P95: {low}–{high} CPM': 'Rango típico P05-P95: {low}-{high} CPM', 'moderate': 'moderada', 'strong': 'fuerte', 'weak': 'débil', '{date}: median {median} CPM, coverage {coverage}%': '{date}: mediana {median} CPM, cobertura {coverage} %', '{direction} · {slope} CPM/day · p={p}': '{direction} · {slope} CPM/día · p={p}', '{hours} covered hours': '{hours} horas cubiertas', '{hours} total elevated hours · longest {longest} h': '{hours} horas elevadas en total · máxima {longest} h', '{observed} daily observations · correlation duration {duration} days': '{observed} observaciones diarias · duración de correlación {duration} días', '{replicates} replicates · block length {block} days': '{replicates} réplicas · longitud de bloque {block} días', 'Long-term': 'Largo plazo', 'stable': 'estable', 'increasing': 'creciente', 'decreasing': 'decreciente'})

# Recent baseline wording 9.1.1
CATALOG.update({'Recent baseline context': 'Contexto reciente de la línea base', 'Seven-day baseline deviation, drift and sustained relative events': 'Desviación de la línea base de 7 días, deriva y eventos relativos persistentes'})


# Extended agreement and seasonal analysis 9.1.1
CATALOG.update({'Bland-Altman bias': 'Sesgo de Bland-Altman', '95% limits of agreement': 'Límites de concordancia del 95 %', 'Mean signed difference A minus B': 'Diferencia media con signo A menos B', 'Exploratory paired-device agreement; correlation alone does not establish agreement.': 'Concordancia exploratoria entre dispositivos emparejados; la correlación por sí sola no demuestra concordancia.', 'Seasonal month-of-year profile': 'Perfil estacional por mes del año', 'Median CPM by calendar month across available years': 'Mediana de CPM por mes calendario en los años disponibles', 'Calendar month': 'Mes calendario', 'Days represented': 'Días representados', 'Not enough months for a seasonal profile': 'No hay suficientes meses para un perfil estacional', 'At least six represented calendar months are required.': 'Se requieren al menos seis meses calendario representados.', 'Exploratory seasonal summary; it does not separate weather, location, detector or calibration changes.': 'Resumen estacional exploratorio; no separa cambios meteorológicos, de ubicación, detector o calibración.'})


# Evidence-based long-term presentation and field-test diagnostics 9.3.0
CATALOG.update({'Not evaluable': 'No evaluable', 'Exploratory': 'Exploratorio', 'Supported': 'Respaldado', 'Well supported': 'Muy bien respaldado', 'Very small practical magnitude': 'Magnitud práctica muy pequeña', 'Small practical magnitude': 'Magnitud práctica pequeña', 'Moderate practical magnitude': 'Magnitud práctica moderada', 'Large practical magnitude': 'Magnitud práctica grande', 'Practical magnitude not available': 'Magnitud práctica no disponible', 'No reliable long-term trend can be assessed yet': 'Aún no puede evaluarse una tendencia fiable a largo plazo', 'At least 30 sufficiently complete days and an adequate effective sample size are required.': 'Se requieren al menos 30 días suficientemente completos y un tamaño de muestra efectivo adecuado.', 'A rising long-term tendency is visible': 'Se observa una tendencia ascendente a largo plazo', 'A falling long-term tendency is visible': 'Se observa una tendencia descendente a largo plazo', 'No statistically clear long-term trend is visible': 'No se observa una tendencia clara a largo plazo', 'Estimated change {value}% per month · {magnitude}': 'Cambio estimado {value}% al mes · {magnitude}', 'Runtime since service start': 'Tiempo de ejecución desde el inicio del servicio', 'Cumulative counters reset when the service restarts.': 'Los contadores acumulados se reinician al reiniciar el servicio.', 'USB / serial recovery': 'Recuperación USB/serie', '{errors} serial errors · {reconnects} reconnects': '{errors} errores serie · {reconnects} reconexiones', 'Longest data gap': 'Mayor laguna de datos', '{count} detected gaps above the expected interval': '{count} lagunas detectadas por encima del intervalo esperado', 'Database write errors': 'Errores de escritura de la base de datos', 'Stored samples: {count}': 'Muestras almacenadas: {count}', 'GMCMap transmission': 'Transmisión GMCMap', '{success} successful · {errors} failed uploads': '{success} correctas · {errors} fallidas', 'Export field-test protocol (JSON)': 'Exportar protocolo de prueba de campo (JSON)', 'Field-test interpretation': 'Interpretación de la prueba de campo', 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.': 'Estos contadores ayudan a evaluar la fiabilidad a largo plazo. No certifican la calibración ni la exactitud.', '{available} of {required} required hourly pairs are available.': 'Hay {available} de {required} pares horarios requeridos.', 'FDR-adjusted p={value}': 'p ajustado por FDR={value}', 'FDR-adjusted significance not available': 'Significación ajustada por FDR no disponible', 'Plain-language assessment': 'Resumen comprensible', 'The main result first; method details remain available below.': 'Primero el resultado principal; los detalles metodológicos siguen disponibles.', 'Current background context': 'Contexto de fondo actual', 'Data basis': 'Base de datos', '{days} covered days · {observed} daily observations': '{days} días cubiertos · {observed} observaciones diarias', 'Integrated derived dose in the measured period': 'Dosis derivada integrada en el periodo medido', 'Seasonal assessment': 'Evaluación estacional', '{months} represented calendar months': '{months} meses calendario representados', 'Extended statistical methods': 'Métodos estadísticos ampliados', 'Confidence intervals, effective sample size, test statistics and practical effect size': 'Intervalos de confianza, tamaño efectivo, pruebas y efecto práctico', 'Trend method details': 'Detalles del método de tendencia', 'Statistical process diagnostics': 'Diagnóstico estadístico del proceso', 'EWMA, CUSUM and dispersion diagnostics; statistical context only': 'Diagnóstico EWMA, CUSUM y dispersión; solo contexto estadístico', 'Exploratory Spearman correlations with false-discovery-rate correction': 'Correlaciones exploratorias de Spearman con corrección FDR', 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.': 'Las correlaciones ambientales son exploratorias. La corrección de Benjamini-Hochberg reduce falsos hallazgos, pero no permite conclusiones causales.', 'Long-term reliability field test': 'Prueba de fiabilidad a largo plazo', 'Operational counters for USB, database continuity and GMCMap transmission': 'Contadores de USB, continuidad de base de datos y transmisión GMCMap', 'Annual projection from the last 90 days: {value} µSv': 'Proyección anual a partir de los últimos 90 días: {value} µSv', 'Annual projection is not shown until a sufficiently complete 90-day period exists.': 'La proyección anual no se muestra hasta disponer de 90 días suficientemente completos.'})


# Sidebar navigation and responsive application shell 9.3.0
CATALOG.update({'Main navigation': 'Navegación principal', 'Monitoring': 'Supervisión', 'Evaluation': 'Evaluación', 'Documentation': 'Documentación', 'Administration': 'Administración', 'Close navigation': 'Cerrar navegación', 'Skip to content': 'Saltar al contenido', 'Menu': 'Menú', 'Refresh': 'Actualizar'})

# Global view control and long-term interpretation context 9.4.0
CATALOG.update({'Choose how many details and tools are shown across all sections. The selection is stored in this browser.': 'Determina cuántos detalles y herramientas se muestran en todas las secciones. La selección se guarda en este navegador.', 'Long-term interpretation context': 'Contexto de interpretación a largo plazo', 'Intelligent analysis, adaptive background and cosmic-influence context for the selected detector.': 'Análisis inteligente, fondo adaptativo y contexto estadístico de la influencia cósmica para el detector seleccionado.'})
