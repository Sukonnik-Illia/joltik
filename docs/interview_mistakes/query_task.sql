WITH RECURSIVE hierarchy AS (
    SELECT
        id,
        first_name,
        last_name,
        title,
        manager_id
    FROM
        employees
    WHERE
        id = 5 -- Desired manager here

    UNION ALL

    SELECT
        e.id,
        e.first_name,
        e.last_name,
        e.title,
        e.manager_id
    FROM
        employees e
        INNER JOIN hierarchy eh ON e.manager_id = eh.id
)
SELECT
    *
FROM
    hierarchy;
