# GMC Radiation Monitor 8.3.5

## Detector profiles instead of duplicated tube settings

Version 8.3.5 introduces explicit detector presets and separates single-tube and dual-tube behavior.

- `gmc_320_plus_v4` represents one physical M4011 tube.
- `gmc_500_plus` represents the M4011 primary tube plus the SI-3BG second/high-dose tube.
- `custom_single` and `custom_dual` remain available for individually calibrated hardware.
- `auto` keeps older configurations compatible by inferring the profile conservatively from the configured model name.

The GMC-320 Plus V4 preset supplies these application working values automatically:

- M4011 tube;
- 154 CPM per µSv/h;
- 120 µs detector dead time;
- non-paralyzable correction model;
- 50,000 CPM reliable working limit;
- 20% conversion-factor uncertainty.

These are predefined working values, not a traceable calibration certificate. Explicit values in the device configuration override the preset and are labelled as customized.

## Cleaner Home Assistant configuration

The duplicated `low_dose_*` option block has been removed from the Supervisor form. The normal device calibration fields now describe:

- the only tube on a single-tube counter; or
- the primary/low-dose tube on a dual-tube counter.

Only the `high_dose_*` fields remain for the second tube of a dual-tube device. Their labels and descriptions now state clearly that they do not apply to the GMC-320.

Existing 8.3.4 `low_dose_*` values are still accepted by the runtime parser as a migration source. Matching GMC-320 and GMC-500+ working values are converted to the new predefined profiles automatically.

## GMC-320 and GMC-500+ safeguards

- The GMC-320 preset always uses single-tube mode.
- Stale SI-3BG or dual-tube fields are ignored for a GMC-320 instead of creating a fictitious second detector.
- The GMC-500+ preset uses M4011 as the primary profile and creates an SI-3BG second profile without inventing a dose-conversion factor.
- A derived SI-3BG dose remains unavailable until a verified, device-specific conversion factor is entered.

## Dashboard and translation cleanup

The Detector and calibration card no longer repeats the same single-tube values in multiple summary blocks. Single-tube devices show one physical detector and one profile card. Dual-tube devices show the primary and second tube separately, along with the active channel and switch information.

Configuration labels and dashboard terms were revised in all eight bundled languages. German terminology now consistently uses **Zählrohr**, **Ein-Zählrohr-Profil** and **Zwei-Zählrohr-Gerät** instead of mixed English/German Dual-Tube wording.

## Retained reporting and history features

The existing professional five-page report structure remains unchanged. Reports continue to label the count-rate axis as `Count rate [CPM]` and describe the instrument result as a combined beta/gamma response where this applies to the detector. History retention and purge controls remain governed by `history_management_enabled`.
