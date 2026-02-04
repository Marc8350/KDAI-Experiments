from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Designates radio or television broadcasts and serial content, ranging from talk shows to mockumentaries and dating programs."""
    span: str  # For instance: "The Gale Storm Show", "12 Corazones", "Jonovision", "Trailer Park Boys", "3 Idiots"

@dataclass
class ArtFilm(Entity):
    """Includes feature-length movies, cinematic works, various adaptations, and series or films made for television."""
    span: str  # For instance: "L'Atlantide", "The Shawshank Redemption", "Bosch", "Men in Her Diary"

@dataclass
class ArtMusic(Entity):
    """Pertains to musical works like albums, songs, and compositions, as well as specific recordings, symphonies, or orchestras."""
    span: str  # For instance: "Hollywood Studio Symphony", "Atkinson, Danko and Ford", "Champion Lover", "Mass in C minor", "Altenberg Lieder"

@dataclass
class ArtOther(Entity):
    """Encompasses various artistic creations not categorized elsewhere, including music videos, fountains, and sculptures."""
    span: str  # For instance: "Venus de Milo", "The Today Show", "Bleed Like Me", "Cloud Gate"

@dataclass
class ArtPainting(Entity):
    """Consists of visual art such as graffiti, paintings, or art series; additionally covers specific product lines like camera lenses according to the data."""
    span: str  # For instance: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Loxia", "Batis", "Kamichama Karin"

@dataclass
class ArtWrittenart(Entity):
    """Includes literary productions like novels, magazines, academic theses, librettos, or tragic plays."""
    span: str  # For instance: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "Rita Hayworth and Shawshank Redemption", "Writing, Teachers and Students in Graeco-Roman Egypt"

@dataclass
class BuildingAirport(Entity):
    """Indicates aviation facilities, covering both specific terminals and entire airport complexes."""
    span: str  # For instance: "Sheremetyevo International Airport", "London Luton Airport", "Newark Liberty International Airport", "Zhuhai Airport"

@dataclass
class BuildingHospital(Entity):
    """Represents healthcare venues, including specialized centers for cancer, clinics, and general hospitals."""
    span: str  # For instance: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Hokkaido University Hospital", "Huntington Hospital"

@dataclass
class BuildingHotel(Entity):
    """Covers lodging establishments such as resorts, hotels, and grand hotels."""
    span: str  # For instance: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel", "Hotel Sacher Salzburg"

@dataclass
class BuildingLibrary(Entity):
    """Refers to archival institutions and state or national libraries."""
    span: str  # For instance: "Bayerische Staatsbibliothek", "British Library", "Berlin State Library", "Edmon Low Library", "National Library of Laos"

@dataclass
class BuildingOther(Entity):
    """Signifies various physical edifices like mansions, recording studios, community centers, museums, and churches."""
    span: str  # For instance: "Henry Ford Museum", "Communiplex", "Alpha Recording Studios", "Church of England parish church of St John The Evangelist", "Palazzo Monte dei Poveri Vergognosi"

@dataclass
class BuildingRestaurant(Entity):
    """Denotes dining spots, including delis, restaurants, and food halls."""
    span: str  # For instance: "Trumbull dining hall", "Carnegie Deli", "Fatburger", "Morrison's"

@dataclass
class BuildingSportsfacility(Entity):
    """Includes venues for athletics, such as stadiums, arenas, and specialized sports gardens."""
    span: str  # For instance: "Boston Garden", "Sports Center", "Glenn Warner Soccer Facility", "Scotiabank Place"

@dataclass
class BuildingTheater(Entity):
    """Represents performance arts locations, like opera houses and theaters."""
    span: str  # For instance: "Sanders Theatre", "Pittsburgh Civic Light Opera", "National Paris Opera", "Whitehall Theatre"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Pertains to wars, specific military engagements, battles, and coordinated offensive maneuvers."""
    span: str  # For instance: "Vietnam War", "Easter Offensive", "Operation Zipper", "Battle of Romani", "World War I"

