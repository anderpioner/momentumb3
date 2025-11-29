import streamlit as st
import pandas as pd
import importlib
import stock_ranker # Import the module, not just the function

# Set page config
st.set_page_config(page_title="Stock Ranker", layout="wide")

# Sidebar with description
st.sidebar.title("Sobre")
st.sidebar.markdown("""
Este aplicativo classifica ações com base em retornos históricos ponderados:
- **40%**: Últimos 63 dias
- **30%**: Dia 63 a 126
- **20%**: Dia 126 a 189
- **10%**: Dia 189 a 252

O **Rating** é o percentil da pontuação da ação em relação às outras (0-100).
""")

st.title("Ranking de Ações")

# Default full list of tickers
default_tickers = "ORVR3, CBAV3, VVEO3, ONCO3, RCSL4, RCSL3, ENEV3, JALL3, CASH3, EVEN3, AGRO3, AZZA3, VAMO3, BPAN4, LJQQ3, JSLG3, SOJA3, TUPY3, PGMN3, IRBR3, PLPL3, TTEN3, ALPA4, MYPK3, HBSA3, ISAE4, VLID3, DXCO3, CVCB3, BLAU3, BRKM5, GGPS3, VBBR3, CURY3, IGTI11, VIVA3, CPLE3, ANIM3, AURE3, SBFG3, BRAP4, ASAI3, CYRE3, SEER3, YDUQ3, SBSP3, CPFE3, SYNE3, LEVE3, EQTL3, MOVI3, CEAB3, POSI3, SLCE3, SIMH3, CMIN3, RECV3, MDNE3, AMOB3, USIM5, CSNA3, GFSA3, RDOR3, RAIL3, NEOE3, TOTS3, CSMG3, CMIG4, TFCO4, GMAT3, HYPE3, PSSA3, QUAL3, MULT3, SAPR11, ABCB4, PCAR3, NATU3, LREN3, RADL3, PNVL3, FRAS3, PETZ3, SUZB3, SANB11, RAPT4, GUAR3, HAPV3, WEGE3, TIMS3, SMTO3, INTB3, CXSE3, ECOR3, MOTV3, TGMA3, TEND3, ABEV3, BPAC11, ODPV3, RANI3, KLBN11, PRIO3, LOGG3, DIRR3, MGLU3, GGBR4, KEPL3, GOAU4, BBAS3, VALE3, FLRY3, UNIP6, ENGI11, BRBI11, EZTC3, ALUP11, LAVV3, BBSE3, TAEE11, MILS3, LWSA3, ARML3, BMOB3, PETR3, GRND3, PETR4, UGPA3, ALOS3, MDIA3, EGIE3, BEEF3, RAIZ4, MRVE3, VIVT3, POMO4, ITSA4, ITUB3, JHSF3, ITUB4, BBDC3, BBDC4, FESA4, CAML3, BHIA3, CSAN3, RENT3, B3SA3, VULC3, BRSR6, BRAV3, SMFT3, COGN3, MBRF3, EMBJ3, CPLE5, AXIA6, AXIA3, BMEB4, VTRU3, ROMI3, DEXP3, HBRE3, REAG3, BRSR3, BRKM3, MEAL3, ALPA3, DOTZ3, TRAD3, DEXP4, GOAU3, GOAU3, CLSC4, PTBL3, TECN3, ETER3, AERI3, AERI3, SHOW3, HBOR3, PDTC3, WIZC3, RNEW3, MATD3, WDCN3, CCTY3, PFRM3, AALR3, ALPK3, BMEB3, MLAS3, ADMF3, DESK3, OFSA3, OFSA3, RDNI3, EUCA4, RVEE3, VITT3, ALLD3, ALLD3, POMO3, SCAR3, WEST3, TASA3, BRAP3, TPIS3, FHER3, LPSB3, MTRE3, LAND3, RNEW4, RNEW4, ISAE3, LOGN3, RAPT3, CSED3, BRST3, AMAR3, USIM3, VSTE3, MELK3, CEDO4, CEDO4, GGBR3, UCAS3, ITSA3, TASA4, LUPA3, FIQE3, FIQE3, BMGB4, OPCT3, ENJU3, DASA3, SEQL3, SEQL3, TRIS3, CMIG3, TCSA3, PINE3, ESPA3, ESPA3, EUCA3, PINE4, TOKY3, AVLL3, CSUD3, NGRD3, NGRD3, DMVF3"

# Input area (hidden by default to clean up UI, but accessible)
with st.expander("Editar Lista de Ações"):
    tickers_input = st.text_area("Insira os Tickers (separados por vírgula)", value=default_tickers, height=150)

if not tickers_input:
    st.warning("Por favor, insira pelo menos um ticker.")
else:
    # Auto-run
    # Force reload of the module to pick up changes (kept for safety)
    importlib.reload(stock_ranker)
    
    # Clean input
    tickers = [t.strip() for t in tickers_input.split(',')]
    tickers = sorted(list(set(tickers))) # Deduplicate and sort
    
    # Run calculation
    # Use st.cache_data to avoid re-running on every interaction if inputs haven't changed
    # But for now, direct call is fine as per "Assim que alguém acessar"
    with st.spinner("Calculando ranking..."):
        df_results = stock_ranker.calculate_rankings(tickers)
    
    if df_results.empty:
        st.error("Nenhum dado encontrado para os tickers fornecidos.")
    else:
        # Display simplified table: Rank, Ticker, Rating, Last Month, Link, Fundamentus
        df_display = df_results[['Rank', 'Ticker', 'Rating', 'Last Month']].copy()
        
        # Add TradingView Link
        # Format: https://www.tradingview.com/chart/?symbol=BMFBOVESPA:PETR4&interval=D
        df_display['Link'] = df_display['Ticker'].apply(
            lambda t: f"https://www.tradingview.com/chart/?symbol=BMFBOVESPA:{t}&interval=D"
        )
        
        # Add Fundamentus Link
        # Format: https://www.fundamentus.com.br/detalhes.php?papel=PETR4
        df_display['Fundamentus'] = df_display['Ticker'].apply(
            lambda t: f"https://www.fundamentus.com.br/detalhes.php?papel={t}"
        )
        
        # Calculate height to avoid internal scrollbar (approx 35px per row + 38px header)
        # This makes the table expand vertically so the page scrolls, not the table.
        table_height = (len(df_display) + 1) * 35 + 3
        
        # Apply styling/formatting
        # use_container_width=True makes it full width
        st.dataframe(
            df_display,
            column_config={
                "Rating": st.column_config.NumberColumn(
                    "Rating",
                    format="%.1f",
                ),
                "Last Month": st.column_config.LineChartColumn(
                    "Tendência (Mês)",
                    y_min=None, # Auto-scale to data range
                    y_max=None, # Auto-scale
                ),
                "Link": st.column_config.LinkColumn(
                    "Gráfico",
                    display_text="TradingView"
                ),
                "Fundamentus": st.column_config.LinkColumn(
                    "Fundamentus",
                    display_text="Fundamentus"
                )
            },
            use_container_width=True,
            hide_index=True,
            height=table_height
        )
        
        # Download button
        # We don't want the list of prices in the CSV, so we drop it from the download if present
        df_download = df_results.drop(columns=['Last Month']) if 'Last Month' in df_results.columns else df_results
        csv = df_download.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar Resultados (CSV)",
            data=csv,
            file_name='ranking_acoes.csv',
            mime='text/csv',
        )
