# Job Application Crew with Ollama (Simplified)

A multi-agent system for tailoring job applications using Ollama's qwen2.5:7b model. This version follows the exact CrewAI pattern from the original file but works with local Ollama instead of OpenAI.

## 🤖 The Crew

- **Tech Job Researcher**: Analyzes job postings to extract key requirements
- **Personal Profiler**: Researches candidate backgrounds and creates profiles  
- **Resume Strategist**: Tailors resumes to match job requirements
- **Interview Preparer**: Creates interview questions and talking points

## 🚀 Quick Start

### Prerequisites

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai/)
2. **Start Ollama**: 
   ```bash
   ollama serve
   ```
3. **Install the model**: 
   ```bash
   ollama pull qwen2.5:7b
   ```

### Installation (Windows/Linux/Mac)

1. **Create project folder**:
   ```bash
   mkdir job-crew
   cd job-crew
   ```

2. **Save the files**:
   - Copy `job_application_crew.py` to your folder
   - Copy `setup.py` to your folder

3. **Install dependencies** (only requests needed):
   ```bash
   pip install requests
   ```
   
   OR run the setup:
   ```bash
   python setup.py
   ```

### Running the Crew

```bash
python job_application_crew.py
```

## 📁 What You'll Get

The script will generate:
- `tailored_resume.md` - Customized resume for the job
- `interview_materials.md` - Interview questions and talking points

## 🎯 How It Works

The crew follows the exact same pattern as the original CrewAI implementation:

1. **Researcher Agent** scrapes and analyzes the job posting
2. **Profiler Agent** analyzes your GitHub and background
3. **Resume Strategist** creates a tailored resume using context from previous agents
4. **Interview Preparer** creates interview materials using all previous context

## 🔧 Customization

### Change Job Details

Edit these lines in `job_application_crew.py`:

```python
job_application_inputs = {
    'job_posting_url': 'YOUR_JOB_URL_HERE',
    'github_url': 'YOUR_GITHUB_URL_HERE', 
    'personal_writeup': """YOUR_BACKGROUND_HERE"""
}
```

### Different Models

Change the model in the script:
```python
MODEL_NAME = "llama2:7b"  # or any other Ollama model
```

Available models you can try:
- `qwen2.5:7b` (recommended)
- `llama2:7b`
- `codellama:7b`
- `mistral:7b`

## 🐛 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Check if Ollama is running
ollama serve

# In another terminal, test:
curl http://localhost:11434/api/tags
```

### "Model not found"
```bash
# Install the model
ollama pull qwen2.5:7b

# List available models
ollama list
```

### "Import Error"
```bash
# Install requests
pip install requests

# Or use the setup script
python setup.py
```

### Windows-specific issues
- Use `python` instead of `python3`
- Make sure Python is in your PATH
- If you get SSL errors, try: `pip install requests --trusted-host pypi.org --trusted-host pypi.python.org`

## 📊 Sample Output

The crew will show detailed output like this:

```
🚀 STARTING JOB APPLICATION CREW
============================================================
🤖 AGENT: Tech Job Researcher
🎯 GOAL: Make sure to do amazing analysis on job posting to help job applicants
📋 TASK: Analyze the job posting URL provided...
🛠️ TOOLS: scrape_tool, search_tool
============================================================
🌐 Scraping job posting...
🧠 THINKING...
💭 Generating response...

✅ AGENT RESPONSE:
----------------------------------------
Based on my analysis of the job posting, here are the key requirements:

TECHNICAL SKILLS REQUIRED:
- Python programming (3+ years)
- Machine Learning frameworks (TensorFlow, PyTorch)
- Cloud platforms (AWS, GCP)
- Database systems (SQL, NoSQL)
...
----------------------------------------
💾 Output saved to: tailored_resume.md

🤖 AGENT: Personal Profiler for Engineers
...
```

## 🔄 Batch Processing

To process multiple jobs, modify the script:

```python
jobs = [
    {
        'job_posting_url': 'https://company1.com/job1',
        'github_url': 'https://github.com/yourprofile',
        'personal_writeup': 'Your background...'
    },
    {
        'job_posting_url': 'https://company2.com/job2', 
        'github_url': 'https://github.com/yourprofile',
        'personal_writeup': 'Your background...'
    }
]

for i, job in enumerate(jobs):
    print(f"\n🔄 Processing job {i+1}...")
    result = job_application_crew.kickoff(inputs=job)
    # Rename output files
    os.rename('tailored_resume.md', f'resume_job_{i+1}.md')
    os.rename('interview_materials.md', f'interview_job_{i+1}.md')
```

## 📈 Performance Tips

1. **Good internet connection** - for web scraping
2. **Let Ollama warm up** - first run might be slower
3. **Check job URL accessibility** - some sites block scraping
4. **Use specific job URLs** - avoid generic company pages

## 🎨 Advanced Customization

### Add More Context

```python
# Add more context to resume_strategy_task
resume_strategy_task = Task(
    description="Your enhanced description...",
    expected_output="More detailed expected output...",
    context=["research_task", "profile_task", "additional_context"],
    agent=resume_strategist
)
```

### Modify Agent Behavior

```python
# Customize agent backstory
researcher = Agent(
    role="Tech Job Researcher",
    goal="Your custom goal...",
    backstory="Your enhanced backstory with specific focus areas...",
    tools=["scrape_tool", "search_tool"],
    verbose=True
)
```

## 🔍 Understanding the Process

Each agent builds on the previous one's work:

1. **Researcher** → Extracts job requirements
2. **Profiler** → Analyzes your background (uses personal_writeup + GitHub)
3. **Resume Strategist** → Matches your background to job requirements
4. **Interview Preparer** → Creates questions based on the matched resume

The `context` parameter ensures each agent has access to previous results.

## 📋 File Structure

```
job-crew/
├── job_application_crew.py    # Main script
├── setup.py                   # Setup script  
├── tailored_resume.md         # Generated resume
├── interview_materials.md     # Generated interview prep
└── README.md                  # This file
```

## 🎯 Tips for Better Results

1. **Use specific job URLs** - direct links to job postings work best
2. **Detailed personal writeup** - more context = better results
3. **Public GitHub profile** - make sure it's accessible
4. **Good job posting** - detailed job descriptions work better
5. **Be patient** - first run downloads the model and might take time

## 🤝 Support

If you encounter issues:

1. Check that Ollama is running: `ollama serve`
2. Verify the model is installed: `ollama list`
3. Test the API: `curl http://localhost:11434/api/tags`
4. Make sure requests is installed: `pip install requests`

