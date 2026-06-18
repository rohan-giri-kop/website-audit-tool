from pydantic import BaseModel


class FindingRead(BaseModel):
    id: int
    category: str
    issue: str
    recommendation: str
    priority: str
    benefit: str = ""

    model_config = {"from_attributes": True}
