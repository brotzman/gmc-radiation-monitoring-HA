from __future__ import annotations

CATALOG: dict[str, str] = {'1 h counting uncertainty': '1 h counting uncertainty',
 '1 h coverage': 'Pokrycie 1 h',
 '1 h mean': 'Średnia 1 h',
 '1 h mean / 7 d mean × 100': 'Średnia 1 h / średnia 7 dni × 100',
 '1 h mean dose rate': 'Średnia moc dawki z 1 h',
 '1 h mean minus 7 d baseline': 'Średnia 1 h minus poziom bazowy 7 dni',
 '24 h Fano factor': 'Współczynnik Fano z 24 h',
 '24 h P95': 'P95 z 24 h',
 '24 h P99': 'P99 z 24 h',
 '24 h Z-score': 'Wynik Z z 24 h',
 '24 h counting uncertainty': '24 h counting uncertainty',
 '24 h distribution, percentiles and latest-value deviation': 'Rozkład 24 h, percentyle i odchylenie ostatniej '
                                                              'wartości',
 '24 h maximum': 'Maksimum z 24 h',
 '24 h mean': 'Średnia z 24 h',
 '24 h mean dose rate': 'Średnia moc dawki z 24 h',
 '24 h median': 'Mediana z 24 h',
 '24 h minimum': 'Minimum z 24 h',
 '24 h standard deviation': 'Odchylenie standardowe z 24 h',
 '50th percentile': '50. percentyl',
 '7 d baseline': 'Poziom odniesienia 7 d',
 '7 d baseline dose rate': 'Moc dawki bazowej z 7 dni',
 '7 d baseline drift': 'Dryf bazowy z 7 dni',
 '7 d counting uncertainty': '7 d counting uncertainty',
 '7-day smoothed daily median': 'Dzienna mediana wygładzona w okresie 7 dni',
 '95th percentile': '95. percentyl',
 '99th percentile': '99. percentyl',
 'A device function is temporarily unavailable.': 'Funkcja urządzenia jest tymczasowo niedostępna.',
 'A fresh backup is recommended before deletion.': 'A fresh backup is recommended before deletion.',
 'A recent position change can affect comparability': 'Niedawna zmiana położenia może wpływać na porównywalność',
 'Above the typical time profile': 'Powyżej typowego profilu czasowego',
 'Above the usual local range': 'Powyżej zwykłego lokalnego zakresu',
 'Absolute radiation assessment': 'Bezwzględna ocena promieniowania',
 'Absolute thresholds and local anomaly detection answer different questions.': 'Progi bezwzględne i lokalne '
                                                                                'wykrywanie anomalii odpowiadają na '
                                                                                'różne pytania.',
 'Acceleration magnitude': 'Wartość przyspieszenia',
 'Acceleration raw values': 'Surowe wartości przyspieszenia',
 'Accepted device values are stored separately after live CPM plausibility confirmation': 'Accepted device values are '
                                                                                          'stored separately after '
                                                                                          'live CPM plausibility '
                                                                                          'confirmation',
 'Active threshold profile': 'Aktywny profil progów',
 'Adaptive background profile': 'Adaptacyjny profil tła',
 'Advanced': 'Zaawansowany',
 'Advanced diagnostics': 'Zaawansowana diagnostyka',
 'Advanced visuals': 'Zaawansowane wizualizacje',
 'Affected GMC devices': 'Affected GMC devices',
 'Agreement': 'Zgodność',
 'Air-pressure source': 'Źródło ciśnienia atmosferycznego',
 'Air-pressure trend': 'Trend ciśnienia atmosferycznego',
 'All GMC history was deleted': 'All GMC history was deleted',
 'All baselines and comparisons use the same robust quality-filtered measurements.': 'Wszystkie poziomy odniesienia i '
                                                                                     'porównania używają tych samych '
                                                                                     'odpornych pomiarów filtrowanych '
                                                                                     'jakościowo.',
 'All connected GMC devices': 'Wszystkie podłączone urządzenia GMC',
 'All devices': 'Wszystkie urządzenia',
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
 'All statistical values, confidence intervals and diagnostics': 'Wszystkie wartości statystyczne, przedziały ufności '
                                                                 'i diagnostyka',
 'All {count} known GMC devices are connected': 'All {count} known GMC devices are connected',
 'Allow restore': 'Zezwól na przywracanie',
 'Already assigned to {name}': 'Already assigned to {name}',
 'Analysis': 'Analiza',
 'Analysis JSON': 'JSON analizy',
 'Analysis PDF': 'PDF analizy',
 'Analysis depth': 'Poziom analizy',
 'Analysis for': 'Analiza dla',
 'Analysis is still being prepared': 'Analysis is still being prepared',
 'Analysis shown': 'Analiza jest wyświetlana',
 'Analysis, the traffic light and downloads will become meaningful after the first stored samples arrive.': 'Analiza, '
                                                                                                            'sygnalizacja '
                                                                                                            'i pliki '
                                                                                                            'do '
                                                                                                            'pobrania '
                                                                                                            'staną się '
                                                                                                            'miarodajne '
                                                                                                            'po '
                                                                                                            'zapisaniu '
                                                                                                            'pierwszych '
                                                                                                            'pomiarów.',
 'Analyze this device': 'Analizuj to urządzenie',
 'Another report is already being generated': 'Inny raport jest już generowany',
 'Another report or maintenance job is running': 'Another report or maintenance job is running',
 'Another report or restore job is running': 'Inny raport lub przywracanie jest już w toku',
 'Another report, maintenance export, or restore job is running': 'Inny raport, eksport konserwacyjny lub proces '
                                                                  'przywracania jest już uruchomiony.',
 'App Started At': 'Aplikacja uruchomiona o',
 'Apply': 'Apply',
 'Assessment': 'Ocena',
 'Assigned': 'Assigned',
 'At least 24 h reference and 6 h persistence are required': 'At least 24 h reference and 6 h persistence are required',
 'At least two daily background values are required.': 'Wymagane są co najmniej dwie dzienne wartości tła.',
 'At least {count} valid hourly values are required': 'Wymagane jest co najmniej {count} prawidłowych wartości '
                                                      'godzinowych',
 'At least {count} valid pairs are required': 'Wymagane jest co najmniej {count} prawidłowych par',
 'At least {days} days of learning data are required': 'Wymagane jest co najmniej {days} dni danych uczących',
 'At least {span:g} hPa pressure variation is required': 'Wymagana jest zmienność ciśnienia co najmniej {span:g} hPa',
 'At the same time, the value is clearly above the usual local background. Review the trend and measurement conditions.': 'Jednocześnie '
                                                                                                                          'wartość '
                                                                                                                          'jest '
                                                                                                                          'wyraźnie '
                                                                                                                          'wyższa '
                                                                                                                          'od '
                                                                                                                          'zwykłego '
                                                                                                                          'lokalnego '
                                                                                                                          'tła. '
                                                                                                                          'Sprawdź '
                                                                                                                          'trend '
                                                                                                                          'i '
                                                                                                                          'warunki '
                                                                                                                          'pomiaru.',
 'Automatic device detection is running': 'Automatic device detection is running',
 'Automatic refresh is temporarily unavailable': 'Automatic refresh is temporarily unavailable',
 'Availability': 'Dostępność',
 'Available': 'Available',
 'Back to analysis': 'Back to analysis',
 'Background index': 'Indeks tła',
 'Background index compares the rolling 1 h mean with the available 7 d baseline.': 'Indeks tła = krocząca średnia 1 h '
                                                                                    'względem dostępnego 7-dniowego '
                                                                                    'poziomu bazowego.',
 'Background index formula explanation': 'Indeks tła = krocząca średnia 1 h względem dostępnego 7-dniowego poziomu '
                                         'bazowego.',
 'Background trend over days and months': 'Zmiana tła w ciągu dni i miesięcy',
 'Backup is compatible and ready to restore.': 'Backup is compatible and ready to restore.',
 'Backup preview failed': 'Backup preview failed',
 'Baseline available': 'Poziom bazowy dostępny',
 'Baseline currently stable': 'Poziom odniesienia jest obecnie stabilny',
 'Baseline deviation': 'Odchylenie od poziomu odniesienia',
 'Baseline deviation, drift and sustained relative events': 'Odchylenie i dryf poziomu odniesienia oraz utrzymujące '
                                                            'się zdarzenia względne',
 'Baseline deviation: {cpm} CPM ({percent}%)': 'Odchylenie od poziomu bazowego: {cpm} CPM ({percent}%)',
 'Baseline drift: {value}%': 'Dryf poziomu bazowego: {value}%',
 'Baseline learning in progress': 'Trwa uczenie poziomu bazowego',
 'Baseline readiness': 'Gotowość poziomu bazowego',
 'Baseline: {value} CPM': 'Poziom bazowy: {value} CPM',
 'Battery voltage': 'Napięcie baterii',
 'Baud rate': 'Szybkość transmisji',
 'Below the typical time profile': 'Poniżej typowego profilu czasowego',
 'Below warning threshold': 'Poniżej progu ostrzegawczego',
 'BfS and ICRP reference profiles convert annual dose values into continuous-rate equivalents for context. They are not official instantaneous alarm limits and cannot replace professional dose assessment.': 'Profile '
                                                                                                                                                                                                               'referencyjne '
                                                                                                                                                                                                               'BfS '
                                                                                                                                                                                                               'i '
                                                                                                                                                                                                               'ICRP '
                                                                                                                                                                                                               'przeliczają '
                                                                                                                                                                                                               'dawki '
                                                                                                                                                                                                               'roczne '
                                                                                                                                                                                                               'na '
                                                                                                                                                                                                               'równoważne '
                                                                                                                                                                                                               'ciągłe '
                                                                                                                                                                                                               'moce '
                                                                                                                                                                                                               'dawki '
                                                                                                                                                                                                               'wyłącznie '
                                                                                                                                                                                                               'dla '
                                                                                                                                                                                                               'kontekstu. '
                                                                                                                                                                                                               'Nie '
                                                                                                                                                                                                               'są '
                                                                                                                                                                                                               'oficjalnymi '
                                                                                                                                                                                                               'natychmiastowymi '
                                                                                                                                                                                                               'progami '
                                                                                                                                                                                                               'alarmowymi '
                                                                                                                                                                                                               'i '
                                                                                                                                                                                                               'nie '
                                                                                                                                                                                                               'zastępują '
                                                                                                                                                                                                               'profesjonalnej '
                                                                                                                                                                                                               'oceny '
                                                                                                                                                                                                               'dawki.',
 'BfS reference projection': 'Projekcja referencyjna BfS',
 'Both connected counters show a quality-filtered simultaneous rise': 'Oba podłączone liczniki pokazują jednoczesny '
                                                                      'wzrost po filtracji jakościowej',
 'Both connected counters show a simultaneous rise': 'Oba podłączone liczniki wykazują jednoczesny wzrost',
 'Broadly compatible with Poisson-like spread': 'Ogólnie zgodne z rozrzutem typu Poissona',
 'CPM': 'CPM',
 'CPM and derived dose rate': 'CPM i wyliczona moc dawki',
 'CPM distribution and Poisson comparison': 'Rozkład CPM i porównanie Poissona',
 'CPM distribution — {title}': 'Rozkład CPM — {title}',
 'CPM is the primary measurement.': 'CPM jest podstawową wartością pomiarową.',
 'CPM per µSv/h': 'CPM na µSv/h',
 'CPM quality': 'Jakość CPM',
 'CPM statistics  min {minimum:.0f} | max {maximum:.0f} | mean {mean:.2f} | median {median:.2f} | SD {sd:.2f} | P95 {p95:.2f} | missing {missing}': 'Statystyki '
                                                                                                                                                    'CPM  '
                                                                                                                                                    'min '
                                                                                                                                                    '{minimum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'maks '
                                                                                                                                                    '{maximum:.0f} '
                                                                                                                                                    '| '
                                                                                                                                                    'średnia '
                                                                                                                                                    '{mean:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'mediana '
                                                                                                                                                    '{median:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'SD '
                                                                                                                                                    '{sd:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'P95 '
                                                                                                                                                    '{p95:.2f} '
                                                                                                                                                    '| '
                                                                                                                                                    'brakujące '
                                                                                                                                                    '{missing}',
 'CPM statistics: no accepted measurements in selected period': 'Statystyki CPM: brak zaakceptowanych pomiarów w '
                                                                'wybranym okresie',
 'CPM–pressure correlation': 'Korelacja CPM–ciśnienie',
 'CPM–temperature correlation': 'Korelacja CPM–temperatura',
 'CPM–voltage correlation': 'Korelacja CPM–napięcie',
 'CSV files preserve every accepted measurement without interpolation. PNG reports include CPM, temperature, voltage, optional raw signed gyro diagnostics, summary statistics, sample completeness, device identity, timezone, period and generation time. ZIP bundles additionally contain analysis JSON, daily summaries, events, histogram, heatmap and a multi-page PDF report.': 'Pliki '
                                                                                                                                                                                                                                                                                                                                                                                       'CSV '
                                                                                                                                                                                                                                                                                                                                                                                       'zachowują '
                                                                                                                                                                                                                                                                                                                                                                                       'każdy '
                                                                                                                                                                                                                                                                                                                                                                                       'zaakceptowany '
                                                                                                                                                                                                                                                                                                                                                                                       'pomiar '
                                                                                                                                                                                                                                                                                                                                                                                       'bez '
                                                                                                                                                                                                                                                                                                                                                                                       'interpolacji. '
                                                                                                                                                                                                                                                                                                                                                                                       'Raporty '
                                                                                                                                                                                                                                                                                                                                                                                       'PNG '
                                                                                                                                                                                                                                                                                                                                                                                       'zawierają '
                                                                                                                                                                                                                                                                                                                                                                                       'CPM, '
                                                                                                                                                                                                                                                                                                                                                                                       'temperaturę, '
                                                                                                                                                                                                                                                                                                                                                                                       'napięcie, '
                                                                                                                                                                                                                                                                                                                                                                                       'opcjonalną '
                                                                                                                                                                                                                                                                                                                                                                                       'surową '
                                                                                                                                                                                                                                                                                                                                                                                       'diagnostykę '
                                                                                                                                                                                                                                                                                                                                                                                       'żyroskopu '
                                                                                                                                                                                                                                                                                                                                                                                       'ze '
                                                                                                                                                                                                                                                                                                                                                                                       'znakiem, '
                                                                                                                                                                                                                                                                                                                                                                                       'statystyki '
                                                                                                                                                                                                                                                                                                                                                                                       'podsumowujące, '
                                                                                                                                                                                                                                                                                                                                                                                       'kompletność, '
                                                                                                                                                                                                                                                                                                                                                                                       'tożsamość '
                                                                                                                                                                                                                                                                                                                                                                                       'urządzenia, '
                                                                                                                                                                                                                                                                                                                                                                                       'strefę '
                                                                                                                                                                                                                                                                                                                                                                                       'czasową, '
                                                                                                                                                                                                                                                                                                                                                                                       'okres '
                                                                                                                                                                                                                                                                                                                                                                                       'i '
                                                                                                                                                                                                                                                                                                                                                                                       'czas '
                                                                                                                                                                                                                                                                                                                                                                                       'utworzenia. '
                                                                                                                                                                                                                                                                                                                                                                                       'Pakiety '
                                                                                                                                                                                                                                                                                                                                                                                       'ZIP '
                                                                                                                                                                                                                                                                                                                                                                                       'dodatkowo '
                                                                                                                                                                                                                                                                                                                                                                                       'zawierają '
                                                                                                                                                                                                                                                                                                                                                                                       'JSON '
                                                                                                                                                                                                                                                                                                                                                                                       'analizy, '
                                                                                                                                                                                                                                                                                                                                                                                       'podsumowania '
                                                                                                                                                                                                                                                                                                                                                                                       'dzienne, '
                                                                                                                                                                                                                                                                                                                                                                                       'zdarzenia, '
                                                                                                                                                                                                                                                                                                                                                                                       'histogram, '
                                                                                                                                                                                                                                                                                                                                                                                       'mapę '
                                                                                                                                                                                                                                                                                                                                                                                       'cieplną '
                                                                                                                                                                                                                                                                                                                                                                                       'i '
                                                                                                                                                                                                                                                                                                                                                                                       'wielostronicowy '
                                                                                                                                                                                                                                                                                                                                                                                       'raport '
                                                                                                                                                                                                                                                                                                                                                                                       'PDF.',
 'Calibrated acceleration': 'Skalibrowane przyspieszenie',
 'Calibration profile': 'Profil kalibracji',
 'Capabilities': 'Możliwości',
 'Check location, orientation and environmental conditions when a persistent jump appears.': 'Gdy pojawi się trwały '
                                                                                             'skok, sprawdź położenie, '
                                                                                             'orientację i warunki '
                                                                                             'otoczenia.',
 'Check manually': 'Sprawdź ręcznie',
 'Check the Home Assistant general settings and restart the add-on.': 'Sprawdź ogólne ustawienia Home Assistant i '
                                                                      'uruchom dodatek ponownie.',
 'Check the USB cable and power supply if this continues for more than 15 minutes.': 'Sprawdź przewód USB i zasilanie, '
                                                                                     'jeśli stan utrzymuje się dłużej '
                                                                                     'niż 15 minut.',
 'Check the measurement conditions, observe the trend and verify the reading with an appropriate instrument if it persists.': 'Sprawdź '
                                                                                                                              'warunki '
                                                                                                                              'pomiaru, '
                                                                                                                              'obserwuj '
                                                                                                                              'trend '
                                                                                                                              'i '
                                                                                                                              'potwierdź '
                                                                                                                              'odczyt '
                                                                                                                              'odpowiednim '
                                                                                                                              'przyrządem, '
                                                                                                                              'jeśli '
                                                                                                                              'podwyższenie '
                                                                                                                              'się '
                                                                                                                              'utrzymuje.',
 'Check the measurement location': 'Sprawdź miejsce pomiaru',
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
 'Choose how much detail the analysis cards show. The selection is stored in this browser.': 'Wybierz poziom '
                                                                                             'szczegółowości kart '
                                                                                             'analizy. Wybór jest '
                                                                                             'zapisywany w tej '
                                                                                             'przeglądarce.',
 'Choose whether reports include all devices or one selected device.': 'Wybierz, czy raporty mają obejmować wszystkie '
                                                                       'urządzenia, czy jedno wybrane urządzenie.',
 'Clear': 'Clear',
 'Clearly above the usual local range': 'Wyraźnie powyżej zwykłego lokalnego zakresu',
 'Clearly elevated': 'Wyraźnie podwyższone',
 'Clearly elevated: clearly above the usual local range': 'Wyraźnie podwyższone: wyraźnie powyżej zwykłego lokalnego '
                                                          'zakresu',
 'Clock offset exceeds warning threshold': 'Odchylenie zegara przekracza próg ostrzegawczy',
 'Clock synchronized': 'Zegar zsynchronizowany',
 'Close to Poisson expectation': 'Blisko oczekiwania Poissona',
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
 'Compared with local baseline': 'W porównaniu z lokalnym poziomem odniesienia',
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
 'Compares the current value with the usual background at this location.': 'Porównuje bieżącą wartość ze zwykłym tłem '
                                                                           'w tej lokalizacji.',
 'Comparison confidence': 'Wiarygodność porównania',
 'Complete ZIP bundle': 'Pełny pakiet ZIP',
 'Complete history deletion failed': 'Complete history deletion failed',
 'Complete history deletion is disabled in the app configuration.': 'Pełne usuwanie historii jest wyłączone w '
                                                                    'konfiguracji aplikacji.',
 'Completeness: {value:.2f}%': 'Kompletność: {value:.2f}%',
 'Confidence': 'Poziom ufności',
 'Configured CPM conversion factor': 'Skonfigurowany współczynnik przeliczeniowy CPM',
 'Configured baud rate': 'Skonfigurowana szybkość transmisji',
 'Configured device name': 'Skonfigurowana nazwa urządzenia',
 'Configured location': 'Skonfigurowana lokalizacja',
 'Configured measurement interval': 'Skonfigurowany interwał pomiaru',
 'Confirmed original samples in 24 h · {accepted} stored': 'Confirmed original samples in 24 h · {accepted} stored',
 'Connect two devices to enable comparison.': 'Podłącz dwa urządzenia, aby włączyć porównanie.',
 'Connect two devices to learn a relative response factor.': 'Connect two devices to learn a relative response factor.',
 'Connected GMC devices': 'Podłączone urządzenia GMC',
 'Connected counters without an active stability warning': 'Połączone liczniki bez aktywnego ostrzeżenia o stabilności',
 'Connected devices': 'Podłączone urządzenia',
 'Connection active': 'Connection active',
 'Consecutive upload errors': 'Kolejne błędy wysyłania',
 'Continue observing': 'Kontynuuj obserwację',
 'Coordinates': 'Współrzędne',
 'Correlation': 'Korelacja',
 'Correlation does not imply causation. Strong values should be investigated over longer periods before drawing conclusions.': 'Korelacja '
                                                                                                                               'nie '
                                                                                                                               'oznacza '
                                                                                                                               'związku '
                                                                                                                               'przyczynowego. '
                                                                                                                               'Silne '
                                                                                                                               'wartości '
                                                                                                                               'należy '
                                                                                                                               'badać '
                                                                                                                               'przez '
                                                                                                                               'dłuższy '
                                                                                                                               'czas '
                                                                                                                               'przed '
                                                                                                                               'wyciągnięciem '
                                                                                                                               'wniosków.',
 'Cosmic influence is possible': 'Możliwy wpływ kosmiczny',
 'Cosmic influence – statistical indication': 'Wpływ kosmiczny – wskazanie statystyczne',
 'Counter ID': 'Identyfikator licznika',
 'Counting statistics': 'Statystyki zliczeń',
 'Counting uncertainty (68%): −{minus:.2f}/+{plus:.2f} CPM · {impulses} impulses in {duration}': 'Counting uncertainty '
                                                                                                 '(68%): '
                                                                                                 '−{minus:.2f}/+{plus:.2f} '
                                                                                                 'CPM · {impulses} '
                                                                                                 'impulses in '
                                                                                                 '{duration}',
 'Counting uncertainty not available': 'Counting uncertainty not available',
 'Country': 'Kraj',
 'Coverage percent': 'Pokrycie procentowe',
 'Coverage, gaps, runtime counters and derived dose-rate values': 'Pokrycie, luki, liczniki działania i wyliczone '
                                                                  'wartości mocy dawki',
 'Critical': 'Krytyczny',
 'Critical: danger threshold exceeded': 'Krytyczny: przekroczono próg zagrożenia',
 'Current': 'Aktualnie',
 'Current air pressure': 'Aktualne ciśnienie atmosferyczne',
 'Current database size': 'Current database size',
 'Current difference': 'Bieżąca różnica',
 'Current value': 'Bieżąca wartość',
 'Current value is {z:+.2f} robust standard deviations from the 24 h median': 'Bieżąca wartość jest oddalona o '
                                                                              '{z:+.2f} odpornych odchyleń '
                                                                              'standardowych od mediany 24 h',
 'Current value is {z:+.2f} standard deviations from the 24 h mean': 'Bieżąca wartość jest oddalona o {z:+.2f} '
                                                                     'odchylenia standardowego od średniej '
                                                                     '24-godzinnej',
 'Current week bundle': 'Pakiet bieżącego tygodnia',
 'Currently selected': 'Aktualnie wybrane',
 'Custom period': 'Własny okres',
 'Custom thresholds': 'Niestandardowe progi',
 'Daily and weekly profile is still being formed': 'Profil dzienny i tygodniowy jest nadal tworzony',
 'Daily quality-filtered medians are smoothed over seven days. The period cards compare the recent part of each period with the preceding part; detected jumps are statistical changes and do not determine their cause.': 'Dzienne '
                                                                                                                                                                                                                           'mediany '
                                                                                                                                                                                                                           'po '
                                                                                                                                                                                                                           'filtracji '
                                                                                                                                                                                                                           'jakościowej '
                                                                                                                                                                                                                           'są '
                                                                                                                                                                                                                           'wygładzane '
                                                                                                                                                                                                                           'w '
                                                                                                                                                                                                                           'okresie '
                                                                                                                                                                                                                           'siedmiu '
                                                                                                                                                                                                                           'dni. '
                                                                                                                                                                                                                           'Karty '
                                                                                                                                                                                                                           'okresów '
                                                                                                                                                                                                                           'porównują '
                                                                                                                                                                                                                           'nowszą '
                                                                                                                                                                                                                           'część '
                                                                                                                                                                                                                           'każdego '
                                                                                                                                                                                                                           'okresu '
                                                                                                                                                                                                                           'z '
                                                                                                                                                                                                                           'poprzednią; '
                                                                                                                                                                                                                           'wykryte '
                                                                                                                                                                                                                           'skoki '
                                                                                                                                                                                                                           'są '
                                                                                                                                                                                                                           'zmianami '
                                                                                                                                                                                                                           'statystycznymi '
                                                                                                                                                                                                                           'i '
                                                                                                                                                                                                                           'nie '
                                                                                                                                                                                                                           'określają '
                                                                                                                                                                                                                           'ich '
                                                                                                                                                                                                                           'przyczyny.',
 'Daily summary CSV': 'CSV podsumowania dziennego',
 'Danger threshold exceeded': 'Przekroczono próg zagrożenia',
 'Danger thresholds': 'Progi zagrożenia',
 'Danger zone': 'Danger zone',
 'Dashboard navigation': 'Dashboard navigation',
 'Data exports': 'Eksport danych',
 'Data period': 'Data period',
 'Data quality': 'Jakość danych',
 'Data quality is too low for a reliable assessment': 'Jakość danych jest zbyt niska do wiarygodnej oceny',
 'Data quality status unavailable': 'Stan jakości danych niedostępny',
 'Data quality: {value}': 'Jakość danych: {value}',
 'Database': 'Database',
 'Database health': 'Stan bazy danych',
 'Database size': 'Rozmiar bazy',
 'Date': 'Data',
 'Delete all GMC history': 'Delete all GMC history',
 'Delete history': 'Delete history',
 'Deletion confirmation text must be exactly DELETE ALL GMC HISTORY': 'Deletion confirmation text must be exactly '
                                                                      'DELETE ALL GMC HISTORY',
 'Deletion is disabled by default.': 'Deletion is disabled by default.',
 'Derived dose rate': 'Wyliczona moc dawki',
 'Derived from 1 h mean CPM': 'Wyliczone ze średniej CPM z 1 h',
 'Derived from 24 h mean CPM': 'Wyliczone ze średniej CPM z 24 h',
 'Derived from 7 d mean CPM': 'Wyliczone ze średniej CPM z 7 dni',
 'Derived from latest CPM': 'Wyliczone z ostatniej wartości CPM',
 'Detailed interpretation and the most useful supporting values': 'Szczegółowa interpretacja i najważniejsze wartości '
                                                                  'pomocnicze',
 'Detect, identify and assign GMC counters': 'Detect, identify and assign GMC counters',
 'Detected': 'Wykryto',
 'Detected Capabilities': 'Wykryte możliwości',
 'Detected GMC device': 'Detected GMC device',
 'Detected baseline jumps': 'Wykryte skoki poziomu bazowego',
 'Detected relative anomaly events: {count}': 'Wykryte względne zdarzenia anomalne: {count}',
 'Deviation': 'Odchylenie',
 'Device': 'Urządzenie',
 'Device Profile': 'Profil urządzenia',
 'Device Time Errors Since Start': 'Błędy czasu urządzenia od uruchomienia',
 'Device assignments saved': 'Device assignments saved',
 'Device assignments were saved.': 'Device assignments were saved.',
 'Device baseline': 'Poziom odniesienia urządzenia',
 'Device capabilities': 'Funkcje urządzenia',
 'Device clock': 'Zegar urządzenia',
 'Device clock offset': 'Odchylenie zegara urządzenia',
 'Device clock status': 'Stan zegara urządzenia',
 'Device clock unavailable': 'Zegar urządzenia niedostępny',
 'Device clock warning': 'Device clock warning',
 'Device comparison': 'Porównanie urządzeń',
 'Device details, live values and analysis selection are shown below.': 'Poniżej znajdują się szczegóły urządzeń, '
                                                                        'bieżące wartości i wybór urządzenia do '
                                                                        'analizy.',
 'Device health warning': 'Device health warning',
 'Device position': 'Położenie urządzenia',
 'Device status updated': 'Device status updated',
 'Device temperature is unavailable.': 'Temperatura urządzenia jest niedostępna.',
 'Device time': 'Czas urządzenia',
 'Device-specific details are listed above.': 'Szczegóły poszczególnych urządzeń znajdują się w sekcji powyżej.',
 'Device: {value}': 'Urządzenie: {value}',
 'Devices': 'Devices',
 'Diagnostics JSON': 'JSON diagnostyczny',
 'Disabled': 'Wyłączone',
 'Discarded CPM peaks': 'Discarded CPM peaks',
 'Discarded unconfirmed CPM peaks': 'Discarded unconfirmed CPM peaks',
 'Display down': 'Płasko, ekran do dołu',
 'Display up': 'Płasko, ekran do góry',
 'Dose rate = CPM / configured conversion factor ({factor:g} CPM per µSv/h).': 'Moc dawki = CPM / skonfigurowany '
                                                                               'współczynnik przeliczeniowy '
                                                                               '({factor:g} CPM na µSv/h).',
 'Dose rate formula explanation': 'Moc dawki = CPM / skonfigurowany współczynnik przeliczeniowy ({factor:g} CPM na '
                                  'µSv/h).',
 'Dose-rate values are derived from CPM using the configured conversion factor.': 'Wartości mocy dawki są wyliczane z '
                                                                                  'CPM przy użyciu skonfigurowanego '
                                                                                  'współczynnika przeliczeniowego.',
 'Dose-rate values, traffic-light states and events are derived indicators. CPM remains the primary measurement.': 'Wartości '
                                                                                                                   'mocy '
                                                                                                                   'dawki, '
                                                                                                                   'stany '
                                                                                                                   'sygnalizacji '
                                                                                                                   'i '
                                                                                                                   'zdarzenia '
                                                                                                                   'są '
                                                                                                                   'wskaźnikami '
                                                                                                                   'pochodnymi. '
                                                                                                                   'CPM '
                                                                                                                   'pozostaje '
                                                                                                                   'podstawową '
                                                                                                                   'wartością '
                                                                                                                   'pomiarową.',
 'Download': 'Pobierz',
 'Downloads': 'Pobieranie',
 'Dual-tube measurement': 'Pomiar dwutubowy',
 'Duration [s]': 'Czas trwania [s]',
 'During the learning phase, leave the counters in a stable location and allow additional measurements to accumulate.': 'W '
                                                                                                                        'fazie '
                                                                                                                        'uczenia '
                                                                                                                        'pozostaw '
                                                                                                                        'liczniki '
                                                                                                                        'w '
                                                                                                                        'stałym '
                                                                                                                        'miejscu '
                                                                                                                        'i '
                                                                                                                        'pozwól '
                                                                                                                        'zgromadzić '
                                                                                                                        'więcej '
                                                                                                                        'pomiarów.',
 'Each device has its own MQTT identity and history. The cards show the latest accepted measurement.': 'Każde '
                                                                                                       'urządzenie ma '
                                                                                                       'własną '
                                                                                                       'tożsamość MQTT '
                                                                                                       'i historię. '
                                                                                                       'Karty pokazują '
                                                                                                       'ostatni '
                                                                                                       'zaakceptowany '
                                                                                                       'pomiar.',
 'Each physical serial device can only be assigned once': 'Each physical serial device can only be assigned once',
 'Elevated': 'Podwyższony',
 'Elevated relative background': 'Podwyższone tło względne',
 'Elevated: within warning range': 'Podwyższony: w zakresie ostrzegawczym',
 'Elevation': 'Wysokość',
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
 'Enable enable_restore in the app configuration and restart only when a restore is planned.': 'Włącz enable_restore w '
                                                                                               'konfiguracji aplikacji '
                                                                                               'i uruchom ponownie '
                                                                                               'tylko wtedy, gdy '
                                                                                               'planowane jest '
                                                                                               'przywracanie.',
 'Enable “{setting}” in the app configuration and restart only when a restore is planned.': 'Włącz „{setting}” w '
                                                                                            'konfiguracji aplikacji i '
                                                                                            'uruchom aplikację '
                                                                                            'ponownie tylko wtedy, gdy '
                                                                                            'planowane jest '
                                                                                            'przywracanie.',
 'End time UTC': 'Czas zakończenia UTC',
 'End time local': 'Lokalny czas zakończenia',
 'Entities': 'Encje',
 'Environment': 'Środowisko',
 'Error time': 'Czas błędu',
 'Estimated pressure influence': 'Szacowany wpływ ciśnienia',
 'Evaluated by': 'Ocena według',
 'Evaluates the current value using the configured thresholds.': 'Ocenia bieżącą wartość według skonfigurowanych '
                                                                 'progów.',
 'Events CSV': 'CSV zdarzeń',
 'Events and diagnostics': 'Events and diagnostics',
 'Events last 24 h': 'Zdarzenia z ostatnich 24 h',
 'Excellent': 'Doskonała',
 'Excluded measurements': 'Wykluczone pomiary',
 'Excluded pairs': 'Wykluczone pary',
 'Expand all': 'Expand all',
 'Expected samples': 'Oczekiwane pomiary',
 'Expert view': 'Widok ekspercki',
 'Explanation of the two assessments': 'Wyjaśnienie dwóch ocen',
 'Export details': 'Szczegóły eksportu',
 'Extremely elevated': 'Skrajnie podwyższone',
 'Extremely elevated: far above the usual local range': 'Skrajnie podwyższone: znacznie powyżej zwykłego lokalnego '
                                                        'zakresu',
 'Falling': 'Malejący',
 'Falling air pressure can slightly increase the share of cosmically generated secondary radiation at ground level, while rising air pressure tends to reduce it; the model detects only such statistical relationships and cannot clearly distinguish them from other natural influences.': 'Spadek '
                                                                                                                                                                                                                                                                                             'ciśnienia '
                                                                                                                                                                                                                                                                                             'atmosferycznego '
                                                                                                                                                                                                                                                                                             'może '
                                                                                                                                                                                                                                                                                             'nieznacznie '
                                                                                                                                                                                                                                                                                             'zwiększać '
                                                                                                                                                                                                                                                                                             'udział '
                                                                                                                                                                                                                                                                                             'wtórnego '
                                                                                                                                                                                                                                                                                             'promieniowania '
                                                                                                                                                                                                                                                                                             'pochodzenia '
                                                                                                                                                                                                                                                                                             'kosmicznego '
                                                                                                                                                                                                                                                                                             'na '
                                                                                                                                                                                                                                                                                             'poziomie '
                                                                                                                                                                                                                                                                                             'gruntu, '
                                                                                                                                                                                                                                                                                             'natomiast '
                                                                                                                                                                                                                                                                                             'wzrost '
                                                                                                                                                                                                                                                                                             'ciśnienia '
                                                                                                                                                                                                                                                                                             'zwykle '
                                                                                                                                                                                                                                                                                             'go '
                                                                                                                                                                                                                                                                                             'zmniejsza; '
                                                                                                                                                                                                                                                                                             'model '
                                                                                                                                                                                                                                                                                             'wykrywa '
                                                                                                                                                                                                                                                                                             'jedynie '
                                                                                                                                                                                                                                                                                             'takie '
                                                                                                                                                                                                                                                                                             'zależności '
                                                                                                                                                                                                                                                                                             'statystyczne '
                                                                                                                                                                                                                                                                                             'i '
                                                                                                                                                                                                                                                                                             'nie '
                                                                                                                                                                                                                                                                                             'potrafi '
                                                                                                                                                                                                                                                                                             'jednoznacznie '
                                                                                                                                                                                                                                                                                             'odróżnić '
                                                                                                                                                                                                                                                                                             'ich '
                                                                                                                                                                                                                                                                                             'od '
                                                                                                                                                                                                                                                                                             'innych '
                                                                                                                                                                                                                                                                                             'naturalnych '
                                                                                                                                                                                                                                                                                             'wpływów.',
 'Falling air pressure is often associated with a slightly higher intensity of cosmically generated secondary radiation at ground level, while rising air pressure is associated with a slightly lower intensity. The strength of this relationship depends on detector, location and atmosphere; the cause cannot be determined unambiguously from total counts.': 'Spadek '
                                                                                                                                                                                                                                                                                                                                                                    'ciśnienia '
                                                                                                                                                                                                                                                                                                                                                                    'atmosferycznego '
                                                                                                                                                                                                                                                                                                                                                                    'jest '
                                                                                                                                                                                                                                                                                                                                                                    'często '
                                                                                                                                                                                                                                                                                                                                                                    'związany '
                                                                                                                                                                                                                                                                                                                                                                    'z '
                                                                                                                                                                                                                                                                                                                                                                    'nieco '
                                                                                                                                                                                                                                                                                                                                                                    'większą '
                                                                                                                                                                                                                                                                                                                                                                    'intensywnością '
                                                                                                                                                                                                                                                                                                                                                                    'wtórnego '
                                                                                                                                                                                                                                                                                                                                                                    'promieniowania '
                                                                                                                                                                                                                                                                                                                                                                    'pochodzenia '
                                                                                                                                                                                                                                                                                                                                                                    'kosmicznego '
                                                                                                                                                                                                                                                                                                                                                                    'na '
                                                                                                                                                                                                                                                                                                                                                                    'poziomie '
                                                                                                                                                                                                                                                                                                                                                                    'gruntu, '
                                                                                                                                                                                                                                                                                                                                                                    'a '
                                                                                                                                                                                                                                                                                                                                                                    'wzrost '
                                                                                                                                                                                                                                                                                                                                                                    'ciśnienia '
                                                                                                                                                                                                                                                                                                                                                                    'z '
                                                                                                                                                                                                                                                                                                                                                                    'nieco '
                                                                                                                                                                                                                                                                                                                                                                    'mniejszą '
                                                                                                                                                                                                                                                                                                                                                                    'intensywnością. '
                                                                                                                                                                                                                                                                                                                                                                    'Siła '
                                                                                                                                                                                                                                                                                                                                                                    'tej '
                                                                                                                                                                                                                                                                                                                                                                    'zależności '
                                                                                                                                                                                                                                                                                                                                                                    'zależy '
                                                                                                                                                                                                                                                                                                                                                                    'od '
                                                                                                                                                                                                                                                                                                                                                                    'detektora, '
                                                                                                                                                                                                                                                                                                                                                                    'miejsca '
                                                                                                                                                                                                                                                                                                                                                                    'i '
                                                                                                                                                                                                                                                                                                                                                                    'atmosfery; '
                                                                                                                                                                                                                                                                                                                                                                    'na '
                                                                                                                                                                                                                                                                                                                                                                    'podstawie '
                                                                                                                                                                                                                                                                                                                                                                    'całkowitej '
                                                                                                                                                                                                                                                                                                                                                                    'liczby '
                                                                                                                                                                                                                                                                                                                                                                    'zliczeń '
                                                                                                                                                                                                                                                                                                                                                                    'nie '
                                                                                                                                                                                                                                                                                                                                                                    'można '
                                                                                                                                                                                                                                                                                                                                                                    'jednoznacznie '
                                                                                                                                                                                                                                                                                                                                                                    'określić '
                                                                                                                                                                                                                                                                                                                                                                    'przyczyny.',
 'Fano factor': 'Współczynnik Fano',
 'Fano factor = variance / mean; a value near 1 is consistent with Poisson-like counting statistics.': 'Współczynnik '
                                                                                                       'Fano = '
                                                                                                       'wariancja / '
                                                                                                       'średnia; '
                                                                                                       'wartość bliska '
                                                                                                       '1 jest zgodna '
                                                                                                       'ze statystyką '
                                                                                                       'zliczeń typu '
                                                                                                       'Poissona.',
 'Fano factor formula explanation': 'Współczynnik Fano = wariancja / średnia; wartość bliska 1 jest zgodna ze '
                                    'statystyką zliczeń typu Poissona.',
 'Fano factor: {value}': 'Współczynnik Fano: {value}',
 'Far above the usual local range': 'Znacznie powyżej zwykłego lokalnego zakresu',
 'File size': 'File size',
 'Firmware version': 'Wersja oprogramowania',
 'Flat': 'Flat',
 'Fleet intelligence': 'Analiza zestawu urządzeń',
 'Format': 'Format',
 'Fri': 'Pt',
 'Friday': 'Piątek',
 'Full history ZIP': 'Pełny ZIP historii',
 'GMC Radiation Monitor': 'Monitor promieniowania GMC',
 'GMC Radiation Monitoring': 'Monitorowanie promieniowania GMC',
 'GMC Reports': 'Raporty GMC',
 'GMC analysis report {period}': 'Raport analizy GMC {period}',
 'GMC detected': 'GMC detected',
 'GMC devices are being detected automatically': 'GMC devices are being detected automatically',
 'GMC radiation analysis report': 'Raport analizy promieniowania GMC',
 'GMC radiation monitoring report {period}': 'Raport monitorowania promieniowania GMC {period}',
 'GMC-300/320 family': 'Rodzina GMC-300/320',
 'GMC-320 and GMC-500+ combined': 'GMC-320 and GMC-500+ combined',
 'GMC-500 family': 'Rodzina GMC-500',
 'GMC-600 family': 'Rodzina GMC-600',
 'GMCMap consecutive upload errors': 'Kolejne błędy wysyłania do GMCMap',
 'GMCMap counter ID': 'Identyfikator licznika GMCMap',
 'GMCMap is enabled, but this device has no counter ID mapping.': 'GMCMap jest włączony, ale temu urządzeniu nie '
                                                                  'przypisano identyfikatora licznika.',
 'GMCMap last HTTP status': 'Ostatni status HTTP GMCMap',
 'GMCMap last error time': 'Czas ostatniego błędu GMCMap',
 'GMCMap last server response': 'Ostatnia odpowiedź serwera GMCMap',
 'GMCMap last successful upload': 'Ostatnie udane wysłanie do GMCMap',
 'GMCMap last upload attempt': 'Ostatnia próba wysłania do GMCMap',
 'GMCMap last upload error': 'Ostatni błąd wysyłania do GMCMap',
 'GMCMap last uploaded CPM': 'Ostatnie CPM wysłane do GMCMap',
 'GMCMap next upload': 'Następne wysłanie do GMCMap',
 'GMCMap successful uploads since start': 'Udane wysłania do GMCMap od uruchomienia',
 'GMCMap upload errors since start': 'Błędy wysyłania do GMCMap od uruchomienia',
 'GMCMap upload status': 'Stan wysyłania do GMCMap',
 'GQ manufacturer recommendation': 'Zalecenie producenta GQ',
 'Gaps are excluded from effective counting time': 'Gaps are excluded from effective counting time',
 'Generated export exceeds the {limit_mib} MiB safety limit': 'Wygenerowany eksport przekracza limit bezpieczeństwa '
                                                              '{limit_mib} MiB.',
 'Generated maintenance export exceeds the 128 MiB safety limit': 'Wygenerowany eksport konserwacyjny przekracza limit '
                                                                  'bezpieczeństwa 128 MiB.',
 'Generated report exceeds the 64 MiB safety limit': 'Wygenerowany raport przekracza limit bezpieczeństwa 64 MiB',
 'Generic GQ GMC / RFC1201-compatible device': 'Ogólne urządzenie GQ GMC zgodne z RFC1201',
 'Generic RFC1201-compatible device': 'Ogólne urządzenie zgodne z RFC1201',
 'Global report settings': 'Globalne ustawienia raportów i eksportu',
 'Good': 'Dobra',
 'Green': 'Zielony',
 'Gyro Calibrated {axis}': 'Gyro Calibrated {axis}',
 'Gyro Errors Since Start': 'Błędy żyroskopu od uruchomienia',
 'Gyro Raw {axis}': 'Surowa wartość żyroskopu {axis}',
 'Gyro X': 'Żyroskop X',
 'Gyro Y': 'Żyroskop Y',
 'Gyro Z': 'Żyroskop Z',
 'Gyro data will be included when available.': 'Dane żyroskopu zostaną dołączone, gdy będą dostępne.',
 'Gyro errors': 'Błędy żyroskopu',
 'Gyro recording is disabled.': 'Rejestrowanie żyroskopu jest wyłączone.',
 'Gyroscope': 'Żyroskop',
 'Hardware model': 'Model sprzętowy',
 'Heartbeat Errors Since Start': 'Błędy heartbeat od uruchomienia',
 'Heartbeat mode': 'Tryb heartbeat',
 'Heartbeat rolling 60 s CPM': 'Kroczące CPM z 60 s heartbeat',
 'Heatmap PNG': 'Mapa cieplna PNG',
 'Heuristic statistical assessment; not a radiation-protection classification.': 'Heurystyczna ocena statystyczna; nie '
                                                                                 'jest klasyfikacją ochrony '
                                                                                 'radiologicznej.',
 'High': 'Wysoki',
 'High relative increase': 'Duży wzrost względny',
 'High-dose Tube CPM': 'Tuba wysokiej dawki CPM',
 'High-dose tube': 'Tuba wysokiej dawki',
 'Highest stored 24 h value': 'Najwyższa zapisana wartość z 24 h',
 'Histogram PNG': 'Histogram PNG',
 'Historical chart is still being formed': 'Wykres historyczny jest jeszcze tworzony',
 'Historical development': 'Rozwój historyczny',
 'History': 'History',
 'History Write Errors Since Start': 'Błędy zapisu historii od uruchomienia',
 'History deleted': 'History deleted',
 'History maintenance': 'Zarządzanie historią',
 'History restore failed': 'Przywracanie historii nie powiodło się',
 'History restore is disabled. Enable enable_restore in the app configuration and restart.': 'Przywracanie historii '
                                                                                             'jest wyłączone. Włącz '
                                                                                             'enable_restore w '
                                                                                             'konfiguracji aplikacji i '
                                                                                             'uruchom ponownie.',
 'History restore is disabled. Enable “{setting}” in the app configuration and restart.': 'Przywracanie historii jest '
                                                                                          'wyłączone. Włącz '
                                                                                          '„{setting}” w konfiguracji '
                                                                                          'aplikacji i uruchom '
                                                                                          'ponownie.',
 'History storage warning': 'History storage warning',
 'Home Assistant API client is not configured': 'Home Assistant API client is not configured',
 'Home Assistant Recorder entity patterns': 'Home Assistant Recorder entity patterns',
 'Home Assistant Recorder history cleared': 'Home Assistant Recorder history cleared',
 'Home Assistant host UART': 'Home Assistant host UART',
 'Home Assistant location': 'Lokalizacja Home Assistant',
 'How are connected counters compared?': 'Jak porównywane są podłączone liczniki?',
 'How closely the observed spread resembles Poisson-like counting': 'Jak bardzo obserwowany rozrzut przypomina '
                                                                    'zliczenia typu Poissona',
 'How is data quality evaluated?': 'Jak oceniana jest jakość danych?',
 'How is the background profile calculated?': 'Jak obliczany jest profil tła?',
 'How is the pressure relationship assessed?': 'Jak oceniana jest zależność od ciśnienia?',
 'However, the value is noticeably above the usual local background. Observe the trend.': 'Wartość jest jednak '
                                                                                          'zauważalnie wyższa od '
                                                                                          'zwykłego lokalnego tła. '
                                                                                          'Obserwuj trend.',
 'ICRP reference projection': 'Projekcja referencyjna ICRP',
 'Inclination': 'Nachylenie',
 'Ingest diagnostics cleared': 'Ingest diagnostics cleared',
 'Inspecting backup…': 'Inspecting backup…',
 'Insufficient': 'Niewystarczająca',
 'Insufficient history for level-shift detection': 'Insufficient history for level-shift detection',
 'Insufficient paired daily values': 'Za mało porównywalnych wartości dziennych',
 'Integrity': 'Integralność',
 'Intelligence': 'Intelligence',
 'Intelligent radiation analysis': 'Inteligentna analiza promieniowania',
 'Internal database cleared': 'Internal database cleared',
 'Internal serial port': 'Internal serial port',
 'Interpret statistics with coverage in mind': 'Interpretuj statystyki z uwzględnieniem pokrycia danych',
 'Interpret these values together with coverage, device stability and the historical background.': 'Interpretuj te '
                                                                                                   'wartości łącznie z '
                                                                                                   'pokryciem, '
                                                                                                   'stabilnością '
                                                                                                   'urządzenia i '
                                                                                                   'historycznym tłem.',
 'Interpretation': 'Interpretacja',
 'Interval diagnostics': 'Diagnostyka interwałów',
 'Invalid deletion confirmation': 'Invalid deletion confirmation',
 'Invalid device clock response': 'Nieprawidłowa odpowiedź zegara urządzenia',
 'Invalid request parameters': 'Nieprawidłowe parametry żądania.',
 'Invalid serial configuration request': 'Invalid serial configuration request',
 'Keep both counters close together and similarly oriented when using the comparison as a reference.': 'Gdy używasz '
                                                                                                       'porównania '
                                                                                                       'jako '
                                                                                                       'odniesienia, '
                                                                                                       'trzymaj oba '
                                                                                                       'liczniki '
                                                                                                       'blisko siebie '
                                                                                                       'i w podobnej '
                                                                                                       'orientacji.',
 'Known radio or Zigbee adapter': 'Known radio or Zigbee adapter',
 'Language': 'Język',
 'Last HTTP status': 'Ostatni status HTTP',
 'Last Successful Measurement': 'Ostatni udany pomiar',
 'Last attempt': 'Ostatnia próba',
 'Last backup requested in this browser': 'Last backup requested in this browser',
 'Last sample age': 'Wiek ostatniego pomiaru',
 'Last server response': 'Ostatnia odpowiedź serwera',
 'Last successful storage': 'Last successful storage',
 'Last update': 'Ostatnia aktualizacja',
 'Last upload': 'Ostatnie wysłanie',
 'Last upload error': 'Ostatni błąd wysyłania',
 'Latest CPM': 'Aktualne CPM',
 'Latest CPM uncertainty': 'Latest CPM uncertainty',
 'Latest CPM vs 24 h distribution': 'Ostatnia wartość CPM względem rozkładu 24 h',
 'Latest accepted value': 'Latest accepted value',
 'Latest dose rate': 'Aktualna moc dawki',
 'Latest measurement': 'Ostatni pomiar',
 'Learned Radiation Baseline': 'Wyuczony bazowy poziom promieniowania',
 'Learned from local history': 'Wyuczony z lokalnej historii',
 'Learned pressure coefficient': 'Wyuczony współczynnik ciśnienia',
 'Learning baseline': 'Uczenie poziomu odniesienia',
 'Learning basis': 'Podstawa uczenia',
 'Learning progress': 'Postęp uczenia',
 'Learning: not enough local history yet': 'Uczenie: za mało lokalnych danych historycznych',
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
 'Less variable than Poisson expectation': 'Mniejsza zmienność niż oczekiwanie Poissona',
 'Likely device-specific deviation': 'Prawdopodobnie odchylenie właściwe dla urządzenia',
 'Limited': 'Ograniczona',
 'Live radiation CPS': 'Bieżące CPS promieniowania',
 'Live system status': 'Live system status',
 'Local background analysis': 'Analiza lokalnego tła',
 'Local background is still being learned': 'Lokalne tło jest nadal analizowane',
 'Local background model is available': 'Model lokalnego tła jest dostępny',
 'Local baseline': 'Lokalny poziom odniesienia',
 'Local hour': 'Godzina lokalna',
 'Local time [{timezone}]': 'Czas lokalny [{timezone}]',
 'Local timestamp': 'Lokalny znacznik czasu',
 'Location data comes from the Home Assistant general settings and is not sent to an external geocoding service.': 'Dane '
                                                                                                                   'lokalizacji '
                                                                                                                   'pochodzą '
                                                                                                                   'z '
                                                                                                                   'ogólnych '
                                                                                                                   'ustawień '
                                                                                                                   'Home '
                                                                                                                   'Assistant '
                                                                                                                   'i '
                                                                                                                   'nie '
                                                                                                                   'są '
                                                                                                                   'wysyłane '
                                                                                                                   'do '
                                                                                                                   'zewnętrznej '
                                                                                                                   'usługi '
                                                                                                                   'geokodowania.',
 'Location unavailable': 'Lokalizacja niedostępna',
 'Long-term context': 'Kontekst długoterminowy',
 'Long-term drift': 'Dryf długoterminowy',
 'Long-term relative factor available': 'Long-term relative factor available',
 'Long-term relative response': 'Long-term relative response',
 'Longest gap': 'Najdłuższa przerwa',
 'Longest gap [s]': 'Najdłuższa przerwa [s]',
 'Longest gap: {seconds} s': 'Najdłuższa przerwa: {seconds} s',
 'Low': 'Niski',
 'Low-dose Tube CPM': 'Tuba niskiej dawki CPM',
 'Low-dose tube': 'Tuba niskiej dawki',
 'Lowest stored 24 h value': 'Najniższa zapisana wartość z 24 h',
 'Machine-readable statistics and event data': 'Statystyki i dane zdarzeń do odczytu maszynowego',
 'Maximum': 'Maksimum',
 'Maximum CPM': 'Maksymalne CPM',
 'Maximum background index [%]': 'Maksymalny indeks tła [%]',
 'Mean': 'Średnia',
 'Mean CPM': 'Średnie CPM',
 'Mean CPM by weekday and hour — {title}': 'Średnie CPM według dnia tygodnia i godziny — {title}',
 'Mean absolute difference': 'Średnia różnica bezwzględna',
 'Mean: {value} CPM': 'Średnia: {value} CPM',
 'Measurement interval': 'Interwał pomiaru',
 'Measurement-site baseline': 'Łączny poziom odniesienia miejsca pomiaru',
 'Measurements': 'Measurements',
 'Measurements are sent to the public GMCMap service.': 'Pomiary są wysyłane do publicznej usługi GMCMap.',
 'Measurements to delete': 'Measurements to delete',
 'Median': 'Mediana',
 'Median CPM': 'Mediana CPM',
 'Median: {value} CPM': 'Mediana: {value} CPM',
 'Medium': 'Średnie',
 'Merge a compatible SQLite backup into the current history. Existing rows are preserved or updated by device serial and UTC timestamp.': 'Scal '
                                                                                                                                          'zgodną '
                                                                                                                                          'kopię '
                                                                                                                                          'SQLite '
                                                                                                                                          'z '
                                                                                                                                          'bieżącą '
                                                                                                                                          'historią. '
                                                                                                                                          'Istniejące '
                                                                                                                                          'wiersze '
                                                                                                                                          'są '
                                                                                                                                          'zachowywane '
                                                                                                                                          'lub '
                                                                                                                                          'aktualizowane '
                                                                                                                                          'według '
                                                                                                                                          'numeru '
                                                                                                                                          'seryjnego '
                                                                                                                                          'urządzenia '
                                                                                                                                          'i '
                                                                                                                                          'znacznika '
                                                                                                                                          'czasu '
                                                                                                                                          'UTC.',
 'Merged {rows} measurement rows from schema {schema}.': 'Scalono {rows} wierszy pomiarów ze schematu {schema}.',
 'Minimum / maximum: {minimum} / {maximum} CPM': 'Minimum / maksimum: {minimum} / {maximum} CPM',
 'Minimum CPM': 'Minimalne CPM',
 'Mixed device profiles': 'Mieszane profile urządzeń',
 'Moderate linear relationship': 'Umiarkowana zależność liniowa',
 'Mon': 'Pn',
 'Monday': 'Poniedziałek',
 'More history is needed before the relative background indicator is classified.': 'Potrzeba więcej historii, zanim '
                                                                                   'względny wskaźnik tła zostanie '
                                                                                   'sklasyfikowany.',
 'More history is needed; approximately {count} additional measurements are required.': 'More history is needed; '
                                                                                        'approximately {count} '
                                                                                        'additional measurements are '
                                                                                        'required.',
 'More measurements are needed for this weekday and hour.': 'Dla tego dnia tygodnia i tej godziny potrzeba więcej '
                                                            'pomiarów.',
 'More variable than Poisson expectation': 'Większa zmienność niż oczekiwanie Poissona',
 'Move away from the suspected source if safe to do so, avoid unnecessary exposure and seek qualified radiation-protection advice.': 'Jeśli '
                                                                                                                                     'można '
                                                                                                                                     'to '
                                                                                                                                     'zrobić '
                                                                                                                                     'bezpiecznie, '
                                                                                                                                     'oddal '
                                                                                                                                     'się '
                                                                                                                                     'od '
                                                                                                                                     'podejrzewanego '
                                                                                                                                     'źródła, '
                                                                                                                                     'unikaj '
                                                                                                                                     'zbędnej '
                                                                                                                                     'ekspozycji '
                                                                                                                                     'i '
                                                                                                                                     'zasięgnij '
                                                                                                                                     'fachowej '
                                                                                                                                     'porady '
                                                                                                                                     'z '
                                                                                                                                     'zakresu '
                                                                                                                                     'ochrony '
                                                                                                                                     'radiologicznej.',
 'Never': 'Nigdy',
 'Newest sample': 'Najnowszy pomiar',
 'Next upload': 'Następne wysłanie',
 'No GMC device detected': 'No GMC device detected',
 'No action is required while the result remains normal. Investigate persistent changes by checking the measurement location and comparing both devices.': 'Dopóki '
                                                                                                                                                           'wynik '
                                                                                                                                                           'pozostaje '
                                                                                                                                                           'prawidłowy, '
                                                                                                                                                           'nie '
                                                                                                                                                           'jest '
                                                                                                                                                           'wymagane '
                                                                                                                                                           'żadne '
                                                                                                                                                           'działanie. '
                                                                                                                                                           'Trwałe '
                                                                                                                                                           'zmiany '
                                                                                                                                                           'sprawdź, '
                                                                                                                                                           'kontrolując '
                                                                                                                                                           'miejsce '
                                                                                                                                                           'pomiaru '
                                                                                                                                                           'i '
                                                                                                                                                           'porównując '
                                                                                                                                                           'oba '
                                                                                                                                                           'urządzenia.',
 'No action is required. Continue normal monitoring.': 'Nie jest wymagane żadne działanie. Kontynuuj zwykłe '
                                                       'monitorowanie.',
 'No action is required. The assessment becomes more reliable as additional measurements are collected.': 'Nie jest '
                                                                                                          'wymagane '
                                                                                                          'żadne '
                                                                                                          'działanie. '
                                                                                                          'Ocena '
                                                                                                          'będzie '
                                                                                                          'bardziej '
                                                                                                          'wiarygodna '
                                                                                                          'po '
                                                                                                          'zgromadzeniu '
                                                                                                          'kolejnych '
                                                                                                          'pomiarów.',
 'No action required': 'Nie są wymagane żadne działania',
 'No active device warnings': 'No active device warnings',
 'No connected GMC device': 'No connected GMC device',
 'No connected counter is available yet. The next serial scan runs automatically.': 'No connected counter is available '
                                                                                    'yet. The next serial scan runs '
                                                                                    'automatically.',
 'No connected devices.': 'Brak podłączonych urządzeń.',
 'No current pressure source is available': 'Brak aktualnego źródła ciśnienia',
 'No data': 'Brak danych',
 'No known GMC devices': 'No known GMC devices',
 'No matching Home Assistant entities': 'No matching Home Assistant entities',
 'No measurement yet': 'Brak pomiaru',
 'No measurements in selected period': 'Brak pomiarów w wybranym okresie',
 'No measurements yet.': 'Brak pomiarów.',
 'No persistent level shift detected': 'No persistent level shift detected',
 'No position changes recorded.': 'Nie zarejestrowano zmian położenia.',
 'No pressure variation': 'Niewystarczająca zmienność ciśnienia',
 'No pressure-typical signature': 'Brak sygnatury typowej dla ciśnienia',
 'No pronounced baseline jumps detected.': 'Nie wykryto wyraźnych skoków poziomu bazowego.',
 'No reports have been requested in this browser yet.': 'No reports have been requested in this browser yet.',
 'No shared rise detected.': 'Nie wykryto wspólnego wzrostu.',
 'No stored measurements': 'No stored measurements',
 'No suitable serial device was found.': 'No suitable serial device was found.',
 'No sustained relative anomaly events detected': 'Nie wykryto utrzymujących się względnych anomalii',
 'No valid CPM baseline': 'Brak prawidłowej linii bazowej CPM',
 'Normal': 'Normalnie',
 'Normal for this time': 'Normalne dla tej pory',
 'Normal: within the usual local range': 'Normalnie: w zwykłym lokalnym zakresie',
 'Not available yet — at least two CPM samples are required': 'Jeszcze niedostępne — wymagane są co najmniej dwa '
                                                              'pomiary CPM',
 'Not available yet — more baseline history is required': 'Jeszcze niedostępne — potrzeba więcej historii poziomu '
                                                          'bazowego',
 'Not available yet — more paired samples are required': 'Jeszcze niedostępne — potrzeba więcej par pomiarów',
 'Not available yet — no temperature samples were stored in the current 24 h window.': 'Jeszcze niedostępne — w '
                                                                                       'bieżącym oknie 24 h nie '
                                                                                       'zapisano pomiarów temperatury.',
 'Not available yet — the 24 h CPM series needs variation and at least two samples': 'Jeszcze niedostępne — seria CPM '
                                                                                     'z 24 h musi wykazywać zmienność '
                                                                                     'i zawierać co najmniej dwa '
                                                                                     'pomiary',
 'Not available yet — the 24 h mean and spread are still insufficient': 'Jeszcze niedostępne — średnia i rozrzut z 24 '
                                                                        'h są nadal niewystarczające',
 'Not available — CPM did not vary during this period': 'Niedostępne — CPM nie zmieniało się w tym okresie',
 'Not available — the sensor value did not vary during this period': 'Niedostępne — wartość czujnika nie zmieniała się '
                                                                     'w tym okresie',
 'Not configured': 'Nie skonfigurowano',
 'Not connected': 'Not connected',
 'Not detected yet': 'Jeszcze nie wykryto',
 'Not enough local history yet': 'Za mało lokalnych danych historycznych',
 'Not found': 'Nie znaleziono',
 'Not recorded in this browser': 'Not recorded in this browser',
 'Not suitable as a GMC device': 'Not suitable as a GMC device',
 'Not suitable for GMC': 'Not suitable for GMC',
 'Not yet checked as a GMC device': 'Not yet checked as a GMC device',
 'Noticeable': 'Zauważalne',
 'Noticeable baseline drift': 'Wyraźny dryf poziomu odniesienia',
 'Noticeable difference from Poisson-like spread': 'Wyraźna różnica względem rozrzutu typu Poissona',
 'Noticeable statistical deviation': 'Wyraźne odchylenie statystyczne',
 'Noticeable: above the usual local range': 'Zauważalne: powyżej zwykłego lokalnego zakresu',
 'Number of samples': 'Liczba pomiarów',
 'Observed': 'Zaobserwowane',
 'Observed SD / √mean': 'Obserwowane SD / √średnia',
 'Official reference values': 'Oficjalne wartości odniesienia',
 'Offline': 'Offline',
 'Oldest sample': 'Najstarszy pomiar',
 'One current weather entity is available': 'Dostępna jest jedna aktualna encja pogodowa',
 'One-hour mean is {deviation:+.1f}% relative to the learned baseline': 'Średnia godzinowa wynosi {deviation:+.1f}% '
                                                                        'względem wyuczonego poziomu bazowego',
 'One-hour means': 'Średnie godzinowe',
 'One-hour robust level is {deviation:+.1f}% relative to the device baseline': 'Odporny poziom jednogodzinny wynosi '
                                                                               '{deviation:+.1f}% względem poziomu '
                                                                               'odniesienia urządzenia',
 'Online': 'Online',
 'Only quality-filtered, one-to-one time-matched measurements are compared. Agreement, correlation, relative bias and stability are evaluated separately so one faulty counter does not automatically define the site result.': 'Porównywane '
                                                                                                                                                                                                                                'są '
                                                                                                                                                                                                                                'wyłącznie '
                                                                                                                                                                                                                                'pomiary '
                                                                                                                                                                                                                                'po '
                                                                                                                                                                                                                                'filtracji '
                                                                                                                                                                                                                                'jakościowej, '
                                                                                                                                                                                                                                'dopasowane '
                                                                                                                                                                                                                                'czasowo '
                                                                                                                                                                                                                                'jeden '
                                                                                                                                                                                                                                'do '
                                                                                                                                                                                                                                'jednego. '
                                                                                                                                                                                                                                'Zgodność, '
                                                                                                                                                                                                                                'korelacja, '
                                                                                                                                                                                                                                'względne '
                                                                                                                                                                                                                                'odchylenie '
                                                                                                                                                                                                                                'i '
                                                                                                                                                                                                                                'stabilność '
                                                                                                                                                                                                                                'są '
                                                                                                                                                                                                                                'oceniane '
                                                                                                                                                                                                                                'oddzielnie, '
                                                                                                                                                                                                                                'aby '
                                                                                                                                                                                                                                'jeden '
                                                                                                                                                                                                                                'wadliwy '
                                                                                                                                                                                                                                'licznik '
                                                                                                                                                                                                                                'nie '
                                                                                                                                                                                                                                'określał '
                                                                                                                                                                                                                                'automatycznie '
                                                                                                                                                                                                                                'wyniku '
                                                                                                                                                                                                                                'dla '
                                                                                                                                                                                                                                'miejsca.',
 'Only the most important conclusions at a glance': 'Tylko najważniejsze wnioski na pierwszy rzut oka',
 'Open': 'Open',
 'Open serial device connections': 'Open serial device connections',
 'Operational events cleared': 'Operational events cleared',
 'Orientation cannot be verified automatically': 'Orientation cannot be verified automatically',
 'Orientation changes detected': 'Orientation changes detected',
 'Orientation data is temporarily unavailable.': 'Dane orientacji są tymczasowo niedostępne.',
 'Orientation qualification': 'Orientation qualification',
 'Orientation stable': 'Orientation stable',
 'Original raw-data CSV': 'Original raw-data CSV',
 'Outliers and invalid measurements': 'Wartości odstające i nieprawidłowe pomiary',
 'Overview': 'Przegląd',
 'P95 CPM': 'CPM P95',
 'P95: {value} CPM': 'P95: {value} CPM',
 'P99 CPM': 'CPM P99',
 'P99: {value} CPM': 'P99: {value} CPM',
 'PDF report': 'Raport PDF',
 'Pair-level disagreement': 'Rozbieżność na poziomie par',
 'Pearson r · n={count} paired samples': 'r Pearsona · n={count} par pomiarów',
 'Period: {period} ({timezone})': 'Okres: {period} ({timezone})',
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
 'Pitch angle': 'Kąt pochylenia',
 'Plausibilised from two weather entities': 'Uwiarygodniono na podstawie dwóch encji pogodowych',
 'Poisson SD ratio': 'Stosunek SD Poissona',
 'Poisson SD ratio = observed standard deviation / √mean; a value near 1 indicates Poisson-like spread.': 'Stosunek SD '
                                                                                                          'Poissona = '
                                                                                                          'obserwowane '
                                                                                                          'odchylenie '
                                                                                                          'standardowe '
                                                                                                          '/ √średnia; '
                                                                                                          'wartość '
                                                                                                          'bliska 1 '
                                                                                                          'wskazuje na '
                                                                                                          'rozrzut '
                                                                                                          'typu '
                                                                                                          'Poissona.',
 'Poisson SD ratio formula explanation': 'Stosunek SD Poissona = obserwowane odchylenie standardowe / √średnia; '
                                         'wartość bliska 1 wskazuje na rozrzut typu Poissona.',
 'Poisson SD ratio: {value}': 'Stosunek SD Poissona: {value}',
 'Poisson counting interval from the observed impulse count': 'Poisson counting interval from the observed impulse '
                                                              'count',
 'Poisson expectation (λ={mean:.2f})': 'Wartość oczekiwana Poissona (λ={mean:.2f})',
 'Poor': 'Słaba',
 'Position change log': 'Dziennik zmian położenia',
 'Possible GMC connection cable': 'Possible GMC connection cable',
 'Possible persistent level shift': 'Possible persistent level shift',
 'Pressure model is still being formed': 'Model ciśnienia jest nadal tworzony',
 'Pressure model unavailable': 'Model ciśnienia niedostępny',
 'Pressure-typical signature is pronounced': 'Wyraźna sygnatura typowa dla ciśnienia',
 'Preview backup': 'Preview backup',
 'Previous day': 'Poprzedni dzień',
 'Previous week': 'Poprzedni tydzień',
 'Probable real change': 'Prawdopodobna rzeczywista zmiana',
 'Probable shared measurement-site change': 'Prawdopodobna wspólna zmiana w miejscu pomiaru',
 'Profile': 'Profil urządzenia',
 'Profile is still being formed': 'Profil jest nadal tworzony',
 'Provider': 'Dostawca',
 'Public GMCMap upload': 'Publiczne wysyłanie do GMCMap',
 'Quality weight': 'Waga jakości',
 'Quality-filtered correlation': 'Korelacja po filtracji jakościowej',
 'Quality-filtered measurement CSV': 'Quality-filtered measurement CSV',
 'Quick downloads': 'Szybkie pobieranie',
 'Radiation 1 h Mean': 'Średnia promieniowania z 1 h',
 'Radiation 1 h Median': 'Mediana promieniowania z 1 h',
 'Radiation 1 h Standard Deviation': 'Odchylenie standardowe promieniowania z 1 h',
 'Radiation Baseline Deviation': 'Odchylenie od bazowego poziomu promieniowania',
 'Radiation CPM': 'Promieniowanie CPM',
 'Radiation Rapid Change': 'Szybka zmiana promieniowania',
 'Radiation count rate [CPM]': 'Częstość zliczeń promieniowania [CPM]',
 'Radiation counts fluctuate naturally. The Fano factor and Poisson spread ratio compare the observed variation with a simple counting-statistics model; they describe distribution shape but not a physical cause or calibration state.': 'Liczba '
                                                                                                                                                                                                                                           'impulsów '
                                                                                                                                                                                                                                           'promieniowania '
                                                                                                                                                                                                                                           'naturalnie '
                                                                                                                                                                                                                                           'się '
                                                                                                                                                                                                                                           'zmienia. '
                                                                                                                                                                                                                                           'Współczynnik '
                                                                                                                                                                                                                                           'Fano '
                                                                                                                                                                                                                                           'i '
                                                                                                                                                                                                                                           'stosunek '
                                                                                                                                                                                                                                           'rozrzutu '
                                                                                                                                                                                                                                           'Poissona '
                                                                                                                                                                                                                                           'porównują '
                                                                                                                                                                                                                                           'obserwowaną '
                                                                                                                                                                                                                                           'zmienność '
                                                                                                                                                                                                                                           'z '
                                                                                                                                                                                                                                           'prostym '
                                                                                                                                                                                                                                           'modelem '
                                                                                                                                                                                                                                           'statystyki '
                                                                                                                                                                                                                                           'zliczeń; '
                                                                                                                                                                                                                                           'opisują '
                                                                                                                                                                                                                                           'kształt '
                                                                                                                                                                                                                                           'rozkładu, '
                                                                                                                                                                                                                                           'ale '
                                                                                                                                                                                                                                           'nie '
                                                                                                                                                                                                                                           'fizyczną '
                                                                                                                                                                                                                                           'przyczynę '
                                                                                                                                                                                                                                           'ani '
                                                                                                                                                                                                                                           'stan '
                                                                                                                                                                                                                                           'kalibracji.',
 'Radiation measurement continues unless the device status says otherwise.': 'Pomiar promieniowania jest kontynuowany, '
                                                                             'chyba że stan urządzenia wskazuje '
                                                                             'inaczej.',
 'Radiation measurement continues. An external Home Assistant temperature may be used when configured.': 'Pomiar '
                                                                                                         'promieniowania '
                                                                                                         'jest '
                                                                                                         'kontynuowany. '
                                                                                                         'Po '
                                                                                                         'skonfigurowaniu '
                                                                                                         'może być '
                                                                                                         'używana '
                                                                                                         'zewnętrzna '
                                                                                                         'temperatura '
                                                                                                         'z Home '
                                                                                                         'Assistant.',
 'Radiation measurement continues; only the optional orientation value is affected.': 'Pomiar promieniowania jest '
                                                                                      'kontynuowany; problem dotyczy '
                                                                                      'tylko opcjonalnej wartości '
                                                                                      'orientacji.',
 'Radiation monitoring analysis': 'Analiza monitorowania promieniowania',
 'Radiation traffic light': 'Sygnalizacja promieniowania',
 'Radiation traffic light hysteresis explanation': 'Sygnalizacja promieniowania używa histerezy: żółty od '
                                                   '{yellow_enter:g}% i powrót poniżej {yellow_clear:g}%; czerwony od '
                                                   '{red_enter:g}% i powrót poniżej {red_clear:g}%.',
 'Radiation traffic light uses hysteresis: it enters yellow at {yellow_enter:g}% and clears below {yellow_clear:g}%; it enters red at {red_enter:g}% and clears below {red_clear:g}%.': 'Sygnalizacja '
                                                                                                                                                                                        'promieniowania '
                                                                                                                                                                                        'używa '
                                                                                                                                                                                        'histerezy: '
                                                                                                                                                                                        'żółty '
                                                                                                                                                                                        'od '
                                                                                                                                                                                        '{yellow_enter:g}% '
                                                                                                                                                                                        'i '
                                                                                                                                                                                        'powrót '
                                                                                                                                                                                        'poniżej '
                                                                                                                                                                                        '{yellow_clear:g}%; '
                                                                                                                                                                                        'czerwony '
                                                                                                                                                                                        'od '
                                                                                                                                                                                        '{red_enter:g}% '
                                                                                                                                                                                        'i '
                                                                                                                                                                                        'powrót '
                                                                                                                                                                                        'poniżej '
                                                                                                                                                                                        '{red_clear:g}%.',
 'Raw CSV': 'Surowy CSV',
 'Raw device values are stored separately before quality filtering': 'Raw device values are stored separately before '
                                                                     'quality filtering',
 'Raw gyro [signed int16]': 'Surowy żyroskop [int16 ze znakiem]',
 'Raw-data archive': 'Raw-data archive',
 'Read-only mode': 'Read-only mode',
 'Ready for new measurements': 'Ready for new measurements',
 'Recent 30 days compared with the preceding 30 days': 'Ostatnie 30 dni w porównaniu z poprzednimi 30 dniami',
 'Recent data quality is high': 'Jakość ostatnich danych jest wysoka',
 'Recent period compared with the preceding period': 'Ostatni okres w porównaniu z poprzednim',
 'Recent quality-filtered data quality is high': 'Jakość ostatnich przefiltrowanych danych jest wysoka',
 'Recent reports': 'Recent reports',
 'Recommendation': 'Zalecenie',
 'Recommended': 'Recommended',
 'Reconnects': 'Ponowne połączenia',
 'Red': 'Czerwony',
 'Reduced': 'Obniżona',
 'Refreshing device status…': 'Refreshing device status…',
 'Relative anomaly indicator only; not a safety classification.': 'Wyłącznie względny wskaźnik anomalii; nie jest to '
                                                                  'klasyfikacja bezpieczeństwa.',
 'Relative correction factor': 'Relative correction factor',
 'Relative spread': 'Relative spread',
 'Relative to 7 d baseline': 'Względem 7-dniowego poziomu bazowego',
 'Relative-factor confidence': 'Relative-factor confidence',
 'Remaining deviation': 'Pozostałe odchylenie',
 'Remove': 'Remove',
 'Report': 'Report',
 'Report generation failed': 'Generowanie raportu nie powiodło się',
 'Report target': 'Urządzenia w raporcie',
 'Reports': 'Reports',
 'Reports for the displayed analysis': 'Reports for the displayed analysis',
 'Rescan devices': 'Rescan devices',
 'Resolve persistent connection gaps before relying on long-term comparisons.': 'Usuń trwałe przerwy w połączeniu, '
                                                                                'zanim oprzesz się na porównaniach '
                                                                                'długoterminowych.',
 'Restore backup': 'Przywróć kopię',
 'Restore complete': 'Przywracanie zakończone',
 'Restore confirmation text must be exactly RESTORE': 'Tekst potwierdzenia musi brzmieć dokładnie RESTORE',
 'Restore history': 'Przywróć historię',
 'Restore is disabled by default.': 'Przywracanie jest domyślnie wyłączone.',
 'Restore upload must be between 1 byte and 128 MiB': 'Plik przywracania musi mieć od 1 bajta do 128 MiB',
 'Return to GMC Radiation Monitoring': 'Powrót do monitorowania promieniowania GMC',
 'Return to GMC Reports': 'Powrót do raportów GMC',
 'Review the event export for timing and severity': 'Sprawdź eksport zdarzeń pod kątem czasu i poziomu',
 'Review the recent trend and event timing. Check both counters and the measurement location if the change persists.': 'Przejrzyj '
                                                                                                                       'ostatni '
                                                                                                                       'trend '
                                                                                                                       'i '
                                                                                                                       'czas '
                                                                                                                       'zdarzeń. '
                                                                                                                       'Jeśli '
                                                                                                                       'zmiana '
                                                                                                                       'się '
                                                                                                                       'utrzymuje, '
                                                                                                                       'sprawdź '
                                                                                                                       'oba '
                                                                                                                       'liczniki '
                                                                                                                       'i '
                                                                                                                       'miejsce '
                                                                                                                       'pomiaru.',
 'Rising': 'Rosnący',
 'Robust medians are used; rejected measurements and isolated spikes do not immediately change the profile.': 'Stosowane '
                                                                                                              'są '
                                                                                                              'odporne '
                                                                                                              'mediany; '
                                                                                                              'odrzucone '
                                                                                                              'pomiary '
                                                                                                              'i '
                                                                                                              'pojedyncze '
                                                                                                              'skoki '
                                                                                                              'nie '
                                                                                                              'zmieniają '
                                                                                                              'profilu '
                                                                                                              'natychmiast.',
 'Robust one-hour values': 'Odporne wartości jednogodzinne',
 'Roll angle': 'Kąt przechyłu',
 'Rolling windows end at the latest stored measurement. Dose-rate values are derived from CPM using the configured factor and are not independently measured. CPM remains the primary measurement. The traffic light is a relative background-anomaly indicator, not an emergency, health, or radiation-safety classification.': 'Okna '
                                                                                                                                                                                                                                                                                                                                 'kroczące '
                                                                                                                                                                                                                                                                                                                                 'kończą '
                                                                                                                                                                                                                                                                                                                                 'się '
                                                                                                                                                                                                                                                                                                                                 'na '
                                                                                                                                                                                                                                                                                                                                 'ostatnim '
                                                                                                                                                                                                                                                                                                                                 'zapisanym '
                                                                                                                                                                                                                                                                                                                                 'pomiarze. '
                                                                                                                                                                                                                                                                                                                                 'Moce '
                                                                                                                                                                                                                                                                                                                                 'dawki '
                                                                                                                                                                                                                                                                                                                                 'są '
                                                                                                                                                                                                                                                                                                                                 'wyliczane '
                                                                                                                                                                                                                                                                                                                                 'z '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'przy '
                                                                                                                                                                                                                                                                                                                                 'użyciu '
                                                                                                                                                                                                                                                                                                                                 'skonfigurowanego '
                                                                                                                                                                                                                                                                                                                                 'współczynnika '
                                                                                                                                                                                                                                                                                                                                 'i '
                                                                                                                                                                                                                                                                                                                                 'nie '
                                                                                                                                                                                                                                                                                                                                 'są '
                                                                                                                                                                                                                                                                                                                                 'mierzone '
                                                                                                                                                                                                                                                                                                                                 'niezależnie. '
                                                                                                                                                                                                                                                                                                                                 'CPM '
                                                                                                                                                                                                                                                                                                                                 'pozostaje '
                                                                                                                                                                                                                                                                                                                                 'podstawowym '
                                                                                                                                                                                                                                                                                                                                 'pomiarem. '
                                                                                                                                                                                                                                                                                                                                 'Sygnalizacja '
                                                                                                                                                                                                                                                                                                                                 'jest '
                                                                                                                                                                                                                                                                                                                                 'wskaźnikiem '
                                                                                                                                                                                                                                                                                                                                 'względnej '
                                                                                                                                                                                                                                                                                                                                 'anomalii '
                                                                                                                                                                                                                                                                                                                                 'tła, '
                                                                                                                                                                                                                                                                                                                                 'a '
                                                                                                                                                                                                                                                                                                                                 'nie '
                                                                                                                                                                                                                                                                                                                                 'klasyfikacją '
                                                                                                                                                                                                                                                                                                                                 'awaryjną, '
                                                                                                                                                                                                                                                                                                                                 'zdrowotną '
                                                                                                                                                                                                                                                                                                                                 'ani '
                                                                                                                                                                                                                                                                                                                                 'ochrony '
                                                                                                                                                                                                                                                                                                                                 'radiologicznej.',
 'SD: {value} CPM': 'SD: {value} CPM',
 'SQLite backup': 'Kopia SQLite',
 'SQLite backup file': 'SQLite backup file',
 'SQLite database vacuum completed': 'SQLite database vacuum completed',
 'Sample standard deviation': 'Odchylenie standardowe próbki',
 'Samples': 'Próbki',
 'Samples: {samples} / {expected}': 'Pomiary: {samples} / {expected}',
 'Sampling interval: {interval} s | Samples: {samples}/{expected} | Completeness: {completeness:.2f}% | Generated: {generated} | App {version}': 'Interwał: '
                                                                                                                                                 '{interval} '
                                                                                                                                                 's '
                                                                                                                                                 '| '
                                                                                                                                                 'Pomiary: '
                                                                                                                                                 '{samples}/{expected} '
                                                                                                                                                 '| '
                                                                                                                                                 'Kompletność: '
                                                                                                                                                 '{completeness:.2f}% '
                                                                                                                                                 '| '
                                                                                                                                                 'Utworzono: '
                                                                                                                                                 '{generated} '
                                                                                                                                                 '| '
                                                                                                                                                 'Aplikacja '
                                                                                                                                                 '{version}',
 'Sampling interval: {seconds} s': 'Interwał próbkowania: {seconds} s',
 'Sat': 'So',
 'Saturday': 'Sobota',
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
 'Second half vs first half of available 7 d window': 'Druga połowa względem pierwszej połowy dostępnego okna 7 dni',
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
 'Serial': 'Numer seryjny',
 'Serial Errors Since Start': 'Błędy portu szeregowego od uruchomienia',
 'Serial Reconnects Since Start': 'Ponowne połączenia szeregowe od uruchomienia',
 'Serial USB device': 'Serial USB device',
 'Serial connection recovered': 'Serial connection recovered',
 'Serial device connections': 'Serial device connections',
 'Serial errors / reconnects': 'Błędy portu szeregowego / ponowne połączenia',
 'Serial port': 'Port szeregowy',
 'Serial: {serial} | Period: {period} | Timezone: {timezone}': 'Numer seryjny: {serial} | Okres: {period} | Strefa '
                                                               'czasowa: {timezone}',
 'Serial: {value}': 'Numer seryjny: {value}',
 'Severity': 'Poziom',
 'Shared CPM rise': 'Wspólny wzrost CPM',
 'Shared event detector': 'Detektor wspólnych zdarzeń',
 'Show analysis': 'Pokaż analizę',
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
 'Simple': 'Prosty',
 'Since app start': 'Od uruchomienia aplikacji',
 'Slightly noticeable': 'Lekko zauważalny',
 'Slightly tilted': 'Slightly tilted',
 'Small baseline drift': 'Mały dryf poziomu odniesienia',
 'Smart Alert State': 'Stan inteligentnego alarmu',
 'Smoothed historical background trend': 'Wygładzony historyczny trend tła',
 'Source validation': 'Walidacja źródeł',
 'Specific ISO week': 'Konkretny tydzień ISO',
 'Specific date': 'Konkretna data',
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
 'Stability and device health': 'Stabilność i stan urządzenia',
 'Stable': 'Stabilny',
 'Stable device path': 'Stable device path',
 'Stable devices': 'Stabilne urządzenia',
 'Standard deviation CPM': 'Odchylenie standardowe CPM',
 'Start time UTC': 'Czas rozpoczęcia UTC',
 'Start time local': 'Lokalny czas rozpoczęcia',
 'Start with a readable PDF or a complete ZIP bundle. Raw and specialist formats remain available below without crowding the main view.': 'Zacznij '
                                                                                                                                          'od '
                                                                                                                                          'czytelnego '
                                                                                                                                          'PDF '
                                                                                                                                          'lub '
                                                                                                                                          'pełnego '
                                                                                                                                          'pakietu '
                                                                                                                                          'ZIP. '
                                                                                                                                          'Formaty '
                                                                                                                                          'surowe '
                                                                                                                                          'i '
                                                                                                                                          'specjalistyczne '
                                                                                                                                          'pozostają '
                                                                                                                                          'dostępne '
                                                                                                                                          'niżej, '
                                                                                                                                          'bez '
                                                                                                                                          'przeładowania '
                                                                                                                                          'głównego '
                                                                                                                                          'widoku.',
 'Statistical indication only': 'Tylko wskazanie statystyczne',
 'Statistical level shift': 'Statistical level shift',
 'Statistically noticeable': 'Statystycznie zauważalne',
 'Statistics': 'Statystyki',
 'Stored samples': 'Zapisane próbki',
 'Stored samples across all devices': 'Zapisane pomiary ze wszystkich urządzeń',
 'Stored samples for this device': 'Pomiary zapisane dla tego urządzenia',
 'Strong common signal': 'Silny wspólny sygnał',
 'Strong linear relationship': 'Silna zależność liniowa',
 'Strong statistical deviation': 'Silne odchylenie statystyczne',
 'Successful uploads': 'Udane wysłania',
 'Successful uploads since start': 'Udane wysłania od uruchomienia',
 'Suitable for most trend analysis': 'Odpowiednie do większości analiz trendów',
 'Summary': 'Podsumowanie',
 'Sun': 'Nd',
 'Sunday': 'Niedziela',
 'Supervisor API access is unavailable': 'Supervisor API access is unavailable',
 'Supply voltage [V]': 'Napięcie zasilania [V]',
 'Suspicious CPM value is being verified': 'Suspicious CPM value is being verified',
 'Sustained Radiation Alert': 'Utrzymujący się alarm promieniowania',
 'Sustained relative anomaly events': 'Utrzymujące się względne zdarzenia anomalii',
 'Sustained yellow/red relative anomaly events': 'Utrzymujące się żółte/czerwone względne zdarzenia anomalii',
 'Temperature': 'Temperatura',
 'Temperature / voltage errors': 'Błędy temperatury / napięcia',
 'Temperature Errors Since Start': 'Błędy temperatury od uruchomienia',
 'Temperature [°C]': 'Temperatura [°C]',
 'Temperature and voltage relationships': 'Zależności od temperatury i napięcia',
 'Temperature bins (24 h)': 'Przedziały temperatury (24 h)',
 'Temperature correlation': 'Korelacja z temperaturą',
 'Temperature profile is still being formed': 'Profil temperatury jest nadal tworzony',
 'Temperature trend': 'Trend temperatury',
 'Temperature-specific background': 'Tło zależne od temperatury',
 'The Supervisor options could not be loaded: {error}': 'The Supervisor options could not be loaded: {error}',
 'The absolute assessment starts after the first measurement.': 'Ocena bezwzględna rozpocznie się po pierwszym '
                                                                'pomiarze.',
 'The absolute level is below the configured warning threshold, but the value is far above the learned local background.': 'Poziom '
                                                                                                                           'bezwzględny '
                                                                                                                           'jest '
                                                                                                                           'poniżej '
                                                                                                                           'skonfigurowanego '
                                                                                                                           'progu '
                                                                                                                           'ostrzegawczego, '
                                                                                                                           'ale '
                                                                                                                           'wartość '
                                                                                                                           'znacznie '
                                                                                                                           'przewyższa '
                                                                                                                           'wyuczony '
                                                                                                                           'lokalny '
                                                                                                                           'poziom '
                                                                                                                           'tła.',
 'The absolute level is currently uncritical, but the local comparison or short-term trend deserves continued observation.': 'Poziom '
                                                                                                                             'bezwzględny '
                                                                                                                             'nie '
                                                                                                                             'jest '
                                                                                                                             'obecnie '
                                                                                                                             'krytyczny, '
                                                                                                                             'jednak '
                                                                                                                             'porównanie '
                                                                                                                             'lokalne '
                                                                                                                             'lub '
                                                                                                                             'trend '
                                                                                                                             'krótkoterminowy '
                                                                                                                             'wymaga '
                                                                                                                             'dalszej '
                                                                                                                             'obserwacji.',
 'The absolute level is currently uncritical. More local history is required before anomaly detection becomes reliable.': 'Poziom '
                                                                                                                          'bezwzględny '
                                                                                                                          'nie '
                                                                                                                          'jest '
                                                                                                                          'obecnie '
                                                                                                                          'krytyczny. '
                                                                                                                          'Do '
                                                                                                                          'wiarygodnego '
                                                                                                                          'wykrywania '
                                                                                                                          'anomalii '
                                                                                                                          'potrzeba '
                                                                                                                          'więcej '
                                                                                                                          'lokalnych '
                                                                                                                          'danych '
                                                                                                                          'historycznych.',
 'The add-on is restarting so the new serial assignments become active.': 'The add-on is restarting so the new serial '
                                                                          'assignments become active.',
 'The app combines the recent trend, robust statistics, agreement between connected counters and the learned local background. The result is a statistical aid and does not identify a physical cause.': 'Aplikacja '
                                                                                                                                                                                                         'łączy '
                                                                                                                                                                                                         'ostatni '
                                                                                                                                                                                                         'trend, '
                                                                                                                                                                                                         'odporne '
                                                                                                                                                                                                         'statystyki, '
                                                                                                                                                                                                         'zgodność '
                                                                                                                                                                                                         'podłączonych '
                                                                                                                                                                                                         'liczników '
                                                                                                                                                                                                         'i '
                                                                                                                                                                                                         'wyuczone '
                                                                                                                                                                                                         'lokalne '
                                                                                                                                                                                                         'tło. '
                                                                                                                                                                                                         'Wynik '
                                                                                                                                                                                                         'jest '
                                                                                                                                                                                                         'pomocą '
                                                                                                                                                                                                         'statystyczną '
                                                                                                                                                                                                         'i '
                                                                                                                                                                                                         'nie '
                                                                                                                                                                                                         'wskazuje '
                                                                                                                                                                                                         'fizycznej '
                                                                                                                                                                                                         'przyczyny.',
 'The app compares quality-filtered measurements from the same weekday and hour. Robust medians reduce the influence of isolated spikes and regular daily patterns are kept separate from unusual changes.': 'Aplikacja '
                                                                                                                                                                                                             'porównuje '
                                                                                                                                                                                                             'pomiary '
                                                                                                                                                                                                             'po '
                                                                                                                                                                                                             'filtracji '
                                                                                                                                                                                                             'jakościowej '
                                                                                                                                                                                                             'z '
                                                                                                                                                                                                             'tego '
                                                                                                                                                                                                             'samego '
                                                                                                                                                                                                             'dnia '
                                                                                                                                                                                                             'tygodnia '
                                                                                                                                                                                                             'i '
                                                                                                                                                                                                             'tej '
                                                                                                                                                                                                             'samej '
                                                                                                                                                                                                             'godziny. '
                                                                                                                                                                                                             'Odporne '
                                                                                                                                                                                                             'mediany '
                                                                                                                                                                                                             'ograniczają '
                                                                                                                                                                                                             'wpływ '
                                                                                                                                                                                                             'pojedynczych '
                                                                                                                                                                                                             'pików, '
                                                                                                                                                                                                             'a '
                                                                                                                                                                                                             'regularne '
                                                                                                                                                                                                             'wzorce '
                                                                                                                                                                                                             'dobowe '
                                                                                                                                                                                                             'są '
                                                                                                                                                                                                             'oddzielane '
                                                                                                                                                                                                             'od '
                                                                                                                                                                                                             'nietypowych '
                                                                                                                                                                                                             'zmian.',
 'The app compares quality-filtered radiation measurements with available air-pressure data. A statistical relationship can support interpretation, but correlation alone does not prove a cosmic or environmental cause.': 'Aplikacja '
                                                                                                                                                                                                                            'porównuje '
                                                                                                                                                                                                                            'pomiary '
                                                                                                                                                                                                                            'promieniowania '
                                                                                                                                                                                                                            'po '
                                                                                                                                                                                                                            'filtracji '
                                                                                                                                                                                                                            'jakościowej '
                                                                                                                                                                                                                            'z '
                                                                                                                                                                                                                            'dostępnymi '
                                                                                                                                                                                                                            'danymi '
                                                                                                                                                                                                                            'ciśnienia '
                                                                                                                                                                                                                            'powietrza. '
                                                                                                                                                                                                                            'Zależność '
                                                                                                                                                                                                                            'statystyczna '
                                                                                                                                                                                                                            'może '
                                                                                                                                                                                                                            'ułatwiać '
                                                                                                                                                                                                                            'interpretację, '
                                                                                                                                                                                                                            'ale '
                                                                                                                                                                                                                            'sama '
                                                                                                                                                                                                                            'korelacja '
                                                                                                                                                                                                                            'nie '
                                                                                                                                                                                                                            'dowodzi '
                                                                                                                                                                                                                            'przyczyny '
                                                                                                                                                                                                                            'kosmicznej '
                                                                                                                                                                                                                            'ani '
                                                                                                                                                                                                                            'środowiskowej.',
 'The comparison uses only quality-filtered, one-to-one paired measurements.': 'Porównanie wykorzystuje wyłącznie '
                                                                               'pomiary filtrowane jakościowo i '
                                                                               'łączone jeden do jednego.',
 'The configured danger threshold is exceeded.': 'Skonfigurowany próg zagrożenia został przekroczony.',
 'The connected counters currently agree well': 'Podłączone liczniki są obecnie dobrze zgodne',
 'The counters disagree, so a device-specific effect is more likely': 'Liczniki są rozbieżne, więc bardziej '
                                                                      'prawdopodobny jest efekt specyficzny dla '
                                                                      'urządzenia',
 'The current radiation level is uncritical according to the selected thresholds.': 'Bieżący poziom promieniowania '
                                                                                    'jest niekrytyczny według '
                                                                                    'wybranych progów.',
 'The current value is below the configured warning threshold and within the usual local range.': 'Bieżąca wartość '
                                                                                                  'jest poniżej '
                                                                                                  'skonfigurowanego '
                                                                                                  'progu '
                                                                                                  'ostrzegawczego i '
                                                                                                  'mieści się w '
                                                                                                  'typowym lokalnym '
                                                                                                  'zakresie.',
 'The current value is within the configured warning range.': 'Bieżąca wartość znajduje się w skonfigurowanym zakresie '
                                                              'ostrzegawczym.',
 'The deviation is device-specific; the measurement-site profile remains normal': 'Odchylenie dotyczy konkretnego '
                                                                                  'urządzenia; profil miejsca pomiaru '
                                                                                  'pozostaje normalny',
 'The device baseline is available, but there are not enough recent measurements for a current comparison.': 'Poziom '
                                                                                                             'bazowy '
                                                                                                             'urządzenia '
                                                                                                             'jest '
                                                                                                             'dostępny, '
                                                                                                             'ale nie '
                                                                                                             'ma '
                                                                                                             'jeszcze '
                                                                                                             'wystarczającej '
                                                                                                             'liczby '
                                                                                                             'nowych '
                                                                                                             'pomiarów '
                                                                                                             'do '
                                                                                                             'bieżącego '
                                                                                                             'porównania.',
 'The device clock differs from Home Assistant time.': 'The device clock differs from Home Assistant time.',
 'The filtered counters disagree, so a device-specific effect is more likely': 'Przefiltrowane liczniki różnią się, '
                                                                               'więc bardziej prawdopodobny jest efekt '
                                                                               'urządzenia',
 'The learned baseline remains available. More current samples are required before the local comparison can be updated.': 'Wyuczony '
                                                                                                                          'poziom '
                                                                                                                          'bazowy '
                                                                                                                          'pozostaje '
                                                                                                                          'dostępny. '
                                                                                                                          'Do '
                                                                                                                          'aktualizacji '
                                                                                                                          'lokalnego '
                                                                                                                          'porównania '
                                                                                                                          'potrzebne '
                                                                                                                          'są '
                                                                                                                          'kolejne '
                                                                                                                          'bieżące '
                                                                                                                          'pomiary.',
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
 'The local background is still being learned, so no anomaly assessment is available yet.': 'Lokalne tło jest nadal '
                                                                                            'uczone, dlatego ocena '
                                                                                            'anomalii nie jest jeszcze '
                                                                                            'dostępna.',
 'The measurement-site baseline is {deviation:+.1f}% above its typical value': 'Poziom odniesienia miejsca pomiaru '
                                                                               'jest o {deviation:+.1f}% wyższy od '
                                                                               'wartości typowej',
 'The measurement-site profile combines both devices with quality weighting': 'Profil miejsca pomiaru łączy oba '
                                                                              'urządzenia z wagami jakości',
 'The measurement-site profile currently relies on one device': 'Profil miejsca pomiaru opiera się obecnie na jednym '
                                                                'urządzeniu',
 'The pressure model cannot prove cosmic radiation and never suppresses radiation warnings.': 'Model ciśnienia nie '
                                                                                              'może potwierdzić '
                                                                                              'promieniowania '
                                                                                              'kosmicznego i nigdy nie '
                                                                                              'wyłącza ostrzeżeń '
                                                                                              'radiacyjnych.',
 'The quality-filtered counter comparison currently agrees well': 'Porównanie liczników po filtracji jakościowej jest '
                                                                  'obecnie zgodne',
 'The recent 30-minute robust trend is rising': 'Odporny trend z ostatnich 30 minut rośnie',
 'The recent 30-minute trend is rising': 'Ostatni trend 30-minutowy rośnie',
 'The request could not be processed. Check the selected options.': 'Nie udało się przetworzyć żądania. Sprawdź '
                                                                    'wybrane opcje.',
 'The score combines time-window coverage, missing or irregular intervals, duplicate timestamps and optional-sensor coverage. It indicates how strongly the analysis can rely on the stored series.': 'Wynik '
                                                                                                                                                                                                      'łączy '
                                                                                                                                                                                                      'pokrycie '
                                                                                                                                                                                                      'okna '
                                                                                                                                                                                                      'czasowego, '
                                                                                                                                                                                                      'brakujące '
                                                                                                                                                                                                      'lub '
                                                                                                                                                                                                      'nieregularne '
                                                                                                                                                                                                      'odstępy, '
                                                                                                                                                                                                      'zduplikowane '
                                                                                                                                                                                                      'znaczniki '
                                                                                                                                                                                                      'czasu '
                                                                                                                                                                                                      'i '
                                                                                                                                                                                                      'pokrycie '
                                                                                                                                                                                                      'opcjonalnych '
                                                                                                                                                                                                      'czujników. '
                                                                                                                                                                                                      'Wskazuje, '
                                                                                                                                                                                                      'w '
                                                                                                                                                                                                      'jakim '
                                                                                                                                                                                                      'stopniu '
                                                                                                                                                                                                      'analiza '
                                                                                                                                                                                                      'może '
                                                                                                                                                                                                      'polegać '
                                                                                                                                                                                                      'na '
                                                                                                                                                                                                      'zapisanej '
                                                                                                                                                                                                      'serii.',
 'The serial connection is unstable.': 'Połączenie szeregowe jest niestabilne.',
 'The traffic light and events are relative anomaly indicators, not safety classifications.': 'Sygnalizacja i '
                                                                                              'zdarzenia są względnymi '
                                                                                              'wskaźnikami anomalii, a '
                                                                                              'nie klasyfikacją '
                                                                                              'bezpieczeństwa.',
 'The value is also within the usual range for this location.': 'Wartość znajduje się również w zwykłym zakresie dla '
                                                                'tej lokalizacji.',
 'The values most users need first': 'Wartości, których większość użytkowników potrzebuje najpierw',
 'These are statistical changes. They can indicate a location, geometry or environmental change, but do not identify the cause.': 'Są '
                                                                                                                                  'to '
                                                                                                                                  'zmiany '
                                                                                                                                  'statystyczne. '
                                                                                                                                  'Mogą '
                                                                                                                                  'wskazywać '
                                                                                                                                  'na '
                                                                                                                                  'zmianę '
                                                                                                                                  'miejsca, '
                                                                                                                                  'geometrii '
                                                                                                                                  'lub '
                                                                                                                                  'środowiska, '
                                                                                                                                  'ale '
                                                                                                                                  'nie '
                                                                                                                                  'określają '
                                                                                                                                  'przyczyny.',
 'These values describe the shape of the count distribution. They do not by themselves prove a physical cause or a calibration state.': 'Te '
                                                                                                                                        'wartości '
                                                                                                                                        'opisują '
                                                                                                                                        'kształt '
                                                                                                                                        'rozkładu '
                                                                                                                                        'zliczeń. '
                                                                                                                                        'Same '
                                                                                                                                        'w '
                                                                                                                                        'sobie '
                                                                                                                                        'nie '
                                                                                                                                        'dowodzą '
                                                                                                                                        'przyczyny '
                                                                                                                                        'fizycznej '
                                                                                                                                        'ani '
                                                                                                                                        'stanu '
                                                                                                                                        'kalibracji.',
 'This analysis detects unusual changes compared with the normal background at this location. It is not a danger classification; an unusual value can still be below the absolute warning threshold.': 'Ta '
                                                                                                                                                                                                       'analiza '
                                                                                                                                                                                                       'wykrywa '
                                                                                                                                                                                                       'nietypowe '
                                                                                                                                                                                                       'zmiany '
                                                                                                                                                                                                       'względem '
                                                                                                                                                                                                       'normalnego '
                                                                                                                                                                                                       'tła '
                                                                                                                                                                                                       'w '
                                                                                                                                                                                                       'tej '
                                                                                                                                                                                                       'lokalizacji. '
                                                                                                                                                                                                       'Nie '
                                                                                                                                                                                                       'jest '
                                                                                                                                                                                                       'klasyfikacją '
                                                                                                                                                                                                       'zagrożenia; '
                                                                                                                                                                                                       'nietypowa '
                                                                                                                                                                                                       'wartość '
                                                                                                                                                                                                       'może '
                                                                                                                                                                                                       'nadal '
                                                                                                                                                                                                       'pozostawać '
                                                                                                                                                                                                       'poniżej '
                                                                                                                                                                                                       'bezwzględnego '
                                                                                                                                                                                                       'progu '
                                                                                                                                                                                                       'ostrzegawczego.',
 'This cannot be undone. Delete all GMC history?': 'This cannot be undone. Delete all GMC history?',
 'This classification only compares the current measurement with the selected thresholds. It does not compare the value with the usual background at this location.': 'Ta '
                                                                                                                                                                      'klasyfikacja '
                                                                                                                                                                      'porównuje '
                                                                                                                                                                      'bieżący '
                                                                                                                                                                      'pomiar '
                                                                                                                                                                      'wyłącznie '
                                                                                                                                                                      'z '
                                                                                                                                                                      'wybranymi '
                                                                                                                                                                      'progami. '
                                                                                                                                                                      'Nie '
                                                                                                                                                                      'porównuje '
                                                                                                                                                                      'go '
                                                                                                                                                                      'ze '
                                                                                                                                                                      'zwykłym '
                                                                                                                                                                      'tłem '
                                                                                                                                                                      'w '
                                                                                                                                                                      'tej '
                                                                                                                                                                      'lokalizacji.',
 'This factor is only a relative device comparison and is not an absolute radiation calibration.': 'This factor is '
                                                                                                   'only a relative '
                                                                                                   'device comparison '
                                                                                                   'and is not an '
                                                                                                   'absolute radiation '
                                                                                                   'calibration.',
 'This report is descriptive and is not a radiation-safety classification.': 'Ten raport ma charakter opisowy i nie '
                                                                             'jest klasyfikacją bezpieczeństwa '
                                                                             'radiologicznego.',
 'Thresholds can be changed in the add-on configuration.': 'Progi można zmienić w konfiguracji dodatku.',
 'Thu': 'Cz',
 'Thursday': 'Czwartek',
 'Tilted': 'Tilted',
 'Time series': 'Szereg czasowy',
 'Time series, Poisson comparison and weekday/hour heatmap': 'Szereg czasowy, porównanie Poissona i mapa cieplna '
                                                             'dzień/godzina',
 'Time-series PNG': 'Szereg czasowy PNG',
 'Timestamp diagnostics': 'Diagnostyka znaczników czasu',
 'Timezone': 'Strefa czasowa',
 'Today so far bundle': 'Pakiet dzisiejszego dnia do tej pory',
 'Too few pressure/CPM pairs': 'Zbyt mało par ciśnienie/CPM',
 'Too few valid paired measurements for a reliable device comparison': 'Zbyt mało prawidłowych par pomiarów do '
                                                                       'wiarygodnego porównania',
 'Too little or too fragmented for strong conclusions': 'Za mało danych lub zbyt duże rozdrobnienie, aby wyciągać '
                                                        'mocne wnioski',
 'Trend (30 min)': 'Trend (30 min)',
 'Tue': 'Wt',
 'Tuesday': 'Wtorek',
 'Type DELETE ALL GMC HISTORY to confirm': 'Type DELETE ALL GMC HISTORY to confirm',
 'Type RESTORE to confirm': 'Wpisz RESTORE, aby potwierdzić',
 'Typical for {weekday} at {hour}:00': 'Typowe dla {weekday} o {hour}:00',
 'USB down': 'Pionowo, USB u dołu',
 'USB left': 'Pionowo, USB po lewej',
 'USB right': 'Pionowo, USB po prawej',
 'USB up': 'Pionowo, USB u góry',
 'UTC timestamp': 'Znacznik czasu UTC',
 'Unavailable': 'Niedostępna',
 'Unconfirmed values since bridge start': 'Unconfirmed values since bridge start',
 'Uncritical': 'Niekrytyczny',
 'Uncritical: below warning threshold': 'Niekrytyczny: poniżej progu ostrzegawczego',
 'Unknown': 'Nieznany',
 'Unknown GMC': 'Nieznane urządzenie GMC',
 'Unknown report device': 'Nieznane urządzenie raportu',
 'Unknown serial device': 'Unknown serial device',
 'Unstable': 'Niestabilny',
 'Unsupported report format': 'Nieobsługiwany format raportu',
 'Upload errors': 'Błędy wysyłania',
 'Upload errors since start': 'Błędy wysyłania od uruchomienia',
 'Upload failed': 'Wysyłanie nie powiodło się',
 'Upload successful': 'Wysyłanie zakończone powodzeniem',
 'Uploading': 'Wysyłanie',
 'Upright': 'Upright',
 'Use this as context only and review longer periods before drawing conclusions.': 'Traktuj to wyłącznie jako kontekst '
                                                                                   'i przeanalizuj dłuższe okresy '
                                                                                   'przed wyciągnięciem wniosków.',
 'Valid measurements': 'Prawidłowe pomiary',
 'Variance / mean': 'Wariancja / średnia',
 'Very close to Poisson-like spread': 'Bardzo blisko rozrzutu typu Poissona',
 'Very complete 24 h data window': 'Bardzo kompletne 24-godzinne okno danych',
 'Very strong linear relationship': 'Bardzo silna zależność liniowa',
 'Very weak linear relationship': 'Bardzo słaba zależność liniowa',
 'Voltage': 'Napięcie',
 'Voltage Errors Since Start': 'Błędy napięcia od uruchomienia',
 'Voltage [V]': 'Napięcie [V]',
 'Voltage correlation': 'Korelacja z napięciem',
 'Waiting for enough recent measurements': 'Oczekiwanie na wystarczającą liczbę nowych pomiarów',
 'Waiting for first upload': 'Oczekiwanie na pierwsze wysłanie',
 'Waiting for recent measurements': 'Oczekiwanie na nowe pomiary',
 'Waiting for the first accepted measurement': 'Waiting for the first accepted measurement',
 'Warning': 'Ostrzeżenie',
 'Warning from {warning} s; critical from {critical} s': 'Ostrzeżenie od {warning} s; krytyczne od {critical} s',
 'Warning threshold exceeded': 'Próg ostrzegawczy został przekroczony',
 'Warning thresholds': 'Progi ostrzegawcze',
 'Weak linear relationship': 'Słaba zależność liniowa',
 'Weather pressure sources disagree': 'Źródła ciśnienia pogodowego są rozbieżne',
 'Wed': 'Śr',
 'Wednesday': 'Środa',
 'Weekday': 'Dzień tygodnia',
 'Weekday/hour heatmap': 'Mapa cieplna dzień/godzina',
 'What does the historical trend mean?': 'Co oznacza trend historyczny?',
 'What each report preserves and how periods are defined': 'Co zawiera każdy raport i jak definiowane są okresy',
 'What should I do?': 'Co należy zrobić?',
 'What this assessment means': 'Znaczenie tej oceny',
 'Why are Poisson values shown?': 'Dlaczego wyświetlane są wartości Poissona?',
 'Why is this assessment shown?': 'Dlaczego wyświetlana jest ta ocena?',
 'Within local background range': 'W zakresie lokalnego tła',
 'Within normal statistical variation': 'W granicach normalnej zmienności statystycznej',
 'Within the usual local range': 'W zwykłym lokalnym zakresie',
 'Within warning range': 'W zakresie ostrzegawczym',
 'Yellow': 'Żółty',
 'Z-score = (latest CPM − 24 h mean) / 24 h standard deviation.': 'Wynik Z = (ostatnie CPM − średnia 24 h) / '
                                                                  'odchylenie standardowe 24 h.',
 'Z-score formula explanation': 'Wynik Z = (ostatnie CPM − średnia 24 h) / odchylenie standardowe 24 h.',
 'complete and regularly spaced data': 'kompletne i regularnie rozmieszczone dane',
 'confirmations': 'confirmations',
 'counting uncertainty {value:.2f}%': 'counting uncertainty {value:.2f}%',
 'coverage': 'pokrycie',
 'daily values': 'wartości dzienne',
 'days': 'dni',
 'duplicates / clock regressions': 'duplikaty / cofnięcia zegara',
 'entity patterns': 'entity patterns',
 'errors': 'errors',
 'estimated signal probability': 'szacowane prawdopodobieństwo sygnału',
 'excluded measurements': 'wykluczone pomiary',
 'longest gap {value} s': 'najdłuższa luka {value} s',
 'measurements': 'measurements',
 'minimum sample coverage': 'minimalne pokrycie próbek',
 'n={count} paired samples': 'n={count} par pomiarów',
 'n={count} · {coverage:.1f}% coverage': 'n={count} · pokrycie {coverage:.1f}%',
 'paired samples': 'pary pomiarów',
 'reconnects': 'reconnects',
 'relative to baseline': 'względem poziomu odniesienia',
 'score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s': 'ocena {score:.1f}/100 · pokrycie '
                                                                           '{coverage:.1f}% · najdłuższa luka {gap} s',
 'short / long intervals': 'krótkie / długie odstępy',
 'since the current bridge start': 'since the current bridge start',
 'temperature coverage {value}%': 'pokrycie temperatury {value}%',
 'unknown': 'nieznane',
 'valid hourly values': 'prawidłowe wartości godzinowe',
 'valid paired samples': 'prawidłowe pary pomiarów',
 'voltage coverage {value}%': 'pokrycie napięcia {value}%',
 'write errors since app start': 'write errors since app start',
 '{before:.2f} → {after:.2f} CPM · {sigma:.1f}σ · {hours} h persistent': '{before:.2f} → {after:.2f} CPM · '
                                                                         '{sigma:.1f}σ · {hours} h persistent',
 '{check_type} result cached for {seconds} s · schema v{schema}': 'Wynik {check_type} w pamięci podręcznej przez '
                                                                  '{seconds} s · schemat v{schema}',
 '{connected} connected · {disconnected} disconnected': '{connected} connected · {disconnected} disconnected',
 '{count} implausible measurements were excluded from the assessment': 'Z oceny wykluczono {count} nieprawdopodobnych '
                                                                       'pomiarów',
 '{count} measurements': '{count} pomiarów',
 '{count} measurements and {events} events were removed.': '{count} measurements and {events} events were removed.',
 '{events} events · {diagnostics} diagnostics': '{events} events · {diagnostics} diagnostics',
 '{gyro_note} History retention: {days} days. Daily periods are local calendar days; weekly periods are ISO weeks from Monday through Sunday.': '{gyro_note} '
                                                                                                                                                'Okres '
                                                                                                                                                'przechowywania '
                                                                                                                                                'historii: '
                                                                                                                                                '{days} '
                                                                                                                                                'dni. '
                                                                                                                                                'Okresy '
                                                                                                                                                'dzienne '
                                                                                                                                                'to '
                                                                                                                                                'lokalne '
                                                                                                                                                'dni '
                                                                                                                                                'kalendarzowe; '
                                                                                                                                                'okresy '
                                                                                                                                                'tygodniowe '
                                                                                                                                                'to '
                                                                                                                                                'tygodnie '
                                                                                                                                                'ISO '
                                                                                                                                                'od '
                                                                                                                                                'poniedziałku '
                                                                                                                                                'do '
                                                                                                                                                'niedzieli.',
 '{model} — Radiation monitoring report': '{model} — Raport monitorowania promieniowania',
 '{seconds} seconds ago': '{seconds} seconds ago',
 '{value:g} h': '{value:g} h',
 '{value:g} min': '{value:g} min',
 '{value} clock regressions observed': 'zaobserwowano {value} cofnięć zegara',
 '{value} duplicate timestamps observed': 'zaobserwowano {value} zduplikowanych znaczników czasu',
 '{value} long intervals': '{value} długich odstępów',
 '{value} unusually short intervals': '{value} nietypowo krótkich odstępów',
 '{value} vs local baseline': '{value} względem lokalnego poziomu bazowego',
 '{value}% time-window coverage': 'pokrycie okna czasowego {value}%'}

