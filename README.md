<img  src="https://badgen.net/github/release/JingZhang-Cherish/azkaban_excel_yaml/latest/">
<a  href="https://pypi.org/project/azkaban-helper/"><img  src="https://badgen.net/pypi/v/azkaban-helper"></a><img  src="https://badgen.net/github/commits/JingZhang-Cherish/azkaban_excel_yaml/"><img  src="https://badgen.net/github/last-commit/JingZhang-Cherish/azkaban_excel_yaml/"><img  src="https://badgen.net/github/license/JingZhang-Cherish/azkaban_excel_yaml/"><img  src="https://badgen.net/github/assets-dl/JingZhang-Cherish/azkaban_excel_yaml/">


<style> a { text-decoration:none} </style> 
<p><a href="https://github.com/JingZhang-Cherish/azkaban_excel_yaml/blob/master/README-zh.md"    >中文文档 </a>
|<a href="https://github.com/JingZhang-Cherish/azkaban_excel_yaml/blob/master/README-zh">English Docs</a></p>
# Azkaban Config Tool


​		According to the job flow content configured in Excel, a YAML configuration file is generated, packaged and uploaded to the specified AzkabanServer, and job flow scheduling is configured.

##  Function

- Configure project to create projet
- Configure flow and create flow files
- Configure the Azkaban Server address, user name, and password
- According to different projects, package into different ZIP files and upload them to the Server
- Provides scheduling configuration for each flow, scheduling setting switch can be turned on and off
- Provide the Excel configuration template and submit the value server according to the configuration one-click configuration
- Supports Windows, Mac OS, Linux and other Unix systems

## Quick Start

Environmental requirements：

- Python3.0+
- Apache Azkaban 3.90+
- Office Excel or WPS

1. Download the project source code locally

   - Linux/OS/Unix

   ```sh
   wget -O https://github.com/JingZhang-Cherish/azkaban_excel_yaml.zip
   ```

   - Windows  User Can Download the source code from the Web page to the local PC

   - you can also get the source by `git clone`

   ```sh
   git clone https://github.com/JingZhang-Cherish/azkaban_excel_yaml.git
   ```

2. Compile the source code

   > Internet download dependencies may be required

   ```shell
   cd azkaban_excel_yaml
   #Linux/OS
   python setup.py install
   #Window
   python setup.py bdist_wininst
   ```

3. Quick Execute 

   modify `docs/template.xlsx` file's`config sheet :Azkaban_url ，user_name，password

   ```sh
   #Run the build and upload commands
   azkaban_helper docs/template.xlsx
   ```

For more details on Excel configuration, see Configuration

## Configuration

​	The default template has 5 sheets, info, Config, Projects, Scheduler, and proA

- info：The version information and filling description of the application have been updated. You do not need to fill in the information
- config: Set the URL, username, and password of Azkaban. The sheet page name cannot be changed
- projects：All Projcets used to create and upload configurations
- scheduler：Is to add and remove the scheduler for the configured project, and the cron column is to satisfy the timer expression,you can refer to [quartz-scheduler](http://www.quartz-scheduler.org/)
- ProA is a project. The name of the sheet page should be the same as the content of projects, otherwise it may not be uploaded. If multiple projects need to be configured, you can copy the sheet page and modify it.

## Detailed Functions

##### Detailed configuration steps:

1. `config`, azkaban_url is listed as the web access address of Azkaban Server. Currently, a single address can be uploaded. In later versions, multiple addresses can be configured and switches can be added. Suggested configuration with ADMIN user permissions, or possible project creation failed, detailed in Azkaban [configuration](https://azkaban.readthedocs.io/en/latest/userManager.html)

2. `projects` Configure project_name and description. If the description does not support Chinese characters, you are advised to change the encoding of the Azkaban database of MySQL to UTF-8

3. `scheduler` The scheduling page adds a scheduler for each job, and the scheduler must be a flow that has been configured for subsequent projects. The CRon column is an expression that satisfies the timer[quartz-scheduler](http://www.quartz-scheduler.org/)

4. flow Sheet Configuration：

   - flow_desc and job_comment，The values of these two columns are not written to the flow, so do not change the order and heading of each column。

   - Starting from the second line configuration details for each job, a set of job a flow, flow parameters can be configured multiple, multiple key = value parameters to use ` | ` connection, fore and aft don't need.

   - You only need to configure flow_configs for the first job of each flow. You need to configure all parameters of the flow in the first job of the flow. See the configuration in the template configuration cases, if you have a lot of repeated use of parameters, such as date of yesterday, suggested configuration in azkaban/executor/conf/global properties

     ```properties
     dt=$(new("org.joda.time.DateTime").minusDays(1).toString("yyyyMMdd"))
     create_script=/home/pg/zhfd_script/public/create_done_file.sh
     ```

   - If the comman parameter is flow_configs, you need to use ${param_name} to reference some built-in parameters. For details, see the Azkaban official website

   - In the dependOn column, the dependent job must be set before the job. Multiple dependent with ` | ` space, fore and aft don't need.

   

## Limits

- If your Azkaban uses triggers and Apache Kafka as an event stream, the current version does not support this configuration
- do not support the configuration of Azkaban [ALL API](https://azkaban.readthedocs.io/en/latest/ajaxApi.html) interface, currently only call the part of the interface development.
- The FLow configuration version of Azkaban is yamL 2.0, and version 1.0 is not supported
- Currently, the following functions are supported: create a project, generate a flow file, package the flow file into a ZIP file, upload it to the server, set scheduling and cancel scheduling
- Currently, the jobtype is mainly command. Other jobtypes are not supported

### RoadMap

​		The new version will add trigger configuration, SLA configuration, conditional flow, document configuration verification, jobType support and other functions.

## Reference

Azkaban installation and use documentation：https://azkaban.readthedocs.io/en/latest/getStarted.html

Azkaban API documentation：https://azkaban.readthedocs.io/en/latest/ajaxApi.html

Python libraries PyYAML，requests，xlrd，requests-toolbelt and more

## Contact

If you have any questions or suggestions during use, please send email to E-mail：cherish244612023@gmail.com