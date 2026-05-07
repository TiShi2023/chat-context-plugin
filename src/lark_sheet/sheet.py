import json
from typing import List, Optional

import lark_oapi as lark


class LarkSheet:
    """飞书电子表格操作封装"""

    def __init__(self, app_id: str, app_secret: str, spreadsheet_token: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.spreadsheet_token = spreadsheet_token
        self.client = lark.Client.builder() \
            .app_id(app_id) \
            .app_secret(app_secret) \
            .build()
        # sheet_title -> sheet_id 的映射缓存
        self._sheet_cache: dict[str, str] = {}

    def _request(self, method: lark.HttpMethod, uri: str, body=None) -> dict:
        """发送请求并返回解析后的 JSON 数据"""
        builder = lark.BaseRequest.builder() \
            .http_method(method) \
            .uri(uri) \
            .token_types([lark.AccessTokenType.TENANT])
        if body is not None:
            builder = builder.body(body)
        req = builder.build()
        resp = self.client.request(req)
        if resp.raw:
            return json.loads(resp.raw.content.decode('utf-8'))
        return {'code': resp.code, 'msg': resp.msg}

    def list_sheets(self) -> List[dict]:
        """获取电子表格中所有 sheet 信息列表"""
        data = self._request(
            lark.HttpMethod.GET,
            f'/open-apis/sheets/v3/spreadsheets/{self.spreadsheet_token}/sheets/query'
        )
        return data.get('data', {}).get('sheets', [])

    def get_sheet_id(self, title: str) -> Optional[str]:
        """根据 sheet 名称获取 sheet_id，带缓存"""
        if title in self._sheet_cache:
            return self._sheet_cache[title]
        sheets = self.list_sheets()
        for s in sheets:
            self._sheet_cache[s.get('title', '')] = s.get('sheet_id', '')
        return self._sheet_cache.get(title)

    def create_sheet(self, title: str) -> Optional[str]:
        """创建新的 sheet，返回 sheet_id"""
        data = self._request(
            lark.HttpMethod.POST,
            f'/open-apis/sheets/v2/spreadsheets/{self.spreadsheet_token}/sheets_batch_update',
            body={
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': title
                        }
                    }
                }]
            }
        )
        replies = data.get('data', {}).get('replies', [])
        if replies:
            sheet_id = replies[0].get('addSheet', {}).get('properties', {}).get('sheetId')
            if sheet_id:
                self._sheet_cache[title] = sheet_id
                return sheet_id
        return None

    def append_data(self, sheet_id: str, values: List[List]) -> bool:
        """追加数据到指定 sheet"""
        data = self._request(
            lark.HttpMethod.POST,
            f'/open-apis/sheets/v2/spreadsheets/{self.spreadsheet_token}/values_append',
            body={
                'valueRange': {
                    'range': f'{sheet_id}!A:C',
                    'values': values
                }
            }
        )
        return data.get('code', -1) == 0

    def ensure_sheet(self, title: str) -> Optional[str]:
        """确保 sheet 存在，不存在则创建，返回 sheet_id"""
        sheet_id = self.get_sheet_id(title)
        if sheet_id:
            return sheet_id
        return self.create_sheet(title)
