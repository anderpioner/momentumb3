import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(tickers):
    """
    Fetches historical data for the given tickers.
    We need at least 252 trading days of history.
    Fetching 400 calendar days to be safe.
    """
    # Append .SA for Brazilian stocks if not present (simple heuristic)
    # The user provided list: PETR4, BBAS3, etc. usually need .SA for yfinance
    sa_tickers = [t + ".SA" if not t.endswith(".SA") else t for t in tickers]
    
    # Download data
    # We need the 'Adj Close' to account for dividends and splits which is better for return calculation
    data = yf.download(sa_tickers, period="2y", auto_adjust=True)['Close']
    
    return data

def calculate_rankings(tickers):
    print("Fetching data...")
    data = get_stock_data(tickers)
    
    results = []
    
    for ticker_sa in data.columns:
        # Get series for the ticker and drop NaNs (some might have different holidays or start dates)
        series = data[ticker_sa].dropna()
        
        # We need at least 253 points to calculate return from -252
        if len(series) < 253:
            print(f"Warning: Not enough data for {ticker_sa}. Skipping.")
            continue
            
        # Get the prices at the specific windows
        # Using negative indexing: -1 is today/latest, -64 is 63 days ago (window size)
        # Note: The prompt asks for "last 63 days", "63 to 126", etc.
        # We assume these are trading days.
        
        try:
            p_now = series.iloc[-1]
            p_63 = series.iloc[-1 - 63]
            p_126 = series.iloc[-1 - 126]
            p_189 = series.iloc[-1 - 189]
            p_252 = series.iloc[-1 - 252]
            
            # Calculate returns
            # Return 1: Last 63 days
            r1 = (p_now / p_63) - 1
            
            # Return 2: 63 to 126 days ago
            r2 = (p_63 / p_126) - 1
            
            # Return 3: 126 to 189 days ago
            r3 = (p_126 / p_189) - 1
            
            # Return 4: 189 to 252 days ago
            r4 = (p_189 / p_252) - 1
            
            # Weighted Score
            # 40% * r1 + 30% * r2 + 20% * r3 + 10% * r4
            score = (0.40 * r1) + (0.30 * r2) + (0.20 * r3) + (0.10 * r4)
            
            # Get last 22 prices (approx 1 month of trading) for sparkline
            # Ensure we have enough data
            last_month_prices = series.iloc[-22:].tolist() if len(series) >= 22 else series.tolist()
            
            results.append({
                'Ticker': ticker_sa.replace('.SA', ''), # Remove .SA for display
                'Score': score,
                'R_63d': r1,
                'R_126d': r2,
                'R_189d': r3,
                'R_252d': r4,
                'Last Month': last_month_prices
            })
            
        except IndexError:
             print(f"Error: Index out of bounds for {ticker_sa} despite length check.")
             continue

    # Create DataFrame
    df_results = pd.DataFrame(results)
    
    if not df_results.empty:
        # Calculate Rating (Percentile)
        # rank(pct=True) gives percentile from 0 to 1. Multiply by 100.
        df_results['Rating'] = df_results['Score'].rank(pct=True) * 100
        
        # Sort by Score descending
        df_results = df_results.sort_values(by='Score', ascending=False).reset_index(drop=True)
        
        # Add Rank column (1-based)
        df_results['Rank'] = df_results.index + 1
    
    return df_results

