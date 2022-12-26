from celery import app
from .services import BookService


@app.shared_task
def update_books():
    book_service = BookService()

    df = book_service.fetch_books()
    book_service.clean_df(df)
    book_service.append_cover_column(df)

    for it, book in df.iterrows():
        if not book_service.is_exist(book):
            book_service.create_book(book)
            continue
        book_service.update_status(book)
