import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="REER Optimizer QC", layout="wide")

st.title("🚀 Ottimizzatore REER & Prestito - Québec 2026")

# Sidebar per i parametri
st.sidebar.header("Parametri Reddito e Prestito")
reddito = st.sidebar.number_input("Tuo Reddito Lordo ($)", value=100000, step=1000)
tasso_interesse = st.sidebar.slider("Tasso interesse prestito (%)", 0.0, 15.0, 5.0) / 100
mesi = st.sidebar.number_input("Mesi per ripagare il residuo", value=12, min_value=1)

# Slider principale per la contribuzione
contributo_totale = st.select_slider(
        "Trascina per vedere quanto versare (incluso eventuale prestito):",
            options=[0, 1000, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000],
                value=10000
)

# Logica Fiscale QC 2026 (Semplificata)
soglia = 98000
refund = 0
for i in range(int(contributo_totale)):
    if (reddito - i) > soglia:
            refund += 0.3712
                else:
                        refund += 0.3253

                        # Logica Prestito
                        interessi_primi_3_mesi = (contributo_totale * tasso_interesse / 12) * 3
                        capitale_residuo = max(0, contributo_totale - refund)
                        interessi_restanti = (capitale_residuo * tasso_interesse / 12) * mesi
                        totale_interessi = interessi_primi_3_mesi + interessi_restanti
                        profitto_netto = refund - totale_interessi

                        # Layout a colonne per i risultati
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Rimborso Tasse", f"${int(refund):,}")
                        col2.metric("Costo Interessi", f"${int(totale_interessi):,}", delta_color="inverse")
                        col3.metric("Guadagno Netto", f"${int(profitto_netto):,}", delta=f"{int(profitto_netto)}")

                        # Grafico Dinamico
                        st.subheader("Analisi Convenienza")
                        fig, ax = plt.subplots(figsize=(10, 4))
                        ax.set_facecolor("#0e1117")
                        fig.patch.set_facecolor("#0e1117")

                        labels = ['Rimborso (Stato)', 'Interessi (Banca)']
                        values = [refund, totale_interessi]
                        colors = ['#2ecc71', '#ff4b4b']

                        ax.barh(labels, values, color=colors)
                        ax.tick_params(axis='x', colors='white')
                        ax.tick_params(axis='y', colors='white')
                        st.pyplot(fig)

                        if profitto_netto > 0:
                            st.success(f"✅ Conviene! Stai guadagnando ${int(profitto_netto)} grazie all'arbitraggio fiscale.")
                            else:
                                st.error("❌ Non conviene: gli interessi del prestito mangiano il risparmio fiscale.")
                                
)