// 基金排名系统

function calculateFundRankings(metrics) {
    const funds = Object.values(metrics);
    
    // 收益排名
    const returnRanking = [...funds].sort((a, b) => 
        parseFloat(b.年化收益率) - parseFloat(a.年化收益率)
    );
    
    // 夏普比率排名
    const sharpeRanking = [...funds].sort((a, b) => 
        parseFloat(b.夏普比率) - parseFloat(a.夏普比率)
    );
    
    // Sortino排名
    const sortinoRanking = [...funds].sort((a, b) => 
        parseFloat(b.Sortino比率) - parseFloat(a.Sortino比率)
    );
    
    // Calmar排名
    const calmarRanking = [...funds].sort((a, b) => 
        parseFloat(b.Calmar比率) - parseFloat(a.Calmar比率)
    );
    
    // 最大回撤排名（回撤越小越好）
    const drawdownRanking = [...funds].sort((a, b) => 
        parseFloat(a.最大回撤) - parseFloat(b.最大回撤)
    );
    
    // 波动率排名（波动率越小越好）
    const volatilityRanking = [...funds].sort((a, b) => 
        parseFloat(a.年化波动率) - parseFloat(b.年化波动率)
    );
    
    return {
        returnRanking,
        sharpeRanking,
        sortinoRanking,
        calmarRanking,
        drawdownRanking,
        volatilityRanking
    };
}

// 基金评级
function getFundGrade(fund) {
    const annRet = parseFloat(fund.年化收益率) || 0;
    constannVol = parseFloat(fund.年化波动率) || 0;
    const sharpe = parseFloat(fund.夏普比率) || 0;
    const drawdown = parseFloat(fund.最大回撤) || 0;
    
    let score = 0;
    
    // 收益评分（30分）
    if (annRet > 0.20) score += 30;
    else if (annRet > 0.15) score += 25;
    else if (annRet > 0.10) score += 20;
    else if (annRet > 0.05) score += 15;
    else if (annRet > 0) score += 10;
    
    // 夏普比率评分（30分）
    if (sharpe > 1.5) score += 30;
    else if (sharpe > 1.2) score += 25;
    else if (sharpe > 0.8) score += 20;
    else if (sharpe > 0.4) score += 15;
    else if (sharpe > 0) score += 10;
    
    // 回撤控制评分（20分）
    if (drawdown < 0.15) score += 20;
    else if (drawdown < 0.20) score += 18;
    else if (drawdown < 0.25) score += 15;
    else if (drawdown < 0.30) score += 12;
    else if (drawdown < 0.40) score += 8;
    
    // 波动率评分（20分）
    if (annVol < 0.10) score += 20;
    else if (annVol < 0.15) score += 18;
    else if (annVol < 0.20) score += 15;
    else if (annVol < 0.25) score += 12;
    
    // 等级
    if (score >= 85) return { grade: 'A', level: 'Excellent', color: '#2ed573' };
    if (score >= 70) return { grade: 'B', level: 'Good', color: '#ffa502' };
    if (score >= 55) return { grade: 'C', level: 'Average', color: '#1e90ff' };
    if (score >= 40) return { grade: 'D', level: 'Warning', color: '#ff4757' };
    return { grade: 'F', level: 'Critical', color: '#880e4f' };
}

// 基金分类
function classifyFund(fund) {
    const annRet = parseFloat(fund.年化收益率) || 0;
    const annVol = parseFloat(fund.年化波动率) || 0;
    const sharpe = parseFloat(fund.夏普比率) || 0;
    
    if (annVol < 0.10 && sharpe > 1.0) {
        return { type: 'Stable', label: '稳健型', color: '#2ed573' };
    } else if (annVol < 0.15 && sharpe > 0.8) {
        return { type: 'Balanced', label: '平衡型', color: '#1e90ff' };
    } else if (annVol < 0.20 && annRet > 0.10) {
        return { type: 'Aggressive', label: '进取型', color: '#ffa502' };
    } else if (annRet > 0.15 || annVol > 0.25) {
        return { type: 'VeryAggressive', label: '高进取型', color: '#ff4757' };
    } else {
        return { type: 'Mixed', label: '混合型', color: '#94a3b8' };
    }
}

