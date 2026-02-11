import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Optimiseur REER QC", layout="wide")

st.title("🚀 Optimiseur REER & Prêt - Québec 2026")

# Barre latérale pour les paramètres
st.sidebar.header("Paramètres de Revenu et Prêt")
reddito = st.sidebar.number_input("Votre Revenu Brut ($)", value=100000, step=1000)
tasso_interesse = st.sidebar.slider("Taux d'intérêt du prêt (%)", 0.0, 15.0, 5.0) / 100
mesi = st.sidebar.number_input("Mois pour rembourser le solde", value=12, min_value=1)

# Curseur principal pour la contribution
contributo_totale = st.select_slider(
    "Faites glisser pour voir combien verser (y compris prêt potentiel):",
    options=[0, 1000, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000],
    value=10000
)

# Logique Fiscale QC 2026 - Optimisée
soglia = 98000
tasso_alto = 0.3712
tasso_basso = 0.3253

# Calcul du remboursement fiscal
if reddito > soglia:
    # Portion au-dessus du seuil au taux élevé
    importo_alto = min(contributo_totale, reddito - soglia)
    importo_basso = contributo_totale - importo_alto
    rimborso = (importo_alto * tasso_alto) + (importo_basso * tasso_basso)
else:
    rimborso = contributo_totale * tasso_basso

# Logique du Prêt
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

