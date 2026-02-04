from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastProgram(Entity):
    """Covers radio or television broadcasts, including talk shows, documentaries, series, and game shows."""
    span: str  # Examples: "The Gale Storm Show", "12 Corazones", "Jonovision", "Trailer Park Boys", "Mozart in Prague", "Soweto TV"

@dataclass
class ArtFilm(Entity):
    """Includes cinematic productions and motion pictures of all genres."""
    span: str  # Examples: "L'Atlantide", "The Shawshank Redemption", "Bosch", "Men in Her Diary", "Dances with Wolves", "Dune"

@dataclass
class ArtMusic(Entity):
    """Describes musical works like albums, songs, ballads, concerts, and compositions."""
    span: str  # Examples: "Atkinson, Danko and Ford", "Champion Lover", "Mass in C minor", "On the Loose", "The Boys of Wexford", "Free Fallin"

@dataclass
class ArtOther(Entity):
    """Covers various artistic creations, including sculptures, theater plays, music videos, and historical relics."""
    span: str  # Examples: "Venus de Milo", "The Today Show", "Cloud Gate", "Without the Prince", "Guys and Dolls", "Sphinx", "Lula and the Sailor"

@dataclass
class ArtPainting(Entity):
    """Designates sketches, paintings, graffiti, or visual lenses and designs."""
    span: str  # Examples: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Kamichama Karin", "The Sacrament of the Last Supper", "Athenaeum Portrait"

@dataclass
class ArtWrittenart(Entity):
    """Pertains to literary or written materials, such as books, magazines, scripts, poems, and theses."""
    span: str  # Examples: "Time", "The Seven Year Itch", "Imelda de' Lambertazzi", "Histories", "Adventure World Magazine", "Standard of Perfection"

@dataclass
class BuildingAirport(Entity):
    """Refers to aviation hubs, airfields, and airport terminals."""
    span: str  # Examples: "Sheremetyevo International Airport", "Newark Liberty International Airport", "Zhuhai Airport", "Vienna International Airport"

@dataclass
class BuildingHospital(Entity):
    """Includes clinics, medical centers, and hospital facilities."""
    span: str  # Examples: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Huntington Hospital", "Brigham and Women’s Hospital"

@dataclass
class BuildingHotel(Entity):
    """Refers to lodging establishments, resorts, and hotels."""
    span: str  # Examples: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel", "Hotel Sacher Salzburg", "Pierre Hotel"

@dataclass
class BuildingLibrary(Entity):
    """Covers institutional archives and library buildings."""
    span: str  # Examples: "Bayerische Staatsbibliothek", "British Library", "Berlin State Library", "Edmon Low Library", "Jefferson Market Library"

@dataclass
class BuildingOther(Entity):
    """Includes various structures such as palaces, recording studios, churches, museums, and drill halls."""
    span: str  # Examples: "Henry Ford Museum", "Alpha Recording Studios", "St John The Evangelist", "Palazzo Monte dei Poveri Vergognosi", "The Echo"

@dataclass
class BuildingRestaurant(Entity):
    """Designates eating establishments, including cafes, delis, fast-food outlets, and restaurants."""
    span: str  # Examples: "Trumbull dining hall", "Carnegie Deli", "Fatburger", "Morrison's", "Skyline", "McDonald's", "El Pollo Loco"

@dataclass
class BuildingSportsfacility(Entity):
    """Refers to athletic fields, arenas, sports centers, and stadiums."""
    span: str  # Examples: "Boston Garden", "Scotiabank Place", "ARCO Arena", "Appleton Arena", "Hughes Stadium", "Capital One Field"

@dataclass
class BuildingTheater(Entity):
    """Includes stages, opera houses, and theaters used for the performing arts."""
    span: str  # Examples: "Sanders Theatre", "Pittsburgh Civic Light Opera", "Whitehall Theatre", "Hicks Theatre", "Piccadilly Theatre", "The Warehouse Theatre"

@dataclass
class EventAttackBattleWarMilitaryConflict(Entity):
    """Includes military operations, specific battles, wars, and bombing incidents."""
    span: str  # Examples: "Vietnam War", "Operation Zipper", "Battle of Romani", "World War I", "Corinthian War", "Bali bombing", "Battle of Taku Forts"

@dataclass
class EventDisaster(Entity):
    """Refers to accidents, famines, natural disasters, and ecological catastrophes."""
    span: str  # Examples: "1693 Sicily earthquake", "North Korean famine", "1912 North Mount Lyell Disaster", "Chernobyl accident", "Hurricane Opal"

