def format_source(source, style="IEEE", number=1):
    authors = source["authors"]
    title = source["title"]
    year = source["year"]
    venue = source["venue"]
    doi = source.get("doi", "")

    if style == "APA":
        ref = f"{authors} ({year}). {title}. {venue}."
        if doi:
            ref += f" https://doi.org/{doi}"
        return ref

    ref = f"[{number}] {authors}, \"{title},\" {venue}, {year}."
    if doi:
        ref += f" doi: {doi}."
    return ref

def build_reference_list(matches, style):
    unique = []
    seen = set()
    for m in matches:
        key = (m["title"], m["year"])
        if key not in seen:
            seen.add(key)
            unique.append(m)

    return "\n".join(
        format_source(m, style, i)
        for i, m in enumerate(unique, 1)
    )

def build_csv_rows(matches):
    import csv
    import io
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["claim_id","claim","title","authors","year","venue","doi","score"])
    for m in matches:
        writer.writerow([
            m["claim_id"], m["claim"], m["title"], m["authors"],
            m["year"], m["venue"], m["doi"], f'{m["score"]:.3f}'
        ])
    return out.getvalue()
