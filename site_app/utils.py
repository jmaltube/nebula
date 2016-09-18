import logging
from bienes_app import models
import datetime

def clean_old_carts(*args):
    logger = logging.getLogger('django')
    days = args[0]
    logger.info("{0}----------Eliminando carritos herejes mayores a {1} día(s)----------".format(datetime.datetime.now(),days))
    pedidos = models.Pedido.objects.filter(confirmado_x_cliente=False, validado_x_admin=False)
    for pedido in pedidos:
        if abs((datetime.datetime.now(datetime.timezone.utc) - pedido.fecha_creacion).days) >= days:
            logger.info('{0}:: Pedido {1} con fecha de creación {2}'.format(datetime.datetime.now(), pedido, pedido.fecha_creacion))
            logger.info('{0}:: {1}'.format(datetime.datetime.now(), pedido.pedidoybien_set.all()))
            try:    
                logger.info('{0}:: {1}'.format(pedido.delete()))
            except Exception as e:
                logger.error(e) 