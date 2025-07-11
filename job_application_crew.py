#!/usr/bin/env python3
"""
Job Application Crew with Ollama
Simplified version following the exact CrewAI pattern
"""

import os
import json
import warnings
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

# Warning control (like the original)
warnings.filterwarnings('ignore')

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "mistral"


@dataclass
class Agent:
    """Agent class following CrewAI pattern"""
    role: str
    goal: str
    backstory: str
    tools: List[str] = None
    verbose: bool = True


@dataclass
class Task:
    """Task class following CrewAI pattern"""
    description: str
    expected_output: str
    agent: Agent
    context: List[str] = None
    output_file: str = None
    async_execution: bool = False


class OllamaLLM:
    """Simple Ollama client"""

    def __init__(self, model: str = MODEL_NAME):
        self.model = model
        self.base_url = OLLAMA_BASE_URL

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response using requests (no extra dependencies)"""
        try:
            import requests

            url = f"{self.base_url}/api/generate"
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            }

            if system_prompt:
                data["system"] = system_prompt

            response = requests.post(url, json=data, timeout=120)
            response.raise_for_status()
            return response.json()["response"]

        except Exception as e:
            return f"Error generating response: {e}"


class SimpleTools:
    """Simple tool implementations without external dependencies"""

    @staticmethod
    def scrape_website(url: str) -> str:
        """Simple web scraping using only requests"""
        try:
            import requests

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Simple text extraction (no BeautifulSoup needed)
            content = response.text

            # Remove HTML tags using simple string replacement
            import re
            content = re.sub(r'<[^>]+>', ' ', content)
            content = re.sub(r'\s+', ' ', content)

            return content[:5000]  # Limit content length

        except Exception as e:
            return f"Error scraping website: {e}"

    @staticmethod
    def read_file(file_path: str) -> str:
        """Read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    @staticmethod
    def search_web(query: str) -> str:
        """Simulate web search (placeholder)"""
        return f"Search results for: {query}\n[This is a placeholder for web search functionality]"


