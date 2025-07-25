import os
import json
import datetime
from analyze_pdf import extract_sections, refine_sections, rank_sections_by_relevance
from utils import load_persona_job

input_dir = "input"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

if not os.path.exists("persona_job.json"):
    raise FileNotFoundError("Missing persona_job.json")

persona_info = load_persona_job("persona_job.json")
persona_text = persona_info["persona"] + " " + persona_info["job"]


metadata = {
    "persona": persona_info["persona"],
    "job_to_be_done": persona_info["job"],
    "processed_at": datetime.datetime.utcnow().isoformat() + "Z"
}

print(" Starting PDF processing...")

for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        print(f"{filename}")
        pdf_path = os.path.join(input_dir, filename)

        
        sections = extract_sections(pdf_path)
        print(f" Extracted {len(sections)} sections.")

    
        ranked_sections = rank_sections_by_relevance(sections, persona_text)
        print(f" Ranked top section score: {ranked_sections[0]['importance_rank']:.4f}")

        
        top_sections = ranked_sections[:5]
        refined = refine_sections(top_sections, persona_text)
        print(f"Refined to {len(refined)} semantic subsections.")

        output_data = {
            "metadata": metadata,
            "extracted_sections": top_sections,
            "subsection_analysis": refined
        }

       
        out_filename = f"output_{filename.replace('.pdf', '').replace(' ', '_')}.json"
        out_path = os.path.join(output_dir, out_filename)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f" Output written to: {out_path}\n")

    else:
        print(f" Skipping non-PDF: {filename}")
