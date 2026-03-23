from django.core.management.base import BaseCommand
from books.models import Book
from datetime import date

class Command(BaseCommand):
    help = 'Load sample books into the database'

    def handle(self, *args, **options):
        # Clear existing books
        Book.objects.all().delete()
        
        sample_books = [
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'description': 'A gripping tale of racial injustice and childhood innocence in the American South during the 1930s. Through the eyes of Scout Finch, we witness her father, lawyer Atticus Finch, defend a black man falsely accused of rape.',
                'price': 189.99,
                'isbn': '9780061120084',
                'publisher': 'Harper Perennial Modern Classics',
                'publication_date': date(2006, 5, 23),
                'pages': 324,
                'language': 'English',
                'stock': 15,
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'description': 'A dystopian social science fiction novel that follows the life of Winston Smith, a low-ranking member of the Party in Oceania, where independent thinking is a crime and reality is constantly manipulated.',
                'price': 159.99,
                'isbn': '9780451524935',
                'publisher': 'Signet Classics',
                'publication_date': date(1950, 7, 1),
                'pages': 328,
                'language': 'English',
                'stock': 20,
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'description': 'A romantic novel of manners that charts the emotional development of Elizabeth Bennet, who learns the error of making hasty judgments and comes to appreciate the difference between the superficial and the essential.',
                'price': 139.99,
                'isbn': '9780141439518',
                'publisher': 'Penguin Classics',
                'publication_date': date(2002, 12, 31),
                'pages': 432,
                'language': 'English',
                'stock': 12,
            },
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'description': 'Set in the Jazz Age on Long Island, the novel depicts narrator Nick Carraway\'s interactions with mysterious millionaire Jay Gatsby and Gatsby\'s obsession to reunite with his former lover, Daisy Buchanan.',
                'price': 149.99,
                'isbn': '9780743273565',
                'publisher': 'Scribner',
                'publication_date': date(2004, 9, 30),
                'pages': 180,
                'language': 'English',
                'stock': 18,
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'description': 'The story of Holden Caulfield, a teenager who leaves his prep school in Pennsylvania and goes underground in New York City for three days, dealing with issues of identity, connection, and alienation.',
                'price': 169.99,
                'isbn': '9780316769488',
                'publisher': 'Little, Brown and Company',
                'publication_date': date(2001, 5, 1),
                'pages': 277,
                'language': 'English',
                'stock': 8,
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'description': 'Bilbo Baggins, a hobbit enjoying his quiet life, is swept into an epic quest to reclaim the lost Dwarf Kingdom of Erebor from the fearsome dragon Smaug, accompanied by thirteen dwarves and the wizard Gandalf.',
                'price': 199.99,
                'isbn': '9780618260300',
                'publisher': 'Houghton Mifflin Harcourt',
                'publication_date': date(2002, 9, 23),
                'pages': 310,
                'language': 'English',
                'stock': 25,
            },
            {
                'title': 'Harry Potter and the Sorcerer\'s Stone',
                'author': 'J.K. Rowling',
                'description': 'Harry Potter, an orphan living with his abusive relatives, discovers on his eleventh birthday that he is a wizard and has been accepted at Hogwarts School of Witchcraft and Wizardry.',
                'price': 219.99,
                'isbn': '9780590353427',
                'publisher': 'Scholastic Inc.',
                'publication_date': date(1998, 10, 1),
                'pages': 309,
                'language': 'English',
                'stock': 30,
            },
            {
                'title': 'The Da Vinci Code',
                'author': 'Dan Brown',
                'description': 'A mystery thriller novel that follows symbologist Robert Langdon and cryptologist Sophie Neveu as they investigate a murder in the Louvre Museum and discover a battle between the Priory of Sion and Opus Dei.',
                'price': 179.99,
                'isbn': '9780307474278',
                'publisher': 'Anchor',
                'publication_date': date(2009, 3, 17),
                'pages': 689,
                'language': 'English',
                'stock': 14,
            },
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'description': 'A philosophical book that tells the story of Santiago, an Andalusian shepherd boy who dreams of finding treasure in the Egyptian pyramids and embarks on a journey that teaches him about following his heart.',
                'price': 129.99,
                'isbn': '9780061122415',
                'publisher': 'HarperOne',
                'publication_date': date(2006, 4, 25),
                'pages': 208,
                'language': 'English',
                'stock': 22,
            },
            {
                'title': 'Brave New World',
                'author': 'Aldous Huxley',
                'description': 'A dystopian novel set in a futuristic World State, where citizens are environmentally engineered into an intelligence-based social hierarchy, and the story explores the dangers of technology and mindless conformity.',
                'price': 159.99,
                'isbn': '9780060850524',
                'publisher': 'Harper Perennial Modern Classics',
                'publication_date': date(2006, 10, 17),
                'pages': 288,
                'language': 'English',
                'stock': 6,
            },
        ]
        
        created_count = 0
        for book_data in sample_books:
            book = Book.objects.create(**book_data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created book: {book.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample books!')
        )