class Crew:
    """Main Crew class following CrewAI pattern"""

    def __init__(self, agents: List[Agent], tasks: List[Task], verbose: bool = True):
        self.agents = agents
        self.tasks = tasks
        self.verbose = verbose
        self.llm = OllamaLLM()
        self.tools = SimpleTools()
        self.results = {}

    def kickoff(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the crew workflow"""

        if self.verbose:
            print("\n" + "=" * 60)
            print("🚀 STARTING JOB APPLICATION CREW")
            print("=" * 60)
            print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🎯 Job URL: {inputs.get('job_posting_url', 'N/A')}")
            print(f"👤 GitHub: {inputs.get('github_url', 'N/A')}")

        # Execute tasks in order
        for task in self.tasks:
            self._execute_task(task, inputs)

        if self.verbose:
            print("\n" + "=" * 60)
            print("🎉 CREW EXECUTION COMPLETED!")
            print("=" * 60)

        return self.results

    def _execute_task(self, task: Task, inputs: Dict[str, Any]) -> str:
        """Execute a single task"""

        if self.verbose:
            print(f"\n{'=' * 60}")
            print(f"🤖 AGENT: {task.agent.role}")
            print(f"🎯 GOAL: {task.agent.goal}")
            print(f"📋 TASK: {task.description}")
            print(f"🛠️  TOOLS: {', '.join(task.agent.tools or [])}")
            print(f"{'=' * 60}")

        # Build context from previous tasks
        context_info = ""
        if task.context:
            context_info = "\n\nPrevious Results:\n"
            for ctx_task in task.context:
                if ctx_task in self.results:
                    context_info += f"\n{ctx_task.upper()}:\n{self.results[ctx_task]}\n"

        # Build system prompt
        system_prompt = f"""You are a {task.agent.role}.

Background: {task.agent.backstory}

Your goal: {task.agent.goal}

Available tools: {', '.join(task.agent.tools or [])}

You must provide detailed, professional analysis and recommendations. 
Be thorough and explain your reasoning step by step."""

        # Build main prompt with job-specific information
        main_prompt = f"""TASK: {task.description}

EXPECTED OUTPUT: {task.expected_output}

INPUT DATA:
- Job Posting URL: {inputs.get('job_posting_url', 'N/A')}
- GitHub URL: {inputs.get('github_url', 'N/A')} 
- Personal Write-up: {inputs.get('personal_writeup', 'N/A')}

{context_info}

INSTRUCTIONS:
1. Analyze the provided information thoroughly
2. Use your expertise in {task.agent.role} to provide insights
3. Focus on actionable recommendations
4. Show your reasoning process
5. Provide specific, detailed output as requested

Begin your analysis:"""

        # Add specific tool usage based on agent role
        if "researcher" in task.agent.role.lower() and inputs.get('job_posting_url'):
            if self.verbose:
                print("🌐 Scraping job posting...")
            job_content = self.tools.scrape_website(inputs['job_posting_url'])
            main_prompt += f"\n\nJOB POSTING CONTENT:\n{job_content}"

        if "profiler" in task.agent.role.lower() and inputs.get('github_url'):
            if self.verbose:
                print("🔍 Analyzing GitHub profile...")
            # Simplified GitHub analysis
            github_info = f"GitHub Profile: {inputs['github_url']}\n[Analysis would include repository overview, commit activity, and technical skills based on projects]"
            main_prompt += f"\n\nGITHUB ANALYSIS:\n{github_info}"

        if self.verbose:
            print("🧠 THINKING...")
            print("💭 Generating response...")

        # Generate response
        response = self.llm.generate(main_prompt, system_prompt)

        if self.verbose:
            print(f"\n✅ AGENT RESPONSE:")
            print("-" * 40)
            print(response)
            print("-" * 40)

        # Store result
        task_key = task.agent.role.lower().replace(" ", "_").replace("for_engineers", "").replace("engineering_", "")
        self.results[task_key] = response

        # Save to file if specified
        if task.output_file:
            self._save_output(task, response)

        return response

    def _save_output(self, task: Task, content: str):
        """Save output to file"""
        try:
            with open(task.output_file, 'w', encoding='utf-8') as f:
                f.write(f"# {task.agent.role} Output\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(content)

            if self.verbose:
                print(f"💾 Output saved to: {task.output_file}")
        except Exception as e:
            if self.verbose:
                print(f"❌ Error saving file: {e}")


def main():
    """Main function following the original CrewAI pattern"""

    print("🔧 Job Application Crew with Ollama")
    print("Following CrewAI pattern with qwen2.5:7b")
    print("=" * 50)

    # Check Ollama connection
    try:
        import requests
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Ollama not running. Please start with: ollama serve")
            return
        print("✅ Ollama connected successfully")
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return

    # Creating Agents (following original pattern)
    researcher = Agent(
        role="Tech Job Researcher",
        goal="Make sure to do amazing analysis on job posting to help job applicants",
        tools=["scrape_tool", "search_tool"],
        verbose=True,
        backstory=(
            "As a Job Researcher, your prowess in "
            "navigating and extracting critical "
            "information from job postings is unmatched. "
            "Your skills help pinpoint the necessary "
            "qualifications and skills sought "
            "by employers, forming the foundation for "
            "effective application tailoring."
        )
    )

    profiler = Agent(
        role="Personal Profiler for Engineers",
        goal="Do incredible research on job applicants to help them stand out in the job market",
        tools=["scrape_tool", "search_tool", "read_resume", "semantic_search_resume"],
        verbose=True,
        backstory=(
            "Equipped with analytical prowess, you dissect "
            "and synthesize information "
            "from diverse sources to craft comprehensive "
            "personal and professional profiles, laying the "
            "groundwork for personalized resume enhancements."
        )
    )

    resume_strategist = Agent(
        role="Resume Strategist for Engineers",
        goal="Find all the best ways to make a resume stand out in the job market.",
        tools=["scrape_tool", "search_tool", "read_resume", "semantic_search_resume"],
        verbose=True,
        backstory=(
            "With a strategic mind and an eye for detail, you "
            "excel at refining resumes to highlight the most "
            "relevant skills and experiences, ensuring they "
            "resonate perfectly with the job's requirements."
        )
    )

    interview_preparer = Agent(
        role="Engineering Interview Preparer",
        goal="Create interview questions and talking points based on the resume and job requirements",
        tools=["scrape_tool", "search_tool", "read_resume", "semantic_search_resume"],
        verbose=True,
        backstory=(
            "Your role is crucial in anticipating the dynamics of "
            "interviews. With your ability to formulate key questions "
            "and talking points, you prepare candidates for success, "
            "ensuring they can confidently address all aspects of the "
            "job they are applying for."
        )
    )

    # Creating Tasks (following original pattern)
    research_task = Task(
        description=(
            "Analyze the job posting URL provided ({job_posting_url}) "
            "to extract key skills, experiences, and qualifications "
            "required. Use the tools to gather content and identify "
            "and categorize the requirements."
        ),
        expected_output=(
            "A structured list of job requirements, including necessary "
            "skills, qualifications, and experiences."
        ),
        agent=researcher,
        async_execution=True
    )

    profile_task = Task(
        description=(
            "Compile a detailed personal and professional profile "
            "using the GitHub ({github_url}) URLs, and personal write-up "
            "({personal_writeup}). Utilize tools to extract and "
            "synthesize information from these sources."
        ),
        expected_output=(
            "A comprehensive profile document that includes skills, "
            "project experiences, contributions, interests, and "
            "communication style."
        ),
        agent=profiler,
        async_execution=True
    )

    resume_strategy_task = Task(
        description=(
            "Using the profile and job requirements obtained from "
            "previous tasks, tailor the resume to highlight the most "
            "relevant areas. Employ tools to adjust and enhance the "
            "resume content. Make sure this is the best resume even but "
            "don't make up any information. Update every section, "
            "including the initial summary, work experience, skills, "
            "and education. All to better reflect the candidates "
            "abilities and how it matches the job posting."
        ),
        expected_output=(
            "An updated resume that effectively highlights the candidate's "
            "qualifications and experiences relevant to the job."
        ),
        output_file="tailored_resume.md",
        context=["research_task", "profile_task"],
        agent=resume_strategist
    )

    interview_preparation_task = Task(
        description=(
            "Create a set of potential interview questions and talking "
            "points based on the tailored resume and job requirements. "
            "Utilize tools to generate relevant questions and discussion "
            "points. Make sure to use these questions and talking points to "
            "help the candidate highlight the main points of the resume "
            "and how it matches the job posting."
        ),
        expected_output=(
            "A document containing key questions and talking points "
            "that the candidate should prepare for the initial interview."
        ),
        output_file="interview_materials.md",
        context=["research_task", "profile_task", "resume_strategy_task"],
        agent=interview_preparer
    )

    # Creating the Crew (following original pattern)
    job_application_crew = Crew(
        agents=[researcher, profiler, resume_strategist, interview_preparer],
        tasks=[research_task, profile_task, resume_strategy_task, interview_preparation_task],
        verbose=True
    )

    # Running the Crew (following original pattern)
    job_application_inputs = {
        'job_posting_url': 'https://jobs.lever.co/AIFund/b9cd61ea-cae1-411a-987f-ea40ea6f7db8',
        'github_url': 'https://github.com/joaomdmoura',
        'personal_writeup': """Noah is an accomplished Software
        Engineering Leader with 18 years of experience, specializing in
        managing remote and in-office teams, and expert in multiple
        programming languages and frameworks. He holds an MBA and a strong
        background in AI and data science. Noah has successfully led
        major tech initiatives and startups, proving his ability to drive
        innovation and growth in the tech industry. Ideal for leadership
        roles that require a strategic and innovative approach."""
    }

    print("\n📋 Job Application Inputs:")
    for key, value in job_application_inputs.items():
        print(f"  {key}: {str(value)[:100]}...")

    # Execute the crew
    result = job_application_crew.kickoff(inputs=job_application_inputs)

    # Display results like the original
    print("\n📈 EXECUTION SUMMARY:")
    print("=" * 50)

    if os.path.exists("tailored_resume.md"):
        print("✅ tailored_resume.md generated")
    if os.path.exists("interview_materials.md"):
        print("✅ interview_materials.md generated")

    print("\n🎉 CONGRATULATIONS! Job application materials generated successfully!")
    print("Check the generated files:")
    print("- tailored_resume.md")
    print("- interview_materials.md")


if __name__ == "__main__":
    main()