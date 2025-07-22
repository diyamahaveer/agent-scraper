from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)


#come edit if needed but this works 

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Therapist:
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    email_found: Optional[str] = None
    phone_found: Optional[str] = None
    profile_url: Optional[str] = None
    extra_info: Optional[dict] = None

@dataclass
class ScrapeTaskResult:
    status: str
    data: Optional[List[Therapist]] = None
    error: Optional[str] = None