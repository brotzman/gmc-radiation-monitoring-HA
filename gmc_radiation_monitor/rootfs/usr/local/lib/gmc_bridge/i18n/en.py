from __future__ import annotations

CATALOG: dict[str, str] = {'1 h counting uncertainty': '1 h counting uncertainty',
 '1 h coverage': '1 h coverage',
 '1 h mean': '1 h mean',
 '1 h mean / 7 d mean × 100': '1 h mean / 7 d mean × 100',
 '1 h mean dose rate': '1 h mean dose rate',
 '1 h mean minus 7 d baseline': '1 h mean minus 7 d baseline',
 '24 h Fano factor': '24 h Fano factor',
 '24 h P95': '24 h P95',
 '24 h P99': '24 h P99',
 '24 h Z-score': '24 h Z-score',
 '24 h counting uncertainty': '24 h counting uncertainty',
 '24 h distribution, percentiles and latest-value deviation': '24 h distribution, percentiles and latest-value '
                                                              'deviation',
 '24 h maximum': '24 h maximum',
 '24 h mean': '24 h mean',
 '24 h mean dose rate': '24 h mean dose rate',
 '24 h median': '24 h median',
 '24 h minimum': '24 h minimum',
 '24 h standard deviation': '24 h standard deviation',
 '50th percentile': '50th percentile',
 '7 d baseline': '7 d baseline',
 '7 d baseline dose rate': '7 d baseline dose rate',
 '7 d baseline drift': '7 d baseline drift',
 '7 d counting uncertainty': '7 d counting uncertainty',
 '7-day smoothed daily median': '7-day smoothed daily median',
 '95th percentile': '95th percentile',
 '99th percentile': '99th percentile',
 'A device function is temporarily unavailable.': 'A device function is temporarily unavailable.',
 'A fresh backup is recommended before deletion.': 'A fresh backup is recommended before deletion.',
 'A recent position change can affect comparability': 'A recent position change can affect comparability',
 'Above the typical time profile': 'Above the typical time profile',
 'Above the usual local range': 'Above the usual local range',
 'Absolute radiation assessment': 'Absolute radiation assessment',
 'Absolute thresholds and local anomaly detection answer different questions.': 'Absolute thresholds and local '
                                                                                'anomaly detection answer different '
                                                                                'questions.',
 'Acceleration magnitude': 'Acceleration magnitude',
 'Acceleration raw values': 'Acceleration raw values',
 'Accepted device values are stored separately after live CPM plausibility confirmation': 'Accepted device values '
                                                                                          'are stored separately '
                                                                                          'after live CPM '
                                                                                          'plausibility confirmation',
 'Active threshold profile': 'Active threshold profile',
 'Adaptive background profile': 'Adaptive background profile',
 'Advanced': 'Advanced',
 'Advanced diagnostics': 'Advanced diagnostics',
 'Advanced visuals': 'Advanced visuals',
 'Affected GMC devices': 'Affected GMC devices',
 'Agreement': 'Agreement',
 'Air-pressure source': 'Air-pressure source',
 'Air-pressure trend': 'Air-pressure trend',
 'All GMC history was deleted': 'All GMC history was deleted',
 'All baselines and comparisons use the same robust quality-filtered measurements.': 'All baselines and comparisons '
                                                                                     'use the same robust '
                                                                                     'quality-filtered measurements.',
 'All connected GMC devices': 'All connected GMC devices',
 'All devices': 'All devices',
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
 'All statistical values, confidence intervals and diagnostics': 'All statistical values, confidence intervals and '
                                                                 'diagnostics',
 'All {count} known GMC devices are connected': 'All {count} known GMC devices are connected',
 'Allow restore': 'Allow restore',
 'Already assigned to {name}': 'Already assigned to {name}',
 'Analysis': 'Analysis',
 'Analysis JSON': 'Analysis JSON',
 'Analysis PDF': 'Analysis PDF',
 'Analysis depth': 'Analysis depth',
 'Analysis for': 'Analysis for',
 'Analysis is still being prepared': 'Analysis is still being prepared',
 'Analysis shown': 'Analysis shown',
 'Analysis, the traffic light and downloads will become meaningful after the first stored samples arrive.': 'Analysis, '
                                                                                                            'the '
                                                                                                            'traffic '
                                                                                                            'light '
                                                                                                            'and '
                                                                                                            'downloads '
                                                                                                            'will '
                                                                                                            'become '
                                                                                                            'meaningful '
                                                                                                            'after '
                                                                                                            'the '
                                                                                                            'first '
                                                                                                            'stored '
                                                                                                            'samples '
                                                                                                            'arrive.',
 'Analyze this device': 'Analyze this device',
 'Another report is already being generated': 'Another report is already being generated',
 'Another report or maintenance job is running': 'Another report or maintenance job is running',
 'Another report or restore job is running': 'Another report or restore job is running',
 'Another report, maintenance export, or restore job is running': 'Another report, maintenance export, or restore '
                                                                  'job is running',
 'App Started At': 'App Started At',
 'Apply': 'Apply',
 'Assessment': 'Assessment',
 'Assigned': 'Assigned',
 'At least 24 h reference and 6 h persistence are required': 'At least 24 h reference and 6 h persistence are '
                                                             'required',
 'At least two daily background values are required.': 'At least two daily background values are required.',
 'At least {count} valid hourly values are required': 'At least {count} valid hourly values are required',
 'At least {count} valid pairs are required': 'At least {count} valid pairs are required',
 'At least {days} days of learning data are required': 'At least {days} days of learning data are required',
 'At least {span:g} hPa pressure variation is required': 'At least {span:g} hPa pressure variation is required',
 'At the same time, the value is clearly above the usual local background. Review the trend and measurement conditions.': 'At '
                                                                                                                          'the '
                                                                                                                          'same '
                                                                                                                          'time, '
                                                                                                                          'the '
                                                                                                                          'value '
                                                                                                                          'is '
                                                                                                                          'clearly '
                                                                                                                          'above '
                                                                                                                          'the '
                                                                                                                          'usual '
                                                                                                                          'local '
                                                                                                                          'background. '
                                                                                                                          'Review '
                                                                                                                          'the '
                                                                                                                          'trend '
                                                                                                                          'and '
                                                                                                                          'measurement '
                                                                                                                          'conditions.',
 'Automatic device detection is running': 'Automatic device detection is running',
 'Automatic refresh is temporarily unavailable': 'Automatic refresh is temporarily unavailable',
 'Availability': 'Availability',
 'Available': 'Available',
 'Back to analysis': 'Back to analysis',
 'Background index': 'Background index',
 'Background index compares the rolling 1 h mean with the available 7 d baseline.': 'Background index compares the '
                                                                                    'rolling 1 h mean with the '
                                                                                    'available 7 d baseline.',
 'Background index formula explanation': 'Background index formula explanation',
 'Background trend over days and months': 'Background trend over days and months',
 'Backup is compatible and ready to restore.': 'Backup is compatible and ready to restore.',
 'Backup preview failed': 'Backup preview failed',
 'Baseline available': 'Baseline available',
 'Baseline currently stable': 'Baseline currently stable',
 'Baseline deviation': 'Baseline deviation',
 'Baseline deviation, drift and sustained relative events': 'Baseline deviation, drift and sustained relative events',
 'Baseline deviation: {cpm} CPM ({percent}%)': 'Baseline deviation: {cpm} CPM ({percent}%)',
 'Baseline drift: {value}%': 'Baseline drift: {value}%',
 'Baseline learning in progress': 'Baseline learning in progress',
 'Baseline readiness': 'Baseline readiness',
 'Baseline: {value} CPM': 'Baseline: {value} CPM',
 'Battery voltage': 'Battery voltage',
 'Baud rate': 'Baud rate',
 'Below the typical time profile': 'Below the typical time profile',
 'Below warning threshold': 'Below warning threshold',
 'BfS and ICRP reference profiles convert annual dose values into continuous-rate equivalents for context. They are not official instantaneous alarm limits and cannot replace professional dose assessment.': 'BfS '
                                                                                                                                                                                                               'and '
                                                                                                                                                                                                               'ICRP '
                                                                                                                                                                                                               'reference '
                                                                                                                                                                                                               'profiles '
                                                                                                                                                                                                               'convert '
                                                                                                                                                                                                               'annual '
                                                                                                                                                                                                               'dose '
                                                                                                                                                                                                               'values '
                                                                                                                                                                                                               'into '
                                                                                                                                                                                                               'continuous-rate '
                                                                                                                                                                                                               'equivalents '
                                                                                                                                                                                                               'for '
                                                                                                                                                                                                               'context. '
                                                                                                                                                                                                               'They '
                                                                                                                                                                                                               'are '
                                                                                                                                                                                                               'not '
                                                                                                                                                                                                               'official '
                                                                                                                                                                                                               'instantaneous '
                                                                                                                                                                                                               'alarm '
                                                                                                                                                                                                               'limits '
                                                                                                                                                                                                               'and '
                                                                                                                                                                                                               'cannot '
                                                                                                                                                                                                               'replace '
                                                                                                                                                                                                               'professional '
                                                                                                                                                                                                               'dose '
                                                                                                                                                                                                               'assessment.',
 'BfS reference projection': 'BfS reference projection',
 'Both connected counters show a quality-filtered simultaneous rise': 'Both connected counters show a '
                                                                      'quality-filtered simultaneous rise',
 'Both connected counters show a simultaneous rise': 'Both connected counters show a simultaneous rise',
 'Broadly compatible with Poisson-like spread': 'Broadly compatible with Poisson-like spread',
 'CPM': 'CPM',
 'CPM and derived dose rate': 'CPM and derived dose rate',
 'CPM distribution and Poisson comparison': 'CPM distribution and Poisson comparison',
 'CPM distribution — {title}': 'CPM distribution — {title}',
 'CPM is the primary measurement.': 'CPM is the primary measurement.',
 'CPM per µSv/h': 'CPM per µSv/h',
 'CPM quality': 'CPM quality',
 'CPM statistics  min {minimum:.0f} | max {maximum:.0f} | mean {mean:.2f} | median {median:.2f} | SD {sd:.2f} | P95 {p95:.2f} | missing {missing}': 'CPM '
                                                                                                                                                    'statistics  '
                                                                                                                                                    'min '
                                                                                                                                                    '{minimum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'max '
                                                                                                                                                    '{maximum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'mean '
                                                                                                                                                    '{mean:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'median '
                                                                                                                                                    '{median:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'SD '
                                                                                                                                                    '{sd:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'P95 '
                                                                                                                                                    '{p95:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'missing '
                                                                                                                                                    '{missing}',
 'CPM statistics: no accepted measurements in selected period': 'CPM statistics: no accepted measurements in '
                                                                'selected period',
 'CPM–pressure correlation': 'CPM–pressure correlation',
 'CPM–temperature correlation': 'CPM–temperature correlation',
 'CPM–voltage correlation': 'CPM–voltage correlation',
 'CSV files preserve every accepted measurement without interpolation. PNG reports include CPM, temperature, voltage, optional raw signed gyro diagnostics, summary statistics, sample completeness, device identity, timezone, period and generation time. ZIP bundles additionally contain analysis JSON, daily summaries, events, histogram, heatmap and a multi-page PDF report.': 'CSV '
                                                                                                                                                                                                                                                                                                                                                                                       'files '
                                                                                                                                                                                                                                                                                                                                                                                       'preserve '
                                                                                                                                                                                                                                                                                                                                                                                       'every '
                                                                                                                                                                                                                                                                                                                                                                                       'accepted '
                                                                                                                                                                                                                                                                                                                                                                                       'measurement '
                                                                                                                                                                                                                                                                                                                                                                                       'without '
                                                                                                                                                                                                                                                                                                                                                                                       'interpolation. '
                                                                                                                                                                                                                                                                                                                                                                                       'PNG '
                                                                                                                                                                                                                                                                                                                                                                                       'reports '
                                                                                                                                                                                                                                                                                                                                                                                       'include '
                                                                                                                                                                                                                                                                                                                                                                                       'CPM, '
                                                                                                                                                                                                                                                                                                                                                                                       'temperature, '
                                                                                                                                                                                                                                                                                                                                                                                       'voltage, '
                                                                                                                                                                                                                                                                                                                                                                                       'optional '
                                                                                                                                                                                                                                                                                                                                                                                       'raw '
                                                                                                                                                                                                                                                                                                                                                                                       'signed '
                                                                                                                                                                                                                                                                                                                                                                                       'gyro '
                                                                                                                                                                                                                                                                                                                                                                                       'diagnostics, '
                                                                                                                                                                                                                                                                                                                                                                                       'summary '
                                                                                                                                                                                                                                                                                                                                                                                       'statistics, '
                                                                                                                                                                                                                                                                                                                                                                                       'sample '
                                                                                                                                                                                                                                                                                                                                                                                       'completeness, '
                                                                                                                                                                                                                                                                                                                                                                                       'device '
                                                                                                                                                                                                                                                                                                                                                                                       'identity, '
                                                                                                                                                                                                                                                                                                                                                                                       'timezone, '
                                                                                                                                                                                                                                                                                                                                                                                       'period '
                                                                                                                                                                                                                                                                                                                                                                                       'and '
                                                                                                                                                                                                                                                                                                                                                                                       'generation '
                                                                                                                                                                                                                                                                                                                                                                                       'time. '
                                                                                                                                                                                                                                                                                                                                                                                       'ZIP '
                                                                                                                                                                                                                                                                                                                                                                                       'bundles '
                                                                                                                                                                                                                                                                                                                                                                                       'additionally '
                                                                                                                                                                                                                                                                                                                                                                                       'contain '
                                                                                                                                                                                                                                                                                                                                                                                       'analysis '
                                                                                                                                                                                                                                                                                                                                                                                       'JSON, '
                                                                                                                                                                                                                                                                                                                                                                                       'daily '
                                                                                                                                                                                                                                                                                                                                                                                       'summaries, '
                                                                                                                                                                                                                                                                                                                                                                                       'events, '
                                                                                                                                                                                                                                                                                                                                                                                       'histogram, '
                                                                                                                                                                                                                                                                                                                                                                                       'heatmap '
                                                                                                                                                                                                                                                                                                                                                                                       'and '
                                                                                                                                                                                                                                                                                                                                                                                       'a '
                                                                                                                                                                                                                                                                                                                                                                                       'multi-page '
                                                                                                                                                                                                                                                                                                                                                                                       'PDF '
                                                                                                                                                                                                                                                                                                                                                                                       'report.',
 'Calibrated acceleration': 'Calibrated acceleration',
 'Calibration profile': 'Calibration profile',
 'Capabilities': 'Capabilities',
 'Check location, orientation and environmental conditions when a persistent jump appears.': 'Check location, '
                                                                                             'orientation and '
                                                                                             'environmental '
                                                                                             'conditions when a '
                                                                                             'persistent jump '
                                                                                             'appears.',
 'Check manually': 'Check manually',
 'Check the Home Assistant general settings and restart the add-on.': 'Check the Home Assistant general settings and '
                                                                      'restart the add-on.',
 'Check the USB cable and power supply if this continues for more than 15 minutes.': 'Check the USB cable and power '
                                                                                     'supply if this continues for '
                                                                                     'more than 15 minutes.',
 'Check the measurement conditions, observe the trend and verify the reading with an appropriate instrument if it persists.': 'Check '
                                                                                                                              'the '
                                                                                                                              'measurement '
                                                                                                                              'conditions, '
                                                                                                                              'observe '
                                                                                                                              'the '
                                                                                                                              'trend '
                                                                                                                              'and '
                                                                                                                              'verify '
                                                                                                                              'the '
                                                                                                                              'reading '
                                                                                                                              'with '
                                                                                                                              'an '
                                                                                                                              'appropriate '
                                                                                                                              'instrument '
                                                                                                                              'if '
                                                                                                                              'it '
                                                                                                                              'persists.',
 'Check the measurement location': 'Check the measurement location',
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
 'Choose how much detail the analysis cards show. The selection is stored in this browser.': 'Choose how much detail '
                                                                                             'the analysis cards '
                                                                                             'show. The selection is '
                                                                                             'stored in this '
                                                                                             'browser.',
 'Choose whether reports include all devices or one selected device.': 'Choose whether reports include all devices '
                                                                       'or one selected device.',
 'Clear': 'Clear',
 'Clearly above the usual local range': 'Clearly above the usual local range',
 'Clearly elevated': 'Clearly elevated',
 'Clearly elevated: clearly above the usual local range': 'Clearly elevated: clearly above the usual local range',
 'Clock offset exceeds warning threshold': 'Clock offset exceeds warning threshold',
 'Clock synchronized': 'Clock synchronized',
 'Close to Poisson expectation': 'Close to Poisson expectation',
 'Co-location and equal geometry must be ensured by the user': 'Co-location and equal geometry must be ensured by '
                                                               'the user',
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
 'Compared with local baseline': 'Compared with local baseline',
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
 'Compares the current value with the usual background at this location.': 'Compares the current value with the '
                                                                           'usual background at this location.',
 'Comparison confidence': 'Comparison confidence',
 'Complete ZIP bundle': 'Complete ZIP bundle',
 'Complete history deletion failed': 'Complete history deletion failed',
 'Complete history deletion is disabled in the app configuration.': 'Complete history deletion is disabled in the '
                                                                    'app configuration.',
 'Completeness: {value:.2f}%': 'Completeness: {value:.2f}%',
 'Confidence': 'Confidence',
 'Configured CPM conversion factor': 'Configured CPM conversion factor',
 'Configured baud rate': 'Configured baud rate',
 'Configured device name': 'Configured device name',
 'Configured location': 'Configured location',
 'Configured measurement interval': 'Configured measurement interval',
 'Confirmed original samples in 24 h · {accepted} stored': 'Confirmed original samples in 24 h · {accepted} stored',
 'Connect two devices to enable comparison.': 'Connect two devices to enable comparison.',
 'Connect two devices to learn a relative response factor.': 'Connect two devices to learn a relative response '
                                                             'factor.',
 'Connected GMC devices': 'Connected GMC devices',
 'Connected counters without an active stability warning': 'Connected counters without an active stability warning',
 'Connected devices': 'Connected devices',
 'Connection active': 'Connection active',
 'Consecutive upload errors': 'Consecutive upload errors',
 'Continue observing': 'Continue observing',
 'Coordinates': 'Coordinates',
 'Correlation': 'Correlation',
 'Correlation does not imply causation. Strong values should be investigated over longer periods before drawing conclusions.': 'Correlation '
                                                                                                                               'does '
                                                                                                                               'not '
                                                                                                                               'imply '
                                                                                                                               'causation. '
                                                                                                                               'Strong '
                                                                                                                               'values '
                                                                                                                               'should '
                                                                                                                               'be '
                                                                                                                               'investigated '
                                                                                                                               'over '
                                                                                                                               'longer '
                                                                                                                               'periods '
                                                                                                                               'before '
                                                                                                                               'drawing '
                                                                                                                               'conclusions.',
 'Cosmic influence is possible': 'Cosmic influence is possible',
 'Cosmic influence – statistical indication': 'Cosmic influence – statistical indication',
 'Counter ID': 'Counter ID',
 'Counting statistics': 'Counting statistics',
 'Counting uncertainty (68%): −{minus:.2f}/+{plus:.2f} CPM · {impulses} impulses in {duration}': 'Counting '
                                                                                                 'uncertainty (68%): '
                                                                                                 '−{minus:.2f}/+{plus:.2f} '
                                                                                                 'CPM · {impulses} '
                                                                                                 'impulses in '
                                                                                                 '{duration}',
 'Counting uncertainty not available': 'Counting uncertainty not available',
 'Country': 'Country',
 'Coverage percent': 'Coverage percent',
 'Coverage, gaps, runtime counters and derived dose-rate values': 'Coverage, gaps, runtime counters and derived '
                                                                  'dose-rate values',
 'Critical': 'Critical',
 'Critical: danger threshold exceeded': 'Critical: danger threshold exceeded',
 'Current': 'Current',
 'Current air pressure': 'Current air pressure',
 'Current database size': 'Current database size',
 'Current difference': 'Current difference',
 'Current value': 'Current value',
 'Current value is {z:+.2f} robust standard deviations from the 24 h median': 'Current value is {z:+.2f} robust '
                                                                              'standard deviations from the 24 h '
                                                                              'median',
 'Current value is {z:+.2f} standard deviations from the 24 h mean': 'Current value is {z:+.2f} standard deviations '
                                                                     'from the 24 h mean',
 'Current week bundle': 'Current week bundle',
 'Currently selected': 'Currently selected',
 'Custom period': 'Custom period',
 'Custom thresholds': 'Custom thresholds',
 'Daily and weekly profile is still being formed': 'Daily and weekly profile is still being formed',
 'Daily quality-filtered medians are smoothed over seven days. The period cards compare the recent part of each period with the preceding part; detected jumps are statistical changes and do not determine their cause.': 'Daily '
                                                                                                                                                                                                                           'quality-filtered '
                                                                                                                                                                                                                           'medians '
                                                                                                                                                                                                                           'are '
                                                                                                                                                                                                                           'smoothed '
                                                                                                                                                                                                                           'over '
                                                                                                                                                                                                                           'seven '
                                                                                                                                                                                                                           'days. '
                                                                                                                                                                                                                           'The '
                                                                                                                                                                                                                           'period '
                                                                                                                                                                                                                           'cards '
                                                                                                                                                                                                                           'compare '
                                                                                                                                                                                                                           'the '
                                                                                                                                                                                                                           'recent '
                                                                                                                                                                                                                           'part '
                                                                                                                                                                                                                           'of '
                                                                                                                                                                                                                           'each '
                                                                                                                                                                                                                           'period '
                                                                                                                                                                                                                           'with '
                                                                                                                                                                                                                           'the '
                                                                                                                                                                                                                           'preceding '
                                                                                                                                                                                                                           'part; '
                                                                                                                                                                                                                           'detected '
                                                                                                                                                                                                                           'jumps '
                                                                                                                                                                                                                           'are '
                                                                                                                                                                                                                           'statistical '
                                                                                                                                                                                                                           'changes '
                                                                                                                                                                                                                           'and '
                                                                                                                                                                                                                           'do '
                                                                                                                                                                                                                           'not '
                                                                                                                                                                                                                           'determine '
                                                                                                                                                                                                                           'their '
                                                                                                                                                                                                                           'cause.',
 'Daily summary CSV': 'Daily summary CSV',
 'Danger threshold exceeded': 'Danger threshold exceeded',
 'Danger thresholds': 'Danger thresholds',
 'Danger zone': 'Danger zone',
 'Dashboard navigation': 'Dashboard navigation',
 'Data exports': 'Data exports',
 'Data period': 'Data period',
 'Data quality': 'Data quality',
 'Data quality is too low for a reliable assessment': 'Data quality is too low for a reliable assessment',
 'Data quality status unavailable': 'Data quality status unavailable',
 'Data quality: {value}': 'Data quality: {value}',
 'Database': 'Database',
 'Database health': 'Database health',
 'Database size': 'Database size',
 'Date': 'Date',
 'Delete all GMC history': 'Delete all GMC history',
 'Delete history': 'Delete history',
 'Deletion confirmation text must be exactly DELETE ALL GMC HISTORY': 'Deletion confirmation text must be exactly '
                                                                      'DELETE ALL GMC HISTORY',
 'Deletion is disabled by default.': 'Deletion is disabled by default.',
 'Derived dose rate': 'Derived dose rate',
 'Derived from 1 h mean CPM': 'Derived from 1 h mean CPM',
 'Derived from 24 h mean CPM': 'Derived from 24 h mean CPM',
 'Derived from 7 d mean CPM': 'Derived from 7 d mean CPM',
 'Derived from latest CPM': 'Derived from latest CPM',
 'Detailed interpretation and the most useful supporting values': 'Detailed interpretation and the most useful '
                                                                  'supporting values',
 'Detect, identify and assign GMC counters': 'Detect, identify and assign GMC counters',
 'Detected': 'Detected',
 'Detected Capabilities': 'Detected Capabilities',
 'Detected GMC device': 'Detected GMC device',
 'Detected baseline jumps': 'Detected baseline jumps',
 'Detected relative anomaly events: {count}': 'Detected relative anomaly events: {count}',
 'Deviation': 'Deviation',
 'Device': 'Device',
 'Device Profile': 'Device Profile',
 'Device Time Errors Since Start': 'Device Time Errors Since Start',
 'Device assignments saved': 'Device assignments saved',
 'Device assignments were saved.': 'Device assignments were saved.',
 'Device baseline': 'Device baseline',
 'Device capabilities': 'Device capabilities',
 'Device clock': 'Device clock',
 'Device clock offset': 'Device clock offset',
 'Device clock status': 'Device clock status',
 'Device clock unavailable': 'Device clock unavailable',
 'Device clock warning': 'Device clock warning',
 'Device comparison': 'Device comparison',
 'Device details, live values and analysis selection are shown below.': 'Device details, live values and analysis '
                                                                        'selection are shown below.',
 'Device health warning': 'Device health warning',
 'Device position': 'Device position',
 'Device status updated': 'Device status updated',
 'Device temperature is unavailable.': 'Device temperature is unavailable.',
 'Device time': 'Device time',
 'Device-specific details are listed above.': 'Device-specific details are listed above.',
 'Device: {value}': 'Device: {value}',
 'Devices': 'Devices',
 'Diagnostics JSON': 'Diagnostics JSON',
 'Disabled': 'Disabled',
 'Discarded CPM peaks': 'Discarded CPM peaks',
 'Discarded unconfirmed CPM peaks': 'Discarded unconfirmed CPM peaks',
 'Display down': 'Display down',
 'Display up': 'Display up',
 'Dose rate = CPM / configured conversion factor ({factor:g} CPM per µSv/h).': 'Dose rate = CPM / configured '
                                                                               'conversion factor ({factor:g} CPM '
                                                                               'per µSv/h).',
 'Dose rate formula explanation': 'Dose rate formula explanation',
 'Dose-rate values are derived from CPM using the configured conversion factor.': 'Dose-rate values are derived from '
                                                                                  'CPM using the configured '
                                                                                  'conversion factor.',
 'Dose-rate values, traffic-light states and events are derived indicators. CPM remains the primary measurement.': 'Dose-rate '
                                                                                                                   'values, '
                                                                                                                   'traffic-light '
                                                                                                                   'states '
                                                                                                                   'and '
                                                                                                                   'events '
                                                                                                                   'are '
                                                                                                                   'derived '
                                                                                                                   'indicators. '
                                                                                                                   'CPM '
                                                                                                                   'remains '
                                                                                                                   'the '
                                                                                                                   'primary '
                                                                                                                   'measurement.',
 'Download': 'Download',
 'Downloads': 'Downloads',
 'Dual-tube measurement': 'Dual-tube measurement',
 'Duration [s]': 'Duration [s]',
 'During the learning phase, leave the counters in a stable location and allow additional measurements to accumulate.': 'During '
                                                                                                                        'the '
                                                                                                                        'learning '
                                                                                                                        'phase, '
                                                                                                                        'leave '
                                                                                                                        'the '
                                                                                                                        'counters '
                                                                                                                        'in '
                                                                                                                        'a '
                                                                                                                        'stable '
                                                                                                                        'location '
                                                                                                                        'and '
                                                                                                                        'allow '
                                                                                                                        'additional '
                                                                                                                        'measurements '
                                                                                                                        'to '
                                                                                                                        'accumulate.',
 'Each device has its own MQTT identity and history. The cards show the latest accepted measurement.': 'Each device '
                                                                                                       'has its own '
                                                                                                       'MQTT '
                                                                                                       'identity and '
                                                                                                       'history. The '
                                                                                                       'cards show '
                                                                                                       'the latest '
                                                                                                       'accepted '
                                                                                                       'measurement.',
 'Each physical serial device can only be assigned once': 'Each physical serial device can only be assigned once',
 'Elevated': 'Elevated',
 'Elevated relative background': 'Elevated relative background',
 'Elevated: within warning range': 'Elevated: within warning range',
 'Elevation': 'Elevation',
 'Enable complete history deletion in the app configuration and restart only when deletion is planned.': 'Enable '
                                                                                                         'complete '
                                                                                                         'history '
                                                                                                         'deletion '
                                                                                                         'in the app '
                                                                                                         'configuration '
                                                                                                         'and '
                                                                                                         'restart '
                                                                                                         'only when '
                                                                                                         'deletion '
                                                                                                         'is '
                                                                                                         'planned.',
 'Enable enable_restore in the app configuration and restart only when a restore is planned.': 'Enable '
                                                                                               'enable_restore in '
                                                                                               'the app '
                                                                                               'configuration and '
                                                                                               'restart only when a '
                                                                                               'restore is planned.',
 'Enable “{setting}” in the app configuration and restart only when a restore is planned.': 'Enable “{setting}” in '
                                                                                            'the app configuration '
                                                                                            'and restart only when a '
                                                                                            'restore is planned.',
 'End time UTC': 'End time UTC',
 'End time local': 'End time local',
 'Entities': 'Entities',
 'Environment': 'Environment',
 'Error time': 'Error time',
 'Estimated pressure influence': 'Estimated pressure influence',
 'Evaluated by': 'Evaluated by',
 'Evaluates the current value using the configured thresholds.': 'Evaluates the current value using the configured '
                                                                 'thresholds.',
 'Events CSV': 'Events CSV',
 'Events and diagnostics': 'Events and diagnostics',
 'Events last 24 h': 'Events last 24 h',
 'Excellent': 'Excellent',
 'Excluded measurements': 'Excluded measurements',
 'Excluded pairs': 'Excluded pairs',
 'Expand all': 'Expand all',
 'Expected samples': 'Expected samples',
 'Expert view': 'Expert view',
 'Explanation of the two assessments': 'Explanation of the two assessments',
 'Export details': 'Export details',
 'Extremely elevated': 'Extremely elevated',
 'Extremely elevated: far above the usual local range': 'Extremely elevated: far above the usual local range',
 'Falling': 'Falling',
 'Falling air pressure can slightly increase the share of cosmically generated secondary radiation at ground level, while rising air pressure tends to reduce it; the model detects only such statistical relationships and cannot clearly distinguish them from other natural influences.': 'Falling '
                                                                                                                                                                                                                                                                                             'air '
                                                                                                                                                                                                                                                                                             'pressure '
                                                                                                                                                                                                                                                                                             'can '
                                                                                                                                                                                                                                                                                             'slightly '
                                                                                                                                                                                                                                                                                             'increase '
                                                                                                                                                                                                                                                                                             'the '
                                                                                                                                                                                                                                                                                             'share '
                                                                                                                                                                                                                                                                                             'of '
                                                                                                                                                                                                                                                                                             'cosmically '
                                                                                                                                                                                                                                                                                             'generated '
                                                                                                                                                                                                                                                                                             'secondary '
                                                                                                                                                                                                                                                                                             'radiation '
                                                                                                                                                                                                                                                                                             'at '
                                                                                                                                                                                                                                                                                             'ground '
                                                                                                                                                                                                                                                                                             'level, '
                                                                                                                                                                                                                                                                                             'while '
                                                                                                                                                                                                                                                                                             'rising '
                                                                                                                                                                                                                                                                                             'air '
                                                                                                                                                                                                                                                                                             'pressure '
                                                                                                                                                                                                                                                                                             'tends '
                                                                                                                                                                                                                                                                                             'to '
                                                                                                                                                                                                                                                                                             'reduce '
                                                                                                                                                                                                                                                                                             'it; '
                                                                                                                                                                                                                                                                                             'the '
                                                                                                                                                                                                                                                                                             'model '
                                                                                                                                                                                                                                                                                             'detects '
                                                                                                                                                                                                                                                                                             'only '
                                                                                                                                                                                                                                                                                             'such '
                                                                                                                                                                                                                                                                                             'statistical '
                                                                                                                                                                                                                                                                                             'relationships '
                                                                                                                                                                                                                                                                                             'and '
                                                                                                                                                                                                                                                                                             'cannot '
                                                                                                                                                                                                                                                                                             'clearly '
                                                                                                                                                                                                                                                                                             'distinguish '
                                                                                                                                                                                                                                                                                             'them '
                                                                                                                                                                                                                                                                                             'from '
                                                                                                                                                                                                                                                                                             'other '
                                                                                                                                                                                                                                                                                             'natural '
                                                                                                                                                                                                                                                                                             'influences.',
 'Falling air pressure is often associated with a slightly higher intensity of cosmically generated secondary radiation at ground level, while rising air pressure is associated with a slightly lower intensity. The strength of this relationship depends on detector, location and atmosphere; the cause cannot be determined unambiguously from total counts.': 'Falling '
                                                                                                                                                                                                                                                                                                                                                                    'air '
                                                                                                                                                                                                                                                                                                                                                                    'pressure '
                                                                                                                                                                                                                                                                                                                                                                    'is '
                                                                                                                                                                                                                                                                                                                                                                    'often '
                                                                                                                                                                                                                                                                                                                                                                    'associated '
                                                                                                                                                                                                                                                                                                                                                                    'with '
                                                                                                                                                                                                                                                                                                                                                                    'a '
                                                                                                                                                                                                                                                                                                                                                                    'slightly '
                                                                                                                                                                                                                                                                                                                                                                    'higher '
                                                                                                                                                                                                                                                                                                                                                                    'intensity '
                                                                                                                                                                                                                                                                                                                                                                    'of '
                                                                                                                                                                                                                                                                                                                                                                    'cosmically '
                                                                                                                                                                                                                                                                                                                                                                    'generated '
                                                                                                                                                                                                                                                                                                                                                                    'secondary '
                                                                                                                                                                                                                                                                                                                                                                    'radiation '
                                                                                                                                                                                                                                                                                                                                                                    'at '
                                                                                                                                                                                                                                                                                                                                                                    'ground '
                                                                                                                                                                                                                                                                                                                                                                    'level, '
                                                                                                                                                                                                                                                                                                                                                                    'while '
                                                                                                                                                                                                                                                                                                                                                                    'rising '
                                                                                                                                                                                                                                                                                                                                                                    'air '
                                                                                                                                                                                                                                                                                                                                                                    'pressure '
                                                                                                                                                                                                                                                                                                                                                                    'is '
                                                                                                                                                                                                                                                                                                                                                                    'associated '
                                                                                                                                                                                                                                                                                                                                                                    'with '
                                                                                                                                                                                                                                                                                                                                                                    'a '
                                                                                                                                                                                                                                                                                                                                                                    'slightly '
                                                                                                                                                                                                                                                                                                                                                                    'lower '
                                                                                                                                                                                                                                                                                                                                                                    'intensity. '
                                                                                                                                                                                                                                                                                                                                                                    'The '
                                                                                                                                                                                                                                                                                                                                                                    'strength '
                                                                                                                                                                                                                                                                                                                                                                    'of '
                                                                                                                                                                                                                                                                                                                                                                    'this '
                                                                                                                                                                                                                                                                                                                                                                    'relationship '
                                                                                                                                                                                                                                                                                                                                                                    'depends '
                                                                                                                                                                                                                                                                                                                                                                    'on '
                                                                                                                                                                                                                                                                                                                                                                    'detector, '
                                                                                                                                                                                                                                                                                                                                                                    'location '
                                                                                                                                                                                                                                                                                                                                                                    'and '
                                                                                                                                                                                                                                                                                                                                                                    'atmosphere; '
                                                                                                                                                                                                                                                                                                                                                                    'the '
                                                                                                                                                                                                                                                                                                                                                                    'cause '
                                                                                                                                                                                                                                                                                                                                                                    'cannot '
                                                                                                                                                                                                                                                                                                                                                                    'be '
                                                                                                                                                                                                                                                                                                                                                                    'determined '
                                                                                                                                                                                                                                                                                                                                                                    'unambiguously '
                                                                                                                                                                                                                                                                                                                                                                    'from '
                                                                                                                                                                                                                                                                                                                                                                    'total '
                                                                                                                                                                                                                                                                                                                                                                    'counts.',
 'Fano factor': 'Fano factor',
 'Fano factor = variance / mean; a value near 1 is consistent with Poisson-like counting statistics.': 'Fano factor '
                                                                                                       '= variance / '
                                                                                                       'mean; a '
                                                                                                       'value near 1 '
                                                                                                       'is '
                                                                                                       'consistent '
                                                                                                       'with '
                                                                                                       'Poisson-like '
                                                                                                       'counting '
                                                                                                       'statistics.',
 'Fano factor formula explanation': 'Fano factor formula explanation',
 'Fano factor: {value}': 'Fano factor: {value}',
 'Far above the usual local range': 'Far above the usual local range',
 'File size': 'File size',
 'Firmware version': 'Firmware version',
 'Flat': 'Flat',
 'Fleet intelligence': 'Fleet intelligence',
 'Format': 'Format',
 'Fri': 'Fri',
 'Friday': 'Friday',
 'Full history ZIP': 'Full history ZIP',
 'GMC Radiation Monitor': 'GMC Radiation Monitor',
 'GMC Radiation Monitoring': 'GMC Radiation Monitoring',
 'GMC Reports': 'GMC Reports',
 'GMC analysis report {period}': 'GMC analysis report {period}',
 'GMC detected': 'GMC detected',
 'GMC devices are being detected automatically': 'GMC devices are being detected automatically',
 'GMC radiation analysis report': 'GMC radiation analysis report',
 'GMC radiation monitoring report {period}': 'GMC radiation monitoring report {period}',
 'GMC-300/320 family': 'GMC-300/320 family',
 'GMC-320 and GMC-500+ combined': 'GMC-320 and GMC-500+ combined',
 'GMC-500 family': 'GMC-500 family',
 'GMC-600 family': 'GMC-600 family',
 'GMCMap consecutive upload errors': 'GMCMap consecutive upload errors',
 'GMCMap counter ID': 'GMCMap counter ID',
 'GMCMap is enabled, but this device has no counter ID mapping.': 'GMCMap is enabled, but this device has no counter '
                                                                  'ID mapping.',
 'GMCMap last HTTP status': 'GMCMap last HTTP status',
 'GMCMap last error time': 'GMCMap last error time',
 'GMCMap last server response': 'GMCMap last server response',
 'GMCMap last successful upload': 'GMCMap last successful upload',
 'GMCMap last upload attempt': 'GMCMap last upload attempt',
 'GMCMap last upload error': 'GMCMap last upload error',
 'GMCMap last uploaded CPM': 'GMCMap last uploaded CPM',
 'GMCMap next upload': 'GMCMap next upload',
 'GMCMap successful uploads since start': 'GMCMap successful uploads since start',
 'GMCMap upload errors since start': 'GMCMap upload errors since start',
 'GMCMap upload status': 'GMCMap upload status',
 'GQ manufacturer recommendation': 'GQ manufacturer recommendation',
 'Gaps are excluded from effective counting time': 'Gaps are excluded from effective counting time',
 'Generated export exceeds the {limit_mib} MiB safety limit': 'Generated export exceeds the {limit_mib} MiB safety '
                                                              'limit',
 'Generated maintenance export exceeds the 128 MiB safety limit': 'Generated maintenance export exceeds the 128 MiB '
                                                                  'safety limit',
 'Generated report exceeds the 64 MiB safety limit': 'Generated report exceeds the 64 MiB safety limit',
 'Generic GQ GMC / RFC1201-compatible device': 'Generic GQ GMC / RFC1201-compatible device',
 'Generic RFC1201-compatible device': 'Generic RFC1201-compatible device',
 'Global report settings': 'Global report settings',
 'Good': 'Good',
 'Green': 'Green',
 'Gyro Calibrated {axis}': 'Gyro Calibrated {axis}',
 'Gyro Errors Since Start': 'Gyro Errors Since Start',
 'Gyro Raw {axis}': 'Gyro Raw {axis}',
 'Gyro X': 'Gyro X',
 'Gyro Y': 'Gyro Y',
 'Gyro Z': 'Gyro Z',
 'Gyro data will be included when available.': 'Gyro data will be included when available.',
 'Gyro errors': 'Gyro errors',
 'Gyro recording is disabled.': 'Gyro recording is disabled.',
 'Gyroscope': 'Gyroscope',
 'Hardware model': 'Hardware model',
 'Heartbeat Errors Since Start': 'Heartbeat Errors Since Start',
 'Heartbeat mode': 'Heartbeat mode',
 'Heartbeat rolling 60 s CPM': 'Heartbeat rolling 60 s CPM',
 'Heatmap PNG': 'Heatmap PNG',
 'Heuristic statistical assessment; not a radiation-protection classification.': 'Heuristic statistical assessment; '
                                                                                 'not a radiation-protection '
                                                                                 'classification.',
 'High': 'High',
 'High relative increase': 'High relative increase',
 'High-dose Tube CPM': 'High-dose Tube CPM',
 'High-dose tube': 'High-dose tube',
 'Highest stored 24 h value': 'Highest stored 24 h value',
 'Histogram PNG': 'Histogram PNG',
 'Historical chart is still being formed': 'Historical chart is still being formed',
 'Historical development': 'Historical development',
 'History': 'History',
 'History Write Errors Since Start': 'History Write Errors Since Start',
 'History deleted': 'History deleted',
 'History maintenance': 'History maintenance',
 'History restore failed': 'History restore failed',
 'History restore is disabled. Enable enable_restore in the app configuration and restart.': 'History restore is '
                                                                                             'disabled. Enable '
                                                                                             'enable_restore in the '
                                                                                             'app configuration and '
                                                                                             'restart.',
 'History restore is disabled. Enable “{setting}” in the app configuration and restart.': 'History restore is '
                                                                                          'disabled. Enable '
                                                                                          '“{setting}” in the app '
                                                                                          'configuration and '
                                                                                          'restart.',
 'History storage warning': 'History storage warning',
 'Home Assistant API client is not configured': 'Home Assistant API client is not configured',
 'Home Assistant Recorder entity patterns': 'Home Assistant Recorder entity patterns',
 'Home Assistant Recorder history cleared': 'Home Assistant Recorder history cleared',
 'Home Assistant host UART': 'Home Assistant host UART',
 'Home Assistant location': 'Home Assistant location',
 'How are connected counters compared?': 'How are connected counters compared?',
 'How closely the observed spread resembles Poisson-like counting': 'How closely the observed spread resembles '
                                                                    'Poisson-like counting',
 'How is data quality evaluated?': 'How is data quality evaluated?',
 'How is the background profile calculated?': 'How is the background profile calculated?',
 'How is the pressure relationship assessed?': 'How is the pressure relationship assessed?',
 'However, the value is noticeably above the usual local background. Observe the trend.': 'However, the value is '
                                                                                          'noticeably above the '
                                                                                          'usual local background. '
                                                                                          'Observe the trend.',
 'ICRP reference projection': 'ICRP reference projection',
 'Inclination': 'Inclination',
 'Ingest diagnostics cleared': 'Ingest diagnostics cleared',
 'Inspecting backup…': 'Inspecting backup…',
 'Insufficient': 'Insufficient',
 'Insufficient history for level-shift detection': 'Insufficient history for level-shift detection',
 'Insufficient paired daily values': 'Insufficient paired daily values',
 'Integrity': 'Integrity',
 'Intelligence': 'Intelligence',
 'Intelligent radiation analysis': 'Intelligent radiation analysis',
 'Internal database cleared': 'Internal database cleared',
 'Internal serial port': 'Internal serial port',
 'Interpret statistics with coverage in mind': 'Interpret statistics with coverage in mind',
 'Interpret these values together with coverage, device stability and the historical background.': 'Interpret these '
                                                                                                   'values together '
                                                                                                   'with coverage, '
                                                                                                   'device stability '
                                                                                                   'and the '
                                                                                                   'historical '
                                                                                                   'background.',
 'Interpretation': 'Interpretation',
 'Interval diagnostics': 'Interval diagnostics',
 'Invalid deletion confirmation': 'Invalid deletion confirmation',
 'Invalid device clock response': 'Invalid device clock response',
 'Invalid request parameters': 'Invalid request parameters',
 'Invalid serial configuration request': 'Invalid serial configuration request',
 'Keep both counters close together and similarly oriented when using the comparison as a reference.': 'Keep both '
                                                                                                       'counters '
                                                                                                       'close '
                                                                                                       'together and '
                                                                                                       'similarly '
                                                                                                       'oriented '
                                                                                                       'when using '
                                                                                                       'the '
                                                                                                       'comparison '
                                                                                                       'as a '
                                                                                                       'reference.',
 'Known radio or Zigbee adapter': 'Known radio or Zigbee adapter',
 'Language': 'Language',
 'Last HTTP status': 'Last HTTP status',
 'Last Successful Measurement': 'Last Successful Measurement',
 'Last attempt': 'Last attempt',
 'Last backup requested in this browser': 'Last backup requested in this browser',
 'Last sample age': 'Last sample age',
 'Last server response': 'Last server response',
 'Last successful storage': 'Last successful storage',
 'Last update': 'Last update',
 'Last upload': 'Last upload',
 'Last upload error': 'Last upload error',
 'Latest CPM': 'Latest CPM',
 'Latest CPM uncertainty': 'Latest CPM uncertainty',
 'Latest CPM vs 24 h distribution': 'Latest CPM vs 24 h distribution',
 'Latest accepted value': 'Latest accepted value',
 'Latest dose rate': 'Latest dose rate',
 'Latest measurement': 'Latest measurement',
 'Learned Radiation Baseline': 'Learned Radiation Baseline',
 'Learned from local history': 'Learned from local history',
 'Learned pressure coefficient': 'Learned pressure coefficient',
 'Learning baseline': 'Learning baseline',
 'Learning basis': 'Learning basis',
 'Learning progress': 'Learning progress',
 'Learning: not enough local history yet': 'Learning: not enough local history yet',
 'Learning: {pairs}/{minimum} pairs · {days:.1f}/{minimum_days:g} days': 'Learning: {pairs}/{minimum} pairs · '
                                                                         '{days:.1f}/{minimum_days:g} days',
 'Learns typical values for the current hour, weekday and temperature range and shows long-term drift.': 'Learns '
                                                                                                         'typical '
                                                                                                         'values for '
                                                                                                         'the '
                                                                                                         'current '
                                                                                                         'hour, '
                                                                                                         'weekday '
                                                                                                         'and '
                                                                                                         'temperature '
                                                                                                         'range and '
                                                                                                         'shows '
                                                                                                         'long-term '
                                                                                                         'drift.',
 'Less variable than Poisson expectation': 'Less variable than Poisson expectation',
 'Likely device-specific deviation': 'Likely device-specific deviation',
 'Limited': 'Limited',
 'Live radiation CPS': 'Live radiation CPS',
 'Live system status': 'Live system status',
 'Local background analysis': 'Local background analysis',
 'Local background is still being learned': 'Local background is still being learned',
 'Local background model is available': 'Local background model is available',
 'Local baseline': 'Local baseline',
 'Local hour': 'Local hour',
 'Local time [{timezone}]': 'Local time [{timezone}]',
 'Local timestamp': 'Local timestamp',
 'Location data comes from the Home Assistant general settings and is not sent to an external geocoding service.': 'Location '
                                                                                                                   'data '
                                                                                                                   'comes '
                                                                                                                   'from '
                                                                                                                   'the '
                                                                                                                   'Home '
                                                                                                                   'Assistant '
                                                                                                                   'general '
                                                                                                                   'settings '
                                                                                                                   'and '
                                                                                                                   'is '
                                                                                                                   'not '
                                                                                                                   'sent '
                                                                                                                   'to '
                                                                                                                   'an '
                                                                                                                   'external '
                                                                                                                   'geocoding '
                                                                                                                   'service.',
 'Location unavailable': 'Location unavailable',
 'Long-term context': 'Long-term context',
 'Long-term drift': 'Long-term drift',
 'Long-term relative factor available': 'Long-term relative factor available',
 'Long-term relative response': 'Long-term relative response',
 'Longest gap': 'Longest gap',
 'Longest gap [s]': 'Longest gap [s]',
 'Longest gap: {seconds} s': 'Longest gap: {seconds} s',
 'Low': 'Low',
 'Low-dose Tube CPM': 'Low-dose Tube CPM',
 'Low-dose tube': 'Low-dose tube',
 'Lowest stored 24 h value': 'Lowest stored 24 h value',
 'Machine-readable statistics and event data': 'Machine-readable statistics and event data',
 'Maximum': 'Maximum',
 'Maximum CPM': 'Maximum CPM',
 'Maximum background index [%]': 'Maximum background index [%]',
 'Mean': 'Mean',
 'Mean CPM': 'Mean CPM',
 'Mean CPM by weekday and hour — {title}': 'Mean CPM by weekday and hour — {title}',
 'Mean absolute difference': 'Mean absolute difference',
 'Mean: {value} CPM': 'Mean: {value} CPM',
 'Measurement interval': 'Measurement interval',
 'Measurement-site baseline': 'Measurement-site baseline',
 'Measurements': 'Measurements',
 'Measurements are sent to the public GMCMap service.': 'Measurements are sent to the public GMCMap service.',
 'Measurements to delete': 'Measurements to delete',
 'Median': 'Median',
 'Median CPM': 'Median CPM',
 'Median: {value} CPM': 'Median: {value} CPM',
 'Medium': 'Medium',
 'Merge a compatible SQLite backup into the current history. Existing rows are preserved or updated by device serial and UTC timestamp.': 'Merge '
                                                                                                                                          'a '
                                                                                                                                          'compatible '
                                                                                                                                          'SQLite '
                                                                                                                                          'backup '
                                                                                                                                          'into '
                                                                                                                                          'the '
                                                                                                                                          'current '
                                                                                                                                          'history. '
                                                                                                                                          'Existing '
                                                                                                                                          'rows '
                                                                                                                                          'are '
                                                                                                                                          'preserved '
                                                                                                                                          'or '
                                                                                                                                          'updated '
                                                                                                                                          'by '
                                                                                                                                          'device '
                                                                                                                                          'serial '
                                                                                                                                          'and '
                                                                                                                                          'UTC '
                                                                                                                                          'timestamp.',
 'Merged {rows} measurement rows from schema {schema}.': 'Merged {rows} measurement rows from schema {schema}.',
 'Minimum / maximum: {minimum} / {maximum} CPM': 'Minimum / maximum: {minimum} / {maximum} CPM',
 'Minimum CPM': 'Minimum CPM',
 'Mixed device profiles': 'Mixed device profiles',
 'Moderate linear relationship': 'Moderate linear relationship',
 'Mon': 'Mon',
 'Monday': 'Monday',
 'More history is needed before the relative background indicator is classified.': 'More history is needed before '
                                                                                   'the relative background '
                                                                                   'indicator is classified.',
 'More history is needed; approximately {count} additional measurements are required.': 'More history is needed; '
                                                                                        'approximately {count} '
                                                                                        'additional measurements are '
                                                                                        'required.',
 'More measurements are needed for this weekday and hour.': 'More measurements are needed for this weekday and hour.',
 'More variable than Poisson expectation': 'More variable than Poisson expectation',
 'Move away from the suspected source if safe to do so, avoid unnecessary exposure and seek qualified radiation-protection advice.': 'Move '
                                                                                                                                     'away '
                                                                                                                                     'from '
                                                                                                                                     'the '
                                                                                                                                     'suspected '
                                                                                                                                     'source '
                                                                                                                                     'if '
                                                                                                                                     'safe '
                                                                                                                                     'to '
                                                                                                                                     'do '
                                                                                                                                     'so, '
                                                                                                                                     'avoid '
                                                                                                                                     'unnecessary '
                                                                                                                                     'exposure '
                                                                                                                                     'and '
                                                                                                                                     'seek '
                                                                                                                                     'qualified '
                                                                                                                                     'radiation-protection '
                                                                                                                                     'advice.',
 'Never': 'Never',
 'Newest sample': 'Newest sample',
 'Next upload': 'Next upload',
 'No GMC device detected': 'No GMC device detected',
 'No action is required while the result remains normal. Investigate persistent changes by checking the measurement location and comparing both devices.': 'No '
                                                                                                                                                           'action '
                                                                                                                                                           'is '
                                                                                                                                                           'required '
                                                                                                                                                           'while '
                                                                                                                                                           'the '
                                                                                                                                                           'result '
                                                                                                                                                           'remains '
                                                                                                                                                           'normal. '
                                                                                                                                                           'Investigate '
                                                                                                                                                           'persistent '
                                                                                                                                                           'changes '
                                                                                                                                                           'by '
                                                                                                                                                           'checking '
                                                                                                                                                           'the '
                                                                                                                                                           'measurement '
                                                                                                                                                           'location '
                                                                                                                                                           'and '
                                                                                                                                                           'comparing '
                                                                                                                                                           'both '
                                                                                                                                                           'devices.',
 'No action is required. Continue normal monitoring.': 'No action is required. Continue normal monitoring.',
 'No action is required. The assessment becomes more reliable as additional measurements are collected.': 'No action '
                                                                                                          'is '
                                                                                                          'required. '
                                                                                                          'The '
                                                                                                          'assessment '
                                                                                                          'becomes '
                                                                                                          'more '
                                                                                                          'reliable '
                                                                                                          'as '
                                                                                                          'additional '
                                                                                                          'measurements '
                                                                                                          'are '
                                                                                                          'collected.',
 'No action required': 'No action required',
 'No active device warnings': 'No active device warnings',
 'No connected GMC device': 'No connected GMC device',
 'No connected counter is available yet. The next serial scan runs automatically.': 'No connected counter is '
                                                                                    'available yet. The next serial '
                                                                                    'scan runs automatically.',
 'No connected devices.': 'No connected devices.',
 'No current pressure source is available': 'No current pressure source is available',
 'No data': 'No data',
 'No known GMC devices': 'No known GMC devices',
 'No matching Home Assistant entities': 'No matching Home Assistant entities',
 'No measurement yet': 'No measurement yet',
 'No measurements in selected period': 'No measurements in selected period',
 'No measurements yet.': 'No measurements yet.',
 'No persistent level shift detected': 'No persistent level shift detected',
 'No position changes recorded.': 'No position changes recorded.',
 'No pressure variation': 'No pressure variation',
 'No pressure-typical signature': 'No pressure-typical signature',
 'No pronounced baseline jumps detected.': 'No pronounced baseline jumps detected.',
 'No reports have been requested in this browser yet.': 'No reports have been requested in this browser yet.',
 'No shared rise detected.': 'No shared rise detected.',
 'No stored measurements': 'No stored measurements',
 'No suitable serial device was found.': 'No suitable serial device was found.',
 'No sustained relative anomaly events detected': 'No sustained relative anomaly events detected',
 'No valid CPM baseline': 'No valid CPM baseline',
 'Normal': 'Normal',
 'Normal for this time': 'Normal for this time',
 'Normal: within the usual local range': 'Normal: within the usual local range',
 'Not available yet — at least two CPM samples are required': 'Not available yet — at least two CPM samples are '
                                                              'required',
 'Not available yet — more baseline history is required': 'Not available yet — more baseline history is required',
 'Not available yet — more paired samples are required': 'Not available yet — more paired samples are required',
 'Not available yet — no temperature samples were stored in the current 24 h window.': 'Not available yet — no '
                                                                                       'temperature samples were '
                                                                                       'stored in the current 24 h '
                                                                                       'window.',
 'Not available yet — the 24 h CPM series needs variation and at least two samples': 'Not available yet — the 24 h '
                                                                                     'CPM series needs variation and '
                                                                                     'at least two samples',
 'Not available yet — the 24 h mean and spread are still insufficient': 'Not available yet — the 24 h mean and '
                                                                        'spread are still insufficient',
 'Not available — CPM did not vary during this period': 'Not available — CPM did not vary during this period',
 'Not available — the sensor value did not vary during this period': 'Not available — the sensor value did not vary '
                                                                     'during this period',
 'Not configured': 'Not configured',
 'Not connected': 'Not connected',
 'Not detected yet': 'Not detected yet',
 'Not enough local history yet': 'Not enough local history yet',
 'Not found': 'Not found',
 'Not recorded in this browser': 'Not recorded in this browser',
 'Not suitable as a GMC device': 'Not suitable as a GMC device',
 'Not suitable for GMC': 'Not suitable for GMC',
 'Not yet checked as a GMC device': 'Not yet checked as a GMC device',
 'Noticeable': 'Noticeable',
 'Noticeable baseline drift': 'Noticeable baseline drift',
 'Noticeable difference from Poisson-like spread': 'Noticeable difference from Poisson-like spread',
 'Noticeable statistical deviation': 'Noticeable statistical deviation',
 'Noticeable: above the usual local range': 'Noticeable: above the usual local range',
 'Number of samples': 'Number of samples',
 'Observed': 'Observed',
 'Observed SD / √mean': 'Observed SD / √mean',
 'Official reference values': 'Official reference values',
 'Offline': 'Offline',
 'Oldest sample': 'Oldest sample',
 'One current weather entity is available': 'One current weather entity is available',
 'One-hour mean is {deviation:+.1f}% relative to the learned baseline': 'One-hour mean is {deviation:+.1f}% relative '
                                                                        'to the learned baseline',
 'One-hour means': 'One-hour means',
 'One-hour robust level is {deviation:+.1f}% relative to the device baseline': 'One-hour robust level is '
                                                                               '{deviation:+.1f}% relative to the '
                                                                               'device baseline',
 'Online': 'Online',
 'Only quality-filtered, one-to-one time-matched measurements are compared. Agreement, correlation, relative bias and stability are evaluated separately so one faulty counter does not automatically define the site result.': 'Only '
                                                                                                                                                                                                                                'quality-filtered, '
                                                                                                                                                                                                                                'one-to-one '
                                                                                                                                                                                                                                'time-matched '
                                                                                                                                                                                                                                'measurements '
                                                                                                                                                                                                                                'are '
                                                                                                                                                                                                                                'compared. '
                                                                                                                                                                                                                                'Agreement, '
                                                                                                                                                                                                                                'correlation, '
                                                                                                                                                                                                                                'relative '
                                                                                                                                                                                                                                'bias '
                                                                                                                                                                                                                                'and '
                                                                                                                                                                                                                                'stability '
                                                                                                                                                                                                                                'are '
                                                                                                                                                                                                                                'evaluated '
                                                                                                                                                                                                                                'separately '
                                                                                                                                                                                                                                'so '
                                                                                                                                                                                                                                'one '
                                                                                                                                                                                                                                'faulty '
                                                                                                                                                                                                                                'counter '
                                                                                                                                                                                                                                'does '
                                                                                                                                                                                                                                'not '
                                                                                                                                                                                                                                'automatically '
                                                                                                                                                                                                                                'define '
                                                                                                                                                                                                                                'the '
                                                                                                                                                                                                                                'site '
                                                                                                                                                                                                                                'result.',
 'Only the most important conclusions at a glance': 'Only the most important conclusions at a glance',
 'Open': 'Open',
 'Open serial device connections': 'Open serial device connections',
 'Operational events cleared': 'Operational events cleared',
 'Orientation cannot be verified automatically': 'Orientation cannot be verified automatically',
 'Orientation changes detected': 'Orientation changes detected',
 'Orientation data is temporarily unavailable.': 'Orientation data is temporarily unavailable.',
 'Orientation qualification': 'Orientation qualification',
 'Orientation stable': 'Orientation stable',
 'Original raw-data CSV': 'Original raw-data CSV',
 'Outliers and invalid measurements': 'Outliers and invalid measurements',
 'Overview': 'Overview',
 'P95 CPM': 'P95 CPM',
 'P95: {value} CPM': 'P95: {value} CPM',
 'P99 CPM': 'P99 CPM',
 'P99: {value} CPM': 'P99: {value} CPM',
 'PDF report': 'PDF report',
 'Pair-level disagreement': 'Pair-level disagreement',
 'Pearson r · n={count} paired samples': 'Pearson r · n={count} paired samples',
 'Period: {period} ({timezone})': 'Period: {period} ({timezone})',
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
 'Pitch angle': 'Pitch angle',
 'Plausibilised from two weather entities': 'Plausibilised from two weather entities',
 'Poisson SD ratio': 'Poisson SD ratio',
 'Poisson SD ratio = observed standard deviation / √mean; a value near 1 indicates Poisson-like spread.': 'Poisson '
                                                                                                          'SD ratio '
                                                                                                          '= '
                                                                                                          'observed '
                                                                                                          'standard '
                                                                                                          'deviation '
                                                                                                          '/ √mean; '
                                                                                                          'a value '
                                                                                                          'near 1 '
                                                                                                          'indicates '
                                                                                                          'Poisson-like '
                                                                                                          'spread.',
 'Poisson SD ratio formula explanation': 'Poisson SD ratio formula explanation',
 'Poisson SD ratio: {value}': 'Poisson SD ratio: {value}',
 'Poisson counting interval from the observed impulse count': 'Poisson counting interval from the observed impulse '
                                                              'count',
 'Poisson expectation (λ={mean:.2f})': 'Poisson expectation (λ={mean:.2f})',
 'Poor': 'Poor',
 'Position change log': 'Position change log',
 'Possible GMC connection cable': 'Possible GMC connection cable',
 'Possible persistent level shift': 'Possible persistent level shift',
 'Pressure model is still being formed': 'Pressure model is still being formed',
 'Pressure model unavailable': 'Pressure model unavailable',
 'Pressure-typical signature is pronounced': 'Pressure-typical signature is pronounced',
 'Preview backup': 'Preview backup',
 'Previous day': 'Previous day',
 'Previous week': 'Previous week',
 'Probable real change': 'Probable real change',
 'Probable shared measurement-site change': 'Probable shared measurement-site change',
 'Profile': 'Profile',
 'Profile is still being formed': 'Profile is still being formed',
 'Provider': 'Provider',
 'Public GMCMap upload': 'Public GMCMap upload',
 'Quality weight': 'Quality weight',
 'Quality-filtered correlation': 'Quality-filtered correlation',
 'Quality-filtered measurement CSV': 'Quality-filtered measurement CSV',
 'Quick downloads': 'Quick downloads',
 'Radiation 1 h Mean': 'Radiation 1 h Mean',
 'Radiation 1 h Median': 'Radiation 1 h Median',
 'Radiation 1 h Standard Deviation': 'Radiation 1 h Standard Deviation',
 'Radiation Baseline Deviation': 'Radiation Baseline Deviation',
 'Radiation CPM': 'Radiation CPM',
 'Radiation Rapid Change': 'Radiation Rapid Change',
 'Radiation count rate [CPM]': 'Radiation count rate [CPM]',
 'Radiation counts fluctuate naturally. The Fano factor and Poisson spread ratio compare the observed variation with a simple counting-statistics model; they describe distribution shape but not a physical cause or calibration state.': 'Radiation '
                                                                                                                                                                                                                                           'counts '
                                                                                                                                                                                                                                           'fluctuate '
                                                                                                                                                                                                                                           'naturally. '
                                                                                                                                                                                                                                           'The '
                                                                                                                                                                                                                                           'Fano '
                                                                                                                                                                                                                                           'factor '
                                                                                                                                                                                                                                           'and '
                                                                                                                                                                                                                                           'Poisson '
                                                                                                                                                                                                                                           'spread '
                                                                                                                                                                                                                                           'ratio '
                                                                                                                                                                                                                                           'compare '
                                                                                                                                                                                                                                           'the '
                                                                                                                                                                                                                                           'observed '
                                                                                                                                                                                                                                           'variation '
                                                                                                                                                                                                                                           'with '
                                                                                                                                                                                                                                           'a '
                                                                                                                                                                                                                                           'simple '
                                                                                                                                                                                                                                           'counting-statistics '
                                                                                                                                                                                                                                           'model; '
                                                                                                                                                                                                                                           'they '
                                                                                                                                                                                                                                           'describe '
                                                                                                                                                                                                                                           'distribution '
                                                                                                                                                                                                                                           'shape '
                                                                                                                                                                                                                                           'but '
                                                                                                                                                                                                                                           'not '
                                                                                                                                                                                                                                           'a '
                                                                                                                                                                                                                                           'physical '
                                                                                                                                                                                                                                           'cause '
                                                                                                                                                                                                                                           'or '
                                                                                                                                                                                                                                           'calibration '
                                                                                                                                                                                                                                           'state.',
 'Radiation measurement continues unless the device status says otherwise.': 'Radiation measurement continues unless '
                                                                             'the device status says otherwise.',
 'Radiation measurement continues. An external Home Assistant temperature may be used when configured.': 'Radiation '
                                                                                                         'measurement '
                                                                                                         'continues. '
                                                                                                         'An '
                                                                                                         'external '
                                                                                                         'Home '
                                                                                                         'Assistant '
                                                                                                         'temperature '
                                                                                                         'may be '
                                                                                                         'used when '
                                                                                                         'configured.',
 'Radiation measurement continues; only the optional orientation value is affected.': 'Radiation measurement '
                                                                                      'continues; only the optional '
                                                                                      'orientation value is '
                                                                                      'affected.',
 'Radiation monitoring analysis': 'Radiation monitoring analysis',
 'Radiation traffic light': 'Radiation traffic light',
 'Radiation traffic light hysteresis explanation': 'Radiation traffic light hysteresis explanation',
 'Radiation traffic light uses hysteresis: it enters yellow at {yellow_enter:g}% and clears below {yellow_clear:g}%; it enters red at {red_enter:g}% and clears below {red_clear:g}%.': 'Radiation '
                                                                                                                                                                                        'traffic '
                                                                                                                                                                                        'light '
                                                                                                                                                                                        'uses '
                                                                                                                                                                                        'hysteresis: '
                                                                                                                                                                                        'it '
                                                                                                                                                                                        'enters '
                                                                                                                                                                                        'yellow '
                                                                                                                                                                                        'at '
                                                                                                                                                                                        '{yellow_enter:g}% '
                                                                                                                                                                                        'and '
                                                                                                                                                                                        'clears '
                                                                                                                                                                                        'below '
                                                                                                                                                                                        '{yellow_clear:g}%; '
                                                                                                                                                                                        'it '
                                                                                                                                                                                        'enters '
                                                                                                                                                                                        'red '
                                                                                                                                                                                        'at '
                                                                                                                                                                                        '{red_enter:g}% '
                                                                                                                                                                                        'and '
                                                                                                                                                                                        'clears '
                                                                                                                                                                                        'below '
                                                                                                                                                                                        '{red_clear:g}%.',
 'Raw CSV': 'Raw CSV',
 'Raw device values are stored separately before quality filtering': 'Raw device values are stored separately before '
                                                                     'quality filtering',
 'Raw gyro [signed int16]': 'Raw gyro [signed int16]',
 'Raw-data archive': 'Raw-data archive',
 'Read-only mode': 'Read-only mode',
 'Ready for new measurements': 'Ready for new measurements',
 'Recent 30 days compared with the preceding 30 days': 'Recent 30 days compared with the preceding 30 days',
 'Recent data quality is high': 'Recent data quality is high',
 'Recent period compared with the preceding period': 'Recent period compared with the preceding period',
 'Recent quality-filtered data quality is high': 'Recent quality-filtered data quality is high',
 'Recent reports': 'Recent reports',
 'Recommendation': 'Recommendation',
 'Recommended': 'Recommended',
 'Reconnects': 'Reconnects',
 'Red': 'Red',
 'Reduced': 'Reduced',
 'Refreshing device status…': 'Refreshing device status…',
 'Relative anomaly indicator only; not a safety classification.': 'Relative anomaly indicator only; not a safety '
                                                                  'classification.',
 'Relative correction factor': 'Relative correction factor',
 'Relative spread': 'Relative spread',
 'Relative to 7 d baseline': 'Relative to 7 d baseline',
 'Relative-factor confidence': 'Relative-factor confidence',
 'Remaining deviation': 'Remaining deviation',
 'Remove': 'Remove',
 'Report': 'Report',
 'Report generation failed': 'Report generation failed',
 'Report target': 'Report target',
 'Reports': 'Reports',
 'Reports for the displayed analysis': 'Reports for the displayed analysis',
 'Rescan devices': 'Rescan devices',
 'Resolve persistent connection gaps before relying on long-term comparisons.': 'Resolve persistent connection gaps '
                                                                                'before relying on long-term '
                                                                                'comparisons.',
 'Restore backup': 'Restore backup',
 'Restore complete': 'Restore complete',
 'Restore confirmation text must be exactly RESTORE': 'Restore confirmation text must be exactly RESTORE',
 'Restore history': 'Restore history',
 'Restore is disabled by default.': 'Restore is disabled by default.',
 'Restore upload must be between 1 byte and 128 MiB': 'Restore upload must be between 1 byte and 128 MiB',
 'Return to GMC Radiation Monitoring': 'Return to GMC Radiation Monitoring',
 'Return to GMC Reports': 'Return to GMC Reports',
 'Review the event export for timing and severity': 'Review the event export for timing and severity',
 'Review the recent trend and event timing. Check both counters and the measurement location if the change persists.': 'Review '
                                                                                                                       'the '
                                                                                                                       'recent '
                                                                                                                       'trend '
                                                                                                                       'and '
                                                                                                                       'event '
                                                                                                                       'timing. '
                                                                                                                       'Check '
                                                                                                                       'both '
                                                                                                                       'counters '
                                                                                                                       'and '
                                                                                                                       'the '
                                                                                                                       'measurement '
                                                                                                                       'location '
                                                                                                                       'if '
                                                                                                                       'the '
                                                                                                                       'change '
                                                                                                                       'persists.',
 'Rising': 'Rising',
 'Robust medians are used; rejected measurements and isolated spikes do not immediately change the profile.': 'Robust '
                                                                                                              'medians '
                                                                                                              'are '
                                                                                                              'used; '
                                                                                                              'rejected '
                                                                                                              'measurements '
                                                                                                              'and '
                                                                                                              'isolated '
                                                                                                              'spikes '
                                                                                                              'do '
                                                                                                              'not '
                                                                                                              'immediately '
                                                                                                              'change '
                                                                                                              'the '
                                                                                                              'profile.',
 'Robust one-hour values': 'Robust one-hour values',
 'Roll angle': 'Roll angle',
 'Rolling windows end at the latest stored measurement. Dose-rate values are derived from CPM using the configured factor and are not independently measured. CPM remains the primary measurement. The traffic light is a relative background-anomaly indicator, not an emergency, health, or radiation-safety classification.': 'Rolling '
                                                                                                                                                                                                                                                                                                                                 'windows '
                                                                                                                                                                                                                                                                                                                                 'end '
                                                                                                                                                                                                                                                                                                                                 'at '
                                                                                                                                                                                                                                                                                                                                 'the '
                                                                                                                                                                                                                                                                                                                                 'latest '
                                                                                                                                                                                                                                                                                                                                 'stored '
                                                                                                                                                                                                                                                                                                                                 'measurement. '
                                                                                                                                                                                                                                                                                                                                 'Dose-rate '
                                                                                                                                                                                                                                                                                                                                 'values '
                                                                                                                                                                                                                                                                                                                                 'are '
                                                                                                                                                                                                                                                                                                                                 'derived '
                                                                                                                                                                                                                                                                                                                                 'from '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'using '
                                                                                                                                                                                                                                                                                                                                 'the '
                                                                                                                                                                                                                                                                                                                                 'configured '
                                                                                                                                                                                                                                                                                                                                 'factor '
                                                                                                                                                                                                                                                                                                                                 'and '
                                                                                                                                                                                                                                                                                                                                 'are '
                                                                                                                                                                                                                                                                                                                                 'not '
                                                                                                                                                                                                                                                                                                                                 'independently '
                                                                                                                                                                                                                                                                                                                                 'measured. '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'remains '
                                                                                                                                                                                                                                                                                                                                 'the '
                                                                                                                                                                                                                                                                                                                                 'primary '
                                                                                                                                                                                                                                                                                                                                 'measurement. '
                                                                                                                                                                                                                                                                                                                                 'The '
                                                                                                                                                                                                                                                                                                                                 'traffic '
                                                                                                                                                                                                                                                                                                                                 'light '
                                                                                                                                                                                                                                                                                                                                 'is '
                                                                                                                                                                                                                                                                                                                                 'a '
                                                                                                                                                                                                                                                                                                                                 'relative '
                                                                                                                                                                                                                                                                                                                                 'background-anomaly '
                                                                                                                                                                                                                                                                                                                                 'indicator, '
                                                                                                                                                                                                                                                                                                                                 'not '
                                                                                                                                                                                                                                                                                                                                 'an '
                                                                                                                                                                                                                                                                                                                                 'emergency, '
                                                                                                                                                                                                                                                                                                                                 'health, '
                                                                                                                                                                                                                                                                                                                                 'or '
                                                                                                                                                                                                                                                                                                                                 'radiation-safety '
                                                                                                                                                                                                                                                                                                                                 'classification.',
 'SD: {value} CPM': 'SD: {value} CPM',
 'SQLite backup': 'SQLite backup',
 'SQLite backup file': 'SQLite backup file',
 'SQLite database vacuum completed': 'SQLite database vacuum completed',
 'Sample standard deviation': 'Sample standard deviation',
 'Samples': 'Samples',
 'Samples: {samples} / {expected}': 'Samples: {samples} / {expected}',
 'Sampling interval: {interval} s | Samples: {samples}/{expected} | Completeness: {completeness:.2f}% | Generated: {generated} | App {version}': 'Sampling '
                                                                                                                                                 'interval: '
                                                                                                                                                 '{interval} '
                                                                                                                                                 's '
                                                                                                                                                 '| '
                                                                                                                                                 'Samples: '
                                                                                                                                                 '{samples}/{expected} '
                                                                                                                                                 '| '
                                                                                                                                                 'Completeness: '
                                                                                                                                                 '{completeness:.2f}% '
                                                                                                                                                 '| '
                                                                                                                                                 'Generated: '
                                                                                                                                                 '{generated} '
                                                                                                                                                 '| '
                                                                                                                                                 'App '
                                                                                                                                                 '{version}',
 'Sampling interval: {seconds} s': 'Sampling interval: {seconds} s',
 'Sat': 'Sat',
 'Saturday': 'Saturday',
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
 'Second half vs first half of available 7 d window': 'Second half vs first half of available 7 d window',
 'Select a SQLite backup file first.': 'Select a SQLite backup file first.',
 'Select a backup to preview its schema, devices, data period and row counts before restoring.': 'Select a backup to '
                                                                                                 'preview its '
                                                                                                 'schema, devices, '
                                                                                                 'data period and '
                                                                                                 'row counts before '
                                                                                                 'restoring.',
 'Select exactly one serial device for every configured GMC': 'Select exactly one serial device for every configured '
                                                              'GMC',
 'Select the GMC-320, the GMC-500+, or a combined report containing both devices.': 'Select the GMC-320, the '
                                                                                    'GMC-500+, or a combined report '
                                                                                    'containing both devices.',
 'Select the physical counter for this configured GMC device.': 'Select the physical counter for this configured GMC '
                                                                'device.',
 'Selected serial device is no longer available': 'Selected serial device is no longer available',
 'Separate original samples in 24 h · {accepted} accepted · {pending} pending': 'Separate original samples in 24 h · '
                                                                                '{accepted} accepted · {pending} '
                                                                                'pending',
 'Serial': 'Serial',
 'Serial Errors Since Start': 'Serial Errors Since Start',
 'Serial Reconnects Since Start': 'Serial Reconnects Since Start',
 'Serial USB device': 'Serial USB device',
 'Serial connection recovered': 'Serial connection recovered',
 'Serial device connections': 'Serial device connections',
 'Serial errors / reconnects': 'Serial errors / reconnects',
 'Serial port': 'Serial port',
 'Serial: {serial} | Period: {period} | Timezone: {timezone}': 'Serial: {serial} | Period: {period} | Timezone: '
                                                               '{timezone}',
 'Serial: {value}': 'Serial: {value}',
 'Severity': 'Severity',
 'Shared CPM rise': 'Shared CPM rise',
 'Shared event detector': 'Shared event detector',
 'Show analysis': 'Show analysis',
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
 'Since app start': 'Since app start',
 'Slightly noticeable': 'Slightly noticeable',
 'Slightly tilted': 'Slightly tilted',
 'Small baseline drift': 'Small baseline drift',
 'Smart Alert State': 'Smart Alert State',
 'Smoothed historical background trend': 'Smoothed historical background trend',
 'Source validation': 'Source validation',
 'Specific ISO week': 'Specific ISO week',
 'Specific date': 'Specific date',
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
 'Stability and device health': 'Stability and device health',
 'Stable': 'Stable',
 'Stable device path': 'Stable device path',
 'Stable devices': 'Stable devices',
 'Standard deviation CPM': 'Standard deviation CPM',
 'Start time UTC': 'Start time UTC',
 'Start time local': 'Start time local',
 'Start with a readable PDF or a complete ZIP bundle. Raw and specialist formats remain available below without crowding the main view.': 'Start '
                                                                                                                                          'with '
                                                                                                                                          'a '
                                                                                                                                          'readable '
                                                                                                                                          'PDF '
                                                                                                                                          'or '
                                                                                                                                          'a '
                                                                                                                                          'complete '
                                                                                                                                          'ZIP '
                                                                                                                                          'bundle. '
                                                                                                                                          'Raw '
                                                                                                                                          'and '
                                                                                                                                          'specialist '
                                                                                                                                          'formats '
                                                                                                                                          'remain '
                                                                                                                                          'available '
                                                                                                                                          'below '
                                                                                                                                          'without '
                                                                                                                                          'crowding '
                                                                                                                                          'the '
                                                                                                                                          'main '
                                                                                                                                          'view.',
 'Statistical indication only': 'Statistical indication only',
 'Statistical level shift': 'Statistical level shift',
 'Statistically noticeable': 'Statistically noticeable',
 'Statistics': 'Statistics',
 'Stored samples': 'Stored samples',
 'Stored samples across all devices': 'Stored samples across all devices',
 'Stored samples for this device': 'Stored samples for this device',
 'Strong common signal': 'Strong common signal',
 'Strong linear relationship': 'Strong linear relationship',
 'Strong statistical deviation': 'Strong statistical deviation',
 'Successful uploads': 'Successful uploads',
 'Successful uploads since start': 'Successful uploads since start',
 'Suitable for most trend analysis': 'Suitable for most trend analysis',
 'Summary': 'Summary',
 'Sun': 'Sun',
 'Sunday': 'Sunday',
 'Supervisor API access is unavailable': 'Supervisor API access is unavailable',
 'Supply voltage [V]': 'Supply voltage [V]',
 'Suspicious CPM value is being verified': 'Suspicious CPM value is being verified',
 'Sustained Radiation Alert': 'Sustained Radiation Alert',
 'Sustained relative anomaly events': 'Sustained relative anomaly events',
 'Sustained yellow/red relative anomaly events': 'Sustained yellow/red relative anomaly events',
 'Temperature': 'Temperature',
 'Temperature / voltage errors': 'Temperature / voltage errors',
 'Temperature Errors Since Start': 'Temperature Errors Since Start',
 'Temperature [°C]': 'Temperature [°C]',
 'Temperature and voltage relationships': 'Temperature and voltage relationships',
 'Temperature bins (24 h)': 'Temperature bins (24 h)',
 'Temperature correlation': 'Temperature correlation',
 'Temperature profile is still being formed': 'Temperature profile is still being formed',
 'Temperature trend': 'Temperature trend',
 'Temperature-specific background': 'Temperature-specific background',
 'The Supervisor options could not be loaded: {error}': 'The Supervisor options could not be loaded: {error}',
 'The absolute assessment starts after the first measurement.': 'The absolute assessment starts after the first '
                                                                'measurement.',
 'The absolute level is below the configured warning threshold, but the value is far above the learned local background.': 'The '
                                                                                                                           'absolute '
                                                                                                                           'level '
                                                                                                                           'is '
                                                                                                                           'below '
                                                                                                                           'the '
                                                                                                                           'configured '
                                                                                                                           'warning '
                                                                                                                           'threshold, '
                                                                                                                           'but '
                                                                                                                           'the '
                                                                                                                           'value '
                                                                                                                           'is '
                                                                                                                           'far '
                                                                                                                           'above '
                                                                                                                           'the '
                                                                                                                           'learned '
                                                                                                                           'local '
                                                                                                                           'background.',
 'The absolute level is currently uncritical, but the local comparison or short-term trend deserves continued observation.': 'The '
                                                                                                                             'absolute '
                                                                                                                             'level '
                                                                                                                             'is '
                                                                                                                             'currently '
                                                                                                                             'uncritical, '
                                                                                                                             'but '
                                                                                                                             'the '
                                                                                                                             'local '
                                                                                                                             'comparison '
                                                                                                                             'or '
                                                                                                                             'short-term '
                                                                                                                             'trend '
                                                                                                                             'deserves '
                                                                                                                             'continued '
                                                                                                                             'observation.',
 'The absolute level is currently uncritical. More local history is required before anomaly detection becomes reliable.': 'The '
                                                                                                                          'absolute '
                                                                                                                          'level '
                                                                                                                          'is '
                                                                                                                          'currently '
                                                                                                                          'uncritical. '
                                                                                                                          'More '
                                                                                                                          'local '
                                                                                                                          'history '
                                                                                                                          'is '
                                                                                                                          'required '
                                                                                                                          'before '
                                                                                                                          'anomaly '
                                                                                                                          'detection '
                                                                                                                          'becomes '
                                                                                                                          'reliable.',
 'The add-on is restarting so the new serial assignments become active.': 'The add-on is restarting so the new '
                                                                          'serial assignments become active.',
 'The app combines the recent trend, robust statistics, agreement between connected counters and the learned local background. The result is a statistical aid and does not identify a physical cause.': 'The '
                                                                                                                                                                                                         'app '
                                                                                                                                                                                                         'combines '
                                                                                                                                                                                                         'the '
                                                                                                                                                                                                         'recent '
                                                                                                                                                                                                         'trend, '
                                                                                                                                                                                                         'robust '
                                                                                                                                                                                                         'statistics, '
                                                                                                                                                                                                         'agreement '
                                                                                                                                                                                                         'between '
                                                                                                                                                                                                         'connected '
                                                                                                                                                                                                         'counters '
                                                                                                                                                                                                         'and '
                                                                                                                                                                                                         'the '
                                                                                                                                                                                                         'learned '
                                                                                                                                                                                                         'local '
                                                                                                                                                                                                         'background. '
                                                                                                                                                                                                         'The '
                                                                                                                                                                                                         'result '
                                                                                                                                                                                                         'is '
                                                                                                                                                                                                         'a '
                                                                                                                                                                                                         'statistical '
                                                                                                                                                                                                         'aid '
                                                                                                                                                                                                         'and '
                                                                                                                                                                                                         'does '
                                                                                                                                                                                                         'not '
                                                                                                                                                                                                         'identify '
                                                                                                                                                                                                         'a '
                                                                                                                                                                                                         'physical '
                                                                                                                                                                                                         'cause.',
 'The app compares quality-filtered measurements from the same weekday and hour. Robust medians reduce the influence of isolated spikes and regular daily patterns are kept separate from unusual changes.': 'The '
                                                                                                                                                                                                             'app '
                                                                                                                                                                                                             'compares '
                                                                                                                                                                                                             'quality-filtered '
                                                                                                                                                                                                             'measurements '
                                                                                                                                                                                                             'from '
                                                                                                                                                                                                             'the '
                                                                                                                                                                                                             'same '
                                                                                                                                                                                                             'weekday '
                                                                                                                                                                                                             'and '
                                                                                                                                                                                                             'hour. '
                                                                                                                                                                                                             'Robust '
                                                                                                                                                                                                             'medians '
                                                                                                                                                                                                             'reduce '
                                                                                                                                                                                                             'the '
                                                                                                                                                                                                             'influence '
                                                                                                                                                                                                             'of '
                                                                                                                                                                                                             'isolated '
                                                                                                                                                                                                             'spikes '
                                                                                                                                                                                                             'and '
                                                                                                                                                                                                             'regular '
                                                                                                                                                                                                             'daily '
                                                                                                                                                                                                             'patterns '
                                                                                                                                                                                                             'are '
                                                                                                                                                                                                             'kept '
                                                                                                                                                                                                             'separate '
                                                                                                                                                                                                             'from '
                                                                                                                                                                                                             'unusual '
                                                                                                                                                                                                             'changes.',
 'The app compares quality-filtered radiation measurements with available air-pressure data. A statistical relationship can support interpretation, but correlation alone does not prove a cosmic or environmental cause.': 'The '
                                                                                                                                                                                                                            'app '
                                                                                                                                                                                                                            'compares '
                                                                                                                                                                                                                            'quality-filtered '
                                                                                                                                                                                                                            'radiation '
                                                                                                                                                                                                                            'measurements '
                                                                                                                                                                                                                            'with '
                                                                                                                                                                                                                            'available '
                                                                                                                                                                                                                            'air-pressure '
                                                                                                                                                                                                                            'data. '
                                                                                                                                                                                                                            'A '
                                                                                                                                                                                                                            'statistical '
                                                                                                                                                                                                                            'relationship '
                                                                                                                                                                                                                            'can '
                                                                                                                                                                                                                            'support '
                                                                                                                                                                                                                            'interpretation, '
                                                                                                                                                                                                                            'but '
                                                                                                                                                                                                                            'correlation '
                                                                                                                                                                                                                            'alone '
                                                                                                                                                                                                                            'does '
                                                                                                                                                                                                                            'not '
                                                                                                                                                                                                                            'prove '
                                                                                                                                                                                                                            'a '
                                                                                                                                                                                                                            'cosmic '
                                                                                                                                                                                                                            'or '
                                                                                                                                                                                                                            'environmental '
                                                                                                                                                                                                                            'cause.',
 'The comparison uses only quality-filtered, one-to-one paired measurements.': 'The comparison uses only '
                                                                               'quality-filtered, one-to-one paired '
                                                                               'measurements.',
 'The configured danger threshold is exceeded.': 'The configured danger threshold is exceeded.',
 'The connected counters currently agree well': 'The connected counters currently agree well',
 'The counters disagree, so a device-specific effect is more likely': 'The counters disagree, so a device-specific '
                                                                      'effect is more likely',
 'The current radiation level is uncritical according to the selected thresholds.': 'The current radiation level is '
                                                                                    'uncritical according to the '
                                                                                    'selected thresholds.',
 'The current value is below the configured warning threshold and within the usual local range.': 'The current value '
                                                                                                  'is below the '
                                                                                                  'configured '
                                                                                                  'warning threshold '
                                                                                                  'and within the '
                                                                                                  'usual local '
                                                                                                  'range.',
 'The current value is within the configured warning range.': 'The current value is within the configured warning '
                                                              'range.',
 'The deviation is device-specific; the measurement-site profile remains normal': 'The deviation is device-specific; '
                                                                                  'the measurement-site profile '
                                                                                  'remains normal',
 'The device baseline is available, but there are not enough recent measurements for a current comparison.': 'The '
                                                                                                             'device '
                                                                                                             'baseline '
                                                                                                             'is '
                                                                                                             'available, '
                                                                                                             'but '
                                                                                                             'there '
                                                                                                             'are '
                                                                                                             'not '
                                                                                                             'enough '
                                                                                                             'recent '
                                                                                                             'measurements '
                                                                                                             'for a '
                                                                                                             'current '
                                                                                                             'comparison.',
 'The device clock differs from Home Assistant time.': 'The device clock differs from Home Assistant time.',
 'The filtered counters disagree, so a device-specific effect is more likely': 'The filtered counters disagree, so a '
                                                                               'device-specific effect is more '
                                                                               'likely',
 'The learned baseline remains available. More current samples are required before the local comparison can be updated.': 'The '
                                                                                                                          'learned '
                                                                                                                          'baseline '
                                                                                                                          'remains '
                                                                                                                          'available. '
                                                                                                                          'More '
                                                                                                                          'current '
                                                                                                                          'samples '
                                                                                                                          'are '
                                                                                                                          'required '
                                                                                                                          'before '
                                                                                                                          'the '
                                                                                                                          'local '
                                                                                                                          'comparison '
                                                                                                                          'can '
                                                                                                                          'be '
                                                                                                                          'updated.',
 'The level-shift detector looks for persistent statistical changes and does not alter radiation warnings.': 'The '
                                                                                                             'level-shift '
                                                                                                             'detector '
                                                                                                             'looks '
                                                                                                             'for '
                                                                                                             'persistent '
                                                                                                             'statistical '
                                                                                                             'changes '
                                                                                                             'and '
                                                                                                             'does '
                                                                                                             'not '
                                                                                                             'alter '
                                                                                                             'radiation '
                                                                                                             'warnings.',
 'The local background is still being learned, so no anomaly assessment is available yet.': 'The local background is '
                                                                                            'still being learned, so '
                                                                                            'no anomaly assessment '
                                                                                            'is available yet.',
 'The measurement-site baseline is {deviation:+.1f}% above its typical value': 'The measurement-site baseline is '
                                                                               '{deviation:+.1f}% above its typical '
                                                                               'value',
 'The measurement-site profile combines both devices with quality weighting': 'The measurement-site profile combines '
                                                                              'both devices with quality weighting',
 'The measurement-site profile currently relies on one device': 'The measurement-site profile currently relies on '
                                                                'one device',
 'The pressure model cannot prove cosmic radiation and never suppresses radiation warnings.': 'The pressure model '
                                                                                              'cannot prove cosmic '
                                                                                              'radiation and never '
                                                                                              'suppresses radiation '
                                                                                              'warnings.',
 'The quality-filtered counter comparison currently agrees well': 'The quality-filtered counter comparison currently '
                                                                  'agrees well',
 'The recent 30-minute robust trend is rising': 'The recent 30-minute robust trend is rising',
 'The recent 30-minute trend is rising': 'The recent 30-minute trend is rising',
 'The request could not be processed. Check the selected options.': 'The request could not be processed. Check the '
                                                                    'selected options.',
 'The score combines time-window coverage, missing or irregular intervals, duplicate timestamps and optional-sensor coverage. It indicates how strongly the analysis can rely on the stored series.': 'The '
                                                                                                                                                                                                      'score '
                                                                                                                                                                                                      'combines '
                                                                                                                                                                                                      'time-window '
                                                                                                                                                                                                      'coverage, '
                                                                                                                                                                                                      'missing '
                                                                                                                                                                                                      'or '
                                                                                                                                                                                                      'irregular '
                                                                                                                                                                                                      'intervals, '
                                                                                                                                                                                                      'duplicate '
                                                                                                                                                                                                      'timestamps '
                                                                                                                                                                                                      'and '
                                                                                                                                                                                                      'optional-sensor '
                                                                                                                                                                                                      'coverage. '
                                                                                                                                                                                                      'It '
                                                                                                                                                                                                      'indicates '
                                                                                                                                                                                                      'how '
                                                                                                                                                                                                      'strongly '
                                                                                                                                                                                                      'the '
                                                                                                                                                                                                      'analysis '
                                                                                                                                                                                                      'can '
                                                                                                                                                                                                      'rely '
                                                                                                                                                                                                      'on '
                                                                                                                                                                                                      'the '
                                                                                                                                                                                                      'stored '
                                                                                                                                                                                                      'series.',
 'The serial connection is unstable.': 'The serial connection is unstable.',
 'The traffic light and events are relative anomaly indicators, not safety classifications.': 'The traffic light and '
                                                                                              'events are relative '
                                                                                              'anomaly indicators, '
                                                                                              'not safety '
                                                                                              'classifications.',
 'The value is also within the usual range for this location.': 'The value is also within the usual range for this '
                                                                'location.',
 'The values most users need first': 'The values most users need first',
 'These are statistical changes. They can indicate a location, geometry or environmental change, but do not identify the cause.': 'These '
                                                                                                                                  'are '
                                                                                                                                  'statistical '
                                                                                                                                  'changes. '
                                                                                                                                  'They '
                                                                                                                                  'can '
                                                                                                                                  'indicate '
                                                                                                                                  'a '
                                                                                                                                  'location, '
                                                                                                                                  'geometry '
                                                                                                                                  'or '
                                                                                                                                  'environmental '
                                                                                                                                  'change, '
                                                                                                                                  'but '
                                                                                                                                  'do '
                                                                                                                                  'not '
                                                                                                                                  'identify '
                                                                                                                                  'the '
                                                                                                                                  'cause.',
 'These values describe the shape of the count distribution. They do not by themselves prove a physical cause or a calibration state.': 'These '
                                                                                                                                        'values '
                                                                                                                                        'describe '
                                                                                                                                        'the '
                                                                                                                                        'shape '
                                                                                                                                        'of '
                                                                                                                                        'the '
                                                                                                                                        'count '
                                                                                                                                        'distribution. '
                                                                                                                                        'They '
                                                                                                                                        'do '
                                                                                                                                        'not '
                                                                                                                                        'by '
                                                                                                                                        'themselves '
                                                                                                                                        'prove '
                                                                                                                                        'a '
                                                                                                                                        'physical '
                                                                                                                                        'cause '
                                                                                                                                        'or '
                                                                                                                                        'a '
                                                                                                                                        'calibration '
                                                                                                                                        'state.',
 'This analysis detects unusual changes compared with the normal background at this location. It is not a danger classification; an unusual value can still be below the absolute warning threshold.': 'This '
                                                                                                                                                                                                       'analysis '
                                                                                                                                                                                                       'detects '
                                                                                                                                                                                                       'unusual '
                                                                                                                                                                                                       'changes '
                                                                                                                                                                                                       'compared '
                                                                                                                                                                                                       'with '
                                                                                                                                                                                                       'the '
                                                                                                                                                                                                       'normal '
                                                                                                                                                                                                       'background '
                                                                                                                                                                                                       'at '
                                                                                                                                                                                                       'this '
                                                                                                                                                                                                       'location. '
                                                                                                                                                                                                       'It '
                                                                                                                                                                                                       'is '
                                                                                                                                                                                                       'not '
                                                                                                                                                                                                       'a '
                                                                                                                                                                                                       'danger '
                                                                                                                                                                                                       'classification; '
                                                                                                                                                                                                       'an '
                                                                                                                                                                                                       'unusual '
                                                                                                                                                                                                       'value '
                                                                                                                                                                                                       'can '
                                                                                                                                                                                                       'still '
                                                                                                                                                                                                       'be '
                                                                                                                                                                                                       'below '
                                                                                                                                                                                                       'the '
                                                                                                                                                                                                       'absolute '
                                                                                                                                                                                                       'warning '
                                                                                                                                                                                                       'threshold.',
 'This cannot be undone. Delete all GMC history?': 'This cannot be undone. Delete all GMC history?',
 'This classification only compares the current measurement with the selected thresholds. It does not compare the value with the usual background at this location.': 'This '
                                                                                                                                                                      'classification '
                                                                                                                                                                      'only '
                                                                                                                                                                      'compares '
                                                                                                                                                                      'the '
                                                                                                                                                                      'current '
                                                                                                                                                                      'measurement '
                                                                                                                                                                      'with '
                                                                                                                                                                      'the '
                                                                                                                                                                      'selected '
                                                                                                                                                                      'thresholds. '
                                                                                                                                                                      'It '
                                                                                                                                                                      'does '
                                                                                                                                                                      'not '
                                                                                                                                                                      'compare '
                                                                                                                                                                      'the '
                                                                                                                                                                      'value '
                                                                                                                                                                      'with '
                                                                                                                                                                      'the '
                                                                                                                                                                      'usual '
                                                                                                                                                                      'background '
                                                                                                                                                                      'at '
                                                                                                                                                                      'this '
                                                                                                                                                                      'location.',
 'This factor is only a relative device comparison and is not an absolute radiation calibration.': 'This factor is '
                                                                                                   'only a relative '
                                                                                                   'device '
                                                                                                   'comparison and '
                                                                                                   'is not an '
                                                                                                   'absolute '
                                                                                                   'radiation '
                                                                                                   'calibration.',
 'This report is descriptive and is not a radiation-safety classification.': 'This report is descriptive and is not '
                                                                             'a radiation-safety classification.',
 'Thresholds can be changed in the add-on configuration.': 'Thresholds can be changed in the add-on configuration.',
 'Thu': 'Thu',
 'Thursday': 'Thursday',
 'Tilted': 'Tilted',
 'Time series': 'Time series',
 'Time series, Poisson comparison and weekday/hour heatmap': 'Time series, Poisson comparison and weekday/hour '
                                                             'heatmap',
 'Time-series PNG': 'Time-series PNG',
 'Timestamp diagnostics': 'Timestamp diagnostics',
 'Timezone': 'Timezone',
 'Today so far bundle': 'Today so far bundle',
 'Too few pressure/CPM pairs': 'Too few pressure/CPM pairs',
 'Too few valid paired measurements for a reliable device comparison': 'Too few valid paired measurements for a '
                                                                       'reliable device comparison',
 'Too little or too fragmented for strong conclusions': 'Too little or too fragmented for strong conclusions',
 'Trend (30 min)': 'Trend (30 min)',
 'Tue': 'Tue',
 'Tuesday': 'Tuesday',
 'Type DELETE ALL GMC HISTORY to confirm': 'Type DELETE ALL GMC HISTORY to confirm',
 'Type RESTORE to confirm': 'Type RESTORE to confirm',
 'Typical for {weekday} at {hour}:00': 'Typical for {weekday} at {hour}:00',
 'USB down': 'USB down',
 'USB left': 'USB left',
 'USB right': 'USB right',
 'USB up': 'USB up',
 'UTC timestamp': 'UTC timestamp',
 'Unavailable': 'Unavailable',
 'Unconfirmed values since bridge start': 'Unconfirmed values since bridge start',
 'Uncritical': 'Uncritical',
 'Uncritical: below warning threshold': 'Uncritical: below warning threshold',
 'Unknown': 'Unknown',
 'Unknown GMC': 'Unknown GMC',
 'Unknown report device': 'Unknown report device',
 'Unknown serial device': 'Unknown serial device',
 'Unstable': 'Unstable',
 'Unsupported report format': 'Unsupported report format',
 'Upload errors': 'Upload errors',
 'Upload errors since start': 'Upload errors since start',
 'Upload failed': 'Upload failed',
 'Upload successful': 'Upload successful',
 'Uploading': 'Uploading',
 'Upright': 'Upright',
 'Use this as context only and review longer periods before drawing conclusions.': 'Use this as context only and '
                                                                                   'review longer periods before '
                                                                                   'drawing conclusions.',
 'Valid measurements': 'Valid measurements',
 'Variance / mean': 'Variance / mean',
 'Very close to Poisson-like spread': 'Very close to Poisson-like spread',
 'Very complete 24 h data window': 'Very complete 24 h data window',
 'Very strong linear relationship': 'Very strong linear relationship',
 'Very weak linear relationship': 'Very weak linear relationship',
 'Voltage': 'Voltage',
 'Voltage Errors Since Start': 'Voltage Errors Since Start',
 'Voltage [V]': 'Voltage [V]',
 'Voltage correlation': 'Voltage correlation',
 'Waiting for enough recent measurements': 'Waiting for enough recent measurements',
 'Waiting for first upload': 'Waiting for first upload',
 'Waiting for recent measurements': 'Waiting for recent measurements',
 'Waiting for the first accepted measurement': 'Waiting for the first accepted measurement',
 'Warning': 'Warning',
 'Warning from {warning} s; critical from {critical} s': 'Warning from {warning} s; critical from {critical} s',
 'Warning threshold exceeded': 'Warning threshold exceeded',
 'Warning thresholds': 'Warning thresholds',
 'Weak linear relationship': 'Weak linear relationship',
 'Weather pressure sources disagree': 'Weather pressure sources disagree',
 'Wed': 'Wed',
 'Wednesday': 'Wednesday',
 'Weekday': 'Weekday',
 'Weekday/hour heatmap': 'Weekday/hour heatmap',
 'What does the historical trend mean?': 'What does the historical trend mean?',
 'What each report preserves and how periods are defined': 'What each report preserves and how periods are defined',
 'What should I do?': 'What should I do?',
 'What this assessment means': 'What this assessment means',
 'Why are Poisson values shown?': 'Why are Poisson values shown?',
 'Why is this assessment shown?': 'Why is this assessment shown?',
 'Within local background range': 'Within local background range',
 'Within normal statistical variation': 'Within normal statistical variation',
 'Within the usual local range': 'Within the usual local range',
 'Within warning range': 'Within warning range',
 'Yellow': 'Yellow',
 'Z-score = (latest CPM − 24 h mean) / 24 h standard deviation.': 'Z-score = (latest CPM − 24 h mean) / 24 h '
                                                                  'standard deviation.',
 'Z-score formula explanation': 'Z-score formula explanation',
 'complete and regularly spaced data': 'complete and regularly spaced data',
 'confirmations': 'confirmations',
 'counting uncertainty {value:.2f}%': 'counting uncertainty {value:.2f}%',
 'coverage': 'coverage',
 'daily values': 'daily values',
 'days': 'days',
 'duplicates / clock regressions': 'duplicates / clock regressions',
 'entity patterns': 'entity patterns',
 'errors': 'errors',
 'estimated signal probability': 'estimated signal probability',
 'excluded measurements': 'excluded measurements',
 'longest gap {value} s': 'longest gap {value} s',
 'measurements': 'measurements',
 'minimum sample coverage': 'minimum sample coverage',
 'n={count} paired samples': 'n={count} paired samples',
 'n={count} · {coverage:.1f}% coverage': 'n={count} · {coverage:.1f}% coverage',
 'paired samples': 'paired samples',
 'reconnects': 'reconnects',
 'relative to baseline': 'relative to baseline',
 'score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s': 'score {score:.1f}/100 · coverage '
                                                                           '{coverage:.1f}% · longest gap {gap} s',
 'short / long intervals': 'short / long intervals',
 'since the current bridge start': 'since the current bridge start',
 'temperature coverage {value}%': 'temperature coverage {value}%',
 'unknown': 'unknown',
 'valid hourly values': 'valid hourly values',
 'valid paired samples': 'valid paired samples',
 'voltage coverage {value}%': 'voltage coverage {value}%',
 'write errors since app start': 'write errors since app start',
 '{before:.2f} → {after:.2f} CPM · {sigma:.1f}σ · {hours} h persistent': '{before:.2f} → {after:.2f} CPM · '
                                                                         '{sigma:.1f}σ · {hours} h persistent',
 '{check_type} result cached for {seconds} s · schema v{schema}': '{check_type} result cached for {seconds} s · '
                                                                  'schema v{schema}',
 '{connected} connected · {disconnected} disconnected': '{connected} connected · {disconnected} disconnected',
 '{count} implausible measurements were excluded from the assessment': '{count} implausible measurements were '
                                                                       'excluded from the assessment',
 '{count} measurements': '{count} measurements',
 '{count} measurements and {events} events were removed.': '{count} measurements and {events} events were removed.',
 '{events} events · {diagnostics} diagnostics': '{events} events · {diagnostics} diagnostics',
 '{gyro_note} History retention: {days} days. Daily periods are local calendar days; weekly periods are ISO weeks from Monday through Sunday.': '{gyro_note} '
                                                                                                                                                'History '
                                                                                                                                                'retention: '
                                                                                                                                                '{days} '
                                                                                                                                                'days. '
                                                                                                                                                'Daily '
                                                                                                                                                'periods '
                                                                                                                                                'are '
                                                                                                                                                'local '
                                                                                                                                                'calendar '
                                                                                                                                                'days; '
                                                                                                                                                'weekly '
                                                                                                                                                'periods '
                                                                                                                                                'are '
                                                                                                                                                'ISO '
                                                                                                                                                'weeks '
                                                                                                                                                'from '
                                                                                                                                                'Monday '
                                                                                                                                                'through '
                                                                                                                                                'Sunday.',
 '{model} — Radiation monitoring report': '{model} — Radiation monitoring report',
 '{seconds} seconds ago': '{seconds} seconds ago',
 '{value:g} h': '{value:g} h',
 '{value:g} min': '{value:g} min',
 '{value} clock regressions observed': '{value} clock regressions observed',
 '{value} duplicate timestamps observed': '{value} duplicate timestamps observed',
 '{value} long intervals': '{value} long intervals',
 '{value} unusually short intervals': '{value} unusually short intervals',
 '{value} vs local baseline': '{value} vs local baseline',
 '{value}% time-window coverage': '{value}% time-window coverage'}

