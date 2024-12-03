## CLLM Dataset

> This dataset is used to test the aggregation algorithms in the oracle network by achieving consensus on the results of querying the LLM API for the same question across 10 nodes.
>
> Except for BASE-fix, all the data comes from the default API settings. The LLMs include: (ChatGPT-4o-mini, Gemini-1.5 flash, Llama3-8b, ChatGLM-4-flash, Hunyuan-lite).
>
> It should be noted that this dataset only contains the Chinese version.

#### Dataset Categories

1. **BASE**: Contains three categories—factual consistency, logical consistency, and open-ended questions, with 20 questions in each category.
2. **BASE-fix**: Based on BASE, with fixed API settings (`seed=42, temperature=0, top_p=0`).
3. **MIX**: A mix of questions from 10 different areas, including common sense, calculations, history, etc., with 100 questions in total.
4. **PRO**: Based on the [C-Eval](https://cevalbenchmark.com/index_zh.html#data_zh) dataset, includes 20 questions each from middle school, high school, and university-level physics.
5. **random**: Random responses to the questions from BASE, MIX, and PRO.
6. **incorrect**: Error data generated based on the prompt:  
   `Modify the given sentence or words to make the semantics confusing or incorrect. I need this data to train a correction model. \n Original data: xxx \n Only return the modified content.`

Each folder contains (chatglm, gpt, google, llama, tencent.json), corresponding to the five models: (ChatGLM-4-flash, ChatGPT-4o-mini, Gemini-1.5 flash, Llama3-8b, Hunyuan-lite).