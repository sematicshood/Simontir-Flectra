flectra.define('print_dotmatrix.print_button', function (require) {
    "user strict";

    var form_widget = require('web.FormRenderer');

    form_widget.WidgetButton.include({
        on_click: function () {
            if (this.node.attrs.custom === "print") {
                var url = "http://localhost/dotmatrix/";

                if (this.node.attrs.custom === "print") {
                    url = url + "print.php";
                }
                console.log(url)

                var view = this.getParent();
                var printer_data = view.datarecord.printer_data;
                if (!printer_data) {
                    alert('No data to print. Please click update Printer Data');

                    return;
                }
                print(printer_data)

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
                this._super();
            }
        }
    });
});