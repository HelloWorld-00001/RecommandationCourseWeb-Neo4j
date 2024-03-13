SELECT C.*
FROM DIM_COURSE c
JOIN FACT_COURSE fc ON c.ID = fc.COURSEID
WHERE EXISTS (
    -- Checks for Programming Language
    SELECT 1
    FROM BRIDGE_COURSE_PROGRAMMINGLANGUAGE bcp
    JOIN DIM_PROGRAMMINGLANGUAGE p ON bcp.PROGRAMMINGLANGUAGE_ID = p.ID
    WHERE fc.ID = bcp.COURSEID AND p.PROGRAMMINGLANGUAGE IN ('JAVA', 'PYTHON')
)
OR EXISTS (
    -- Optional: Checks for Frameworks related to the Course through Programming Language
    SELECT 1
    FROM BRIDGE_COURSE_FRAMEWORK bcf
    JOIN DIM_FRAMEWORK fw ON bcf.FRAMEWORK_ID = fw.ID
    WHERE fc.ID = bcf.COURSEID AND fw.FRAMEWORK IN ('SPRING', 'SPARK')
)
OR EXISTS (
    -- Optional: Checks for Tools related to the Course
    SELECT 1
    FROM BRIDGE_COURSE_TOOL bct
    JOIN DIM_TOOL tl ON bct.TOOL_ID = tl.ID
    WHERE fc.ID = bct.COURSEID AND tl.TOOL = 'GIT'
)
OR EXISTS (
    -- Optional: Checks for Knowledge related to the Course
    SELECT 1
    FROM BRIDGE_COURSE_KNOWLEDGE bck
    JOIN DIM_KNOWLEDGE kl ON bck.KNOWLEDGE_ID = kl.ID
    WHERE fc.ID = bck.COURSEID AND kl.KNOWLEDGE IN ('DATA ANALYSIS', 'DATA WAREHOUSE')
)
OR EXISTS (
    -- Optional: Checks for Platforms related to the Course through Framework
    SELECT 1
    FROM BRIDGE_COURSE_PLATFORM bcpf
    JOIN DIM_PLATFORM pf ON bcpf.PLATFORM_ID = pf.ID
    WHERE fc.ID = bcpf.COURSEID AND pf.PLATFORM IN ('AZURE', 'CLOUD', 'MYSQL')
);