// 高风险预警
function checkRiskAlerts(funds) {
    const alerts = [];
    
    funds.forEach(fund => {
        const annVol = parseFloat(fund.年化波动率) || 0;
        const drawdown = parseFloat(fund.最大回撤) || 0;
        
        if (annVol > 0.25) {
            alerts.push({ type: 'high_volatility', fund: fund, message: `${fund.持仓简称} 波动率过高 (${(annVol*100).toFixed(1)}%)` });
        }
        
        if (drawdown > 0.35) {
            alerts.push({ type: 'large_drawdown', fund: fund, message: `${fund.持仓简称} 回撤过大 (${(drawdown*100).toFixed(1)}%)` });
        }
        
        if (annVol > 0.20 && drawdown > 0.25) {
            alerts.push({ type: 'double_risk', fund: fund, message: `${fund.持仓简称} 高波动+大回撤` });
        }
    });
    
    return alerts;
}

// 基金组合分析
function analyzePortfolio(metrics) {
    const funds = Object.values(metrics);
    
    // 计算组合加权指标（假设等权重）
    const avgReturn = funds.reduce((sum, f) => sum + (parseFloat(f.年化收益率) || 0), 0) / funds.length;
    const avgSharpe = funds.reduce((sum, f) => sum + (parseFloat(f.夏普比率) || 0), 0) / funds.length;
    const avgSortino = funds.reduce((sum, f) => sum + (parseFloat(f.Sortino比率) || 0), 0) / funds.length;
    
    // 组合评级
    let grade;
    if (avgReturn > 0.15 && avgSharpe > 1.0) grade = 'Excellent';
    else if (avgReturn > 0.10 && avgSharpe > 0.8) grade = 'Good';
    else if (avgReturn > 0.05 && avgSharpe > 0.5) grade = 'Average';
    else grade = 'NeedsImprovement';
    
    return {
        avgReturn,
        avgSharpe,
        avgSortino,
        grade,
        fundCount: funds.length,
        types: [...new Set(funds.map(f => f.类型))],
        bestFund: funds.reduce((a, b) => (parseFloat(a.年化收益率) > parseFloat(b.年化收益率)) ? a : b),
        worstFund: funds.reduce((a, b) => (parseFloat(a.年化收益率) < parseFloat(b.年化收益率)) ? a : b),
        highestRiskFund: funds.reduce((a, b) => (parseFloat(a.年化波动率) > parseFloat(b.年化波动率)) ? a : b)
    };
}

// 动态范围标记
function getPerformanceBadge(fund) {
    const annRet = parseFloat(fund.年化收益率) || 0;
    
    if (annRet > 0.30) return { text: '⭐⭐⭐', color: '#ffa502' };
    if (annRet > 0.20) return { text: '⭐⭐', color: '#2ed573' };
    if (annRet > 0.10) return { text: '⭐', color: '#1e90ff' };
    if (annRet > 0) return { text: '✓', color: '#94a3b8' };
    return { text: '⚠️', color: '#ff4757' };
}

// 波动率分级
function getVolatilityLevel(vol) {
    if (vol < 0.10) return { level: '低', color: '#2ed573', bg: 'rgba(46,213,115,0.2)' };
    if (vol < 0.15) return { level: '中低', color: '#2ed573', bg: 'rgba(46,213,115,0.1)' };
    if (vol < 0.20) return { level: '中', color: '#ffa502', bg: 'rgba(255,165,2,0.2)' };
    if (vol < 0.25) return { level: '中高', color: '#ff4757', bg: 'rgba(255,71,87,0.2)' };
    return { level: '高', color: '#ff4757', bg: 'rgba(255,71,87,0.3)' };
}

// 夏普比率分级
function getSharpeLevel(sharpe) {
    if (sharpe > 1.5) return { level: '优秀', color: '#2ed573', bg: 'rgba(46,213,115,0.2)' };
    if (sharpe > 1.0) return { level: '良好', color: '#1e90ff', bg: 'rgba(30,144,255,0.2)' };
    if (sharpe > 0.5) return { level: '一般', color: '#ffa502', bg: 'rgba(255,165,2,0.2)' };
    if (sharpe > 0) return { level: '较差', color: '#ff4757', bg: 'rgba(255,71,87,0.2)' };
    return { level: '风险高', color: '#880e4f', bg: 'rgba(136,14,79,0.2)' };
}

// 累计收益等级
function getCumulativeReturnLevel(cumRet) {
    if (cumRet > 2.0) return { text: '🏆 压倒性胜利', color: '#ffa502' };
    if (cumRet > 1.0) return { text: '✅ 优秀表现', color: '#2ed573' };
    if (cumRet > 0.5) return { text: '✓ 良好收益', color: '#1e90ff' };
    if (cumRet > 0) return { text: '✓ 正收益', color: '#94a3b8' };
    return { text: '⚠️ 亏损', color: '#ff4757' };
}
