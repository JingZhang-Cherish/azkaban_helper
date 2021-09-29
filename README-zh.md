<style> a { text-decoration:none} </style>  <img  src="https://badgen.net/github/release/JingZhang-Cherish/azkaban_excel_yaml/latest/"><a  href="https://pypi.org/project/azkaban-helper/"><img  src="https://badgen.net/pypi/v/azkaban-helper"></a><img  src="https://badgen.net/github/commits/JingZhang-Cherish/azkaban_excel_yaml/"><img  src="https://badgen.net/github/last-commit/JingZhang-Cherish/azkaban_excel_yaml/"><img  src="https://badgen.net/github/license/JingZhang-Cherish/azkaban_excel_yaml/"><img  src="https://badgen.net/github/assets-dl/JingZhang-Cherish/azkaban_excel_yaml/">
<p><a href="https://github.com/JingZhang-Cherish/azkaban_excel_yaml/blob/master/README-zh.md">中文文档 </a>|<a href="https://github.com/JingZhang-Cherish/azkaban_excel_yaml/blob/master/README-zh.md">English Docs</a></p>

# Azkaban配置工具

​		根据Excel配置的作业流内容，生成yaml格式配置文件，打包上传到指定的AzkabanServer，并配置作业流调度

## 功能

- 配置project，创建projet
- 配置flow，创建flow文件
- 配置Azkaban Server地址，用户名，密码
- 按不同的project，打包成不同的zip文件，并上传到Server上
- 为每个flow提供调度配置，调度设置开关可开启和关闭
- 提供excel配置模板，按照配置一键配置提交值服务器
- 支持Windows，Mac OS，Linux及其他Unix系统

## 快速开始

环境需求：

- Python3.0+
- Apache Azkaban 3.90+
- Office Excel 或者 WPS

1. 下载项目源码到本地

   - Linux/OS/Unix

   ```sh
   wget -O https://github.com/JingZhang-Cherish/azkaban_excel_yaml.zip
   ```

   - Windows 直接下载源码到本地

   - Git

   ```sh
   git clone https://github.com/JingZhang-Cherish/azkaban_excel_yaml.git
   ```

2. 编译源码

   (可能需要联网下载依赖)

   ```shell
   cd azkaban_excel_yaml
   #Linux/OS
   python setup.py install
   #Window
   python setup.py bdist_wininst
   ```

3. 快速执行

   修改docs/template.xlsx的config sheet页的Azkaban地址，用户名，密码

   ```sh
   #执行生产和上传命令
   azkaban_helper docs/template.xlsx
   ```

更多Excel内容详细配置，详见配置

## 配置

​	默认的模板中有5个sheet页，info，config，projects，scheduler，proA

- info：应用的相关版本信息和填写说明已经功能更新，无需填写
- config: 配置Azkaban的url，username，password等信息，sheet页名称不可更改
- projects：所有projcets，用于创建和上传的配置
- scheduler：是为已经配置的project添加和取消调度器，cron列是满足定时器表达式，详情可参考[quartz-scheduler](http://www.quartz-scheduler.org/)
- proA是一个项目的，这个sheet页的名称需要和projects的内容相同，否则可能出现无法上传的情况，如有多个project需要配置，则可以复制该sheet页，进行修改。

## 详细功能说明

详细配置步骤：

1. `config页`，azkaban_url列为Azkaban Server的web 访问地址，  目前支持单个地址上传，后续版本可配置多个地址，且增加开关。建议配置具有ADMIN权限的用户，否则可能出现project创建失败的情况，详见Azkaban[配置](https://azkaban.readthedocs.io/en/latest/userManager.html)

2. `projects`这里配置project_name和描述信息，如果描述信息中不支持写入中文，建议修改azkaban数据库的编码为utf-8

3. `scheduler`调度页面为每个作业添加调度器，这里的调度器，必须是后续project已经配置过的flow才行。cron列是满足定时器表达式，详情可参考[quartz-scheduler](http://www.quartz-scheduler.org/)

4. flow页面配置：

   - flow_desc和job_comment，这两列的值不会写入到flow中，不要改变每个列的顺序和标题。

   - 从第二行开始为每个job的的配置细节，一组job组成一个flow，flow的参数可配置多个，多个key=value参数对使用`|`连接，首尾不需要。

   - 每个flow，只需要为第一个job配置flow_configs即可，其他不需要，请把该flow的所有参数都配置在该flow的第一个job中。详见配置模板中的配置案例，如果你有一些大量重复使用的参数，例如昨日日期，建议配置在azkaban/executor/conf/global.properties中

     ```properties
     dt=$(new("org.joda.time.DateTime").minusDays(1).toString("yyyyMMdd"))
     create_script=/home/pg/zhfd_script/public/create_done_file.sh
     ```

   - comman参数中使用flow_configs定义的参数时，需要使用${param_name}方式引用，部分内置参数可以参考Azkaban官网

   - dependOn列，被依赖的job必须配置在该job之前。多个依赖用`|`分隔，首尾不需要。

   

## 限制

- 如果你的Azkaban有使用到Trigger(触发器)，以及Apache Kafka作为事件流的传递，目前版本还不支持配置
- 不支持Azkaban配置的[全部API](https://azkaban.readthedocs.io/en/latest/ajaxApi.html)接口，目前仅调用了部分接口开发。
- 目前Azkaban的FLow配置版本为2.0的yaml格式，不支持生成1.0版本
- 目前功能仅支持，创建project，生成flow文件，打包flow文件成zip文件，上传到server，设置调度和取消调度
- 目前主要支持的jobtype主要是command，其他暂不支持

### 后续计划

​		新版本中会增加trigger的配置，SLA的配置，条件流，文档配置校验，多种jobtype支持等功能。

## 参考

Azkaban的安装和使用文档：https://azkaban.readthedocs.io/en/latest/getStarted.html

Azkaban的API接口文档：https://azkaban.readthedocs.io/en/latest/ajaxApi.html

Python 库 PyYAML，requests，xlrd，requests-toolbelt等等

## 联系方式

如果在使用过程中有任何疑问或者建议，请发送邮件到E-mail：cherish244612023@gmail.com

