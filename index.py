from google import genai
import streamlit as st
import yfinance as yf

client = genai.Client(api_key='AIzaSyC20Qu0Sb6uo7ApieMVtJlwhS45VBymRnE')

st.title("Financial Advice Chatbot with Gemini")
tickers=st.text_input("enter your ticker symbols (comma-separated)",placeholder="e.g., AAPL, TSLA, MSFT")
goals=st.text_area("what are your financial goals ",placeholder="e.g., I want long-term growth with moderate risk")
run_button=st.button("Get Investment Recommendation")
if tickers and goals and run_button:
    with st.spinner("analyzing"):
        group = yf.Tickers(tickers.split(", "))
        group_data = group.history(period = "5d")
        group_data_close = group_data["Close"]
        dict_all_tickers = {
        }
        column_names = group_data_close.columns
        for i,row in group_data_close.iterrows():
            for column in column_names: 
                val = dict_all_tickers.get(column,None)
                if val:
                    val.append(float(row[column]))
                    dict_all_tickers[column] = val
                else:
                    dict_all_tickers[column] = [float(row[column])]
        prompt = (
            f"Given the following stock ticker symbols: {tickers}\n"
            f"And the user's financial goals: {goals}\n"
            f"Along with the past 5 days of ticker close prices: {str(dict_all_tickers)}\n"
            "What investment advice would you give? Be specific and concise, include numbers from the 5d close prices or percentages/ratios."
        )       
        response = client.models.generate_content( 
            model='gemini-2.0-flash', contents=prompt
        )
        st.write(response.text)
else:
    st.info("Please enter both ticker symbols and your goals to get a recommendation.")