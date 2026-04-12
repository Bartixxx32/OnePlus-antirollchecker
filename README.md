# OnePlus Anti-Rollback (ARB) Checker

<!-- Badges -->
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Bartixxx32/OnePlus-antirollchecker/check_arb.yml?style=flat-square&logo=github&label=ARB%20Checking)
![GitHub stars](https://img.shields.io/github/stars/Bartixxx32/OnePlus-antirollchecker?style=flat-square&color=yellow)
![GitHub forks](https://img.shields.io/github/forks/Bartixxx32/OnePlus-antirollchecker?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/Bartixxx32/OnePlus-antirollchecker?style=flat-square)
![Python Version](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Views](https://visitor-badge.laobi.icu/badge?page_id=Bartixxx32.OnePlus-antirollchecker)
---

Automated ARB (Anti-Rollback) index tracker for OnePlus devices. This repository monitors firmware updates and tracks ARB changes over time.

**🌐 ARB Info Website:** [https://oparb.pages.dev/](https://oparb.pages.dev/)

## 🤖 OnePlus ARB Checker Bot

Our Telegram bot allows you to check the Anti-Rollback (ARB) index of any OnePlus firmware instantly.

- **Bot Username:** [@oparbcheckerbot](https://t.me/oparbcheckerbot)
- **Group:** [@oneplusarbchecker](https://t.me/oneplusarbchecker)
- **Supported Commands:**
  - `/check <url>` - Analyze a firmware file (Direct Download Link required)
  - `/download <device> [region]` - Fetch latest firmware & auto-check ARB
  - `/devicestatus <device>` - Show current firmware & ARB info
  - `/latest` - Show the 5 most recently discovered firmwares
  - `/help` - Show usage instructions
  - `/about` - Bot version and stats

> **Note:** The bot **only** works within the [@oneplusarbchecker](https://t.me/oneplusarbchecker) group. DM checks are disabled. Checks are powered by GitHub Actions and may take a minute to process.

### 🍻 Support the Project
If you find this tool helpful, consider buying me a beer! Your support keeps the updates coming.

[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20beer&emoji=%F0%9F%8D%BA&slug=bartixxx32&button_colour=FFDD00&font_colour=000000&font_family=Comic&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/bartixxx32)

## 📊 Current Status

### OnePlus 15

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2747 | CPH2747_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>6086e417cba87486cceab28f08635b19</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| Europe | CPH2747 | CPH2747_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>529891ce7bbbaf52357a7fdee83431ff</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| India | CPH2745 | CPH2745_16.0.5.702(EX01)<br><details><summary>MD5</summary><code>d4bd922b0f7b55021795751e74bbf009</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| China | PLK110 | PLK110_16.0.5.701(CN01)<br><details><summary>MD5</summary><code>9e9688532ff5ec1eb19b4ca9de363199</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2747_16.0.3.503(EX01)<br><details><summary>MD5</summary><code>1f617649e2d5d76a5863776bb65100c0</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-16 | ✅ Safe |
| CPH2747_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>4c9d70c8dbe2b867a7e497aa063acb71</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-08 | ✅ Safe |
| CPH2747_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>a5ddbd8ae6c4a86e4eac062520ac5d0a</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-11 | ✅ Safe |
| CPH2747_16.0.1.303(EX01)<br><details><summary>MD5</summary><code>e6da9981cab374beeae4ddbba4e8d083</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2747_16.0.3.503(EX01)<br><details><summary>MD5</summary><code>aead3e10aadb3ff506ae0673a110f8c6</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2747_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>fbaeb7dc54da345cf94aeeced0af502c</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-08 | ✅ Safe |
| CPH2747_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>9e39c1366c03ff0f8f50a8d49a252ad7</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2747_16.0.1.303(EX01)<br><details><summary>MD5</summary><code>2ff1781d46561bf44a0eb40c128390a4</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-06 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2745_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>b01f22e57655584a93a7e6051752f4c4</code></details> | 0 | Major: 3, Minor: 0 | 2026-04-06 | ✅ Safe |
| CPH2745_16.0.3.503(EX01)<br><details><summary>MD5</summary><code>e9e6a68cc908913ac7a03578dc41366d</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-11 | ✅ Safe |
| CPH2745_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>3b72808a5cd0d8133fb7311e53f5f7e3</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2745_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>45404f2227169e79b328fde3c008aef6</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-11 | ✅ Safe |
| CPH2745_16.0.1.305(EX01)<br><details><summary>MD5</summary><code>2b6eca2467b6456e921574278b1d3a89</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| CPH2745_16.0.1.303(EX01)<br><details><summary>MD5</summary><code>3e1530d09182e7a10cd673b6d142d0fc</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PLK110_16.0.3.503(CN01)<br><details><summary>MD5</summary><code>0912b44f2bcc36beec783941e1016c47</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| PLK110_16.0.3.502(CN01)<br><details><summary>MD5</summary><code>2620712413a1f04dfae81b64ec32eb6e</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| PLK110_16.0.2.402(CN01)<br><details><summary>MD5</summary><code>6e5ecbdbd9f49e6e5d054340f52b9641</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-26 | ✅ Safe |
| PLK110_16.0.2.401(CN01)<br><details><summary>MD5</summary><code>6866e32183304023149907b7899c1963</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| PLK110_16.0.1.301(CN01)<br><details><summary>MD5</summary><code>18f1654b5f21e2af8c19190042a3c612</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>


---

### OnePlus 15R

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2769 | CPH2769_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>ffb1c3aa990044f327a8171e6162af21</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| Europe | CPH2769 | CPH2769_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>8ed18c461d884a4b5108147840644bb7</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| India | CPH2767 | CPH2767_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>13f5c6f6338480d641c381e2644dd3f7</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2769_16.0.3.503(EX01)<br><details><summary>MD5</summary><code>bbf8456ba035fd52691af46cf4d87222</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2769_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>cb319baa6d71168d9743f4b0492859f5</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2769_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>557df71dadd39f65968ad8bbc0ce2293</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-06 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2769_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>44828fb8b432f3c38dadef0d7cb7f400</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-29 | ✅ Safe |
| CPH2769_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>77e4748592f464726b8d72f6614d2875</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2767_16.0.3.503(EX01)<br><details><summary>MD5</summary><code>2c9829fafdd4921812f293a4e3ed2d26</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2767_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>b66486ede893305d3c4b297cef45d3f2</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2767_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>310d2f5237de8789f0cb8f886b4c0bb4</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2767_16.0.1.305(EX01)<br><details><summary>MD5</summary><code>40f81334dddadd8e1917148c57cbc713</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>


---

### OnePlus 13

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2653 | CPH2653_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>385877a9463d7b5de2f5a2ffea4a12d6</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| Europe | CPH2653 | CPH2653_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>23318bec5be6849803c95d47c0e7d8f8</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| India | CPH2649 | CPH2649_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>6998133c921d754bf06e693455aabcdc</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| North America | CPH2655 | CPH2655_15.0.0.832(EX01)<br><details><summary>MD5</summary><code>7d0ce94be24263393454ae140889a523</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| China | PJZ110 | PJZ110_16.0.5.702(CN01)<br><details><summary>MD5</summary><code>e79027edfae91a2594e965cc21b14f99</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2653_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>55382e1f872388d09a539d64ce09d65e</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-24 | ❌ Protected |
| CPH2653_16.0.2.402(EX01)<br><details><summary>MD5</summary><code>515f5110ca780fda710ef1ff1ad9f100</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-11 | ✅ Safe |
| CPH2653_16.0.1.304(EX01)<br><details><summary>MD5</summary><code>e854bde9b2f472d1cfb499c886b1cbe9</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-06 | ✅ Safe |
| CPH2653_16.0.0.210(EX01)<br><details><summary>MD5</summary><code>2dfc7934f7610af104e094e1a8f43cb1</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2653_15.0.0.864(EX01)<br><details><summary>MD5</summary><code>fdde59c8fb76a88491b44d44b8d2797d</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2653_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>4a5640ac2917ad8baeb334b286572b46</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-24 | ❌ Protected |
| CPH2653_16.0.2.402(EX01)<br><details><summary>MD5</summary><code>8a63e3f165b7ed13be5bb2bf6517e365</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |
| CPH2653_16.0.1.304(EX01)<br><details><summary>MD5</summary><code>1c8603874051bc2dd5e5d001ffaf3fe2</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2653_15.0.0.864(EX01)<br><details><summary>MD5</summary><code>eee24307e73dd6ec6d2abbef660e1b42</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2653_15.0.0.860(EX01)<br><details><summary>MD5</summary><code>c702554a85e63c7afd930241112ea3bc</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2649_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>c5987fd6c9052e39b5dce573883b2f97</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-16 | ❌ Protected |
| CPH2649_16.0.2.402(EX01)<br><details><summary>MD5</summary><code>b8bb28a60b49b828a5e5fb93a9a76c55</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2649_16.0.1.304(EX01)<br><details><summary>MD5</summary><code>d9b18f26264785200dfcdf42e625338c</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-04 | ✅ Safe |
| CPH2649_16.0.0.210(EX01)<br><details><summary>MD5</summary><code>9207f5e5aa09b192946b30026f6569d3</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| CPH2649_15.0.0.860(EX01)<br><details><summary>MD5</summary><code>7792bdabc5d756298ab6891d6fa4711c</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |

</details>

<details>
<summary>📜 <b>North America History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2655_15.0.0.405(EX01)<br><details><summary>MD5</summary><code>5b693110ced8964a707defcd198acfc4</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PJZ110_16.0.5.701(CN01)<br><details><summary>MD5</summary><code>552380013ed612435e17774068d3dc38</code></details> | 1 | Major: 3, Minor: 0 | 2026-04-08 | ❌ Protected |
| PJZ110_16.0.3.502(CN01)<br><details><summary>MD5</summary><code>adbce2f7f46d081e68a87bb75b524fd0</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-12 | ❌ Protected |
| PJZ110_16.0.3.501(CN01)<br><details><summary>MD5</summary><code>084a427ff00012ce4b2dbeb683f1601d</code></details> | 1 | Major: 3, Minor: 0 | 2026-02-04 | ❌ Protected |
| PJZ110_16.0.2.403(CN01)<br><details><summary>MD5</summary><code>e88c0d89f3feffed5dc9e8d5c4ce99fb</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-11 | ✅ Safe |
| PJZ110_16.0.1.303(CN01)<br><details><summary>MD5</summary><code>bbe9311fd7953f89af8faa8863920654</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| PJZ110_16.0.0.212(EX01)<br><details><summary>MD5</summary><code>2cd31ab98ebfd28e0331bcabdffcb976</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>


---

### OnePlus 13R

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2645 | CPH2645_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>9d947f896823878e3a32a809ec76fd71</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| Europe | CPH2645 | CPH2645_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>3ba2218f9e855815653d54839f50fa66</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| India | CPH2691 | CPH2691_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>6e491c496b73deea2dc834cd5f460d8b</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2645_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>9fd992eaf16b4c0b2212d8675d2f57a7</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-25 | ❌ Protected |
| CPH2645_16.0.0.205(EX01)<br><details><summary>MD5</summary><code>72c1aa34316c7ee6ba23b39be0edb5ea</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2645_15.0.0.871(EX01)<br><details><summary>MD5</summary><code>dec1cc4c7c37f67bcbc0d0921a99a4b5</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2645_15.0.0.860(EX01)<br><details><summary>MD5</summary><code>a090f7c9ef5d4bb789c729dd8376bf89</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| CPH2645_15.0.0.850(EX01)<br><details><summary>MD5</summary><code>7a4ecdcdb8ec576fc3960ee4c4af26e2</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2645_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>fc83d78ebf942ee641d6a70bea3c2646</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-25 | ❌ Protected |
| CPH2645_16.0.0.205(EX01)<br><details><summary>MD5</summary><code>2af9f3eea8081a1d027d97cb62a4c686</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-11 | ✅ Safe |
| CPH2645_15.0.0.871(EX01)<br><details><summary>MD5</summary><code>72c84c0f77618a85dd483d7eb3561530</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| CPH2645_15.0.0.860(EX01)<br><details><summary>MD5</summary><code>901792cb15c4e43d6e5a1eeabe3ba91d</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |
| CPH2645_15.0.0.850(EX01)<br><details><summary>MD5</summary><code>c03cfe25321e8451076f4322708b5458</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2691_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>7052fdc3ef6ba695876c463e220b0666</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-23 | ❌ Protected |
| CPH2691_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>a4af2544839c988d898b2f7d22e9d2e5</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |
| CPH2691_16.0.1.302(EX01)<br><details><summary>MD5</summary><code>bea10f391a69cffabf770457a1c65953</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-11 | ✅ Safe |
| CPH2691_16.0.0.205(EX01)<br><details><summary>MD5</summary><code>40a9662c0c40130043b83a48daa44de5</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2691_15.0.0.860(EX01)<br><details><summary>MD5</summary><code>9616225a40cc97ad0e27072aaa2fe72b</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>


---

### OnePlus 13T

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | PKX110 | PKX110_16.0.5.701(CN01)<br><details><summary>MD5</summary><code>77e2399108c694805d711231570bc2dc</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PKX110_16.0.3.502(CN01)<br><details><summary>MD5</summary><code>cd9a0b7b1b34f2402637f07ad93c9639</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-11 | ❌ Protected |
| PKX110_16.0.3.501(CN01)<br><details><summary>MD5</summary><code>4b08985d35a0fa74c5041ac96d5efb0b</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-11 | ❌ Protected |
| PKX110_16.0.2.400(CN01)<br><details><summary>MD5</summary><code>9e24382675ed8ca6fede1da4b69043f7</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-11 | ✅ Safe |
| PKX110_16.0.1.301(CN01)<br><details><summary>MD5</summary><code>77b376681c8ac0a7a4d1a65e0a6b12f5</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-11 | ✅ Safe |

</details>


---

### OnePlus 13s

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| India | CPH2723 | CPH2723_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>7352d39b42bef6e0bc79263925e4df51</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2723_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>8d3c3d88720a2097c02e7de193a9d969</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-13 | ❌ Protected |
| CPH2723_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>83966b4ce06e0839f885db0f1f32d674</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2723_16.0.1.303(EX01)<br><details><summary>MD5</summary><code>7f19055c5ac85499a884c510e6494423</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-12 | ✅ Safe |
| CPH2723_16.0.0.211(EX01)<br><details><summary>MD5</summary><code>b8f70c2ec2e24c9bcadfcae362580780</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-12 | ✅ Safe |
| CPH2723_15.0.2.601(EX01)<br><details><summary>MD5</summary><code>295320daf7b8f7c7299c0be010a689c4</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-12 | ✅ Safe |

</details>


---

### OnePlus Open

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | CPH2551 | CPH2551_16.0.3.505(EX01)<br><details><summary>MD5</summary><code>b0b7acd843ad2eb4e736fae0aa079e88</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| India | CPH2551 | CPH2551_16.0.3.505(EX01)<br><details><summary>MD5</summary><code>992c3916a53a72e8e0b7449a60e5c83f</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| North America | CPH2551 | CPH2551_15.0.0.822(EX01)<br><details><summary>MD5</summary><code>9ee66cf78b25acaee3681d138f04c04f</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2551_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>c6e40fec39894a2f17684fc5d826dbce</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-21 | ✅ Safe |
| CPH2551_16.0.2.400(EX01) | 0 | Major: 2, Minor: 0 | 2026-02-06 | ✅ Safe |
| CPH2551_16.0.1.300(EX01)<br><details><summary>MD5</summary><code>37d145dd87e260c6833efcc2d65e6475</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-26 | ✅ Safe |
| CPH2551_16.0.0.201(EX01)<br><details><summary>MD5</summary><code>142855cdadd173b2b515e24663b89ae9</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-21 | ✅ Safe |
| CPH2551_15.0.0.863(EX01)<br><details><summary>MD5</summary><code>4f1b8c4f45cfb394c05e1ef5728b13a2</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2551_15.0.0.610(EX01)<br><details><summary>MD5</summary><code>e0bf4e8bf23adc7db70f06656e0b4b9b</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-13 | ✅ Safe |
| CPH2551_14.0.0.850(EX01)<br><details><summary>MD5</summary><code>99aac9f56000f0da0f232fa3ccff4529</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-10 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2551_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>33f9bce9ecb17b30e8f84f97c91edb7f</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-16 | ✅ Safe |
| CPH2551_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>dc72dd05d476d8ecb198014177572cbf</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2551_16.0.1.300(EX01)<br><details><summary>MD5</summary><code>d131d0fcd87a0aa53cf5cf2549d239a2</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-21 | ✅ Safe |
| CPH2551_16.0.0.201(EX01)<br><details><summary>MD5</summary><code>0969618dfdfaaf6ca8867ac16f3dc32e</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>


---

### OnePlus 12

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2581 | CPH2581_16.0.5.702(EX01)<br><details><summary>MD5</summary><code>7d46f0c9123feec1c4d06e9e61133c52</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| Europe | CPH2581 | CPH2581_16.0.5.702(EX01)<br><details><summary>MD5</summary><code>a67c5530baf67def45927cd7bd67104f</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| India | CPH2573 | CPH2573_16.0.5.702(EX01)<br><details><summary>MD5</summary><code>a599a8f3fdbd426588b8f544c5b19fa3</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| North America | CPH2583 | CPH2583_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>c4bf38e7b691b79f32605967303b77e0</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| China | PJD110 | PJD110_16.0.3.500(CN01)<br><details><summary>MD5</summary><code>50eb6ea86f6d7b2b9936b477920151aa</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2581_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>3386a9f7548f18e9cda8558ca851a059</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-25 | ❌ Protected |
| CPH2581_16.0.0.201(EX01)<br><details><summary>MD5</summary><code>15ba498ef524eea6e173a53e390054ec</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-26 | ✅ Safe |
| CPH2581_15.0.0.863(EX01)<br><details><summary>MD5</summary><code>e4e38d8a69fec1e73ee3b897027597f0</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-11 | ✅ Safe |
| CPH2581_15.0.0.204(EX01)<br><details><summary>MD5</summary><code>f9034c616e472c4e4e097da203fede90</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2581_14.0.0.850(EX01)<br><details><summary>MD5</summary><code>4922bd352fbc39f51d01af5284662327</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2581_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>3770e5ac2f6e8750d8172ca2788bd36b</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-25 | ❌ Protected |
| CPH2581_16.0.0.201(EX01)<br><details><summary>MD5</summary><code>a83aafae40f24e43e41b2c7c1be2f6ec</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2581_15.0.0.863(EX01)<br><details><summary>MD5</summary><code>ab9462ac5766c96daff20b425ef1df78</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-04 | ✅ Safe |
| CPH2581_15.0.0.204(EX01)<br><details><summary>MD5</summary><code>d9da31c8e681b27598b220b196901ab5</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2581_14.0.0.850(EX01)<br><details><summary>MD5</summary><code>51f474db6c5d3e1e426dd293248f2402</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2573_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>54fd9ec64be6d91bb7b68b9c14864033</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-23 | ❌ Protected |
| CPH2573_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>669ed996a75edf5f511988953ffc002a</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2573_16.0.1.300(EX01)<br><details><summary>MD5</summary><code>b66c873aa39cee31906a1257c46b5261</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2573_16.0.0.201(EX01)<br><details><summary>MD5</summary><code>84a95ef4f01c7f1c8e96a607e931af6e</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| CPH2573_15.0.0.860(EX01)<br><details><summary>MD5</summary><code>313e1e889a69333f6eac245871fee652</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>

<details>
<summary>📜 <b>North America History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2583_11_C.61<br><details><summary>MD5</summary><code>0930cc879bd35c5c17c3f0e4eb0b014b</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-09 | ✅ Safe |

</details>

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PJD110_16.0.1.300(CN01)<br><details><summary>MD5</summary><code>2f93175745bf530adfaf3f80e0b4945a</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-26 | ✅ Safe |
| PJD110_16.0.0.201(CN01)<br><details><summary>MD5</summary><code>c79e0d5283b76ee44074f41ed2578378</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-04 | ✅ Safe |
| PJD110_15.0.0.860(CN01)<br><details><summary>MD5</summary><code>bb3c50f36650178e9da4d35c1ae46f1b</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| PJD110_15.0.0.502(CN01)<br><details><summary>MD5</summary><code>f499e6f7683a1c87ccb1f5a83e9be433</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>


---

### OnePlus 12R

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2609 | CPH2609_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>3d8966b0addcc72059f43c75c910eeac</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Europe | CPH2609 | CPH2609_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>3bf4f77014c7ecc56da8c34b8e2da4a8</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| India | CPH2585 | CPH2585_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>febde3a798251dc6ce1c3d29d6f6cb9e</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| North America | CPH2611 | CPH2611_11_A.65<br><details><summary>MD5</summary><code>a16a2f0dbbd5eeaff10041299f4d1508</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2609_16.0.1.300(EX01)<br><details><summary>MD5</summary><code>27066da992805a67c321ab81caf83ff7</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-22 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2609_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>6ad8b8c67ad8500b573df241254fcdd6</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-11 | ✅ Safe |

</details>


---

### OnePlus 11

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2449 | CPH2449_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>8744bb0bfc9b3bc5e02bf0c3ad0d8352</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Europe | CPH2449 | CPH2449_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>9db981106445969885335a2d35cfda5f</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| India | CPH2447 | CPH2447_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>f98c5382db9a4486355e5fa4e7979abd</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| North America | CPH2451 | CPH2451_15.0.0.800(EX01)<br><details><summary>MD5</summary><code>6cf186b46c64e0e0f81ce44f9df02689</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2449_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>b5745266807941dfbd1740eb4d81b26c</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2449_15.0.0.862(EX01)<br><details><summary>MD5</summary><code>54cc417e44e221c6960e4a6446c56cd0</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-10 | ✅ Safe |
| CPH2449_15.0.0.600(EX01)<br><details><summary>MD5</summary><code>419b9c2222c3db98dd3dab2092b071ea</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-04 | ✅ Safe |
| CPH2449_14.0.0.833(EX01)<br><details><summary>MD5</summary><code>b9d025ed11a63e79b8a27120f528bcd5</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-13 | ✅ Safe |
| CPH2449_14.0.0.304(EX01)<br><details><summary>MD5</summary><code>e698b0fa87d61c1b081abe119c52fb86</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2449_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>7f3b8a402aaba42654f4b23aa3065120</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-25 | ✅ Safe |
| CPH2449_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>3a0e1f9b1288270b6a9339d36e91012b</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-04 | ✅ Safe |
| CPH2449_15.0.0.862(EX01)<br><details><summary>MD5</summary><code>005720cd3a7ed022c504ea46aa08b108</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-04 | ✅ Safe |
| CPH2449_15.0.0.600(EX01)<br><details><summary>MD5</summary><code>34bbda6b42e72c2e9e536087355df1ae</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-26 | ✅ Safe |
| CPH2449_14.0.0.833(EX01)<br><details><summary>MD5</summary><code>c3e9d3216214792f7106adf6f72d5f4c</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2449_14.0.0.304(EX01)<br><details><summary>MD5</summary><code>c1f0435152c274076284d579f94b3427</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2447_16.0.2.400(EX01) | 0 | Major: 2, Minor: 0 | 2026-02-04 | ✅ Safe |
| CPH2447_16.0.1.300(EX01)<br><details><summary>MD5</summary><code>642d05f8e9f90941d039053fb2ef9a20</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-25 | ✅ Safe |
| CPH2447_15.0.0.862(EX01)<br><details><summary>MD5</summary><code>c0debf3a37dea71b0155a97781de08b4</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-04 | ✅ Safe |
| CPH2447_15.0.0.600(EX01)<br><details><summary>MD5</summary><code>4cc0d301bd86dd3ff0713e5fade8eaf7</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2447_14.0.0.833(EX01)<br><details><summary>MD5</summary><code>5339aa54232836e9f81f5b09304ca784</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-13 | ✅ Safe |
| CPH2447_14.0.0.304(EX01)<br><details><summary>MD5</summary><code>14942843ae7c515bce8f829008806095</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-10 | ✅ Safe |

</details>


---

### OnePlus 11R

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| India | CPH2487 | CPH2487_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>be9da74a7e6549b50b667f9420d1df84</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2487_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>d81040f0f7c1ce65b89094847abbec6a</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-09 | ✅ Safe |
| CPH2487_15.0.0.870(EX01)<br><details><summary>MD5</summary><code>ab372586fbb439bad1e8cfa19dfee40f</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-11 | ✅ Safe |
| CPH2487_15.0.0.601(EX01)<br><details><summary>MD5</summary><code>ca359a0253ba4d590b38bbc44dd55607</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2487_14.0.0.810(EX01)<br><details><summary>MD5</summary><code>41257dd6ab4cd746d7855c6b320c2285</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-04 | ✅ Safe |
| CPH2487_14.0.0.300(EX01)<br><details><summary>MD5</summary><code>0dce73db5e8c7278656b99d41c3c8a81</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-26 | ✅ Safe |
| CPH2487_13.1.0.583(EX01)<br><details><summary>MD5</summary><code>fd77cd0cde25bb7e0ad3718ab286e963</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-10 | ✅ Safe |

</details>


---

### OnePlus 10 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | NE2213 | NE2213_16.0.3.520(EX01)<br><details><summary>MD5</summary><code>adb64bb0101e46c2428c0387ba49060d</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Europe | NE2213 | NE2213_16.0.3.520(EX01)<br><details><summary>MD5</summary><code>6f11cb2e7b9ad8ca103927d558605da5</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| India | NE2211 | NE2211_16.0.3.520(EX01)<br><details><summary>MD5</summary><code>46f577fb0b2656d629b5993c3a7762e3</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| North America | NE2215 | NE2215_15.0.0.401(EX01)<br><details><summary>MD5</summary><code>203d379328732fae89f3134e3b808304</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| China | NE2210 | NE2210_15.0.0.1301(CN01)<br><details><summary>MD5</summary><code>d1b71c63550e15270a3580cf7220e927</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| NE2213_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>442a1ffc6ab53fdcafb05e4b555a7c31</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-30 | ✅ Safe |
| NE2213_15.0.0.1302(EX01)<br><details><summary>MD5</summary><code>4f4678dc3a6898a2c76745886fa79313</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |
| NE2213_15.0.0.700(EX01)<br><details><summary>MD5</summary><code>9544be7ad28064a120da7c8ccd6290be</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-25 | ✅ Safe |
| NE2213_14.0.0.940(EX01)<br><details><summary>MD5</summary><code>6fd2cf03a80a55fe4337a754f76d16a8</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-10 | ✅ Safe |
| NE2213_14.0.0.202(EX01)<br><details><summary>MD5</summary><code>2cd47fb517e2d0869da9daab7a673ce4</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-13 | ✅ Safe |
| NE2213_13.1.0.597(EX01)<br><details><summary>MD5</summary><code>c4d883a698e3f1de8a8a6392fd5c36ba</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-26 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| NE2213_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>0602a2e727fc048cf73ad53577013a9a</code></details> | 0 | Major: 2, Minor: 0 | 2026-04-01 | ✅ Safe |
| NE2213_15.0.0.1302(EX01)<br><details><summary>MD5</summary><code>5daffaee08f4eeb3062b09b887aaa8c9</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-26 | ✅ Safe |
| NE2213_15.0.0.700(EX01)<br><details><summary>MD5</summary><code>ee4d7ff2fde85bfff044267251a1e204</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-04 | ✅ Safe |
| NE2213_14.0.0.940(EX01)<br><details><summary>MD5</summary><code>594bf98e18eafe719715a1441eece196</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-11 | ✅ Safe |
| NE2213_14.0.0.202(EX01)<br><details><summary>MD5</summary><code>4054362ce373912e3c815bd0203504f0</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |
| NE2213_13.1.0.597(EX01)<br><details><summary>MD5</summary><code>48c7cc94e62946762e71b32f7f264f26</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| NE2211_16.0.3.510(EX01)<br><details><summary>MD5</summary><code>6789b9fa5b12cea96885ed118c29cf7b</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-17 | ✅ Safe |
| NE2211_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>c55ab503dde1551ecd950c06b01dae79</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-26 | ✅ Safe |
| NE2211_15.0.0.1302(EX01)<br><details><summary>MD5</summary><code>7ff5b88637be13d09bae0b4fa1c7cf99</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-25 | ✅ Safe |
| NE2211_15.0.0.700(EX01)<br><details><summary>MD5</summary><code>2b63361c7ace205d733e9d7d1847b79e</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-11 | ✅ Safe |
| NE2211_14.0.0.940(EX01)<br><details><summary>MD5</summary><code>e80f3c13212f59565f7d325c0545bfbb</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-10 | ✅ Safe |
| NE2211_14.0.0.300(EX01)<br><details><summary>MD5</summary><code>6a3d5f4f7b52ef32358820b4adaa3b6c</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| NE2210_15.0.0.1202(CN01)<br><details><summary>MD5</summary><code>851094bc9f6829aae556cb124ae35a55</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-10 | ✅ Safe |
| NE2210_15.0.0.700(CN01)<br><details><summary>MD5</summary><code>83bfd50e3b49ebc8c73a3fa7f7ddae50</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-25 | ✅ Safe |
| NE2210_14.0.0.940(CN01)<br><details><summary>MD5</summary><code>58d3a22b4a1e05194d5ce7374fe58282</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |
| NE2210_14.0.0.300(CN01)<br><details><summary>MD5</summary><code>2f8b4435bd0db699fbce689846ed46ae</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-26 | ✅ Safe |

</details>


---

### OnePlus 10T

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2415 | CPH2415_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>f13eab2d1a00aa9179e0e5e1e04b7d4c</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Europe | CPH2415 | CPH2415_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>7789c263157952e4b85a1dc505771a5a</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| India | CPH2413 | CPH2413_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>f2f49f81fdec15884d9b6df3f8018d4b</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| North America | CPH2417 | CPH2417_11_C.46<br><details><summary>MD5</summary><code>c0fe595ca50e4db92c009f49273c5c9a</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2415_15.0.0.1601(EX01)<br><details><summary>MD5</summary><code>98462c7099333250b1ec2f168af822ce</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-08 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2415_15.0.0.1601(EX01)<br><details><summary>MD5</summary><code>ae910e6219c0b40dfe8127768b1c9cdb</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-08 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2413_15.0.0.1601(EX01) | 0 | Major: 2, Minor: 0 | 2026-02-05 | ✅ Safe |

</details>


---

### OnePlus 9 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | LE2123 | LE2123_14.0.0.1902(EX01)<br><details><summary>MD5</summary><code>95f48596dd863486130da6b32b823036</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | LE2121 | LE2121_14.0.0.1902(EX01)<br><details><summary>MD5</summary><code>5353f56dfa6db49482d1801ede7b4ca0</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| North America | LE2125 | LE2125_11_F.30<br><details><summary>MD5</summary><code>b08d06b5f340ccb6c2a5e58c3cd51218</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus 9

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | LE2113 | LE2113_14.0.0.1902(EX01)<br><details><summary>MD5</summary><code>ef5915d51a38a0213a15a31102ad904a</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | LE2111 | LE2111_14.0.0.1902(EX01)<br><details><summary>MD5</summary><code>25b0c8e1c6c1c3a9630644f08c02bf81</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| North America | LE2115 | LE2115_11_F.30<br><details><summary>MD5</summary><code>7f497eba018cba18d4a57c720a2120eb</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus 9RT

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| India | MT2111 | MT2111_14.0.0.2702(EX01)<br><details><summary>MD5</summary><code>ce87f568d2c236229f628f95bb82a08a</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus 8T

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | KB2003 | KB2003_14.0.0.1311(EX01)<br><details><summary>MD5</summary><code>1c53e270fe049b1cdbd361f6a29900d0</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | KB2001 | KB2001_14.0.0.1311(EX01)<br><details><summary>MD5</summary><code>0fb14a28fe6ac6d91b52a66a9d6e76e7</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| North America | KB2005 | KB2005_11_F.67<br><details><summary>MD5</summary><code>68134307caa39d9f0f07cbb107619dee</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus 8 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | IN2023 | IN2023_13.1.0.591(EX01)<br><details><summary>MD5</summary><code>6cce909b7b011d59bdd04b0830e364c6</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | IN2021 | IN2021_13.1.0.590(EX01)<br><details><summary>MD5</summary><code>309ff476170e0e5233214d3b271a2436</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| North America | IN2025 | IN2025_11_F.67<br><details><summary>MD5</summary><code>9262c4d8d4591ac891d13bf2e3bc9c04</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| IN2023_13.1.0.590(EX01)<br><details><summary>MD5</summary><code>2c929877e9643a9f37d548ad7debe4b3</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-27 | ✅ Safe |

</details>


---

### OnePlus 8

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | IN2013 | IN2013_13.1.0.593(EX01)<br><details><summary>MD5</summary><code>918bda26536c88621a0210b64f887074</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | IN2011 | IN2011_13.1.0.590(EX01)<br><details><summary>MD5</summary><code>b9701ec83f0df32427606f56d14275ca</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| North America | IN2015 | IN2015_11_F.67<br><details><summary>MD5</summary><code>38f9e3ee0be3b595e5b3f4ccf244aca0</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus 7T Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | HD1913 | HD1917_11_F.22<br><details><summary>MD5</summary><code>3d15c9a772241e92cfb0c74acac2d739</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Europe | HD1913 | HD1913_11_F.22<br><details><summary>MD5</summary><code>e6681e6d8c0e0e903c514bd5f29b8c7a</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | HD1911 | HD1911_11_F.22<br><details><summary>MD5</summary><code>4eb9c8bf005ad8b76ed0fc23ddc6f6e4</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus 7T

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | HD1903 | HD1905_11_F.22<br><details><summary>MD5</summary><code>87a2d003e867c131ff0d0b5829f9d91a</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Europe | HD1903 | HD1903_11_F.22<br><details><summary>MD5</summary><code>03f0b0432ad0b1420fecdcbc5de9a6ed</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | HD1901 | HD1901_11_F.22<br><details><summary>MD5</summary><code>b4e4a35d93399eca1543acb4fa126a36</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus 7 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | GM1917 | GM1917_11_H.41<br><details><summary>MD5</summary><code>1ccb5dc4196b7979673ef1cf8338dd76</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Europe | GM1913 | GM1913_11_H.40<br><details><summary>MD5</summary><code>96591b6e18ef733a63f631077928f384</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | GM1911 | GM1911_11_H.40<br><details><summary>MD5</summary><code>33dac37728530166116a3e354d16fda6</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus 7

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | GM1905 | GM1905_11_H.41<br><details><summary>MD5</summary><code>49eb65dde1179f77ad92c5035a51c4ae</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Europe | GM1903 | GM1903_11_H.40<br><details><summary>MD5</summary><code>6bb15c264956576babcd5ded2eae55d0</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | GM1901 | GM1901_11_H.40<br><details><summary>MD5</summary><code>ab3c412e906853535f21f2823d2358d7</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus Nord 5

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2709 | CPH2709_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>1fa0ad252c46d6ccdc9699a4f331bbd4</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| Europe | CPH2709 | CPH2709_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>d462744e077d08fab080ee7c54bbe2da</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| India | CPH2707 | CPH2707_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>8a0c0fc15a64768dd40c6599197c5e46</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2709_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>215ac417ec05bafcd5d2c8afe8fa140f</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-28 | ✅ Safe |
| CPH2709_16.0.1.300(EX01)<br><details><summary>MD5</summary><code>e897c75b850e4acbb9a6556d541bc3b7</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-22 | ✅ Safe |
| CPH2709_15.0.2.604(EX01)<br><details><summary>MD5</summary><code>e5d66cec7708b0178f31bd7b6c67c74a</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2709_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>7988a8ec49273c093ed02b906deb20a1</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-28 | ✅ Safe |
| CPH2709_16.0.1.300(EX01)<br><details><summary>MD5</summary><code>1c641f0b3c40922ba9f736d54a957c8a</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2709_15.0.2.604(EX01)<br><details><summary>MD5</summary><code>07641d9d8bf4466472600f8ea8a083a0</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-04 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2707_16.0.2.400(EX01)<br><details><summary>MD5</summary><code>3dcfeee921d76d936ed403304bd8179c</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-24 | ✅ Safe |

</details>


---

### OnePlus Nord 4

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2663 | CPH2663_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>e64b6607ccb5361937039a6e10f34483</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| Europe | CPH2663 | CPH2663_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>75cb2c75c9f1c1c2c34515a6462b871a</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| India | CPH2661 | CPH2661_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>6352d9d637f01ddfb574d13c412c3cae</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2663_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>94c3d509d75d2cf2ef7ff546a19d12d2</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-25 | ✅ Safe |
| CPH2663_16.0.1.301(EX01)<br><details><summary>MD5</summary><code>48c0cb97cbfe448d50b8f730236c8019</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2663_15.0.0.401(EX01)<br><details><summary>MD5</summary><code>f35c38d521127a1cfb5be683711fa5db</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-26 | ✅ Safe |
| CPH2663_14.1.0.605(EX01)<br><details><summary>MD5</summary><code>89d7e0f18fe0b145fc3ab2e3430a5fea</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2663_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>0fabc357b219c3f26b48c8a688f5f2eb</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-27 | ✅ Safe |
| CPH2663_16.0.1.301(EX01)<br><details><summary>MD5</summary><code>57c99d530f04ff66f78acbfce67fb509</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2663_15.0.0.1301(EX01)<br><details><summary>MD5</summary><code>fac4c9f584f53d2e05315a980ee2eded</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |
| CPH2663_15.0.0.401(EX01)<br><details><summary>MD5</summary><code>a2a5e83b73bc395eac686d6c6516ace8</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| CPH2663_14.1.0.605(EX01)<br><details><summary>MD5</summary><code>ec7efaa59e89c06a1e4f433f955235ac</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2661_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>f4d9b971fe52613b02edfe8225e86c95</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-23 | ✅ Safe |
| CPH2661_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>99f21627efd3fddd4b4ba184030f4319</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-19 | ✅ Safe |
| CPH2661_16.0.1.301(EX01)<br><details><summary>MD5</summary><code>187c8af4dc17c391be140f384b52044e</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |
| CPH2661_15.0.0.401(EX01)<br><details><summary>MD5</summary><code>5974618c636bad07afbaf4cbbabe3646</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| CPH2661_14.1.0.603(EX01)<br><details><summary>MD5</summary><code>c951f7927e020df08932ba8aaf1db309</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-26 | ✅ Safe |

</details>


---

### OnePlus Nord CE 4 Lite

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2619 | CPH2621_16.0.1.303(EX01)<br><details><summary>MD5</summary><code>b7c365069ec43d6ac385bcc54709ea07</code></details> | **?** | Major: 0, Minor: 120 | 2026-04-12 | ⚠️ Undetectable ARB |
| Europe | CPH2619 | CPH2621_16.0.1.303(EX01)<br><details><summary>MD5</summary><code>7f747226ec77f81583f012f71a24a974</code></details> | **?** | Major: 0, Minor: 120 | 2026-04-12 | ⚠️ Undetectable ARB |
| India | CPH2619 | CPH2619_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>0dffbff8aa99af0be4b4a250f878b191</code></details> | **?** | Major: 0, Minor: 120 | 2026-04-12 | ⚠️ Undetectable ARB |

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2619_16.0.1.303(EX01)<br><details><summary>MD5</summary><code>317e7a25185b6acfa3188b188609d552</code></details> | ? | Major: 0, Minor: 120 | 2026-04-09 | ⚠️ Undetectable ARB |

</details>


---

### OnePlus Nord CE 4

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| India | CPH2613 | CPH2613_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>f08b3046c8ed7b7a6baf1e72d16d815f</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2613_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>3990e7a5b3eb6dd87b82ab4ee9efebbd</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-31 | ✅ Safe |

</details>


---

### OnePlus Nord CE 3

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| India | CPH2567 | CPH2569_15.0.0.1604(EX01)<br><details><summary>MD5</summary><code>4182a58172f56cac990e1b3685113af7</code></details> | **?** | Major: 0, Minor: 120 | 2026-04-12 | ⚠️ Undetectable ARB |

---

### OnePlus Nord CE 3 Lite

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2465 | CPH2465_15.0.0.1800(EX01)<br><details><summary>MD5</summary><code>896bcc834f23fb5b29a68af89628a281</code></details> | **?** | Major: 0, Minor: 120 | 2026-04-12 | ⚠️ Undetectable ARB |
| Europe | CPH2465EEA | CPH2465_15.0.0.1800(EX01)<br><details><summary>MD5</summary><code>431b6e97ef2d135b41b3f5a1816bd484</code></details> | **?** | Major: 0, Minor: 120 | 2026-04-12 | ⚠️ Undetectable ARB |
| India | CPH2467 | CPH2467_15.0.0.1800(EX01)<br><details><summary>MD5</summary><code>8726ea7cfe6acb09a6c31ac8a0e82679</code></details> | **?** | Major: 0, Minor: 120 | 2026-04-12 | ⚠️ Undetectable ARB |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2465_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>72d0c27bdc608978592e04cdce62b016</code></details> | ? | Major: 0, Minor: 120 | 2026-03-25 | ⚠️ Undetectable ARB |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2465_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>b08db09891b432a2ef4648888803668a</code></details> | ? | Major: 0, Minor: 120 | 2026-03-25 | ⚠️ Undetectable ARB |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2467_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>479a7a4ead369db901314969f4728b37</code></details> | ? | Major: 0, Minor: 120 | 2026-03-20 | ⚠️ Undetectable ARB |

</details>


---

### OnePlus Nord CE 2 Lite

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | CPH2409 | CPH2409_14.0.0.2700(EX01)<br><details><summary>MD5</summary><code>b101fe4ea22334155ed14c766bb8d1ab</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Europe | CPH2409EEA | CPH2409_14.0.0.2700(EX01)<br><details><summary>MD5</summary><code>4b628f389081f069651aaf8663ce1355</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | CPH2381 | CPH2381_14.0.0.2700(EX01)<br><details><summary>MD5</summary><code>99fec841bb7c8abb22a11dd88b8bd73e</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus Nord N30

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| North America | CPH2513 | CPH2513_11_C.62<br><details><summary>MD5</summary><code>0aee1de71ddf7ea9251b46d0bce01fdd</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus Nord N20

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| North America | CPH2459 | CPH2459_11_C.24<br><details><summary>MD5</summary><code>b2dac2cc86b0f5315ce9f5ff861ac6cb</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus Nord

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | AC2003 | AC2003_11_F.24<br><details><summary>MD5</summary><code>c704f8b99a545a5a53b3bbe141bfb0ec</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | AC2001 | AC2001_11_F.24<br><details><summary>MD5</summary><code>fa6ff6d1f91c0549371c28932f7b37cc</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus Nord N200 5G

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| North America | DE2117 | DE2117_11_C.34<br><details><summary>MD5</summary><code>29ba37ef58d043e6f1d6088946844fae</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

### OnePlus Ace 6T

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | PLR110 | PLR110_16.0.5.702(CN01)<br><details><summary>MD5</summary><code>d51484f274245087d9eecfbbe5af7c77</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PLR110_16.0.3.503(CN01)<br><details><summary>MD5</summary><code>44b826a364824bfc10d0720402b8822f</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-16 | ✅ Safe |
| PLR110_16.0.3.501(CN01)<br><details><summary>MD5</summary><code>adc7d4b44fd3c7dcb0bea4a13c78e098</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| PLR110_16.0.2.403(CN01)<br><details><summary>MD5</summary><code>aced29f4184f9065781679b9008375f9</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-04 | ✅ Safe |
| PLR110_16.0.2.402(CN01)<br><details><summary>MD5</summary><code>273266741cdbcad2217c4c3d256a1853</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| PLR110_16.0.1.308(CN01)<br><details><summary>MD5</summary><code>6849eca4f011cbfc58b340dff6f6a434</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>


---

### OnePlus Ace 6

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | PLQ110 | PLQ110_16.0.5.701(CN01)<br><details><summary>MD5</summary><code>4b24d6fdc2e5d35a304a5eaaaea57def</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PLQ110_16.0.5.700(CN01)<br><details><summary>MD5</summary><code>d8f24e1cf3c2f0ef83fe6325dca9cc12</code></details> | 1 | Major: 3, Minor: 0 | 2026-04-07 | ❌ Protected |
| PLQ110_16.0.3.502(CN01)<br><details><summary>MD5</summary><code>8a8ea78fe60581d9401cfdf93950fd8a</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-16 | ✅ Safe |
| PLQ110_16.0.2.403(CN01)<br><details><summary>MD5</summary><code>c70cfbbbd421bc0122163269b4429661</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-26 | ✅ Safe |
| PLQ110_16.0.2.402(CN01)<br><details><summary>MD5</summary><code>0b170c8300f4f7f77e52c4853bcef5bc</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| PLQ110_16.0.1.302(CN01)<br><details><summary>MD5</summary><code>22b21e9abf8974ea27e0714b21cefefc</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| PLQ110_16.0.0.207(CN01)<br><details><summary>MD5</summary><code>8204d55061bfa575e58c18a0de3622aa</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>


---

### OnePlus Ace 5 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | PKR110 | PKR110_16.0.5.700(CN01)<br><details><summary>MD5</summary><code>1032105ab6780803db30bfb1ceaf8cff</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PKR110_16.0.3.500(CN01)<br><details><summary>MD5</summary><code>a29150f57f67b99083f6a4081c468171</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-23 | ✅ Safe |
| PKR110_16.0.2.400(CN01)<br><details><summary>MD5</summary><code>06baa976a14a8410a779a34fe1d73224</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-04 | ✅ Safe |
| PKR110_16.0.1.300(CN01)<br><details><summary>MD5</summary><code>b8eca2908e26cf004d9a45601e97bf30</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-26 | ✅ Safe |
| PKR110_16.0.0.204(CN01)<br><details><summary>MD5</summary><code>b4585916847bf6d7076783d68bcaffe9</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| PKR110_15.0.0.871(CN01)<br><details><summary>MD5</summary><code>0f44432e4b1ff820e1cd2e36da6058f7</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |

</details>


---

### OnePlus Ace 5

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | PKG110 | PKG110_16.0.5.701(CN01)<br><details><summary>MD5</summary><code>9e846bf2d37cfc10168757bbf98f9606</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PKG110_16.0.3.500(CN01)<br><details><summary>MD5</summary><code>d216133625b3690b7e66df13d17fc659</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-23 | ❌ Protected |
| PKG110_16.0.2.400(CN01)<br><details><summary>MD5</summary><code>687170822ca972c5575d5438c347ab1b</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-11 | ✅ Safe |
| PKG110_16.0.1.302(CN01)<br><details><summary>MD5</summary><code>26661ccd5c07e13f010623e83abfdfc5</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-06 | ✅ Safe |
| PKG110_16.0.0.205(CN01)<br><details><summary>MD5</summary><code>7a84ff899a56dec114c8bf3b61016208</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| PKG110_15.0.0.860(CN01)<br><details><summary>MD5</summary><code>f1dc5639c3965964bdd99e4f18550857</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>


---

### OnePlus Ace 3 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | PJX110 | PJX110_16.0.1.301(CN01)<br><details><summary>MD5</summary><code>171c22c558cc25e3624419a11a80a420</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PJX110_15.0.0.861(CN01)<br><details><summary>MD5</summary><code>8b9af5316e75bf1a3332a3dae65deacf</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| PJX110_15.0.0.500(CN01)<br><details><summary>MD5</summary><code>9d263a30644f553dcd0958a84c3894c3</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-06 | ✅ Safe |
| PJX110_14.1.0.510(CN01)<br><details><summary>MD5</summary><code>8cd9735ba7301c2b9311f0a1aae46b75</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>


---

### OnePlus Ace 3V

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | PJF110 | PJF110_16.0.1.301(CN01)<br><details><summary>MD5</summary><code>856a520469ed78dce30155893f413617</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PJF110_15.0.0.500(CN01)<br><details><summary>MD5</summary><code>99f6ed36e6b64144836d9cf1531c96f7</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| PJF110_14.0.1.720(CN01)<br><details><summary>MD5</summary><code>a1331494ba071363e8b2fba9138258e1</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>


---

### OnePlus Ace 3

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | PJE110 | PJE110_16.0.1.300(CN01)<br><details><summary>MD5</summary><code>2133450d657b8accda00dcd97101de80</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PJE110_15.0.0.870(CN01)<br><details><summary>MD5</summary><code>41ecfd297b1aa4b2d71410e4dd817781</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-10 | ✅ Safe |
| PJE110_15.0.0.600(CN01)<br><details><summary>MD5</summary><code>aa6baa53941cb20c2cb430343c16bdba</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-18 | ✅ Safe |
| PJE110_14.0.0.817(CN01)<br><details><summary>MD5</summary><code>e0487fc4818e8a2837aaf5f01dfae06e</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-26 | ✅ Safe |

</details>


---

### OnePlus Pad 3

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | OPD2415 | OPD2415_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>c245716d418c3a6417df4662dfae9efb</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| Europe | OPD2415 | OPD2415_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>efad8cb2b8e9024919366bd0699c934f</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| India | OPD2415 | OPD2415_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>8f4c4c2d5cc38455bf74e3f20c0884b2</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| North America | OPD2415 | OPD2415_15.0.1.500(EX01)<br><details><summary>MD5</summary><code>4a431268abcc614778a06fa408aa1064</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| OPD2415_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>64101499d86baf3ef11eb91384f782fe</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-26 | ❌ Protected |
| OPD2415_16.0.1.302(EX01)<br><details><summary>MD5</summary><code>29a03855c25e72197c24d5c603ace45a</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| OPD2415_16.0.0.211(EX01)<br><details><summary>MD5</summary><code>6be9e071c6c3284866ddd02c06e52fb0</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| OPD2415_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>2a9096260fd856ede66700ddf207b49b</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-26 | ❌ Protected |
| OPD2415_16.0.1.302(EX01)<br><details><summary>MD5</summary><code>9dbeb1decd4e820a95dd6c8ecf68b87e</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| OPD2415_16.0.0.211(EX01)<br><details><summary>MD5</summary><code>6070fbd5daf4d3ea7ae7e5e5af4d67cc</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| OPD2415_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>f04541e8fba46fe4b066b7f7deaa0334</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-25 | ❌ Protected |
| OPD2415_16.0.1.302(EX01)<br><details><summary>MD5</summary><code>ed72adfd06e1f9684e051be6fc797d02</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| OPD2415_16.0.0.211(EX01)<br><details><summary>MD5</summary><code>31422d40cca779e619e20aec05910e61</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>


---

### OnePlus Pad 2 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | OPD2413 | OPD2413_16.0.3.501(CN01)<br><details><summary>MD5</summary><code>7af2eda10018ec1b4c0d66b1df258e55</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| OPD2413_16.0.2.400(CN01)<br><details><summary>MD5</summary><code>d91040afb739f2b5b119cc9cc585a7c9</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-04 | ✅ Safe |
| OPD2413_16.0.1.301(CN01)<br><details><summary>MD5</summary><code>a29d0fc70c772358d489097213b8e2ad</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-26 | ✅ Safe |
| OPD2413_15.0.1.801(CN01)<br><details><summary>MD5</summary><code>92b47da43846054c6906e8d5fb78c1a2</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>


---

### OnePlus Pad 2

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Global | OPD2403 | OPD2403_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>a2af0d57211c379b8bf70f5a0bd381a5</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| Europe | OPD2403 | OPD2403_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>995d3095adbd8be28edf59e85c3d29e0</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |
| India | OPD2403 | OPD2403_16.0.5.701(EX01)<br><details><summary>MD5</summary><code>81159aae331be32f00155760c8b14b14</code></details> | **1** | Major: 3, Minor: 0 | 2026-04-12 | ❌ Protected |

<details>
<summary>📜 <b>Global History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| OPD2403_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>dcf3998f433db53966a08aa889ce5228</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-26 | ❌ Protected |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| OPD2403_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>8440c19505c47de99a60f66a9daa8d17</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-26 | ❌ Protected |
| OPD2403_16.0.0.202(EX01)<br><details><summary>MD5</summary><code>8e31a7ea8e1c47112de078f2e8b5644c</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>

<details>
<summary>📜 <b>India History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| OPD2403_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>b549aa2ee70831834ff52baada2f91f0</code></details> | 1 | Major: 3, Minor: 0 | 2026-03-23 | ❌ Protected |
| OPD2403_16.0.1.301(EX01)<br><details><summary>MD5</summary><code>b45470fbeb6a785f32209d7711e37ffa</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| OPD2403_16.0.0.202(EX01)<br><details><summary>MD5</summary><code>d3dd8401e908aa37be0d34921c04068e</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>


---

### Oppo Reno10 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Singapore | CPH2525SG | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>308573b1553dc7381448f4a4a669b42c</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Taiwan | CPH2525TW | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>2c5dbdc609f8eec4e127584dc103c82f</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Malaysia | CPH2525MY | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>6966558af815390daee7bcaca2a5885f</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Indonesia | CPH2525ID | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>afbfa780bdb0d4eb6b31ad63bf895804</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Thailand | CPH2525TH | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>19f4a1e35ab303463061db6c4d91ff1e</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Vietnam | CPH2525VN | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>f072fc3b8c605d96852168abe549d873</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Asia Pacific | CPH2525 | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>dbd2b3559dd8b1ef6c62d26ff1df4dcb</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Oceania | CPH2525OCA | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>0407edf6593a82dc2d02b13bc38c0a2e</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Saudi Arabia | CPH2525SA | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>1f6d57b4a491cfdc11ea8a67d480eebc</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Middle East | CPH2525MEA | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>ae1e910b70f736368c2aec048b8f1d99</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Philippines | CPH2525PH | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>8b682eb6bda3ae1adb3a75bbe4cea3ee</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Europe | CPH2525EEA | CPH2525_15.0.0.1603(EX01)<br><details><summary>MD5</summary><code>128650aa4175ac0e3c4cda9f3ae9eb25</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| India | CPH2525IN | CPH2525_13.1.1.147(EX01)<br><details><summary>MD5</summary><code>abb2a1ef3450621de3073f48d5215b19</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Singapore History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>3835050ceee6140cf06affe9cf7db263</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-27 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Taiwan History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>d3aeff26f756d3b5e7e85de67999662c</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-30 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Malaysia History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>0da7796177735bd736ae027aad6ffbde</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Indonesia History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>b502f539b8bc91a414018a5eebd68250</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Thailand History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>b72448e68f81b4efb446f67570935915</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Vietnam History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>945e55b6759b3147e2661e0db1cdb0a3</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-27 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Asia Pacific History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>7ffcae1c7860325a9db9ebd846c9f072</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-27 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Oceania History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>6554872f0d665c9a77cefb972287a7e5</code></details> | 0 | Major: 0, Minor: 120 | 2026-04-01 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Saudi Arabia History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>c1f95a3c9caae0d0a89c62e9d6589fea</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-30 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Middle East History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>d75e6df459ee8ed050e99e143a9ffe1c</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-27 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Philippines History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>1f6e08b4926652d580b2fce0839b95f4</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2525_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>5331936b839bd4267088fa89b461d060</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-27 | ✅ Safe |

</details>


---

### Oppo Find X8 Ultra

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| China | PKJ110 | PKJ110_16.0.3.500(CN01)<br><details><summary>MD5</summary><code>0f2a5043def5b99ae0903db69d932bff</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PKJ110_16.0.2.400(CN01)<br><details><summary>MD5</summary><code>d6133146502d44b3a9795d2686f0b06c</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-10 | ✅ Safe |
| PKJ110_16.0.1.301(CN01)<br><details><summary>MD5</summary><code>41e50bbe474aab4c7cfaf60eef6d218e</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-11 | ✅ Safe |
| PKJ110_16.0.0.212(CN01)<br><details><summary>MD5</summary><code>3d758b4da350de2dca8a6825984d5486</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-13 | ✅ Safe |
| PKJ110_15.0.1.622(CN01)<br><details><summary>MD5</summary><code>0e06b14fd353c14855c21312d00bd158</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>


---

### Oppo Find N5

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Singapore | CPH2671 | CPH2671_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>84b434d3337990b381cb6de3898f7c8e</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| Malaysia | CPH2671 | CPH2671_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>228e24d61a2a79d5e6702aac2296e288</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| Indonesia | CPH2671 | CPH2671_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>11fc5bc7dad9dd4b15d1166f0d42034f</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| Thailand | CPH2671 | CPH2671_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>00a4eb590b6d5ef63a39d4424855cf3a</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| Asia Pacific | CPH2671 | CPH2671_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>86da73ef6fcfeca76e6c4ea80f543481</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| Mexico | CPH2671 | CPH2671_16.0.5.700(EX01)<br><details><summary>MD5</summary><code>1dc9bb44e6e64ce0397434b2330f528d</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |
| China | PKV110 | PKH110_16.0.3.500(CN01)<br><details><summary>MD5</summary><code>0f0d5e5ca45e64af32b99f7401d65a12</code></details> | **0** | Major: 3, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Singapore History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2671_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>de7a9e13bbc55161b557883f77edb1ca</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Malaysia History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2671_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>01a344e7df285c3cc131bb2726620b73</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Indonesia History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2671_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>18f07a08f16946cd095decd8945ced7f</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Thailand History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2671_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>d7aa0bf5f0f86e68711f68f2ff8bc7c1</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Asia Pacific History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2671_16.0.2.401(EX01)<br><details><summary>MD5</summary><code>8092cdb0dcf5a44e27ff8b863bbcde89</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Mexico History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2671_16.0.1.302(EX01)<br><details><summary>MD5</summary><code>18d2e0aadec512467ad8f7b38c40d115</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>China History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| PKH110_16.0.2.401(CN01)<br><details><summary>MD5</summary><code>00b0dede5abeff5658076861f2ea8792</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-04 | ✅ Safe |
| PKH110_16.0.1.302(CN01)<br><details><summary>MD5</summary><code>8fb8fbb2d3f009fe0e5ecc9e211736e0</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-06 | ✅ Safe |
| PKH110_16.0.0.208(CN01)<br><details><summary>MD5</summary><code>b2c749968762898844999f838b9a658f</code></details> | 0 | Major: 3, Minor: 0 | 2026-03-18 | ✅ Safe |
| PKH110_15.0.1.860(CN01)<br><details><summary>MD5</summary><code>367e3b4be47bcea04f101d4c4aefe5d1</code></details> | 0 | Major: 3, Minor: 0 | 2026-02-26 | ✅ Safe |

</details>


---

### Oppo Find N3

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Singapore | CPH2499 | CPH2499_16.0.3.505(EX01)<br><details><summary>MD5</summary><code>b7b3a230dfe513127dbb292ed6b045b0</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Taiwan | CPH2499 | CPH2499_16.0.3.505(EX01)<br><details><summary>MD5</summary><code>9bfc00e1335a3f6dab6ccdeacf242d65</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Malaysia | CPH2499 | CPH2499_16.0.3.505(EX01)<br><details><summary>MD5</summary><code>19cc7654da5c2e342268ab804c8fb464</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Indonesia | CPH2499 | CPH2499_16.0.3.505(EX01)<br><details><summary>MD5</summary><code>c7978bb9b21f5ab05179ce1957e1e7fa</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Thailand | CPH2499 | CPH2499_16.0.3.505(EX01)<br><details><summary>MD5</summary><code>7be67cb2c369073250877959ca0ca104</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Vietnam | CPH2499 | CPH2499_16.0.3.505(EX01)<br><details><summary>MD5</summary><code>08baa3b9dc0fbf4f56897da909dddb18</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Oceania | CPH2499 | CPH2499_16.0.3.505(EX01)<br><details><summary>MD5</summary><code>d16a29224fce0f371833e7077dd6e389</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Singapore History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2499_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>0d6ec3447fd78d448810857cdb0b2d5b</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-21 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Taiwan History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2499_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>202302d926d361279622913314cf2c6c</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-23 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Malaysia History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2499_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>f9cbe5cdb1cda3f8a1fa46e7a60c3bfe</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-23 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Indonesia History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2499_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>fe33546e7733610b7b0e39a49d0f923f</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-17 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Thailand History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2499_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>b7cfb500593a0367872fbf860d1d31f5</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-21 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Vietnam History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2499_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>fa577cadcd61718f70d11d12bce8f3ee</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-21 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Oceania History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2499_16.0.3.500(EX01)<br><details><summary>MD5</summary><code>c5977aa2232a230e43012cc872dd9109</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-24 | ✅ Safe |
| CPH2499_16.0.0.203(EX01)<br><details><summary>MD5</summary><code>1c4c4bcffbef770d54aff9d8f569ffb1</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-11 | ✅ Safe |

</details>


---

### Oppo Find X5 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | CPH2305 | CPH2305_15.0.0.1303(EX01)<br><details><summary>MD5</summary><code>e242b3d05c10cdfeeda73d70656b8ef5</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Singapore | CPH2305 | CPH2305_16.0.3.501(EX01)<br><details><summary>MD5</summary><code>2409c487fa9f44fd5b9aee130fabc8c9</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Taiwan | CPH2305 | CPH2305_16.0.3.510(EX01)<br><details><summary>MD5</summary><code>cad47f9b17760e4549cbb82af3c85b13</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Oceania | CPH2305 | CPH2305_11_A.22<br><details><summary>MD5</summary><code>d47d75e64707954fece8083ddb3c5437</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |
| Egypt | CPH2305 | CPH2305_11_A.19<br><details><summary>MD5</summary><code>f61010fa1d6349cc6e8000f62c70b670</code></details> | **0** | Major: 2, Minor: 0 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Singapore History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2305_15.0.0.1301(EX01)<br><details><summary>MD5</summary><code>81aa48b49783dffec339e362edeb230b</code></details> | 0 | Major: 2, Minor: 0 | 2026-02-25 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Taiwan History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2305_15.0.0.1301(EX01)<br><details><summary>MD5</summary><code>f872fdd23787fec04579586d7a34ac20</code></details> | 0 | Major: 2, Minor: 0 | 2026-03-30 | ✅ Safe |

</details>


---

### Oppo Find X5

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | CPH2307 | CPH2307_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>2e4983e349bea6c8122a4cb7122fce2e</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Oceania | CPH2307 | CPH2307_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>459ce1072fbd5f00c30b7c69cae5fb1f</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Egypt | CPH2307 | CPH2307_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>fe06415c8aa4aad526cb40e776ba9b36</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Saudi Arabia | CPH2307 | CPH2307_15.0.0.1600(EX01)<br><details><summary>MD5</summary><code>e08d24c25c9ca0b7187849047b819e76</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

<details>
<summary>📜 <b>Europe History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2307_15.0.0.1304(EX01)<br><details><summary>MD5</summary><code>49b35b780091e214da73b2ba51034c8c</code></details> | 0 | Major: 0, Minor: 120 | 2026-02-26 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Oceania History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2307_15.0.0.1302(EX01)<br><details><summary>MD5</summary><code>fbf19255ade70753b33e310b1dbd35c3</code></details> | 0 | Major: 0, Minor: 120 | 2026-03-02 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Egypt History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2307_15.0.0.1302(EX01)<br><details><summary>MD5</summary><code>9ca6d58709b963d43df51a90a08e2128</code></details> | 0 | Major: 0, Minor: 120 | 2026-02-24 | ✅ Safe |

</details>

<details>
<summary>📜 <b>Saudi Arabia History</b> (click to expand)</summary>

| Firmware Version | ARB | OEM Version | Last Seen | Safe |
|:---|:---|:---|:---|:---|
| CPH2307_15.0.0.1302(EX01)<br><details><summary>MD5</summary><code>7b946f15e2b828d937db541b0586897b</code></details> | 0 | Major: 0, Minor: 120 | 2026-02-27 | ✅ Safe |

</details>


---

### Oppo Find X3 Pro

| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |
|:---|:---|:---|:---|:---|:---|:---|
| Europe | CPH2173 | CPH2173_14.0.0.2102(EX01)<br><details><summary>MD5</summary><code>81bc0356f4e9dee62a305db9be52c3a8</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Singapore | CPH2173 | CPH2173_14.0.0.2102(EX01)<br><details><summary>MD5</summary><code>0d2005b4b7818ccdc3590096b88d8d09</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |
| Taiwan | CPH2173 | CPH2173_14.0.0.2102(EX01)<br><details><summary>MD5</summary><code>4de6a395dea47703937b9786949868a5</code></details> | **0** | Major: 0, Minor: 120 | 2026-04-12 | ✅ Safe |

---

## 🤖 On-Demand ARB Checker

You can check the ARB index of any OnePlus Ozip/Zip URL manually using our automated workflow.

### How to use:
1. Go to the [Issues Tab](https://github.com/Bartixxx32/OnePlus-antirollchecker/issues).
2. Click **"New Issue"**.
3. Set the **Title** to start with `[CHECK]` (e.g., `[CHECK] OnePlus 12 Update`).
4. Paste the **Firmware Download URL** (direct link ending in `.zip`) in the description.
5. Click **"Submit New Issue"**.

The bot will automatically pick up the request, analyze the firmware, and post the results as a comment on your issue.

---

## 🌐 OOS Downloader API

Need direct download URLs for OnePlus firmware? Use our **OOS Downloader API**!

🌐 **API Endpoint**: [https://oosdownloader-gui.fly.dev/](https://oosdownloader-gui.fly.dev/)

Our OOS Downloader API provides direct, signed download URLs for OnePlus OTA firmware files by leveraging the [Oxygen Updater API](https://play.google.com/store/apps/details?id=com.arjanvlek.oxygenupdater).

---

## Credits

- **Payload Extraction**: [otaripper](https://github.com/syedinsaf/otaripper) by syedinsaf
- **Payload Extraction (Fallback)**: [payload-dumper-go](https://github.com/ssut/payload-dumper-go) by ssut
- **ARB Extraction**: [arbextract](https://github.com/koaaN/arbextract) by koaaN
- **API for CN variants**: [roms.danielspringer.at](https://roms.danielspringer.at/) by Daniel Springer
- **Firmware API**: [Oxygen Updater](https://play.google.com/store/apps/details?id=com.arjanvlek.oxygenupdater)

---

## 📱 Android App

Prefer a native mobile experience? We have an official Android app on F-Droid! Check firmware statuses, view ARB indices, and stay protected directly from your phone.

[<img src="https://f-droid.org/badge/get-it-on.png"
    alt="Get it on F-Droid"
    height="80">](https://f-droid.org/packages/com.bartixxx.oneplusarbchecker/)

## 💬 Community & Support

- **Telegram Group:** [@oneplusarbchecker](https://t.me/oneplusarbchecker)

> **Important:** The bot **only** works within this group to prevent spam and ensure availability. DM checks are disabled.

---
*Last updated: 2026-04-12 03:27 UTC*