# Runtime presentation templates added in 7.1.4.
CATALOG.update({
    'Comparison confidence: {confidence}': 'Pewność porównania: {confidence}',
    'Confidence: {confidence}': 'Poziom ufności: {confidence}',
    'Status': 'Status',
    'Typical background': 'Typowe tło',
    'Valid paired samples': 'Prawidłowe pary pomiarowe',
    'Warning from {warning:g} s; critical from {critical:g} s': 'Ostrzeżenie od {warning:g} s; stan krytyczny od {critical:g} s',
    'valid hourly values · {days:.1f} days · {span:.1f} hPa': 'prawidłowe wartości godzinowe · {days:.1f} dni · {span:.1f} hPa',
    '{a:+.1f}% / {b:+.1f}%': '{a:+.1f}% / {b:+.1f}%',
    '{b} × factor → {a}': '{b} × współczynnik → {a}',
    '{content}': '{content}',
    '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)': '{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)',
    '{days} days': '{days} dni',
    '{dose:.3f} µSv/h': '{dose:.3f} µSv/h',
    '{first} {second}': '{first} {second}',
    '{from_value} → {to_value}': '{from_value} → {to_value}',
    '{note} · n={samples}': '{note} · n={samples}',
    '{pairs} valid paired samples': '{pairs} prawidłowych par pomiarowych',
    '{pairs} valid paired samples · counting uncertainty {value:.2f}%': '{pairs} prawidłowych par pomiarowych · niepewność zliczania {value:.2f}%',
    '{probability:.0f}% estimated signal probability': '{probability:.0f} % szacowanego prawdopodobieństwa sygnału',
    '{span:.0f} {days_label} · {count} {daily_label}': '{span:.0f} {days_label} · {count} {daily_label}',
    '{start}–{end} °C · {samples} Samples': '{start}–{end} °C · {samples} pomiarów',
    '{trend:+.1f} CPM': '{trend:+.1f} CPM',
    '{value:g} µSv/h': '{value:g} µSv/h',
    'Last uploaded CPM': 'Ostatnio wysłane CPM',
    'Last uploaded ACPM': 'Ostatnio wysłane ACPM',
    'GMCMap last uploaded ACPM': 'Ostatnio wysłane ACPM do GMCMap',
    'GMCMap ACPM accepted samples': 'Zaakceptowane próbki dla ACPM GMCMap',
    'ACPM is the average of all accepted CPM readings since the current app measurement session began.': 'ACPM jest średnią wszystkich zaakceptowanych odczytów CPM od rozpoczęcia bieżącej sesji pomiarowej aplikacji.',
    'User manual': 'Podręcznik użytkownika',
    'Open user manual PDF': 'Otwórz podręcznik użytkownika w PDF',
    'User manual is not available': 'Podręcznik użytkownika jest niedostępny',
})

# Version 8.2.1 report and history labels.
CATALOG.update({
    'Accepted measurements [count]': 'Zaakceptowane pomiary [liczba]',
    'Local hour [h]': 'Godzina lokalna [h]',
    'Mean count rate [CPM]': 'Średnia częstość zliczeń [CPM]',
    'Radiation Monitoring': 'Monitorowanie promieniowania',
    'Rejected raw value': 'Odrzucona wartość surowa',
})


# Version 8.2.1 complete runtime localization.
CATALOG.update({
    'The recent level differs from counting noise with {probability:.2f}% statistical confidence': 'Ostatni poziom różni się od szumu zliczeń z ufnością statystyczną {probability:.2f} %',
    'A comparable or more extreme hourly level occurred about once in {rarity:.1f} historical hours': 'Porównywalny lub bardziej skrajny poziom godzinowy występował historycznie mniej więcej raz na {rarity:.1f} godziny',
})
