const getBookByISBN = async isbn => {
  const data = await fetch(
    `https://www.googleapis.com/books/v1/volumes?key=AIzaSyBGjLVK8mlt9ZxyHBp8bDKUvEknWzYQ28s&q=isbn:${isbn}`,
    {
      method: "GET"
    }
  );

  console.log(data)

  if (!data.ok) {
    throw "Failed retreiving data"
    getWarningMessage("Speelings are wrong or words do not exist");
    return false;
  }


  const result = await data.json();
  console.log(result)
  if (result.items) {
    return result.items.length == 0 ? false : result.items[0].volumeInfo;
  }
  throw "Cannot get book. Please try different one.";
};

const getRandomIndex = array => {
  return Math.floor(Math.random() * array.length);
};

const getListOfBooks = async username => {
  a = await $.ajax({
    method: "POST",
    contentType: "application/json",
    url: Flask.url_for("api.get_books", { _external: true }),
    data: JSON.stringify({ username })
  })
  
  return a.value
}

$.fn.extend({
  animateCss: function(animationName, callback) {
    var animationEnd = (function(el) {
      var animations = {
        animation: 'animationend',
        OAnimation: 'oAnimationEnd',
        MozAnimation: 'mozAnimationEnd',
        WebkitAnimation: 'webkitAnimationEnd',
      };

      for (var t in animations) {
        if (el.style[t] !== undefined) {
          return animations[t];
        }
      }
    })(document.createElement('div'));

    this.addClass('animated ' + animationName).one(animationEnd, function() {
      $(this).removeClass('animated ' + animationName);

      if (typeof callback === 'function') callback();
    });

    return this;
  },
});
