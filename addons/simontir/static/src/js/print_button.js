flectra.define('print_lapharian.print_button', function (require) {
    "user strict";

    var form_widget = require('web.FormRenderer');
    var core = require('web.core');

    form_widget.include({
        _addOnClickAction: function ($el, node) {
            var self = this;

            $el.click(function () {
                if (node.attrs.custom === "print_dotmetrix") {
                    var url = "http://localhost/dotmatrix/";

                    if (node.attrs.custom === "print_dotmetrix") {
                        url = url + "print.php";
                    }
                    console.log(url)

                    var printer_data = self.state.data.printer_data;
                    if (!printer_data) {
                        alert('No data to print. Please click update Printer Data');

                        return;
                    }
                    console.log(printer_data)

                    $.ajax({
                        method: "POST",
                        url: url,
                        data: {
                            printer_data: printer_data
                        },
                        success: function (data) {
                            console.log('success')
                            console.log(data)
                        },
                        error: function (data) {
                            console.log('Failed');
                            console.log(data);
                        }
                    });
                } else {
                    self.trigger_up('button_clicked', {
                        attrs: node.attrs,
                        record: self.state,
                    });
                }
            });
        }
    });
});