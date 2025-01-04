---

#  YouTube Emotion Analyzer

This project analyzes the sentiments and emotions of both content creators and viewers by examining various components of a YouTube video, such as comments, video title, description, tags, and transcript. It uses the YouTube Data API and Natural Language Toolkit (NLTK) to extract and process emotional and sentiment data. The analysis results are displayed with an intuitive GUI built using customtkinter, providing graphical visualizations for insights.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Dependencies](#dependencies)  
- [API Setup](#api-setup)  
- [Usage](#usage)  
- [Introductory Emotion & Sentiment Analysis Files](#introductory-emotion-and-sentiment-analysis-files)
  
   1.[Basic_Emotion_Analysis.py](#basic_emotion_analysis)
  
   2.[Emotion_and_Sentiment_Analysis.py](#emotion_and_sentiment_analysis)

- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Milestones](#milestones)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)



## Introduction

The YouTube Emotion Analyzer is a tool designed to extract and analyze emotions from YouTube video comments and creator data. This tool can help content creators, teachers, and organizations understand the emotional responses of their audience, thereby improving content quality and audience engagement.
  

## Features 

- **Extract Video ID**: Automatically parses the YouTube video URL to get the video ID.  
- **Viewers' Sentiment Analysis**: Analyzes top-level comments on the video and detects the viewers' sentiment using NLP.  
- **Creator's Content Analysis**: Analyzes the video title, description, tags, and transcripts (if available).  
- **Emotion Detection**: Identifies a wide range of emotions (joy, sadness, anger, etc.) from both the creator and the viewers using a predefined emotion list.  
- **Sentiment Classification**: Uses the NLTK `SentimentIntensityAnalyzer` to determine whether the content has a positive, neutral, or negative sentiment.  
- **Graphical Visualization**: Displays the emotions and sentiment data through custom bar graphs for both the **creator** and **viewers**.
- User-friendly GUI: Built with customtkinter for smooth interaction.
- File Handling: View combined analysis results from saved text files.
- Error Handling: Alerts for invalid inputs or API errors.

## Technologies Used

- Python: Core programming language

- YouTube Data API: For fetching video data and comments

- NLTK (Natural Language Toolkit): For sentiment and emotion analysis

- Tkinter / CustomTkinter: GUI framework for the desktop interface

- Matplotlib: For visualizing emotion graphs

- Pillow: For handling images in the GUI

## Installation  

1. **Clone the repository**:  
   git clone https://github.com/ArunKumarMohanta/sentiment_analysis.git
   
   cd sentiment_analysis

3. **Set up a virtual environment (optional)**:  
   python -m venv venv
   
   source venv/bin/activate  # On Linux/Mac
   
   .\venv\Scripts\activate   # On Windows

5. **Install dependencies**:  
   pip install -r requirements.txt  

6. **Download NLTK resources**:  
   Open a Python shell and run the following:
   
   import nltk
   
   nltk.download('vader_lexicon')
   
   nltk.download('punkt')
   
   nltk.download('wordnet')
   
   nltk.download('stopwords')
7. **Run the project:**
   
   MAIN_APP.py


## Dependencies  

- Python 3.x (I have used 3.10.8)
  
- google-api-python-client==2.55.0: Used to interact with the YouTube Data API.
  
- google-auth==2.6.0: Used for authentication with Google services.
  
- matplotlib==3.5.1: Used for plotting graphs.
  
- nltk==3.6.2: Used for natural language processing tasks, including tokenization, stop word removal, and sentiment analysis.
  
- customtkinter==4.0.0: Used to create a modern and customizable GUI.
  
- Pillow==8.3.2: Used for handling image files, particularly for the GUI buttons.
  
- youtube-transcript-api==0.5.0: Used to fetch video subtitles.
  

## API Setup  

1. Go to [Google Cloud Console](https://console.cloud.google.com/).  
2. Create a project and enable **YouTube Data API v3**.  
3. Generate an **API key**.  
4. In `MAIN_APP.py`, replace the `DEVELOPER_KEY` with your API key:
   
   DEVELOPER_KEY = "YOUR_API_KEY_HERE"
   

## Usage  

**Running the Application**

1. Run the GUI:
MAIN_APP.py

3. Enter the YouTube video URL in the input box.

4. Analyze the sentiments and view results with graphs in the GUI.

5. Open Combined Files: Use the buttons to view saved analysis text files (read.txt and read1.txt).

**Example of Emotion Analysis**

The results will display the overall tone (e.g., Happy, Sad, Positive) and corresponding graphs for both creators and viewers.


## Introductory Emotion and Sentiment Analysis Files


Here's a draft for the "Introductory Emotion & Sentiment Analysis Files" section:

**Introductory Emotion and Sentiment Analysis Files**
For users interested in understanding the foundational steps of this project, we've included two introductory files that demonstrate basic techniques in text processing, emotion analysis, and sentiment analysis. These files are excellent starting points for those looking to build from scratch.

## Basic_Emotion_Analysis

**Basic_Emotion_Analysis.py**

This file provides a simple, step-by-step approach to:

**Text cleaning**: Lowercasing, removing punctuation, and tokenizing words.
Stop word removal: Excluding common words that don't contribute meaning (e.g., "and," "the").
Emotion detection: Using the emotion.txt dataset to identify and count emotions expressed in the text.
Visualization: Creating a bar graph to visualize the frequency of each detected emotion.
It is a good entry point to understand how to clean and analyze text data for emotional content.

## Emotion_and_Sentiment_Analysis

**Emotion_and_Sentiment_Analysis.py**

Building on the first file, this version adds more advanced steps:

**Lemmatization**: Reducing words to their base forms (e.g., "better" to "good").
Sentiment analysis: Using the VADER Sentiment Intensity Analyzer to evaluate the overall sentiment (positive, negative, or neutral) of the text.
Visualization: Similar to the basic file, it visualizes the frequency of detected emotions.
This file offers a transition toward integrating both emotion and sentiment analysis into a more complex workflow.

**Next Steps**: Once you've explored these introductory files, you can proceed to the main YouTube Video Analyzer script (Modulated1.py) for a more comprehensive application, where these techniques are applied to analyze YouTube video content.


## Project Structure  
sentiment_analysis/  
│  

├── Modulated1.py         # Contains the core logic for data extraction, preprocessing, emotion analysis, and sentiment analysis.

├── MAIN_APP.PY           # Contains the GUI implementation using customtkinter.

├── emotion.txt           # Lexicon file containing word-emotion associations. 

├── button_image.png      # Image for the analyze button in the GUI.

├── view.png              # Image for the button to view viewers' comments.

├── content.png           # Image for the button to view creators' data. 

├── read.txt              # File containing the viewers' comments.

├── read1.txt             # File containing the creators' data.

├── combined.txt          # File containing the combined data of viewers' comments and creators' data.

├── graph_viewers.png     # Image of the graph for viewers' emotions.

├── graph_creators.png    # Image of the graph for creators' emotions.

├── requirements.txt      # List of Python dependencies required for the project.

├── icon.ico              # YouTube Icon image for GUI window.

├── Basic_Emotion_Analysis.py  # Covers basic text cleaning, tokenization, and emotion analysis using the emotion.txt dataset.

├── Emotion_and_Sentiment_Analysis.py  # Builds on the basic file, introducing lemmatization, advanced tokenization, and a simple sentiment analysis using VADER.

└── README.md             # Project documentation .


## Screenshots 

![image](https://github.com/user-attachments/assets/bf4ca139-bcbb-49da-a6c0-6e003862bbef)

![image](https://github.com/user-attachments/assets/ec166df0-8b63-488d-b674-adb290948bc3)

![image](https://github.com/user-attachments/assets/71bd281f-a26d-4516-974d-6961c0c94c85)

![image](https://github.com/user-attachments/assets/850c8e24-b732-43dc-b0fd-2e1d7b6ec902)


## Milestones

**Achieved**

Developed the core logic for extracting and analyzing YouTube video data.
Implemented text preprocessing and emotion analysis using a lexicon-based approach.
Integrated VADER sentiment analysis for more accurate sentiment scores.
Created bar graphs to visualize the emotion distribution and overall sentiment.
Developed a graphical user interface (GUI) using customtkinter for user interaction.
Provided buttons to view the raw data and display the overall tone and sentiment analysis results.

**Partially Achieved**

Subtitle extraction: Subtitles are fetched if available, but the handling of non-English subtitles is not fully implemented.
Advanced emotion analysis: The current implementation uses a simple lexicon-based approach. More advanced techniques (e.g., machine learning models) could be integrated for better accuracy.

**Not Achieved**

Real-time analysis: The tool currently processes data in a batch mode. Real-time analysis and live updates are not implemented.
Multilingual support: The tool is primarily designed for English text. Support for other languages is not fully developed.


## Contributing
Contributions are welcome! If you'd like to contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Open a pull request to the main repository.
   

## License  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
Special thanks to all the developers and contributors whose libraries and APIs made this project possible.
This project was inspired by and adapted from:
- [Sentiment Analysis with/without NLTK Python] by [buildwithpython]  
- [How to extract YouTube Comments Using the YouTube API] by [Analytics with Adam]  
- Additional coding support from ChatGPT by OpenAI and HuggingChat by HuggingFace [Model: nvidia/Llama-3.1-Nemotron-70B-Instruct-HF].

## Contact
For any questions or feedback, please contact [ mahantaarunkumar809@gmail.com ].

---
