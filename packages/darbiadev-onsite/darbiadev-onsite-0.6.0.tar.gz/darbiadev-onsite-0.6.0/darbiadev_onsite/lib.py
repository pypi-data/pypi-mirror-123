#!/usr/bin/env python

from importlib.resources import files
from typing import Any

import jaydebeapi


class OnSiteServices:
    """A class wrapping an ODBC connection to OnSite.

    This class wraps an ODBC connection to OnSite.
    """

    def __init__(
            self,
            connection_url: str,
            username: str,
            password: str
    ):
        self._connection_url: str = connection_url
        self.__username: str = username
        self.__password: str = password

    def _connect(
            self,
    ):
        return jaydebeapi.connect(
            "com.filemaker.jdbc.Driver",
            self._connection_url,
            [self.__username, self.__password],
            str(files("darbiadev_onsite").joinpath("vendor/fmjdbc.jar")),
        )

    def _make_query(
            self,
            sql: str,
    ) -> list[dict[str, Any]]:
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_order(
            self,
            order_number: int,
    ) -> dict[str, Any]:
        order_sql = open("sql/order.sql").read().format(order_number=order_number)
        line_sql = open("sql/linesoe.sql").read().format(order_number=order_number)
        address_sql = open("sql/address.sql").read().format(order_number=order_number)
        package_sql = open("sql/packimport.sql").read().format(order_number=order_number)

        order_data = self._make_query(sql=order_sql)[0]
        order_data["lines"] = self._make_query(sql=line_sql)
        order_data["addresses"] = self._make_query(sql=address_sql)
        order_data["packages"] = self._make_query(sql=package_sql)

        return order_data
