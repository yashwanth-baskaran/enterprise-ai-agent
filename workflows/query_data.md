# Workflow: Query Data

## Objective
Read, filter, and export records from the business system.

## Required inputs
- Record model / table name (e.g. `crm.lead`, `res.partner`)
- Filter conditions in plain English (e.g. "all open opportunities created this month")
- Fields to return
- Output format (screen, CSV, Google Sheets)

## Steps

1. **Translate filters** — Convert the plain English filter into API domain syntax. Ask if any condition is ambiguous (e.g. "this month" — confirm the date range).

2. **Execute `tools/read_records.py`** with the translated parameters. Check the output count before proceeding — if 0 records returned, check the filter logic before assuming no data.

3. **Handle pagination** — If more than 500 records are expected, pass `limit` and `offset` parameters and loop until all records are retrieved.

4. **Format and deliver** — Write to the requested output format. For Google Sheets, use `tools/write_to_sheets.py`. For CSV, write to `.tmp/` and confirm the path.

## Edge cases
- **Empty results**: Re-check the domain filter. Confirm the model name is correct. Log the raw query.
- **Field not found**: Use `tools/read_records.py --describe MODEL` to inspect available fields before querying.
- **Rate limits**: Add a 1-second sleep between paginated calls. Update this workflow if a specific limit is discovered.

## Expected output
Structured data delivered to the requested destination. Confirm record count to the user.
