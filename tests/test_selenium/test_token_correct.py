from tests.test_selenium.base import TokenCorrectBase, TokenCorrect2CorporaBase
import selenium


class TestTokenCorrectWauchierCorpus(TokenCorrectBase):
    def test_edit_token_lemma_with_allowed_values(self):
        """ [Wauchier] Test the edition of a token lemma with allowed values"""
        # Try first with an edit that would word
        self.addCorpus(with_token=True, with_allowed_lemma=True, tokens_up_to=24)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("un", id_row="1")
        self.assertEqual(token.lemma, "un", "Lemma should have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )


        # Try with an unallowed lemma
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("WRONG", id_row="2")
        self.assertEqual(token.lemma, "saint", "Lemma should have not been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-danger").text.strip(),
            "Invalid value in lemma"
        )

        # Try with a POS update but keeping the lemma
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("ADJqua", value_type="POS", id_row="3")
        self.assertEqual(token.lemma, "martin", "Lemma should have not been changed")
        self.assertEqual(token.POS, "ADJqua", "POS should have been changed to ADJqua")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )

    def test_edit_token_lemma_with_allowed_values_autocomplete(self):
        """ [Wauchier] Test the edition of a token with the use of autocompletion"""
        # Try first with an edit that would word
        self.addCorpus(with_token=True, with_allowed_lemma=True, tokens_up_to=24)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value(
            "d", id_row="1",
            autocomplete_selector=".autocomplete-suggestion[data-val='devoir']"
        )
        self.assertEqual(token.lemma, "devoir", "Lemma should have been changed to devoir")
        self.assertEqual(token.POS, "PRE", "POS should not have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )


    def test_edit_POS(self):
        """ [Wauchier] Edit POS of a token """
        self.addCorpus(with_token=True, with_allowed_lemma=True, tokens_up_to=24)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value(
            "ADJqua", id_row="1", value_type="POS"
        )
        self.assertEqual(token.lemma, "de", "Lemma should have been changed to devoir")
        self.assertEqual(token.POS, "ADJqua", "POS should not have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )


    def test_edit_morph(self):
        """ [Wauchier]  Edit morph of a token """
        self.addCorpus(with_token=True, with_allowed_lemma=True, tokens_up_to=24)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value(
            "_", id_row="1", value_type="morph"
        )
        self.assertEqual(token.lemma, "de", "Lemma should not have been changed")
        self.assertEqual(token.POS, "PRE", "POS should not have been changed")
        self.assertEqual(token.morph, "_", "Morph has been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )


        # Try with an unallowed morph
        token, status_text, row = self.edith_nth_row_value(
            "Not Allowed", id_row="2", value_type="morph"
        )
        self.assertEqual(token.lemma, "saint", "Lemma should not have been changed")
        self.assertEqual(token.POS, "ADJqua", "POS should not have been changed")
        self.assertEqual(token.morph, "Not Allowed", "Morph should have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )


    def test_edit_morph_with_allowed(self):
        """ [Wauchier] Edit morph of a token with allowed values as control"""
        self.addCorpus(with_token=True, with_allowed_lemma=True, with_allowed_morph=True, tokens_up_to=24)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value(
            "_", id_row="1", value_type="morph"
        )
        self.assertEqual(token.lemma, "de", "Lemma should not have been changed")
        self.assertEqual(token.POS, "PRE", "POS should not have been changed")
        self.assertEqual(token.morph, "_", "Morph has been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )


        # Try with an unallowed morph
        token, status_text, row = self.edith_nth_row_value(
            "Not Allowed", id_row="2", value_type="morph"
        )
        self.assertEqual(token.lemma, "saint", "Lemma should not have been changed")
        self.assertEqual(token.POS, "ADJqua", "POS should not have been changed")
        self.assertEqual(token.morph, "None", "Morph should not have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-danger").text.strip(),
            "Invalid value in morph"
        )

        # With auto complete
        token, status_text, row = self.edith_nth_row_value(
            "masc sing", id_row="3", corpus_id="1", value_type="morph",
            autocomplete_selector=".autocomplete-suggestion[data-val='NOMB.=s|GENRE=m|CAS=n']"
        )
        self.assertEqual(token.lemma, "martin", "Lemma should not have been changed")
        self.assertEqual(token.POS, "NOMpro", "POS should not have been changed")
        self.assertEqual(token.morph, "NOMB.=s|GENRE=m|CAS=n", "Morph should not have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )

        # With auto complete based on value and not label
        token, status_text, row = self.edith_nth_row_value(
            "NOMB.=s GENRE=m", id_row="4", corpus_id="1", value_type="morph",
            autocomplete_selector=".autocomplete-suggestion[data-val='NOMB.=s|GENRE=m|CAS=n']"
        )
        self.assertEqual(token.lemma, "mout", "Lemma should not have been changed")
        self.assertEqual(token.POS, "ADVgen", "POS should not have been changed")
        self.assertEqual(token.morph, "NOMB.=s|GENRE=m|CAS=n", "Morph should not have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )


class TestTokensCorrectFloovant(TokenCorrectBase):
    CORPUS = "floovant"
    CORPUS_ID = "2"

    def test_edit_POS(self):
        """ [Floovant] Edit POS of a token """
        self.addCorpus(with_token=True, with_allowed_lemma=True)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value(
            "ADJqua", id_row="1", value_type="POS"
        )
        self.assertEqual(token.lemma, "seignor", "Lemma should have been changed to devoir")
        self.assertEqual(token.POS, "ADJqua", "POS should not have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )

    def test_edit_token_lemma_with_allowed_values_lemma_pos(self):
        """ [Floovant] Test the edition of a token with allowed lemma and POS"""
        # Try first with an edit that would word
        self.addCorpus(with_token=True, with_allowed_lemma=True, with_allowed_pos=True)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("estoire1", id_row="1")
        self.assertEqual(token.lemma, "estoire1", "Lemma should have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )

        # Try with an unallowed lemma
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("WRONG", id_row="2")
        self.assertEqual(token.lemma, "or4", "Lemma should have not been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-danger").text.strip(),
            "Invalid value in lemma"
        )

        # Try with a POS update but keeping the lemma
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("ADJqua", value_type="POS", id_row="3")
        self.assertEqual(token.lemma, "escouter", "Lemma should have not been changed")
        self.assertEqual(token.POS, "ADJqua", "POS should have been changed to ADJqua")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )

    def test_edit_token_morph_with_allowed_values_lemma(self):
        """  [Floovant] Test the edition of a token's morph  with allowed_lemma """
        # Try first with an edit that would word
        self.addCorpus(with_token=True, with_allowed_lemma=True)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("SomeMorph", id_row="1", value_type="morph")
        self.assertEqual(token.lemma, "seignor", "Lemma should have been changed")
        self.assertEqual(token.morph, "SomeMorph", "Lemma should have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )

    def test_edit_token_morph(self):
        """ [Floovant] Test the edition of a token's morph"""
        # Try first with an edit that would word
        self.addCorpus(with_token=True)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("SomeMorph", id_row="1", value_type="morph")
        self.assertEqual(token.lemma, "seignor", "Lemma should have been changed")
        self.assertEqual(token.morph, "SomeMorph", "Lemma should have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )

    def test_edit_token_with_same_value(self):
        """ [Floovant] Test the edition of a token's lemma with the same value"""
        # Try first with an edit that would word
        self.addCorpus(with_token=True)
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("seignor", id_row="1", value_type="lemma")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-danger").text.strip(),
            "No value where changed"
        )
        self.assertNotIn("table-changed", row.get_attribute("class"))


class TestTokensEditTwoCorpora(TokenCorrect2CorporaBase):
    CORPUS = "wauchier"
    CORPUS_ID = "1"

    def test_edit_token_lemma_with_allowed_values_lemma_pos(self):
        """ [TwoCorpora] Test the edition of a token """
        # Try first with an edit that would work
        self.addCorpus(with_token=True, with_allowed_lemma=True, with_allowed_pos=True, tokens_up_to=24)
        token, status_text, row = self.edith_nth_row_value("saint", id_row="1")
        self.assertEqual(token.lemma, "saint", "Lemma should have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )


        # Try with an allowed lemma from the second corpus
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("seignor", id_row="2")
        self.assertEqual(token.lemma, "saint", "Lemma should not have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-danger").text.strip(),
            "Invalid value in lemma"
        )

        # Try with a POS update but keeping the lemma
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value("ADJqua", value_type="POS", id_row="3")
        print(status_text)
        self.assertEqual(token.lemma, "martin", "Lemma should have not been changed")
        self.assertEqual(token.POS, "ADJqua", "POS should have been changed to ADJqua")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )

    def test_edit_token_lemma_with_typeahead_click(self):
        """ [TwoCorpora] Test the edition of a token using typeahead"""
        # Try first with an edit that would work
        self.addCorpus(with_token=True, with_allowed_lemma=True, tokens_up_to=24)
        token, status_text, row = self.edith_nth_row_value(
            "s", id_row="1", corpus_id="1",
            autocomplete_selector=".autocomplete-suggestion[data-val='saint']"
        )
        self.assertEqual(token.lemma, "saint", "Lemma should have been changed")
        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )
        self.assertEqual(
            row.find_elements_by_tag_name("b")[0].text,
            token.form,
            "Bold should be used to highlight in-context word"
        )

        # Try with an allowed lemma from the second corpus
        self.driver.refresh()
        token, status_text, row = self.edith_nth_row_value(
            "s", id_row=str(self.first_token_id(2)+1), corpus_id="2",
            autocomplete_selector=".autocomplete-suggestion[data-val='seignor']"
        )
        self.assertEqual(token.lemma, "seignor", "Lemma should have been changed")

        self.assertEqual(
            row.find_element_by_css_selector(".badge-status.badge-success").text.strip(),
            "Saved"
        )

        # Try with an allowed lemma from the second corpus
        self.driver.refresh()
        with self.assertRaises(selenium.common.exceptions.TimeoutException):
            _ = self.edith_nth_row_value(
                "s", id_row=str(self.first_token_id(2)+1), corpus_id="2",
                autocomplete_selector=".autocomplete-suggestion[data-val='saint']"
            )
