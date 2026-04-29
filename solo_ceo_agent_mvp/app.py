from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import SessionLocal, KnowledgeTask
from tasks import process_document_pipeline

app = FastAPI(title="Solo CEO Agent MVP Console")

class DocumentInput(BaseModel):
    file_name: str
    content: str

@app.post("/submit_task")
def submit_task(doc: DocumentInput):
    db = SessionLocal()
    try:
        # 1. 在 SQLite 中创建初始任务记录
        new_task = KnowledgeTask(file_name=doc.file_name)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        # 2. 异步分发给 Celery Worker (多智能体集群)
        process_document_pipeline.delay(new_task.id, doc.content)
        
        return {"status": "queued", "task_id": new_task.id, "message": "Agent集群已开始处理"}
    finally:
        db.close()

@app.get("/tasks")
def list_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(KnowledgeTask).order_by(KnowledgeTask.created_at.desc()).all()
        return tasks
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)