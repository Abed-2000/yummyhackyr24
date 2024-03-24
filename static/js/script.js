function getAllRecipes(category){
    var xhr = new XMLHttpRequest();
    var url = window.location.href + "/searchcategory";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);

            var mealTitle = document.getElementById('mealstitle');
            mealTitle.innerHTML = 'All ' + category + ' Meals';

            var startingObject = document.getElementById('startRecipesObject');

            for (x=0; x < response['meals'].length; x++){
                var mealName = response['meals'][x]['strMeal'];
                var mealCode = response['meals'][x]['idMeal'];
                var mealPicture = response['meals'][x]['strMealThumb'];

                var mealCard = '<div class="row w-100 p-1"><div class="card w-100"><div class="card-body"><div class="container"><div class="row"><div class="col-2"><img alt="food image" src=' + mealPicture + ' class="img-fluid"></div><div class="col"><h5 class="card-title">' + mealName + '</h5><p class="card-text">' + mealCode + '</p><a href="/recipe/' + mealCode +'" class="btn btn-primary">View Recipe</a></div></div></div></div></div></div>';
                startingObject.insertAdjacentHTML('afterend', mealCard);
            }
        }

    }; 

    var data = JSON.stringify({"category": category});
    xhr.send(data);
};

document.addEventListener('DOMContentLoaded', function () {
    var likeButton = document.getElementById('like-button');
    likeButton.addEventListener('click', function () {
    if (likeButton.classList.contains('btn-secondary')) {                
        likeButton.classList.remove('btn-secondary');
        likeButton.classList.add('btn-danger');
        likeButton.innerText = 'Liked!';
    } else {
        likeButton.classList.remove('btn-danger');
        likeButton.classList.add('btn-secondary');
        likeButton.innerText = 'Like <3';
    }
    });
});