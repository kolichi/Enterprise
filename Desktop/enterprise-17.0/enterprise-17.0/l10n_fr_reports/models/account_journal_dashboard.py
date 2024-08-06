# -*- coding: utf-8 -*-

from odoo import models, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _get_journal_dashboard_data_batched(self):
        # add a 'l10n_fr_has_rejected_tax_report' key
        dashboard_data = super()._get_journal_dashboard_data_batched()
        tax_journal_id = self.company_id.account_tax_periodicity_journal_id or self.filtered(lambda journal: journal.type == 'general')[:1]
        if tax_journal_id and tax_journal_id.id in dashboard_data:
            dashboard_data[tax_journal_id.id]['l10n_fr_has_rejected_tax_report'] = bool(
                self.env['account.report.async.export'].search([
                    ('report_id', '=', self.env.ref('l10n_fr.tax_report').id),
                    ('state', '=', 'rejected'),
                ], limit=1)
            )
        return dashboard_data

    def show_rejected_tax_reports(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _("EDI exports"),
            'res_model': 'account.report.async.export',
            'view_mode': 'list,form',
            'context': {**self.env.context, 'search_default_state_rejected': 1},
        }