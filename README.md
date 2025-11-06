# 🚀 AutoLinkedAI — Automated LinkedIn Content Creator and Publisher

AutoLinkedAI is an intelligent workflow-based system that **automatically generates, reviews, enhances, and posts LinkedIn content** using AI agents built with **LangGraph**, **OpenAI GPT-4o**, and **Gemini API**.  
It streamlines the entire process — from topic generation to LinkedIn publishing and MongoDB storage.

---

## 👨‍💻 Developed By
**Vipun Sanjana**  
B.Sc. (Software Engineering) Hon's (University of Kelaniya)  
Software Engineer | AI & Automation Enthusiast  
📧 Email: vipunsanjana@gmail.com  
🌐 GitHub: [vipunsanjana](https://github.com/vipunsanjana)

---

## 🧩 Key Features

- 🤖 **AI-Generated Content** — Uses OpenAI GPT-4o to generate post topics and engaging LinkedIn content.  
- 🧠 **Smart Review Cycle** — Automatically reviews and improves drafts until approved.  
- 🖼️ **AI Image Generation** — Creates contextual images using Gemini API.  
- 🔗 **LinkedIn Automation** — Publishes posts directly to LinkedIn with asset URN support.  
- 💾 **Post Archival** — Saves post details in MongoDB for recordkeeping.  
- 🧱 **LangGraph Workflow** — Modular, node-based AI workflow with transparent execution and retries.

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| AI & NLP | OpenAI GPT-4o |
| Image Generation | Google Gemini API |
| Workflow Engine | LangGraph |
| Backend | Python |
| Database | MongoDB |
| Logging | Custom Logger with Rotation |

---

## 📁 Project Structure

```
AutoLinkedAI/
│
├── client/                               # 💻 Frontend (React + Vite + TypeScript + Tailwind CSS)
│   ├── dist/                             # Compiled production build files
│   ├── node_modules/                     # Frontend dependencies
│   ├── src/                              # Application source code
│   │   ├── assets/                       # Images, icons, and static assets
│   │   ├── components/                   # Reusable UI components
│   │   ├── pages/                        # Page-level components
│   │   ├── App.tsx                       # Main app component
│   │   └── main.tsx                      # Entry point for React app
│   ├── .env                              # Client environment variables (e.g., VITE_API_URL)
│   ├── .gitignore                        # Git ignore rules for client
│   ├── eslint.config.js                  # ESLint configuration for linting
│   ├── index.html                        # Root HTML template
│   ├── package-lock.json                 # Locked dependency tree
│   ├── package.json                      # Project metadata and scripts
│   ├── postcss.config.js                 # PostCSS configuration
│   ├── tailwind.config.js                # Tailwind CSS configuration
│   ├── tsconfig.app.json                 # TypeScript configuration (App scope)
│   ├── tsconfig.json                     # Base TypeScript configuration
│   ├── tsconfig.node.json                # TypeScript config for Node/Vite environment
│   └── vite.config.ts                    # Vite build and dev configuration
│
├── server/                               # ⚙️ Backend (FastAPI + LangGraph + Gemini + MongoDB + LinkedIn API)
│   ├── app/
│   │   ├── main.py                       # FastAPI application entry point
│   │   ├── models/
│   │   │   └── agent.py                  # AgentState and Post models (Pydantic)
│   │   ├── services/
│   │   │   ├── agent_graph.py            # LangGraph workflow orchestration
│   │   │   ├── linkedin_service.py       # LinkedIn automation and posting logic
│   │   │   ├── gemini_service.py         # Google Gemini image/content generation
│   │   │   └── mongodb_service.py        # MongoDB persistence and retrieval
│   │   ├── utils/
│   │   │   ├── config.py                 # Configuration (API keys, constants)
│   │   │   └── logger.py                 # Centralized custom logger
│   │   └── __init__.py                   # Marks directory as a package
│   ├── logs/                             # Application log files
│   ├── venv/                             # Python virtual environment
│   ├── .env                              # Server environment variables (Mongo URI, API keys, etc.)
│   ├── requirements.txt                  # Python dependency list
│   └── .gitignore                        # Git ignore rules for server
│
└── README.md                             # 📘 Project documentation

````

---

## 🔑 Environment Variables (`.env`)

```bash
OPENAI_API_KEY=your_openai_api_key_here
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_PERSON_URN=urn:li:person:xxxxxxxxxxxx
POST_NICHE=Artificial Intelligence
GEMINI_API_KEY=your_gemini_api_key
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net
````

---

## 🧰 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/vipunsanjana/AutoLinkedAI.git
   cd AutoLinkedAI
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment**

   ```bash
   cp .env.example .env
   # Add your API keys and LinkedIn URN
   ```

---

## 🚀 Run the Agent

```bash
python app/main.py
```

Example output:

```
2025-10-29 21:55:57,653 | INFO | app.services.agent_graph | ✅ Agent graph compiled successfully.
2025-10-29 21:55:57,653 | INFO | __main__ | 🚀 Starting workflow for niche: Artificial Intelligence
2025-10-29 21:55:57,653 | INFO | __main__ | 🎯 Workflow finished successfully.
```

---

## 🕒 Automate Daily Posting (Cron Job Example)

**Linux/macOS:**

```bash
0 9 * * * /usr/bin/python3 /path/to/AutoLinkedAI/app/main.py >> /path/to/AutoLinkedAI/logs/cron.log 2>&1
```

**Windows (Task Scheduler):**

* Create a task that runs `python app\main.py` daily at a specific time.

---

## 🧩 Future Enhancements

* Add Comment Monitoring Workflow
* Integrate with Twitter and Facebook
* Dashboard for analytics (React + FastAPI)
* Custom AI tone/style selection

---

## 💬 Contact

For collaborations, issues, or enhancements — feel free to connect!
📧 [vipunsanjana@gmail.com](mailto:vipunsanjana@gmail.com) | 🌐 [GitHub Profile](https://github.com/vipunsanjana)

---