# Runtime presentation templates added in 7.1.4.
CATALOG.update({
    'Comparison confidence: {confidence}': 'Comparison confidence: {confidence}',
    'Confidence: {confidence}': 'Confidence: {confidence}',
    'Status': 'Status',
    'Typical background': 'Typical background',
    'Valid paired samples': 'Valid paired samples',
    'Warning from {warning:g} s; critical from {critical:g} s': 'Warning from {warning:g} s; critical from {critical:g} s',
    'valid hourly values · {days:.1f} days · {span:.1f} hPa': 'valid hourly values · {days:.1f} days · {span:.1f} hPa',
    '{a:+.1f}% / {b:+.1f}%': '{a:+.1f}% / {b:+.1f}%',
    '{b} × factor → {a}': '{b} × factor → {a}',
    '{content}': '{content}',
    '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)': '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)',
    '{days} days': '{days} days',
    '{dose:.3f} µSv/h': '{dose:.3f} µSv/h',
    '{first} {second}': '{first} {second}',
    '{from_value} → {to_value}': '{from_value} → {to_value}',
    '{note} · n={samples}': '{note} · n={samples}',
    '{pairs} valid paired samples': '{pairs} valid paired samples',
    '{pairs} valid paired samples · counting uncertainty {value:.2f}%': '{pairs} valid paired samples · counting uncertainty {value:.2f}%',
    '{probability:.0f}% estimated signal probability': '{probability:.0f}% estimated signal probability',
    '{span:.0f} {days_label} · {count} {daily_label}': '{span:.0f} {days_label} · {count} {daily_label}',
    '{start}–{end} °C · {samples} Samples': '{start}–{end} °C · {samples} samples',
    '{trend:+.1f} CPM': '{trend:+.1f} CPM',
    '{value:g} µSv/h': '{value:g} µSv/h',
    'Last uploaded CPM': 'Last uploaded CPM',
    'Last uploaded ACPM': 'Last uploaded ACPM',
    'GMCMap last uploaded ACPM': 'GMCMap last uploaded ACPM',
    'GMCMap ACPM accepted samples': 'GMCMap ACPM accepted samples',
    'ACPM is the average of all accepted CPM readings since the current app measurement session began.': 'ACPM is the average of all accepted CPM readings since the current app measurement session began.',
    'User manual': 'User manual',
    'Open user manual PDF': 'Open user manual PDF',
    'User manual is not available': 'User manual is not available',
})

