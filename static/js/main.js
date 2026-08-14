// static/js/main.js

// Fetch and display books from GET /api/books/
async function fetchBooks() {
    try {
        const response = await fetch('/api/books/');
        const result = await response.json();

        const list = document.getElementById('bookList');
        list.innerHTML = '';

        if (result.status === 'success') {
            result.data.forEach(book => {
                const li = document.createElement('li');
                li.textContent = `[ID: ${book.book_id}] ${book.title} by ${book.author} (${book.status})`;
                list.appendChild(li);
            });
        }
    } catch (error) {
        console.error('Error fetching books:', error);
    }
}

// Send new book data to POST /api/books/
document.getElementById('addBookForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const bookData = {
        book_id: parseInt(document.getElementById('book_id').value),
        title: document.getElementById('title').value,
        subject: document.getElementById('subject').value,
        author: document.getElementById('author').value,
        isbn: document.getElementById('isbn').value,
        status: document.getElementById('status').value
    };

    try {
        const response = await fetch('/api/books/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookData)
        });

        const result = await response.json();
        alert(result.message);
        
        if (response.ok) {
            document.getElementById('addBookForm').reset();
            fetchBooks();
        }
    } catch (error) {
        console.error('Error adding book:', error);
    }
});

// Load books on initial page load
window.onload = fetchBooks;
