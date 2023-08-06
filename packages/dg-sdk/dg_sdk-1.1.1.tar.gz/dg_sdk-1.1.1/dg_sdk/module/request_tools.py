# url path 统一管理 花括号中变量代表待替换值
from dg_sdk.core.api_request import ApiRequest

from dg_sdk.core.api_request_v1 import ApiRequest as ApiRequestV1
from dg_sdk.dg_client import DGClient
from dg_sdk.common_util import generate_mer_order_id
import datetime

# ---------- 聚合正扫----------
online_payment_create = '/v2/trade/payment/jspay'  # 聚合正扫
online_payment_close = '/v2/trade/payment/scanpay/close'  # 交易关单
online_payment_close_query = '/v2/trade/payment/scanpay/closequery'  # 交易关单查询
online_payment_query = '/v2/trade/payment/scanpay/query'  # 交易查询
online_payment_refund = '/v2/trade/payment/scanpay/refund'  # 交易退款
online_payment_refund_query = '/v2/trade/payment/scanpay/refundquery'  # 退款查询

# ---------- 聚合反扫----------
offline_payment_scan = '/v2/trade/payment/micropay'  # 聚合反扫

union_user_id = '/v2/trade/payment/usermark/query'  # 获取银联用户标识

# 调用域名
BASE_URL = 'https://api.huifu.com'
BASE_URL_V1 = 'https://spin.cloudpnr.com'


def __request_init(url, request_params, base_url=BASE_URL):
    if not request_params.get('req_seq_id'):
        request_params['req_seq_id'] = generate_mer_order_id()

    if not request_params.get('req_date'):
        request_params['req_date'] = datetime.datetime.now().strftime('%Y%m%d')

    mer_config = DGClient.mer_config

    if mer_config is None:
        raise RuntimeError('SDK 未初始化')

    if "huifu_id" not in request_params:
        request_params['huifu_id'] = mer_config.huifu_id

    if BASE_URL in url:
        ApiRequest.base_url = url
        url = ""
    else:
        ApiRequest.base_url = base_url

    ApiRequest.build(mer_config.product_id, mer_config.sys_id, mer_config.private_key, mer_config.public_key, url,
                     request_params, DGClient.connect_timeout)


def request_post(url, request_params, files=None, base_url=None):
    """
    网络请求方法
    :param url: 请求地址
    :param request_params: 请求参数
    :param files: 附带文件，可为空
    :param base_url: 请求地址基本域名，可为空，默认为 https://api.huifu.com
    :return: 网络请求返回内容
    """

    if base_url is None:
        base_url = BASE_URL
    ApiRequest.sdk_version = DGClient.__version__
    __request_init(url, request_params, base_url)
    return ApiRequest.post(files)


def request_post_without_seq_id(url, request_params, files=None, base_url=None):
    if base_url is None:
        base_url = BASE_URL
    __request_init(url, request_params, base_url)
    return ApiRequest.post(files)


def request_post_v1(url, request_params, files=None, base_url=None):
    """
    网络请求方法，V1 版本接口
    :param url: 请求地址
    :param request_params: 请求参数
    :param files: 附带文件，可为空
    :param base_url: 请求地址基本域名，可为空，默认为 https://spin.cloudpnr.com
    :return: 网络请求返回内容
    """
    if not request_params.get('req_seq_id'):
        request_params['req_seq_id'] = generate_mer_order_id()

    if not request_params.get('req_date'):
        request_params['req_date'] = datetime.datetime.now().strftime('%Y%m%d')
    if base_url is None:
        base_url = BASE_URL_V1

    mer_config = DGClient.mer_config

    if mer_config is None:
        raise RuntimeError('SDK 未初始化')

    if "huifu_id" not in request_params:
        request_params['huifu_id'] = mer_config.huifu_id

    if BASE_URL_V1 in url:
        ApiRequestV1.base_url = url
        url = ""
    else:
        ApiRequestV1.base_url = base_url
    ApiRequestV1.sdk_version = DGClient.__version__
    ApiRequestV1.build(mer_config.product_id, mer_config.sys_id, mer_config.private_key, mer_config.public_key, url,
                       request_params, DGClient.connect_timeout)
    return ApiRequestV1.post(files)
