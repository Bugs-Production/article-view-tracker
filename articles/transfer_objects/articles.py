from dataclasses import dataclass


@dataclass
class ArticleDTO:
    id: int
    user_id: int
    title: str
    content: str
    created_at: str
