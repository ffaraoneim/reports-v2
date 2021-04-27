# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Globex Corporation
# All rights reserved.
#

from datetime import date

from connect.client.rql import R


def generate(client, parameters, progress_callback, renderer_type, extra_context):
    """
    Extracts data from Connect using the ConnectClient instance
    and input parameters provided as arguments, applies
    required transformations (if any) and returns an iterator of rows
    that will be used to fill the Excel file.
    Each element returned by the iterator must be an iterator over
    the columns value.

    :param client: An instance of the CloudBlue Connect
                    client.
    :type client: cnct.ConnectClient
    :param parameters: Input parameters used to calculate the
                        resulting dataset.
    :type parameters: dict
    :param progress_callback: A function that accepts t
                                argument of type int that must
                                be invoked to notify the progress
                                of the report generation.
    :type progress_callback: func
    """

    filters = R().visibility.catalog.eq(True) & R().status.eq('published')

    count = client.products.filter(filters).count()

    i = 0

    ctx = {
        'products_count': count,
        'vendors_count': 0,
        'generation_date': date.today().strftime('%B %d, %Y'),
    }

    vendors = set()

    data = []

    for prod in client.products.filter(filters):
        i += 1
        data.append(prod)
        vendors.add(prod['owner']['id'])
        progress_callback(i, count)

    ctx['vendors_count'] = len(vendors)

    extra_context(ctx)

    return data
