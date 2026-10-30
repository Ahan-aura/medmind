from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., pattern=r'^(user|assistant|system)$')
    content: str = Field(..., min_length=1)

class AssistantChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    history: Optional[List[ChatMessage]] = Field(default_factory=list)

class AssistantCitation(BaseModel):
    ref_id: str
    source_title: str
    quote: Optional[str] = None
    relevance: Optional[str] = None

class RecommendedLessonItem(BaseModel):
    id: str
    title: str

class AssistantChatResponse(BaseModel):
    reply: str
    citations: List[AssistantCitation] = Field(default_factory=list)
    suggested_questions: List[str] = Field(default_factory=list)
    recommended_lessons: List[RecommendedLessonItem] = Field(default_factory=list)
    model: str
    disclaimer: str = "Educational simulation only. Not medical advice. Never for real patient management."

class StarterPromptGroup(BaseModel):
    category: str
    description: str
    prompts: List[str]

class StarterPromptsResponse(BaseModel):
    groups: List[StarterPromptGroup]
