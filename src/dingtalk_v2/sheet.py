# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import List, Any

from alibabacloud_dingtalk.doc_1_0 import models as dingtalkdoc__1__0_models
from alibabacloud_dingtalk.doc_1_0.client import Client as dingtalkdoc_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sheet:
    def __init__(self):
        self.client = Sheet.create_client()

    @staticmethod
    def create_client() -> dingtalkdoc_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkdoc_1_0Client(config)

    def create(self, token, union_id, sheet_name, workbook_id) -> None:
        create_sheet_headers = dingtalkdoc__1__0_models.CreateSheetHeaders()
        create_sheet_headers.x_acs_dingtalk_access_token = token
        create_sheet_request = dingtalkdoc__1__0_models.CreateSheetRequest(
            operator_id=union_id,
            name=sheet_name
        )
        try:
            self.client.create_sheet_with_options(workbook_id, create_sheet_request, create_sheet_headers,
                                                  util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    async def create_async(self, token, union_id, sheet_name, workbook_id) -> None:
        create_sheet_headers = dingtalkdoc__1__0_models.CreateSheetHeaders()
        create_sheet_headers.x_acs_dingtalk_access_token = '<your access token>'
        create_sheet_request = dingtalkdoc__1__0_models.CreateSheetRequest(
            operator_id='ppgAQuHfOoNVpJiStDwWCEgiEiE',
            name='Sheet1'
        )
        try:
            await self.client.create_sheet_with_options_async('e54Lqxxx', create_sheet_request, create_sheet_headers,
                                                              util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    def read(self, token, union_id, workbook_id, sheet_id, range_address):
        get_range_headers = dingtalkdoc__1__0_models.GetRangeHeaders()
        get_range_headers.x_acs_dingtalk_access_token = token
        get_range_request = dingtalkdoc__1__0_models.GetRangeRequest(
            select='values',
            operator_id=union_id
        )
        try:
            resp = self.client.get_range_with_options(workbook_id, sheet_id, range_address,
                                                      get_range_request, get_range_headers,
                                                      util_models.RuntimeOptions())
            return resp.body.to_map()
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass
            print(err)
            return None

    @staticmethod
    async def read_async(
            args: List[str],
    ) -> None:
        client = Sheet.create_client()
        get_range_headers = dingtalkdoc__1__0_models.GetRangeHeaders()
        get_range_headers.x_acs_dingtalk_access_token = '<your access token>'
        get_range_request = dingtalkdoc__1__0_models.GetRangeRequest(
            select='values',
            operator_id='ppgAxxx'
        )
        try:
            await client.get_range_with_options_async('e54Lq3xxx', 'Sheet1', 'A1:B2', get_range_request,
                                                      get_range_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    def write(self, token, union_id, values, workbook_id, sheet_id, range_address, background_colors=None) -> None:
        update_range_headers = dingtalkdoc__1__0_models.UpdateRangeHeaders()
        update_range_headers.x_acs_dingtalk_access_token = token
        update_range_request = dingtalkdoc__1__0_models.UpdateRangeRequest(
            operator_id=union_id,
            values=values,
            background_colors=background_colors,
        )
        try:
            self.client.update_range_with_options(workbook_id, sheet_id, range_address,
                                                  update_range_request, update_range_headers,
                                                  util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass
            print(err)

    @staticmethod
    async def write_async(
            args: List[str],
    ) -> None:
        client = Sheet.create_client()
        update_range_headers = dingtalkdoc__1__0_models.UpdateRangeHeaders()
        update_range_headers.x_acs_dingtalk_access_token = '<your access token>'
        update_range_request = dingtalkdoc__1__0_models.UpdateRangeRequest(
            operator_id='ppgAQuxxxxx',
            values=[
                [
                    'text'
                ]
            ],
            background_colors=[
                [
                    '#ff0000'
                ]
            ],
            hyperlinks=[
                [
                    None
                ]
            ],
            number_format='@'
        )
        try:
            await client.update_range_with_options_async('e54Lqxxxxx', 'Sheet1', 'A1:B1', update_range_request,
                                                         update_range_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    def list(self, token, union_id, workbook_id) -> list[Any]:
        get_all_sheets_headers = dingtalkdoc__1__0_models.GetAllSheetsHeaders()
        get_all_sheets_headers.x_acs_dingtalk_access_token = token
        get_all_sheets_request = dingtalkdoc__1__0_models.GetAllSheetsRequest(
            operator_id=union_id
        )
        try:
            resp = self.client.get_all_sheets_with_options(workbook_id, get_all_sheets_request, get_all_sheets_headers,
                                                           util_models.RuntimeOptions())
            sheet_object_list = resp.body.to_map().get('value', [])
            return [sheet_object['name'] for sheet_object in sheet_object_list if sheet_object.get('name') is not None]
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def list_async(
            args: List[str],
    ) -> None:
        client = Sheet.create_client()
        get_all_sheets_headers = dingtalkdoc__1__0_models.GetAllSheetsHeaders()
        get_all_sheets_headers.x_acs_dingtalk_access_token = '<your access token>'
        get_all_sheets_request = dingtalkdoc__1__0_models.GetAllSheetsRequest(
            operator_id='ppgAxxx'
        )
        try:
            await client.get_all_sheets_with_options_async('e54Lq3xxx', get_all_sheets_request, get_all_sheets_headers,
                                                           util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    def profile(self, token, union_id, workbook_id, sheet_id) -> dict:
        get_sheet_headers = dingtalkdoc__1__0_models.GetSheetHeaders()
        get_sheet_headers.x_acs_dingtalk_access_token = token
        get_sheet_request = dingtalkdoc__1__0_models.GetSheetRequest(
            operator_id=union_id
        )
        try:
            resp = self.client.get_sheet_with_options(workbook_id, sheet_id, get_sheet_request, get_sheet_headers,
                                                      util_models.RuntimeOptions())
            return resp.body.to_map()
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def main_async(
            args: List[str],
    ) -> None:
        client = Sheet.create_client()
        get_sheet_headers = dingtalkdoc__1__0_models.GetSheetHeaders()
        get_sheet_headers.x_acs_dingtalk_access_token = '<your access token>'
        get_sheet_request = dingtalkdoc__1__0_models.GetSheetRequest(
            operator_id='ppgAxxx'
        )
        try:
            await client.get_sheet_with_options_async('e54Lq3xxx', 'Sheet1', get_sheet_request, get_sheet_headers,
                                                      util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    from oauth import Oauth

    oauth = Oauth(
        app_key='dingyyrnvl9ueyp6vayf',
        app_secret='lkXbbuAYdYPoQCoZ5_zZDqYl0OKKRrF-FVy5rCYDT0iZXgaeedViuK2TDkSv_C33'
    )
    resp = oauth.main()
    access_token = resp['accessToken']
    union_id = 'H5u3CnWUh4RJX2Pw4dcxBgiEiE'
    workbook_id = 'l6Pm2Db8DaXrm0Q1FnNAj7RrWxLq0Ee4'

    sheet = Sheet()
    # sheet.create(token=access_token, union_id=union_id, sheet_name='test', workbook_id=workbook_id)
    # sheets = sheet.list(token=access_token, union_id=union_id, workbook_id=workbook_id)
    sheet_profile = sheet.profile(token=access_token, union_id=union_id, workbook_id=workbook_id, sheet_id='Sheet1')
    print(sheet_profile)
