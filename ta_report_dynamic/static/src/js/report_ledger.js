odoo.define('report_ledger.main', function (require) {
'use strict';
    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    var QWeb = core.qweb;

    const LedgerReportAction = AbstractAction.extend({
            template: "LedgerCust",
            info: "this message comes from the JS",
            events: {
                    'click .view-source': 'view_move_line',
                    'click .apply_filter': 'apply_filter',
                    'click .print_view': 'print_view',
               },
               init: function(parent, action) {
                   this._super(parent, action);
               },
               start: function() {
                   var self = this;
                   self.load_filter();
//                   self.load_data();

               },
               apply_filter: function () {
//                   console.log(this)
                   var selected_partner = this.$('#partner_id option:selected').val();
                   var date_start = document.getElementById("date_start").value;
                   var date_end = document.getElementById("date_end").value;
//                   console.log("///////////////////", date_start)
                   var self = this;
                   self._rpc({
                               model: 'dynamic.report.ledger',
                               method: 'ta_get_dynamic_report_values',
                               args: [1,selected_partner,date_start,date_end],
                           }).then(function(datas) {
//                           console.log("dataaaaaa", datas)
                               self.$('.table_view').html(QWeb.render('LedgerTable', datas));
                           });
               },

               load_filter: function () {
                   var self = this;
                   self._rpc({
                        model: 'dynamic.report.ledger',
                        method: 'ta_get_report_filters',
                        args: [1],
                   }).then(function(filters) {
//                        console.log("fileter_partnerrrrrr", filters)
                        self.$('.filter_view_tb').html(QWeb.render('filter_view', filters));
                    });
               },
               print_view: function () {
                  var self = this;
                  var printContents = document.getElementsByClassName("table_view")[0].innerHTML;
                  var originalContents = document.body.innerHTML;
                  document.body.innerHTML = printContents;
                  window.print();
                  document.location.reload(true);
               },
                view_move_line : function(event){
                event.preventDefault();
                var self = this;
                var context = {};
                var redirect_to_document = function (res_model, res_id, view_id) {
//                    console.log(res_model, res_id, view_id)
                var action = {
                        type:'ir.actions.act_window',
                        view_type: 'form',
                        view_mode: 'form',
                        res_model: res_model,
                        views: [[view_id || false, 'form']],
                        res_id: res_id,
                        target: 'current',
                        context: context,
                        };
                return self.do_action(action);
                };
                redirect_to_document('account.move',$(event.currentTarget).data('move-id'));
                },
            });
    core.action_registry.add('ta_party_ledger.action', LedgerReportAction);
});