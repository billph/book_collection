const getBookByISBN = async isbn => {
  const data = await fetch(`https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}`, {
    method: "GET",
  });

  if (!data.ok) {
    getWarningMessage("Speelings are wrong or words do not exist");
    return false;
  }

  const result = await data.json();
  return result.items.length == 0 ? false : result.items[0].volumeInfo
};
