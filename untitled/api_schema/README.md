
##说明：

###版本：

v1.0

###协议：

HTTP2 / HTTPS

**支持：**

TLS 1.2、TLS 1.3

**不支持:**

HTTP、SSLv2、SSLv3


###请求方法：

GET、POST、PUT、DELETE、PATCH

###数据格式：

```
Accept Header:

无加密:

	Json (application/json)

	MsgPack (applicaiton/msgpack)

AES加密:

	MsgPack-AES(application/aes+msgpack)
	MsgPack-AES-BASE64(application/aes+base64+msgpack)

```

###名称解释：

**请求参数：** App向服务端请求数据时所传入的数据。

**响应参数：** 服务端接收到App的请求，向App返回的数据。

###HTTP响应状态码：

**2XX** - 成功操作

**4XX** - 请求调用失败

**5XX** - 服务端内部错误


###错误码：

errno|errmsg|说明
----|-------|---
400001|parameter missing|参数缺失
400003|operation failed|操作失败
400004|not found|没有找到
400005|no authority|没有权限
500001|system error|系统异常


###公共参数

**请求header**

```
    X-APP-KEY: 092fewifq21fj219
    # 当前请求的唯一标示和时间戳，用半角逗号分隔
    X-MSG-ID: UUID-string,TIMESTAMP

    # 授权签名证书，签名算法见后
    X-AUTH: X-AUTH-SIGN
    # or 表示这是用publisher key做的签名
    X-AUTH: X-AUTH-SIGN, publisher
    # or 表示这是启用超级模式，同时，必须用secret key签名
    X-AUTH: X-AUTH-SIGN, master

    # AccessToken和AccessToken的HMAC签名
    X-TOKEN: APP-Access-Token, X-TOKEN-SIGN
    # 表示这是使用publisher key做的签名
    X-TOKEN: APP-Access-Token, X-TOKEN-SIGN, publisher

```

#### 应用访问授权机制

每个App会同时有一对Access Key 和 Secret Key。Publisher Key 是由后端服务根据Secret Key生成一个一次性的替代物，用于Web场景。

1. X-APP-KEY：App对应的App Access Key

2. X-AUTH 和 X-TOKEN 只能二选一. X-AUTH 用于没有可用的用户凭证时使用，比如注册、登录这些操作。
X-TOKEN是当用户登录成功，后续需要以该用户身份进行访问的时候使用。X-TOKEN相当于一个用户身份令牌。

3. SecretKey / PublisherKey:

App 密钥。 PublisherKey 用于在Web等场景，缺乏安全保证的情况下使用.（PublisherKey 是一次性生成，兑换成功Access Key后即作废。）

4. HMAC Signature的签名算法:

    X-AUTH-SIGN = HEXDIGEST(HAMC(SECRET_KEY|PUBLISHER_KEY, X-MSG-ID-UUID + ':' + TIMESTAMP))

    X-TOKEN-SIGN = HEXDIGEST(HMAC(SECRET_KEY||PUBLISHER_KEY, APP-ACCESS-TOKEN + ':' + X-MSG-ID-UUID + ':' + TIMESTAMP))


```

**请求参数**

参数|类型|是否必须|描述
---|----|------|----
where|json|否|查询条件
page|int|否|请求页码（默认为1）
limit|int|否|请求条数（默认为10）
sort|json|否|排序（默认按照创建时间倒序）
_meta|json|否|包含上述参数的JSON串
**请求参数**


**响应参数**

参数|类型|是否必须|描述
---|----|------|----
err_no|int|否|错误码
err_name|string|否|错误名称(short string name)
err_msg|string|否|错误描述
results|dict/list|否|数据
__meta|dict|否|当返回一个结果集的时候会存在，里面包含 {count:结果集记录数, has_more:是否还有结果集, type:'result_set'}
ticket|string|是|唯一标识
time|UTC|是|时间

###API接口网关:

```
所有API Gateway接口ENDPOINT为：

https://\<API_DOMAIN>/\<API_VERION\>/\<ResourceClassName\>/

Example:

https://aoao-api.o3cloud.cn/1.0/products/

https://api.aoao.cn/1.0/oauth/

```

###Authorization接口：

```
1. App 使用Access Key 获取Request Token
2. App 使用Request Token 换取Access Token
3. App 使用Access Token 来获得相应的权限
```

###其它注意事项:

**时间单位：** UTC时间

**金额单位：** 分

**距离单位：** 米

**坐标：** 百度坐标