@dataclass
class EventElection(Entity):
    """Designates political campaign cycles, by-elections, and general elections."""
    span: str  # Examples: "March 1898 elections", "Elections to the European Parliament", "1982 Mitcham and Morden by-election", "1940 presidential election"

@dataclass
class EventOther(Entity):
    """Covers sundry organized events such as art salons, air shows, movements, and revolutions."""
    span: str  # Examples: "Masaryk Democratic Movement", "The Proms", "Romanian Revolution", "1995 Paris Air Show", "Salon des Indépendants"

@dataclass
class EventProtest(Entity):
    """Refers to organized protests, rebellions, boycotts, and revolutions."""
    span: str  # Examples: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Irish Rebellion of 1798", "Defiance Campaign", "Pro-Test Petition"

@dataclass
class EventSportsevent(Entity):
    """Includes athletic matches, cups, championships, and tournaments."""
    span: str  # Examples: "Stanley Cup", "World Cup", "Giro d'Italia", "Basketball ID", "United States Figure Skating Championships"

@dataclass
class LocationGpe(Entity):
    """Represents Geopolitical Entities (GPE) such as nations, municipalities, states, and provinces."""
    span: str  # Examples: "Croatia", "Europe", "Cornwall", "Michigan", "Germany", "Sweden", "United States", "Azerbaijani"

@dataclass
class LocationBodiesofwater(Entity):
    """Refers to lakes, rivers, bays, seas, and oceans."""
    span: str  # Examples: "Atatürk Dam Lake", "Arthur Kill", "East China Sea", "Jordan River", "Newark Bay", "Upper New York Bay", "Onkaparinga River"

@dataclass
class LocationIsland(Entity):
    """Includes peninsulas, archipelagos, and islands."""
    span: str  # Examples: "Laccadives", "Maldives", "Mainland", "Shetland", "Long Island", "Khark Islalnd", "Annobón", "Staten Island"

@dataclass
class LocationMountain(Entity):
    """Designates mountain ranges, individual peaks, ridges, and glaciers."""
    span: str  # Examples: "Ruweisat Ridge", "Salamander Glacier", "Mount Diablo", "K2", "Himalayan", "Karakoram", "Innuitian Mountains"

@dataclass
class LocationOther(Entity):
    """Covers miscellaneous locations such as valleys, forests, bridges, and particular estates."""
    span: str  # Examples: "Cartuther", "Victoria line", "Camino Palmero", "West Gate Bridge", "Bintan Resorts", "Jawai Bandh forests", "Helike"

@dataclass
class LocationPark(Entity):
    """Refers to conservation areas, historical districts, and parks."""
    span: str  # Examples: "Gramercy Park", "Shenandoah National Park", "Millennium Park", "Yellowstone Park", "Wind Cave", "Dalymount Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Includes transit routes, railway lines, highways, streets, and roads."""
    span: str  # Examples: "Friern Barnet Road", "North Jersey Coast Line", "Outerbridge Crossing", "State Route 151", "Claremont Avenue", "Salisbury Highway"

@dataclass
class OrganizationCompany(Entity):
    """Refers to businesses, corporations, and private firms."""
    span: str  # Examples: "Church's Chicken", "Taco Cabana", "WHL", "Warner Brothers", "Chiltern Air Support", "Braathens SAFE", "Hooper & Co."

@dataclass
class OrganizationEducation(Entity):
    """Includes educational academies, colleges, universities, and schools."""
    span: str  # Examples: "Belfast Royal Academy", "MIT", "Barnard College", "Latvia University of Life Sciences", "University of Canterbury", "Harvard"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Designates legislative assemblies, departments, courts, and government bodies."""
    span: str  # Examples: "Supreme Court", "Diet", "US Park Police", "Rajasthan government", "United States District Court"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Includes magazines, TV networks, newspapers, and news agencies."""
    span: str  # Examples: "Al Jazeera", "Clash", "TimeOut Melbourne", "Nickelodeon", "Sky Sports", "Pro Football Focus TV", "VH1"

@dataclass
class OrganizationOther(Entity):
    """Covers miscellaneous organizations such as councils, clubs, foundations, and armies."""
    span: str  # Examples: "IAEA", "4th Army", "SS Division Nordland", "Quixtar", "Leicester City Council", "John McAslan + Partners"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Refers to organizations and political parties."""
    span: str  # Examples: "Shimpotō", "Haq Movement", "National Liberal Party", "Republican", "BNG", "Democratic Party", "Socialist Party"

