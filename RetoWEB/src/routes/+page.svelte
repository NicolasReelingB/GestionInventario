<script>
  import { onMount } from 'svelte';
  import { db } from '$lib/firebase';
  import { collection, getDocs, addDoc, deleteDoc, doc } from 'firebase/firestore';

  let recipes = [];
  let availableIngredients = {};
  let newRecipe = { name: '', ingredients: [] };
  let newIngredient = { name: '', amount: '' };
  let videoElement;
  let canvasElement;

  const fetchRecipes = async () => {
    const querySnapshot = await getDocs(collection(db, 'recipes'));
    recipes = querySnapshot.docs.map(doc => ({ ...doc.data(), id: doc.id, expanded: false }));
  };

  const addRecipe = async () => {
    await addDoc(collection(db, 'recipes'), newRecipe);
    newRecipe = { name: '', ingredients: [] };
    newIngredient = { name: '', amount: '' };
    fetchRecipes();
  };

  const deleteRecipe = async (id) => {
    await deleteDoc(doc(db, 'recipes', id));
    fetchRecipes();
  };

  const addIngredient = () => {
    newRecipe.ingredients.push({ ...newIngredient });
    newIngredient = { name: '', amount: '' };
  };

  const toggleRecipe = (id) => {
    recipes = recipes.map(recipe => {
      if (recipe.id === id) {
        recipe.expanded = !recipe.expanded;
      }
      return recipe;
    });
  };

  const calculatePossibleRecipes = (recipe) => {
    return Math.min(...recipe.ingredients.map(ingredient => {
      const availableAmount = availableIngredients[ingredient.name.toLowerCase()] || 0;
      return Math.floor(availableAmount / ingredient.amount) || 0;
    }));
  };

  const captureImage = () => {
    const context = canvasElement.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
    const imageData = canvasElement.toDataURL('image/jpeg');
    return imageData.split(',')[1]; // Get base64 part
  };

  const sendImageToBackend = async () => {
    const imageBase64 = captureImage();
    try {
      const response = await fetch('http://localhost:5000/process_image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageBase64 })
      });
      const data = await response.json();
      availableIngredients = data;
      console.log(availableIngredients);  // Debugging: Check the available ingredients
    } catch (error) {
      console.error('Error sending image:', error);
    }
  };

  async function uploadImage(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = async () => {
                const base64data = reader.result.split(',')[1];
                const response = await fetch('http://localhost:5000/process_image', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ image: base64data })
                });

                const data = await response.json();
                newIngredient = data;
                console.log(newIngredient)
            };
            reader.readAsDataURL(file);
        }
    }
  onMount(() => {
    fetchRecipes();

    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        videoElement.srcObject = stream;
        videoElement.play();
      })
      .catch(error => {
        console.error('Error accessing the camera:', error);
      });

    //setInterval(sendImageToBackend, 5000);  // Send image every 5 seconds
  });
</script>

<main>
  <h1>Recipe Manager</h1>

  <div>
    <h2>Current Ingredients</h2>
    <table>
      <thead>
        <tr>
          <th>Ingredient</th>
          <th>Amount</th>
        </tr>
      </thead>
      <tbody>
        {#each Object.entries(availableIngredients) as [name, amount]}
          <tr>
            <td>{name}</td>
            <td>{amount}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  <div>
    <h2>Camera</h2>
    <video bind:this={videoElement} width="640" height="480" autoplay></video>
    <canvas bind:this={canvasElement} width="640" height="480" style="display: none;"></canvas>
  </div>

  <div>
    <input type="file" accept="image/*" on:change={uploadImage} />
</div>

  <div>
    <h2>Recipes</h2>
    <div>
      <input bind:value={newRecipe.name} placeholder="Recipe name" />
    </div>
    <div>
      <input bind:value={newIngredient.name} placeholder="Ingredient name" />
      <input bind:value={newIngredient.amount} placeholder="Amount" />
      <button on:click={addIngredient}>Add Ingredient</button>
    </div>
    <ul>
      {#each newRecipe.ingredients as ingredient, index}
        <li>{ingredient.name}: {ingredient.amount}</li>
      {/each}
    </ul>
    <button on:click={addRecipe}>Add Recipe</button>
  </div>
  <ul>
    {#each recipes as recipe}
      <li class={recipe.expanded ? 'expanded' : 'collapsed'}>
        <div class="recipe-header">
          <h3>{recipe.name}</h3>
          <div class="buttons">
            <button on:click={() => deleteRecipe(recipe.id)}>Delete</button>
            <button on:click={() => toggleRecipe(recipe.id)}>
              {recipe.expanded ? '▲' : '▼'}
            </button>
          </div>
        </div>
        {#if recipe.expanded}
          <ul>
            {#each recipe.ingredients as ingredient}
              <li>{ingredient.name}: {ingredient.amount}</li>
            {/each}
          </ul>
          <p>Possible Recipes: {calculatePossibleRecipes(recipe)}</p>
        {/if}
      </li>
    {/each}
  </ul>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
    max-width: 800px;
  }
  h1 {
    color: #ff3e00;
    margin: 0.5em 0;
  }
  div {
    text-align: left;
    margin: 1em 0;
  }
  input {
    margin-right: 0.5em;
    padding: 0.5em;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  button {
    padding: 0.5em 1em;
    background-color: #ff3e00;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  ul {
    list-style: none;
    padding: 0;
  }
  li {
    margin: 1em 0;
    padding: 1em;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1em;
  }
  th, td {
    border: 1px solid #ccc;
    padding: 0.5em;
    text-align: left;
  }
  .collapsed {
    padding: 0.5em;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .recipe-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .buttons {
    display: flex;
    gap: 0.5em;
  }
</style>