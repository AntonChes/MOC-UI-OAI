from flask import Blueprint, jsonify


check_tasks_bp = Blueprint('check_tasks_bp', __name__)


@check_tasks_bp.route("/tasks/<job_id>", methods=["GET"])
def get_task_status(job_id):
    from celery.result import AsyncResult

    task_result = AsyncResult(job_id)
    result = {
        "job_id": job_id,
        "task_status": task_result.status,
        "task_name": task_result.name,
        "task_result": str(task_result.result)
    }
    
    # hanlde FileNotFoundError error
    if isinstance(result['task_result'], FileNotFoundError):
        return jsonify({
            "error": task_result.result.strerror
        }), 400

    return jsonify({"status": result}), 200