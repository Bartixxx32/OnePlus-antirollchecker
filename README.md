# OnePlus Anti-Rollback (ARB) Checker

Automated ARB (Anti-Rollback) index tracker for OnePlus devices. This repository monitors firmware updates and tracks ARB changes over time.

## 📊 Current Status & History

### OnePlus 15 - China (PLK110)

| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |
|---------|-----------|-------------|------------|--------------|--------|------|
| PLK110_16.0.3.504(CN01) | **1** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | 🟢 Current | ❌ |
| PLK110_16.0.3.503(CN01) | **0** | Major: **3**, Minor: **0** | 2026-01-27 | 2026-01-27 | ⚫ Archived | ✅ |

---

---

---

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
