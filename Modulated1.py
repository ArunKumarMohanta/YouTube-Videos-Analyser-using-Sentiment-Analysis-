import googleapiclient.discovery
import googleapiclient.errors
import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import textwrap
import re
import time

# Constants
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
DEVELOPER_KEY = "Your_Developer_API_Key Here" #Generate API Key and Put at DEVELOPER_KEY variable
m=""

class YouTubeAnalyzer:
    def __init__(self, api_key=DEVELOPER_KEY):
        self.youtube = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, developerKey=api_key)
        self.vid = None
        self.response_c = None
        self.response_v = None

    def extract_video_id(self, url):
        if "youtu.be/" in url:
            return url.split("youtu.be/")[1][:11]
        if "youtube.com/watch?v=" in url:
            return url.split("v=")[1][:11]
        if "youtube.com/shorts/" in url:
            return url.split("shorts/")[1][:11]
        if "&" in url:
            return url.split("v=")[1].split("&")[0]
        print("Invalid video link")
        return None
        

    def get_creators(self):
        request = self.youtube.videos().list(
            part="snippet",
            id=self.vid
        )
        self.response_c = request.execute()
        return self.response_c

    def get_title(self):
        return self.response_c['items'][0]['snippet']['title']

    def get_viewers(self, max_comments=1000):
        comments = []
        
        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=self.vid,
            maxResults=100
        )

        while request and len(comments) < max_comments:
            response = request.execute()
            items = response.get('items', [])
        
            
            comments.extend(items)
        
           
            if len(items) < 100:
                break
        
           
        request = self.youtube.commentThreads().list_next(request, response)

       
        self.response_v = { 'items': comments[:max_comments] }
        return self.response_v


    def save_viewers_comments(self, filename='read.txt'):
        
        with open(filename, 'w', encoding='utf-8') as f:
            for item in self.response_v['items']:
                text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                f.write(text + '\n')

       
        global m
        m = "✅ Comments, "      

    def save_creators_data(self, filename='read1.txt'):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Title:\n")
            f.write(self.response_c['items'][0]['snippet']['title'] + '\n')
            f.close()
        
        global m
        m=m+'Title, '
        with open(filename, 'a', encoding='utf-8') as f:
            f.write("\nTags:\n")
            l = self.response_c['items'][0]['snippet'].get('tags', [])
            for tags in l:
                f.write(tags + '\n')
            f.close()
       
        m=m+'Tags, '
        with open(filename, 'a', encoding='utf-8') as f:
            f.write("\nDescription:\n")
            for item in self.response_c['items']:
                f.write(item['snippet']['description'] + '\n')
            f.close()
       
        m=m+'Description '

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.vid)
        
            english_transcript = None
            other_transcript = None
            for transcript in transcript_list:
                if transcript.language_code in ['en', 'en-US', 'en-GB']:
                    english_transcript = transcript
                    break
                else:
                    other_transcript = transcript
        
            transcript_to_use = english_transcript if english_transcript else other_transcript
        
            transcript_fetched = False  
            if transcript_to_use:
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        print(f"Attempt {attempt + 1}: Fetching subtitles in {transcript_to_use.language} ({transcript_to_use.language_code})...")
                        transcript_data = transcript_to_use.fetch()
        
                        if not transcript_data:
                            print("Warning: Transcript data is empty.")
                            if attempt < max_retries - 1:
                                time.sleep(2)
                                continue
                            else:
                                raise Exception("Transcript data is empty after all retries.")
        
                        
                        with open("transcript.txt", 'w', encoding='utf-8') as f:
                            f.write(f"\nFetching subtitles in {transcript_to_use.language} ({transcript_to_use.language_code})...\n")
                            for entry in transcript_data:
                                if isinstance(entry, dict):
                                    text = entry.get('text', '')
                                else:
                                    text = getattr(entry, 'text', '')
                                f.write(f"{text}\n")
        
                        m += f"and Subtitles ({transcript_to_use.language}) fetched"
                        transcript_fetched = True 
                        break
        
                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed with error: {e}")
                        if attempt < max_retries - 1:
                            time.sleep(2)
                        else:
                            raise
            else:
                print("No available subtitles for this video.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
       
        if transcript_fetched:
            with open('transcript.txt', 'r', encoding='utf-8') as source_file:
                content = source_file.read()
            with open(filename, 'a', encoding='utf-8') as destination_file:
                destination_file.write(content)
        else:
            print("Transcript not fetched, skipping append.")
        
        return m        
        
    

    def ai_analysis(self, api_key="Your_Gemini_API_Key_Here", max_chunk_size=10000): #Generate And put your Gemini API Key at api_key variable
        transcript_filename="transcript.txt"

       
        genai.configure(api_key=api_key)

        
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

       
        with open(transcript_filename, "r", encoding="utf-8") as file:
            file_content = file.read()

        
        chunks = textwrap.wrap(file_content, max_chunk_size)

        
        summaries = []
        for i, chunk in enumerate(chunks):
            prompt = f"Please provide an overall summary of the following Youtube video's transcript in Very short sentences, but more number of sentences, in very much detailed explanation :\n\n{chunk}"
            response = model.generate_content(prompt)
            summaries.append(response.text)

        
        combined_summary = "\n".join(summaries)
        final_prompt = f"Please provide an overall summary of the following Youtube video's transcript in Very short sentences, but more number of sentences, in very much detailed explanation :\n\n{combined_summary}"
        final_response = model.generate_content(final_prompt)

       
        summary_filename = "summary.txt"
        sentences = re.split(r'(?<=[.!?]) +', final_response.text.strip())


       
        with open(summary_filename, 'w', encoding='utf-8') as f:
            for sentence in sentences:
                f.write(sentence.strip() + '\n')

    def ai_factcheck(self, api_key="Your_Gemini_API_Key_Here", max_chunk_size=10000): #Generate And put your Gemini API Key at api_key variable
        transcript_filename="transcript.txt"

       
        genai.configure(api_key=api_key)

       
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

        
        with open(transcript_filename, "r", encoding="utf-8") as file:
            file_content = file.read()

        
        chunks = textwrap.wrap(file_content, max_chunk_size)

        
        summaries = []
        for i, chunk in enumerate(chunks):
            prompt = f"Identify various facts in the following transcript of the Youtube video, by giving number, fact check all the facts and their credibility. Put separate line for each fact. The output text must be cleaned. The output should be of this format only:\n1.\nFact: \nCredibility: \nFact Check: . :\n\n{chunk}"
            response = model.generate_content(prompt)
            summaries.append(response.text)

        
        combined_summary = "\n".join(summaries)
        final_prompt = f"Identify various facts in the following transcript of the Youtube video, by giving number, fact check all the facts and their credibility. Put separate line for each fact. The output text must be cleaned. The output should be of this format only:\n1.\nFact: \nCredibility: \nFact Check: .  :\n\n{combined_summary}"
        final_response = model.generate_content(final_prompt)

       
        factcheck_filename = "factcheck.txt"
        sentences = re.split(r'(?<=[.!?]) +', final_response.text.strip())


        
        with open(factcheck_filename, 'w', encoding='utf-8') as f:
            for sentence in sentences:
                f.write(sentence.strip() + '\n')
    

class SentimentAnalyzer:
    def __init__(self, video_title=None):
        self.video_title = video_title
    def cleaning_text(self, rt_text):
        text = open(rt_text, encoding='utf-8').read()
        lower_case = text.lower()
        cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
        return cleaned_text
      

    def emotions_from_emotions_txt(self, rt_text):
        cleaned_text = self.cleaning_text(rt_text)
        tokenized_words = word_tokenize(cleaned_text, "english")
      
        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words('english'):
                final_words.append(word)
        
        lemma_words = []
        for word in final_words:
            word = WordNetLemmatizer().lemmatize(word)
            lemma_words.append(word)
        emotion_list = []
        with open('emotion.txt', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')
                if word in lemma_words:
                    emotion_list.append(emotion)
            file.close()
        
        w = Counter(emotion_list)
        
        return w
        

    def polarity_score(self, app_text):
        sentiment_text = self.cleaning_text(app_text)
        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
        return score
       

    def convert_scores_to_percent(self,scores):
        
        percent_scores = {}

       
        for key in ['neg', 'neu', 'pos']:
            percent_scores[key] = round(scores[key] * 100, 2) 


        
        compound_score = scores['compound']
        if compound_score < 0:
            percent_scores['compound'] = 0.0  
        else:
            percent_scores['compound'] = round(((compound_score + 1) / 2) * 100, 2) 
        return percent_scores

    def sentiment_analyse(self,app_text):
        score=self.polarity_score(app_text)
        if score['neg'] > score['pos']:
            return "Negative Sentiment"
        elif score['neg'] < score['pos']:
            return "Positive Sentiment"
        else:
            return "Neutral Sentiment"

    def graph_plot(self, file_path, label, whose):
        emotions = self.emotions_from_emotions_txt(file_path)
        if whose == "Viewers'":
            global viw
            viw = emotions
        else:
            global cre
            cre = emotions

        
        total_count = sum(emotions.values())
        percentages = {k: (v / total_count) * 100 for k, v in emotions.items()}

        
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')  
        ax.set_facecolor('black')

       
        bars = ax.bar(percentages.keys(), percentages.values(), color='#00FF00')

        
        ax.set_ylim(0, max(percentages.values()) * 1.2)  

        
        ax.spines['left'].set_color('white')  
        ax.spines['bottom'].set_color('white')  
        ax.spines['top'].set_color('white')  
        ax.spines['right'].set_color('white')  
        
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)

        ax.tick_params(axis='x', colors='#00FF00')  
        ax.tick_params(axis='y', colors='#00FF00')  
        ax.xaxis.label.set_color('#00FF00')  
        ax.yaxis.label.set_color('#00FF00')  

        
        for idx, bar in enumerate(bars):
            height = bar.get_height()

            
            offset = 8 if idx % 2 == 0 else 15

            ax.annotate(f"{round(height, 1)}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height),  
                        xytext=(0, offset),  
                        textcoords="offset points",
                        ha='center', va='bottom', color='#00FF00', fontsize=7)

        
        ax.text(-0.145, 1.12, self.video_title, transform=ax.transAxes, fontsize=9.0,
                bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'), color='#00FF00')
        ax.set_title("\n" + whose + " Emotions", color='white')

       
        plt.subplots_adjust(top=0.85, bottom=0.2)

        fig.autofmt_xdate()  

       
        ax.text(0.5, -0.25, "Overall Sentiment[NLTK]: " + label,
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'),
                color='#00FF00')

       
        plt.savefig('graph_' + whose.lower() + '.png', bbox_inches='tight')
        

def combine_files(file1, file2, output_file):
    text = ''
    with open(output_file, 'w', encoding='utf-8') as f:
        with open(file1, 'r', encoding='utf-8') as f1:
            text = f1.read()
            f1.close()
        with open(file2, 'r', encoding='utf-8') as f2:
            text = text + f2.read()
            f2.close()
        f.write(text)
        f.close()

def find_overall_tone(file_path):
    combo = SentimentAnalyzer().emotions_from_emotions_txt(file_path)
    max_count = max(combo.values())
    oelist = []
    for k, v in combo.items():
        if v == max_count:
            oelist.append(k)
    if len(oelist) == 1:
        oe = oelist[0].upper()
    else:
        oe = ",".join(oelist).upper()
    return oe


if __name__ == "__main__":
    url = input("Enter a valid Youtube video link: ")
    analyzer = YouTubeAnalyzer()
    analyzer.vid = analyzer.extract_video_id(url)
    analyzer.get_creators()
    analyzer.get_viewers()
    analyzer.save_viewers_comments()
    analyzer.save_creators_data()
    analyzer.ai_analysis()
    analyzer.ai_factcheck()
    

    video_title = analyzer.get_title()
    sentiment_analyzer = SentimentAnalyzer( video_title)
    viewers_sentiment_label = sentiment_analyzer.sentiment_analyse('read.txt')
    sentiment_analyzer.graph_plot('read.txt', viewers_sentiment_label, r"Viewers'")
    creators_sentiment_label = sentiment_analyzer.sentiment_analyse('read1.txt')
    sentiment_analyzer.graph_plot('read1.txt', creators_sentiment_label, r"Creator's")

    combine_files('read.txt', 'read1.txt', 'Combined.txt')
    oe = find_overall_tone('Combined.txt')
    print("THE OVERALL TONE OF THE VIDEO (COMBINED EMOTIONS OF BOTH VIEWERS' AND CREATOR's): ", oe)
    plt.show()