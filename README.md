# OnePlus Anti-Rollback (ARB) Checker

This repository automatically tracks the Anti-Rollback (ARB) index for OnePlus devices by analyzing the `xbl_config.img` from the latest OxygenOS firmware.

## 📊 Current Status

| Device | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|--------|-------|------------------|-----------|-------------|--------------|------|
| OnePlus 15 (Global) | OnePlus 15 | **<!-- VERSION_START_GLO -->Waiting for scan...<!-- VERSION_END_GLO -->** | **<!-- ARB_START_GLO -->-<!-- ARB_END_GLO -->** | Major: **<!-- MAJOR_START_GLO -->-<!-- MAJOR_END_GLO -->**, Minor: **<!-- MINOR_START_GLO -->-<!-- MINOR_END_GLO -->** | <!-- DATE_START_GLO -->-<!-- DATE_END_GLO --> | <!-- STATUS_START_GLO -->-<!-- STATUS_END_GLO --> |
| OnePlus 15 (Europe) | OnePlus 15 | **<!-- VERSION_START_EU -->Waiting for scan...<!-- VERSION_END_EU -->** | **<!-- ARB_START_EU -->-<!-- ARB_END_EU -->** | Major: **<!-- MAJOR_START_EU -->-<!-- MAJOR_END_EU -->**, Minor: **<!-- MINOR_START_EU -->-<!-- MINOR_END_EU -->** | <!-- DATE_START_EU -->-<!-- DATE_END_EU --> | <!-- STATUS_START_EU -->-<!-- STATUS_END_EU --> |
| OnePlus 15 (North America) | OnePlus 15 | **<!-- VERSION_START_NA -->Waiting for scan...<!-- VERSION_END_NA -->** | **<!-- ARB_START_NA -->-<!-- ARB_END_NA -->** | Major: **<!-- MAJOR_START_NA -->-<!-- MAJOR_END_NA -->**, Minor: **<!-- MINOR_START_NA -->-<!-- MINOR_END_NA -->** | <!-- DATE_START_NA -->-<!-- DATE_END_NA --> | <!-- STATUS_START_NA -->-<!-- STATUS_END_NA --> |
| OnePlus 15 (India) | OnePlus 15 | **<!-- VERSION_START_IN -->Waiting for scan...<!-- VERSION_END_IN -->** | **<!-- ARB_START_IN -->-<!-- ARB_END_IN -->** | Major: **<!-- MAJOR_START_IN -->-<!-- MAJOR_END_IN -->**, Minor: **<!-- MINOR_START_IN -->-<!-- MINOR_END_IN -->** | <!-- DATE_START_IN -->-<!-- DATE_END_IN --> | <!-- STATUS_START_IN -->-<!-- STATUS_END_IN --> |

> [!NOTE]
> This status is updated automatically by GitHub Actions.

## 🛠 How it works
1.  **Check Update**: Periodically checks for new OxygenOS firmware using the `oosdownloader` API.
2.  **Download & Extract**: If a new version is found, it downloads the firmware and extracts the `xbl_config.img` partition (using `payload-dumper-go`).
3.  **Analyze**: Uses `arbextract` to read the ARB index from the image.
4.  **Report**: Updates this README with the latest findings.

## 🤖 Workflow Status
[![Check ARB](https://github.com/Bartixxx32/Oneplus-antiroackchecker/actions/workflows/check_arb.yml/badge.svg)](https://github.com/Bartixxx32/Oneplus-antiroackchecker/actions/workflows/check_arb.yml)
