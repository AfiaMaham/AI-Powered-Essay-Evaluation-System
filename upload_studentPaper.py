import customtkinter as ck
from tkinter import *
import re
import unicodedata
import threading
import copy
from spacy.lang.en.stop_words import STOP_WORDS
syllabus_dict = {}
answer_dict = {}
marks_dict = {}
report_data_list = []
marks_dict = {}

ck.set_appearance_mode("light")  
ck.set_default_color_theme("blue")
from tkinter import filedialog


class StudentMaterial:
    from collections import Counter
    
    report_data_list = []
    models_loaded = False
    loading_label = Label()
    data_list = []
    report_data = {}
    student_essay_list = []
    topic = ""

    def add_loading(self):
        self.topic += self.topic_box.get()
        self.loading_label = Label(self.studentMaterial, text='Wait a minute, It may take a while...', fg='#330000') 
        self.loading_label.configure(font=("Calibri", 11))
        self.loading_label.place(x=70,y=360)
        threading.Thread(target=self.load_models, daemon=True).start()

    def load_models(self):
        from nltk.corpus import brown
        from nltk import FreqDist      
        import spacy
        import language_tool_python
        # nltk.download('wordnet')
        self.tool = language_tool_python.LanguageTool('en-US')
        self.nlp = spacy.load("en_core_web_sm")
        self.fdist = FreqDist(brown.words())

        # Pre-calculate word ranks
        sorted_words = sorted(self.fdist.items(), key=lambda x: x[1], reverse=True)
        self.word_ranks = {word.lower(): rank + 1 for rank, (word, _) in enumerate(sorted_words)}
        self.models_loaded = True
        print(self.models_loaded)
        if self.models_loaded:
            self.loading_label.destroy()
            self.analyze_answer()
        

    def show_result_details(self,all_essay_results):
        popup = Toplevel()
        popup.title("Final Result Summary")
        popup.geometry("400x350")
        popup.configure(bg="#fefefe")

        # Configure grid layout
        popup.grid_rowconfigure(1, weight=1)  # Scrollable text area grows
        popup.grid_columnconfigure(0, weight=1)

        # Title label
        title_label = Label(popup, text="Essay Evaluation Score",
                            font=("yu gothic ui", 12, "bold"), bg="#fefefe")
        title_label.grid(row=0, column=0, pady=(10, 5))

        # Scrollable text area inside a frame
        text_frame = Frame(popup)
        text_frame.grid(row=1, column=0, sticky="nsew", padx=10)

        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        result_text = Text(text_frame, wrap=WORD, font=("yu gothic ui", 10, "bold"))
        result_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = Scrollbar(text_frame, orient=VERTICAL, command=result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        result_text.config(yscrollcommand=scrollbar.set)

        # Insert text
        for essay_result in all_essay_results:
            result_text.insert(END, f"{essay_result['Essay']}:\n")
            for criterion, score in essay_result["Breakdown"].items():
                result_text.insert(END, f"   {criterion}: {score}\n")
            result_text.insert(END, f"   ➤ Final Score: {essay_result['Total Score']} / 100\n\n")


        result_text.config(state=DISABLED)

        # Download button
        check_button = ck.CTkButton(
            popup,
            text="Download Detailed Report",
            font=("Arial", 15, "bold"),
            command=self.show_detailed_breakdown,
            corner_radius=10,
            height=35,
            width=200,
            fg_color="firebrick4",
            hover_color="firebrick3"
        )
        check_button.grid(row=2, column=0, pady=10)
        self.data_list.clear()

   
    def show_detailed_breakdown(self):
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import simpleSplit
        from tkinter import filedialog, messagebox
        import datetime

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Detailed_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        if filepath:
            c = canvas.Canvas(filepath, pagesize=A4)
            width, height = A4
            y = height - 50
            line_height = 16

            def write_line(text, bold=False):
                nonlocal y
                if y < 80:
                    c.showPage()
                    y = height - 50
                c.setFont("Helvetica-Bold" if bold else "Helvetica", 10)
                c.drawString(50, y, text)
                y -= line_height

            def write_wrapped_text(text, bold=False):
                nonlocal y
                font_name = "Helvetica-Bold" if bold else "Helvetica"
                font_size = 10
                max_width = width - 100  # 50px margin each side
                lines = simpleSplit(text, font_name, font_size, max_width)
                for line in lines:
                    if y < 80:
                        c.showPage()
                        y = height - 50
                    c.setFont(font_name, font_size)
                    c.drawString(50, y, line)
                    y -= line_height

            write_line("STUDENT ESSAY REPORT", bold=True)
            write_line("-" * 70)
            write_line(f"Date: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}")
            write_line("")
            print(f'Whole Error Report of an essay inside --------------:: {self.report_data_list}')

            for idx, report_data in enumerate(self.report_data_list):
                write_line("=" * 70)
                write_line(f"ESSAY {idx+1} REPORT:", bold=True)
                write_line("=" * 70)
                write_line("")

                spelling = report_data.get("Spelling", {})
                write_line("SPELLING ANALYSIS", bold=True)
                write_line(f"Error Count: {spelling.get('error_count', 'N/A')}")
                for error in spelling.get("errors", []):
                    write_line(f" - Incorrect Word: {error['incorrect_word']}")
                    write_line(f"   Message: {error['message']}")
                    write_line(f"   Suggestions: {', '.join(error['suggestions'])}")
                write_line("")



                grammar = report_data.get("Grammar", {})
                write_line("GRAMMAR ANALYSIS", bold=True)
                write_line(f"Score: {grammar.get('score', 'N/A')}")
                write_line(f"Error Count: {grammar.get('error_count', 'N/A')}")
                write_line(f"Error Density: {grammar.get('error_density', 'N/A')}")
                write_line("Issues:")
                for issue in grammar.get("issues", []):
                    write_line(f" - Message: {issue.get('message')}")
                    write_line(f"   Sentence: {issue.get('sentence')}")
                    write_line(f"   Suggestions: {', '.join(issue.get('suggestions', []))}")
                    write_line("")

                vocab = report_data.get("Vocabulary", {})
                write_line("VOCABULARY ANALYSIS", bold=True)
                write_wrapped_text(f"Basic words: {vocab.get('basic_words_list', 'N/A')}")
                write_wrapped_text(f"Advanced words: {vocab.get('advanced_words_list', 'N/A')}")
                write_line(f"Basic words percentage: {vocab.get('basic_words_percentage', 'N/A')}")
                write_line(f"Advanced words percentage: {vocab.get('advanced_words_percentage', 'N/A')}")

                write_line("")

                readability = report_data.get("Readability", {})
                write_line("READABILITY ANALYSIS", bold=True)
                write_line(f"Flesch Reading Ease: {readability.get('flesch_reading_ease', 'N/A')}")
                write_line(f"Ease Description: {readability.get('ease_description', 'N/A')}")
                write_line(f"Flesch-Kincaid Grade: {readability.get('flesch_kincaid_grade', 'N/A')}")
                write_line(f"Estimated Grade Level: {readability.get('estimated_grade_level', 'N/A')}")

                write_line("\n\n")


            c.save()
            messagebox.showinfo("Success", f"PDF Report saved to:\n{filepath}")

    def preprocess_essay(self,text: str):
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
   
        return {
            "cleaned_text": text,
            "sentences": sentences,
            "spacy_doc": doc 
        }
    
    def evaluate_organization(self,processed_essay: dict):
        sentences = processed_essay["sentences"]
        text = processed_essay["cleaned_text"]
        # Define common transition/conclusion words
        intro_signals = [
            "this essay", "in this essay", "the purpose", "i will discuss", "i am going to",
            "the topic of", "this paper", "we will explore", "the focus of this essay", 
            "the main idea", "this article discusses", "this composition", "let us examine"
        ]     
        conclusion_signals = [
            "in conclusion", "to conclude", "to sum up", "overall", "finally", "in summary",
            "to summarize", "as a result", "all in all", "thus", "at the end", "in closing", 
            "in short", "we can conclude that"
        ]
        transition_words = [
            "however", "moreover", "therefore", "furthermore", "in addition", "meanwhile",
            "instead", "on the other hand", "although", "even though", "in contrast", 
            "for example", "for instance", "as a result", "likewise", "similarly", 
            "consequently", "in other words", "nonetheless", "additionally", "hence", 
            "despite", "notably", "on the contrary", "besides", "subsequently"
        ]
        # Heuristic flags
        has_intro = any(sig in text.lower() for sig in intro_signals)
        has_conclusion = any(sig in text.lower() for sig in conclusion_signals)
        transition_count = sum(text.lower().count(word) for word in transition_words)
        
        body_sentences = [s for s in sentences if not any(kw in s.lower() for kw in intro_signals + conclusion_signals)]

        # Structure logic
        has_body = len(body_sentences) >= 5

        # Final logic for scoring
        score = 0

        if has_intro:
            score += 1

        if has_body:
            score += 1
        if has_conclusion:
            score += 1

        if transition_count >= 2:
            score += 1
        elif transition_count == 1:
            score += 0.5

        # Clip score to max 5
        return {
            "component": "Organization",
            "score": round(score, 1),
            "out_of": 5,
        }

    def evaluate_content_relevance(self,student_essay, topic):
        essay_doc = self.nlp(student_essay)
        topic_doc = self.nlp(topic)

        # STEP 1: Extract topic keywords (nouns, verbs, named entities)
        topic_keywords = set([token.lemma_.lower() for token in topic_doc 
                            if token.pos_ in ['NOUN', 'PROPN', 'VERB'] and not token.is_stop])

        # STEP 2: Extract essay keywords
        essay_keywords = set([token.lemma_.lower() for token in essay_doc 
                            if token.pos_ in ['NOUN', 'PROPN', 'VERB'] and not token.is_stop])

        # STEP 3: Keyword overlap
        matched_keywords = topic_keywords.intersection(essay_keywords)
        overlap_ratio = len(matched_keywords) / (len(topic_keywords) + 1e-5)  # Avoid division by zero

        # STEP 4: Semantic similarity (backup if low keyword match)
        similarity_score = topic_doc.similarity(essay_doc)

        # STEP 5: Decide score (out of 5)
        if overlap_ratio > 0.6 or similarity_score > 0.85:
            score = 5
        elif overlap_ratio > 0.4 or similarity_score > 0.75:
            score = 4
        elif overlap_ratio > 0.25 or similarity_score > 0.65:
            score = 3
        elif overlap_ratio > 0.1 or similarity_score > 0.5:
            score = 2
        else:
            score = 1
        return {
            "Component": "Content Relevance",
            "score": score,
            "overlap_ratio": round(overlap_ratio, 2),
            "similarity_score": round(similarity_score, 2),
            "matched_keywords": list(matched_keywords)
        }
    
    def evaluate_grammar_mechanics(self,essay_text):

        matches = self.tool.check(essay_text)
        
        num_errors = len(matches)
        num_words = len(essay_text.split())
        error_density = num_errors / (num_words + 1e-5)  

        if error_density < 0.01:
            score = 5
        elif error_density < 0.02:
            score = 4
        elif error_density < 0.04:
            score = 3
        elif error_density < 0.06:
            score = 2
        else:
            score = 1

        issues = [{
            "message": m.message,
            "suggestions": m.replacements,
            "sentence": m.context,
            "offset": m.offset
        } for m in matches]

        if "Grammar" not in self.report_data:
            self.report_data["Grammar"] = {}

        self.report_data["Grammar"] = {
            "score": score,
            "error_count": num_errors,
            "error_density": round(error_density, 4),
            "issues": issues
                }

        return {
            "Component": "Grammar",
            "score": score,
            "error_count": num_errors,
            "error_density": round(error_density, 4),
            "issues": issues
        }

    def evaluate_vocabulary(self, student_essay):
        freq_dict = {}
        with open('en_50k.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    word, freq = parts
                    freq_dict[word] = int(freq)

        text = unicodedata.normalize("NFKD", student_essay).encode("ascii", "ignore").decode("utf-8")
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)

        tokens = [token for token in text.lower().split(' ') if token.isalpha() and token not in STOP_WORDS]
        threshold = 500000  

        basic_words = []
        advanced_words = []

        for word in tokens:
            freq = freq_dict.get(word, 0)
            if freq >= threshold:
                basic_words.append(word)
            else:
                advanced_words.append(word)


        total_words = len(tokens)
        basic_count = len(basic_words)
        advanced_count = len(advanced_words)
        basic_words_percentage = (basic_count / total_words) * 100 if total_words else 0
        advanced_words_percentage = (advanced_count / total_words) * 100 if total_words else 0

        # Store in report
        self.report_data["Vocabulary"] = {
                "total_words": total_words,
                "basic_words_count": basic_count,
                "advanced_words_count": advanced_count,
                "basic_words_percentage": basic_words_percentage,
                "advanced_words_percentage": advanced_words_percentage - basic_words_percentage,
                "basic_words_list": basic_words,
                "advanced_words_list": advanced_words
        }
        return {
                "total_words": total_words,
                "basic_words_count": basic_count,
                "advanced_words_count": advanced_count,
                "basic_words_percentage": basic_words_percentage,
                "advanced_words_percentage": advanced_words_percentage - basic_words_percentage,
                "basic_words_list": basic_words,
                "advanced_words_list": advanced_words
            }
   
        
    def check_spelling(self, text):
        matches = self.tool.check(text)
        spelling_errors = [match for match in matches if match.ruleId == 'MORFOLOGIK_RULE_EN_US']
        error_count = len(spelling_errors)

        errors_detail = []
        for err in spelling_errors:
            errors_detail.append({
                'incorrect_word': text[err.offset : err.offset + err.errorLength],
                'message': err.message,
                'suggestions': err.replacements
            })

        if "Spelling" not in self.report_data:
            self.report_data["Spelling"] = {}
        self.report_data["Spelling"]["error_count"] = len(spelling_errors)
        self.report_data["Spelling"]["errors"] = errors_detail
    
        return {
            "Component" : "Spelling",
            'spelling_error_count': error_count,
            'spelling_errors': errors_detail
        }

    def evaluate_length(self,text, min_words=100, max_words=1000):
        word_count = len(text.split())
        if word_count < min_words:
            return ("Too Short", word_count)
        elif word_count > max_words:
            return ("Too Long", word_count)
        else:
            return ("Good Length", word_count)

  
    def evaluate_readability(self,text):
        import textstat
        grade_level = textstat.flesch_kincaid_grade(text)
       
        if 8 <= grade_level <= 18:
            score = 10
        elif 6 <= grade_level < 8:
            score = 8
        elif 4 <= grade_level < 6:
            score = 6
        elif 2 <= grade_level < 4:
            score = 4
        else:
            score = 2


        if "Readability" not in self.report_data:
            self.report_data["Readability"] = {}

        self.report_data["Readability"] = {
            "flesch_kincaid_grade": round(grade_level, 2),
            "estimated_grade_level": f"{int(round(grade_level))}th grade",
            "score": score
        }

        return {
            "Component" : "Readability",
            "flesch_kincaid_grade": round(grade_level, 2),
            "estimated_grade_level": f"{int(round(grade_level))}th grade",
            "score": score
        }


    def analyze_answer(self):
        self.all_essay_results = []
        for idx, student_essay in enumerate(self.student_essay_list, start=1):
            processed_data = self.preprocess_essay(student_essay)
            organized_data = self.evaluate_organization(processed_data)
            relevance = self.evaluate_content_relevance(student_essay, self.topic)
            grammar = self.evaluate_grammar_mechanics(student_essay)
            vocabulary = self.evaluate_vocabulary(student_essay)
            spelling = self.check_spelling(student_essay)
            readability = self.evaluate_readability(student_essay)
            total_score = 0
            breakdown = {}
            # Each out of 5 → weighted to 20
            org_score = (organized_data['score'] / 5) * 20
            breakdown["Organization"] = f"{round(org_score, 2)} / 20"
            total_score += org_score

            # Content Relevance (out of 20)
            rel_score = (relevance['score'] / 5) * 10
            breakdown["Content Relevance"] = f"{round(rel_score, 2)} / 10"
            total_score += rel_score

            # Grammar (out of 20)
            grammar_score = (grammar['score'] / 5) * 20
            breakdown["Grammar"] = f"{round(grammar_score, 2)} / 20"
            total_score += grammar_score

            # Vocabulary (out of 15)
            def calculate_vocab_score(evaluation_result):
                adv_pct = evaluation_result["advanced_words_percentage"]
                basic_pct = evaluation_result["basic_words_percentage"]

                # Base score from advanced words percentage
                score = (adv_pct / 100) * 15

                # Penalize if too many basic words (>70% for example)
                if basic_pct > 70:
                    penalty = (basic_pct - 70) / 100 * 5  # penalty up to 5 points
                    score -= penalty

                return round(max(score, 0), 2) 

            vocab_score = calculate_vocab_score(vocabulary)
            breakdown["Vocabulary"] = f"{vocab_score} / 15"
            total_score += vocab_score

            # Spelling (out of 10)
            num_words = len(student_essay.split())
            spelling_errors = spelling['spelling_error_count']
            spelling_penalty = min(spelling_errors / (num_words + 1e-5), 1.0)
            spelling_score = (1 - spelling_penalty) * 10
            breakdown["Spelling"] = f"{round(spelling_score, 2)} / 10"
            total_score += spelling_score

            # Readability (out of 10)
            
            breakdown["Readability"] = f"{readability['score']} / 10"
            total_score += readability["score"]



            
            if vocab_score >=10 and grammar_score >= 15:
                total_score += 10
            elif vocab_score >= 8 and grammar_score >= 13:
                total_score += 5
            total_score = round((total_score / 95) * 100, 2)

            self.all_essay_results.append({
                "Essay": f"Essay {idx}",
                "Total Score": round(total_score, 2),
                "Breakdown": breakdown
            })
            self.report_data_list.append(copy.deepcopy(self.report_data))
            self.report_data.clear()


      
        self.show_result_details(self.all_essay_results)
           

    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")]
        )
        if filename:
            self.label.config(text=filename.split('/')[-1])
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.student_essay_list.append(content)
            except Exception as e:
                print("Error reading file:", e)
        else:
            self.label.config(text="No file chosen")

    def reset(self):
        self.student_essay_list.clear()
        self.label.config(text="No file chosen")

    def __init__(self, master):
        self.studentMaterial = Toplevel(master)
        self.studentMaterial.title("Student materials")
        self.studentMaterial.geometry("800x550")

        self.canvas = Canvas(self.studentMaterial, width=800, height=550, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # self.content_frame = Frame(self.canvas, bg="#330000")
        # self.canvas.create_window((0, 0), window=self.content_frame, anchor='nw', width=800, height=550)

       
        topic_text = ("Essay Evaluation Using Natural\n"
                        "Language Processing")
        uploadArea_label = Label(self.studentMaterial, text=topic_text, fg="#330000", 
                                font=("Game Of Squids", 26, "bold"))
        uploadArea_label.place(x=53, y=70)

        welcome_text = (
                    "Empowering educators with smart, efficient, and fair essay evaluation.Your smart\n" 
                    "assistant for faster, unbiased assessment.Leveraging the power of AI and NLP\n" 
                    "to analyze and evaluate intelligently."
                )
                
        welcome_label = Label(self.studentMaterial, text=welcome_text, fg='#330000',justify="left")
        welcome_label.configure(font=("Calibri", 11))
        welcome_label.place(x=53,y=165)

        line = ck.CTkFrame(self.studentMaterial, height=2, fg_color="#888888",width=400)
        line.place(x=57,y=230)

        uploadMaterial_label = Label(self.studentMaterial, text="Just upload student material and let automation do the rest.",
                                    fg="#330000", font=("yu gothic ui", 11, "bold"))
        uploadMaterial_label.place(x=57, y=250)

        uploadMaterial_label = Label(self.studentMaterial, text="Topic",
                                    fg="#330000", font=("yu gothic ui", 11, "bold"))
        uploadMaterial_label.place(x=270, y=310)

        self.topic_box = Entry(self.studentMaterial, width=30)
        self.topic_box.place(x=370,y=310)
        upload_btn = Button(self.studentMaterial, text="Choose file", command=self.browse_file)
        upload_btn.place(x=370,y=360)

        self.label = Label(self.studentMaterial, text="No file chosen", padx=10, fg='#330000')
        self.label.place(x=450,y=360)

        evaluate_button = ck.CTkButton(self.studentMaterial, text="Evaluate", font=("Arial", 15, "bold"),
                                    command=self.add_loading, corner_radius=10, height=37, width=100,
                                    fg_color="firebrick4", hover_color="firebrick3")
        evaluate_button.place(x=460, y=430)

        evaluate_button = ck.CTkButton(self.studentMaterial, text="Reset", font=("Arial", 15, "bold"),
                                    command=self.reset, corner_radius=10, height=37, width=100,
                                    fg_color="firebrick4", hover_color="firebrick3")
        evaluate_button.place(x=260, y=430)

      
