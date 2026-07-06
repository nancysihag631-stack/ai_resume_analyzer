import re
from typing import Tuple, List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Unified Configuration Pool for clean maintenance
APP_CONFIG = {
    "HARD_SKILLS": {
        "python", "sql", "java", "javascript", "react", "aws", "docker", 
        "git", "html", "css", "tableau", "excel", "c++", "linux", "cloud", "api"
    },
    "SOFT_SKILLS": {
        "leadership", "communication", "teamwork", "problem-solving", 
        "agile", "management", "collaboration", "adaptability", "critical thinking"
    },
    "ACTION_VERBS": {
        "developed", "optimized", "implemented", "designed", "built", 
        "engineered", "led", "managed", "created", "automated", "analyzed"
    },
    "BLUEPRINTS": {
        "Python": "Build an Automated Web Scraper that tracks internship listings and stores them in a CSV.",
        "Sql": "Design an Identity Management Relational Database schema with complex JOIN queries for a mock store.",
        "Aws": "Deploy a static portfolio website using AWS S3, CloudFront, and set up a budget alarm.",
        "Docker": "Containerize a multi-service web application (Frontend + Backend + DB) using Docker Compose.",
        "React": "Create a responsive Personal Dashboard App utilizing external REST APIs and custom hooks.",
        "Git": "Publish an open-source contribution or document a repository using robust Git Branching strategies."
    }
}

class ResumeAnalyzer:
    """Handles core computational NLP workflows and structural heuristics for resume parsing."""
    
    def __init__(self, resume_text: str, jd_text: str):
        self.resume_raw = resume_text.strip()
        self.resume_lower = self.resume_raw.lower()
        self.jd_raw = jd_text.strip()
        
        # Tokenize words into a clean set using regex for faster lookups
        self.resume_words = set(re.findall(r'\b\w+\b', self.resume_lower))
        self.jd_words = set(re.findall(r'\b\w+\b', self.jd_raw.lower()))

    def calculate_match_score(self) -> int:
        """Computes contextual text alignment percentage via Cosine Similarity."""
        if not self.resume_raw or not self.jd_raw:
            return 0
        
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([self.resume_raw, self.jd_raw])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            
            # Map math outputs into standard recruiting score thresholds
            score = int(similarity[0][0] * 100)
            return min(score + 15, 100)
        except Exception:
            return 0

    def extract_keyword_gaps(self) -> Tuple[List[str], List[str]]:
        """Identifies missing keyword requirements split by hard tools and soft skills."""
        missing_words = self.jd_words - self.resume_words
        
        missing_hard = [w.capitalize() for w in missing_words if w in APP_CONFIG["HARD_SKILLS"]]
        missing_soft = [w.capitalize() for w in missing_words if w in APP_CONFIG["SOFT_SKILLS"]]
        
        return sorted(missing_hard), sorted(missing_soft)

    def check_structural_compliance(self) -> Dict[str, bool]:
        """Validates existence of standard mandatory resume headers."""
        sections = {
            "Education": ["education", "academic", "qualification"],
            "Projects": ["project", "capstone", "repositories", "github"],
            "Skills": ["skills", "technical proficiencies", "technologies"],
            "Experience": ["experience", "employment", "work history", "internship"]
        }
        return {sec: any(kw in self.resume_lower for kw in kws) for sec, kws in sections.items()}

    def evaluate_phrasing_tone(self) -> Tuple[str, int]:
        """Scores vocabulary impact based on frequency of descriptive action verbs."""
        found_verbs = [w for w in self.resume_lower.split() if w in APP_CONFIG["ACTION_VERBS"]]
        count = len(found_verbs)
        
        if count >= 8:
            return "Strong & Impactful 💪", count
        elif count >= 4:
            return "Moderate Phrasing 👍", count
        return "Passive Tone ⚠️", count

    def get_readability_metrics(self) -> Tuple[str, str]:
        """Runs a density test matching standard single-page length constraints."""
        word_count = len(self.resume_raw.split())
        
        if word_count == 0:
            return "Empty Document", "red"
        elif word_count < 200:
            return f"Too Short ({word_count} words) - Lacks technical depth for modern parser parsing.", "orange"
        elif word_count > 650:
            return f"Too Wordy ({word_count} words) - Exceeds ideal single page density guidelines.", "red"
        return f"Ideal Length ({word_count} words) - Highly optimized layout density.", "green"

    def generate_project_roadmaps(self, missing_hard: List[str]) -> List[Tuple[str, str]]:
        """Maps specific tool gaps to actionable code blueprints for portfolios."""
        roadmaps = []
        for skill in missing_hard:
            if skill in APP_CONFIG["BLUEPRINTS"]:
                roadmaps.append((skill, APP_CONFIG["BLUEPRINTS"][skill]))
        return roadmaps[:3]