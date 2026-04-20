import json
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def check_escalation(context: str) -> dict:
    """
    Analyzes conversation context and returns escalation decision.
    
    Args:
        context: Enriched ticket information including category, urgency, text
        
    Returns:
        dict: {"escalate": bool, "reason": str}
    """
    try:
        system_prompt = """You are a customer support escalation expert. Your job is to analyze support tickets and decide if they need immediate human escalation."""
        
        user_prompt = f"""Analyze the following support ticket information and decide if it needs escalation to a human agent.

IMPORTANT: Reply with ONLY a JSON object. No explanation, no markdown, no code blocks.
Format: {{"escalate": true or false, "reason": "one clear sentence"}}

Ticket Information:
{context}"""
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        # Parse JSON response
        result = json.loads(content)
        
        return {
            "escalate": bool(result.get("escalate", False)),
            "reason": str(result.get("reason", "No reason provided"))
        }
        
    except json.JSONDecodeError as e:
        return {
            "escalate": False,
            "reason": f"JSON parsing error: {str(e)}"
        }
    except Exception as e:
        raise Exception(f"LLM service error: {str(e)}")
