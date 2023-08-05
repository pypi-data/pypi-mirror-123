# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from mo_parsing.helpers import delimitedList, restOfLine
from mo_parsing.whitespaces import NO_WHITESPACE, Whitespace

from mo_sql_parsing.keywords import *
from mo_sql_parsing.utils import *
from mo_sql_parsing.windows import window


def combined_parser():
    combined_ident = Combine(delimitedList(
        ansi_ident | mysql_backtick_ident | sqlserver_ident | Word(IDENT_CHAR),
        separator=".",
        combine=True,
    )).set_parser_name("identifier")

    return parser(ansi_string, combined_ident)


def mysql_parser():
    mysql_string = ansi_string | mysql_doublequote_string
    mysql_ident = Combine(delimitedList(
        mysql_backtick_ident | sqlserver_ident | Word(IDENT_CHAR),
        separator=".",
        combine=True,
    )).set_parser_name("mysql identifier")

    return parser(mysql_string, mysql_ident)


def parser(literal_string, ident):
    with Whitespace() as engine:
        engine.add_ignore(Literal("--") + restOfLine)
        engine.add_ignore(Literal("#") + restOfLine)

        var_name = ~RESERVED + ident

        # EXPRESSIONS
        column_definition = Forward()
        column_type = Forward()
        expr = Forward()

        # CASE
        case = (
            CASE
            + Group(ZeroOrMore(
                (WHEN + expr("when") + THEN + expr("then")).addParseAction(to_when_call)
            ))("case")
            + Optional(ELSE + expr("else"))
            + END
        ).addParseAction(to_case_call)

        # SWITCH
        switch = (
            CASE
            + expr("value")
            + Group(ZeroOrMore(
                (WHEN + expr("when") + THEN + expr("then")).addParseAction(to_when_call)
            ))("case")
            + Optional(ELSE + expr("else"))
            + END
        ).addParseAction(to_switch_call)

        # CAST
        cast = Group(
            CAST("op") + LB + expr("params") + AS + known_types("params") + RB
        ).addParseAction(to_json_call)

        # TRIM
        trim = (
            Group(
                Keyword("trim", caseless=True).suppress()
                + LB
                + expr("chars")
                + Optional(FROM + expr("from"))
                + RB
            )
            .addParseAction(to_trim_call)
            .set_parser_name("trim")
        )

        _standard_time_intervals = MatchFirst([
            Keyword(d, caseless=True).addParseAction(lambda t: durations[t[0].lower()])
            for d in durations.keys()
        ]).set_parser_name("duration")("params")

        duration = (realNum | intNum)("params") + _standard_time_intervals

        interval = (
            INTERVAL + ("'" + delimitedList(duration) + "'" | duration)
        ).addParseAction(to_interval_call)

        timestamp = (
            time_functions("op")
            + (
                literal_string("params")
                | MatchFirst([
                    Keyword(t, caseless=True).addParseAction(lambda t: t.lower())
                    for t in times
                ])("params")
            )
        ).addParseAction(to_json_call)

        extract = (
            Keyword("extract", caseless=True)("op")
            + LB
            + (_standard_time_intervals | expr("params"))
            + FROM
            + expr("params")
            + RB
        ).addParseAction(to_json_call)

        namedColumn = Group(
            Group(expr)("value") + Optional(Optional(AS) + Group(var_name))("name")
        )

        distinct = (
            DISTINCT("op") + delimitedList(namedColumn)("params")
        ).addParseAction(to_json_call)

        ordered_sql = Forward()

        call_function = (
            ident("op")
            + LB
            + Optional(Group(ordered_sql) | delimitedList(Group(expr)))("params")
            + Optional(
                Keyword("ignore", caseless=True) + Keyword("nulls", caseless=True)
            )("ignore_nulls")
            + RB
        ).addParseAction(to_json_call)

        with NO_WHITESPACE:

            def scale(tokens):
                return {"mul": [tokens[0], tokens[1]]}

            scale_function = ((realNum | intNum) + call_function).addParseAction(scale)
            scale_ident = ((realNum | intNum) + ident).addParseAction(scale)

        compound = (
            NULL
            | TRUE
            | FALSE
            | NOCASE
            | interval
            | timestamp
            | extract
            | case
            | switch
            | cast
            | distinct
            | trim
            | (LB + Group(ordered_sql) + RB)
            | (LB + Group(delimitedList(expr)).addParseAction(to_tuple_call) + RB)
            | literal_string.set_parser_name("string")
            | hexNum.set_parser_name("hex")
            | scale_function
            | scale_ident
            | realNum.set_parser_name("float")
            | intNum.set_parser_name("int")
            | call_function
            | known_types
            | Combine(var_name + Optional(".*"))
        )

        sortColumn = expr("value").set_parser_name("sort1") + Optional(
            DESC("sort") | ASC("sort")
        ) | expr("value").set_parser_name("sort2")

        expr << (
            (
                Literal("*")
                | infixNotation(
                    compound,
                    [
                        (
                            o,
                            1 if o in unary_ops else (3 if isinstance(o, tuple) else 2),
                            RIGHT_ASSOC if o in unary_ops else LEFT_ASSOC,
                            to_json_operator,
                        )
                        for o in KNOWN_OPS
                    ],
                ).set_parser_name("expression")
            )("value")
            + Optional(window(expr, sortColumn))
        ).addParseAction(to_expression_call)

        alias = (
            (Group(var_name) + Optional(LB + delimitedList(ident("col")) + RB))("name")
            .set_parser_name("alias")
            .addParseAction(to_alias)
        )

        selectColumn = (
            Group(
                Group(expr).set_parser_name("expression1")("value")
                + Optional(Optional(AS) + alias)
                | Literal("*")("value")
            )
            .set_parser_name("column")
            .addParseAction(to_select_call)
        )

        table_source = (
            (
                (LB + ordered_sql + RB) | call_function
            )("value").set_parser_name("table source")
            + Optional(Optional(AS) + alias)
            | (var_name("value").set_parser_name("table name") + Optional(AS) + alias)
            | var_name.set_parser_name("table name")
        )

        join = (
            Group(
                CROSS_JOIN
                | FULL_JOIN
                | FULL_OUTER_JOIN
                | INNER_JOIN
                | JOIN
                | LEFT_JOIN
                | LEFT_OUTER_JOIN
                | RIGHT_JOIN
                | RIGHT_OUTER_JOIN
            )("op")
            + Group(table_source)("join")
            + Optional((ON + expr("on")) | (USING + expr("using")))
        ).addParseAction(to_join_call)

        unordered_sql = Group(
            SELECT
            + Optional(
                TOP
                + expr("value")
                + Optional(Keyword("percent", caseless=True))("percent")
                + Optional(WITH + Keyword("ties", caseless=True))("ties")
            )("top").addParseAction(to_top_clause)
            + delimitedList(selectColumn)("select")
            + Optional(
                (FROM + delimitedList(Group(table_source)) + ZeroOrMore(join))("from")
                + Optional(WHERE + expr("where"))
                + Optional(GROUP_BY + delimitedList(Group(namedColumn))("groupby"))
                + Optional(HAVING + expr("having"))
            )
        ).set_parser_name("unordered sql")

        ordered_sql << (
            (
                unordered_sql
                + ZeroOrMore(
                    Group(UNION_ALL | UNION | INTERSECT | EXCEPT | MINUS)
                    + unordered_sql
                )
            )("union")
            + Optional(ORDER_BY + delimitedList(Group(sortColumn))("orderby"))
            + Optional(LIMIT + expr("limit"))
            + Optional(OFFSET + expr("offset"))
        ).set_parser_name("ordered sql").addParseAction(to_union_call)

        statement = Forward()
        statement << (
            Optional(
                WITH
                + delimitedList(Group(
                    var_name("name") + AS + LB + (statement | expr)("value") + RB
                ))
            )("with")
            + Group(ordered_sql)("query")
        ).addParseAction(to_statement)

        #####################################################################
        # CREATE TABLE
        #####################################################################
        createStmt = Forward()

        BigQuery_STRUCT = (
            Keyword("struct", caseless=True)("op")
            + Literal("<").suppress()
            + delimitedList(column_definition)("params")
            + Literal(">").suppress()
        ).addParseAction(to_json_call)

        BigQuery_ARRAY = (
            Keyword("array", caseless=True)("op")
            + Literal("<").suppress()
            + delimitedList(column_type)("params")
            + Literal(">").suppress()
        ).addParseAction(to_json_call)

        column_type << (
            BigQuery_STRUCT
            | BigQuery_ARRAY
            | Group(
                ident("op") + Optional(LB + delimitedList(intNum)("params") + RB)
            ).addParseAction(to_json_call)
        )

        column_def_references = (
            REFERENCES
            + var_name("table")
            + LB
            + delimitedList(var_name)("columns")
            + RB
        )("references")

        column_def_check = Keyword("check", caseless=True).suppress() + LB + expr + RB

        column_def_default = Keyword(
            "default", caseless=True
        ).suppress() + expr("default")

        column_options = ZeroOrMore(Group(
            (NOT + NULL).addParseAction(lambda: "not null")
            | NULL.addParseAction(lambda t: "nullable")
            | Keyword("unique", caseless=True)
            | Keyword("primary key", caseless=True)
            | column_def_references
            | column_def_check("check")
            | column_def_default
        )).set_parser_name("column_options")

        column_definition << Group(
            var_name("name").addParseAction(lambda t: t[0].lower())
            + column_type("type")
            + Optional(column_options)("option")
        ).set_parser_name("column_definition")

        # MySQL's index_type := Using + ( "BTREE" | "HASH" )
        index_type = Optional(USING + ident("index_type"))

        index_column_names = LB + delimitedList(var_name("columns")) + RB

        column_def_foreign_key = FOREIGN_KEY + Optional(
            var_name("index_name") + index_column_names + column_def_references
        )

        index_options = ZeroOrMore(var_name)("table_constraint_options")

        table_constraint_definition = Optional(CONSTRAINT + var_name("name")) + (
            (
                PRIMARY_KEY + index_type + index_column_names + index_options
            )("primary_key")
            | (
                UNIQUE
                + Optional(INDEX | KEY)
                + Optional(var_name("index_name"))
                + index_type
                + index_column_names
                + index_options
            )("unique")
            | (
                (INDEX | KEY)
                + Optional(var_name("index_name"))
                + index_type
                + index_column_names
                + index_options
            )("index")
            | column_def_check("check")
            | column_def_foreign_key("foreign_key")
        )

        table_element = (
            column_definition("columns") | table_constraint_definition("constraint")
        )

        createStmt << (
            CREATE_TABLE
            + (
                var_name("name")
                + Optional(LB + delimitedList(table_element) + RB)
                + Optional(
                    AS.suppress() + infixNotation(statement, [])
                )("select_statement")
            )("create table")
        )

        return (statement | createStmt).finalize()
