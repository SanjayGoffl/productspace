import os
import shutil
import yaml
import json

import streamlit as st
from streamlit_option_menu import option_menu

from analyzer import CompetitorAnalyzer
from llm import LLMModel


DEFAULT_ROOT_FOLDER = "results"
LOGO_PATH = "logo.png"


def main():
    st.set_page_config(page_title="Comperator - Outsmart Your Competitors", layout="wide")
    
    # Set color scheme
    primary_color = "#2a7fff"  # Blue
    secondary_color = "#1fd160"  # Green
    
    # Add logo to the sidebar
    if os.path.exists(LOGO_PATH):
        with st.sidebar:
            st.image(LOGO_PATH, use_column_width=True)
    else:
        st.warning("Logo image not found.")
    
    # Sidebar
    with st.sidebar:
        selected_page = option_menu(
            menu_title=None,
            options=["Home", "Settings", "Competitors", "Analysis"],
            icons=["house", "gear", "people", "graph-up"],
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#f5f5f5"},
                "icon": {"color": primary_color, "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": primary_color},
            }
        )
    
    if selected_page == "Home":
        home_page(primary_color, secondary_color)
    elif selected_page == "Competitors":
        competitors_page(primary_color, secondary_color)
    elif selected_page == "Analysis":
        analysis_page(primary_color, secondary_color)
    elif selected_page == "Settings":
        settings_page(primary_color, secondary_color)


def home_page(primary_color, secondary_color):
    st.title("Welcome to Comperator")
    st.write("Analyze your competitors and gain valuable insights to stay ahead in your market.")

    st.divider()

    st.header("My Product", anchor="my-product")
    
    # Load existing product information
    product_info = load_product_info()
    
    # Display current product information
    if product_info:
        st.subheader("Current Product Information")
        st.info(f"**Name:** {product_info['name']}\n\n**Description:** {product_info['description']}\n\n**Key Features:** {product_info.get('key_features', 'N/A')}")
    
    # Input fields for product name and description
    st.subheader("Update Product Information")
    with st.form(key="product_info_form"):
        product_name = st.text_input("Product Name", value=product_info['name'] if product_info else "")
        product_description = st.text_area("Product Description", value=product_info['description'] if product_info else "")
        product_features = st.text_area("Key Features", value=product_info.get('key_features', '') if product_info else "")
        submit_button = st.form_submit_button(label="Save Product Information")
    
    if submit_button:
        product_info = {
            "name": product_name,
            "description": product_description,
            "key_features": product_features
        }
        save_product_info(product_info)
        st.success("Product information saved successfully!")
        
        # Trigger a rerun of the app to refresh the page content
        st.rerun()

    st.divider()
    st.subheader("Automated Competitor Discovery")
    st.write("Let our AI automatically discover 5 top competitors based on your product details.")
    find_competitors = st.button("🔍 Find Competitors Automatically")

    if find_competitors and product_info:
        config = load_config()
        # Init LLM with Gemini key and model
        llm_model = LLMModel(
            api_key=config.get("gemini", {}).get("api_key", ""), 
            model_name=config.get("llm", {}).get("model_name", "models/gemini-2.5-flash")
        )

        prompt = f"""Based on the following product, identify 5 top direct competitors. 
Product Name: {product_info['name']}
Description: {product_info['description']}
Key Features: {product_info.get('key_features', '')}

For each competitor, provide:
1. The competitor's name.
2. The main domain of their website (e.g., 'competitor.com').
3. The best starting URL for scraping their product features (e.g., 'https://www.competitor.com/').

Return the result ONLY as a valid JSON array of objects, with each object having the keys: "name", "allowed_domains" (list of strings), and "start_urls" (list of strings). Do not include any HTML or markdown formatting outside the JSON array. Example:
[
  {{"name": "CompetitorA", "allowed_domains": ["competitora.com"], "start_urls": ["https://competitora.com/features"]}}
]
"""
        with st.spinner("Searching the web and analyzing market for competitors..."):
            response = llm_model.chat(prompt, max_token=2000, temp=0.5)
            res_content = response.choices[0].message.content if response else ""
            res_content = res_content.replace("```json", "").replace("```", "").strip()
            
            try:
                found_competitors = json.loads(res_content)
                existing_competitors = load_competitors()
                existing_names = {c["name"].lower() for c in existing_competitors}
                
                added_count = 0
                for comp in found_competitors:
                    name = comp.get("name")
                    if name and name.lower() not in existing_names:
                        clean_comp = {
                            "name": name,
                            "allowed_domains": comp.get("allowed_domains", []),
                            "start_urls": comp.get("start_urls", comp.get("start,urls", []))
                        }
                        existing_competitors.append(clean_comp)
                        existing_names.add(name.lower())
                        added_count += 1
                
                if added_count > 0:
                    save_competitors(existing_competitors)
                    st.success(f"Successfully found and added {added_count} new competitors! Check the 'Competitors' tab.")
                else:
                    st.info("Found competitors that were already in your list.")
            except Exception as e:
                st.error("Failed to parse competitors. The LLM might have returned an invalid format. Please try again.")


