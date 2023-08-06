# iSpace 应用标准化开发框架法式（FaSh） v0.0.3

## 简介
iSpace 应用标准化开发框架法式（Fash）有助于快速构建 iSpace 应用。通过遵守一定的文件组织方式和通信格式，FaSh 能够帮助开发者监视素材文件夹、初始化数据库、以多进程方式运行 iSpace 组件，并以 Redis 为中介实现进程间通信。此外，通过 Node-Red 还可以进一步拓展不同类型的组件，实现多种传感器、反应器、学习器、数据库的接入。

FaSh 库的数据存储依赖 SQlite，SQlite 是一个软件库，实现了自给自足的、无服务器的、零配置的、事务性的 SQL 数据库引擎, 简而言之能够在本地建立数据库，其数据结构近似于 Excel。

FaSh 库中多个 iSpace 组件之间使用 Redis 数据库进行数据交换，redis 是一个开源的内存型 Key-Value数据库，简而言之就是在内存中新建了一个高性能字典型数据库，每条数据都由一个 key 和一个 value 组成，查询 key 即可获得 value。

## 环境
### 安装 FaSh 库
```python
pip install FaSh
```


### 安装并启动 redis
#### redis 下载
至 [redis 官方页面](https://redis.io/)下载 redis 安装包，或使用官方命令进行安装。

windows 环境请至 tporadowski 大佬的[Redis for Windows 项目](https://github.com/tporadowski/redis/releases)下载Windows版本，目前支持到5.0.10版本。

#### redis 安装与启动
安装过程中请勾选 "Add the Redis installation folder to PATH environment variable."；

请勿修改默认端口号（6379）,并勾选 "Add an exception to the Windows Firewall"；

其他按照默认选项安装即可。

安装后打开 redis 所在位置，运行 redis-server.exe，窗口可能闪退。

redis 已经运行，地址为127.0.0.1: 6379。


### 安装并启动 Node-Red
施工中……


### 调试工具
#### redis 调试工具
[Another Redis Desktop Manager](https://github.com/qishibo/AnotherRedisDesktopManager/releases) 是一款开源免费的图形化 redis 调试工具，安装后将自动连接默认数据库，也可指定连接自定数据库。

#### SQlite调试工具
[SQliteSpy](https://www.yunqa.de/delphi/apps/sqlitespy/index) 是一款免费的轻量级图形化SQlite调试工具，可用于打开 SQlite 生成的数据库文件。


## 基础
### 总体架构&程序框架
Fash 库规定了一个 iSpace 应用四个主要方面：程序框架、文件组织方式、数据库格式和通信格式，其中，程序框架是理解 FaSh 库运行的核心。

FaSh 认为，一个 iSpace 应用一般逻辑为：

![FaSh 总体架构](https://user-images.githubusercontent.com/84532033/137523587-d125a3ee-88b9-415f-b63a-102657838448.png)

为实现一般逻辑，Fash 规定一个 iSpace 应用包括六个独立的组件：msghub、sensor、performer、selector、corrector、learner。其示意图如下：

![FaSh 组件关系](https://user-images.githubusercontent.com/84532033/137523998-3e4c051a-3315-4436-93f2-62717b6b3a12.png)

* msghub 是一个 redis 数据库实例，sensor、performer、selector、corrector、learner 等五个组件分别独立地向其中更新或请求信息，并且根据获取到的信息进行执行内部代码。

* sensor 是传感器组件，不断向 msghub 更新传感数据。

* performer 是反应器组件，不断从 msghub 中拉取反应信息，并上报反应器是否在运行

* selector 是选择器组件，不断从 msghub 拉取传感数据，以及对应的反应器是否在运行，若符合条件，则读取素材和参数数据库，向 msghub 更新反应信息

* corrector 是更新器组件，不断从 msghub 拉取更新数据，并对涉及的数据库进行更新

* learner 是学习器组件，不断从 msghub 拉取传感数据、反应数据、反应器运行状态，并将其打包封存，按照一定条件运行学习模型，并上报更新数据

Fash 库并未规定组件间的对应关系，也就是说，一个 sensor 上传的数据可供多个 performer 使用，多个 performer 及其 sensor 的数据又可供一个 learner 学习，任意个 learner 对参数的更新均可通过一个corrector 进行更新，等等。组件更新和查询信息时所使用的 key 在运行组件程序前就设置好，所以为了准确调用信息，Fash 库要求每个运行中的 sensor、performer、learner 具有唯一的名称。

一般而言，一个 selector 只为一个 performer 服务。


### 文件组织方式
目前 Fash 仅规定了 performer 程序的文件组织方式。performer 文件夹的名称应当与该 performer 的名字一致（FaSh 会自动获取文件夹名称作为 performer 程序的名称），必须包含 rmlib（rated-materials-lib）和 database 两个文件夹。除此以外，对其他文件夹或文件并无规定。脚本应当放在根目录下，应当为如下结构：

![performer 文件组织](https://user-images.githubusercontent.com/84532033/137524211-e7ee5069-fa4e-45de-a4e5-16e3a766775f.png)

rmlib 文件夹用于存放各种需要评分的素材，请将**同一用途**的素材文件（也就是需要从中进行比较和选择的一组文件）放在同一个文件夹内。请勿新建二级子文件夹，无法对其下的素材建库。

database 文件夹用于存放数据库文件，名字为 performer_name.db


### 数据库格式
在每个 performer 的 database 文件夹下都存在一个 performer_name.db 文件夹，包含若干张表单，共有两种表单：

* parameters 表单：用于记录 performer 运行时需要选择的参数信息，包含 key(用于储存参数名称)、value(用于储存选择依据)、path(用于储存所属程序)，checked（用于数据库自检）四个字段；

* 其他表单：记录着 rmlib 文件夹下某个文件夹中所有文件的信息，包含 key(用于文件名称)、value(用于储存选择依据)、path(用于储存文件路径)，checked（用于数据库自检）四个字段；

key、path 字段下储存的是字符串，value 字段下储存的是以字符串形式保留的字典，checked 只储存 0 或 1

value 字段下储存采用字典格式可以同时容纳多个参数或者多个判断依据。

![数据库结构](https://user-images.githubusercontent.com/84532033/137524366-62cb3969-a324-46bb-ac41-42cc6afe2755.png)

### 通信协议
在 FaSh 框架中，各 iSpace 组件都必须与 Msghub 通信，向其中写入或者拉取数据，所使用数据都遵循一定的格式。

#### redis 库中的 key-value 规定
redis 数据库中包括以下四种 key-value 对：
* sensor_name : sensing_json  -- 由传感器上报，告知当前读数
* performer_name : perform_json -- 由选择器上报，告知反应器反应中运用的素材和参数
* performer_name_active ：0/1 -- 由反应器上报，告知当前反应器是否运行，value 只能为 0 或 1，0 表示反应停止
* corrector : correct_json -- 由学习器上报，告知更新器如何更新数据库

#### json 格式规定
redis 数据库种储存的值大多为 json 字符串，其格式为：
```python
# 传感器上报格式
sensing_json = {
  'index1_name' : value1,
  'index2_name' : value2,
  'index3_name' : value3}
  
# 选择器上报的格式
perform_json = {
  'materials' : {
    'material_name' : 'path1',
    'material_name' : 'path2',
    'materia3_name' : 'path3'},
  'parameters' : {
    'parameterl_name' : value1,
    'parameterl_name' : value2,
    'parameterl_name' : value3}}
    
# 学习器上报的格式
correct_json = {
  'db' : 'db_path',
  'table1' : '[(key1,value1),(key2,value2),(key3,value3)]',
  'table2' : '[(key1,value1),(key2,value2),(key3,value3)]',
  'table3' : '[(key1,value1),(key2,value2),(key3,value3)]'}
```
上报前请先将字典文件转化为 json 字符串：
```python
# 声明 json 库
import json

# 示例数据字典
sensing_data = {
  'index1_name' : value1,
  'index2_name' : value2,
  'index3_name' : value3}

# 转化为 json 字符串
sensing_json = json.dumps(sensing_data)
```


## 组件类及其程序逻辑
### Rmlib类
Rmlib 类可实现对 rmlib 文件夹下每个素材文件夹的实时监控（目前仅有监控功能）。
#### 实例化
无需传入任何参数，只要文件组织结构正确，脚本位于根目录下，即可建立对象。
#### 方法
使用 start 方法即可开启监听进程。
#### 示例
```python
# 引用声明
import FaSh as fs

# 实例化
performer_rmlib = fs.Rmlib()

# 开启监听
performer_rmlib.start()
```

### Db类
Db 类可实现对 performer_name.db 的初始化。如果 performer_name.db 不存在则创建，若存在则进行检查（目前仅检查）。
#### 实例化
无需传入任何参数，只要文件组织结构正确，脚本位于根目录下，即可建立对象。但若不传入 parameter_dic 参数，就不会创建 “parameters” 表单

parameter_dic是一个字典，其数据结构为:
```python
{'index_name1':'value_generate_func1','index_name2':'value_generate_func2,'index_name3':'value_generate_func3'}
```
#### 方法
使用 init 方法，如果 performer_name.db 不存在则创建，若存在则进行检查。
#### 示例
```python
# 引用声明
import FaSh as fs

# 实例化
performer_db = db()

# 数据库初始化
performer_db.init()
```

### Sensor类
Sensor 类可实现传感器信息的上报。建立 sensor 类至少需要提供传感器名称、初始化函数、主函数三个参数。

Sensor 的运行逻辑为：
* 运行初始化函数一次
* 循环运行主函数，上报获取的内容

主函数应当返回一个符合通信协议的 sensing_json 字符串
```python
sensing_json = {
  'index1_name' : value1,
  'index2_name' : value2,
  'index3_name' : value3}
```
#### 实例化
传入传感器名称、初始化函数、主函数进行实例化，推荐使用关键字传参：
```python
# 引用声明
import FaSh as fs

# 实例化
sensor = fs.Sensor(
  name="sensor_name", #传感器名称
  setup_func=setup_func,  #初始化函数，一段代码，传感器程序运行时仅运行一次
  main_func=main_func, #主函数，一段代码，传感器程序运行时循环运行
)
```
#### 方法
使用 start 方法就可以运行 sensor。
#### 示例
```python
# 引用声明
import json
import FaSh as fs

# 定义初始化函数
def setup_func():
  global value1, value2, value3 #如果想在初始化函数和主函数之间传参，请做全局变量声明
  value1 = 'test_value1'
  value2 = 'test_value2'
  value3 = 'test_value3'

# 定义主函数
def main_func():
  global value1, value2, value3 #如果想在初始化函数和主函数之间传参，请做全局变量声明
  return json.dumps{'index1':value1,'index2':value2,'index3':value3} #主函数必须返回符合 sensing_json 格式的 json 字符串

# 实例化
sensor = fs.Sensor(
  name="sensor_name", #传感器名称
  setup_func=setup_func,  #初始化函数，一段代码，传感器程序运行时仅运行一次
  main_func=main_func, #主函数，一段代码，传感器程序运行时循环运行
)

# 打开传感器
sensor.start()
```

### Performer类
Performer 类可根据获取到的反应信息驱动反应。建立 sensor 类至少需要提供反应器名称、初始化函数、主函数三个参数。

Sensor 的运行逻辑为：
* 读取 Msghub 中的反应信息
* 上报 performer_name_active, 1
* 运行初始化函数一次
* 运行主函数一次，当主函数结束，上报 performer_name_active, 0
* 主函数运行的过程中，会不断读取 Msghub 中的反应信息，如果反应信息更新，进程会停止运行中的主程序，上报 performer_name_active, 0，并且以新的反应信息重新运行主函数
* 重新运行主函数会重复第 2-4 步
#### 实例化
传入传反应器名称、初始化函数、主函数进行实例化，推荐使用关键字传参：
```python
# 引用声明
import FaSh as fs

# 实例化
performer = fs.Performer(
  name="performer_name", #传感器名称
  setup_func=setup_func,  #初始化函数，一段代码，传感器程序运行时仅运行一次
  main_func=main_func, #主函数，一段代码，传感器程序运行时循环运行
)
```
如果 Performer 依赖某些需要评价的参数，可以传入 parameter_dic，即可建立完整的数据库：
```python
# 引用声明
import random
import Fash as fs

#建立包含三个 parameter 的 parameter_dic，数值初始化方法均为 random.randint(0,1)
parameter_dic = {'index1': random.randint(0,1), 'index2': random.randint(0,1), 'index3': random.randint(0,1)} 

# 实例化
performer = fs.Performer(
  name="performer_name", #传感器名称
  setup_func=setup_func,  #初始化函数，一段代码，传感器程序运行时仅运行一次
  main_func=main_func, #主函数，一段代码，传感器程序运行时循环运行
  parameter_dic=parameter_dic
)

# 使用实例的 parameter_dic 属性即可得到 parameter_dic，此时会根据 parameter_dic 创建表格
performer_db = Db(parameter_dic=performer.parameter_dic)
performer_db.init()

```
#### 方法
使用 start 方法就可以运行 performer。

#### 示例
```python
# 引用声明
import pyaudio
import wave
import FaSh as fs

# 定义初始化函数
def MusicPlayer_setup_func():
  global waveopen
  waveopen = pyaudio.PyAudio()
  
# 定义主函数
def MusicPlayer_main_func(dic):
    global waveopen
    wavefile = wave.open(dic['materials']['music'], 'rb')
    stream = waveopen.open(
        format=waveopen.get_format_from_width(wavefile.getsampwidth()),
        channels=wavefile.getnchannels(),
        rate=wavefile.getframerate(),
        output=True)
    while True:
        data = wavefile.readframes(10000)
        if data == '':
            break
        stream.write(data)
    stream.stop_stream()
    stream.close()
    waveopen.terminate()

# 创建 Performer 类
MusicPlayer = fs.Performer(
  name="MusicPlayer", #反应器名称
  setup_func=setup_func,  #初始化函数，一段代码，反应器程序运行时仅运行一次
  main_func=main_func, #主函数，一段代码，反应器程序运行时运行一次，但会循环激活
)
MusicPlayer.start()
```
### Selector类
Selector 类会不断从 Msghub 中拉取传感器数据和反应器工作状态数据。建立 selector 类至少需要提供传感器名称，评价函数，反应器名称，选择函数以建立该类。

Sensor 的运行逻辑为：
* 从 Msghub 中读取所有传感器信息，创建感应字典
* 读取反应器活动状态
* 若反应器在活动，且将传感器信息传入评价函数（用于判断是否需要改变反应），结果为 True，则重新开始循环
* 否则，读取 performer_name.db，将所有表单转化为 dataframe，储存在字典中，并传入选择函数
* 上报反应信息，重新开始循环

选择函数返回值应当是一个满足 perform_json 格式要求的 json 字符串：
```python
perform_json = {
  'materials' : {
    'material_name' : 'path1',
    'material_name' : 'path2',
    'materia3_name' : 'path3'},
  'parameters' : {
    'parameterl_name' : value1,
    'parameterl_name' : value2,
    'parameterl_name' : value3}}
```

#### 实例化
传入传反应器名称、，评价函数，反应器名称，选择函数进行实例化，推荐使用关键字传参：
```python
# 引用声明
import FaSh as fs

# 实例化
performer_selector = fs.Selector(
  name="performer_name", #反应器名称
  judge_func=judge_func, #判断函数，传入传感器读数，返回 True 或 False
  select_func=select_func #选择函数，传入 dataframe，传出 perform_json)
```
#### 方法
使用 start 方法就可以运行 selector。

#### 示例
```python
# 引用声明
import FaSh as fs

# 定义选择函数，返回值为 True 或 False
def judge_func(sensing_dic):
  if sensing_dic['sensor1']['index1'] != 0 and sensing_dic['sensor2']['index2'] != 0:
    result = True
  else:
    result = True
  return result
  
# 定义选择函数，返回对象必须符合 perform_json 要求
def selector_func(df_dic):
    perform_data = {}
    parameters_data = {}
    materials_data = {}
    for key in df_dic.keys():
      if key == 'parameters':
          for index, row in df_dic[key].iterrows():
              parameters_data[index] = row['value']-5
              perform_data['parameters'] = json.dumps(parameters_data) #需要先将 json 中嵌套的 json 字典转化为 json 字符串
      else:
          if key == 'music':
              index = df_dic[key]['value'].idxmax(axis=0)
              materials_data[key] = index
              perform_data['materials'] = json.dumps(materials_data) #需要先将 json 中嵌套的 json 字典转化为 json 字符串
    return json.dumps(perform_data)

# 实例化
performer_selector = fs.Selector(
  name="performer_name", 
  judge_func=judge_func,
  select_func=select_func)
  
performer_selector.start()
```
### Corrector类
施工中……
### Learner类
施工中……
### MsgHub类
用于创建一个 redis 客户端。前提是 redis 已经运行在默认地址。当 Fash 库默认模块无法满足使用需求时，可用于自由构建各类程序。
#### 实例化
无需传入任何参数就可以实例化
#### 方法
使用 .read(key) 方法可以读取 redis 数据库中 key 对应的 value
使用 .write(key，value) 方法可以在数据库中设定键 key 的值为 value
#### 示例
```python
# 引用声明
import FaSh as fs

# 实例化
msg_hub = fs.MsgHub()

# 读写操作
msg_hub.write('test_client','test_msg')
msg_hub.read('test_client') #应当返回 test_msg
```

## 功能函数的写法
### 将函数传入类
唯一要注意的事情是，若要将函数作为对象传入类，不要加上最后的括号。

```python
# 创建一个参数
def test_func():
  return 666

# 正确示例
obj = ClassName(
  func=test_func)

# 错误示例
obj = ClassName(
  func=test_func())
 ```
### 函数间传参
若想在同一个程序的不同函数之间传参，请使用全局变量声明
```python
# 引用声明
import random
 
# 创建两个参数，传参
def number_generator():
  global a
  a = random.random()
  
def a_printer():
  global a
  print(a)  
 ```
