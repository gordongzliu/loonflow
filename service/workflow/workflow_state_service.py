from django.db.models import QuerySet

from apps.workflow.models import State
from service.base_service import BaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.common.log_service import auto_log


class WorkflowStateService(BaseService):
    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_workflow_states(workflow_id):
        """
        获取流程的状态列表，每个流程的state不会很多，所以不分页
        :param self:
        :param workflow_id:
        :return:
        """
        if not workflow_id:
            return False, 'except workflow_id but not provided'
        else:
            workflow_states = State.objects.filter(workflow_id=workflow_id, is_deleted=False)
            return workflow_states, ''

    @staticmethod
    @auto_log
    def get_workflow_state_by_id(state_id):
        """
        获取state详情
        :param self:
        :param state_id:
        :return:
        """
        if not state_id:
            return False, 'except state_id but not provided'
        else:
            workflow_state = State.objects.filter(id=state_id, is_deleted=False).first()
            if not workflow_state:
                return False, '工单状态不存在或已被删除'
            return workflow_state, ''

    @classmethod
    @auto_log
    def get_workflow_start_state(cls, workflow_id):
        """
        获取工作流初始状态
        :param workflow_id:
        :return:
        """
        workflow_state_queryset = State.objects.filter(is_deleted=0, workflow_id=workflow_id).all()
        for workflow_state in workflow_state_queryset:
            if workflow_state.type_id == CONSTANT_SERVICE.STATE_TYPE_START:
                return workflow_state, ''
        return False, '该工作流未配置初始状态，请检查工作流配置'

