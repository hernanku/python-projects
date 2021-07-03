from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

# define recipe data
recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a loveley egg salad recipe'
    },
    {
        'id': 2,
        'name': 'Tomato Pasta',
        'description': 'This is a loveley tomato pasta recipe'
    }
]

# recipes route to get all recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    return jsonify(
        {
            'data': recipes
            }
        )

# route to get a particular recipe by recipe id
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if recipe:
        return jsonify(recipe)

    return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND


# route to add a recipe 
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')

    recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'description': description
    }

    recipes.append(recipe)

    return jsonify(recipe), HTTPStatus.CREATED    


# route to update a particular recipe
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    if not recipe:
        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

    data = request.get_json()

    recipe.update(
        {
            'name': data.get('name'),
            'description': data.get('description')
        }
    )

    return jsonify(recipe)



if __name__ == '__main__':
    app.run(host='0.0.0.0')