@dataclass
class OrganizationReligion(Entity):
    """Includes organized religious groups, sects, and denominations."""
    span: str  # Examples: "Jewish", "Christian", "Episcopalians", "United Methodists", "United Protestant Church of France", "Buddhism"

@dataclass
class OrganizationShoworganization(Entity):
    """Refers to artistic ensembles, performing groups, orchestras, and bands."""
    span: str  # Examples: "Mr. Mister", "Yeah Yeah Yeahs", "New York Youth Symphony", "Yakshagana Himmela", "Collegium 1704"

@dataclass
class OrganizationSportsleague(Entity):
    """Designates athletic conferences and professional or collegiate sports leagues."""
    span: str  # Examples: "First Division", "NHL", "China League One", "Bundesliga", "F1", "Atlantic Coast Conference"

@dataclass
class OrganizationSportsteam(Entity):
    """Refers to national athletic teams and specific sports clubs."""
    span: str  # Examples: "Arsenal", "Tottenham", "Luc Alphand Aventures", "Tre Kronor", "Utah Jazz", "Dallas Mavericks", "Wuhan Zall"

@dataclass
class OtherAstronomything(Entity):
    """Designates celestial bodies and regions, including stars, planets, constellations, and asteroids."""
    span: str  # Examples: "Algol", "42 Camelopardalis", "Sun", "Tandun III", "Ceres", "Birgitta", "Mars", "Asteroid Belt", "DC-7"

@dataclass
class OtherAward(Entity):
    """Includes prestigious recognitions, medals, honors, and prizes."""
    span: str  # Examples: "Order of the Republic", "European Car of the Year", "Kodansha Manga Award", "Spotlight Award", "CMAA"

@dataclass
class OtherBiologything(Entity):
    """Describes biological entities like proteins, genes, cells, organism families, and domains."""
    span: str  # Examples: "Amphiphysin", "p53 protein", "Ismaridae", "Hymenoptera", "Retinoblastoma protein", "collagen", "hydroxyproline"

@dataclass
class OtherChemicalthing(Entity):
    """Refers to chemical additives, gases, compounds, and elements."""
    span: str  # Examples: "uranium", "carbon monoxide", "sulfur", "Molybdenum sulfide", "acetone", "atropine", "amphetamines"

@dataclass
class OtherCurrency(Entity):
    """Designates financial amounts and specific monetary units."""
    span: str  # Examples: "Travancore Rupee", "Aruban florin", "Netherlands Antillean guilder", "Euro", "Deutsche mark"

@dataclass
class OtherDisease(Entity):
    """Includes syndromes, medical conditions, and illnesses."""
    span: str  # Examples: "Dysentery", "hypothyroidism", "cancer", "Septic shock", "polyp", "Glial scarring", "diabetes", "infertility"

@dataclass
class OtherEducationaldegree(Entity):
    """Refers to certifications, diplomas, and academic degrees."""
    span: str  # Examples: "BSc", "Master of Visual Studies", "Ph.D.", "Medical Degree", "Doctor of Military Science", "MB ChB"

@dataclass
class OtherGod(Entity):
    """Includes mythological figures, gods, and deities of worship."""
    span: str  # Examples: "El", "Raijin", "Baglamukhi", "Jesus", "Zeus", "Prometheus", "Aeolians", "Achilles"

@dataclass
class OtherLanguage(Entity):
    """Designates linguistic versions and specific languages."""
    span: str  # Examples: "English", "Breton-speaking", "Latin", "Italian", "Tibetan", "Tajik", "Aramaic", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Refers to formal legal resolutions, acts, statutes, and treaties."""
    span: str  # Examples: "Freedom Support Act", "Thirty Years' Peace", "America Invents Act", "Rush–Bagot Treaty", "War Powers Resolution"

@dataclass
class OtherLivingthing(Entity):
    """Includes biological families, insects, animals, and plants."""
    span: str  # Examples: "monkeys", "patchouli", "Rafflesiaceae", "zebras", "beetle", "Lagerstroemia", "Carp", "rainbow trout"

@dataclass
class OtherMedical(Entity):
    """Describes medical terminology, procedures, drugs, and treatments."""
    span: str  # Examples: "amitriptyline", "Pediatrics", "cryoprecipitate", "transplants", "oxycodone", "Folic acid", "Melatonin", "MRI"

@dataclass
class PersonActor(Entity):
    """Refers to individuals who perform professionally in theater, film, and television."""
    span: str  # Examples: "Ellaline Terriss", "Edmund Payne", "Tchéky Karyo", "Jean Rochefort", "Bajpayee", "Sharon Duncan-Brewster"

