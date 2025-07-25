from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util

def extract_sections(pdf_path):
    """
    Split PDF into page-based sections.
    """
    reader = PdfReader(pdf_path)
    sections = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            sections.append({"page": i + 1, "text": text.strip()})
    return sections

def refine_sections(sections, persona_text):
    """
    Further split and clean top sections into smaller subsections.
    """
    refined = []
    for section in sections:
        parts = [p.strip() for p in section["text"].split("\n") if len(p.strip()) > 40]
        for part in parts:
            refined.append({
                "page": section["page"],
                "content": part
            })
    return refined

def rank_sections_by_relevance(sections, persona_text):
    """
    Rank full page sections based on semantic similarity with persona + job.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    persona_embedding = model.encode(persona_text, convert_to_tensor=True)

    ranked = []
    for section in sections:
        embedding = model.encode(section["text"], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(persona_embedding, embedding).item()
        section["importance_rank"] = similarity
        ranked.append(section)

    return sorted(ranked, key=lambda x: x["importance_rank"], reverse=True)
