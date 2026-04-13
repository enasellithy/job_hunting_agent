import os
import re
from cerebras.cloud.sdk import Cerebras

client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

def clean_ai_response(text):
    return re.sub(r'```python|```markdown|```', '', text, flags=re.IGNORECASE).strip()

def get_ai_completion(prompt):
    response = client.chat.completions.create(
        model="llama3.1-8b",
        messages=[{"role": "user", "content": prompt}]
    )
    return clean_ai_response(response.choices[0].message.content)

def process_file(file_path):
    with open(file_path, "r") as f:
        code = f.read()
    
    # 1. توليد التوثيق في ملف منفصل (.md)
    doc_prompt = f"Create a comprehensive documentation for this code in Markdown format. Explain functions, logic, and usage:\n{code}"
    doc_content = get_ai_completion(doc_prompt)
    
    doc_filename = f"docs/docs_{os.path.basename(file_path).replace('.py', '.md')}"
    with open(doc_filename, "w") as f:
        f.write(doc_content)
    
    # 2. توليد الاختبارات (كما في السابق)
    test_prompt = f"Create a robust unit test file for this code using 'unittest'. Return ONLY clean Python code:\n{code}"
    test_code = get_ai_completion(test_prompt)
    
    test_filename = f"tests/test_{os.path.basename(file_path)}"
    with open(test_filename, "w") as f:
        f.write(test_code)
        
    print(f"✅ Documented in docs/ and tested in tests/: {file_path}")

if __name__ == "__main__":
    # إنشاء المجلدات اللازمة
    for folder in ["tests", "docs"]:
        if not os.path.exists(folder): os.makedirs(folder)
        
    for file in os.listdir("."):
        if file.endswith(".py") and file != "app.py" and not file.startswith("test_") and not file.startswith("ai_generator"):
            process_file(file)