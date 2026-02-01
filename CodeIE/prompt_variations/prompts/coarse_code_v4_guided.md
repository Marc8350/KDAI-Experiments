# CodeIE Prompt Variation: Guided Entity Recognition

## Metadata
- **Variation ID**: `v4_guided`
- **Style**: Code-Style (pl-func)
- **Granularity**: coarse
- **Entity Types**: 8
- **Generated**: 2026-02-01 16:52:27

## Configuration

| Property | Value |
|----------|-------|
| Function Name | `guided_ner` |
| Docstring | "Identify named entities in the input text using the entity type guidelines defined below" |
| Entity Header | `# Entity type guidelines` |

## Entity Definitions

The following entity types are included in this prompt:

| Entity Type | Description |
|-------------|-------------|
| `person` | A named individual, including fictional characters, historical figures, celebrities, and common people. |
| `location` | A geographical location such as a city, country, continent, region, or landmark. |
| `organization` | A named organization, institution, company, or group. |
| `building` | A named structure or building, such as a stadium, museum, or hotel. |
| `art` | A work of art including films, books, music, paintings, or other creative works. |
| `product` | A named commercial product, software, vehicle model, or branded item. |
| `event` | A named event such as a war, sports event, festival, or historical occurrence. |
| `other` | Other named entities that don't fit into the above categories. |


## Sample Prompt

Below is a sample prompt generated with this variation:

```python
def guided_ner(input_text):
	""" Identify named entities in the input text using the entity type guidelines defined below """
	# Entity type guidelines
	# "person": A named individual, including fictional characters, historical figures, celebrities, and common people.
	# "location": A geographical location such as a city, country, continent, region, or landmark.
	# "organization": A named organization, institution, company, or group.
	# "building": A named structure or building, such as a stadium, museum, or hotel.
	# "art": A work of art including films, books, music, paintings, or other creative works.
	# "product": A named commercial product, software, vehicle model, or branded item.
	# "event": A named event such as a war, sports event, festival, or historical occurrence.
	# "other": Other named entities that don't fit into the above categories.

	input_text = "Apple announced that Steve Jobs would present the new iPhone at WWDC in San Francisco."
	entity_list = []
	# extracted named entities
```

## Usage

To use this variation in experiments:

```bash
python run_codeie_experiments.py --granularity coarse --style pl --variation v4_guided
```
