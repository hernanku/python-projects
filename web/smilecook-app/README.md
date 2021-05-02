# Smile Cook recipe flask api app



**Endpoint design table.**
| HTTP Verp | Description | Methods to handle the requests | url |
| GET | Gets all the recipes | RecipeListResource.get | http://localhost:5000/recipes |
| POST | Creates a recipe | RecipeListResource.post | http://localhost:5000/recipes |
| GET | Gets a recipe | RecipeResource.get | http://localhost:5000/recipes/1 |
| PUT | Updates a recipe | RecipeResource.put | http://localhost:5000/recipes/1 |
| DELETE | Deletes a recipe | RecipeResource.delete | http://localhost:5000/recipes/1 |
| PUT | Sets a recipe to published | RecipePublishResource.put | http://localhost:5000/recipes/1/publish |
| DELETE | Sets a recipe to draft | RecipePublishResource.delete | http://localhost:5000/recipes/1/publish |


