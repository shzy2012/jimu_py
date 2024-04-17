from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import json
import os
import uuid

os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'  # 2G = 0.294


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf'}


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "."

# 加载模型
model = SentenceTransformer('moka-ai/m3e-base')


text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=10,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/embedding', methods=['POST'])
def embedding():
    try:
        sentence = request.get_json()["sentence"].encode('utf-8')
        print("开始处理:", sentence)
        embeddings = model.encode(sentence)
        data = {
            "sentence": sentence,
            "vector": embeddings.tolist(),
        }
        print("处理完成:", sentence)
        return json.dumps(data)
    except Exception as e:
        return jsonify(e)


@app.route('/embedding/file', methods=['POST'])
def embeddingFile():
    filepath = ""
    try:
        if 'file' not in request.files:
            raise Exception("缺少文件")

        file = request.files['file']
        print(file)
        if file.filename == '':
            raise Exception("缺少文件")

        if not allowed_file(file.filename):
            raise Exception("非法文件")

        filename = secure_filename(file.filename)
        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'], str(uuid.uuid4())+"."+filename)
        file.save(filepath)
        print("开始处理:", filepath)

        # load pdf
        loader = PyPDFLoader(filepath)
        pages = loader.load_and_split()
        segments = text_splitter.split_documents(pages)
        sentences = [seg.page_content for seg in segments]
        embeddings = model.encode(sentences)
        result = []
        for i in range(len(segments)):
            result.append(
                {"page_content": segments[i].page_content, "metadata":  {
                    "source": file.filename,
                    "page": segments[i].metadata.get("page")
                }, "vector": embeddings[i].tolist()})

        print("处理完成:", len(result))
        return json.dumps(result)
    except Exception as e:
        print("处理失败:", e)
        return str(e)
    finally:
        os.remove(filepath)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10003)
