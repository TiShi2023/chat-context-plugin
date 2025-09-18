import json
from collections import deque

from apscheduler.schedulers.background import BackgroundScheduler
from omni_bot_sdk.plugins.interface import (
    Bot,
    Plugin,
    PluginExcuteContext,
    MessageType,
)
from pydantic import BaseModel

from dingtalk_v2 import *
from .utils import get_color

class ChatContextPluginConfig(BaseModel):
    """
    上下文插件配置
    enabled: 是否启用该插件
    priority: 插件优先级，数值越大优先级越高
    """

    enabled: bool = False
    priority: int = 1001
    clean_crontab: str = "0 0 * * *"  # 每天凌晨清理一次
    max_session_length: int = 50

    ding_app_key: str = "unknown"
    ding_app_secret: str = "unknown"
    union_id: str = "unknown"
    workbook_id: str = "unknown"


class ChatContextPlugin(Plugin):
    """
    消息上下文插件实现类
    """

    priority = 1001
    name = "chat-context-plugin"

    def __init__(self, bot: "Bot"):
        super().__init__(bot)
        self.session_messages = {}
        self.user = bot.user_info
        # 动态优先级支持
        self.priority = getattr(self.plugin_config, "priority", self.__class__.priority)
        self.register_clean_crontab()

        self.max_session_length = self.plugin_config.max_session_length

        self.access_token = ''
        self.ding_app_key = self.plugin_config.ding_app_key
        self.ding_app_secret = self.plugin_config.ding_app_secret
        self.union_id = self.plugin_config.union_id
        self.workbook_id = self.plugin_config.workbook_id
        self.oauth = Oauth(
            app_key=self.ding_app_key,
            app_secret=self.ding_app_secret
        )
        self.register_crontab(self.update_token, "0 */2 * * *", True)  # 每2小时更新一次 token
        self.sheet = Sheet()
        self.sheet_list = list_sheets(self.access_token, self.union_id, self.workbook_id, self.sheet)
        self.sessions_for_sheet = {}

    def update_token(self):
        resp = self.oauth.main()
        self.access_token = resp['accessToken']

    def register_crontab(self, function: callable, cron_expression: str, run_now: bool = False):
        """
        注册定时任务
        :param function: 定时任务函数
        :param cron_expression: cron 表达式
        :param run_now: 是否立即执行一次
        """
        if run_now:
            function()
        scheduler = BackgroundScheduler()
        configs = cron_expression.split()
        scheduler.add_job(
            function,
            "cron",
            hour=configs[1],
            minute=configs[0],
            day=configs[2],
            month=configs[3],
            day_of_week=configs[4],
        )
        scheduler.start()
        self.logger.info(
            f"已注册定时任务，{function} 计划时间: {configs}"
        )

    def register_clean_crontab(self):
        """
        定时清理过期的会话消息
        """
        if self.plugin_config.clean_crontab:
            configs = self.plugin_config.clean_crontab.split()
        else:
            configs = ["0", "0", "*", "*", "*"]  # 默认每天凌晨清理一次
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            self.clean_expired_sessions,
            "cron",
            hour=configs[1],
            minute=configs[0],
            day=configs[2],
            month=configs[3],
            day_of_week=configs[4],
        )
        scheduler.start()
        self.logger.info(
            f"已注册定时任务，清理过期会话消息，计划时间: {self.plugin_config.clean_crontab}"
        )

    def save_sessions_to_sheet(self):
        """
        将当前会话消息保存到钉钉表格中
        """
        if not self.sessions_for_sheet:
            self.logger.info("当前没有会话消息，无需保存到表格")
            return

        sessions = {}
        for session_id, messages in self.sessions_for_sheet.items():
            rows = []
            colors = []
            for speaker_name, content in messages:
                rows.append([speaker_name, content])
                color = get_color(speaker_name)
                colors.append([color, color])
            sessions[session_id] = (rows, colors)

        if not sessions:
            self.logger.info("没有新的会话消息需要保存到表格")
            return

        for session_id, (rows, colors) in sessions.items():
            if session_id not in self.sheet_list:
                try:
                    create_sheet(self.access_token, self.union_id, self.workbook_id, session_id, self.sheet)
                    self.sheet_list.append(session_id)
                    self.logger.info(f"已创建新表格: {session_id}")
                except Exception as e:
                    self.logger.error(f"创建新表格[{session_id}]失败: {e}")
            index = write_index(self.access_token, self.union_id, self.workbook_id, session_id, self.sheet)
            write_range = f"A{index}:B{index + len(rows) - 1}"
            write_row(write_range, rows, self.access_token, self.sheet, self.union_id, self.workbook_id, session_id,
                      colors)
            self.logger.info(f"已将群聊 [{session_id}] {len(rows)} 条会话消息保存到表格")

    def clean_expired_sessions(self):
        """
        清理所有会话消息，重置上下文
        """
        self.save_sessions_to_sheet()
        self.sessions_for_sheet.clear()
        self.session_messages.clear()
        self.logger.info("已清理所有会话消息上下文")

    def _get_session_messages(self, session_id):
        if session_id not in self.session_messages:
            self.session_messages[session_id] = deque(maxlen=self.max_session_length)
        return self.session_messages[session_id]

    def _format_message(self, message):
        sender = self.user.nickname if message.is_self else message.contact.display_name
        content = (
            message.to_text()
            if message.local_type == MessageType.Quote
            else message.parsed_content
        )
        return {
            "speaker_name": sender,
            "content": str(content or ""),
            "is_bot": message.is_self,
        }

    def _build_chat_history(self, session_id):
        messages = self._get_session_messages(session_id)
        if not messages:
            return ""
        return json.dumps(list(messages), ensure_ascii=False)

    def get_priority(self) -> int:
        return self.priority

    async def handle_message(self, plusginExcuteContext: PluginExcuteContext) -> None:
        message = plusginExcuteContext.get_message()
        context = plusginExcuteContext.get_context()
        # TODO 目前只维护了文本消息，其他消息类型暂时忽略
        if (
                message.local_type != MessageType.Text
                and message.local_type != MessageType.Quote
        ):
            return
        target = (
            message.room.username if message.is_chatroom else message.contact.username
        )
        session_messages = self._get_session_messages(target)
        formatted_message = self._format_message(message)
        session_messages.append(formatted_message)
        chat_history = self._build_chat_history(target)
        context["chat_history"] = chat_history
        # 不再调用 dify 判断是否 for bot，只维护上下文

        # 如果是群聊消息，保存到sessions_for_sheet
        if message.is_chatroom:
            session_name = message.room.display_name
            nickname = message.contact.display_name
            if session_name not in self.sessions_for_sheet:
                self.sessions_for_sheet[session_name] = []
            self.sessions_for_sheet[session_name].append((
                nickname,
                formatted_message["content"]
            ))
        return

    def get_plugin_name(self) -> str:
        return self.name

    def get_plugin_description(self) -> str:
        return "这是一个用于维护消息上下文的插件"

    @classmethod
    def get_plugin_config_schema(cls):
        """
        返回插件配置的pydantic schema类。
        """
        return ChatContextPluginConfig
