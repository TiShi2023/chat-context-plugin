import time

from dingtalk_v2 import Sheet


def read_whole_column(column: str, access_token: str, read_sheet: Sheet, union_id: str, workbook_id: str,
                      sheet_id: str) -> list:
    """
    读取指定列的所有数据，直到遇到空值为止
    :param column: 列名，例如 'A'
    :param access_token: 钉钉的 access_token
    :param read_sheet: ReadSheet 实例
    :param union_id: 用户的 union_id
    :param workbook_id: 工作簿的 ID
    :param sheet_id: 表格的 ID
    """
    cursor = 2
    read_flag = True
    rows = []

    while read_flag:
        time.sleep(1)
        # 读取表格数据
        resp = read_sheet.read(
            token=access_token,
            union_id=union_id,
            workbook_id=workbook_id,
            sheet_id=sheet_id,
            range_address=f'{column}{cursor}:{column}{cursor + 1000}'
        )
        values = resp['values']
        for value in values:
            if value[0] == '':
                # 结束循环
                read_flag = False
                break
            else:
                rows.append(value[0])
        cursor = cursor + 1000
    return rows


def write_row(write_range: str, values: list, token: str, write_sheet: Sheet, union_id: str, workbook_id: str,
              sheet_id: str, background_colors: list = None) -> None:
    """
    写入一行数据到指定的范围
    :param write_range: 写入的范围，例如 'A1:B2'
    :param token: 钉钉的 access_token
    :param union_id: 用户的 union_id
    :param values: 要写入的值列表
    :param workbook_id: 工作簿的 ID
    :param sheet_id: 表格的 ID
    :param write_sheet: WriteSheet 实例
    :param background_colors: 背景颜色列表
    """
    write_sheet.write(
        token=token,
        union_id=union_id,
        values=values,
        workbook_id=workbook_id,
        sheet_id=sheet_id,
        range_address=write_range,
        background_colors=background_colors,
    )


def list_sheets(token: str, union_id: str, workbook_id: str, sheet: Sheet) -> list[str]:
    """
    列出工作簿中的所有表格
    :param token: 钉钉的 access_token
    :param union_id: 用户的 union_id
    :param workbook_id: 工作簿的 ID
    :param sheet: Sheet 实例
    """
    return sheet.list(token=token, union_id=union_id, workbook_id=workbook_id)


def create_sheet(token: str, union_id: str, workbook_id: str, sheet_name: str, sheet: Sheet) -> None:
    """
    创建一个新的表格
    :param token: 钉钉的 access_token
    :param union_id: 用户的 union_id
    :param workbook_id: 工作簿的 ID
    :param sheet_name: 新表格的标题
    :param sheet: Sheet 实例
    """
    return sheet.create(token=token, union_id=union_id, workbook_id=workbook_id, sheet_name=sheet_name)


def write_index(token: str, union_id: str, workbook_id: str, sheet_id: str, sheet: Sheet) -> int:
    """
    获取当前表格的索引位置，用于确定下一行写入的位置
    :param token: 钉钉的 access_token
    :param union_id: 用户的 union_id
    :param workbook_id: 工作簿的 ID
    :param sheet_id: 表格的 ID
    :param sheet: Sheet 实例
    :return: 当前表格的最后非空行（从0开始） + 2
    """
    return sheet.profile(token, union_id, workbook_id, sheet_id)['lastNonEmptyRow'] + 2
