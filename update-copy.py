"""Keep website FAQ text and structured data aligned after feature changes."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FAQ = {
  "Does image OCR need an online service?": "No. The development build bundles an English OCR engine and recognition data. Read project images or import an image into Knowledge without an online OCR account or Windows language-pack setup. PNG, JPEG, BMP and TIFF are supported; only the first frame of a multi-page image is read. Recognition can be wrong, so verify important text.",
  "When can I download Offline Coder?": "Offline Coder is coming soon. This website previews the development build; public downloads and the final price will be announced at launch. Optional service connections still need live account validation and applicable Google verification before release.",
  "Is it a private, offline alternative to ChatGPT or Copilot?": "For everyday coding help, the development build provides local chat, project search, proposed edits and approved commands. Local inference stays on your PC. Optional research, connected services and commands that use the network can communicate online. Smaller local models can require more steps and review for complex work.",
  "Why does Windows SmartScreen show a warning?": "The development executable is not code-signed yet, so Windows can show a publisher or reputation warning. Signing and distribution are still being prepared. Public downloads will open at launch; use only the official download link announced here.",
  "How do updates work?": "The development build checks this website once a day for a newer version and opens the official download page when an update is announced. Nothing is installed automatically. Public release downloads are coming soon.",
  "Does Offline Coder really work without the internet?": "Yes. After the required model and voice downloads, chat, code search, file edits, tutoring and local instruction packs run on your PC without internet. Downloads, update checks, online research and optional service connections use the network. Optional connections start disabled.",
  "Is my code or chat history sent anywhere?": "The AI model runs locally, and projects, chats and imported knowledge are stored on your PC. Online research sends search queries to its provider; enabled extensions communicate with the service you connect. Retrieved content is processed by the local model. Connection credentials are encrypted for your Windows account and are not supplied as credentials to the model. Approved commands run with your Windows account and may use the network.",
  "Can the assistant change my files without asking?": "By default it previews edits and commands and waits for approval, except commands on your project's allowed list. Approvals have no countdown and return after a page refresh while the app remains open. Allow Auto-Approval is an optional per-project setting for reversible file edits and detected tests plus exact configured build/check commands. Deletions, moves, commits and other unrestricted commands still ask. File changes are backed up; commands can affect your PC and should be trusted.",
  "Can the assistant send emails on its own?": "No. Gmail and advanced IMAP/SMTP connections can search, read, summarize and prepare drafts; the Outlook extension currently reads mail only. Sending requires your Send button and confirmation of the recipients, subject and body. Project Auto-Approval does not authorize email sending. External emails are treated as untrusted content.",
  "How do extensions connect?": "The development build includes twelve connection adapters and sixteen local instruction packs, grouped by specialty. Gmail, Google Drive and Google Calendar use browser-based Google sign-in after the app's Google registration is configured. GitHub, GitLab, Notion, Slack, Dropbox, OneDrive and Outlook currently use service access tokens with the required permissions. Tokens stay encrypted on this PC. Live account validation and Google verification remain release requirements; instruction packs work offline. Local Ghidra inspection requires separately installed Ghidra/GhidraMCP. Local MCP connects to one reviewed local HTTP server, with approval for every tool invocation even in Auto-Approval projects.",
  "Are the specialist roles separate expert models?": "No. The 82 roles guide your selected local model using focused instructions. Auto chooses a role locally, without an extra routing model call. A specialist consultation makes one additional model call with the supplied context. Responses depend on the model and information available; advanced or practical work may need current references or qualified review.",
  "Can I save, archive or delete chats?": "The development build saves chats on your PC, separately by project and for general conversations. Titles are generated locally from the chat topic and can be renamed. New chat keeps earlier conversations. Search titles, reopen, archive and restore from Chats. Permanent deletion asks for confirmation. Conversations do not sync to a cloud account.",
  "Are settings grouped into tabs?": "Yes. Assistant, Models & speed, Knowledge, Extensions, Connections, Appearance and Updates each have their own category tab. Switching categories preserves input values, and shortcuts open the relevant category.",
  "Do specialists use the built-in tools automatically?": "The built-in search, outline, syntax, Python lint/type and OCR tools are available when project tools are on, which is the default for opened projects. Specialists are instructed to choose relevant tools without another toggle. Knowledge imports build local meaning search automatically in the background. Model tool choice and diagnostics can still need review. Optional service connections need setup; every Local MCP invocation requires approval, including in Auto-Approval projects."
}
description = "Coming soon: Offline Coder for Windows, with local coding, learning and practical guidance, 82 specialist roles, categorized extensions and optional project Auto-Approval."
path = ROOT / "index.html"
page = path.read_text(encoding="utf-8")
for key in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
    page = re.sub(r'(<meta ' + re.escape(key) + r' content=")[^"]*(">)', lambda m: m[1] + html.escape(description, quote=True) + m[2], page, count=1)
match = re.search(r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)', page)
data = json.loads(match[2])
software = next(item for item in data["@graph"] if item["@type"] == "SoftwareApplication")
software["description"] = description
software["softwareVersion"] = "1.0.0-development"
software["featureList"] = [
    "Local AI chat and project tools",
    "Locally saved chats with automatic topic titles, search, rename, archive, restore and confirmed deletion",
    "Seven categorized Settings tabs with immediate switching and retained input values",
    "82 categorized specialist roles for coding, learning, science, arts, practical skills, health education and animal care",
    "Offline Crisis help panel independent of model inference; limited English urgent self-harm phrase response",
    "Local Auto routing without another model call",
    "Approval requests without a countdown and recovery after refresh while the hub stays open",
    "Optional per-project Auto-Approval for reversible edits and test/build/check commands",
    "File backups and undo",
    "28 categorized extensions: twelve optional connection adapters and sixteen local instruction packs",
    "Importable instruction packs with no executable plug-in code",
    "Google sign-in prepared for Gmail, Drive and Calendar; app setup and live account checks required",
    "Encrypted local connection credentials; email sending requires human confirmation",
    "Automatic built-in tool guidance: fast project search, structural outlines, Python lint/type diagnostics and multi-language parsing",
    "Background local meaning search for imported notes and bundled English image OCR",
    "Reviewed local HTTP MCP tools with approval for every invocation",
    "Project code search, visible plans, project notes and focused checks",
    "Voice input, imported knowledge, themes and hardware tuning",
    "Background status checks and coalesced interface updates",
    "Repeated failure prevention and Python/PowerShell/JS/TS/C#/Java/Rust/Go proposal syntax checks"
]
software['screenshot'] = ['https://renegade-android.github.io/OfflineCoder/img/' + name for name in
    ['agent-summary.webp', 'settings-models.webp', 'saved-chats.webp', 'coding-tests.webp']]
faq_data = next(item for item in data["@graph"] if item["@type"] == "FAQPage")
known = {item["name"]: item for item in faq_data["mainEntity"]}
for question, answer in FAQ.items():
    if question in known:
        known[question]["acceptedAnswer"]["text"] = answer
    else:
        faq_data["mainEntity"].append({"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}})
page = page[:match.start(2)] + "\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n  " + page[match.end(2):]
details = []
for i, item in enumerate(faq_data["mainEntity"]):
    details.append('        <details' + (' open' if i == 0 else '') + '><summary><h3>' + html.escape(item["name"]) + '</h3></summary><p>' + html.escape(item["acceptedAnswer"]["text"]) + '</p></details>')
page = re.sub(r'(<div class="faq">)[\s\S]*?(      </div>)', lambda m: m[1] + "\n" + "\n".join(details) + "\n" + m[2], page, count=1)
page = page.replace("No cloud, no account, no subscription.", "Local AI, no cloud AI account, no subscription. Online connections are optional.")
path.write_text(page, encoding="utf-8")
print("Website copy and structured FAQ updated")

