from celery import Celery
from models import SessionLocal, KnowledgeTask
import time
import os

# 使用 Redis 作为消息队列
# 建议在环境变量中配置，此处为本地默认值
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app = Celery('agent_worker', broker=REDIS_URL)

@app.task
def process_document_pipeline(task_id, raw_text):
    db = SessionLocal()
    task = db.query(KnowledgeTask).filter(KnowledgeTask.id == task_id).first()
    
    try:
        # Agent 1: 文档结构化解析 (模拟长链条推理过程)
        print(f"Agent 1 正在解析任务 {task_id}...")
        time.sleep(3) 
        md_content = f"### 结构化商业笔记\n\n**核心摘要**: {raw_text[:50]}...\n\n**标签**: #一人公司 #供应链 #自动化"
        
        # Agent 2: 关键动作提取与逻辑推演
        print(f"Agent 2 正在提取动作...")
        time.sleep(3)
        action_items = "- [ ] 基于文档完成供应链风险评估\n- [ ] 同步至 Obsidian Canvas 脑图"
        
        # Agent 3: 外部系统同步占位 (飞书/企微 Webhook)
        print(f"Agent 3 正在同步外部系统状态...")
        # requests.post(WEBHOOK_URL, json=...) 
        
        # 更新数据库状态
        task.status = "completed"
        task.md_content = md_content
        task.action_items = action_items
        db.commit()
        print(f"任务 {task_id} 处理成功。")
    except Exception as e:
        print(f"任务 {task_id} 失败: {str(e)}")
        task.status = "failed"
        db.commit()
    finally:
        db.close()