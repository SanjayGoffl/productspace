import logging
import json
import concurrent.futures

from wordcloud import WordCloud

from crawler import BeautifulSoupCrawler
from summarizer import Summarizer
from classifier import ContentClassifier
from llm import LLMModel
from utils import normalize_text, nltk_lan_mapper


AVG_WORD_LEN = 7 # chars
MAX_NUM_WORDS = 4000 # words
MAX_TXT_LENGTH = AVG_WORD_LEN * MAX_NUM_WORDS # chars


logger = logging.getLogger(__name__)


MULTI_COMPETITOR_PROMPT = """As an Expert Market Analyst, your objective is to analyze the market by comparing our product, {product_name}, against several key competitors based on their website data.

Our Product: {product_name}
Description & Features: {product_description}

Below is the scraped and summarized data for multiple competitors. 

Generate a comprehensive, highly readable Market Analysis Report. You must specifically focus on:
1. Feature Matrix: What features do we offer versus what the competitors offer?
2. Pricing Strategy: What is the pricing strategy of the competitors (if mentioned in the data)?
3. Market Gaps: What features or services are competitors offering that we are missing?
4. Unique Value Proposition: Where does {product_name} stand out among the crowd?

Present the report in clear Markdown formatting, utilizing tables and bullet points where appropriate for maximum readability. Start directly with the analysis without introductory filler."""


class CompetitorAnalyzer:
    def __init__(self, llm_model: LLMModel, product_name: str, product_desc: str) -> None:
        self.llm_model = llm_model
        self.product_name = product_name
        self.product_desc = product_desc

        self.sys_prompt = MULTI_COMPETITOR_PROMPT.format(product_name=product_name, product_description=product_desc)

        # In most pages at begining only some meta infromaiton are saved
        self.txt_offset = 150 # chars

        self.summarizer = Summarizer(self.llm_model)
        self.classifier = ContentClassifier(self.llm_model)
    
    def chat(self, content):
        response = self.llm_model.chat(content, sys_prompt=self.sys_prompt, 
                                       max_token=8000, temp=0.)

        res = response.choices[0].message.content
        # Remove the newline character and the end-of-text identifier
        res = res.strip().replace("<|eot_id|>", "")
        return res

    def analyze(self, base_folder, name: str, allowed_domains: list[str], 
            start_urls: list[str], languages: list[str], 
            max_pages: int = 5):
        
        logger.info(f"Running competitor analysis for '{name}'.")

        crawler_file = f'{base_folder}/content_{name}.json'
        wordcloud_file = f'{base_folder}/wordcloud_{name}.png'
        summary_file = f"{base_folder}/summaries_{name}.json"
        res_file = f"{base_folder}/res_competitor_analysis_{name}.txt"
        
        # Start crawling
        process = BeautifulSoupCrawler(
            name=name,
            allowed_domains=allowed_domains,
            start_urls=start_urls,
            languages=languages,
            out_file=crawler_file,
            max_pages=max_pages
        )
        process.start()
        
        # Load the extracted data from the JSON file
        with open(crawler_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        ### Building the word cloud ###############################

        # Concatenate all the orignial text contents into a single string
        org_contents = " ".join([item['text_content'] for item in data])

        # normalize the text
        langs = [nltk_lan_mapper[lan] for lan in languages]
        org_contents = normalize_text(org_contents, langs)
        # remove also the name of the company
        org_contents = org_contents.replace(name, "")

        # Generate and save the word cloud
        if org_contents.strip():
            logger.info("Generating word cloud.")
            try:
                wordcloud = WordCloud(width=800, height=800, background_color='white').generate(org_contents)
                wordcloud.to_file(wordcloud_file)
            except ValueError as e:
                logger.warning(f"Failed to generate word cloud for {name}: {e}")
        else:
            logger.warning(f"No text extracted for {name}; skipping word cloud generation.")

        ### Classifing the content and filtering ################

        def classify_item(item):
            try:
                txt = item['text_content'][self.txt_offset:]
                txt = f"url: {item['url']} \n\n {txt}"
                cls = self.classifier.classify(txt)
                if cls in self.classifier.exclude_types:
                    return None
                item['class'] = cls
                return item
            except Exception as e:
                logger.warning(f"Classification failed for {item.get('url')}: {e}")
                return None

        filtered_data = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for res in executor.map(classify_item, data):
                if res is not None:
                    filtered_data.append(res)


        ### Summarizing #########################################

        # Summarize the content of each page seperatly
        def summarize_item(item):
            try:
                txt = item['text_content'][self.txt_offset:]
                item['summary'] = self.summarizer.summarize(txt)
            except Exception as e:
                logger.warning(f"Summarization failed for {item.get('url')}: {e}")
                item['summary'] = ""
            return item

        summaries = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for res in executor.map(summarize_item, filtered_data):
                if res.get('summary'):
                    summaries.append(res)

        # Concatenate all the text content into a single string
        content = " .".join([item['summary'] for item in summaries])
        
        content = content[:min(len(content), MAX_TXT_LENGTH)]

        # Summarize the entire company text
        summary = self.summarizer.summarize(content=content)
        summaries.append({"total_summary": summary})

        # Save the extracted data to a JSON file
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, ensure_ascii=False, indent=4)

        logger.info(f"Data extraction and summarization for {name} completed.")
        return wordcloud_file, summary_file, crawler_file, summary

    def generate_global_analysis(self, base_folder, all_competitor_summaries):
        logger.info("Generating global market analysis...")
        res_file = f"{base_folder}/global_market_analysis.txt"
        
        # Build the final prompt content
        combined_content = "### COMPETITOR DATA ###\n\n"
        for comp_name, comp_summary in all_competitor_summaries.items():
            combined_content += f"--- {comp_name.upper()} ---\n{comp_summary}\n\n"
            
        res = self.chat(combined_content)
        
        with open(res_file, 'w', encoding='utf-8') as f:
            f.write(res)
            
        logger.info("Global market analysis completed.")
        return res_file

