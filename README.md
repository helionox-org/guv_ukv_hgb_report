# GuV nach Umsatzkostenverfahren (HGB § 275) - ERPNext Version 16 App

This repository contains the custom Frappe/ERPNext app `guv_ukv_hgb_report` which implements the German vertical Profit and Loss Statement following the **Cost of Sales Method (Umsatzkostenverfahren)** as defined by **HGB § 275 Abs. 3**, based on the **SKR04** Chart of Accounts 2026 version (which is published and used by DATEV). Extensive care was taken to transfer the relevant Chart of Accounts positions from the DATEV document to frappe. You can find the `.csv` file fro import in `/SKR04_Blueprint_chart_of_accounts.csv`

The repository uses the code of frappes implementation of the proit_and_loss_statement.py. However, it is heavily modified to fit the financial needs of German HGB law.

The app is fully integrated with standard ERPNext and features:

1. **Standalone script report**: Available in the Financial Reports workspace according to the Umsatzkostenverfahren nach HGB § 275 Abs. 3.
2. **New Cost Centers**: Added the cost centers Herstellungskosten, Vertriebskosten, Verwaltungskosten, Sonstige betriebliche Aufwendungen (english: Manufacturing Costs, Sales Costs, Administration Costs, Other Business Expenses) which are required to map the positions from the chart of accounts into the correct positions of the profit and loss calculation. You have to assign the correct Cost Center to the Journal Entries bookings when doing your accounting. Additionally, the Cost Centers have a custom field now called `umsatzkostenverfahren_type` which needs to be provided for these specific cost centers.
3. **Updated Chart of Accounts**: Transfered the 2026 chart of accounts to frappe

---

## Legal Notice & Disclaimer

This repository, including the `guv_ukv_hgb_report` application and the `SKR04_Blueprint_chart_of_accounts.csv`, is provided under the **GNU General Public License v3.0 (GPLv3)**.

### Important Notice

While this project was developed with care and testing based on **HGB § 275 Abs. 3 (Cost of Sales Method)** and the **SKR04 2026** standards, please note the following:

- **No Professional Advice:** This software is not a substitute for professional accounting or tax advice. Financial regulations are complex and subject to individual interpretation and legislative changes.
- **Verification Required:** Users are responsible for verifying that the mappings within the Chart of Accounts and the resulting financial reports meet the requirements of their specific entity and local tax authority (e.g. _Finanzamt_).
- **Limitation of Liability:** As stated in the LICENSE file, this software is provided **"as is"**, without warranty of any kind. The contributors of this project shall not be held liable for any damages, tax penalties, or financial discrepancies arising from the use of this software or its outputs.

> **Recommendation:** We strongly advise having the configuration and reporting output reviewed by a qualified accountant or _Steuerberater_ before using it for formal financial statements or tax filings.
