import uuid
from koza.cli_runner import get_koza_app

koza_app = get_koza_app("orphanet_gene_to_disease")

while (row := koza_app.get_row()) is not None:
    try:
        disease_id = "Orphanet:" + row["OrphaCode"]
        possible_genes = row["DisorderGeneAssociationList"]["DisorderGeneAssociation"]["Gene"]["ExternalReferenceList"][
            "ExternalReference"]
        possible_hgnc_genes = [gene for gene in possible_genes if gene["Source"] == 'HGNC']
        assert len(possible_hgnc_genes) == 1
        gene = possible_hgnc_genes[0]
        gene_id = gene["Source"] + ':' + gene["Reference"]

        orphanet_association_type = row["DisorderGeneAssociationList"]["DisorderGeneAssociation"]['DisorderGeneAssociationType']['Name']['#text']

        # todo: map the orphanet_association_type to a biolink predicate

        # todo: make an association rather than just printing stuff after sorting out the predicates
        print(f"{disease_id}\t{orphanet_association_type}\t{gene_id}")


    except:
        pass
