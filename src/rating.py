from member import Member


class Rating:
    """
    Represents a rating given by a member to a book in a book club.
    """

    def __init__(self, member: "Member", book: "Book", num_stars: float) -> None:
        if num_stars < 0 or num_stars > 5:
            raise ValueError("Rating must be between 0 and 5.")

        self.member = member
        self.book = book
        self.num_stars = num_stars
