import uuid

from biolink.model import Association, Disease, Gene
from koza.cli_runner import get_koza_app

PREFERRED_GENE_SOURCES = ["HGNC"]

koza_app = get_koza_app("orphanet_gene_to_disease")

while (row := koza_app.get_row()) is not None:
    try:
        disease_id = "Orphanet:" + row["OrphaCode"]
        disease = Disease(
            id = disease_id,
            name = row['Name']['#text'],
            category = "biolink:Disease"
        )

        possible_genes = row["DisorderGeneAssociationList"]["DisorderGeneAssociation"]["Gene"]["ExternalReferenceList"][
            "ExternalReference"]
        possible_hgnc_genes = [gene for gene in possible_genes if gene["Source"] in PREFERRED_GENE_SOURCES]
        assert len(possible_hgnc_genes) == 1
        gene = possible_hgnc_genes[0]
        gene_id = gene["Source"] + ':' + gene["Reference"]
        gene = Gene(
            id = gene_id,
            category = "biolink:Gene"
        )

        # todo: map the orphanet_association_type to a biolink predicate
        orphanet_association_type = row["DisorderGeneAssociationList"]["DisorderGeneAssociation"]['DisorderGeneAssociationType']['Name']['#text']
        association = Association(
            id = "uuid:" + str(uuid.uuid1()),
            subject = disease.id,
            predicate = "biolink:Association",
            object = gene.id,
        )

        koza_app.write(disease, association, gene)
    
    except (TypeError, ValueError) as e:
        print(f"Invalid entry: {e}. Row contents: {row}")

