from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastProgram(Entity):
    """Refers to television or radio programs, including game shows, talk shows, documentaries, and series."""
    span: str  # Such as: "The Gale Storm Show", "12 Corazones", "Jonovision", "Trailer Park Boys", "Mozart in Prague", "Soweto TV"

@dataclass
class ArtFilm(Entity):
    """Refers to movies and cinema productions of any genre."""
    span: str  # Such as: "L'Atlantide", "The Shawshank Redemption", "Bosch", "Men in Her Diary", "Dances with Wolves", "Dune"

@dataclass
class ArtMusic(Entity):
    """Refers to songs, albums, musical compositions, ballads, and concert performances."""
    span: str  # Such as: "Atkinson, Danko and Ford", "Champion Lover", "Mass in C minor", "On the Loose", "The Boys of Wexford", "Free Fallin"

@dataclass
class ArtOther(Entity):
    """Refers to miscellaneous artistic works like sculptures, theatrical plays, music videos, or historic artifacts."""
    span: str  # Such as: "Venus de Milo", "The Today Show", "Cloud Gate", "Without the Prince", "Guys and Dolls", "Sphinx", "Lula and the Sailor"

@dataclass
class ArtPainting(Entity):
    """Refers to paintings, sketches, graffiti, or visual designs and lenses."""
    span: str  # Such as: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Kamichama Karin", "The Sacrament of the Last Supper", "Athenaeum Portrait"

@dataclass
class ArtWrittenart(Entity):
    """Refers to books, magazines, poems, scripts, theses, and other literary or written works."""
    span: str  # Such as: "Time", "The Seven Year Itch", "Imelda de' Lambertazzi", "Histories", "Adventure World Magazine", "Standard of Perfection"

@dataclass
class BuildingAirport(Entity):
    """Refers to airports, aviation terminals, and airfields."""
    span: str  # Such as: "Sheremetyevo International Airport", "Newark Liberty International Airport", "Zhuhai Airport", "Vienna International Airport"

@dataclass
class BuildingHospital(Entity):
    """Refers to medical facilities, hospitals, and clinics."""
    span: str  # Such as: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Huntington Hospital", "Brigham and Women’s Hospital"

@dataclass
class BuildingHotel(Entity):
    """Refers to hotels, resorts, and lodging establishments."""
    span: str  # Such as: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel", "Hotel Sacher Salzburg", "Pierre Hotel"

@dataclass
class BuildingLibrary(Entity):
    """Refers to libraries and institutional archives."""
    span: str  # Such as: "Bayerische Staatsbibliothek", "British Library", "Berlin State Library", "Edmon Low Library", "Jefferson Market Library"

@dataclass
class BuildingOther(Entity):
    """Refers to miscellaneous buildings such as museums, churches, recording studios, palaces, and drill halls."""
    span: str  # Such as: "Henry Ford Museum", "Alpha Recording Studios", "St John The Evangelist", "Palazzo Monte dei Poveri Vergognosi", "The Echo"

@dataclass
class BuildingRestaurant(Entity):
    """Refers to restaurants, cafes, delis, and fast-food outlets."""
    span: str  # Such as: "Trumbull dining hall", "Carnegie Deli", "Fatburger", "Morrison's", "Skyline", "McDonald's", "El Pollo Loco"

@dataclass
class BuildingSportsfacility(Entity):
    """Refers to arenas, stadiums, sports centers, and athletic fields."""
    span: str  # Such as: "Boston Garden", "Scotiabank Place", "ARCO Arena", "Appleton Arena", "Hughes Stadium", "Capital One Field"

@dataclass
class BuildingTheater(Entity):
    """Refers to theaters, opera houses, and stages for performing arts."""
    span: str  # Such as: "Sanders Theatre", "Pittsburgh Civic Light Opera", "Whitehall Theatre", "Hicks Theatre", "Piccadilly Theatre", "The Warehouse Theatre"