@dataclass
class EventDisaster(Entity):
    """Covers tragic incidents such as famines, earthquakes, aviation crashes, and mining accidents."""
    span: str  # For instance: "1693 Sicily earthquake", "1990s North Korean famine", "1912 North Mount Lyell Disaster", "Trigana Air Service Flight 267"

@dataclass
class EventElection(Entity):
    """Refers to voting events, parliamentary terms, and by-elections."""
    span: str  # For instance: "March 1898 elections", "Elections to the European Parliament", "1982 Mitcham and Morden by-election", "1997-2001 parliament"

@dataclass
class EventOther(Entity):
    """Includes miscellaneous events like political movements, stage-based occurrences, and enforcement campaigns."""
    span: str  # For instance: "Eastwood Scoring Stage", "Masaryk Democratic Movement", "Union for a Popular Movement", "Haq Movement"

@dataclass
class EventProtest(Entity):
    """Signifies acts of organized political or social defiance, such as boycotts, revolutions, and uprisings."""
    span: str  # For instance: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Iranian revolution", "Irish Rebellion of 1798"

@dataclass
class EventSportsevent(Entity):
    """Includes competitions, championship series, tournaments, and specific athletic races."""
    span: str  # For instance: "2021 Stanley Cup", "1958 World Cup", "2008 National Champions", "Round 3/Race 9"

@dataclass
class LocationGpe(Entity):
    """Designates geopolitical entities like cities, regions, countries, states, and provinces."""
    span: str  # For instance: "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall", "Dearborn", "Michigan"

@dataclass
class LocationBodiesofwater(Entity):
    """Represents aquatic features, whether natural or artificial, such as rivers, dams, seas, lakes, and kills."""
    span: str  # For instance: "Atatürk Dam Lake", "Arthur Kill", "Norfolk coast", "East China Sea", "Jordan River"

@dataclass
class LocationIsland(Entity):
    """Refers to landmasses such as archipelagos, islands, and peninsulas."""
    span: str  # For instance: "Samsat district", "Staten Island", "Laccadives", "Maldives", "Mainland", "Shetland"

@dataclass
class LocationMountain(Entity):
    """Includes geographical elevations like glaciers, ridges, mountain peaks, and ranges."""
    span: str  # For instance: "Ruweisat Ridge", "Salamander Glacier", "Mount Diablo", "K2", "Himalayan", "Karakoram"

@dataclass
class LocationOther(Entity):
    """Covers miscellaneous places such as transit paths, specific estates, and points of interest."""
    span: str  # For instance: "Cartuther", "Victoria line", "Cley next the Sea", "Camino Palmero", "Big Meadows"

@dataclass
class LocationPark(Entity):
    """Pertains to designated green spaces, including national parks, city parks, and historical community districts."""
    span: str  # For instance: "Gramercy Park", "Painted Desert Community Complex", "Shenandoah National Park", "Millennium Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Includes transportation infrastructure like highways, bridges, rail lines, and roads."""
    span: str  # For instance: "Newark-Elizabeth Rail Link", "Friern Barnet Road", "North Jersey Coast Line", "Outerbridge Crossing"

@dataclass
class OrganizationCompany(Entity):
    """Represents commercial entities, corporate businesses, record labels, and food chains."""
    span: str  # For instance: "Church's Chicken", "WHL", "Two Pesos, Inc.", "Taco Cabana, Inc.", "Warner Brothers"

@dataclass
class OrganizationEducation(Entity):
    """Includes academic institutions such as colleges, universities, specific faculties, and academies."""
    span: str  # For instance: "Belfast Royal Academy", "MIT", "Barnard College", "Latvia University of Life Sciences and Technologies"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Refers to official bodies like parliaments, courts, and federal or state law enforcement agencies."""
    span: str  # For instance: "Supreme Court", "Congregazione dei Nobili", "Diet", "US Park Police", "US Postal Police"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Signifies media platforms, news outlets, magazines, TV networks, and online information sites."""
    span: str  # For instance: "Al Jazeera", "Clash", "TimeOut Melbourne", "Nickelodeon", "Wikipedia"

