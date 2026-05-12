import os
import re
from pathlib import Path
from datetime import datetime

REPO_DIR = Path(__file__).parent

def human_size(size_bytes: int) -> str:
	for unit in ["B", "KB", "MB"]:
		if size_bytes < 1024:
			return f"{size_bytes:.0f} {unit}"
		size_bytes /= 1024
	return f"{size_bytes:.1f} MB"

def clean_name(filename: str) -> str:
	name = Path(filename).stem
	name = re.sub(r'\s+-\s+[a-f0-9]{8,}(-[a-f0-9]+)*$', "", name, flags=re.IGNORECASE)
	name = re.sub(r'\s+[A-Z0-9]{6,12}$', "", name)
	name = re.sub(r'\s*[\-_]?(Coursera|Google|edX|Udacity|Coursera Certificate|Certificate of|Completion|Certificate)$', "", name, flags=re.IGNORECASE)
	name = re.sub(r'\s*[\-_]?\d+[A-Z0-9]{4,}$', "", name)
	name = re.sub(r'\s*\(.*?\)', "", name)
	name = re.sub(r'\s+', " ", name).strip()
	name = name.title()
	return name if name else Path(filename).stem

def get_icon(filename: str) -> tuple:
	fn = filename.lower()
	if "coursera" in fn:
		return ("&#x1F3F3;", "Coursera")
	if "google" in fn or "gcp" in fn or "vertex" in fn or "google gen ai" in fn:
		return ("&#x1F534;", "Google")
	if "ibm" in fn:
		return ("&#x1F517;", "IBM")
	if "hugging" in fn:
		return ("&#x1F917;", "Hugging Face")
	if "kaggle" in fn:
		return ("&#x1F4CA;", "Kaggle")
	if "udemy" in fn:
		return ("&#x1F4DA;", "Udemy")
	if "linkedin" in fn:
		return ("&#x1F3BC;", "LinkedIn")
	if "tata" in fn:
		return ("&#x1F3E2;", "TATA")
	if "deep learning" in fn or "neural" in fn or "keras" in fn:
		return ("&#x1F9E0;", "Deep Learning")
	if "mlops" in fn or "vertex" in fn:
		return ("&#x2699;&#xFE0F;", "MLOps")
	if "generative ai" in fn or "gen ai" in fn or "llm" in fn or "gpt" in fn or "chatgpt" in fn:
		return ("&#x2728;", "Generative AI")
	if "cloud" in fn:
		return ("&#x2601;&#xFE0F;", "Cloud")
	if "dsa" in fn or "algorithm" in fn or "dynamic programming" in fn:
		return ("&#x1F4BB;", "Algorithms")
	if "docker" in fn or "kubernetes" in fn or "devops" in fn:
		return ("&#x1F41B;", "DevOps")
	if "python" in fn:
		return ("&#x1F40D;", "Python")
	return ("&#x1F4DC;", "Certificate")

def format_date(path: Path) -> str:
	ts = os.path.getmtime(path)
	return datetime.fromtimestamp(ts).strftime("%b %Y")

