from flask import Blueprint, request, flash, render_template, jsonify



blueprint = Blueprint('quote_generation', __name__)

@blueprint.route('/gpt', methods=['POST'])
def generate_quote_gpt():
    from app.services.GPT import QuoteGenerator
    json_data = request.get_json()
    prompt = json_data["prompt"]
    print(f"Quote submit pressed. {prompt}")
    generator = QuoteGenerator(prompt)
    # prompt = request.get_json()["prompt"]
    res = generator.generate()
    # threading.Thread(target=simulate_time_consuming_process, args=()).start()
    
    return jsonify(res)

@blueprint.route('/category', methods=['POST'])
def generate_quote_from_category():
    print("category selected")
    json_data = request.get_json()
    category = json_data['category']
    is_same_as_clippack = json_data['sameCategoryBln']
    clippackCategory = json_data['clippack']

    print("category:", category)
    print("bln:", is_same_as_clippack)
    print("clippack:", clippackCategory)
    print(f"category submit pressed. {category}")
    # threading.Thread(target=simulate_time_consuming_process, args=()).start()

    if is_same_as_clippack == 'true':
        res = clippackCategory
    else:
        res = category
    
    return jsonify(res)