@dataclass
class EventAttackBattleWarMilitaryConflict(Entity):
    """Refers to wars, specific battles, military operations, and bombings."""
    span: str  # Such as: "Vietnam War", "Operation Zipper", "Battle of Romani", "World War I", "Corinthian War", "Bali bombing", "Battle of Taku Forts"

@dataclass
class EventDisaster(Entity):
    """Refers to natural disasters, famines, accidents, and environmental catastrophes."""
    span: str  # Such as: "1693 Sicily earthquake", "North Korean famine", "1912 North Mount Lyell Disaster", "Chernobyl accident", "Hurricane Opal"

@dataclass
class EventElection(Entity):
    """Refers to political elections, by-elections, and campaign cycles."""
    span: str  # Such as: "March 1898 elections", "Elections to the European Parliament", "1982 Mitcham and Morden by-election", "1940 presidential election"

@dataclass
class EventOther(Entity):
    """Refers to miscellaneous organized events like revolutions, movements, air shows, and art salons."""
    span: str  # Such as: "Masaryk Democratic Movement", "The Proms", "Romanian Revolution", "1995 Paris Air Show", "Salon des Indépendants"

@dataclass
class EventProtest(Entity):
    """Refers to revolutions, boycotts, rebellions, and organized protests."""
    span: str  # Such as: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Irish Rebellion of 1798", "Defiance Campaign", "Pro-Test Petition"

@dataclass
class EventSportsevent(Entity):
    """Refers to sporting tournaments, championships, matches, and cups."""
    span: str  # Such as: "Stanley Cup", "World Cup", "Giro d'Italia", "Basketball ID", "United States Figure Skating Championships"

@dataclass
class LocationGpe(Entity):
    """Refers to Geopolitical Entities like countries, cities, states, and provinces."""
    span: str  # Such as: "Croatia", "Europe", "Cornwall", "Michigan", "Germany", "Sweden", "United States", "Azerbaijani"

@dataclass
class LocationBodiesofwater(Entity):
    """Refers to rivers, lakes, seas, oceans, and bays."""
    span: str  # Such as: "Atatürk Dam Lake", "Arthur Kill", "East China Sea", "Jordan River", "Newark Bay", "Upper New York Bay", "Onkaparinga River"

@dataclass
class LocationIsland(Entity):
    """Refers to islands, archipelagos, and peninsulas."""
    span: str  # Such as: "Laccadives", "Maldives", "Mainland", "Shetland", "Long Island", "Khark Islalnd", "Annobón", "Staten Island"

@dataclass
class LocationMountain(Entity):
    """Refers to mountains, mountain ranges, peaks, and ridges."""
    span: str  # Such as: "Ruweisat Ridge", "Salamander Glacier", "Mount Diablo", "K2", "Himalayan", "Karakoram", "Innuitian Mountains"

@dataclass
class LocationOther(Entity):
    """Refers to miscellaneous locations like bridges, forests, valleys, and specific estates."""
    span: str  # Such as: "Cartuther", "Victoria line", "Camino Palmero", "West Gate Bridge", "Bintan Resorts", "Jawai Bandh forests", "Helike"

@dataclass
class LocationPark(Entity):
    """Refers to parks, conservation areas, and historical districts."""
    span: str  # Such as: "Gramercy Park", "Shenandoah National Park", "Millennium Park", "Yellowstone Park", "Wind Cave", "Dalymount Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Refers to roads, streets, highways, railway lines, and transit routes."""
    span: str  # Such as: "Friern Barnet Road", "North Jersey Coast Line", "Outerbridge Crossing", "State Route 151", "Claremont Avenue", "Salisbury Highway"

@dataclass
class OrganizationCompany(Entity):
    """Refers to private companies, corporations, and businesses."""
    span: str  # Such as: "Church's Chicken", "Taco Cabana", "WHL", "Warner Brothers", "Chiltern Air Support", "Braathens SAFE", "Hooper & Co."

