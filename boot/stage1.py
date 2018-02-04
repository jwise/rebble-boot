from flask import Blueprint, jsonify, request
import requests

UPSTREAM_BOOT = 'https://boot.getpebble.com/api/config'
CLOUDPEBBLE_WS_PROXY = 'wss://ws-proxy.cloudpebble.rebble.io/device'

boot_api = Blueprint('boot_api', __name__)


def patch_boot(endpoint: str, version: str):
    boot = requests.get(f'{UPSTREAM_BOOT}/{endpoint}', params={'app_version': version}).json()
    boot['config'].get('developer', {})['ws_proxy_url'] = CLOUDPEBBLE_WS_PROXY
    boot['config']['href'] = request.base_url
    return boot


@boot_api.route('/ios')
def boot_ios():
    app_version = request.args.get('app_version', '4.3')
    return jsonify(patch_boot('ios/v3/207/28', app_version))


@boot_api.route('/android/v3/<int:build>')
def boot_android(build: int):
    app_version = request.args.get('app_version', '4.3')
    return jsonify(patch_boot(f'android/v3/{build}', app_version))
