SELECT
    TradingPair,
    TimeFrame,
    COUNT(*) AS TotalPredictions,
    AVG(Stake) AS AverageStake,
    AVG(Payout) AS AveragePayout,
    MIN(Stake) AS MinStake,
    MAX(Stake) AS MaxStake,
    SUM(CASE WHEN TrueValue = PredictedValue THEN 1 ELSE 0 END) AS SuccessfulPredictions
FROM predictoor
GROUP BY TradingPair, TimeFrame;