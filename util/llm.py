# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2024年12月08日
描述：用来处理与大模型的交互
"""
from ollama import chat
from ollama import ChatResponse

import requests
import json


# request访问
def llm_promt(content,port=11434):
    url = f"http://localhost:{port}/api/chat"
    payload={
        "model":"llama3.2",
        "messages":[
            {"role":"user",
             "content":content}
        ]
    }
    response = requests.post(url,json=payload)

    if response.status_code == 200:
        response_content = ""
        for line in response.iter_lines():
            if line:
                response_content += json.loads(line)["message"]["content"]
        return response_content
    else:
        return f"Error:{response.status_code} - {response.text}"





from openai import OpenAI
def openai_llm_old(model="llama3.1:latest"):
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system",
             "content": "你是一个画画高手，可以根据文字想象出完美的画面，而且还擅长古风的风格"},

            {"role":"system","content":"雪落山庄不是一座山庄。只是一个客栈。还是个很破很破的客栈。\n方圆百里也只有这一家客栈。它背靠一座高山。面朝一条大河。翻越那座山需要很久。越过那条河也并不容易。所以成了赶路人中途歇息的必选之地。但是这几个月。雪落山庄的生意并不是很好。因为正如它的名字。一场雪落了很久很久。阻挡了来路。封住了去处。萧瑟穿着白色的裘皮大衣靠在门口。看着窗外漫天飞舞的雪花。轻轻叹了一口气。这一声。叹得如同他的名字一般萧瑟。三三两两的小二正趴在桌上打盹儿。偶尔醒过来也是给冻醒的。猛地哆嗦一下。惊醒过来。扫视一圈。却见依旧只有那个自负风雅的老板靠在那里看雪。于是裹了裹身上破旧的大衣。当然他们也会忍不住在心里抱怨几句：本来店里还有几个不愿在风雪天赶路而打算住下来的客人。但因为老板一直舍不得出钱整修客栈。以至于每间客房都是漏风的。客人们冻了几天后便宁愿挨风雪吹刮的苦也毅然上路了。这位名叫萧瑟的老板曾经训诫他们：“咱们这客栈。背靠青山。面朝绿水。如果房间再多些颓败感。就更显风雅了。这才是旅途中人热衷的感觉。\n”小二不懂。问：“那究竟是什么感觉？”萧瑟故作高深地摇了摇头：“唉。\n自然是在路上的感觉啊。”小二似懂非懂地点了点头。直到有一天。\n一个赶路的大汉大半夜实在受不住被风吹得吱嘎吱嘎响的窗户。\n一拳把房间打出了一个大窟窿。然后。被老板留下罚做了一个月的苦力。\n那大汉倒不是没有反抗。只是他刚举起拳头。就被萧瑟打出了门。他刚站起来。\n就见萧瑟顺手抄起一根棍子。那根棍子还没打下去。大汉就跪倒在地了。其实。\n关于那根棍子究竟有没有打下去。小二们是有争议的。有一位眼尖的小二说。\n他仿佛看到那根棍子微微抖动了一下。舞出了虚虚幻幻数朵棍花。那一瞬间。\n这个摇摇欲坠的客栈几乎都抖了一抖。但是那个汉子毕竟还是毫发无损的。\n所以谁也不能确定那根棍子是不是真的打了下去。只是那一个月的时间。\n他一句话都没再敢多说。别人问他。他就跑。萧瑟叹完一口气后就开始算账。\n他琢磨着把客栈卖掉。毕竟百里之外鸿路镇上的李员外早前也提过几次。\n可现在就算他想买。也得先找着他的人才行。或者先辞退几个小二。\n可这天寒地冻的。几个没什么功夫底子的小二辞退了以后怕是没有别的去处。\n突然。萧瑟脑中灵光一闪。既然辞退了小二后他们无处可去。\n不就得住下了？住下了就是客官。就得掏银子啊。\n问题不就解决了吗？萧瑟脸上不禁露出了欣慰的笑容。正当他想明白此事。\n心中大为舒畅的时候。突然看到不远的地方似乎有一团红色闪了一下。\n他眨了眨眼睛。想是自己看错了。可那红色却分明越来越明显了。\n他再眨了眨眼睛。便懒洋洋地喊道：“来客人了。”查看上面的文本，然后扮演一个文本编辑来回答问题。"},
            {"role":"user","content":"这个文本里的故事类型：历史奇幻 时代背景：玄幻小说中的古代，人物要符合故事类型和时代背景， 主角有哪几个， 每个角色的性别年龄穿着是啥？没外观描述的直接猜测，尽量精简 格式按照：故事类型：（故事类型）\n时代背景：（时代背景）\n主角1：（名字，编号AA，性别，年龄，发型和颜色，衣服类型和颜色 ）\n主角2：（名字，编号BB，性别，年龄，发型和颜色，衣服类型和颜色  ）\n主角3........ ，不知道的直接猜测设定，有头发的都设置为黑色，例如：（拉拉，AA，男，白色短发，黑色西装，20岁）或者（我，BB，女，黄色短发，紫色连衣裙，25岁）等.注意这里是例子实际细节要符合剧本.每个角色的衣服颜色要不同，衣服类型要不同，年龄要不同，外观细节要不同，必须包含AA BB等编号，不能出不详 未知等字 中文回答。"}
        ]
    )
    print(response.choices[0].message.content)

def openai_llm(messages,model="llama3.1:latest"):
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    response = client.chat.completions.create(
        model="llama3.2",
        messages=messages
    )
    return response.choices[0].message.content

from langchain_community.llms import Ollama

def langchain_llm():
    host="localhost"
    port="11434"

    llm=Ollama(base_url=f"http://{host}:{port}",model="llama3.1:latest",temperature=0)

    res=llm.invoke("介绍一下杭州的旅游景点")
    print(res)

from llama_index.llms.ollama import Ollama

def llama_api():
    host="localhost"
    port="11434"
    llm = Ollama(base_url=f"http://{host}:{port}",model="llama3.1:latest",request_timeout=30.0)

    # response = llm.chat(messages=[{"role":"user","content":"你是谁"}])
    #
    # print(response)


    response = llm.complete("介绍一下杭州的旅游景点")

    print(response)
import ollama
import json

def ollama_api():
    host ="localhost"
    port="11434"

    client = ollama.Client(host=f"http://{host}:{port}")

    res = client.chat(model="llama3.1:latest",messages=[{"role":"user","content":"介绍一下杭州的旅游景点"}],options={"temperature":0})


    print(res.message.content)





if __name__ == '__main__':
    # user_input = "介绍一下杭州的旅游景点"
    # response = send_message_to_ollama(user_input)
    # print("Ollama's response:")
    # print(response)
    openai_llm_old()

