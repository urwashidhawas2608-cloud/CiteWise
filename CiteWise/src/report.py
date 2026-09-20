import csv
import io


def build_reference_list(matches, style="IEEE"):
    unique = []
    seen = set()

    for m in matches:
        key = (m["title"], m["year"])

        if key not in seen:
            seen.add(key)
            unique.append(m)

    references = []

    for i, m in enumerate(unique, 1):
        authors = m["authors"]
        title = m["title"]
        year = m["year"]
        venue = m["venue"]
        doi = m.get("doi", "")

        if style == "APA":
            reference = f"{authors} ({year}). {title}. {venue}."

            if doi:
                reference += f" https://doi.org/{doi}"

        else:
            reference = f'[{i}] {authors}, "{title}," {venue}, {year}.'

            if doi:
                reference += f" doi: {doi}."

        references.append(reference)

    return "\n".join(references)


def build_csv_rows(matches):
    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "claim_id",
        "claim",
        "title",
        "authors",
        "year",
        "venue",
        "doi",
        "score"
    ])

    for m in matches:
        writer.writerow([
            m["claim_id"],
            m["claim"],
            m["title"],
            m["authors"],
            m["year"],
            m["venue"],
            m.get("doi", ""),
            f'{m["score"]:.3f}'
        ])

    return output.getvalue()