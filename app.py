import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configurazione Dashboard
st.set_page_config(page_title="REER Master Scaglioni", layout="centered")

# CSS per look scuro e pulito
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    div[data-testid="stMetric"] { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Master degli Scaglioni REER")
st.caption("Analisi chirurgica soglie fiscali Québec/Federal 2026")

# --- DATI FISCALI 2026 (COMBINATI QC + FED) ---
SCAGLIONI = [
    (0, 0.25),        # Fino a 51k
    (51708, 0.3253),  # Da 51k a 103k
    (103545, 0.4112), # Da 103k a 126k
    (126000, 0.4571), # Da 126k a 173k
    (173205, 0.50),   # Da 173k a 240k
    (243723, 0.53)    # Oltre 243k
]

# --- SIDEBAR INPUT ---
with st.sidebar:
    st.header("Configurazione")
    reddito_lordo = st.number_input("Salario Base Lordo ($)", value=80000, step=1000)
    tasso_prestito = st.slider("Interesse Prestito (%)", 0.0, 15.0, 6.0) / 100
    contributo = st.select_slider(
        "Importo REER ($)",
        options=[0, 1000, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000],
        value=10000
    )
    mesi_prestito = st.number_input("Mesi per ripagare il debito residuo", value=12)

# --- LOGICA DI CALCOLO FISCALE ---
def calcola_tasse(r):
    tasse = 0
    # Calcolo a scaglioni progressivi
    for i in range(len(SCAGLIONI)):
        soglia_attuale = SCAGLIONI[i][0]
        aliquota = SCAGLIONI[i][1]
        soglia_successiva = SCAGLIONI[i+1][0] if i < len(SCAGLIONI)-1 else float('inf')
        
        if r > soglia_attuale:
            tassabile = min(r, soglia_successiva) - soglia_attuale
            tasse += tassabile * aliquota
    return tasse

tasse_senza = calcola_tasse(reddito_lordo)
tasse_con = calcola_tasse(reddito_lordo - contributo)
refund = tasse_senza - tasse_con

# --- LOGICA PRESTITO (CASH FLOW) ---
# Assumiamo rimborso al mese 3
int_fase_1 = (contributo * tasso_prestito / 12) * 3
capitale_residuo = max(0, contributo - refund)
int_fase_2 = (capitale_residuo * tasso_prestito / 12) * mesi_prestito
interessi_totali = int_fase_1 + int_fase_2
guadagno_netto = refund - interessi_totali

# --- METRICHE PRINCIPALI ---
c1, c2, c3 = st.columns(3)
c1.metric("Refund Totale", f"${int(refund):,}")
c2.metric("Costo Interessi", f"${int(interessi_totali):,}", delta_color="inverse")
c3.metric("Guadagno Netto", f"${int(guadagno_netto):,}")

# --- GRAFICO SCAGLIONI ---
st.write("### 📉 Analisi Visiva Scaglioni")
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#0b0e14')
ax.set_facecolor('#0b0e14')

# Disegno scalini
for i in range(len(SCAGLIONI)):
    x_start = SCAGLIONI[i][0]
    x_end = SCAGLIONI[i+1][0] if i < len(SCAGLIONI)-1 else reddito_lordo * 1.2
    y = SCAGLIONI[i][1]
    ax.hlines(y * 100, x_start, x_end, colors='#30363d', linestyles='--')
    ax.text(x_start, y * 100 + 1, f"{int(y*100)}%", color='#8b949e', fontsize=9)

# Evidenzia area REER
ax.axvspan(reddito_lordo - contributo, reddito_lordo, color='#00ffcc', alpha=0.2, label='Area Risparmio REER')
ax.axvline(reddito_lordo, color='white', label='Reddito Attuale')
ax.axvline(reddito_lordo - contributo, color='#00ffcc', linestyle='--', label='Nuovo Imponibile')

ax.set_ylabel("Aliquota Combinata (%)", color='white')
ax.set_xlabel("Reddito Lordo ($)", color='white')
ax.tick_params(colors='white')
ax.legend()
st.pyplot(fig)



# --- ANALISI TECNICA ---
st.divider()
aliquota_marg = 0
for s, a in reversed(SCAGLIONI):
    if reddito_lordo > s:
        aliquota_marg = a
        break

st.write(f"💡 **Il tuo ultimo dollaro è tassato al {int(aliquota_marg*100)}%.**")
if (reddito_lordo - contributo) < 51708:
    st.warning("⚠️ Stai scendendo sotto i 51.700$. Qui l'aliquota cala al 25%, l'efficienza del REER diminuisce drasticamente.")
elif (reddito_lordo > 103545) and (reddito_lordo - contributo < 103545):
    st.success("✅ Strategia Eccellente: Hai abbattuto lo scaglione del 41%!")