def competitors_page(primary_color, secondary_color):
    st.title("Competitors")
    
    # Load competitors
    competitors = load_competitors()
    
    # Display competitors in a visually appealing structure
    if competitors:
        st.subheader("Competitor List")
        
        # Create a container for the competitors
        with st.container():
            selected_competitors = []
            
            # Display each competitor in an expander
            for index, competitor in enumerate(competitors):
                with st.expander(competitor["name"], expanded=False):
                    col1, col2 = st.columns(2)
                    
                    # Display competitor details in the first column
                    with col1:
                        st.markdown(f"**Allowed Domains:**\n{', '.join(competitor.get('allowed_domains', []))}")
                        st.markdown(f"**Start URLs:**\n{', '.join(competitor.get('start_urls', []))}")
                    
                    # Display the checkbox in the second column
                    with col2:
                        selected = st.checkbox("Select for removal", key=f"checkbox_{index}")
                        if selected:
                            selected_competitors.append(competitor)
            
            # Remove selected competitors
            if selected_competitors:
                remove_button = st.button("Remove Selected", key="remove_selected")
                if remove_button:
                    for competitor in selected_competitors:
                        competitors.remove(competitor)
                    save_competitors(competitors)
                    st.success(f"{len(selected_competitors)} competitor(s) removed successfully!")
                    st.rerun()
    else:
        st.info("No competitors found. Add a competitor using the form below.")
    
    # Add a new competitor
    st.subheader("Add Competitor")
    with st.form(key="add_competitor_form"):
        name = st.text_input("Name")
        domains = st.text_input("Allowed Domains (comma-separated)")
        urls = st.text_input("Start URLs (comma-separated)")
        submit_button = st.form_submit_button("Add Competitor")
    
    if submit_button:
        competitor = {
            "name": name,
            "allowed_domains": domains.split(","),
            "start_urls": urls.split(",")
        }
        competitors.append(competitor)
        save_competitors(competitors)
        st.success(f"Competitor '{name}' added successfully!")
        st.rerun()


def analysis_page(primary_color, secondary_color):
    st.title("Market Analysis")
    st.write("Analyze your product against all competitors simultaneously to discover feature gaps and pricing strategies.")
    
    competitors = load_competitors()
    
    if not competitors:
        st.info("No competitors found. Go to the Home or Competitors tab to add some.")
        return

    product_info = load_product_info()
    product_name = product_info['name']
    product_desc = product_info['description']
    product_features = product_info.get('key_features', '')

    config = load_config()
    languages = config.get("settings", {}).get("languages", ["en"])
    max_pages = config.get("settings", {}).get("max_pages", 10)
    
    # Init LLM with Gemini key and model
    llm_model = LLMModel(
        api_key=config.get("gemini", {}).get("api_key", ""), 
        model_name=config.get("llm", {}).get("model_name", "models/gemini-2.5-flash")
    )
    
    st.write(f"**Ready to run a global market analysis against {len(competitors)} competitors.**")
    start_button = st.button("🚀 Start Global Market Analysis", key="start_analysis")
    
    if start_button:
        analyzer = CompetitorAnalyzer(
            llm_model=llm_model, 
            product_name=product_name, 
            product_desc=f"{product_desc}\nKey Features: {product_features}"
        )
        
        base_folder = f"{DEFAULT_ROOT_FOLDER}/global_analysis"
        shutil.rmtree(base_folder, ignore_errors=True)
        os.makedirs(base_folder, exist_ok=True)

        all_summaries = {}
        wordcloud_paths = {}
        
        progress_text = st.empty()
        progress_bar = st.progress(0)

        # 1. Loop through all competitors
        for i, competitor in enumerate(competitors):
            compat_name = competitor["name"]
            allowed_domains = competitor.get("allowed_domains", [])
            start_urls = competitor.get("start_urls", [])

            progress_text.text(f"Analyzing competitor {i+1}/{len(competitors)}: {compat_name}...")
            
            comp_folder = f"{base_folder}/{compat_name}"
            os.makedirs(comp_folder, exist_ok=True)

            wordcloud_file, summary_file, crawler_file, summary = analyzer.analyze(
                base_folder=comp_folder, 
                name=compat_name, 
                allowed_domains=allowed_domains, 
                start_urls=start_urls, 
                languages=languages, 
                max_pages=max_pages
            )

            all_summaries[compat_name] = summary
            wordcloud_paths[compat_name] = wordcloud_file
            
            progress_bar.progress((i + 1) / len(competitors))

        # 2. Generate Global Analysis
        progress_text.text("Generating the final Global Market Report...")
        res_file = analyzer.generate_global_analysis(base_folder, all_summaries)
        
        progress_bar.empty()
        progress_text.empty()
        
        # 3. Display the Global Report
        st.subheader("🌍 Global Market Analysis Report")
        if os.path.exists(res_file):
            with open(res_file, "r", encoding="utf-8") as f:
                analysis_text = f.read()
            st.markdown(analysis_text)
        else:
            st.error("Failed to generate global analysis report.")
            
        st.divider()
        
        # 4. Display Individual Breakdown (Wordclouds)
        st.subheader("🔍 Individual Competitor Breakdowns")
        cols = st.columns(min(3, len(competitors)))
        
        for idx, (comp_name, path) in enumerate(wordcloud_paths.items()):
            col = cols[idx % len(cols)]
            with col:
                with st.expander(f"{comp_name} Word Cloud"):
                    if os.path.exists(path):
                        st.image(path, use_column_width=True)
                    else:
                        st.info("No content found or word cloud generation failed.")


