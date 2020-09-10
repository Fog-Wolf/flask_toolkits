flask_toolkits
====
本人经过几个flask完整项目的历练，总结了这些方法希望能在未来帮助到自己或者同样使用flask框架的挚友们！

### 环境依赖
flask v1.1.1+
flask_sqlalchemy v2.4.1+
xlrd v1.2.0
wtforms v2.2.1

### 安装步骤
1.下载到本地
2.将整个文件放置到项目中即可

### 目录结构描述
* Readme.md                       // 帮助
* LICENSE                         // 许可证
* .gitignore                      // 忽略文件
* redprint.py                     // 红图（蓝图升级）
* api_request                     // API请求包
    * __init__.py
    * api_request.py
* api_response                    // API响应包
    * __init__.py
    * code.py
* db_module                       // 针对模型数据库操作，暂时只有mysql
    * __init__.py
    * action.py
    * methods.py
* excel                           // EXCEL操作包
    * __init__.py
    * read_excel.py
* layer_data                      // 图层数据处理
    * __init__.py
    * helper.py
    * processing.py
* layer_form                      // 表单数据处理
    * __init__.py
    * id_card.py
    * number.py
    * time.py
* sign                            // 签名加密
    * __init__.py


### V1.0.0 版本内容更新
*  `注意：需要注册的方法中包含配置内容，使用时可以阅读一下代码中的注释，代码比较通俗易懂，这个不用担心～`
1. 红图是蓝图的升级版，将路径配置更加人性化
2. API请求包，包含了请求日志记录（包含执行时间记录），请求数据库长链接检测记录，整合化request请求方法。请求日志记录，请求数据库长链接检测记录需要注册使用 `RequestHandler(app) `， `RequestsLog(app)`
3. API响应包，包含了全局错误返回提示，美化json返回数据格式，返回响应码。全局错误返回提示需要注册 `FrameworkError(app)`
4. 针对模型数据库操作, 现在只有针对mysql， 只要建好模型，引入方法，继承在模型中，就可以直接使用增删改查，查询分查单条，查多条，条件按照字典和列表都可以传入.操作数据库分为按条件操作和直接传入模型。
支持特殊条件查询，详见 db_module/methods.py `FilterName`类
5. EXCEL操作包， excel的操作方法（写的一般，适用性有点局限，可以忽略）
6. 图层数据处理，包含数据处理方法和处理文件方法
7. 表单数据处理，包含针对表单的操作，在验证form表单的时候，直接继承`BaseForm`方法即可使用验证，还有见证数字范围和有效性方法，验证身份证和时间方法。

