from dotenv import load_dotenv
load_dotenv()

from crewai import LLM, Agent, Crew, Process, Task
from crewai_tools import FirecrawlScrapeWebsiteTool

# Initialize LLM
llm = LLM(
    model="gemini/gemini-2.5-flash", 
    temperature=0.7
)

# Initialize tools 
tool = [FirecrawlScrapeWebsiteTool()]

# Create agents
blog_scraper = Agent(
    name = "Blog Scraper", 
    role = "Web Content Researcher",           # Web Scraper
    goal = "Extract complete and accurate information from Blog URLs", 
    backstory = "You are an expert web researcher specialized in extracting main content from blogs while filtering out ads and navigation elements.", 
    verbose = True, 
    allow_delegation = False, 
    llm = llm, 
    tools = tool
)

blog_summarizer = Agent(
    name = "Blog Summarizer", 
    role = "Content Analyst",                  # Blog summarizer
    goal = "Create concise, informative summaries capturing key points from blog content", 
    backstory = "You are a skilled content analyst with expertise in distilling information into clear summaries", 
    verbose = True, 
    allow_delegation = False, 
    llm = llm 
)

# Define tasks 

def scrape_blog_task(url):
    return Task(
        description=f"Scrape content from the blog at {url} using FirecrawlScrapeWebsiteTool. Extract main article text, filtering out navigation and ads. Always use FirecrawlScrapeWebsiteTool",
        expected_output="Full text content of the blog post in markdown format.", 
        agent = blog_scraper
    )
    
def summarize_blog_task(scrape_task): 
    return Task(
        description = "Create comprehensive summary of scraped blog content for generating AI podcast episode",
        expected_output = """
        Concise summary with keypoints, insights and important details.
        The summary will be used to generate an AI podcast episode using a text to speech model.
        Create summary suitable for podcast format, focusing on clarity and engagement.
        Do not include that this is a blog summary or mention any links or URLs.""", 
        agent = blog_summarizer, 
        context = [scrape_task]        # Pass the Task Object, not String
    )

def create_blog_summary_crew(url):
    scrape_task = scrape_blog_task(url)
    summarize_task = summarize_blog_task(scrape_task)
    
    crew = Crew(
        agents = [blog_scraper, blog_summarizer], 
        tasks = [scrape_task, summarize_task], 
        verbose = True, 
        process = Process.sequential
    )
    
    return crew

def run_blog_summary_crew(url):
    crew = create_blog_summary_crew(url)
    result = crew.kickoff()
    
    return result.raw

if __name__ == "__main__":
    url = "https://ai.meta.com/blog/llama-helps-efficiency-anz-bank/"
    summary = run_blog_summary_crew(url)
    print(summary)