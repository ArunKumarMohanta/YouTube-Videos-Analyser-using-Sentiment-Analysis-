import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox
from Modulated1 import YouTubeAnalyzer, SentimentAnalyzer, combine_files, find_overall_tone
from PIL import Image, ImageTk
import sys
import ctypes
#import os

class TextRedirect:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  

    def flush(self):
        pass

class YouTubeEmotionAnalyzerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.video_title = ""

        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")


        
        self.state("zoomed")  
        
        global BASE_FONT_SIZE
        BASE_FONT_SIZE = -20

        self.title("YouTube Emotion Analyzer")
        #self.geometry("800x600")

        
        self.iconbitmap('icon.ico')  


        

        
        url_frame = tk.Frame(self, bg="#2b2b2b")
        url_frame.pack(fill=tk.X,pady=int(0.001 * self.winfo_screenheight()))

       
        search_frame = tk.Frame(self, bg="#2b2b2b")
        search_frame.pack(fill=tk.X, pady=int(0.01 * self.winfo_screenheight()))

        self.url_label = ctk.CTkLabel(search_frame, text="YouTube Video URL:", font=("Arial", BASE_FONT_SIZE))
        self.url_label.pack(side=tk.LEFT, padx=int(0.01 * self.winfo_screenwidth()))



        self.url_entry = ctk.CTkEntry(search_frame, font=("Arial", BASE_FONT_SIZE - 2))
        self.url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=int(0.001 * self.winfo_screenwidth()))
       
        button_frame = tk.Frame(self, bg="#2b2b2b")
        button_frame.pack(fill=tk.X, pady=(0, int(0.001 * self.winfo_screenheight())))

        button_image_path = "button_image.png"
        button_image = Image.open(button_image_path)
        button_image = button_image.resize((int(0.03 * self.winfo_screenwidth()), int(0.05 * self.winfo_screenheight())))
        tk_button_image = ImageTk.PhotoImage(button_image)

        self.analyze_button = ctk.CTkButton(search_frame, image=tk_button_image, text="", compound=tk.TOP, 
                                            command=self.analyze_video, width=int(0.04 * self.winfo_screenwidth()), height=int(0.04 * self.winfo_screenheight()))
        self.analyze_button.image = tk_button_image
        self.analyze_button.pack(side=tk.RIGHT, padx=int(0.01 * self.winfo_screenwidth()), pady=int(0.005 * self.winfo_screenheight()))

       

        
        graph_container_frame = tk.Frame(self, bg="#2b2b2b")
        graph_container_frame.pack(pady=int(0.01 * self.winfo_screenheight()), fill=tk.BOTH, expand=True)

        self.creator_graph_frame = tk.Frame(graph_container_frame, bg="#2b2b2b")
        self.creator_graph_frame.pack(side=tk.LEFT, padx=int(0.01 * self.winfo_screenwidth()), fill=tk.BOTH, expand=True)

        self.viewer_graph_frame = tk.Frame(graph_container_frame, bg="#2b2b2b")
        self.viewer_graph_frame.pack(side=tk.LEFT, padx=int(0.01 * self.winfo_screenwidth()), fill=tk.BOTH, expand=True)

       
        self.output_text_box = tk.Text(self, height=6, width=120, bg="#2b2b2b", fg="#FFFFFF")
        self.output_text_box.config(font=("Courier new", 25))  
        self.output_text_box.pack(fill=tk.BOTH, expand=True, pady=(10, 10))


        
        self.status_bar = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.overall_tone_label = ctk.CTkLabel(self.status_bar, text="", font=("Arial", BASE_FONT_SIZE))
        self.overall_tone_label.pack(side=tk.LEFT, padx=10, pady=5)

       
        sys.stdout = TextRedirect(self.output_text_box)

        self.status_bar_separator = ctk.CTkLabel(self.status_bar, text="|", font=("Arial", BASE_FONT_SIZE), fg_color="#2b2b2b",
                                                 text_color="#AAAAAA")
        self.status_bar_separator.pack(side=tk.LEFT, padx=5, pady=5)

        
        image_path = "path_to_your_image.png"
        image = Image.open('view.png')
        
        image = image.resize((int(0.02 * self.winfo_screenwidth()), int(0.03 * self.winfo_screenheight()))) 
        
        tk_image = ImageTk.PhotoImage(image)

        
        self.view_buttons_frame = tk.Frame(self.status_bar, bg="#2b2b2b")
        self.view_buttons_frame.pack(side=tk.LEFT, padx=5, pady=5)

        self.view_read_txt_button = ctk.CTkButton(self.view_buttons_frame, text="Comments", compound=tk.TOP, command=self.display_read_txt,
                                                  width=30, height=30)
        self.view_read_txt_button.image = tk_image  
        self.view_read_txt_button.pack(side=tk.LEFT, padx=2, pady=2)

       
        image_path1 = "content.png"
        image1 = Image.open(image_path1)
       
        image1 = image1.resize((int(0.02 * self.winfo_screenwidth()), int(0.03 * self.winfo_screenheight()))) 
       
        tk_image = ImageTk.PhotoImage(image1)

        self.view_read1_txt_button = ctk.CTkButton(self.view_buttons_frame,  text="Video Metadata",compound=tk.TOP, command=self.display_read1_txt,
                                                   width=30, height=30)
        self.view_read_txt_button.image = tk_image  
        self.view_read1_txt_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.view_aisummary_button = ctk.CTkButton(self.view_buttons_frame,  text="Summary",compound=tk.TOP, command=self.display_aisummary,
                                                   width=30, height=30)
        self.view_aisummary_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.view_factcheck_button = ctk.CTkButton(self.view_buttons_frame,  text="Fact Checker",compound=tk.TOP, command=self.display_factcheck,
                                                   width=30, height=30)
        self.view_factcheck_button.pack(side=tk.LEFT, padx=2, pady=2)



        self.status_bar_copyright = ctk.CTkLabel(self.status_bar, text="© 2025  Arun Kumar Mohanta",
                                                 font=("Arial", 20), fg_color="#2b2b2b", text_color="#AAAAAA")
        self.status_bar_copyright.pack(side=tk.RIGHT, padx=10, pady=5)

    def display_read_txt(self):
        try:
            with open('read.txt', 'r', encoding='utf-8') as file:
                content = file.read()
                file.close()

            
            read_txt_window = tk.Toplevel(self)
            read_txt_window.title("Viewers' Comments")
            read_txt_window.geometry("1000x800")

            
            text_widget = tk.Text(read_txt_window, font=("Consolas", 25))
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(tk.INSERT, content)
            text_widget.config(state="disabled")  
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_read1_txt(self):
        try:
            with open('read1.txt', 'r', encoding='utf-8') as file:
                content = file.read()
                file.close()

            
            read1_txt_window = tk.Toplevel(self)
            read1_txt_window.title("Content Metadata")
            read1_txt_window.geometry("1000x800")

           
            text_widget = tk.Text(read1_txt_window, font=("Consolas", 25))
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(tk.INSERT, content)
            text_widget.config(state="disabled")  
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def display_aisummary(self):
        try:
            with open('summary.txt', 'r', encoding='utf-8') as file:
                content = file.read()
                file.close()
        
           
            aisummary_window = tk.Toplevel(self)
            aisummary_window.title("Summary")
            aisummary_window.geometry("600x400")

            
            text_widget = tk.Text(aisummary_window, font=("Consolas", 20))
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(tk.INSERT, content)
            text_widget.config(state="disabled")  
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_factcheck(self):
        try:
            with open('factcheck.txt', 'r', encoding='utf-8') as file:
                content = file.read()
                file.close()
        
            
            aifactcheck_window = tk.Toplevel(self)
            aifactcheck_window.title("Fact Checker")
            aifactcheck_window.geometry("600x400")

            
            text_widget = tk.Text(aifactcheck_window, font=("Helvetica", 21))
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(tk.INSERT, content)
            text_widget.config(state="disabled")  
        except Exception as e:
            messagebox.showerror("Error", str(e))    

    def graph_plot(self, frame, emotions, label, whose):
        for widget in frame.winfo_children():
            widget.destroy()

       
        total_count = sum(emotions.values())
        percentages = {k: (v / total_count) * 100 for k, v in emotions.items() if total_count!= 0}

        if not percentages: 
            
            label_no_data = tk.Label(frame, text=f"{whose} Emotions\nNo Emotion Data Available", font=('Helvetica', 20))
            label_no_data.pack()
            return  

        
        figure = Figure(figsize=(int(0.1 * self.winfo_screenwidth()) / 100, int(0.5 * self.winfo_screenheight()) / 100), dpi=100)
        ax = figure.add_subplot(111)
        figure.patch.set_facecolor('#121212')  
        ax.set_facecolor('#1E1E1E')  

        
        bars = ax.bar(percentages.keys(), percentages.values(), color='#FF8C00')  

        
        ax.set_ylim(0, max(percentages.values()) * 1.2)

       
        for spine in ax.spines.values():
            spine.set_color('#B0B0B0')  
            spine.set_linewidth(1.5)

        
        ax.grid(True, which='major', color='#444444', linestyle='--', linewidth=0.7)  
        ax.grid(True, which='minor', color='#2E2E2E', linestyle=':', linewidth=0.5)  
        ax.minorticks_on() 

       
        ax.tick_params(axis='x', colors='#00FA9A', labelsize=20)
        ax.tick_params(axis='y', colors='#00FA9A', labelsize=20)
        
        ax.set_xlabel("Emotion Type-->", fontsize=15, color='#FFD700', labelpad=7)  

       
        ax.set_ylabel("Percentage-->", fontsize=15, color='#FFD700', labelpad=10)  

       
       
        for idx, bar in enumerate(bars):
            height = bar.get_height()
            offset = 8 if idx % 2 == 0 else 15  
            ax.annotate(f"{round(height, 1)}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height), 
                        xytext=(0, offset),  
                        textcoords="offset points",
                        ha='center', va='bottom', color='#FFD700', fontsize=20)  

       
        ax.text(-0.145, 1.12, self.video_title, transform=ax.transAxes, fontsize=20.0,
                bbox=dict(facecolor='#8A7F8D', alpha=0.5, edgecolor='none'), color='#FFD700')
        ax.set_title("\n" + whose + " Emotions", color='white',fontsize=20)

       
        plt.subplots_adjust(top=0.85, bottom=0.2)
        figure.autofmt_xdate()  

       
        ax.text(-0.145, -0.25, "Overall Sentiment[NLTK]: " + label,
                 verticalalignment='center',
                transform=ax.transAxes, fontsize=17,
                bbox=dict(facecolor='#8A7F8D', alpha=0.5, edgecolor='none'),  
                color='#FFD700')  

       
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def analyze_video(self):
       

        
        self.output_text_box.delete(1.0, tk.END)  

        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube video URL")
            return

       
        youtube_analyzer = YouTubeAnalyzer()
        sentiment_analyzer = SentimentAnalyzer()

        
        youtube_analyzer.vid = youtube_analyzer.extract_video_id(url)
        youtube_analyzer.get_creators()
        youtube_analyzer.get_viewers()

       

        
        youtube_analyzer.save_viewers_comments()
        m=youtube_analyzer.save_creators_data()
        youtube_analyzer.ai_analysis()
        youtube_analyzer.ai_factcheck()

        
        print("* "+m)

        
        self.video_title = youtube_analyzer.get_title()  

        
        combine_files('read.txt', 'read1.txt', 'Combined.txt')

       
        overall_tone = find_overall_tone('Combined.txt')
        if isinstance(overall_tone, list):
            overall_tone_str = ", ".join(overall_tone)
        else:
            overall_tone_str = overall_tone

        
        score = sentiment_analyzer.polarity_score('Combined.txt')

        
        percent_score=sentiment_analyzer.convert_scores_to_percent(score)


        print(f"* Overall Tone: {overall_tone_str} \n*SCORES* \n* Positive Score:{percent_score['pos']}(%) \n* Negative Score:{percent_score['neg']}(%) \n* Neutral Score:{percent_score['neu']}(%) \n* Compound Score:{percent_score['compound']}(%)")

        
        creator_emotions = sentiment_analyzer.emotions_from_emotions_txt('read1.txt')
        viewer_emotions = sentiment_analyzer.emotions_from_emotions_txt('read.txt')
        
        label1=sentiment_analyzer.sentiment_analyse('read1.txt')
        label2 = sentiment_analyzer.sentiment_analyse('read.txt')

        

        self.graph_plot(self.creator_graph_frame, creator_emotions, label1, "Creator's")
        self.graph_plot(self.viewer_graph_frame, viewer_emotions, label2, "Viewer's")


if __name__ == "__main__":
    app = YouTubeEmotionAnalyzerGUI()

    app.mainloop()