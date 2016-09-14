$(document).ready(function () {

      utilidad();

      $("select[id*='id_pedidoybien_set-']").change(function () {
            rownum = $(this).attr('id').replace(/(^.+\D)(\d+)(\D.+$)/i, '$2'); //=> '123'
            $.ajax({
                  url: "/admin/bienes_app/forms/pedido/pedidoybien-inline-autocomplete/",
                  type: "GET",
                  data: {
                        bien: $(this).val(),
                        cliente: $("#id_cliente").val(),
                  },
                  dataType: "json",
                  success: function (data) {
                        if ($("#id_pedidoybien_set-" + rownum + "-precio").length != 0) {
                              $("#id_pedidoybien_set-" + rownum + "-precio").val(data['precio']);
                        } else {
                              $("#pedidoybien_set-" + rownum).find(".field-precio").html("<p>" + data['precio'] + "</p>");
                        }
                        $("#pedidoybien_set-" + rownum).find(".field-costo").html("<p>" + data['costo'] + "</p>");
                        $("#id_pedidoybien_set-" + rownum + "-cantidad_solicitada").val('');
                  }
            });
            calc_precio_total();
            calc_costo_total();
            utilidad();
            
      });

      $("input[id*='-cantidad_solicitada']").change(function () {
            calc_precio_total();
            calc_costo_total();
            utilidad();
      });

      $("input[id*='-precio']").change(function () {
            calc_precio_total();
            utilidad();
      });

      $("input[id*='-descuento']").change(function () {
            calc_precio_total();
            utilidad();
      });


      function calc_precio_total() {
            total = 0;
            $(".dynamic-pedidoybien_set").each(function () {
                  cant = $(this).find("[id*='cantidad_solicitada']").val();

                  if ($(this).find("[id*='precio']").length != 0) {
                        valor = $(this).find("[id*='precio']").val();
                  } else {
                        valor = $(this).find(".field-precio").find("p").text().replace(',', '.');
                  }
                  valor = parseFloat(valor).toFixed(2);

                  if (!isNaN(valor) && cant > 0) {
                        if ($(this).find("[id*='descuento']").length != 0) {
                              dto = 1-($(this).find("[id*='descuento']").val()/100);
                        } else {
                              dto = 1;
                        }
                        total += cant * valor * dto;
                  }
            });
            if (total > 0) {
                  $('.field-precio_total').find('p').text(total.toFixed(2));
            } else {
                  $('.field-precio_total').find('p').text('-');
            }
      };

      function calc_costo_total() {
            total = 0;
            $(".dynamic-pedidoybien_set").each(function () {
                  cant = $(this).find("[id*='cantidad_solicitada']").val();
                  valor = $(this).find(".field-costo").find("p").text().replace(',', '.');
                  valor = parseFloat(valor).toFixed(2);

                  if (!isNaN(valor) && cant > 0) {
                        total += cant * valor;
                  }
            });
            if (total > 0) {
                  $('.field-costo_total').find('p').text(total.toFixed(2));
            } else {
                  $('.field-costo_total').find('p').text('-');
            }
      };

      function utilidad() {
            precio = $('.field-precio_total').find('p').text();
            precio = parseFloat(precio).toFixed(2);

            costo = $('.field-costo_total').find('p').text();
            costo = parseFloat(costo).toFixed(2);

            porc = 0;
            if (!isNaN(precio) && !isNaN(costo)){
                  porc = ((precio / costo)-1) * 100;
            }

            $('.field-utilidad').find('p').text(porc.toFixed(2) + "%");
      };

}); 