@dataclass
class OrganizationOther(Entity):
    """Includes various groups like military units, international organizations, armies, and non-profits."""
    span: str  # For instance: "IAEA", "4th Army", "SS Division Nordland", "Defence Sector C"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Pertains to established political groups and parties."""
    span: str  # For instance: "Shimpotō", "Kenseitō", "Al Wafa ' Islamic party", "National Liberal Party", "Republican"

@dataclass
class OrganizationReligion(Entity):
    """Represents religious denominations, faiths, sacred traditions, and theological schools."""
    span: str  # For instance: "Jewish", "Christian", "Episcopalians", "United Methodists", "United Church of Christ"

@dataclass
class OrganizationShoworganization(Entity):
    """Includes musical groups, orchestras, and performing arts ensembles."""
    span: str  # For instance: "Mr. Mister", "Yeah Yeah Yeahs", "Bochumer Symphoniker"

@dataclass
class OrganizationSportsleague(Entity):
    """Refers to athletic leagues and their constituent divisions."""
    span: str  # For instance: "First Division", "China League One", "NHL", "Bundesliga"

@dataclass
class OrganizationSportsteam(Entity):
    """Represents professional teams, national squads, and racing outfits."""
    span: str  # For instance: "Arsenal", "Tottenham", "Luc Alphand Aventures", "Swedish national men's ice hockey team", "Audi"

@dataclass
class OtherAstronomything(Entity):
    """Pertains to astronomical entities like stars, zodiac signs, constellations, and planets."""
    span: str  # For instance: "Zodiac", "Algol", "42 Camelopardalis", "Sun", "Tandun III"

@dataclass
class OtherAward(Entity):
    """Includes prizes, honors, and distinctions for accomplishments in science, national service, or the arts."""
    span: str  # For instance: "Order of the Republic of Guinea", "Grammy", "European Car of the Year", "Kodansha Manga Award"

@dataclass
class OtherBiologything(Entity):
    """Covers biological items such as genes, proteins, taxonomic categories, and cell cycle stages."""
    span: str  # For instance: "Amphiphysin", "p53 protein", "Ismaridae", "G0 phase", "Rb"

@dataclass
class OtherChemicalthing(Entity):
    """Refers to chemical components like elements, gases, atmospheric blends, and compounds."""
    span: str  # For instance: "uranium", "carbon dioxide", "sulfur", "Carbon monoxide"

@dataclass
class OtherCurrency(Entity):
    """Represents monetary units and specific denominations of money."""
    span: str  # For instance: "Travancore Rupee", "$", "Rs 25 lac crore", "Aruban florin", "Netherlands Antillean guilder"

@dataclass
class OtherDisease(Entity):
    """Includes medical ailments, syndromes, epidemics, and diseases."""
    span: str  # For instance: "French Dysentery Epidemic of 1779", "hypothyroidism", "bladder cancer", "Septic shock"

@dataclass
class OtherEducationaldegree(Entity):
    """Pertains to academic credentials, diplomas, and honorary titles."""
    span: str  # For instance: "BSc ( Hons ) in physics", "Master of Visual Studies", "Bachelor of Education", "Ph.D .", "Medical Degree"

@dataclass
class OtherGod(Entity):
    """Represents divine figures, deities, and historical personalities considered holy."""
    span: str  # For instance: "El", "Raijin", "Fujin", "Baglamukhi", "Jesus"

@dataclass
class OtherLanguage(Entity):
    """Includes specific tongues and families of languages."""
    span: str  # For instance: "Hebrew", "Breton-speaking", "Latin", "English", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Refers to legal acts, statutes, specific legislative sections, and treaties."""
    span: str  # For instance: "United States Freedom Support Act", "Thirty Years ' Peace", "Leahy–Smith America Invents Act", "Rush–Bagot Treaty"

@dataclass
class OtherLivingthing(Entity):
    """Signifies animals and plants, as well as taxonomic groups excluding humans."""
    span: str  # For instance: "monkeys", "insects", "patchouli", "Rafflesiaceae", "zebras"

@dataclass
class OtherMedical(Entity):
    """Includes healthcare specialties, clinical procedures, pharmacological agents, and medical actions."""
    span: str  # For instance: "amitriptyline", "Pediatrics", "cryoprecipitate", "heart transplants"

