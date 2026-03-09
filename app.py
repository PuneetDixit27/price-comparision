from serpapi import GoogleSearch
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import urllib.parse


def compare(med_name):
    params = {
        "engine": "google_shopping",
        "q": med_name,
        "api_key": "7039a5688ea4a116e749970ac8a8e8fd4f9a20a0d4997b0c2c27ffdb681be07e",
        "gl": "in"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results.get("shopping_results", [])
    return shopping_results


# Header Section
c1, c2 = st.columns(2)
c1.image("e_pharmacy.png", width=200)
c2.header("E-pharmacy price comparison system by PUNEET DIXIT")

st.sidebar.title("Enter name of medicine:")
med_name = st.sidebar.text_input("Enter name here:")
number = st.sidebar.text_input("Enter number of options here:")
medcine_comp=[]
med_price=[]
if med_name and number:
    if st.sidebar.button("Price Compare"):

        shopping_results = compare(med_name)

        if len(shopping_results) == 0:
            st.error("No results found.")
        else:
            try:
                num_options = min(int(number), len(shopping_results))
            except:
                st.error("Please enter a valid number.")
                st.stop()

            # Initialize lowest price
            first_price_str = shopping_results[0].get('price', "₹0")
            lowest_price = float(first_price_str.replace("₹", "").replace(",", ""))
            lowest_price_index = 0

            # Display Options
            st.sidebar.image(shopping_results[0].get('thumbnail'))
            for i in range(num_options):

                price_str = shopping_results[i].get('price', "₹0")
                current_price = float(price_str.replace("₹", "").replace(",", ""))
                medcine_comp.append(shopping_results[i].get('source'))
                med_price.append(float(first_price_str.replace("₹", "").replace(",", "")))

                st.title(f"Option {i+1}")
                c1, c2 = st.columns(2)

                c1.write("Company :")
                c2.write(shopping_results[i].get('source', "N/A"))

                c1.write("Title :")
                c2.write(shopping_results[i].get('title', "N/A"))

                c1.write("Price :")
                c2.write(price_str)

                # Safe Google Search Link (Never Expired)
                title = shopping_results[i].get('title', '')
                search_query = urllib.parse.quote(title)
                url = f"https://www.google.com/search?q={search_query}"

                c1.write("Buy link :")
                c2.markdown(f"[Buy Here]({url})")

                # Check lowest price
                if current_price < lowest_price:
                    lowest_price = current_price
                    lowest_price_index = i

            # Best Option Section
            st.title("Best Option :")

            c1, c2 = st.columns(2)

            c1.write("Company :")
            c2.write(shopping_results[lowest_price_index].get('source', "N/A"))

            c1.write("Title :")
            c2.write(shopping_results[lowest_price_index].get('title', "N/A"))

            c1.write("Price :")
            c2.write(shopping_results[lowest_price_index].get('price', "N/A"))

            best_title = shopping_results[lowest_price_index].get('title', '')
            best_query = urllib.parse.quote(best_title)
            best_url = f"https://www.google.com/search?q={best_query}"

            c1.write("Buy link :")
            c2.markdown(f"[Buy Here]({best_url})")
            df = pd.DataFrame(medcine_comp,med_price)
            st.title("chart comparision :")
            st.bar_chart(df)
            fig,ax=plt.subplots()
            ax.pie(med_price,labels=medcine_comp,shadow=True)
            ax.axis("equal")
            st.pyplot(fig)