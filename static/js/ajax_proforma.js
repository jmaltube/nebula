$(document).ready(function () {
      $("select[id*='id_proformaybien_set-']").change(function () {
            rownum = $(this).attr('id').replace(/(^.+\D)(\d+)(\D.+$)/i, '$2'); //=> '123'
            $.ajax({
                  url: "/admin/bienes_app/forms/proforma/proformaybien-inline-autocomplete/",
                  type: "GET",
                  data: {
                        item: $(this).val(),
                  },
                  dataType: "json",
                  success: function (data) {
                        rewrite(data, rownum);
                  },
                  error: function () {
                        data = [];
                        data['cant_solic'] = "";
                        data['cant_pend'] = "";
                        data['precio'] = "";
                        rewrite(data, rownum);
                  }
            });
      });

      $("input[id*='-cantidad']").change(function () {
            rownum = $(this).attr('id').replace(/(^.+\D)(\d+)(\D.+$)/i, '$2'); //=> '123'
            cant = $(this).val();
            cant_solic = $("#proformaybien_set-" + rownum).find(".field-cantidad_solicitada").find("p").text();
            cant_pend = cant_solic - cant;
            $("#proformaybien_set-" + rownum).find(".field-cantidad_pendiente").html("<p>" + cant_pend + "</p>");
      });

      
      $( "#Autocompletar" ).click(function() {
            var pedidos_form = $("#id_pedidos").val().toString();
            $.ajax({
                  url: "/admin/bienes_app/forms/proforma/proforma-autocomplete/",
                  type: "GET",
                  data: { 
                        pedidos: pedidos_form,
                  },
                  dataType: "json",
                  success: function (data) {
                        $.each(data['items'], function (i, item) {
                              last_row_id = $("#id_proformaybien_set-TOTAL_FORMS").val()-1;
                              $("#id_proformaybien_set-"+last_row_id+"-item").append($('<option>', { 
                                    value: item.value,
                                    text : item.text 
                              }));
                              $("#id_proformaybien_set-"+last_row_id+"-item").val(item.value);
                              rewrite(item, last_row_id);
                              $('.add-row a').trigger('click');
                        });
                  },
            });
      });

      function rewrite(data, rownum) {
            $("#id_proformaybien_set-" + rownum + "-cantidad").val(data['cant_solic']);
            $("#proformaybien_set-" + rownum).find(".field-cantidad_solicitada").html("<p>" + data['cant_solic'] + "</p>");
            $("#proformaybien_set-" + rownum).find(".field-cantidad_pendiente").html("<p>" + data['cant_pend'] + "</p>");
            $("#proformaybien_set-" + rownum).find(".field-precio").html("<p>" + data['precio'] + "</p>");
      };
});
