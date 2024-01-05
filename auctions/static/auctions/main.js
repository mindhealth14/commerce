$(".open").on("click", function(){
    $(".popup, .popup-content").addClass("active");
    });


$(".close, .popup").on("click", function(){
    $(".popup, .popup-content").removeClass("active");
    });

 function myFunction() {
    alert("The seller can not place bid!");
      }
        
const addwatch = "Add to watchlist";
const remwatch = "Remove watchlist";


function watchlist() {
    let watchList = document.querySelector('#watchlist');

    if (watchList.innerHTML == 'Add to Watchlist')  {
        watchList.innerHTML = 'Remove watchlist'
    } else {
        watchList.innerHTML = 'Add to Watchlist';
    }

}
           

function handleMsg(){
    const watch = document.querySelector('.own-list');
    if (watch.style.display == 'none' ){
           watch.style.display = 'block'
    } else {
        watch.style.display = 'none'
    }
           
    
    
    
    
}