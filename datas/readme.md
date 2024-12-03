## CLLM 数据集

> 用于测试预言机网络中的聚合算法，通过10个节点就同一问题询问LLM API的结果达成一致。
>
> 除BASE-fix外，所有的数据的来自默认API设置。LLM包括：(ChatGPT-4o-mini, Gemini-1.5 f lash, Llama3-8b, ChatGLM-4-flash, Hunyuan-lite）。
>
> 需要注意的是，本数据集仅包含中文版本。

#### 数据集分类

1. BASE：包含事实一致性、逻辑一致性、开放性问题三类，各20道。
2. BASE-fix：在BASE的基础上固定API中`seed=42，temperature=0,top_p=0`。
3. MIX：包含常识、计算、历史等10个方面的混合问题，共100道。
4. PRO：基于[C-Eval](https://cevalbenchmark.com/index_zh.html#data_zh) 数据集，包含初中、高中、大学物理题各20道。
5. random：对BASE、MIX、PRO中问题的随机回复
6. incorrect：基于Prompt`Modifythe givensentenceorwords tomake thesemanticsconfusingor incorrect. I need this data to traina correctionmodel. \n Originaldata: xxx \n Onlyreturnthemodifiedcontent.` 所生成的错误数据。

每个文件夹中包含（chatglm、gpt、google、llama、tencent.json），对应(ChatGLM-4-flash, ChatGPT-4o-mini, Gemini-1.5 f lash, Llama3-8b, Hunyuan-lite）五个模型。