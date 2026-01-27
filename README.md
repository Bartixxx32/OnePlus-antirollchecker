# OnePlus Anti-Rollback (ARB) Checker

Automated ARB (Anti-Rollback) index tracker for OnePlus devices. This repository monitors firmware updates and tracks ARB changes over time.

## 📊 Current Status & History

### OnePlus 15 - Global (CPH2747)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2747_16.0.3.501(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ✅ |

### OnePlus 15 - Europe (CPH2747)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2747_16.0.3.501(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ✅ |

### OnePlus 15 - India (CPH2745)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2745_16.0.3.501(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ✅ |

---

### OnePlus 15R - Global (CPH2741)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2769_16.0.2.401(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ✅ |

### OnePlus 15R - Europe (CPH2741)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2769_16.0.2.401(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ✅ |

### OnePlus 15R - India (CPH2741)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2767_16.0.3.501(EX01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ✅ |

---

### OnePlus 13 - Global (CPH2649)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2653_16.0.3.501(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ❌ |

### OnePlus 13 - Europe (CPH2649)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2653_16.0.3.501(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ❌ |

### OnePlus 13 - India (CPH2649)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2649_16.0.3.501(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ❌ |

---

### OnePlus 12 - Global (CPH2573)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2581_16.0.3.500(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ❌ |

### OnePlus 12 - Europe (CPH2573)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2581_16.0.3.500(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ❌ |

### OnePlus 12 - India (CPH2573)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| CPH2573_16.0.3.500(EX01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ❌ |

### OnePlus 12 - China (PJD110)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
|  | **0** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ✅ |

---

## 📈 Legend

- 🟢 **Current**: Latest firmware detected
- ⚫ **Archived**: Previous firmware version
- ✅ **Safe**: ARB = 0 (downgrade possible)
- ❌ **Protected**: ARB > 0 (anti-rollback active)

## 🛠 How it works

1. **Check Update**: Checks for new firmware using the `oosdownloader` API
2. **Download & Extract**: Downloads firmware and extracts `xbl_config.img`
3. **Analyze**: Uses `arbextract` to read ARB index
4. **Store History**: Saves to JSON in `data/history/`
5. **Generate README**: Rebuilds this document from JSON

## 🤖 Workflow Status
[![Check ARB](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml/badge.svg)](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml)