def settings_page(primary_color, secondary_color):
    st.title("Settings")
    
    # Load existing settings
    config = load_config()
    
    # Settings
    st.subheader("Gemini API Settings")
    api_key = st.text_input("API Key", type="password", value=config.get("gemini", {}).get("api_key", ""))
    
    # LLM settings
    st.subheader("LLM Settings")
    llm_model = st.text_input("LLM Model Name", value=config.get("llm", {}).get("model_name", "models/gemini-2.5-flash"))
    
    # Other settings
    st.subheader("Other Settings")
    max_pages = st.number_input("Max Pages to Analyze", value=config.get("settings", {}).get("max_pages", 10), min_value=1)
    languages = st.text_input("Languages (comma-separated)", value=",".join(config.get("settings", {}).get("languages", ["en"])))
    
    save_button = st.button("Save Settings", key="save_settings")
    
    if save_button:
        settings = {
            "gemini": {
                "api_key": api_key
            },
            "llm": {
                "model_name": llm_model
            },
            "settings": {
                "max_pages": max_pages,
                "languages": languages.replace(" ", "").split(","),
            }
        }
        save_config(settings)
        st.success("Settings saved successfully!")


def load_config():
    try:
        with open(f"{DEFAULT_ROOT_FOLDER}/config.yaml", "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        config = {
            "gemini": {
                "api_key": ""
            },
            "llm": {
                "model_name": "models/gemini-2.5-flash"
            },
            "settings": {
                "max_pages": 10,
                "languages": ["en"],
            }
        }
        save_config(config)
    return config

def save_config(config):
    with open(f"{DEFAULT_ROOT_FOLDER}/config.yaml", "w") as f:
        yaml.dump(config, f)

def load_competitors():
    try:
        with open(f"{DEFAULT_ROOT_FOLDER}/competitors.json", "r") as f:
            competitors = json.load(f)
    except FileNotFoundError:
        competitors = []
    return competitors

def save_competitors(competitors):
    with open(f"{DEFAULT_ROOT_FOLDER}/competitors.json", "w") as f:
        json.dump(competitors, f)

def load_product_info():
    try:
        with open(f"{DEFAULT_ROOT_FOLDER}/product_info.json", "r") as f:
            product_info = json.load(f)
    except FileNotFoundError:
        product_info = {"name": "BestApp", "description": "Best AI BI tool.", "key_features": "Fast, Reliable, AI-powered."}
        save_product_info(product_info)
    return product_info

def save_product_info(product_info):
    with open(f"{DEFAULT_ROOT_FOLDER}/product_info.json", "w") as f:
        json.dump(product_info, f)

if __name__ == "__main__":

    # Create the "DEFAULT_ROOT_FOLDER" folder if it doesn't exist
    if not os.path.exists(DEFAULT_ROOT_FOLDER):
        os.makedirs(DEFAULT_ROOT_FOLDER, exist_ok=True)
    main()