# Solo CEO Agent MVP

这是一个专为“一人公司”设计的自动化运营中台原型。

## 核心架构
1. **FastAPI**: 任务控制台，负责接收外部指令。
2. **Celery + Redis**: 多 Agent 异步调度中心。
3. **SQLite**: 轻量级本地数据库，存储任务状态与内化知识。

## 快速启动
1. **安装依赖**:
   `pip install -r requirements.txt`
2. **启动 Redis**:
   确保本地已安装并运行 `redis-server`。
3. **启动 Agent Worker (负责处理逻辑)**:
   `celery -A tasks worker --loglevel=info`
4. **启动 API 控制台**:
   `python app.py`
5. **使用**:
   访问 `http://localhost:8000/docs` 提交任务。