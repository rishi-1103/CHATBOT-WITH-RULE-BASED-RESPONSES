import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> list:
    with open(file_path, 'r') as file:
        data: list = json.load(file)
        return data
    

def save_knowledge_base(file_path: str, data: list):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.5)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: list) -> str | None:
    for q in knowledge_base:
        if q["question"].lower() == question.lower():
            return q["answer"]
        
def chat_bot():
    knowledge_base: list = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')  
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base])
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Sam: {answer}')
        else:
            print('Sam: I don\'t know the answer. Can you teach me?') 
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base.append({"question": user_input, "answer": new_answer})
                save_knowledge_base('brain', knowledge_base)
                print('Sam: Thank You! I learned a new response!')

if __name__ == '__main__':
    chat_bot()