@dataclass
class OrganizationEducation(Entity):
    """Refers to schools, universities, colleges, and educational academies."""
    span: str  # Such as: "Belfast Royal Academy", "MIT", "Barnard College", "Latvia University of Life Sciences", "University of Canterbury", "Harvard"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Refers to government bodies, courts, departments, and legislative assemblies."""
    span: str  # Such as: "Supreme Court", "Diet", "US Park Police", "Rajasthan government", "United States District Court"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Refers to news agencies, newspapers, television networks, and magazines."""
    span: str  # Such as: "Al Jazeera", "Clash", "TimeOut Melbourne", "Nickelodeon", "Sky Sports", "Pro Football Focus TV", "VH1"

@dataclass
class OrganizationOther(Entity):
    """Refers to miscellaneous organizations like armies, foundations, clubs, and councils."""
    span: str  # Such as: "IAEA", "4th Army", "SS Division Nordland", "Quixtar", "Leicester City Council", "John McAslan + Partners"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Refers to political parties and organizations."""
    span: str  # Such as: "Shimpotō", "Haq Movement", "National Liberal Party", "Republican", "BNG", "Democratic Party", "Socialist Party"

@dataclass
class OrganizationReligion(Entity):
    """Refers to religious denominations, sects, and organized religious groups."""
    span: str  # Such as: "Jewish", "Christian", "Episcopalians", "United Methodists", "United Protestant Church of France", "Buddhism"

@dataclass
class OrganizationShoworganization(Entity):
    """Refers to bands, orchestras, performing groups, and artistic ensembles."""
    span: str  # Such as: "Mr. Mister", "Yeah Yeah Yeahs", "New York Youth Symphony", "Yakshagana Himmela", "Collegium 1704"

@dataclass
class OrganizationSportsleague(Entity):
    """Refers to professional and collegiate sports leagues and conferences."""
    span: str  # Such as: "First Division", "NHL", "China League One", "Bundesliga", "F1", "Atlantic Coast Conference"

@dataclass
class OrganizationSportsteam(Entity):
    """Refers to specific sports teams and national athletic teams."""
    span: str  # Such as: "Arsenal", "Tottenham", "Luc Alphand Aventures", "Tre Kronor", "Utah Jazz", "Dallas Mavericks", "Wuhan Zall"

@dataclass
class OtherAstronomything(Entity):
    """Refers to stars, planets, constellations, asteroids, and celestial regions."""
    span: str  # Such as: "Algol", "42 Camelopardalis", "Sun", "Tandun III", "Ceres", "Birgitta", "Mars", "Asteroid Belt", "DC-7"

@dataclass
class OtherAward(Entity):
    """Refers to prizes, honors, medals, and prestigious recognitions."""
    span: str  # Such as: "Order of the Republic", "European Car of the Year", "Kodansha Manga Award", "Spotlight Award", "CMAA"

@dataclass
class OtherBiologything(Entity):
    """Refers to proteins, genes, families of organisms, cells, and biological domains."""
    span: str  # Such as: "Amphiphysin", "p53 protein", "Ismaridae", "Hymenoptera", "Retinoblastoma protein", "collagen", "hydroxyproline"

@dataclass
class OtherChemicalthing(Entity):
    """Refers to elements, compounds, gases, and chemical additives."""
    span: str  # Such as: "uranium", "carbon monoxide", "sulfur", "Molybdenum sulfide", "acetone", "atropine", "amphetamines"

@dataclass
class OtherCurrency(Entity):
    """Refers to specific monetary units and financial amounts."""
    span: str  # Such as: "Travancore Rupee", "Aruban florin", "Netherlands Antillean guilder", "Euro", "Deutsche mark"

@dataclass
class OtherDisease(Entity):
    """Refers to illnesses, medical conditions, and syndromes."""
    span: str  # Such as: "Dysentery", "hypothyroidism", "cancer", "Septic shock", "polyp", "Glial scarring", "diabetes", "infertility"