@dataclass
class PersonActor(Entity):
    """Pertains to individuals recognized for their performances in theater, television, or film."""
    span: str  # For instance: "Ellaline Terriss", "Edmund Payne", "Tchéky Karyo", "Fernando Rey", "Bajpayee"

@dataclass
class PersonArtistAuthor(Entity):
    """Includes creators of art, such as writers, lyricists, composers, and authors."""
    span: str  # For instance: "George Axelrod", "Gaetano Donizetti", "Deborah Lurie", "Stephen King", "Karen O"

@dataclass
class PersonAthlete(Entity):
    """Represents people in sports, including racers and professional players."""
    span: str  # For instance: "Neville", "Tozawa", "Jaguar", "Bruno Zanoni", "Ernie Johnson"

@dataclass
class PersonDirector(Entity):
    """Refers to individuals who oversee the production of films, plays, or TV shows."""
    span: str  # For instance: "Richard Quine", "Bob Swaim", "Frank Darabont", "Costner"

@dataclass
class PersonOther(Entity):
    """Includes people not categorized by profession, such as family members or fictional characters."""
    span: str  # For instance: "Holden", "Olympia Elizabeth", "Wallis", "Rockefeller", "Binion"

@dataclass
class PersonPolitician(Entity):
    """Represents royalty or political officeholders like presidents, monarchs, and legislators."""
    span: str  # For instance: "Emeric", "William III", "Mary II", "Gillis Long", "Barack Obama"

@dataclass
class PersonScholar(Entity):
    """Pertains to intellectuals, professors, researchers, and academics."""
    span: str  # For instance: "Stedman", "Wurdack", "Davis", "Ted Robert Gurr"

@dataclass
class PersonSoldier(Entity):
    """Includes military members, commanders, and high-ranking generals."""
    span: str  # For instance: "Krukenberg", "Helmuth Weidling", "Bruno Loerzer", "Sir James Outram"

@dataclass
class ProductAirplane(Entity):
    """Represents flying machines like helicopters, specific aircraft models, and fighter jets."""
    span: str  # For instance: "EC135T2 CPDS", "FGR.2s", "Mil Mi-58", "Su-30", "WC-135"

@dataclass
class ProductCar(Entity):
    """Refers to automobiles, specific vehicle models, and motor platforms."""
    span: str  # For instance: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Lancia Thema 8.32"

@dataclass
class ProductFood(Entity):
    """Includes culinary items, grape types, wines, and food varieties."""
    span: str  # For instance: "V. labrusca", "yakiniku", "red grape", "Merlot", "Cabernet Sauvignon"

@dataclass
class ProductGame(Entity):
    """Signifies role-playing games, video games, and gaming consoles."""
    span: str  # For instance: "Splinter Cell", "Airforce Delta", "RPG", "Game Boy Advance", "Game Boy Micro"

@dataclass
class ProductOther(Entity):
    """Covers miscellaneous products like hardware, mechanical parts, and encryption tools."""
    span: str  # For instance: "Fairbottom Bobs", "PDP-1", "X11", "SecurID 800"

@dataclass
class ProductShip(Entity):
    """Refers to maritime craft, including frigates, submersibles, and landing vessels."""
    span: str  # For instance: "HMS Chinkara", "Congress", "Essex", "Embuscade", "Alvin"

@dataclass
class ProductSoftware(Entity):
    """Represents computer programs, development utilities, and programming languages."""
    span: str  # For instance: "Wikipedia", "Apdf", "BIDS Helper", "micro-PROLOG", "SQL Server"

@dataclass
class ProductTrain(Entity):
    """Includes rail vehicles, locomotives, and high-speed train models."""
    span: str  # For instance: "High Speed Trains", "55022 Royal Scots Grey", "Lexus CT 200h", "Keystone Service"

@dataclass
class ProductWeapon(Entity):
    """Signifies military hardware like artillery, guns, and rifles."""
    span: str  # For instance: "ZU-23-2M Wróbel", "AR-15", "ZSU-57-2", "40mm Bofors gun"

ENTITY_DEFINITIONS: List[Entity] = [
    ArtBroadcastprogram,
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
    EventAttackBattleWarMilitaryconflict,
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