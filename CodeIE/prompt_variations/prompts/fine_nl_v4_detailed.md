# CodeIE Prompt Variation: Detailed Annotation Style

## Metadata
- **Variation ID**: `v4_detailed`
- **Style**: Natural Language (nl-sel)
- **Granularity**: fine
- **Entity Types**: 66
- **Generated**: 2026-02-01 16:52:39

## Configuration

| Property | Value |
|----------|-------|
| Text Prefix | `Analyze the following text for named entities.
Val...` |
| Entity Prompt | `Identified entities: ` |

## Entity Definitions

The following entity types are included in this prompt:

| Entity Type | Description |
|-------------|-------------|
| `person-actor` | An actor or actress in film, television, or theater. |
| `person-artist/author` | A creative artist, writer, or author. |
| `person-athlete` | A professional or amateur sports player. |
| `person-director` | A film, television, or theater director. |
| `person-politician` | A political figure or government official. |
| `person-scholar` | An academic, researcher, or scholar. |
| `person-soldier` | A military personnel or soldier. |
| `person-other` | Other individuals not fitting specific person categories. |
| `location-GPE` | A geo-political entity like a country, state, or city. |
| `location-bodiesofwater` | A named body of water like an ocean, sea, river, or lake. |
| `location-island` | A named island or archipelago. |
| `location-mountain` | A named mountain, mountain range, or hill. |
| `location-park` | A named park, nature reserve, or recreational area. |
| `location-road/railway/highway/transit` | A named road, railway, highway, or transit route. |
| `location-other` | Other geographical locations. |
| `organization-company` | A business company or corporation. |
| `organization-education` | An educational institution like a university or school. |
| `organization-government/governmentagency` | A government body or agency. |
| `organization-media/newspaper` | A media outlet, newspaper, or broadcast company. |
| `organization-politicalparty` | A political party or movement. |
| `organization-religion` | A religious organization or denomination. |
| `organization-showorganization` | An entertainment or performance organization. |
| `organization-sportsleague` | A sports league or athletic organization. |
| `organization-sportsteam` | A named sports team. |
| `organization-other` | Other organizations. |
| `building-airport` | A named airport. |
| `building-hospital` | A named hospital or medical facility. |
| `building-hotel` | A named hotel or lodging establishment. |
| `building-library` | A named library. |
| `building-restaurant` | A named restaurant or dining establishment. |
| `building-sportsfacility` | A named sports stadium, arena, or facility. |
| `building-theater` | A named theater or performance venue. |
| `building-other` | Other named buildings or structures. |
| `art-broadcastprogram` | A television or radio program. |
| `art-film` | A movie or film. |
| `art-music` | A musical work, song, or album. |
| `art-painting` | A painting or visual artwork. |
| `art-writtenart` | A book, poem, or other written work. |
| `art-other` | Other works of art. |
| `product-airplane` | A named aircraft or airplane model. |
| `product-car` | A named car or vehicle model. |
| `product-food` | A named food product or brand. |
| `product-game` | A named game or video game. |
| `product-ship` | A named ship or watercraft. |
| `product-software` | A named software product or application. |
| `product-train` | A named train or railway vehicle. |
| `product-weapon` | A named weapon or weapons system. |
| `product-other` | Other products. |
| `event-attack/battle/war/militaryconflict` | A military conflict, battle, or attack. |
| `event-disaster` | A natural or man-made disaster. |
| `event-election` | A political election. |
| `event-protest` | A protest or demonstration. |
| `event-sportsevent` | A sports event or competition. |
| `event-other` | Other named events. |
| `other-astronomything` | An astronomical object or phenomenon. |
| `other-award` | A named award or prize. |
| `other-biologything` | A biological entity such as a species or organism. |
| `other-chemicalthing` | A chemical compound or substance. |
| `other-currency` | A named currency. |
| `other-disease` | A named disease or medical condition. |
| `other-educationaldegree` | An educational degree or qualification. |
| `other-god` | A deity or god from mythology or religion. |
| `other-language` | A named language. |
| `other-law` | A named law or legal document. |
| `other-livingthing` | Other living things not covered by biologything. |
| `other-medical` | Medical terms or procedures. |


## Sample Prompt

Below is a sample prompt generated with this variation:

```python
Analyze the following text for named entities.
Valid entity types are: person-actor, person-artist/author, person-athlete, person-director, person-politician, person-scholar, person-soldier, person-other, location-GPE, location-bodiesofwater, location-island, location-mountain, location-park, location-road/railway/highway/transit, location-other, organization-company, organization-education, organization-government/governmentagency, organization-media/newspaper, organization-politicalparty, organization-religion, organization-showorganization, organization-sportsleague, organization-sportsteam, organization-other, building-airport, building-hospital, building-hotel, building-library, building-restaurant, building-sportsfacility, building-theater, building-other, art-broadcastprogram, art-film, art-music, art-painting, art-writtenart, art-other, product-airplane, product-car, product-food, product-game, product-ship, product-software, product-train, product-weapon, product-other, event-attack/battle/war/militaryconflict, event-disaster, event-election, event-protest, event-sportsevent, event-other, other-astronomything, other-award, other-biologything, other-chemicalthing, other-currency, other-disease, other-educationaldegree, other-god, other-language, other-law, other-livingthing, other-medical

Text for analysis: "Apple announced that Steve Jobs would present the new iPhone at WWDC in San Francisco."

Identified entities: 
```

## Usage

To use this variation in experiments:

```bash
python run_codeie_experiments.py --granularity fine --style nl --variation v4_detailed
```
