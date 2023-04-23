const apiUrl = "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=900917e1c843409288a40c7c9330fcb9";
const articlesContainer = document.querySelector(".articles");
const browseMoreButton = document.querySelector(".browse-more");
let currentPage = 1;
let pageSize = 5;
async function fetchNews(page) {
  try {
    const response = await fetch(`${apiUrl}&page=${page}&pageSize=${pageSize}`);
    const data = await response.json();
    articlesContainer.innerHTML = "";
    for (let article of data.articles) {
      const articleDiv = document.createElement("div");
      articleDiv.classList.add("article");
      const thumbnailDiv = document.createElement("div");
      thumbnailDiv.classList.add("thumbnail");
      const thumbnailImg = document.createElement("img");
      thumbnailImg.src = article.urlToImage;
      thumbnailImg.alt = article.title;
      thumbnailDiv.appendChild(thumbnailImg);
      articleDiv.appendChild(thumbnailDiv);
      const contentDiv = document.createElement("div");
      contentDiv.classList.add("content");
      const headline = document.createElement("h2");
      headline.textContent = article.title;
      contentDiv.appendChild(headline);
      const descriptionWrapper = document.createElement("div");
      descriptionWrapper.classList.add("description-wrapper"); 
      const description = document.createElement("p");
      description.textContent = article.description;
      descriptionWrapper.appendChild(description);
      contentDiv.appendChild(descriptionWrapper);
      const readMoreLink = document.createElement("a");
      readMoreLink.href = article.url;
      readMoreLink.textContent = "Read More";
      readMoreLink.classList.add("read-more");
      contentDiv.appendChild(readMoreLink);
      articleDiv.appendChild(contentDiv);
      articlesContainer.appendChild(articleDiv);
    }
    const totalResults = data.totalResults;
    const totalPages = Math.ceil(totalResults / pageSize);
    if (currentPage < totalPages) {
      browseMoreButton.style.display = "block";
    } else {
      browseMoreButton.style.display = "none";
    }
  } catch (error) {
    console.log(error);
  }
}
fetchNews(currentPage);
browseMoreButton.addEventListener("click", () => {
  currentPage++;
  fetchNews(currentPage);
});
articlesContainer.addEventListener("click", (event) => {
  const target = event.target;
  if (target.classList.contains("read-more")) {
    event.preventDefault();
    window.open(target.href, "_blank");
  }
});