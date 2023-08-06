# -*- coding: utf-8 -*
def run_hive(sql,host1,host2,port,username,url):
    from pyhive import hive
    import requests
    import json
    import re
    try:
        sqls='''set hive.tez.auto.reducer.parallelism=true;
        set hive.exec.reducers.max=99;
        set hive.merge.tezfiles=true;
        set hive.merge.smallfiles.avgsize=32000000;
        set hive.merge.size.per.task=128000000;
        set tez.queue.name=analyst;'''+sql
        sqllist = [j for j in sqls.replace('\n',' ').split(';') if j != '']
        res=[]
        conn = hive.connect(host=host1,port=port,username=username)
        cursor = conn.cursor()
        for i in sqllist:
            cursor.execute(i)
            try:
                res = cursor.fetchall()
            except:
                pass
            conn.commit()
        conn.close()
        return res
    except:
        try:
            conn = hive.connect(host=host2,port=port,username=username)
            cursor = conn.cursor()
            for i in sqllist:
                cursor.execute(i)
                try:
                    res = cursor.fetchall()
                except:
                    pass
                conn.commit()
            conn.close()
            return res
        except Exception as e:
            try:
                error='告警消息: '+i+'\n'+re.match(r'.* (FAILED:.*)',str(e)).group(1)
            except:
                error='告警消息: '+i+'\n'+str(e)
            finally:
                headers = {'Content-Type': 'application/json'}
                data={
                    "msgtype": "text",
                    "text": {
                        "content": error,
                    }
                }
                url=url
                response=requests.post(url,data=json.dumps(data),headers=headers)
                
def send_alert(message,url):
    import requests
    import json
    message='提示消息: '+message
    headers = {'Content-Type': 'application/json'}
    data={
        "msgtype": "text",
        "text": {
            "content": message,
        }
    }
    url=url
    response=requests.post(url,data=json.dumps(data),headers=headers)
                
url='https://oapi.dingtalk.com/robot/send?access_token=0ef0a1174134d10948c479604059f4d0f43596b716932563a749dd51cb0f8502'
sql='''drop table if exists wlst.test_02;
    create table if not exists wlst.test_02
    ROW FORMAT SERDE
       'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
    WITH SERDEPROPERTIES (
      'field.delim'='\\t',
      'line.delim'='\\n',
      'serialization.format'='\\t')
    STORED AS INPUTFORMAT
      'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
    OUTPUTFORMAT
      'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
    LOCATION
      's3n://risk-emr/data/wlas/wlst/test_02'
    TBLPROPERTIES (
      'last_modified_by'='hadoop',
      'orc.compress'='SNAPPY') as
      select 2;
      select * from wlst.test_02'''
result=run_hive(sql,'10.60.21.198','10.60.21.198','10000','hadoop',url) 

send_alert(result,url)




   
                

    
    
 


