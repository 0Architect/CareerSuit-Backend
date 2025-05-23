import json

success_stories = {
    "Sanguine-Choleric": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/TechCrunch_Disrupt_San_Francisco_2019_-_Day_1_%2848834070763%29_%28cropped%29.jpg/640px-TechCrunch_Disrupt_San_Francisco_2019_-_Day_1_%2848834070763%29_%28cropped%29.jpg", "name": "Will Smith", "description": "Energetic and charismatic actor and entrepreneur known for his confident and ambitious personality."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Tony_Robbins.jpg/230px-Tony_Robbins.jpg", "name": "Tony Robbins", "description": "High-energy motivational speaker and entrepreneur, inspiring millions worldwide."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Dwayne_Johnson_2%2C_2013.jpg", "name": "Dwayne 'The Rock' Johnson", "description": "Actor and entrepreneur, known for his infectious enthusiasm and drive."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/8/88/Shonda_Rhimes_at_the_75th_Annual_Peabody_Awards_%28cropped%29.jpg", "name": "Shonda Rhimes", "description": "Successful TV producer and writer, known for her dynamic leadership in the entertainment industry."}
    ],
    "Sanguine-Melancholy": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/5/59/Robin_Williams_Happy_Feet_premiere.jpg", "name": "Robin Williams", "description": "Comedic genius with a deep, introspective side that fueled his legendary performances."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Dickens_Gurney_head.jpg", "name": "Charles Dickens", "description": "Writer known for his engaging storytelling combined with deep social critique."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Lady_Gaga_Vogue_2024_02.jpg", "name": "Lady Gaga", "description": "Creative and expressive artist with an emotional depth reflected in her music and activism."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/e/ed/Jim_Carrey_2020_cropped.jpg", "name": "Jim Carrey", "description": "Actor with an energetic, humorous persona but also a reflective and philosophical mind."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Ed_Sheeran-6826_%28cropped%29.jpg", "name": "Ed Sheeran", "description": "Singer-songwriter whose emotional lyrics and charisma captivate audiences worldwide."}
    ],
    "Sanguine-Phlegmatic": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Ellen_DeGeneres_2011.jpg", "name": "Ellen DeGeneres", "description": "Talk show host with a relaxed and humorous approach, spreading joy and positivity."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Jimmy_Fallon%2C_Montclair_Film_Festival%2C_2013.jpg", "name": "Jimmy Fallon", "description": "Comedic and charming late-night host known for his lighthearted and friendly personality."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Jennifer_Aniston_2011_%28cropped_2%29.jpg", "name": "Jennifer Aniston", "description": "Actress beloved for her warm and relatable on-screen presence."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/3/35/John_Legend_May_2022.jpg", "name": "John Legend", "description": "Talented musician and philanthropist known for his soulful voice and calm demeanor."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Paul_McCartney_.jpg", "name": "Paul McCartney", "description": "Legendary musician known for his upbeat personality and timeless music."}
    ],
    "Choleric-Sanguine": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/9/91/Jeff_Bezos%27_iconic_laugh_crop.jpg", "name": "Jeff Bezos", "description": "Founder of Amazon, balancing relentless ambition with calculated decision-making."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/5/56/Alexander_the_Great%2C_from_Alexandria%2C_Egypt%2C_3rd_cent._BCE%2C_Ny_Carlsberg_Glyptotek%2C_Copenhagen_%285%29_%2836375553176%29.jpg", "name": "Alexander the Great", "description": "Bold and ambitious military leader who conquered vast territories with his decisive leadership and charismatic presence."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/5/5b/Theodore_Roosevelt_by_the_Pach_Bros.jpg", "name": "Theodore Roosevelt", "description": "Energetic U.S. president known for his aggressive leadership style and dynamic public presence."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Richard_Branson_March_2015_%28cropped%29.jpg", "name": "Richard Branson", "description": "Founder of Virgin Group, known for his adventurous spirit and high-energy approach to entrepreneurship."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Oprah_Winfrey_2016.jpg", "name": "Oprah Winfrey", "description": "Influential media mogul and philanthropist, known for her charismatic leadership and emotional intelligence."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/3/33/Muhammad_Ali%2C_gtfy.00140.jpg", "name": "Muhammad Ali", "description": "Legendary boxer with a bold, confident personality and an unmatched ability to inspire people."}
    ],
    "Choleric-Melancholy": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/b/b9/Steve_Jobs_Headshot_2010-CROP.jpg", "name": "Steve Jobs", "description": "Visionary leader who combined charisma with bold decision-making to revolutionize technology."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Elon_Musk_Royal_Society_crop.jpg", "name": "Elon Musk", "description": "Visionary entrepreneur with a relentless drive for innovation and deep analytical thinking."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/f/fd/Angela_Merkel_%282008%29.jpg", "name": "Angela Merkel", "description": "Former German chancellor known for her calculated decision-making and strong leadership."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Margaret_Thatcher_%281983%29.jpg", "name": "Margaret Thatcher", "description": "Determined and strategic leader who reshaped Britain's economic policies."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/2/27/Santi_di_Tito_-_Niccolo_Machiavelli%27s_portrait_headcrop.jpg", "name": "Niccolò Machiavelli", "description": "Political thinker known for his strategic and pragmatic philosophy on power."}
    ],
    "Choleric-Phlegmatic": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/5/53/Simon_sinek.jpg", "name": "Simon Sinek", "description": "Leadership expert and motivational speaker known for his structured, inspiring approach."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/4/42/Condoleezza_Rice_cropped.jpg", "name": "Condoleezza Rice", "description": "Former U.S. Secretary of State, known for her diplomatic and strategic mindset."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/5/51/%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_%D0%9F%D1%83%D1%82%D0%B8%D0%BD_%2818-06-2023%29_%28cropped%29.jpg", "name": "Vladimir Putin", "description": "Political leader who exhibits strong control and a strategic, reserved approach to governance."}
    ],
    "Melancholy-Sanguine": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Freddie_Mercury_performing_in_New_Haven%2C_CT%2C_November_1977.jpg", "name": "Freddie Mercury", "description": "Iconic musician with a dramatic stage presence and deeply emotional songwriting."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/3/30/Emily_Dickinson_writing_a_poem_in_her_bedroom.jpg", "name": "Emily Dickinson", "description": "Poet known for her introspective yet imaginative writing."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project_%28454045%29.jpg", "name": "Vincent van Gogh", "description": "Renowned painter who deeply analyzed human emotions and expressed them through his Melancholy yet expressive artwork."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/8/8d/JK_Rowling_1999.jpg", "name": "J.K. Rowling", "description": "Author of 'Harry Potter,' blending creativity with deep themes of human nature."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Heath_Ledger.jpg", "name": "Heath Ledger", "description": "Talented actor known for his emotional depth and commitment to complex roles."}
    ],
    "Melancholy-Choleric": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/c/cc/Bill_Gates%2C_September_2024.jpg", "name": "Bill Gates", "description": "Tech visionary and philanthropist who combines strategic leadership with a calm demeanor."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/5/50/Sir_Isaac_Newton_by_Sir_Godfrey_Kneller%2C_Bt.jpg", "name": "Isaac Newton", "description": "Brilliant scientist known for his rigorous work ethic and groundbreaking discoveries."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Mariecurie.jpg", "name": "Marie Curie", "description": "Pioneering scientist whose methodical research in radioactivity revolutionized physics and medicine."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/c/c9/Howard_Hughes_1938_%28cropped%29.jpg", "name": "Howard Hughes", "description": "Inventor and business tycoon with a relentless drive for perfection and control."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Arthur_Schopenhauer_by_J_Sch%C3%A4fer%2C_1859b.jpg", "name": "Arthur Schopenhauer", "description": "Philosopher with a deep, strategic mind focused on human nature and existential thought."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/9/92/El_Greco_%28Ethniki_Epitheorisis_1870%29.jpg", "name": "El Greco", "description": "Artist whose dramatic and meticulously crafted paintings reflect a Melancholy yet driven personality."}
    ],
    "Melancholy-Phlegmatic": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/4/44/Abraham_Lincoln_head_on_shoulders_photo_portrait.jpg", "name": "Abraham Lincoln", "description": "Thoughtful and patient leader who used his deep introspection and calm demeanor to navigate the U.S. through a civil war."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/d/da/Mother_Theresa_in_watercolour.png", "name": "Mother Teresa", "description": "Compassionate humanitarian, known for her patient and selfless service to others."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/d/d4/J._R._R._Tolkien%2C_ca._1925.jpg", "name": "J.R.R. Tolkien", "description": "Author of 'The Lord of the Rings,' known for his deep world-building and reflective storytelling."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/1/1f/Mahatma_Gandhi_%28114348265%29.jpg", "name": "Mahatma Gandhi", "description": "Nonviolent resistance leader, whose patience and deep sense of justice led to India’s independence."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/1/17/Fred_Rogers_and_Tatiana_Vedeneyeva_on_Set_of_Mister_Rogers%27_Neighborhood_%28cropped%29.jpg", "name": "Fred Rogers", "description": "Beloved television host, known for his gentle nature and deep care for children's emotional well-being."}
    ],
    "Phlegmatic-Sanguine": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/8/8d/President_Barack_Obama.jpg", "name": "Barack Obama", "description": "A calm yet assertive leader, known for his composed demeanor and strategic decision-making."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Bob_Marley_1976_press_photo.jpg", "name": "Bob Marley", "description": "Musician spreading peace and positivity through his calm yet uplifting music."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/3/33/Reuni%C3%A3o_com_o_ator_norte-americano_Keanu_Reeves_%2846806576944%29_%28cropped%29.jpg", "name": "Keanu Reeves", "description": "Actor known for his humble, kind, and down-to-earth personality."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/1/13/Tenzin_Gyatso_-_Trento_2013_01.JPG", "name": "Dalai Lama", "description": "Spiritual leader promoting peace and emotional balance worldwide."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/8/81/Weston_Library_Opening_by_John_Cairns_20.3.15-139_David_Attenborough.jpg", "name": "David Attenborough", "description": "Documentary narrator with a soothing, informative, and passionate approach to nature."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/1/17/Fred_Rogers_and_Tatiana_Vedeneyeva_on_Set_of_Mister_Rogers%27_Neighborhood_%28cropped%29.jpg", "name": "Mister Rogers", "description": "Children’s TV host known for his kindness and ability to connect with people warmly."}
    ],
    "Phlegmatic-Choleric": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/1/14/Nelson_Mandela-2008_%28edit%29.jpg", "name": "Nelson Mandela", "description": "Resilient and diplomatic, combining patience with firm leadership to achieve justice."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Angela_Bassett_2000.jpg", "name": "Angela Bassett", "description": "A composed yet commanding actress, known for her controlled yet powerful performances."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Warren_Buffett_at_the_2015_SelectUSA_Investment_Summit_%28cropped%29.jpg", "name": "Warren Buffett", "description": "Legendary investor, known for his patient, analytical approach to long-term success."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/0/06/Serena_Williams_US_Open_2013.jpg", "name": "Serena Williams", "description": "A focused and disciplined athlete, balancing her calm demeanor with fierce determination."}
    ],
    "Phlegmatic-Melancholy": [
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Steve_Wozniak_by_Gage_Skidmore.jpg", "name": "Steve Wozniak", "description": "Technical genius behind Apple, combining precision with an ambitious drive."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/0/00/CGJung.jpg", "name": "Carl Jung", "description": "Pioneering psychologist whose deep introspection led to groundbreaking theories in personality and human nature."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/8/82/George_Orwell%2C_c._1940_%2841928180381%29.jpg", "name": "George Orwell", "description": "Author of '1984,' using his observant and analytical mind to critique societal structures."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/5/5f/HarperLee_2007Nov05.jpg", "name": "Harper Lee", "description": "Author of 'To Kill a Mockingbird,' known for her quiet, observant nature and impactful storytelling."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/1/17/Alan_Turing_%281912-1954%29_in_1936_at_Princeton_University.jpg", "name": "Alan Turing", "description": "Mathematical genius who laid the foundation for modern computing while working in quiet brilliance."},
        {"imageURL": "https://upload.wikimedia.org/wikipedia/commons/9/99/Jane_Goodall_2010.jpg", "name": "Jane Goodall", "description": "Primatologist known for her patient, methodical research and deep connection to nature."}
    ]
}

with open("success_stories.json", "w", encoding="utf-8") as file:
    json.dump(success_stories, file, indent=4, ensure_ascii=False)