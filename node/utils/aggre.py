from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def find_most_similar_sentence(tasks):
    """
    给定一个任务列表 (task_id, sentence)，找到与其他句子平均相似度最高的句子及其相似度。

    Parameters:
        tasks (list of tuples): 任务列表，每个元素为 (task_id, sentence)。

    Returns:
        tuple: 任务 ID，最佳句子及其相似度值 (int, str, float)。
    """
    if not tasks or len(tasks) < 2:
        raise ValueError("任务列表至少需要包含两个任务进行相似度计算。")

    # 提取句子列表
    sentences = [task[1] for task in tasks]

    # 使用 TF-IDF 向量化句子
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # 计算相似度矩阵
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # 计算每个句子的平均相似度（排除自身的相似度）
    n = len(sentences)
    average_similarity = (
        similarity_matrix.sum(axis=1) - np.diag(similarity_matrix)
    ) / (n - 1)

    # 找到平均相似度最高的句子
    most_similar_idx = np.argmax(average_similarity)
    most_similar_sentence = sentences[most_similar_idx]
    highest_similarity = average_similarity[most_similar_idx]

    # 返回 task_id 和相似度最高的句子及其相似度
    most_similar_task = tasks[most_similar_idx]
    return most_similar_task[0], most_similar_sentence, highest_similarity


# 加载BERT模型和tokenizer
def load_bert_model(model_name="bert-base-uncased"):
    """
    加载BERT模型和Tokenizer
    """
    tokenizer = BertTokenizer.from_pretrained(
        model_name, clean_up_tokenization_spaces=True
    )
    model = BertModel.from_pretrained(model_name)
    return tokenizer, model


# 编码句子
def encode_sentences(sentences, tokenizer, model):
    """
    将句子编码为BERT嵌入
    """
    embeddings = []
    for sentence in sentences:
        # Tokenize输入的句子
        inputs = tokenizer(
            sentence, return_tensors="pt", padding=True, truncation=True, max_length=512
        )

        # 获取BERT的输出
        with torch.no_grad():
            outputs = model(**inputs)

        # 获取句子的嵌入，通常是[CLS] token的向量表示
        sentence_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        embeddings.append(sentence_embedding)

    return np.array(embeddings)


# 计算最优句子
def find_most_similar_sentence_bert(tasks, node_weight, model_name="./node/model/"):
    """
    给定任务列表 [(task_id, sentence)]，返回平均相似度最高的句子及其相似度。
    """
    if not tasks or len(tasks) < 2:
        raise ValueError("任务列表至少需要包含两个任务进行相似度计算。")

    # 加载BERT模型 (load SBERT Model)
    tokenizer, model = load_bert_model(model_name)

    # 提取句子列表
    sentences = [task[1] for task in tasks]

    # 将句子编码为BERT嵌入
    embeddings = encode_sentences(sentences, tokenizer, model)

    # 计算相似度矩阵
    similarity_matrix = cosine_similarity(embeddings)

    # 计算每个句子的平均相似度（排除自身的相似度）
    n = len(sentences)
    average_similarity = (
        similarity_matrix.sum(axis=1) - np.diag(similarity_matrix)
    ) / (n - 1)
    
    old = sum(average_similarity)
    new = sum(node_weight * average_similarity)
    average_similarity = (old / new) * node_weight * average_similarity
    

    # 找到平均相似度最高的句子
    most_similar_idx = np.argmax(average_similarity)
    most_similar_sentence = sentences[most_similar_idx]
    highest_similarity = average_similarity[most_similar_idx]

    # 返回 task_id 和相似度最高的句子及其相似度
    most_similar_task = tasks[most_similar_idx]
    return most_similar_task[0], most_similar_sentence, highest_similarity, average_similarity
