# OnePlus Anti-Rollback (ARB) Checker

Automated ARB (Anti-Rollback) index tracker for OnePlus devices. This repository monitors firmware updates and tracks ARB changes over time.

## 📊 Current Status

### OnePlus 15

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|--------|-------|------------------|-----------|-------------|--------------|------|
| Global | CPH2747 | CPH2747_16.0.3.501(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | ✅ |
| Europe | CPH2747 | CPH2747_16.0.3.501(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | ✅ |
| India | CPH2745 | CPH2745_16.0.3.501(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | ✅ |
| China | PLK110 | PLK110_16.0.3.503(CN01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | ✅ |

---

### OnePlus 15R

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|--------|-------|------------------|-----------|-------------|--------------|------|
| Global | CPH2741 | CPH2769_16.0.2.401(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | ✅ |
| Europe | CPH2741 | CPH2769_16.0.2.401(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | ✅ |
| India | CPH2741 | CPH2767_16.0.3.501(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | ✅ |

---

### OnePlus 13

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|--------|-------|------------------|-----------|-------------|--------------|------|
| Global | CPH2649 | CPH2653_16.0.3.501(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | ❌ |
| Europe | CPH2649 | CPH2653_16.0.3.501(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | ❌ |
| India | CPH2649 | CPH2649_16.0.3.501(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | ❌ |
| China | PJZ110 | PJZ110_16.0.3.501(CN01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | ❌ |

---

### OnePlus 12

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|--------|-------|------------------|-----------|-------------|--------------|------|
| Global | CPH2573 | CPH2581_16.0.3.500(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | ❌ |
| Europe | CPH2573 | CPH2581_16.0.3.500(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | ❌ |
| India | CPH2573 | CPH2573_16.0.3.500(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | ❌ |
| China | PJD110 | PJD110_16.0.1.300(CN01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | ✅ |


> [!IMPORTANT]
> This status is updated automatically by GitHub Actions. Some device/region combinations may not be available and will show as "Waiting for scan...".

## 📈 Legend

- ✅ **Safe**: ARB = 0 (downgrade possible)
- ❌ **Protected**: ARB > 0 (anti-rollback active)

## 🤖 Workflow Status
[![Check ARB](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml/badge.svg)](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml)