# Version 8.2.1 report and history labels.
CATALOG.update({
    'Accepted measurements [count]': 'Accepted measurements [count]',
    'Local hour [h]': 'Local hour [h]',
    'Mean count rate [CPM]': 'Mean count rate [CPM]',
    'Radiation Monitoring': 'Radiation Monitoring',
    'Rejected raw value': 'Rejected raw value',
})


# Version 8.2.1 complete runtime localization.
CATALOG.update({
    'The recent level differs from counting noise with {probability:.2f}% statistical confidence': 'The recent level differs from counting noise with {probability:.2f}% statistical confidence',
    'A comparable or more extreme hourly level occurred about once in {rarity:.1f} historical hours': 'A comparable or more extreme hourly level occurred about once in {rarity:.1f} historical hours',
})

# Long-term analysis 9.1.1
CATALOG.update({'24 hours': '24 hours', '30 days': '30 days', '365 days': '365 days', '7 days': '7 days', '7-day rolling median': '7-day rolling median', '90 days': '90 days', '95% block-bootstrap interval for mean': '95% block-bootstrap interval for mean', '95% block-bootstrap interval for median': '95% block-bootstrap interval for median', 'Air-pressure association': 'Air-pressure association', 'Annual projection from the last 30 days: {value} µSv': 'Annual projection from the last 30 days: {value} µSv', 'Annual projection is not shown until a sufficiently complete 30-day period exists.': 'Annual projection is not shown until a sufficiently complete 30-day period exists.', 'Based on {hours} covered hours': 'Based on {hours} covered hours', 'Bootstrap uncertainty, distribution dispersion, EWMA and CUSUM': 'Bootstrap uncertainty, distribution dispersion, EWMA and CUSUM', 'Calendar heat map': 'Calendar heat map', 'Calendar heat map of daily median CPM': 'Calendar heat map of daily median CPM', 'Connected periods above the robust local long-term threshold': 'Connected periods above the robust local long-term threshold', 'Contextual Fano-like ratio; rolling CPM values are not independent Poisson counts': 'Contextual Fano-like ratio; rolling CPM values are not independent Poisson counts', 'Correlation does not prove causation.': 'Correlation does not prove causation.', 'Coverage {coverage}% · at least {required}% required': 'Coverage {coverage}% · at least {required}% required', 'Covered hours': 'Covered hours', 'Cumulative derived dose': 'Cumulative derived dose', 'Daily and monthly development': 'Daily and monthly development', 'Daily median': 'Daily median', 'Daily median and 7-day rolling median': 'Daily median and 7-day rolling median', 'Daily medians, rolling median and calendar view': 'Daily medians, rolling median and calendar view', 'Derived cumulative dose: {dose} µSv': 'Derived cumulative dose: {dose} µSv', 'Derived dose (µSv)': 'Derived dose (µSv)', 'Derived from the robust local background; not an official alarm threshold': 'Derived from the robust local background; not an official alarm threshold', 'Duration (h)': 'Duration (h)', 'EWMA, CUSUM, trend tests and relative event detection provide statistical context only. They do not identify a radiation source and do not replace calibrated radiation-protection measurements.': 'EWMA, CUSUM, trend tests and relative event detection provide statistical context only. They do not identify a radiation source and do not replace calibrated radiation-protection measurements.', 'Effective sample size': 'Effective sample size', 'Environmental correlations are exploratory. They may reflect common time patterns, ventilation, weather or other confounding factors and do not prove causation.': 'Environmental correlations are exploratory. They may reflect common time patterns, ventilation, weather or other confounding factors and do not prove causation.', 'Excess area (CPM·h)': 'Excess area (CPM·h)', 'Exploratory Spearman correlations at 0, 3, 6, 12 and 24 hour lags': 'Exploratory Spearman correlations at 0, 3, 6, 12 and 24 hour lags', 'Higher': 'Higher', 'Hourly dispersion ratio': 'Hourly dispersion ratio', 'Lagged environmental associations': 'Lagged environmental associations', 'Long-term analysis': 'Long-term analysis', 'Long-term analysis for {device}': 'Long-term analysis for {device}', 'Long-term background, cumulative dose, trend, recurring patterns and statistical process diagnostics': 'Long-term background, cumulative dose, trend, recurring patterns and statistical process diagnostics', 'Long-term overview': 'Long-term overview', 'Long-term statistical diagnostics': 'Long-term statistical diagnostics', 'Long-term trend': 'Long-term trend', 'Lower': 'Lower', 'Mann-Kendall test with Sen slope on sufficiently covered daily medians': 'Mann-Kendall test with Sen slope on sufficiently covered daily medians', 'Maximum CPM': 'Maximum CPM', 'Mean CPM': 'Mean CPM', 'Median CPM': 'Median CPM', 'Median {median} CPM · coverage {coverage}%': 'Median {median} CPM · coverage {coverage}%', 'Month': 'Month', 'Monthly aggregates': 'Monthly aggregates', 'Moving blocks preserve short-range time dependence': 'Moving blocks preserve short-range time dependence', 'No calendar data available': 'No calendar data available', 'No long-term analysis available yet': 'No long-term analysis available yet', 'No monthly aggregates available': 'No monthly aggregates available', 'No persistent CUSUM signal detected': 'No persistent CUSUM signal detected', 'No persistent EWMA signal detected': 'No persistent EWMA signal detected', 'No persistent relative elevation episodes detected': 'No persistent relative elevation episodes detected', 'No supported dose conversion for this period': 'No supported dose conversion for this period', 'No value is calculated until enough hourly pairs are available.': 'No value is calculated until enough hourly pairs are available.', 'Not enough daily values for a long-term chart': 'Not enough daily values for a long-term chart', 'Not enough paired data': 'Not enough paired data', 'Not yet meaningful': 'Not yet meaningful', 'Only {covered} of {required} days covered': 'Only {covered} of {required} days covered', 'Persistent elevation episodes': 'Persistent elevation episodes', 'Persistent episodes': 'Persistent episodes', 'Preliminary': 'Preliminary', 'Ready': 'Ready', 'Real time windows with duration and coverage checks': 'Real time windows with duration and coverage checks', 'Recent 7-day median relative to the robust long-term background': 'Recent 7-day median relative to the robust long-term background', 'Recent background deviation': 'Recent background deviation', 'Relative event threshold': 'Relative event threshold', 'Robust local background': 'Robust local background', 'Scientific interpretation': 'Scientific interpretation', 'Start': 'Start', 'Statistical signal detected': 'Statistical signal detected', 'Stored measurements are required before long-term statistics can be calculated.': 'Stored measurements are required before long-term statistics can be calculated.', 'Strongest at {lag} h lag · {pairs} pairs · {strength} association': 'Strongest at {lag} h lag · {pairs} pairs · {strength} association', 'Temperature association': 'Temperature association', 'The detector uses the robust long-term local background and does not replace radiation-safety alarms.': 'The detector uses the robust long-term local background and does not replace radiation-safety alarms.', 'Time at or above configured danger threshold': 'Time at or above configured danger threshold', 'Time in configured warning range': 'Time in configured warning range', 'Typical range P05–P95: {low}–{high} CPM': 'Typical range P05–P95: {low}–{high} CPM', 'moderate': 'moderate', 'strong': 'strong', 'weak': 'weak', '{date}: median {median} CPM, coverage {coverage}%': '{date}: median {median} CPM, coverage {coverage}%', '{direction} · {slope} CPM/day · p={p}': '{direction} · {slope} CPM/day · p={p}', '{hours} covered hours': '{hours} covered hours', '{hours} total elevated hours · longest {longest} h': '{hours} total elevated hours · longest {longest} h', '{observed} daily observations · correlation duration {duration} days': '{observed} daily observations · correlation duration {duration} days', '{replicates} replicates · block length {block} days': '{replicates} replicates · block length {block} days', 'Long-term': 'Long-term', 'stable': 'stable', 'increasing': 'increasing', 'decreasing': 'decreasing'})