@dataclass
class OtherEducationaldegree(Entity):
    """Refers to academic degrees, diplomas, and certifications."""
    span: str  # Such as: "BSc", "Master of Visual Studies", "Ph.D.", "Medical Degree", "Doctor of Military Science", "MB ChB"

@dataclass
class OtherGod(Entity):
    """Refers to deities, gods, and figures of worship or mythology."""
    span: str  # Such as: "El", "Raijin", "Baglamukhi", "Jesus", "Zeus", "Prometheus", "Aeolians", "Achilles"

@dataclass
class OtherLanguage(Entity):
    """Refers to specific languages and linguistic versions."""
    span: str  # Such as: "English", "Breton-speaking", "Latin", "Italian", "Tibetan", "Tajik", "Aramaic", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Refers to treaties, statutes, acts, and formal legal resolutions."""
    span: str  # Such as: "Freedom Support Act", "Thirty Years' Peace", "America Invents Act", "Rush–Bagot Treaty", "War Powers Resolution"

@dataclass
class OtherLivingthing(Entity):
    """Refers to plants, animals, insects, and biological families."""
    span: str  # Such as: "monkeys", "patchouli", "Rafflesiaceae", "zebras", "beetle", "Lagerstroemia", "Carp", "rainbow trout"

@dataclass
class OtherMedical(Entity):
    """Refers to medical treatments, drugs, procedures, and terminology."""
    span: str  # Such as: "amitriptyline", "Pediatrics", "cryoprecipitate", "transplants", "oxycodone", "Folic acid", "Melatonin", "MRI"

@dataclass
class PersonActor(Entity):
    """Refers to professional performers in film, theater, and television."""
    span: str  # Such as: "Ellaline Terriss", "Edmund Payne", "Tchéky Karyo", "Jean Rochefort", "Bajpayee", "Sharon Duncan-Brewster"

@dataclass
class PersonArtistAuthor(Entity):
    """Refers to creators of art, music, literature, and humor."""
    span: str  # Such as: "George Axelrod", "Gaetano Donizetti", "Deborah Lurie", "Stephen King", "Ace Frehley", "Sam Levenson"

@dataclass
class PersonAthlete(Entity):
    """Refers to professional sports players and athletes."""
    span: str  # Such as: "Neville", "Tozawa", "Bruno Zanoni", "Ernie Johnson", "Guto", "Fausto Coppi"

@dataclass
class PersonDirector(Entity):
    """Refers to individuals who manage and direct the production of films, plays, or music videos."""
    span: str  # Such as: "Richard Quine", "Bob Swaim", "Frank Darabont", "Denis Villeneuve", "McG", "Peter Johnson"

@dataclass
class PersonOther(Entity):
    """Refers to notable individuals and family figures not primarily categorized by other professional roles."""
    span: str  # Such as: "Mrs. Strong", "Wallis", "Barbara Hutton", "Binion", "Reitman", "Chief Irvin Irving"

@dataclass
class PersonPolitician(Entity):
    """Refers to government officials, monarchs, presidents, and candidates."""
    span: str  # Such as: "Emeric", "Louis XIV", "Nikolai Ryzhkov", "Barack Obama", "Bill Haslam", "Mitt Romney"

@dataclass
class PersonScholar(Entity):
    """Refers to researchers, scientists, academics, and historians."""
    span: str  # Such as: "Stedman", "Wurdack", "Ted Robert Gurr", "Döndrup", "R. Brent Tully", "William Stimpson"

@dataclass
class PersonSoldier(Entity):
    """Refers to military personnel, commanders, and soldiers."""
    span: str  # Such as: "Krukenberg", "Helmuth Weidling", "Bruno Loerzer", "James Outram", "Joachim Murat", "Dong Laifu"

@dataclass
class ProductAirplane(Entity):
    """Refers to specific models of aircraft and spacecraft."""
    span: str  # Such as: "EC135T2 CPDS", "FGR.2s", "Mil Mi-58", "Su-30", "WC-135", "Gull III", "Soyuz spacecraft"