def build_readme():
	pdf_files = sorted(REPO_DIR.glob("*.pdf"), key=lambda p: p.stat().st_size)

	cards = []
	for f in pdf_files:
		icon, platform = get_icon(f.name)
		name = clean_name(f.name)
		size = human_size(f.stat().st_size)
		date = format_date(f)
		encoded = f.name.replace(" ", "%20").replace("(", "%28").replace(")", "%29")
		# raw URL for PDF embedding
		raw_url = f"https://github.com/atul-harsh33108/My-Certificate/raw/main/{encoded}"
		view_url = f"https://github.com/atul-harsh33108/My-Certificate/blob/main/{encoded}"

		card = (
			f'<details class="cert-card">\n'
			f' <summary class="cert-summary">\n'
			f' <div class="cert-icon">{icon}</div>\n'
			f' <div class="cert-info">\n'
			f' <div class="cert-name">{name}</div>\n'
			f' <div class="cert-meta">\n'
			f' <span class="cert-platform">{platform}</span>\n'
			f' <span class="cert-sep">&#183;</span>\n'
			f' <span>{size}</span>\n'
			f' <span class="cert-sep">&#183;</span>\n'
			f' <span>{date}</span>\n'
			f' </div>\n'
			f' </div>\n'
			f' <div class="cert-toggle">&#9660;</div>\n'
			f' </summary>\n'
			f' <div class="cert-preview">\n'
			f' <embed src="{raw_url}" type="application/pdf" />\n'
			f' <div class="cert-footer">\n'
			f' <a href="{view_url}" target="_blank" class="cert-open-btn">\n'
			f' Open in GitHub &#8599;</a>\n'
			f' </div>\n'
			f' </div>\n'
			f'</details>'
		)
		cards.append(card)

	card_grid = "\n".join(cards)

	total = len(pdf_files)
	updated = datetime.now().strftime("%B %Y")

	readme = f"""# 🎓 My Certificates

> A curated collection of all my professional certificates, courses, and achievements.

![Visitors](https://img.shields.io/badge/Certificates-{total}-blue?style=for-the-badge)
![Last Updated](https://img.shields.io/badge/Updated-{updated}-green?style=for-the-badge)

---

## 📂 All Certificates ({total} total) — click any row to preview

<!-- CSS -->
<style>
.cert-card {{
 background: #161b22;
 border: 1px solid #30363d;
 border-radius: 10px;
 margin-bottom: 10px;
 overflow: hidden;
 transition: border-color 0.2s;
}}
.cert-card:hover {{
 border-color: #58a6ff;
}}
.cert-card summary {{
 list-style: none;
 display: flex;
 align-items: center;
 gap: 14px;
 padding: 14px 18px;
 cursor: pointer;
 user-select: none;
}}
.cert-card summary::-webkit-details-marker {{ display: none; }}
.cert-card summary::before {{ display: none; }}
.cert-icon {{
 font-size: 26px;
 flex-shrink: 0;
 width: 40px;
 text-align: center;
}}
.cert-info {{
 flex: 1;
 min-width: 0;
}}
.cert-name {{
 font-size: 15px;
 font-weight: 600;
 color: #e6edf3;
 margin-bottom: 4px;
 white-space: nowrap;
 overflow: hidden;
 text-overflow: ellipsis;
}}
.cert-meta {{
 font-size: 12px;
 color: #8b949e;
 display: flex;
 gap: 6px;
 align-items: center;
 flex-wrap: wrap;
}}
.cert-platform {{
 background: #1f6feb22;
 color: #58a6ff;
 padding: 1px 8px;
 border-radius: 20px;
 font-weight: 500;
}}
.cert-sep {{ color: #484f58; }}
.cert-toggle {{
 font-size: 11px;
 color: #8b949e;
 flex-shrink: 0;
 transition: transform 0.2s;
}}
.cert-card[open] .cert-toggle {{ transform: rotate(180deg); }}
.cert-preview {{
 border-top: 1px solid #30363d;
 background: #0d1117;
}}
.cert-preview embed {{
 width: 100%;
 height: 620px;
 border: none;
 display: block;
}}
.cert-footer {{
 padding: 10px 18px;
 border-top: 1px solid #21262d;
 text-align: right;
}}
.cert-open-btn {{
 font-size: 12px;
 color: #58a6ff;
 text-decoration: none;
 font-weight: 500;
}}
.cert-open-btn:hover {{ text-decoration: underline; }}
</style>

<!-- CERT_GRID_START -->
{card_grid}
<!-- CERT_GRID_END -->

---

*<em>Auto-updated by GitHub Actions &middot; Last refresh: {updated}</em>*
"""

	readme_path = REPO_DIR / "README.md"
	readme_path.write_text(readme, encoding="utf-8")
	print(f"README.md written with {total} certificates")

if __name__ == "__main__":
	build_readme()