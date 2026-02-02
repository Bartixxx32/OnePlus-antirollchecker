# OnePlus Anti-Rollback (ARB) Checker

Automated ARB (Anti-Rollback) index tracker for OnePlus devices. This repository monitors firmware updates and tracks ARB changes over time.

**Website:** [https://bartixxx32.github.io/OnePlus-antirollchecker/](https://bartixxx32.github.io/OnePlus-antirollchecker/)

## 📊 Current Status


> [!IMPORTANT]
> This status is updated automatically by GitHub Actions. Some device/region combinations may not be available and will show as "Waiting for scan...".

## 📈 Legend

- ✅ **Safe**: ARB = 0 (downgrade possible)
- ❌ **Protected**: ARB > 0 (anti-rollback active)

## 🛠️ Credits
- **Payload Extraction**: [otaripper](https://github.com/syedinsaf/otaripper) by [syedinsaf](https://github.com/syedinsaf) - for fast and reliable OTA extraction.

## 🤖 Workflow Status
[![Check ARB](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml/badge.svg)](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml)
