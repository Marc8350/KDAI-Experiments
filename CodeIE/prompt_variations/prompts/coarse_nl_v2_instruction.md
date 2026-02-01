# CodeIE Prompt Variation: Instruction Style

## Metadata
- **Variation ID**: `v2_instruction`
- **Style**: Natural Language (nl-sel)
- **Granularity**: coarse
- **Entity Types**: 8
- **Generated**: 2026-02-01 16:52:27

## Configuration

| Property | Value |
|----------|-------|
| Text Prefix | `Identify entities of types ({schema}) in: "{text}"...` |
| Entity Prompt | `Entities: ` |

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
Identify entities of types (person, location, organization, building, art, product, event, other) in: "Apple announced that Steve Jobs would present the new iPhone at WWDC in San Francisco."

Entities: 
```

## Usage

To use this variation in experiments:

```bash
python run_codeie_experiments.py --granularity coarse --style nl --variation v2_instruction
```
