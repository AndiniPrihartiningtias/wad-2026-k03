from fastapi import APIRouter, HTTPException, Query, Response, status

from app.data import sessions
from app.schemas import SessionCreate, SessionOut

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get("", response_model=list[SessionOut])
def get_sessions(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    search: str | None = None,
):
    filtered_sessions = sessions

    if search:
        keyword = search.lower()
        filtered_sessions = [
            session
            for session in sessions
            if keyword in session["book_title"].lower()
            or keyword in session["borrower_name"].lower()
        ]

    start = (page - 1) * limit
    end = start + limit

    return filtered_sessions[start:end]


@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: int):
    for session in sessions:
        if session["id"] == session_id:
            return session

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Session not found",
    )


@router.post(
    "",
    response_model=SessionOut,
    status_code=status.HTTP_201_CREATED,
)
def create_session(session_data: SessionCreate):
    from app import data

    new_session = {
        "id": data.next_id,
        "book_title": session_data.book_title,
        "borrower_name": session_data.borrower_name,
        "status": session_data.status,
    }

    sessions.append(new_session)
    data.next_id += 1

    return new_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int):
    for index, session in enumerate(sessions):
        if session["id"] == session_id:
            sessions.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Session not found",
    )