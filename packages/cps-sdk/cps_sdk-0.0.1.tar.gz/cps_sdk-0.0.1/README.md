# Python 电商CPS SDK 整合
#### 目前仅支持:
1. 淘宝CPS
2. 京东CPS
3. 拼多多CPS
4. 唯品会CPS

#### 使用示例: 
##### 1.以淘宝CPS为例(其他供应商大同小异, 返回response均为requests模块返回的response对象)

```python
from third_sdk import TbClient, JdClient, PddClient, VipClient

client = TbClient(appkey='', secret='')

# 商品查询
resp = client.taobao_tbk_dg_item_info_get(**{'num_iid': 'xxx'})
print(resp.text)  # res.json 直接获取dict结构数据

# 物料搜索
client.taobao_tbk_dg_material_optional(**{'q': 'xxx', 'pid': ''})
print(resp.text)

# 尚未录入的api调用方式 (以物料精选为例)
from third_sdk.top.api.rest.TbkDgOptimusMaterialRequest import TbkDgOptimusMaterialRequest

req = TbkDgOptimusMaterialRequest()
resp = client.api_invoke(req, **{'pid': ''})
print(resp)
```