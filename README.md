# OnePlus Anti-Rollback (ARB) Checker

Automated ARB (Anti-Rollback) index tracker for OnePlus devices. This repository monitors firmware updates and tracks ARB changes over time.

**Website:** [https://bartixxx32.github.io/OnePlus-antirollchecker/](https://bartixxx32.github.io/OnePlus-antirollchecker/)

## 📊 Current Status

## 🤖 On-Demand ARB Checker

You can check the ARB index of any OnePlus Ozip/Zip URL manually using our automated workflow.

### How to use:
1. Go to the [Actions Tab](https://github.com/Bartixxx32/OnePlus-antirollchecker/actions).
2. Select **"Manual ARB Check"** from the sidebar.
3. Click **"Run workflow"**.
4. Paste the **Firmware Download URL** (direct link preferred, e.g., from Oxygen Updater).
5. Click **Run workflow**.

The bot will extract the payload, check the ARB index, and post the result as a comment on the workflow run summary (or you can view the logs).

---

## Credits

- **Payload Extraction**: [otaripper](https://github.com/syedinsaf/otaripper) by syedinsaf
- **Fallback Extraction**: [payload-dumper-go](https://github.com/ssut/payload-dumper-go) by ssut
- **ARB Extraction**: [arbextract](https://github.com/koaaN/arbextract) by koaaN

---
*Last updated: 2026-02-04 00:34 UTC*