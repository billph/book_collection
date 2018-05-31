const getBookByISBN = async isbn => {
  const data = await fetch(
    `https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}`,
    {
      method: "GET"
    }
  );

  if (!data.ok) {
    getWarningMessage("Speelings are wrong or words do not exist");
    return false;
  }
  console.log(data);
  const result = await data.json();
  return result.items.length == 0 ? false : result.items[0].volumeInfo;
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
