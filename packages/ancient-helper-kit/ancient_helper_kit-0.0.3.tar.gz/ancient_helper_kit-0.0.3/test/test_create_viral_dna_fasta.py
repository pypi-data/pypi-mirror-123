import pytest
import ancient_helper_kit.kraken2.create_viral_dna_fasta as cvdf
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq


class TestGenerator:
    seq = Seq("GTTGGCCTACTGGTCGGTCAGTAAAAACTACATCAAGATCCGGTAATT")
    id = "NC_055757.1|kraken:taxid|2250214"
    desc = f"{id} Escherichia virus KFS-EC, complete genome"
    seq_rec = SeqRecord(seq=seq, id=id, name=id, description=desc)
    seq_dict = {"NC_055757.1": seq_rec}
    tax_lookup = {"NC_055757.1": "2250214"}

    def test_same_seq_returned(self):
        rec = next(cvdf.my_generator(seq_dict=self.seq_dict,
                                     tax_lookup=self.tax_lookup))
        assert rec.seq == self.seq

    def test_id(self):
        rec = next(cvdf.my_generator(seq_dict=self.seq_dict,
                                     tax_lookup=self.tax_lookup))
        assert rec.id == self.id

    def test_description(self):
        rec = next(cvdf.my_generator(seq_dict=self.seq_dict,
                                     tax_lookup=self.tax_lookup))
        assert rec.description == self.desc

    def test_empty_description(self):
        self.seq_rec.description = self.id
        rec = next(cvdf.my_generator(seq_dict=self.seq_dict,
                                     tax_lookup=self.tax_lookup))
        assert rec.description == self.id

