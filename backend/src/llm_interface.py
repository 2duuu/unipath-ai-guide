"""
LLM integration for UniHub academic advising system.
Supports multiple LLM providers (OpenAI, Anthropic).
"""
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMInterface:
    """Interface for interacting with LLM providers."""
    
    def __init__(self, provider: str = "openai", model: str = "gpt-4"):
        """
        Initialize LLM interface.
        
        Args:
            provider: LLM provider ("openai" or "anthropic")
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo", "claude-3-opus")
        """
        self.provider = provider.lower()
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        
        # Get API keys from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        self._validate_setup()
    
    def _validate_setup(self):
        """Validate that necessary API keys are present."""
        if self.provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        elif self.provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def set_system_prompt(self, prompt: str):
        """Set the system prompt for the conversation."""
        self.conversation_history = [{"role": "system", "content": prompt}]
    
    def send_message(self, message: str) -> str:
        """
        Send a message to the LLM and get a response.
        
        Args:
            message: User message
            
        Returns:
            LLM response
        """
        self.conversation_history.append({"role": "user", "content": message})
        
        if self.provider == "openai":
            response = self._send_openai_message()
        elif self.provider == "anthropic":
            response = self._send_anthropic_message()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
    
    def _send_openai_message(self) -> str:
        """Send message using OpenAI API."""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except ImportError:
            return "OpenAI library not installed. Please run: pip install openai"
        except Exception as e:
            return f"Error communicating with OpenAI: {str(e)}"
    
    def _send_anthropic_message(self) -> str:
        """Send message using Anthropic API."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            
            # Anthropic requires system message separate
            system_message = next((msg["content"] for msg in self.conversation_history if msg["role"] == "system"), None)
            messages = [msg for msg in self.conversation_history if msg["role"] != "system"]
            
            response = client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=system_message,
                messages=messages
            )
            
            return response.content[0].text
        except ImportError:
            return "Anthropic library not installed. Please run: pip install anthropic"
        except Exception as e:
            return f"Error communicating with Anthropic: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history except system prompt."""
        system_prompts = [msg for msg in self.conversation_history if msg["role"] == "system"]
        self.conversation_history = system_prompts
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation."""
        if len(self.conversation_history) <= 1:
            return "No conversation yet."
        
        summary = []
        for msg in self.conversation_history:
            if msg["role"] == "user":
                summary.append(f"Student: {msg['content'][:100]}...")
            elif msg["role"] == "assistant":
                summary.append(f"Advisor: {msg['content'][:100]}...")
        
        return "\n".join(summary)


class AdvisorLLM:
    """High-level interface for academic advising with LLM."""
    
    def __init__(self, provider: str = "openai", model: str = "gpt-4"):
        self.llm = LLMInterface(provider, model)
    
    def start_interview(self) -> str:
        """Start an interview session."""
        from interview_system import InterviewSystem
        
        interview_system = InterviewSystem()
        prompt = interview_system.build_interview_prompt()
        self.llm.set_system_prompt(prompt)
        
        # Get initial greeting
        return self.llm.send_message("Hello! I'm ready to learn about my college options.")
    
    def continue_interview(self, user_message: str) -> str:
        """Continue the interview conversation."""
        return self.llm.send_message(user_message)
    
    def start_application_assistance(self, university_name: str) -> str:
        """Start application assistance for a specific university."""
        from university_database import UniversityDatabase
        from application_assistant import ApplicationAssistant
        
        db = UniversityDatabase()
        universities = db.get_all_universities()
        university = next((u for u in universities if u.name == university_name), None)
        
        if not university:
            return f"University '{university_name}' not found in database."
        
        assistant = ApplicationAssistant()
        prompt = assistant.generate_application_prompt_for_llm(university)
        self.llm.set_system_prompt(prompt)
        
        return self.llm.send_message(f"I want to apply to {university_name}. Can you help me?")
    
    def get_personalized_advice(self, context: str, question: str) -> str:
        """Get personalized advice based on context."""
        prompt = f"""You are an experienced college admissions advisor.

Context: {context}

Provide thoughtful, personalized advice to help the student with their question. Be encouraging, specific, and actionable."""
        
        self.llm.set_system_prompt(prompt)
        return self.llm.send_message(question)