# Recent baseline wording 9.1.1
CATALOG.update({'Recent baseline context': 'Recent baseline context', 'Seven-day baseline deviation, drift and sustained relative events': 'Seven-day baseline deviation, drift and sustained relative events'})


# Extended agreement and seasonal analysis 9.1.1
CATALOG.update({'Bland-Altman bias': 'Bland-Altman bias', '95% limits of agreement': '95% limits of agreement', 'Mean signed difference A minus B': 'Mean signed difference A minus B', 'Exploratory paired-device agreement; correlation alone does not establish agreement.': 'Exploratory paired-device agreement; correlation alone does not establish agreement.', 'Seasonal month-of-year profile': 'Seasonal month-of-year profile', 'Median CPM by calendar month across available years': 'Median CPM by calendar month across available years', 'Calendar month': 'Calendar month', 'Days represented': 'Days represented', 'Not enough months for a seasonal profile': 'Not enough months for a seasonal profile', 'At least six represented calendar months are required.': 'At least six represented calendar months are required.', 'Exploratory seasonal summary; it does not separate weather, location, detector or calibration changes.': 'Exploratory seasonal summary; it does not separate weather, location, detector or calibration changes.'})


# Evidence-based long-term presentation and field-test diagnostics 10.0.0
CATALOG.update({'{available} of {required} required hourly pairs are available.': '{available} of {required} required hourly pairs are available.', 'FDR-adjusted p={value}': 'FDR-adjusted p={value}', 'Practical magnitude not available': 'Practical magnitude not available', 'Moderate practical magnitude': 'Moderate practical magnitude', 'Estimated change {value}% per month · {magnitude}': 'Estimated change {value}% per month · {magnitude}', 'Runtime since service start': 'Runtime since service start', 'Cumulative counters reset when the service restarts.': 'Cumulative counters reset when the service restarts.', 'GMCMap transmission': 'GMCMap transmission', 'Export field-test protocol (JSON)': 'Export field-test protocol (JSON)', '{months} represented calendar months': '{months} represented calendar months', 'Statistical process diagnostics': 'Statistical process diagnostics', 'At least 30 sufficiently complete days and an adequate effective sample size are required.': 'At least 30 sufficiently complete days and an adequate effective sample size are required.', '{success} successful · {errors} failed uploads': '{success} successful · {errors} failed uploads', 'No statistically clear long-term trend is visible': 'No statistically clear long-term trend is visible', 'Longest data gap': 'Longest data gap', 'Stored samples: {count}': 'Stored samples: {count}', 'Field-test interpretation': 'Field-test interpretation', 'A falling long-term tendency is visible': 'A falling long-term tendency is visible', 'Large practical magnitude': 'Large practical magnitude', '{days} covered days · {observed} daily observations': '{days} covered days · {observed} daily observations', 'Data basis': 'Data basis', 'A rising long-term tendency is visible': 'A rising long-term tendency is visible', 'Small practical magnitude': 'Small practical magnitude', 'Current background context': 'Current background context', 'Annual projection from the last 90 days: {value} µSv': 'Annual projection from the last 90 days: {value} µSv', 'The main result first; method details remain available below.': 'The main result first; method details remain available below.', 'Annual projection is not shown until a sufficiently complete 90-day period exists.': 'Annual projection is not shown until a sufficiently complete 90-day period exists.', 'Supported': 'Supported', 'Well supported': 'Well supported', 'Extended statistical methods': 'Extended statistical methods', 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.': 'Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.', 'USB / serial recovery': 'USB / serial recovery', 'Database write errors': 'Database write errors', 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.': 'These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.', 'Plain-language assessment': 'Plain-language assessment', '{errors} serial errors · {reconnects} reconnects': '{errors} serial errors · {reconnects} reconnects', 'Long-term reliability field test': 'Long-term reliability field test', 'No reliable long-term trend can be assessed yet': 'No reliable long-term trend can be assessed yet', 'Operational counters for USB, database continuity and GMCMap transmission': 'Operational counters for USB, database continuity and GMCMap transmission', 'EWMA, CUSUM and dispersion diagnostics; statistical context only': 'EWMA, CUSUM and dispersion diagnostics; statistical context only', '{count} detected gaps above the expected interval': '{count} detected gaps above the expected interval', 'Trend method details': 'Trend method details', 'FDR-adjusted significance not available': 'FDR-adjusted significance not available', 'Exploratory Spearman correlations with false-discovery-rate correction': 'Exploratory Spearman correlations with false-discovery-rate correction', 'Seasonal assessment': 'Seasonal assessment', 'Not evaluable': 'Not evaluable', 'Integrated derived dose in the measured period': 'Integrated derived dose in the measured period', 'Exploratory': 'Exploratory', 'Confidence intervals, effective sample size, test statistics and practical effect size': 'Confidence intervals, effective sample size, test statistics and practical effect size', 'Very small practical magnitude': 'Very small practical magnitude'})
