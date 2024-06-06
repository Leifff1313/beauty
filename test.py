import os
os.environ["OPENAI_API_KEY"] = ""
os.environ["SERPAPI_API_KEY"] = ""
#memory
from langchain.memory import ConversationBufferMemory

MEMORY_KEY = "chat_history"
memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)

#prompt
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.prompts import MessagesPlaceholder

systemMessage = SystemMessage(content="""You are a search consistent, who can do detailed research on ant topic and produce facts. 
                                         You will try as hard as possible to gather facts and data to back up the research.   
                            Please make sure you complete the objective above with the following rules:
                            1/ You should  do enough research to gather as much information as possible about the objective
                            2/ If there are url of relevent links and articles, you will scrape it to gather more information
                            3/ After scraping and searching, you should think "is there any new things i should search and scrape
                            4/ You should not make things up, you should write facts and data that you have gathered
                            5/ In the final output, you should include all reference data and links to back up your research 
                            6/ You can connect with Google Hotel api to fetch informations about hotel when user input query about hotel or something about stay for a night.
                              
                            if invoke search_hotel function, give me these information : Hotel search: Use keywords, location or other criteria to search for hotels to find hotel information that meets the criteria.

                            Hotel details: Get detailed information about the hotel, including address, contact information, facilities, room types, prices, etc.

                            Booking function: Integrated hotel booking function, users can book hotel rooms directly through the application.

                            Reviews and ratings: Browse other users reviews and ratings of hotels to help users make choices.

                            Picture display: Display pictures of the hotel to allow users to understand the appearance and facilities of the hotel more intuitively.

                            Map display: Mark the location of the hotel on the map to facilitate users to check the geographical location and surrounding environment.
                            
                            if invoke search_local function, give me these information : Location search: Use keywords or types to search for locations to find specific location information such as nearby businesses, attractions, restaurants, etc.

                             Reviews and ratings: You can check user reviews and ratings of a specific place to help users understand the quality and services of the place.

                             Opening hours: You can check the opening hours of a business, letting users know when they can visit a specific location.

                             Location details: Provide detailed information about the location, including address, contact information, photos, and more.

                             Map display: Combined with Google Maps, search results can be displayed on the map to facilitate users to check their geographical location. 
                              """)
prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=systemMessage,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)]
)
def search(q):
    from serpapi import GoogleSearch

    params = {
  "engine": "google",
   "gl": "tw",
  "hl": "zh-tw",
  "q":q,
  "api_key": ""
    }


    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]

def search_hotel(q):
    from serpapi import GoogleSearch

    params = {
  "engine": "google_hotels",
  "q":q,
  "check_in_date": "2024-06-06",
  "check_out_date": "2024-06-07",
  "adults": "2",
  "currency": "TWD",
  "gl": "tw",
  "hl": "zh-tw",
  "api_key": "",
  "sort_by":"8"
    }
    #有eco_certified這個參數，Parameter defines to show results that are eco certified.

    search = GoogleSearch(params)
    results = search.get_dict()

def search_local(q):
    from serpapi import GoogleSearch

    params = {
  "engine": "google_local",
  "q": q,
  "location": "Taiwan",
  "api_key": "",
  "gl": "tw",
  "hl": "zh-tw"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    local_results = results["local_results"]



from langchain.agents import Tool
tools = [
    Tool(
        name = 'search',
        func = search,
        description = '''useful for when you need to answer questions about current events. You should ask targeted questions. 
        For search engine related functions and data. Using the Google Search API, developers can easily integrate search engine functionality and data into their own applications'''
    ),
    Tool(
        name='search_hotel',
        func = search_hotel,
        description = '''useful for when you need to answer questions about hotel information. 
        
        To find the correct data.Hotel search: Use keywords, location or other criteria to search for hotels to find hotel information that meets the criteria.

        Hotel details: Get detailed information about the hotel, including address, contact information, facilities, room types, prices, etc.

        Booking function: Integrated hotel booking function, users can book hotel rooms directly through the application.

        Reviews and ratings: Browse other users reviews and ratings of hotels to help users make choices.

        Picture display: Display pictures of the hotel to allow users to understand the appearance and facilities of the hotel more intuitively.

        Map display: Mark the location of the hotel on the map to facilitate users to check the geographical location and surrounding environment.'''
    ),
    Tool(
        name = 'search_local',
        func = search_local,
        description = '''useful for when you need to answer questions about Location search: Use keywords or types to search for locations to find specific location information such as nearby businesses, attractions, restaurants, etc.

        Reviews and ratings: You can check user reviews and ratings of a specific place to help users understand the quality and services of the place.

        Opening hours: You can check the opening hours of a business, letting users know when they can visit a specific location.

        Location details: Provide detailed information about the location, including address, contact information, photos, and more.

        Map display: Combined with Google Maps, search results can be displayed on the map to facilitate users to check their geographical location.    '''
    )
]

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI()

#agent
from langchain.agents import AgentExecutor

search_agent = OpenAIFunctionsAgent(llm = llm, tools = tools, prompt = prompt, memory = memory)

#agent executor
agentExecutor = AgentExecutor(agent=search_agent, tools=tools, memory=memory, verbose = True)

query = input("What do you want to ask?")

agentExecutor(query)