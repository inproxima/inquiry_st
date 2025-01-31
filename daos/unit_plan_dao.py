import logging
from typing import Optional

from .postgres_util import PostgresClient
from entities.unit_plan import UnitPlan
from constants import UNIT_PLAN_TABLE_NAME

# from ..error_handling import error_handler
from typing import List

import math

logger = logging.getLogger(__name__)


class UnitPlanDAO:
    # @error_handler
    async def insert(self, unit_plan: UnitPlan):
        pg_client = PostgresClient()
        try:
            insert_query = f"""
                    INSERT INTO {UNIT_PLAN_TABLE_NAME} (
                        grade, temperature, outcomes, user_context, unit_plan,
                        guiding_question, essential_knowledge, teacher_knowledge, assessment_plan,
                        inquiry_impact, differentiation, ipad, western_views, user_id, is_favorite,
                        is_generated, progress_percentage, created_at, title
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19
                    )
                    RETURNING unit_plan_id
                    """
            result = await pg_client.fetchval(
                insert_query,
                unit_plan.grade,
                unit_plan.temperature,
                unit_plan.outcomes,
                unit_plan.user_context,
                unit_plan.unit_plan,
                unit_plan.guiding_question,
                unit_plan.essential_knowledge,
                unit_plan.teacher_knowledge,
                unit_plan.assessment_plan,
                unit_plan.inquiry_impact,
                unit_plan.differentiation,
                unit_plan.ipad,
                unit_plan.western_views,
                unit_plan.user_id,
                unit_plan.is_favorite,
                unit_plan.is_generated,
                unit_plan.progress_percentage,
                unit_plan.created_at,
                unit_plan.title,
            )
            await pg_client.close()
            # await release_connection(pg_client)
            logger.info("Inserted the unit plan")
            logger.info(f"result is {result}")
            return result
        finally:
            await pg_client.close()



    # @error_handler
    def generate_update_sql(self, entity_id, fields_values):
        if not fields_values:
            raise ValueError("fields_values must not be empty.")

        set_clause = ", ".join(
            [f"{field} = ${i + 1}" for i, field in enumerate(fields_values.keys())]
        )
        sql = f"UPDATE {UNIT_PLAN_TABLE_NAME} SET {set_clause} WHERE unit_plan_id = ${len(fields_values) + 1};"

        values = list(fields_values.values())
        values.append(entity_id)
        return sql, values

    # @error_handler
    async def update(self, unit_plan_id: int, update_values: dict):
        update_sql, values = self.generate_update_sql(unit_plan_id, update_values)

        pg_client = PostgresClient()
        try:
            print(update_sql, values)
            await pg_client.execute(update_sql, *values)
            print("Update completed successfully!")
        finally:
            await pg_client.close()

    # @error_handler
    async def update_progress(self, unit_plan_id: int, update_values: dict):
        percentage_query = f"SELECT progress_percentage FROM {UNIT_PLAN_TABLE_NAME} WHERE unit_plan_id = $1"
        pg_client = PostgresClient()
        try:
            #async with conn.transaction():
            row = await pg_client.fetchrow(percentage_query, unit_plan_id)
            if row:
                # print(f"r p: {int(update_values["progress_percentage"])}")
                print(f"db p: {int(row["progress_percentage"])}")
                update_values["progress_percentage"] = int(
                    row["progress_percentage"]
                ) + int(update_values["progress_percentage"])
                # print(f"a p: {int(update_values["progress_percentage"])}")
                if int(update_values["progress_percentage"]) == 100:
                    update_values["is_generated"] = True
            update_sql, values = self.generate_update_sql(
                unit_plan_id, update_values
            )
            print(update_sql, values)
            await pg_client.execute(update_sql, *values)
            print("Execute completed successfully!")
            #print("Update completed successfully!")
        finally:
            await pg_client.close()

    # @error_handler
    async def delete(self, unit_plan_id: int):
        pg_client = PostgresClient()
        sql = f"DELETE FROM {UNIT_PLAN_TABLE_NAME} WHERE unit_plan_id = $1;"
        values = [unit_plan_id]
        try:
            await pg_client.execute(sql, *values)
        finally:
            await pg_client.close()

    # @error_handler
    async def find(self, unit_plan_id: int):
        pg_client = PostgresClient()
        query = f"SELECT * FROM {UNIT_PLAN_TABLE_NAME} WHERE unit_plan_id = $1"
        try:
            row = await pg_client.fetchrow(query, unit_plan_id)
            await pg_client.close()
            if row:
                unit_plan = UnitPlan(**row)
                return unit_plan
            return None
        finally:
            await pg_client.close()

    async def update_favorite_unit_plan(self, unit_plan_id: int, is_favorite: bool):
        await self.update(unit_plan_id, {"is_favorite": is_favorite})

    # @error_handler
    async def find_unit_plans_by_user(
        self,
        user_id: str,
        page_size: int,
        page_number: int,
        is_favorite: Optional[bool] = None,
        search_tags: List[str] = None,
        search_title: str = None,
    ):
        pg_client = PostgresClient()
        try:

            offset = (page_number - 1) * page_size

            # Fetch the actual page of results
            is_favorite_clause = ""
            if is_favorite is not None:
                is_favorite_clause += f"AND is_favorite = {is_favorite}"

            by_tags = ""
            if search_tags is not None:
                by_tags = f"AND tags && ARRAY{search_tags}"

            by_title = ""
            if search_title is not None:
                by_title = f"AND title ILIKE  '%{search_title}%'"

            query = (
                f"SELECT * FROM {UNIT_PLAN_TABLE_NAME} "
                f"WHERE user_id = '{user_id}' {is_favorite_clause} {by_tags} {by_title}"
                f"ORDER BY created_at DESC "
            )

            page_query = f"{query}" f"OFFSET {offset} LIMIT {page_size}"

            print(page_query)
            results = await pg_client.fetch(page_query)

            count_query = f"SELECT COUNT(*) FROM ({query}) AS MainQuery"
            total_records = await pg_client.fetchval(count_query)
            # print("total_records" + str(total_records))
            page_count = math.ceil(total_records / page_size)
            # print(f"page_size: {page_size}")
            # print(f"page_count: {page_count}")
            return results, page_count
        finally:
            await pg_client.close()

    async def update_unit_plan_title(self, unit_plan_id: int, title: str):
        await self.update(unit_plan_id, {"title": title})

    async def add_tag(self, unit_plan_id: int, tag: str):
        values = [unit_plan_id, tag]
        update_sql = (
            f"UPDATE {UNIT_PLAN_TABLE_NAME} "
            f"SET tags = tags || ARRAY[$2] "
            f"WHERE unit_plan_id = $1;"
        )
        pg_client = PostgresClient()
        try:
            print(update_sql)
            await pg_client.execute(update_sql, *values)
            print("Update completed successfully!")
        finally:
            await pg_client.close()

    async def remove_tag(self, unit_plan_id: int, tag: str):
        values = [unit_plan_id, tag]
        update_sql = (
            f"UPDATE {UNIT_PLAN_TABLE_NAME} "
            f"SET tags = array_remove(tags, $2) "
            f"WHERE unit_plan_id = $1;"
        )
        pg_client = PostgresClient()
        try:
            print(update_sql)
            await pg_client.execute(update_sql, *values)
            print("Tag removed successfully!")
        finally:
            await pg_client.close()

    async def get_user_tags(self, user_id: str, unit_plan_id: int):
        pg_client = PostgresClient()
        try:
            allTagsQuery = (
                f"SELECT DISTINCT UNNEST(tags) AS tags "
                f"FROM {UNIT_PLAN_TABLE_NAME} "
                f"WHERE user_id = '{user_id}'"
            )
            allTags = await pg_client.fetch(allTagsQuery)

            selectedTagsQuery = (
                f"SELECT DISTINCT UNNEST(tags) AS tags "
                f"FROM {UNIT_PLAN_TABLE_NAME} "
                f"WHERE user_id = '{user_id}' AND unit_plan_id={unit_plan_id}"
            )
            selectedTags = await pg_client.fetch(selectedTagsQuery)

            return allTags, selectedTags
        finally:
            await pg_client.close()

    async def get_all_user_tags(self, user_id: str):
        pg_client = PostgresClient()
        try:
            allTagsQuery = (
                f"SELECT DISTINCT UNNEST(tags) AS tags "
                f"FROM {UNIT_PLAN_TABLE_NAME} "
                f"WHERE user_id = '{user_id}'"
            )
            allTags = await pg_client.fetch(allTagsQuery)

            return allTags
        finally:
            await pg_client.close()