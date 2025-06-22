SELECT pf.number,
    pf.Name, 
    pf.cup,
    pf.Team,
    CASE
        WHEN pf.Team = '台電公司' THEN '台電男排'
        WHEN pf.Team = 'MIZUNO' THEN '雲林Mizuno'
        WHEN pf.Team = '中國人纖' THEN '新北中纖'
        WHEN pf.Team = 'conti' THEN '臺北Conti'
        WHEN pf.Team = '桃園台灣產險' THEN '桃園臺產'
        WHEN pf.Team = '桃園臺灣產險' THEN '桃園臺產'
        WHEN pf.Team = '長力男排' THEN '臺中長力'
        WHEN pf.Team = '屏東台電' THEN '台電男排'
        WHEN pf.Team = '桃園臺產隼鷹' THEN '桃園臺產'
        WHEN pf.Team = '愛山林' THEN '愛山林建設'
        WHEN pf.Team = '高雄台電' THEN '台電女排'
        WHEN pf.Team = '連莊' THEN '連莊排球隊'
        WHEN pf.Team = '雲林美津濃' THEN '雲林Mizuno'
        ELSE pf.Team
    END AS COR_TEAM,
    COUNT(*) AS Games_Played, 
    SUM(ms.is_winner) AS Games_Won, 
    ROUND(SUM(ms.is_winner) * 1.0 / COUNT(*), 3) AS Real_Win_Rate 
FROM 
    ( 
        SELECT ps.number, 
            ps.Name, 
            ps.match_cup_id, 
            SUBSTRING_INDEX(ps.match_cup_id, '_', -1) AS cup, 
            ps.Team, 
            CASE WHEN COALESCE(ps.`Serve_Total`, 0) + COALESCE(ps.`Receive_Total`, 0) 
            + COALESCE(ps.`Attack_Total`, 0) + COALESCE(ps.`Block_Point`, 0) + COALESCE(ps.`Dig_Total`, 0) 
            + COALESCE(ps.`Set_Total`, 0) > 0 THEN 1 ELSE 0 END AS Played_Flag 
        FROM Player_Stats ps ) pf 
JOIN Match_Score ms ON pf.match_cup_id = ms.match_cup_id AND pf.Team = ms.match_Team 
GROUP BY pf.number, pf.Name, pf.cup, pf.Team
ORDER BY pf.cup, pf.Name