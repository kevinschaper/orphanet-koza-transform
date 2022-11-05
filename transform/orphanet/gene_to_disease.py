import uuid

from biolink.model import Disease, Gene, Association
from koza.cli_runner import get_koza_app

# Options here include:
# Ensembl, Genatlas, HGNC,
# IUPHAR, OMIM, Reactome
# Swissprot
# PREFERRED_GENE_SOURCES = ["HGNC"]
PREFERRED_GENE_SOURCES = [
    "Ensembl",
    "Genatlas",
    "HGNC",
    "IUPHAR",
    "OMIM",
    "Reactome",
    "Swissprot",
]

RELATION_TYPE_MAP = {
    "Disease-causing germline mutation(s) in": "biolink:condition_associated_with_gene",
    "Disease-causing germline mutation(s) (loss of function) in": "biolink:condition_associated_with_gene",
    "Disease-causing germline mutation(s) (gain of function) in": "biolink:condition_associated_with_gene",
    "Role in the phenotype of": "biolink:condition_associated_with_gene",
    "Major susceptibility factor in": "biolink:condition_associated_with_gene",
    "Disease-causing somatic mutation(s) in": "biolink:condition_associated_with_gene",
    "Candidate gene tested in": "biolink:related_to",
    "Part of a fusion gene in": "biolink:condition_associated_with_gene",
    "Biomarker tested in": "biolink:has_biomarker",
}

koza_app = get_koza_app("orphanet_gene_to_disease")

while (row := koza_app.get_row()) is not None:
    try:

        # Disease
        disease_id = "Orphanet:" + row["OrphaCode"]
        disease = Disease(
            id=disease_id, name=row["Name"]["#text"], category="biolink:Disease"
        )

        koza_app.write(disease)

        # Gene
        possible_genes = row["DisorderGeneAssociationList"]["DisorderGeneAssociation"][
            "Gene"
        ]["ExternalReferenceList"]["ExternalReference"]
        possible_preferred_genes = [
            gene for gene in possible_genes if gene["Source"] in PREFERRED_GENE_SOURCES
        ]

        for gene in possible_preferred_genes:
            gene_id = gene["Source"] + ":" + gene["Reference"]
            gene = Gene(id=gene_id, category="biolink:Gene")

            # Association
            orphanet_association_type = row["DisorderGeneAssociationList"][
                "DisorderGeneAssociation"
            ]["DisorderGeneAssociationType"]["Name"]["#text"]
            if orphanet_association_type in RELATION_TYPE_MAP:
                predicate = RELATION_TYPE_MAP[orphanet_association_type]
            else:
                predicate = "biolink:related_to"
            association = Association(
                id="uuid:" + str(uuid.uuid1()),
                subject=disease.id,
                predicate=predicate,
                category="biolink:Association",
                object=gene.id,
            )

            koza_app.write(association, gene)

    except (TypeError, ValueError) as e:
        row_id = row["@id"]
        print(f"Invalid entry: {e}. See entry {row_id}")
