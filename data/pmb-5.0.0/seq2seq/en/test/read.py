import re

if __name__ == '__main__':
    with open("long.sbn", "r", encoding="utf-8") as f:
        text = f.readlines()
        sbn_text = ""
        for t in text:
            sbn = t.split("\t")[-1]
            sbn_text += sbn

        unique_uppercase_words = set()  # 使用集合来存储唯一的单词

        # 移除所有在双引号内的内容
        text_without_quotes = re.sub(r'"[^"]*"', '', sbn_text)

        # 使用正则表达式查找所有大写单词
        uppercase_words = re.findall(r'\b[A-Z]+\b', text_without_quotes)

        for word in uppercase_words:
            unique_uppercase_words.add(word)  # 添加到集合中，自动去重

        print("Unique uppercase words:", unique_uppercase_words)