@dataclass
class PersonArtistAuthor(Entity):
    """Includes humorists and creators of literature, music, and art."""
    span: str  # Examples: "George Axelrod", "Gaetano Donizetti", "Deborah Lurie", "Stephen King", "Ace Frehley", "Sam Levenson"

@dataclass
class PersonAthlete(Entity):
    """Refers to athletes and professional sports players."""
    span: str  # Examples: "Neville", "Tozawa", "Bruno Zanoni", "Ernie Johnson", "Guto", "Fausto Coppi"

@dataclass
class PersonDirector(Entity):
    """Designates individuals managing the production of music videos, plays, or films."""
    span: str  # Examples: "Richard Quine", "Bob Swaim", "Frank Darabont", "Denis Villeneuve", "McG", "Peter Johnson"

@dataclass
class PersonOther(Entity):
    """Covers family members and notable individuals not primarily defined by other professional categories."""
    span: str  # Examples: "Mrs. Strong", "Wallis", "Barbara Hutton", "Binion", "Reitman", "Chief Irvin Irving"

@dataclass
class PersonPolitician(Entity):
    """Refers to political candidates, presidents, monarchs, and government officials."""
    span: str  # Examples: "Emeric", "Louis XIV", "Nikolai Ryzhkov", "Barack Obama", "Bill Haslam", "Mitt Romney"

@dataclass
class PersonScholar(Entity):
    """Includes historians, academics, scientists, and researchers."""
    span: str  # Examples: "Stedman", "Wurdack", "Ted Robert Gurr", "Döndrup", "R. Brent Tully", "William Stimpson"

@dataclass
class PersonSoldier(Entity):
    """Refers to soldiers, military commanders, and personnel."""
    span: str  # Examples: "Krukenberg", "Helmuth Weidling", "Bruno Loerzer", "James Outram", "Joachim Murat", "Dong Laifu"

@dataclass
class ProductAirplane(Entity):
    """Designates specific spacecraft and aircraft models."""
    span: str  # Examples: "EC135T2 CPDS", "FGR.2s", "Mil Mi-58", "Su-30", "WC-135", "Gull III", "Soyuz spacecraft"

@dataclass
class ProductCar(Entity):
    """Includes specific models of locomotives, trucks, and cars."""
    span: str  # Examples: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Lancia Thema", "Rolls Royce Sweptail", "Ferrari F12 TRS"

@dataclass
class ProductFood(Entity):
    """Refers to recipes, beverages, ingredients, and specific food products."""
    span: str  # Examples: "icewine", "yakiniku", "Merlot", "Wahaha branded products", "focaccia", "Yellow coq au vin", "Hop Monster"

@dataclass
class ProductGame(Entity):
    """Covers tabletop game systems, gaming consoles, and video games."""
    span: str  # Examples: "Splinter Cell", "Airforce Delta", "Game Boy Micro", "Ms. Pac-Man", "RuneQuest II", "Samurai Warriors"

@dataclass
class ProductOther(Entity):
    """Includes sundry commercial products such as cryptographic devices, missiles, or hardware."""
    span: str  # Examples: "PDP-1", "SecurID 800", "Sinclair Spectrum", "Apple II", "Durandal", "A330", "Airbus A320neos"

@dataclass
class ProductShip(Entity):
    """Designates specific submarines, ships, and marine vessels."""
    span: str  # Examples: "HMS Chinkara", "Congress", "Essex", "Embuscade", "Alvin", "HMS Milford", "Niels Juel"

@dataclass
class ProductSoftware(Entity):
    """Refers to protocols, operating systems, applications, and computer programs."""
    span: str  # Examples: "Wikipedia", "Apdf", "BIDS Helper", "Visual Studio", "SQL Server", "Apache Wave", "Android 4.1.2 Jelly Bean"

@dataclass
class ProductTrain(Entity):
    """Includes specific locomotives, railway services, and train models."""
    span: str  # Examples: "High Speed Trains", "Royal Scots Grey", "Lexus CT 200h", "Keystone Service", "ICE 3M", "Class 90"

@dataclass
class ProductWeapon(Entity):
    """Refers to specific artillery, missiles, firearms, and weapon types."""
    span: str  # Examples: "ZU-23-2M Wrúbel", "AR-15", "M-14", "ZSU-57-2", "40mm Bofors gun", "Lee-Enfield", "Gongchen"


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