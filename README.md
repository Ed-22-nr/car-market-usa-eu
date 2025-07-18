# US vs EU Car Market Analyzer 🚗

Un'applicazione **Streamlit** per analizzare il mercato delle auto usate negli **USA** e confrontarlo con l'**Europa**, stimando i costi di importazione e il potenziale profitto.

---

## ✅ Funzionalità principali
- **Dataset simulato** per auto USA ed EU, filtrabile per:
  - Modello
  - Anni di produzione (con auto-calcolo se non inseriti)
  - Chilometraggio massimo
  - Condizione (scarse, buone, ottime)
- **Prezzi in USD e EUR** (conversione live con exchangerate.host)
- **Analisi comparativa** tra prezzi medi USA e EU
- **Grafici interattivi** (distribuzione prezzi)
- **Simulatore import**:
  - Calcolo costi (dazi, IVA, spedizione, omologazione, extra)
  - Stima del **profitto**
  - Indicatore profittabilità
- **Esportazione dati in CSV** (USA ed EU)

---

## 🔧 Installazione locale
Clona il repo e installa le dipendenze:

```bash
pip install -r requirements.txt