def main():
    raw_tickers = "ORVR3, CBAV3, VVEO3, ONCO3, RCSL4, RCSL3, ENEV3, JALL3, CASH3, EVEN3, AGRO3, AZZA3, VAMO3, BPAN4, LJQQ3, JSLG3, SOJA3, TUPY3, PGMN3, IRBR3, PLPL3, TTEN3, ALPA4, MYPK3, HBSA3, ISAE4, VLID3, DXCO3, CVCB3, BLAU3, BRKM5, GGPS3, VBBR3, CURY3, IGTI11, VIVA3, CPLE3, ANIM3, AURE3, SBFG3, BRAP4, ASAI3, CYRE3, SEER3, YDUQ3, SBSP3, CPFE3, SYNE3, LEVE3, EQTL3, MOVI3, CEAB3, POSI3, SLCE3, SIMH3, CMIN3, RECV3, MDNE3, AMOB3, USIM5, CSNA3, GFSA3, RDOR3, RAIL3, NEOE3, TOTS3, CSMG3, CMIG4, TFCO4, GMAT3, HYPE3, PSSA3, QUAL3, MULT3, SAPR11, ABCB4, PCAR3, NATU3, LREN3, RADL3, PNVL3, FRAS3, PETZ3, SUZB3, SANB11, RAPT4, GUAR3, HAPV3, WEGE3, TIMS3, SMTO3, INTB3, CXSE3, ECOR3, MOTV3, TGMA3, TEND3, ABEV3, BPAC11, ODPV3, RANI3, KLBN11, PRIO3, LOGG3, DIRR3, MGLU3, GGBR4, KEPL3, GOAU4, BBAS3, VALE3, FLRY3, UNIP6, ENGI11, BRBI11, EZTC3, ALUP11, LAVV3, BBSE3, TAEE11, MILS3, LWSA3, ARML3, BMOB3, PETR3, GRND3, PETR4, UGPA3, ALOS3, MDIA3, EGIE3, BEEF3, RAIZ4, MRVE3, VIVT3, POMO4, ITSA4, ITUB3, JHSF3, ITUB4, BBDC3, BBDC4, FESA4, CAML3, BHIA3, CSAN3, RENT3, B3SA3, VULC3, BRSR6, BRAV3, SMFT3, COGN3, MBRF3, EMBJ3, CPLE5, AXIA6, AXIA3, BMEB4, VTRU3, ROMI3, DEXP3, HBRE3, REAG3, BRSR3, BRKM3, MEAL3, ALPA3, DOTZ3, TRAD3, DEXP4, GOAU3, GOAU3, CLSC4, PTBL3, TECN3, ETER3, AERI3, AERI3, SHOW3, HBOR3, PDTC3, WIZC3, RNEW3, MATD3, WDCN3, CCTY3, PFRM3, AALR3, ALPK3, BMEB3, MLAS3, ADMF3, DESK3, OFSA3, OFSA3, RDNI3, EUCA4, RVEE3, VITT3, ALLD3, ALLD3, POMO3, SCAR3, WEST3, TASA3, BRAP3, TPIS3, FHER3, LPSB3, MTRE3, LAND3, RNEW4, RNEW4, ISAE3, LOGN3, RAPT3, CSED3, BRST3, AMAR3, USIM3, VSTE3, MELK3, CEDO4, CEDO4, GGBR3, UCAS3, ITSA3, TASA4, LUPA3, FIQE3, FIQE3, BMGB4, OPCT3, ENJU3, DASA3, SEQL3, SEQL3, TRIS3, CMIG3, TCSA3, PINE3, ESPA3, ESPA3, EUCA3, PINE4, TOKY3, AVLL3, CSUD3, NGRD3, NGRD3, DMVF3"
    
    # Clean and deduplicate tickers
    tickers = [t.strip() for t in raw_tickers.split(',')]
    tickers = sorted(list(set(tickers))) # Deduplicate and sort
    
    print(f"Ranking {len(tickers)} stocks...")
    ranked_stocks = calculate_rankings(tickers)
    
    print("\nStock Rankings (Weighted Returns) - Top 50:")
    # Print top 50 to avoid spamming the console too much, but user asked for the list.
    # I'll print all of them if it's not insane, but 200+ lines might be much.
    # Let's print all but maybe formatted or just the top ones?
    # The user said "rankeie as ações" (rank the stocks), usually implies seeing the list.
    # I will print all of them.
    print(ranked_stocks.to_string(formatters={
        'Score': '{:,.2%}'.format,
        'R_63d': '{:,.2%}'.format,
        'R_126d': '{:,.2%}'.format,
        'R_189d': '{:,.2%}'.format,
        'R_252d': '{:,.2%}'.format
    }))

if __name__ == "__main__":
    main()
