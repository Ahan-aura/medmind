from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.assistant import AssistantChatRequest, AssistantChatResponse, StarterPromptsResponse
from app.services.assistant import ask_assistant, get_starter_prompts
from app.security import get_current_user
from app.limiter import limiter
from slowapi.util import get_remote_address
import logging

logger = logging.getLogger("medmind.assistant")

router = APIRouter(prefix="/assistant", tags=["assistant"])

def get_assistant_limiter_key(request: Request) -> str:
    auth = request.headers.get("authorization", "")
    ip = get_remote_address(request)
    return f"assistant:{auth}:{ip}"

@router.post("/chat", response_model=AssistantChatResponse)
@limiter.limit("30/minute", key_func=get_assistant_limiter_key)
def chat_assistant(
    request: Request,
    payload: AssistantChatRequest,
    current_user = Depends(get_current_user)
):
    try:
        response = ask_assistant(payload)
        return response
    except Exception as e:
        logger.error("Error in chat_assistant: %s", e)
        raise HTTPException(status_code=500, detail=f"Assistant processing error: {str(e)}")

@router.get("/prompts", response_model=StarterPromptsResponse)
def starter_prompts(
    current_user = Depends(get_current_user)
):
    return get_starter_prompts()