@dataclass
class ProductCar(Entity):
    """Refers to specific models of cars, trucks, and locomotives."""
    span: str  # Such as: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Lancia Thema", "Rolls Royce Sweptail", "Ferrari F12 TRS"

@dataclass
class ProductFood(Entity):
    """Refers to specific food items, ingredients, beverages, and recipes."""
    span: str  # Such as: "icewine", "yakiniku", "Merlot", "Wahaha branded products", "focaccia", "Yellow coq au vin", "Hop Monster"

@dataclass
class ProductGame(Entity):
    """Refers to video games, gaming consoles, and tabletop game systems."""
    span: str  # Such as: "Splinter Cell", "Airforce Delta", "Game Boy Micro", "Ms. Pac-Man", "RuneQuest II", "Samurai Warriors"

@dataclass
class ProductOther(Entity):
    """Refers to miscellaneous commercial products like hardware, missiles, or cryptographic devices."""
    span: str  # Such as: "PDP-1", "SecurID 800", "Sinclair Spectrum", "Apple II", "Durandal", "A330", "Airbus A320neos"

@dataclass
class ProductShip(Entity):
    """Refers to specific marine vessels, ships, and submarines."""
    span: str  # Such as: "HMS Chinkara", "Congress", "Essex", "Embuscade", "Alvin", "HMS Milford", "Niels Juel"

@dataclass
class ProductSoftware(Entity):
    """Refers to computer programs, applications, operating systems, and protocols."""
    span: str  # Such as: "Wikipedia", "Apdf", "BIDS Helper", "Visual Studio", "SQL Server", "Apache Wave", "Android 4.1.2 Jelly Bean"

@dataclass
class ProductTrain(Entity):
    """Refers to specific train models, railway services, and locomotives."""
    span: str  # Such as: "High Speed Trains", "Royal Scots Grey", "Lexus CT 200h", "Keystone Service", "ICE 3M", "Class 90"

@dataclass
class ProductWeapon(Entity):
    """Refers to specific types of weapons, firearms, missiles, and artillery."""
    span: str  # Such as: "ZU-23-2M Wrúbel", "AR-15", "M-14", "ZSU-57-2", "40mm Bofors gun", "Lee-Enfield", "Gongchen"


ENTITY_DEFINITIONS: List[Entity] = [
    ArtBroadcastProgram,
    ArtFilm,
    ArtMusic,
    ArtOther,
    ArtPainting,
    ArtWrittenart,
    BuildingAirport,
    BuildingHospital,
    BuildingHotel,
    BuildingLibrary,
    BuildingOther,
    BuildingRestaurant,
    BuildingSportsfacility,
    BuildingTheater,
    EventAttackBattleWarMilitaryConflict,
    EventDisaster,
    EventElection,
    EventOther,
    EventProtest,
    EventSportsevent,
    LocationGpe,
    LocationBodiesofwater,
    LocationIsland,
    LocationMountain,
    LocationOther,
    LocationPark,
    LocationRoadRailwayHighwayTransit,
    OrganizationCompany,
    OrganizationEducation,
    OrganizationGovernmentGovernmentagency,
    OrganizationMediaNewspaper,
    OrganizationOther,
    OrganizationPoliticalparty,
    OrganizationReligion,
    OrganizationShoworganization,
    OrganizationSportsleague,
    OrganizationSportsteam,
    OtherAstronomything,
    OtherAward,
    OtherBiologything,
    OtherChemicalthing,
    OtherCurrency,
    OtherDisease,
    OtherEducationaldegree,
    OtherGod,
    OtherLanguage,
    OtherLaw,
    OtherLivingthing,
    OtherMedical,
    PersonActor,
    PersonArtistAuthor,
    PersonAthlete,
    PersonDirector,
    PersonOther,
    PersonPolitician,
    PersonScholar,
    PersonSoldier,
    ProductAirplane,
    ProductCar,
    ProductFood,
    ProductGame,
    ProductOther,
    ProductShip,
    ProductSoftware,
    ProductTrain,
    ProductWeapon,
]