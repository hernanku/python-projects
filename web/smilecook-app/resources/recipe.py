from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe, recipe_list

# create the RecipeListResource class which inherits from flask_restful.Resource
class RecipeListResource(Resource):

    def get(self):
        # declare empty list to write recipe data
        data = []

        # loop through list of recipes from models, 
        # get all recipes that are not published and write to data list.
        for recipe in recipe_list:
            if recipe.is_publish is True:
                data.append(recipe.data)

        # return data to user.
        return {'data': data}, HTTPStatus.OK


    def post(self):

        # define data required for post request
        recipe = Recipe(
            name=data['name'],
            num_of_servings=data['num_of_servings'],
            cook_time=data['cook_time'],
            directions=data['directions']
            )

        # add data to recipe list
        recipe_list.append(recipe)

        # return created recipe data to user.
        return recipe.data, HTTPStatus.CREATED



# create the RecipeResource class which inherits from flask_restful.Resource
class RecipeResource(Resource):

    def get(self, recipe_id):
        # getting a single recipe id by looping through recipe_list and
        # getting those recipes with ids that have is_publish = True
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish == True ), None)

        # if the recipe is not found in recipe_list, 
        # return NOT_FOUND http status error.
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # otherwise return the recipe data and an OK http status
        return recipe.data, HTTPStatus.OK


    # put function to handle recipe update
    def put(self, recipe_id):
        # get recipe data details from request call (request.get_json())
        data = request.get_json()

        # getting a single recipe id by looping through recipe_list and
        # getting the recipe id to update
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        # if the recipe is not found in recipe_list, 
        # return NOT_FOUND http status error.
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # update data
        recipe.name = data['name']
        recipe.description = data['description']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.direction = data['direction']

        # return data and an OK http status
        return recipe.data, HTTPStatus.OK


class RecipePublishResource(Resource):
    # define put function to handle publishing recipe.
    def put(self, recipe_id):
        # getting a single recipe id by looping through recipe_list and getting the recipe id.
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # publish the recipe
        recipe.is_publish = True

        # return no data and the NO_CONTENT http status error.
        return {}, HTTPStatus.NO_CONTENT


    def delete(self, recipe_id):
        # getting a single recipe id by looping through recipe_list and getting the recipe id.
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # unpublish the recipe
        recipe.is_publish = False

        # return no data and the NO_CONTENT http status error.
        return {}, HTTPStatus.NO_CONTENT





