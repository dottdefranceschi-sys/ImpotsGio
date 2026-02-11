import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="REER Tax Bracket Master", layout="centered")

# CSS per look professionale
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .status-box { background-color: #161b22; border-radius: 10px; padding: 20px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Master degli Scaglioni REER")
st.caption("Ottimizzazione chirurgica basata sulle soglie fiscali Québec/Federal 2026")

# --- DATI FISCALI 2026 (COMBINATI QC + FED - STIME) ---
# Struttura: (Soglia reddito, Aliquota Marginale Combinata)
SCAGLIONI = [
    (0, 0.25),        # Fino a 51k circa
    (51708, 0.32),    # Da 51k a 103k
    (103545, 0.41),   # Da 103k a 126k
    (126000, 0.45),   # Da 126k a 173k
    (173205, 0.50),   # Da 173k a 240k
    (243723, 0.53)    # Oltre 243k
]

# --- INPUT ---
with st.sidebar:
    st.header("Configurazione")
    reddito_lordo = st.number_input("Salario Base Lordo ($)", value=80000, step=1000)
    tasso_prestito = st.slider("Interesse Prestito (%)", 0.0, 15.0, 6.0) / 100
    contributo = st.select_slider(
        "Importo REER ($)",
        options=[0, 1000, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 60000],
        value=10000
    )

# --- LOGICA DI CALCOLO PUNTUALE ---
def calcola_tasse(r):
    tasse = 0
    precedente_soglia = 0
    for soglia, aliquota in SCAGLIONI:
        if r > soglia:
            tassabile = min(r - soglia, (SCAGLIONI[SCAGLIONI.index((soglia, aliquota))+1][0] - soglia) if SCAGLIONI.index((soglia, aliquota)) < len(SCAGLIONI)-1 else r - soglia)
            tasse += tassabile * aliquota
    return tasse

tasse_senza = calcola_tasse(reddito_lordo)
tasse_con = calcola_tasse(reddito_lordo - contributo)
refund = tasse_senza - tasse_con

# Interessi (Logica 3 mesi per il refund)
interessi = (contributo * tasso_prestito / 12 * 3) + (max(0, contributo-refund) * tasso_prestito / 12 * 12)
guadagno_netto = refund - interessi

# --- VISUALIZZAZIONE ---
st.markdown('<div class="status-box">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Refund Totale", f"${int(refund):,}")
c2.metric("Efficienza", f"{int((refund/contributo)*100) if contributo > 0 else 0}%")
c3.metric("Netto (Post Interessi)", f"${int(guadagno_netto):,}")
st.markdown('</div>', unsafe_allow_html=True)

# --- GRAFICO DEGLI SCAGLIONI (L'IMPATTO VISIVO) ---
st.write("### 📉 Il tuo reddito e le soglie fiscali")
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#0b0e14')
ax.set_facecolor('#0b0e14')

# Disegna i gradini degli scaglioni
soglie_x = [s[0] for s in SCAGLIONI] + [max(reddito_lordo * 1.2, 150000)]
aliquote_y = [s[1] for s in SCAGLIONI]

for i in range(len(SCAGLIONI)):
    x_start = SCAGLIONI[i][0]
    x_end = SCAGLIONI[i+1][0] if i < len(SCAGLIONI)-1 else soglie_x[-1]
    y = SCAGLIONI[i][1]
    ax.hlines(y, x_start, x_end, colors='gray', linestyles='--', alpha=0.5)
    ax.text(x_start, y + 0.01, f"{int(y*100)}%", color='gray', fontsize=8)

# Evidenzia la zona del tuo reddito
ax.axvspan(reddito_lordo - contributo, reddito_lordo, color='#00ffcc', alpha=0.3, label='Riduzione REER')
ax.axvline(reddito_lordo, color='white', linestyle='-', label='Reddito Iniziale')
ax.axvline(reddito_lordo - contributo, color='#00ffcc', linestyle='-', label='Nuovo Imponibile')

ax.set_ylabel("Aliquota Fiscale (%)", color='white')
ax.set_xlabel("Reddito Annuo ($)", color='white')
ax.tick_params(colors='white')
ax.legend()
st.pyplot(fig)

# --- SPIEGAZIONE DINAMICA ---
st.divider()
nuovo_reddito = reddito_lordo - contributo
aliquota_marginale = 0
for s, a in reversed(SCAGLIONI):
    if reddito_lordo > s:
        aliquota_marginale = a
        break

st.write(f"💡 **Analisi Tecnica:**")
st.write(f"- Il tuo ultimo dollaro è tassato al **{int(aliquota_marginale*100)}%**.")
if nuovo_reddito < 51708:
    st.warning("⚠️ Stai scendendo sotto i 51k. Qui il risparmio è minimo (25%), forse stai mettendo troppo nel REER.")
elif reddito_lordo > 103545 and nuovo_reddito < 103545:
    st.success("✅ OTTIMO: Hai 'scavallato' la soglia dei 103k. Hai evitato la tassazione al 41% su una parte del reddito!")
interessi_primi_3_mesi = (contributo_totale * tasso_interesse / 12) * 3
capitale_residuo = max(0, contributo_totale - rimborso)
interessi_restanti = (capitale_residuo * tasso_interesse / 12) * mesi
totale_interessi = interessi_primi_3_mesi + interessi_restanti
profitto_netto = rimborso - totale_interessi

# Affichage des résultats en colonnes
col1, col2, col3 = st.columns(3)
col1.metric("Remboursement Fiscal", f"${int(rimborso):,}")
col2.metric("Frais d'Intérêt", f"${int(totale_interessi):,}", delta_color="inverse")
col3.metric("Gain Net", f"${int(profitto_netto):,}", delta=f"{int(profitto_netto)}")

# Graphique Dynamique
st.subheader("Analyse de Rentabilité")
fig, ax = plt.subplots(figsize=(10, 4))
ax.set_facecolor("#0e1117")
fig.patch.set_facecolor("#0e1117")

labels = ['Remboursement (État)', 'Intérêts (Banque)']
values = [rimborso, totale_interessi]
colors = ['#2ecc71', '#ff4b4b']

ax.barh(labels, values, color=colors)
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_xlabel('Montant ($)', color='white')
st.pyplot(fig)

# Message de recommandation
if profitto_netto > 0:
    st.success(f"✅ Rentable! Vous gagnez ${int(profitto_netto)} grâce à l'arbitrage fiscal.")
else:
    st.error("❌ Non rentable: les intérêts du prêt réduisent les économies fiscales.")                                

